# 遷移指南（v1 到 v2）

## 摘要

- **對於 v1.2 或更早版本的使用者**：升級至 v1.4 並使用知識庫（KB）重新建立您的機器人。在轉換期間，確認一切使用 KB 運作正常後，再升級到 v2。
- **對於 v1.3 的使用者**：即使您已經在使用 KB，也**強烈建議**升級到 v1.4 並重新建立您的機器人。如果您仍在使用 pgvector，請在 v1.4 中使用 KB 重新建立機器人以進行遷移。
- **對於希望繼續使用 pgvector 的使用者**：如果您打算繼續使用 pgvector，則不建議升級到 v2。升級到 v2 將刪除所有與 pgvector 相關的資源，並且未來將不再提供支援。在這種情況下，請繼續使用 v1。
- 請注意，**升級到 v2 將導致刪除所有 Aurora 相關的資源。**未來的更新將專注於 v2，v1 將被棄用。

## 簡介

### 將會發生什麼事

v2 更新通過用 [Amazon Bedrock 知識庫](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) 取代 Aurora Serverless 和基於 ECS 的嵌入，引入了一個重大變更。這個變更是不向後兼容的。

### 為什麼此儲存庫採用知識庫並停止使用 pgvector

這個變更有幾個原因：

#### 改善 RAG 準確性

- 知識庫使用 OpenSearch Serverless 作為後端，允許混合搜尋，包括全文和向量搜尋。這導致在回應包含專有名詞的問題時更加準確，而 pgvector 在這方面表現較差。
- 它還支持更多改善 RAG 準確性的選項，如高級分塊和解析。
- 截至 2024 年 10 月，知識庫已普遍可用近一年，並已添加網路爬蟲等功能。預期未來更新將使採用高級功能變得更加容易。例如，儲存庫在 pgvector 中尚未實現從現有 S3 儲存桶匯入（一個經常被請求的功能），但在知識庫中已經支援。

#### 維護

- 目前的 ECS + Aurora 設置依賴於許多庫，包括用於 PDF 解析、網路爬蟲和提取 YouTube 字幕的庫。相比之下，像知識庫這樣的託管解決方案可以減少使用者和儲存庫開發團隊的維護負擔。

## 遷移流程（摘要）

我們強烈建議在遷移至 v2 之前先升級到 v1.4。在 v1.4 中，您可以同時使用 pgvector 和知識庫機器人，這允許您有一個過渡期來重新建立現有的 pgvector 機器人到知識庫中，並驗證它們是否如預期運作。即使 RAG 文件保持不變，請注意由於後端變更到 OpenSearch 可能會產生略微不同的結果，儘管通常相似，這是由於 k-NN 演算法等差異造成的。

通過在 `cdk.json` 中將 `useBedrockKnowledgeBasesForRag` 設定為 true，您可以使用知識庫建立機器人。但是，pgvector 機器人將變為唯讀，防止建立或編輯新的 pgvector 機器人。

![](../imgs/v1_to_v2_readonly_bot.png)

在 v1.4 中，[Amazon Bedrock 的守護規則](https://aws.amazon.com/jp/bedrock/guardrails/) 也被引入。由於知識庫的區域限制，上傳文件的 S3 儲存桶必須與 `bedrockRegion` 在同一個區域。我們建議在更新前備份現有的文件儲存桶，以避免之後需要手動上傳大量文件（因為 S3 儲存桶匯入功能可用）。

## 遷移流程（詳細說明）

根據您是使用 v1.2 或更早版本，還是 v1.3，步驟會有所不同。

![](../imgs/v1_to_v2_arch.png)

### 針對 v1.2 或更早版本的使用者

1. **備份現有的文件儲存桶（可選但建議）。** 如果您的系統已經在運作，我們強烈建議執行此步驟。備份名為 `bedrockchatstack-documentbucketxxxx-yyyy` 的儲存桶。例如，我們可以使用 [AWS 備份](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)。

2. **更新至 v1.4**：取得最新的 v1.4 標籤，修改 `cdk.json`，並部署。按照以下步驟進行：

   1. 取得最新標籤：
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. 按照以下方式修改 `cdk.json`：
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

3. **重新建立您的機器人**：在知識庫上重新建立具有相同定義（文件、區塊大小等）的機器人，就像 pgvector 機器人一樣。如果您有大量文件，則使用步驟 1 中的備份將使此過程更加容易。要還原，我們可以使用跨區域複製還原。更多詳細資訊，請訪問[此處](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)。要指定還原的儲存桶，請按照以下方式設置 `S3 資料來源` 部分。路徑結構為 `s3://<bucket-name>/<user-id>/<bot-id>/documents/`。您可以在 Cognito 使用者池和機器人建立畫面的網址列上查看使用者 ID 和機器人 ID。

![](../imgs/v1_to_v2_KB_s3_source.png)

**請注意，某些功能在知識庫中不可用，如網路爬蟲和 YouTube 字幕支持（計劃支持網路爬蟲（[議題](https://github.com/aws-samples/bedrock-claude-chat/issues/557)）)）。另外，請記住，在遷移期間，使用知識庫將同時產生 Aurora 和知識庫的費用。**

4. **移除已發佈的 API**：由於 VPC 刪除，所有先前發佈的 API 都需要在部署 v2 之前重新發佈。要執行此操作，您需要先刪除現有的 API。使用[管理員的 API 管理功能](../ADMINISTRATOR_zh-TW.md)可以簡化此過程。一旦所有 `APIPublishmentStackXXXX` CloudFormation 堆疊刪除完成，環境就準備就緒了。

5. **部署 v2**：發佈 v2 後，取得標記的原始碼並按如下方式部署（一旦發佈將成為可能）：
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!警告]
> 部署 v2 後，**所有前綴為 [不支持，唯讀] 的機器人將被隱藏。** 確保在升級前重新建立必要的機器人，以避免失去存取權。

> [!提示]
> 在堆疊更新期間，您可能會遇到重複的訊息：資源處理程序返回訊息："子網路 'subnet-xxx' 有依賴關係，無法刪除。" 在這種情況下，導航至管理控制台 > EC2 > 網路介面，並搜尋 BedrockChatStack。刪除與此名稱相關的顯示介面，以幫助確保更順暢的部署流程。

### 針對 v1.3 的使用者

如前所述，在 v1.4 中，由於區域限制，知識庫必須在 bedrockRegion 中建立。因此，您將需要重新建立知識庫。如果您已在 v1.3 中測試知識庫，請在 v1.4 中使用相同的定義重新建立機器人。按照針對 v1.2 使用者概述的步驟進行。