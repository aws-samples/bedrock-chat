# 資料庫遷移指南

> [!Warning]
> 本指南適用於從 v0 到 v1 的遷移。

本指南概述了在執行包含 Aurora 叢集替換的 Bedrock Chat 更新時遷移資料的步驟。以下程序確保平穩過渡，同時將停機時間和資料遺失降至最低。

## 概觀

遷移流程包括掃描所有機器人並為每個機器人啟動嵌入式 ECS 任務。這種方法需要重新計算嵌入，可能會因 ECS 任務執行和 Bedrock Cohere 使用費而耗費大量時間和成本。如果您希望避免這些成本和時間要求，請參考本指南稍後提供的[替代遷移選項](#alternative-migration-options)。

## 遷移步驟

- 在使用 [npx cdk deploy](../README.md#deploy-using-cdk) 替換 Aurora 後，打開 [migrate_v0_v1.py](./migrate_v0_v1.py) 腳本，並使用適當的值更新以下變數。這些值可以在 `CloudFormation` > `BedrockChatStack` > `Outputs` 選項卡中查看。

```py
# 在 AWS 管理控制台中打開 CloudFormation 堆棧，並從 Outputs 選項卡複製值。
# 鍵：DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# 鍵：EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# 鍵：EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 無需更改
# 鍵：PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# 鍵：EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 運行 `migrate_v0_v1.py` 腳本以啟動遷移過程。該腳本將掃描所有機器人，啟動嵌入 ECS 任務，並將數據創建到新的 Aurora 集群。請注意：
  - 該腳本需要 `boto3`。
  - 環境需要 IAM 權限以訪問 dynamodb 表並調用 ECS 任務。

## 替代遷移選項

如果您因時間和成本考量不想使用上述方法，可以考慮以下替代方案：

### 快照還原和 DMS 遷移

首先，記下存取當前 Aurora 叢集的密碼。然後執行 `npx cdk deploy`，這將觸發叢集的替換。之後，從原始資料庫的快照建立一個臨時資料庫。
使用 [AWS 資料庫遷移服務 (DMS)](https://aws.amazon.com/dms/) 將資料從臨時資料庫遷移到新的 Aurora 叢集。

注意：截至 2024 年 5 月 29 日，DMS 尚不原生支援 pgvector 擴充套件。不過，您可以探索以下選項來解決此限制：

使用 [DMS 同質遷移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，該方法利用原生邏輯複寫。在這種情況下，來源和目標資料庫都必須是 PostgreSQL。DMS 可以為此目的利用原生邏輯複寫。

在選擇最適合的遷移方法時，請考慮專案的具體需求和限制。