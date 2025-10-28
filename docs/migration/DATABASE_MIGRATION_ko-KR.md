# 데이터베이스 마이그레이션 가이드

> [!Warning]
> 이 가이드는 v0에서 v1로의 마이그레이션을 위한 것입니다.

이 가이드는 Aurora 클러스터 교체가 포함된 Bedrock Chat 업데이트를 수행할 때 데이터를 마이그레이션하는 단계를 설명합니다. 다음 절차는 다운타임과 데이터 손실을 최소화하면서 원활한 전환을 보장합니다.

## 개요

마이그레이션 프로세스는 모든 봇을 스캔하고 각각에 대해 임베딩 ECS 작업을 실행하는 것을 포함합니다. 이 접근 방식은 임베딩의 재계산이 필요하며, 이는 시간이 많이 소요되고 ECS 작업 실행과 Bedrock Cohere 사용 요금으로 인한 추가 비용이 발생할 수 있습니다. 이러한 비용과 시간 요구사항을 피하고 싶으시다면, 이 가이드의 후반부에 제공되는 [대체 마이그레이션 옵션](#alternative-migration-options)을 참조해 주시기 바랍니다.

## 마이그레이션 단계

- Aurora 교체와 함께 [npx cdk deploy](../README.md#deploy-using-cdk)를 실행한 후, [migrate_v0_v1.py](./migrate_v0_v1.py) 스크립트를 열어 다음 변수들을 적절한 값으로 업데이트하세요. 이 값들은 `CloudFormation` > `BedrockChatStack` > `Outputs` 탭에서 확인할 수 있습니다.

```py
# AWS Management Console에서 CloudFormation 스택을 열고 Outputs 탭에서 값들을 복사하세요.
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 변경할 필요 없음
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- `migrate_v0_v1.py` 스크립트를 실행하여 마이그레이션 프로세스를 시작하세요. 이 스크립트는 모든 봇을 스캔하고, 임베딩 ECS 태스크를 실행하며, 새로운 Aurora 클러스터에 데이터를 생성합니다. 다음 사항에 주의하세요:
  - 이 스크립트는 `boto3`가 필요합니다.
  - 환경에는 dynamodb 테이블에 접근하고 ECS 태스크를 호출하기 위한 IAM 권한이 필요합니다.

## 대체 마이그레이션 옵션

위의 방법이 소요 시간과 비용 문제로 적합하지 않다면, 다음과 같은 대체 접근 방식을 고려해보세요:

### 스냅샷 복원 및 DMS 마이그레이션

먼저, 현재 Aurora 클러스터의 접속 비밀번호를 기록해두세요. 그런 다음 `npx cdk deploy`를 실행하면 클러스터가 교체됩니다. 이후 원본 데이터베이스의 스냅샷에서 복원하여 임시 데이터베이스를 생성하세요.
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)를 사용하여 임시 데이터베이스에서 새로운 Aurora 클러스터로 데이터를 마이그레이션하세요.

참고: 2024년 5월 29일 기준으로 DMS는 pgvector 확장을 기본적으로 지원하지 않습니다. 하지만 이 제한을 해결하기 위해 다음과 같은 옵션을 고려할 수 있습니다:

[DMS 동종 마이그레이션](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)을 사용하세요. 이는 네이티브 논리적 복제를 활용합니다. 이 경우 소스와 대상 데이터베이스 모두 PostgreSQL이어야 합니다. DMS는 이를 위해 네이티브 논리적 복제를 활용할 수 있습니다.

가장 적합한 마이그레이션 방식을 선택할 때는 프로젝트의 특정 요구사항과 제약사항을 고려하세요.