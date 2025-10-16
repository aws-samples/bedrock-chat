# 마이그레이션 가이드 (v1에서 v2로)

## 요약

- **v1.2 이하 버전 사용자**: v1.4로 업그레이드하고 Knowledge Base(KB)를 사용하여 봇을 다시 생성하세요. 전환 기간 후 KB로 모든 것이 정상 작동하는 것을 확인한 다음 v2로 업그레이드를 진행하세요.
- **v1.3 사용자**: 이미 KB를 사용 중이더라도 v1.4로 업그레이드하고 봇을 다시 생성하는 것을 **강력히 권장**합니다. 아직 pgvector를 사용 중이라면 v1.4에서 KB를 사용하여 봇을 다시 생성하여 마이그레이션하세요.
- **pgvector를 계속 사용하고자 하는 사용자**: pgvector를 계속 사용할 계획이라면 v2로의 업그레이드는 권장되지 않습니다. v2로 업그레이드하면 pgvector 관련 모든 리소스가 제거되며, 향후 지원도 더 이상 제공되지 않습니다. 이 경우 v1을 계속 사용하세요.
- **v2로 업그레이드하면 모든 Aurora 관련 리소스가 삭제된다**는 점에 유의하세요. 향후 업데이트는 v2에만 집중될 것이며, v1은 더 이상 사용되지 않습니다.

## 소개

### 예정된 변경사항

v2 업데이트에서는 Aurora Serverless와 ECS 기반 임베딩을 [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)로 대체하는 중요한 변경이 있습니다. 이 변경은 이전 버전과 호환되지 않습니다.

### 이 리포지토리가 Knowledge Bases를 채택하고 pgvector를 중단한 이유

이러한 변경에는 여러 이유가 있습니다:

#### RAG 정확도 향상

- Knowledge Bases는 OpenSearch Serverless를 백엔드로 사용하여 전문 검색과 벡터 검색을 모두 지원하는 하이브리드 검색이 가능합니다. 이를 통해 pgvector가 어려움을 겪었던 고유명사가 포함된 질문에 대한 응답의 정확도가 향상됩니다.
- 또한 고급 청킹 및 구문 분석과 같은 RAG 정확도 향상을 위한 더 많은 옵션을 제공합니다.
- Knowledge Bases는 2024년 10월 기준으로 웹 크롤링과 같은 기능이 이미 추가된 상태로 거의 1년 동안 일반 공개되어 왔습니다. 향후 업데이트가 예상되어 장기적으로 고급 기능을 더 쉽게 도입할 수 있습니다. 예를 들어, 이 리포지토리는 pgvector에서 자주 요청되던 기능인 기존 S3 버킷에서의 가져오기를 구현하지 않았지만, KB(KnowledgeBases)에서는 이미 지원되고 있습니다.

#### 유지보수

- 현재의 ECS + Aurora 설정은 PDF 파싱, 웹 크롤링, YouTube 자막 추출을 위한 다양한 라이브러리에 의존합니다. 이에 비해 Knowledge Bases와 같은 관리형 솔루션은 사용자와 리포지토리 개발팀 모두의 유지보수 부담을 줄여줍니다.

## 마이그레이션 프로세스 (요약)

v2로 이전하기 전에 v1.4로 업그레이드하는 것을 강력히 권장합니다. v1.4에서는 pgvector와 Knowledge Base 봇을 모두 사용할 수 있어, 기존 pgvector 봇을 Knowledge Base로 재생성하고 정상 작동하는지 확인할 수 있는 전환 기간을 가질 수 있습니다. RAG 문서가 동일하더라도 k-NN 알고리즘과 같은 차이로 인해 OpenSearch로의 백엔드 변경으로 약간 다른 결과가 나올 수 있지만, 일반적으로는 비슷합니다.

`cdk.json`에서 `useBedrockKnowledgeBasesForRag`를 true로 설정하면 Knowledge Bases를 사용하여 봇을 생성할 수 있습니다. 하지만 pgvector 봇은 읽기 전용이 되어 새로운 pgvector 봇의 생성이나 편집이 불가능해집니다.

![](../imgs/v1_to_v2_readonly_bot.png)

v1.4에서는 [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/)도 도입되었습니다. Knowledge Bases의 지역 제한으로 인해 문서 업로드를 위한 S3 버킷은 `bedrockRegion`과 동일한 리전에 있어야 합니다. S3 버킷 가져오기 기능이 제공되므로, 나중에 대량의 문서를 수동으로 업로드하는 것을 피하기 위해 업데이트 전에 기존 문서 버킷을 백업하는 것을 권장합니다.

## 마이그레이션 프로세스 (상세)

v1.2 이하 버전을 사용하는지 또는 v1.3을 사용하는지에 따라 단계가 다릅니다.

![](../imgs/v1_to_v2_arch.png)

### v1.2 이하 버전 사용자를 위한 단계

1. **기존 문서 버킷 백업(선택 사항이나 권장됨).** 시스템이 이미 운영 중인 경우 이 단계를 강력히 권장합니다. `bedrockchatstack-documentbucketxxxx-yyyy`라는 이름의 버킷을 백업하십시오. 예를 들어, [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)을 사용할 수 있습니다.

2. **v1.4로 업데이트**: 최신 v1.4 태그를 가져오고, `cdk.json`을 수정한 후 배포하십시오. 다음 단계를 따르세요:

   1. 최신 태그 가져오기:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. `cdk.json`을 다음과 같이 수정:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. 변경사항 배포:
      ```bash
      npx cdk deploy
      ```

3. **봇 재생성**: Knowledge Base에서 pgvector 봇과 동일한 정의(문서, 청크 크기 등)로 봇을 재생성하십시오. 문서 양이 많은 경우, 1단계에서 생성한 백업에서 복원하면 이 과정이 더 쉬워집니다. 복원하려면 교차 리전 복사본 복원을 사용할 수 있습니다. 자세한 내용은 [여기](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)를 참조하십시오. 복원된 버킷을 지정하려면 `S3 Data Source` 섹션을 다음과 같이 설정하십시오. 경로 구조는 `s3://<bucket-name>/<user-id>/<bot-id>/documents/`입니다. 사용자 ID는 Cognito 사용자 풀에서, 봇 ID는 봇 생성 화면의 주소 표시줄에서 확인할 수 있습니다.

![](../imgs/v1_to_v2_KB_s3_source.png)

**웹 크롤링 및 YouTube 트랜스크립트 지원과 같은 일부 기능은 Knowledge Bases에서 사용할 수 없습니다(웹 크롤러 지원 계획 중 ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** 또한 전환 기간 동안 Aurora와 Knowledge Bases 모두에 대한 요금이 발생한다는 점을 유의하십시오.

4. **게시된 API 제거**: VPC 삭제로 인해 v2를 배포하기 전에 이전에 게시된 모든 API를 다시 게시해야 합니다. 이를 위해 기존 API를 먼저 삭제해야 합니다. [관리자의 API 관리 기능](../ADMINISTRATOR_ko-KR.md)을 사용하면 이 과정을 단순화할 수 있습니다. 모든 `APIPublishmentStackXXXX` CloudFormation 스택 삭제가 완료되면 환경이 준비됩니다.

5. **v2 배포**: v2가 출시된 후, 태그된 소스를 가져와 다음과 같이 배포하십시오(출시 후 가능):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> v2 배포 후, **[Unsupported, Read-only] 접두사가 있는 모든 봇은 숨겨집니다.** 접근 손실을 방지하기 위해 업그레이드 전에 필요한 봇을 재생성하십시오.

> [!Tip]
> 스택 업데이트 중에 "Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted."와 같은 메시지가 반복적으로 표시될 수 있습니다. 이런 경우, Management Console > EC2 > 네트워크 인터페이스로 이동하여 BedrockChatStack을 검색하십시오. 이 이름과 관련된 표시된 인터페이스를 삭제하면 더 원활한 배포 과정에 도움이 됩니다.

### v1.3 사용자를 위한 단계

앞서 언급했듯이, v1.4에서는 지역 제한으로 인해 Knowledge Bases를 bedrockRegion에 생성해야 합니다. 따라서 KB를 재생성해야 합니다. v1.3에서 이미 KB를 테스트한 경우, v1.4에서 동일한 정의로 봇을 재생성하십시오. v1.2 사용자를 위한 단계를 따르십시오.