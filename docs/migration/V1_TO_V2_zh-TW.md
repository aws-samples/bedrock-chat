# 遷移指南 (v1 至 v2)

## 重點摘要

- **v1.2 或更早版本的使用者**：請升級到 v1.4 並使用 Knowledge Base (KB) 重新建立您的機器人。在過渡期間，一旦確認 KB 運作正常，再進行 v2 的升級。
- **v1.3 的使用者**：即使您已在使用 KB，**強烈建議**升級到 v1.4 並重新建立機器人。如果您仍在使用 pgvector，請透過在 v1.4 中使用 KB 重新建立機器人來進行遷移。
- **希望繼續使用 pgvector 的使用者**：如果您計劃繼續使用 pgvector，不建議升級到 v2。升級到 v2 將移除所有與 pgvector 相關的資源，且未來將不再提供支援。在這種情況下，請繼續使用 v1。
- 請注意，**升級到 v2 將導致所有 Aurora 相關資源被刪除。**未來的更新將專注於 v2，v1 將被棄用。

## 簡介

### 將會發生什麼

v2 更新引入了一項重大變更，將 Aurora Serverless 上的 pgvector 和基於 ECS 的嵌入替換為 [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)。此變更不向後相容。

### 為什麼本專案採用 Knowledge Bases 並停用 pgvector

這項變更有幾個原因：

#### 改善 RAG 準確度

- Knowledge Bases 使用 OpenSearch Serverless 作為後端，允許同時進行全文和向量搜索的混合搜索。這提高了回答包含專有名詞問題的準確度，這是 pgvector 過去較為困難的部分。
- 它還支援更多選項來提升 RAG 準確度，例如進階分塊和解析。
- Knowledge Bases 自 2024 年 10 月起已經全面可用近一年，並已新增了網頁爬蟲等功能。預期未來會有更多更新，使長期採用進階功能變得更容易。例如，雖然本專案尚未在 pgvector 中實現從現有 S3 儲存桶匯入（一個經常被要求的功能），但 KB (KnowledgeBases) 已經支援此功能。

#### 維護

- 目前的 ECS + Aurora 設置依賴於許多函式庫，包括用於 PDF 解析、網頁爬蟲和擷取 YouTube 字幕的函式庫。相比之下，像 Knowledge Bases 這樣的受管理解決方案可以減輕使用者和專案開發團隊的維護負擔。

## 遷移流程（摘要）

我們強烈建議在升級到 v2 之前先升級到 v1.4。在 v1.4 中，您可以同時使用 pgvector 和 Knowledge Base 機器人，這提供了一段過渡期來重新建立現有的 pgvector 機器人到 Knowledge Base 並驗證其功能是否符合預期。即使 RAG 文件保持相同，由於後端改用 OpenSearch 以及 k-NN 演算法等差異，可能會產生略微不同但大致相似的結果。

透過在 `cdk.json` 中將 `useBedrockKnowledgeBasesForRag` 設定為 true，您可以使用 Knowledge Bases 建立機器人。但是，pgvector 機器人將變成唯讀模式，無法建立或編輯新的 pgvector 機器人。

![](../imgs/v1_to_v2_readonly_bot.png)

在 v1.4 中，也引入了 [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/)。由於 Knowledge Bases 的區域限制，用於上傳文件的 S3 儲存桶必須與 `bedrockRegion` 位於相同區域。我們建議在更新之前備份現有的文件儲存桶，以避免之後需要手動上傳大量文件（因為有 S3 儲存桶匯入功能可用）。

## 遷移程序（詳細）

根據您使用的是 v1.2 或更早版本，還是 v1.3，步驟會有所不同。

![](../imgs/v1_to_v2_arch.png)

### v1.2 或更早版本使用者的步驟

1. **備份現有的文件儲存桶（選擇性但建議）。** 如果您的系統已在運作中，我們強烈建議執行此步驟。備份名為 `bedrockchatstack-documentbucketxxxx-yyyy` 的儲存桶。例如，我們可以使用 [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)。

2. **更新至 v1.4**：取得最新的 v1.4 標籤，修改 `cdk.json`，並部署。請依照以下步驟：

   1. 取得最新標籤：
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. 修改 `cdk.json` 如下：
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. 部署變更：
      ```bash
      npx cdk deploy
      ```

3. **重新建立您的聊天機器人**：在 Knowledge Base 上使用與 pgvector 機器人相同的定義（文件、區塊大小等）重新建立您的聊天機器人。如果您有大量文件，從步驟 1 的備份還原將使此過程更容易。要還原，我們可以使用跨區域複製還原。詳細資訊請參閱[這裡](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)。要指定還原的儲存桶，請按照以下方式設定 `S3 Data Source` 部分。路徑結構為 `s3://<bucket-name>/<user-id>/<bot-id>/documents/`。您可以在 Cognito 使用者池查看使用者 ID，在機器人建立畫面的網址列查看機器人 ID。

![](../imgs/v1_to_v2_KB_s3_source.png)

**請注意，某些功能在 Knowledge Bases 上不可用，例如網頁爬蟲和 YouTube 字幕支援（計劃支援網頁爬蟲 ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))）。** 另外，請記住，在過渡期間使用 Knowledge Bases 將同時產生 Aurora 和 Knowledge Bases 的費用。

4. **移除已發布的 API**：由於 VPC 刪除，所有先前發布的 API 都需要在部署 v2 之前重新發布。為此，您需要先刪除現有的 API。使用[管理員的 API 管理功能](../ADMINISTRATOR_zh-TW.md)可以簡化此過程。一旦所有 `APIPublishmentStackXXXX` CloudFormation 堆疊刪除完成，環境就準備就緒了。

5. **部署 v2**：v2 發布後，取得標記的原始碼並按如下方式部署（一旦發布後即可執行）：
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> 部署 v2 後，**所有帶有 [Unsupported, Read-only] 前綴的聊天機器人都將被隱藏。** 請確保在升級前重新建立必要的聊天機器人，以避免失去存取權限。

> [!Tip]
> 在堆疊更新期間，您可能會遇到重複的訊息，如：Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." 在這種情況下，請前往 Management Console > EC2 > Network Interfaces 並搜尋 BedrockChatStack。刪除與此名稱相關聯的顯示介面，以確保部署過程更順暢。

### v1.3 使用者的步驟

如前所述，在 v1.4 中，由於區域限制，Knowledge Bases 必須在 bedrockRegion 中建立。因此，您需要重新建立 KB。如果您已經在 v1.3 中測試了 KB，請在 v1.4 中使用相同的定義重新建立聊天機器人。請按照 v1.2 使用者的步驟進行操作。