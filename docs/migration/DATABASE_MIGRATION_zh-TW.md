# 資料庫遷移指南

本指南概述了在執行 Bedrock Claude Chat 更新（包含 Aurora 叢集替換）時遷移資料的步驟。以下程序確保在最小化停機時間和資料遺失的情況下進行順暢的過渡。

## 概述

遷移過程涉及掃描所有機器人並為每個機器人啟動嵌入式 ECS 任務。這種方法需要重新計算嵌入，可能會耗費時間，並因 ECS 任務執行和 Bedrock Cohere 使用費而產生額外成本。如果您希望避免這些成本和時間要求，請參閱本指南稍後提供的[替代遷移選項](#alternative-migration-options)。

## 遷移步驟

- 在執行 [npx cdk deploy](../README.md#deploy-using-cdk) 替換 Aurora 後，開啟 [migrate.py](./migrate.py) 腳本並使用適當的值更新以下變數。這些值可以在 `CloudFormation` > `BedrockChatStack` > `Outputs` 標籤中找到。

```py
# 在 AWS 管理控制台中開啟 CloudFormation 堆疊，並從 Outputs 標籤複製值。
# 金鑰：DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# 金鑰：EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# 金鑰：EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 無需更改
# 金鑰：PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# 金鑰：EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 執行 `migrate.py` 腳本以啟動遷移流程。此腳本將掃描所有機器人，啟動嵌入 ECS 任務，並將資料建立到新的 Aurora 叢集。請注意：
  - 腳本需要 `boto3`。
  - 環境需要 IAM 權限以存取 DynamoDB 表格並調用 ECS 任務。

## 替代遷移選項

如果您由於相關的時間和成本考量而不想使用上述方法，可以考慮以下替代方法：

### 快照還原和 DMS 遷移

首先，記下訪問當前 Aurora 叢集的密碼。然後執行 `npx cdk deploy`，這將觸發叢集的替換。之後，透過從原始資料庫的快照還原來建立一個臨時資料庫。
使用 [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) 將資料從臨時資料庫遷移到新的 Aurora 叢集。

注意：截至 2024 年 5 月 29 日，DMS 尚不原生支援 pgvector 擴充套件。不過，您可以探索以下選項來解決此限制：

使用 [DMS 同質遷移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，該方法利用原生邏輯複寫。在這種情況下，來源和目標資料庫都必須是 PostgreSQL。DMS 可以為此目的利用原生邏輯複寫。

在選擇最適合的遷移方法時，請考慮您專案的具體需求和限制。