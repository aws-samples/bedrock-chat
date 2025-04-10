# 마이그레이션 가이드 (v1에서 v2로)

## 요약

- **v1.2 이하 버전 사용자**: v1.4로 업그레이드하고 Knowledge Base (KB)를 사용하여 봇을 다시 생성하세요. 전환 기간 후, 모든 것이 KB와 함께 예상대로 작동하는지 확인한 후 v2로 업그레이드하세요.
- **v1.3 사용자**: 이미 KB를 사용하고 있더라도 v1.4로 업그레이드하고 봇을 다시 생성하는 것이 **강력히 권장**됩니다. pgvector를 계속 사용 중이라면, v1.4의 KB를 사용하여 봇을 다시 생성하여 마이그레이션하세요.
- **pgvector 계속 사용을 원하는 사용자**: pgvector를 계속 사용할 계획이라면 v2로 업그레이드하는 것은 권장되지 않습니다. v2로 업그레이드하면 pgvector 관련 모든 리소스가 제거되며 향후 지원이 중단됩니다. 이 경우 v1을 계속 사용하세요.
- **v2로 업그레이드하면 모든 Aurora 관련 리소스가 삭제된다는 점에 유의하세요.** 향후 업데이트는 v2에 집중될 예정이며, v1은 더 이상 사용되지 않을 것입니다.

## 소개

### 무슨 일이 일어날까요

v2 업데이트는 Aurora Serverless와 ECS 기반 임베딩의 pgvector를 [Amazon Bedrock 지식 기반](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)으로 대체함으로써 주요한 변화를 도입합니다. 이 변경은 이전 버전과 호환되지 않습니다.

### 이 저장소가 지식 기반을 채택하고 pgvector를 중단한 이유

이 변경에는 몇 가지 이유가 있습니다:

#### RAG 정확성 향상

- 지식 기반은 OpenSearch Serverless를 백엔드로 사용하여 전체 텍스트와 벡터 검색을 모두 포함하는 하이브리드 검색을 허용합니다. 이는 고유명사를 포함하는 질문에 대해 pgvector가 어려워했던 더 나은 정확성으로 이어집니다.
- 또한 고급 청크 분할 및 구문 분석과 같은 RAG 정확성 개선을 위한 더 많은 옵션을 지원합니다.
- 지식 기반은 2024년 10월 기준으로 거의 1년 동안 일반적으로 사용 가능했으며, 웹 크롤링과 같은 기능이 이미 추가되었습니다. 향후 업데이트로 장기적으로 고급 기능을 채택하기 쉬워질 것으로 예상됩니다. 예를 들어, 이 저장소는 pgvector에서 기존 S3 버킷에서 가져오기와 같은 자주 요청되는 기능을 구현하지 않았지만, KB(지식 기반)에서는 이미 지원됩니다.

#### 유지 관리

- 현재 ECS + Aurora 설정은 PDF 구문 분석, 웹 크롤링, YouTube 트랜스크립트 추출을 포함한 수많은 라이브러리에 의존합니다. 반면에 지식 기반과 같은 관리형 솔루션은 사용자와 저장소 개발팀 모두에 대한 유지 관리 부담을 줄입니다.

## 마이그레이션 프로세스 (요약)

v2로 이동하기 전에 v1.4로 업그레이드하는 것을 강력히 권장합니다. v1.4에서는 pgvector와 Knowledge Base 봇을 모두 사용할 수 있어, 기존 pgvector 봇을 Knowledge Base로 다시 생성하고 예상대로 작동하는지 확인할 수 있는 전환 기간을 제공합니다. RAG 문서가 동일하더라도, OpenSearch에 대한 백엔드 변경으로 인해 k-NN 알고리즘과 같은 차이로 인해 약간 다른 결과가 생성될 수 있습니다. 일반적으로 비슷하지만 주의해야 합니다.

`cdk.json`에서 `useBedrockKnowledgeBasesForRag`를 true로 설정하면 Knowledge Bases를 사용하여 봇을 생성할 수 있습니다. 그러나 pgvector 봇은 읽기 전용이 되어 새로운 pgvector 봇의 생성이나 편집이 불가능해집니다.

![](../imgs/v1_to_v2_readonly_bot.png)

v1.4에서는 [Amazon Bedrock의 가드레일](https://aws.amazon.com/jp/bedrock/guardrails/)도 도입됩니다. Knowledge Bases의 지역 제한으로 인해 문서 업로드용 S3 버킷은 `bedrockRegion`과 동일한 지역에 있어야 합니다. 대량의 문서를 수동으로 다시 업로드하는 것을 방지하기 위해 업데이트 전에 기존 문서 버킷을 백업하는 것을 권장합니다 (S3 버킷 가져오기 기능을 사용할 수 있음).

## 마이그레이션 프로세스 (상세)

버전 1.2 이전 또는 버전 1.3을 사용하는지에 따라 단계가 다릅니다.

![](../imgs/v1_to_v2_arch.png)

### 버전 1.2 이전 사용자를 위한 단계

1. **기존 문서 버킷 백업 (선택 사항이지만 권장됨).** 시스템이 이미 운영 중인 경우 이 단계를 강력히 권장합니다. `bedrockchatstack-documentbucketxxxx-yyyy` 이름의 버킷을 백업하세요. 예를 들어 [AWS 백업](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)을 사용할 수 있습니다.

2. **v1.4로 업데이트**: 최신 v1.4 태그를 가져오고, `cdk.json`을 수정한 후 배포합니다. 다음 단계를 따르세요:

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
   3. 변경 사항 배포:
      ```bash
      npx cdk deploy
      ```

3. **봇 재생성**: 기존 pgvector 봇과 동일한 정의(문서, 청크 크기 등)로 Knowledge Base에 봇을 다시 생성하세요. 문서 볼륨이 큰 경우, 1단계의 백업에서 복원하면 이 과정이 더 쉬워집니다. 복원하려면 교차 리전 복사본 복원을 사용할 수 있습니다. 자세한 내용은 [여기](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)를 참조하세요. 복원된 버킷을 지정하려면 다음과 같이 `S3 데이터 소스` 섹션을 설정하세요. 경로 구조는 `s3://<버킷-이름>/<사용자-ID>/<봇-ID>/documents/`입니다. Cognito 사용자 풀에서 사용자 ID를, 봇 생성 화면의 주소 표시줄에서 봇 ID를 확인할 수 있습니다.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Knowledge Base에서는 웹 크롤링 및 YouTube 트랜스크립트 지원과 같은 일부 기능을 사용할 수 없습니다(웹 크롤러 지원 계획 중 ([이슈](https://github.com/aws-samples/bedrock-chat/issues/557))).** 또한 전환 중에는 Aurora와 Knowledge Base에 대한 요금이 모두 청구됩니다.

4. **게시된 API 제거**: VPC 삭제로 인해 이전에 게시된 모든 API를 v2 배포 전에 다시 게시해야 합니다. 먼저 기존 API를 삭제해야 합니다. [관리자의 API 관리 기능](../ADMINISTRATOR_ko-KR.md)을 사용하면 이 프로세스를 간소화할 수 있습니다. 모든 `APIPublishmentStackXXXX` CloudFormation 스택 삭제가 완료되면 환경이 준비됩니다.

5. **v2 배포**: v2 릴리스 후, 태그가 지정된 소스를 가져오고 다음과 같이 배포합니다 (릴리스되면 가능):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!경고]
> v2를 배포한 후 **[지원되지 않음, 읽기 전용] 접두사가 있는 모든 봇이 숨겨집니다.** 업그레이드 전에 필요한 봇을 다시 생성하여 액세스 손실을 방지하세요.

> [!팁]
> 스택 업데이트 중 "서브넷 'subnet-xxx'에 종속성이 있어 삭제할 수 없습니다."와 같은 반복 메시지가 표시될 수 있습니다. 이 경우 관리 콘솔 > EC2 > 네트워크 인터페이스로 이동하여 BedrockChatStack을 검색하세요. 이 이름과 연결된 표시된 인터페이스를 삭제하면 배포 프로세스가 더 원활해집니다.

### 버전 1.3 사용자를 위한 단계

앞서 언급했듯이 v1.4에서는 지역 제한으로 인해 Knowledge Base를 bedrockRegion에서 생성해야 합니다. 따라서 KB를 다시 생성해야 합니다. v1.3에서 이미 KB를 테스트한 경우 v1.4에서 동일한 정의로 봇을 다시 생성하세요. v1.2 사용자를 위한 단계를 따르세요.