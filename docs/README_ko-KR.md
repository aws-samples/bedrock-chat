<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


[Amazon Bedrock](https://aws.amazon.com/bedrock/)을 기반으로 한 다국어 생성형 AI 플랫폼입니다.
채팅, 지식 기반 커스텀 봇(RAG), 봇 스토어를 통한 봇 공유, 에이전트를 사용한 작업 자동화를 지원합니다.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3가 출시되었습니다. 업데이트하려면 [마이그레이션 가이드](./migration/V2_TO_V3_ko-KR.md)를 주의 깊게 검토하세요.** 주의하지 않으면 **V2의 봇들이 사용할 수 없게 됩니다.**

### 봇 개인화 / 봇 스토어

자신만의 지시사항과 지식([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/))을 추가할 수 있습니다. 봇은 봇 스토어 마켓플레이스를 통해 애플리케이션 사용자들과 공유할 수 있습니다. 커스터마이즈된 봇은 독립 실행형 API로도 게시할 수 있습니다 ([자세히 보기](./PUBLISH_API_ko-KR.md)).

<details>
<summary>스크린샷</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

기존 [Amazon Bedrock의 KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/)도 가져올 수 있습니다.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> 거버넌스 상의 이유로 허가된 사용자만 커스텀 봇을 생성할 수 있습니다. 커스텀 봇 생성을 허용하려면 사용자가 `CreatingBotAllowed` 그룹의 멤버여야 합니다. 이는 관리 콘솔 > Amazon Cognito User pools 또는 aws cli를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`에서 확인할 수 있습니다.

### 관리 기능

API 관리, 필수 봇 표시, 봇 사용량 분석 [자세히 보기](./ADMINISTRATOR_ko-KR.md)

<details>
<summary>스크린샷</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### 에이전트

[에이전트 기능](./AGENT_ko-KR.md)을 사용하면 챗봇이 더 복잡한 작업을 자동으로 처리할 수 있습니다. 예를 들어, 사용자의 질문에 답하기 위해 에이전트는 외부 도구에서 필요한 정보를 검색하거나 작업을 여러 단계로 나누어 처리할 수 있습니다.

<details>
<summary>스크린샷</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 간편한 배포

- us-east-1 리전에서 [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)를 열고 > `Manage model access` > 사용하고자 하는 모든 모델을 선택한 후 `Save changes`를 클릭하세요.

<details>
<summary>스크린샷</summary>

![](./imgs/model_screenshot.png)

</details>

### 지원되는 리전

봇과 지식 베이스를 사용하려면(OpenSearch Serverless가 기본 선택임) Bedrock Chat을 [OpenSearch Serverless와 Ingestion API를 사용할 수 있는 리전](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html)에 배포해야 합니다. 2025년 8월 기준으로 다음 리전들이 지원됩니다: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

**bedrock-region** 파라미터의 경우 [Bedrock이 사용 가능한 리전](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)을 선택해야 합니다.

- 배포하고자 하는 리전에서 [CloudShell](https://console.aws.amazon.com/cloudshell/home)을 엽니다
- 다음 명령어로 배포를 실행합니다. 배포할 버전을 지정하거나 보안 정책을 적용해야 하는 경우 [선택적 파라미터](#optional-parameters)에서 적절한 파라미터를 지정하세요.

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 새로운 사용자인지 v3 사용자인지 묻는 메시지가 표시됩니다. v0 이전 버전의 기존 사용자가 아닌 경우 `y`를 입력하세요.

### 선택적 파라미터

배포 시 보안 강화와 사용자 지정을 위해 다음 파라미터들을 지정할 수 있습니다:

- **--disable-self-register**: 자체 등록 비활성화 (기본값: 활성화). 이 플래그가 설정되면 모든 사용자를 cognito에서 생성해야 하며 사용자가 직접 계정을 등록할 수 없습니다.
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 활성화 (기본값: 비활성화). 이 플래그가 설정되면 Lambda 함수의 콜드 스타트 시간이 개선되어 더 나은 사용자 경험을 위한 빠른 응답 시간을 제공합니다.
- **--ipv4-ranges**: 허용된 IPv4 범위의 쉼표로 구분된 목록. (기본값: 모든 ipv4 주소 허용)
- **--ipv6-ranges**: 허용된 IPv6 범위의 쉼표로 구분된 목록. (기본값: 모든 ipv6 주소 허용)
- **--disable-ipv6**: IPv6 연결 비활성화. (기본값: 활성화)
- **--allowed-signup-email-domains**: 가입이 허용된 이메일 도메인의 쉼표로 구분된 목록. (기본값: 도메인 제한 없음)
- **--bedrock-region**: bedrock이 사용 가능한 리전 정의. (기본값: us-east-1)
- **--repo-url**: 포크되었거나 사용자 지정 소스 컨트롤의 경우, 배포할 Bedrock Chat의 사용자 지정 리포지토리. (기본값: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: 배포할 Bedrock Chat의 버전. (기본값: 개발 중인 최신 버전)
- **--cdk-json-override**: CDK 컨텍스트 값을 배포 중에 재정의하기 위해 override JSON 블록을 사용할 수 있습니다. 이를 통해 cdk.json 파일을 직접 수정하지 않고도 구성을 수정할 수 있습니다.

사용 예시:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

override JSON은 cdk.json과 동일한 구조를 따라야 합니다. 다음을 포함한 모든 컨텍스트 값을 재정의할 수 있습니다:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: 활성화할 모델 ID 목록을 허용합니다. 기본값은 빈 목록으로, 모든 모델을 활성화합니다.
- `logoPath`: 내비게이션 드로어 상단에 표시되는 프론트엔드 `public/` 디렉토리 내의 로고 자산에 대한 상대 경로.
- 그리고 cdk.json에 정의된 기타 컨텍스트 값들

> [!Note]
> override 값은 AWS 코드 빌드에서 배포 시 기존 cdk.json 구성과 병합됩니다. override에 지정된 값이 cdk.json의 값보다 우선합니다.

#### 파라미터를 포함한 명령어 예시:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 약 35분 후에 브라우저에서 접속할 수 있는 다음과 같은 출력이 표시됩니다

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

위와 같은 가입 화면이 표시되며, 이메일을 등록하고 로그인할 수 있습니다.

> [!Important]
> 선택적 파라미터를 설정하지 않으면, 이 배포 방법은 URL을 아는 모든 사람이 가입할 수 있습니다. 프로덕션 환경에서는 보안 위험을 줄이기 위해 IP 주소 제한을 추가하고 자체 가입을 비활성화하는 것이 강력히 권장됩니다 (allowed-signup-email-domains를 정의하여 회사 도메인의 이메일 주소만 가입할 수 있도록 제한할 수 있습니다). IP 주소 제한을 위해 ipv4-ranges와 ipv6-ranges를 모두 사용하고, ./bin 실행 시 disable-self-register를 사용하여 자체 가입을 비활성화하세요.

> [!TIP]
> `Frontend URL`이 나타나지 않거나 Bedrock Chat이 제대로 작동하지 않는 경우, 최신 버전의 문제일 수 있습니다. 이 경우 파라미터에 `--version "v3.0.0"`를 추가하고 배포를 다시 시도하세요.

## 아키텍처

AWS 관리형 서비스를 기반으로 구축된 아키텍처로, 인프라 관리가 필요하지 않습니다. Amazon Bedrock을 활용하여 AWS 외부 API와의 통신이 불필요합니다. 이를 통해 확장 가능하고 안정적이며 안전한 애플리케이션을 배포할 수 있습니다.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): 대화 기록 저장을 위한 NoSQL 데이터베이스
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): 백엔드 API 엔드포인트 ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): 프론트엔드 애플리케이션 전송 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP 주소 제한
- [Amazon Cognito](https://aws.amazon.com/cognito/): 사용자 인증
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): API를 통해 기반 모델을 활용할 수 있는 관리형 서비스
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): 검색 증강 생성(Retrieval-Augmented Generation, [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/))을 위한 관리형 인터페이스를 제공하며, 문서 임베딩 및 구문 분석 서비스 제공
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): DynamoDB 스트림에서 이벤트를 수신하고 외부 지식을 임베딩하기 위한 Step Functions 실행
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Bedrock Knowledge Bases에 외부 지식을 임베딩하기 위한 수집 파이프라인 오케스트레이션
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Bedrock Knowledge Bases의 백엔드 데이터베이스로 작동하며, 전체 텍스트 검색과 벡터 검색 기능을 제공하여 관련 정보를 정확하게 검색 가능
- [Amazon Athena](https://aws.amazon.com/athena/): S3 버킷을 분석하기 위한 쿼리 서비스

![](./imgs/arch.png)

## CDK를 사용한 배포

Super-easy Deployment는 내부적으로 CDK를 사용하여 배포를 수행하기 위해 [AWS CodeBuild](https://aws.amazon.com/codebuild/)를 사용합니다. 이 섹션에서는 CDK를 직접 사용하여 배포하는 절차를 설명합니다.

- UNIX, Docker 및 Node.js 런타임 환경이 필요합니다.

> [!Important]
> 배포 중 로컬 환경에 저장 공간이 부족한 경우 CDK 부트스트래핑에서 오류가 발생할 수 있습니다. 배포 전에 인스턴스의 볼륨 크기를 확장하는 것을 권장합니다.

- 이 저장소를 복제합니다

```
git clone https://github.com/aws-samples/bedrock-chat
```

- npm 패키지를 설치합니다

```
cd bedrock-chat
cd cdk
npm ci
```

- 필요한 경우 [cdk.json](./cdk/cdk.json)의 다음 항목을 수정합니다.

  - `bedrockRegion`: Bedrock이 사용 가능한 리전. **참고: Bedrock은 현재 모든 리전을 지원하지 않습니다.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: 허용된 IP 주소 범위.
  - `enableLambdaSnapStart`: 기본값은 true입니다. [Python 함수에 대해 Lambda SnapStart를 지원하지 않는 리전](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)에 배포하는 경우 false로 설정하세요.
  - `globalAvailableModels`: 기본값은 모두입니다. 설정된 경우(모델 ID 목록), Bedrock Chat 애플리케이션의 모든 사용자의 채팅과 봇 생성 시 드롭다운 메뉴에 나타나는 모델을 전역적으로 제어할 수 있습니다.
  - `logoPath`: 애플리케이션 드로어 상단에 표시되는 이미지를 가리키는 `frontend/public` 아래의 상대 경로.
다음 모델 ID가 지원됩니다(배포 리전의 Bedrock 콘솔의 Model access에서 활성화되어 있는지 확인하세요):
- **Claude 모델:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova 모델:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral 모델:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek 모델:** `deepseek-r1`
- **Meta Llama 모델:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

전체 목록은 [index.ts](./frontend/src/constants/index.ts)에서 확인할 수 있습니다.

- CDK를 배포하기 전에 배포하려는 리전에 대해 한 번 Bootstrap 작업을 수행해야 합니다.

```
npx cdk bootstrap
```

- 이 샘플 프로젝트를 배포합니다

```
npx cdk deploy --require-approval never --all
```

- 다음과 같은 출력이 표시됩니다. 웹 앱의 URL은 `BedrockChatStack.FrontendURL`에 출력되므로 브라우저에서 접속하시기 바랍니다.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### 파라미터 정의

배포를 위한 파라미터는 `cdk.json`을 사용하거나 타입 안전한 `parameter.ts` 파일을 사용하는 두 가지 방법으로 정의할 수 있습니다.

#### cdk.json 사용 (전통적인 방법)

파라미터를 구성하는 전통적인 방법은 `cdk.json` 파일을 편집하는 것입니다. 이 방식은 간단하지만 타입 체크가 없습니다:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### parameter.ts 사용 (권장되는 타입 안전 방법)

더 나은 타입 안전성과 개발자 경험을 위해 `parameter.ts` 파일을 사용하여 파라미터를 정의할 수 있습니다:

```typescript
// 기본 환경에 대한 파라미터 정의
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// 추가 환경에 대한 파라미터 정의
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 개발 환경을 위한 비용 절감
  enableBotStoreReplicas: false, // 개발 환경을 위한 비용 절감
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 프로덕션을 위한 가용성 향상
  enableBotStoreReplicas: true, // 프로덕션을 위한 가용성 향상
});
```

> [!Note]
> 기존 사용자는 변경 없이 `cdk.json`을 계속 사용할 수 있습니다. `parameter.ts` 방식은 새로운 배포나 여러 환경을 관리해야 할 때 권장됩니다.

### 다중 환경 배포

`parameter.ts` 파일과 `-c envName` 옵션을 사용하여 동일한 코드베이스에서 여러 환경을 배포할 수 있습니다.

#### 전제 조건

1. 위에서 보여진 대로 `parameter.ts`에 환경을 정의합니다
2. 각 환경은 환경별 접두사가 있는 자체 리소스 세트를 가집니다

#### 배포 명령어

특정 환경을 배포하려면:

```bash
# 개발 환경 배포
npx cdk deploy --all -c envName=dev

# 프로덕션 환경 배포
npx cdk deploy --all -c envName=prod
```

환경이 지정되지 않은 경우 "default" 환경이 사용됩니다:

```bash
# 기본 환경 배포
npx cdk deploy --all
```

#### 중요 사항

1. **스택 이름 지정**:

   - 각 환경의 메인 스택은 환경 이름으로 접두사가 붙습니다(예: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - 하지만 커스텀 봇 스택(`BrChatKbStack*`)과 API 게시 스택(`ApiPublishmentStack*`)은 런타임에 동적으로 생성되므로 환경 접두사를 받지 않습니다

2. **리소스 이름 지정**:

   - 일부 리소스만 이름에 환경 접두사를 받습니다(예: `dev_ddb_export` 테이블, `dev-FrontendWebAcl`)
   - 대부분의 리소스는 원래 이름을 유지하지만 다른 스택에 있어 격리됩니다

3. **환경 식별**:

   - 모든 리소스는 환경 이름이 포함된 `CDKEnvironment` 태그가 지정됩니다
   - 이 태그를 사용하여 리소스가 어떤 환경에 속하는지 식별할 수 있습니다
   - 예: `CDKEnvironment: dev` 또는 `CDKEnvironment: prod`

4. **기본 환경 재정의**: `parameter.ts`에서 "default" 환경을 정의하면 `cdk.json`의 설정을 재정의합니다. `cdk.json`을 계속 사용하려면 `parameter.ts`에서 "default" 환경을 정의하지 마세요.

5. **환경 요구사항**: "default" 이외의 환경을 만들려면 `parameter.ts`를 사용해야 합니다. 해당하는 환경 정의 없이 `-c envName` 옵션만으로는 충분하지 않습니다.

6. **리소스 격리**: 각 환경은 자체 리소스 세트를 생성하므로 동일한 AWS 계정에서 충돌 없이 개발, 테스트 및 프로덕션 환경을 가질 수 있습니다.

## 기타

배포에 대한 매개변수를 정의하는 방법에는 두 가지가 있습니다: `cdk.json`을 사용하거나 타입 안전성이 보장되는 `parameter.ts` 파일을 사용하는 것입니다.

#### cdk.json 사용 (전통적인 방법)

매개변수를 구성하는 전통적인 방법은 `cdk.json` 파일을 편집하는 것입니다. 이 방법은 간단하지만 타입 검사가 없습니다:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### parameter.ts 사용 (권장되는 타입 안전 방법)

더 나은 타입 안전성과 개발자 경험을 위해 `parameter.ts` 파일을 사용하여 매개변수를 정의할 수 있습니다:

```typescript
// 기본 환경에 대한 매개변수 정의
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// 추가 환경에 대한 매개변수 정의
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 개발 환경을 위한 비용 절감
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 프로덕션을 위한 향상된 가용성
});
```

> [!Note]
> 기존 사용자는 변경 없이 `cdk.json`을 계속 사용할 수 있습니다. `parameter.ts` 방식은 새로운 배포나 여러 환경을 관리해야 할 때 권장됩니다.

### 다중 환경 배포

`parameter.ts` 파일과 `-c envName` 옵션을 사용하여 동일한 코드베이스에서 여러 환경을 배포할 수 있습니다.

#### 전제 조건

1. 위에서 보여진 대로 `parameter.ts`에 환경을 정의
2. 각 환경은 환경별 접두사가 있는 자체 리소스 세트를 가짐

#### 배포 명령어

특정 환경을 배포하려면:

```bash
# 개발 환경 배포
npx cdk deploy --all -c envName=dev

# 프로덕션 환경 배포
npx cdk deploy --all -c envName=prod
```

환경이 지정되지 않은 경우 "default" 환경이 사용됩니다:

```bash
# 기본 환경 배포
npx cdk deploy --all
```

#### 중요 사항

1. **스택 이름 지정**:

   - 각 환경의 주요 스택은 환경 이름으로 접두사가 붙습니다(예: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - 단, 커스텀 봇 스택(`BrChatKbStack*`)과 API 게시 스택(`ApiPublishmentStack*`)은 런타임에 동적으로 생성되므로 환경 접두사를 받지 않습니다

2. **리소스 이름 지정**:

   - 일부 리소스만 이름에 환경 접두사를 받습니다(예: `dev_ddb_export` 테이블, `dev-FrontendWebAcl`)
   - 대부분의 리소스는 원래 이름을 유지하지만 다른 스택에 있어 격리됩니다

3. **환경 식별**:

   - 모든 리소스에는 환경 이름이 포함된 `CDKEnvironment` 태그가 지정됩니다
   - 이 태그를 사용하여 리소스가 어느 환경에 속하는지 식별할 수 있습니다
   - 예: `CDKEnvironment: dev` 또는 `CDKEnvironment: prod`

4. **기본 환경 재정의**: `parameter.ts`에서 "default" 환경을 정의하면 `cdk.json`의 설정을 재정의합니다. `cdk.json`을 계속 사용하려면 `parameter.ts`에서 "default" 환경을 정의하지 마세요.

5. **환경 요구사항**: "default" 이외의 환경을 만들려면 반드시 `parameter.ts`를 사용해야 합니다. 해당 환경 정의 없이 `-c envName` 옵션만으로는 충분하지 않습니다.

6. **리소스 격리**: 각 환경은 자체 리소스 세트를 생성하므로 동일한 AWS 계정에서 충돌 없이 개발, 테스트 및 프로덕션 환경을 가질 수 있습니다.

## 기타

### 리소스 제거

cli와 CDK를 사용하는 경우 `npx cdk destroy`를 실행하세요. 그렇지 않은 경우 [CloudFormation](https://console.aws.amazon.com/cloudformation/home)에 접속하여 `BedrockChatStack`과 `FrontendWafStack`을 수동으로 삭제하세요. `FrontendWafStack`은 `us-east-1` 리전에 있다는 점에 유의하세요.

### 언어 설정

이 애셋은 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)를 사용하여 언어를 자동으로 감지합니다. 애플리케이션 메뉴에서 언어를 전환할 수 있습니다. 또는 아래와 같이 쿼리 문자열을 사용하여 언어를 설정할 수 있습니다.

> `https://example.com?lng=ja`

### 자체 회원가입 비활성화

이 샘플은 기본적으로 자체 회원가입이 활성화되어 있습니다. 자체 회원가입을 비활성화하려면 [cdk.json](./cdk/cdk.json)을 열고 `selfSignUpEnabled`를 `false`로 변경하세요. [외부 ID 공급자](#external-identity-provider)를 구성하는 경우, 이 값은 무시되고 자동으로 비활성화됩니다.

### 회원가입 이메일 주소의 도메인 제한

기본적으로 이 샘플은 회원가입 이메일 주소의 도메인을 제한하지 않습니다. 특정 도메인에서만 회원가입을 허용하려면 `cdk.json`을 열고 `allowedSignUpEmailDomains`에 도메인 목록을 지정하세요.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 외부 ID 공급자

이 샘플은 외부 ID 공급자를 지원합니다. 현재 [Google](./idp/SET_UP_GOOGLE_ko-KR.md)과 [사용자 지정 OIDC 공급자](./idp/SET_UP_CUSTOM_OIDC_ko-KR.md)를 지원합니다.

### 선택적 프론트엔드 WAF

CloudFront 배포의 경우 AWS WAF WebACL은 us-east-1 리전에 생성되어야 합니다. 일부 조직에서는 정책에 의해 기본 리전 외부에 리소스를 생성하는 것이 제한될 수 있습니다. 이러한 환경에서는 us-east-1에서 프론트엔드 WAF를 프로비저닝하려고 할 때 CDK 배포가 실패할 수 있습니다.

이러한 제한을 수용하기 위해 프론트엔드 WAF 스택은 선택사항입니다. 비활성화된 경우 CloudFront 배포는 WebACL 없이 배포됩니다. 이는 프론트엔드 엣지에서 IP 허용/거부 제어가 없다는 것을 의미합니다. 인증 및 기타 모든 애플리케이션 제어는 정상적으로 작동합니다. 이 설정은 프론트엔드 WAF(CloudFront 범위)에만 영향을 미치며, 게시된 API WAF(지역)는 영향을 받지 않습니다.

프론트엔드 WAF를 비활성화하려면 `parameter.ts`에서 다음과 같이 설정하세요(권장되는 타입-세이프 방법):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

또는 레거시 `cdk/cdk.json`을 사용하는 경우 다음과 같이 설정하세요:

```json
"enableFrontendWaf": false
```

### 새 사용자를 그룹에 자동으로 추가

이 샘플에는 사용자에게 권한을 부여하기 위한 다음과 같은 그룹이 있습니다:

- [`Admin`](./ADMINISTRATOR_ko-KR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ko-KR.md)

새로 생성된 사용자를 자동으로 그룹에 가입시키려면 [cdk.json](./cdk/cdk.json)에서 지정할 수 있습니다.

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

기본적으로 새로 생성된 사용자는 `CreatingBotAllowed` 그룹에 가입됩니다.

### RAG 복제본 구성

`enableRagReplicas`는 [cdk.json](./cdk/cdk.json)의 옵션으로, Amazon OpenSearch Serverless를 사용하는 지식 베이스의 RAG 데이터베이스 복제본 설정을 제어합니다.

- **기본값**: true
- **true**: 추가 복제본을 활성화하여 가용성을 향상시키며, 프로덕션 환경에 적합하지만 비용이 증가합니다.
- **false**: 복제본을 줄여 비용을 절감하며, 개발 및 테스트에 적합합니다.

이는 계정/리전 수준의 설정으로, 개별 봇이 아닌 전체 애플리케이션에 영향을 미칩니다.

> [!Note]
> 2024년 6월 기준, Amazon OpenSearch Serverless는 0.5 OCU를 지원하여 소규모 워크로드의 초기 비용을 낮춥니다. 프로덕션 배포는 2 OCU로 시작할 수 있으며, 개발/테스트 워크로드는 1 OCU를 사용할 수 있습니다. OpenSearch Serverless는 워크로드 요구 사항에 따라 자동으로 확장됩니다. 자세한 내용은 [공지사항](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)을 참조하세요.

### 봇 스토어 구성

봇 스토어 기능을 통해 사용자는 사용자 정의 봇을 공유하고 검색할 수 있습니다. [cdk.json](./cdk/cdk.json)에서 다음 설정을 통해 봇 스토어를 구성할 수 있습니다:

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: 봇 스토어 기능의 활성화 여부를 제어합니다(기본값: `true`)
- **botStoreLanguage**: 봇 검색 및 발견을 위한 기본 언어를 설정합니다(기본값: `"en"`). 이는 봇이 인덱싱되고 검색되는 방식에 영향을 미치며, 지정된 언어에 맞게 텍스트 분석을 최적화합니다.
- **enableBotStoreReplicas**: 봇 스토어가 사용하는 OpenSearch Serverless 컬렉션의 대기 복제본 활성화 여부를 제어합니다(기본값: `false`). `true`로 설정하면 가용성이 향상되지만 비용이 증가하며, `false`로 설정하면 비용이 감소하지만 가용성에 영향을 미칠 수 있습니다.
  > **중요**: 컬렉션이 이미 생성된 후에는 이 속성을 업데이트할 수 없습니다. 이 속성을 수정하려고 시도해도 컬렉션은 원래 값을 계속 사용합니다.

### 교차 리전 추론

[교차 리전 추론](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)을 통해 Amazon Bedrock은 피크 수요 기간 동안 처리량과 복원력을 향상시키기 위해 여러 AWS 리전에 걸쳐 모델 추론 요청을 동적으로 라우팅할 수 있습니다. 구성하려면 `cdk.json`을 편집하세요.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)는 Lambda 함수의 콜드 스타트 시간을 개선하여 더 나은 사용자 경험을 위한 더 빠른 응답 시간을 제공합니다. 반면에 Python 함수의 경우 [캐시 크기에 따른 요금이 부과](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)되며 현재 [일부 리전에서는 사용할 수 없습니다](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions). SnapStart를 비활성화하려면 `cdk.json`을 편집하세요.

```json
"enableLambdaSnapStart": false
```

### 사용자 정의 도메인 구성

[cdk.json](./cdk/cdk.json)에서 다음 매개변수를 설정하여 CloudFront 배포에 대한 사용자 정의 도메인을 구성할 수 있습니다:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: 채팅 애플리케이션의 사용자 정의 도메인 이름(예: chat.example.com)
- `hostedZoneId`: 도메인 레코드가 생성될 Route 53 호스팅 영역의 ID

이러한 매개변수가 제공되면 배포는 자동으로:

- us-east-1 리전에서 DNS 검증이 포함된 ACM 인증서를 생성합니다
- Route 53 호스팅 영역에 필요한 DNS 레코드를 생성합니다
- CloudFront가 사용자 정의 도메인을 사용하도록 구성합니다

> [!Note]
> 도메인은 AWS 계정의 Route 53에서 관리되어야 합니다. 호스팅 영역 ID는 Route 53 콘솔에서 찾을 수 있습니다.

### 허용된 국가 구성(지역 제한)

클라이언트가 접근하는 국가를 기반으로 Bedrock-Chat에 대한 접근을 제한할 수 있습니다.
[cdk.json](./cdk/cdk.json)의 `allowedCountries` 매개변수를 사용하여 [ISO-3166 국가 코드](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) 목록을 지정하세요.
예를 들어, 뉴질랜드 기반 비즈니스는 뉴질랜드(NZ)와 호주(AU)의 IP 주소만 포털에 접근할 수 있도록 하고 다른 모든 사용자의 접근을 거부하도록 결정할 수 있습니다.
이 동작을 구성하려면 [cdk.json](./cdk/cdk.json)에서 다음 설정을 사용하세요:

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

또는 `parameter.ts`를 사용하세요(권장되는 타입-세이프 방법):

```ts
// 기본 환경에 대한 매개변수 정의
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### IPv6 지원 비활성화

프론트엔드는 기본적으로 IP와 IPv6 주소를 모두 가져옵니다. 드문 경우지만
명시적으로 IPv6 지원을 비활성화해야 할 수 있습니다. 이를 위해
[parameter.ts](./cdk/parameter.ts) 또는 유사하게 [cdk.json](./cdk/cdk.json)에서 다음 매개변수를 설정하세요:

```ts
"enableFrontendIpv6": false
```

설정하지 않으면 IPv6 지원이 기본적으로 활성화됩니다.

### 로컬 개발

[LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_ko-KR.md)를 참조하세요.

### 기여

이 리포지토리에 기여하는 것을 고려해 주셔서 감사합니다! 버그 수정, 언어 번역(i18n), 기능 개선, [에이전트 도구](./docs/AGENT.md#how-to-develop-your-own-tools) 및 기타 개선 사항을 환영합니다.

기능 개선 및 기타 개선 사항의 경우, **풀 리퀘스트를 생성하기 전에 구현 접근 방식과 세부 사항을 논의하

## 연락처

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 주요 기여자

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## 기여자

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## 라이선스

이 라이브러리는 MIT-0 라이선스를 따릅니다. [라이선스 파일](./LICENSE)을 참조하세요.