# 資料庫遷移指南

> [!Warning]
> 本指南適用於從 v0 升級至 v1。

本指南概述了在更新包含 Aurora 集群替換的 Bedrock Chat 時，進行資料遷移的步驟。以下程序確保順利過渡，同時將停機時間和資料損失降至最低。

## 概述

遷移過程涉及掃描所有機器人並為每個機器人啟動嵌入式 ECS 任務。這種方法需要重新計算嵌入向量，這可能會耗費較長時間，並且由於執行 ECS 任務和使用 Bedrock Cohere 而產生額外費用。如果您想避免這些成本和時間消耗，請參考本指南後面提供的[替代遷移選項](#alternative-migration-options)。

## 遷移步驟

- 在使用 Aurora 替換完成 [npx cdk deploy](../README.md#deploy-using-cdk) 後，開啟 [migrate_v0_v1.py](./migrate_v0_v1.py) 腳本並更新以下變數為適當的值。這些值可以在 `CloudFormation` > `BedrockChatStack` > `Outputs` 分頁中找到。

```py
# 在 AWS Management Console 中開啟 CloudFormation 堆疊並從 Outputs 分頁複製這些值。
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 無需更改
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 執行 `migrate_v0_v1.py` 腳本以開始遷移程序。此腳本將掃描所有機器人、啟動嵌入式 ECS 任務，並在新的 Aurora 叢集中建立資料。請注意：
  - 此腳本需要 `boto3`。
  - 執行環境需要具有存取 dynamodb 資料表和調用 ECS 任務的 IAM 權限。

## 替代遷移選項

如果由於時間和成本的考量而不想使用上述方法，可以考慮以下替代方案：

### 快照還原和 DMS 遷移

首先，記下目前 Aurora 叢集的密碼。然後執行 `npx cdk deploy`，這會觸發叢集的替換。之後，透過原始資料庫的快照來建立一個臨時資料庫。
使用 [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) 將資料從臨時資料庫遷移到新的 Aurora 叢集。

注意：截至 2024 年 5 月 29 日，DMS 尚未原生支援 pgvector 擴充功能。不過，您可以探索以下解決方案來克服這個限制：

使用 [DMS 同質遷移](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)，它利用原生邏輯複寫。在這種情況下，來源和目標資料庫都必須是 PostgreSQL。DMS 可以利用原生邏輯複寫來達成這個目的。

在選擇最適合的遷移方法時，請考慮您專案的具體需求和限制。