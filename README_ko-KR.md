<h1 align="center">Bedrock 채팅 (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)

[Amazon Bedrock](https://aws.amazon.com/bedrock/)에서 제공하는 다국어 생성형 AI 플랫폼입니다.
채팅, 지식 기반 맞춤형 봇(RAG), 봇 스토어를 통한 봇 공유, 에이전트를 사용한 작업 자동화를 지원합니다.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3가 출시되었습니다. 업데이트 시 [마이그레이션 가이드](./migration/V2_TO_V3_ko-KR.md)를 주의깊게 검토해 주세요.** 주의하지 않으면 **V2의 봇은 사용할 수 없게 됩니다.**

### 봇 개인화 / 봇 스토어

고유한 지침과 지식(소위 [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/))을 추가할 수 있습니다. 봇은 봇 스토어 마켓플레이스를 통해 애플리케이션 사용자 간에 공유할 수 있으며, 맞춤형 봇은 독립형 API로 게시할 수도 있습니다 ([자세히 보기](./PUBLISH_API_ko-KR.md)).

<details>
<summary>스크린샷</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

기존 [Amazon Bedrock의 지식 기반](https://aws.amazon.com/bedrock/knowledge-bases/)도 가져올 수 있습니다.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> 거버넌스 이유로, 허용된 사용자만 맞춤형 봇을 생성할 수 있습니다. 맞춤형 봇 생성을 허용하려면 사용자가 `CreatingBotAllowed` 그룹의 구성원이어야 합니다. 이는 관리 콘솔 > Amazon Cognito 사용자 풀 또는 AWS CLI를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > 출력 > `AuthUserPoolIdxxxx`에서 확인할 수 있습니다.

### 관리 기능

API 관리, 봇을 필수로 표시, 봇 사용량 분석 ([자세히 보기](./ADMINISTRATOR_ko-KR.md))

<details>
<summary>스크린샷</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### 에이전트

[에이전트 기능](./AGENT_ko-KR.md)을 사용하면 챗봇이 더 복잡한 작업을 자동으로 처리할 수 있습니다. 예를 들어, 사용자의 질문에 답변하기 위해 에이전트는 외부 도구에서 필요한 정보를 검색하거나 작업을 여러 단계로 나누어 처리할 수 있습니다.

<details>
<summary>스크린샷</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 초간단 배포

- us-east-1 리전에서 [Bedrock 모델 접근](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)으로 이동 > `모델 접근 관리` > 사용하고 싶은 모든 모델을 선택하고 `변경사항 저장`을 클릭하세요.

<details>
<summary>스크린샷</summary>

![](./imgs/model_screenshot.png)

</details>

- 배포하려는 리전의 [CloudShell](https://console.aws.amazon.com/cloudshell/home)을 열어주세요.
- 다음 명령어로 배포를 진행하세요. 특정 버전을 배포하거나 보안 정책을 적용하려면 [선택적 매개변수](#선택적-매개변수)에서 적절한 매개변수를 지정해 주세요.

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- 새 사용자인지 v3 버전을 사용하는지 묻는 메시지가 표시됩니다. v0부터 계속 사용하는 사용자가 아니라면 `y`를 입력해 주세요.

### 선택적 매개변수

다음 매개변수를 배포 시 지정하여 보안과 맞춤설정을 강화할 수 있습니다:

- **--disable-self-register**: 자체 등록 비활성화 (기본값: 활성화됨). 이 플래그를 설정하면 Cognito에서 모든 사용자를 직접 생성해야 하며 사용자의 자체 계정 등록이 허용되지 않습니다.
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) 활성화 (기본값: 비활성화). 이 플래그를 설정하면 Lambda 함수의 콜드 스타트 시간이 개선되어 사용자 경험을 위한 더 빠른 응답 시간을 제공합니다.
- **--ipv4-ranges**: 허용된 IPv4 범위의 쉼표로 구분된 목록. (기본값: 모든 IPv4 주소 허용)
- **--ipv6-ranges**: 허용된 IPv6 범위의 쉼표로 구분된 목록. (기본값: 모든 IPv6 주소 허용)
- **--disable-ipv6**: IPv6를 통한 연결 비활성화. (기본값: 활성화됨)
- **--allowed-signup-email-domains**: 가입에 허용된 이메일 도메인의 쉼표로 구분된 목록. (기본값: 도메인 제한 없음)
- **--bedrock-region**: Bedrock을 사용할 수 있는 리전 정의. (기본값: us-east-1)
- **--repo-url**: 포크되거나 사용자 정의된 Bedrock Chat 저장소를 배포할 때 사용. (기본값: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: 배포할 Bedrock Chat 버전. (기본값: 개발 중인 최신 버전)
- **--cdk-json-override**: 배포 중 모든 CDK 컨텍스트 값을 재정의할 수 있는 JSON 블록. 이를 통해 cdk.json 파일을 직접 편집하지 않고도 구성을 수정할 수 있습니다.

사용 예시:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

재정의 JSON은 cdk.json과 동일한 구조를 따라야 합니다. 다음을 포함한 모든 컨텍스트 값을 재정의할 수 있습니다:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- cdk.json에 정의된 기타 컨텍스트 값

> [!Note]
> 재정의 값은 AWS 코드 빌드 중 배포 시 기존 cdk.json 구성과 병합됩니다. 재정의에 지정된 값이 cdk.json의 값보다 우선 적용됩니다.

#### 매개변수를 사용한 예시 명령어:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- 약 35분 후, 브라우저에서 접속할 수 있는 다음 출력을 얻게 됩니다.

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

위와 같은 로그인 화면이 나타나며, 여기서 이메일을 등록하고 로그인할 수 있습니다.

> [!Important]
> 선택적 매개변수를 설정하지 않으면 URL을 아는 누구나 가입할 수 있습니다. 프로덕션 환경에서는 보안 위험을 완화하기 위해 IP 주소 제한을 추가하고 자체 가입을 비활성화하는 것이 강력히 권장됩니다(회사 도메인의 이메일 주소만 가입할 수 있도록 allowed-signup-email-domains을 정의할 수 있습니다). ./bin 실행 시 ipv4-ranges와 ipv6-ranges로 IP 주소 제한을 적용하고, disable-self-register를 사용하여 자체 가입을 비활성화하세요.

> [!TIP]
> `Frontend URL`이 나타나지 않거나 Bedrock Chat이 제대로 작동하지 않는 경우, 최신 버전에 문제가 있을 수 있습니다. 이 경우 매개변수에 `--version "v3.0.0"`을 추가하고 다시 배포해 보세요.

## 아키텍처

AWS 관리형 서비스를 기반으로 구축된 아키텍처로, 인프라 관리의 필요성을 제거합니다. Amazon Bedrock을 활용하여 AWS 외부 API와 통신할 필요가 없습니다. 이를 통해 확장 가능하고 안정적이며 안전한 애플리케이션을 배포할 수 있습니다.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): 대화 기록 저장을 위한 NoSQL 데이터베이스
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): 백엔드 API 엔드포인트 ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): 프론트엔드 애플리케이션 전송 ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP 주소 제한
- [Amazon Cognito](https://aws.amazon.com/cognito/): 사용자 인증
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): API를 통해 기본 모델을 활용하는 관리형 서비스
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): 검색 증강 생성([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/))을 위한 관리형 인터페이스 제공, 문서 임베딩 및 파싱 서비스 제공
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): DynamoDB 스트림에서 이벤트 수신 및 외부 지식 임베딩을 위한 Step Functions 시작
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Bedrock Knowledge Bases에 외부 지식을 임베딩하기 위한 수집 파이프라인 오케스트레이션
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Bedrock Knowledge Bases의 백엔드 데이터베이스로 전체 텍스트 검색 및 벡터 검색 기능 제공, 관련 정보의 정확한 검색 가능
- [Amazon Athena](https://aws.amazon.com/athena/): S3 버킷을 분석하기 위한 쿼리 서비스

![](./imgs/arch.png)

## CDK를 사용하여 배포하기

Super-easy 배포는 내부적으로 [AWS CodeBuild](https://aws.amazon.com/codebuild/)를 사용하여 CDK로 배포를 수행합니다. 이 섹션에서는 CDK를 직접 사용하여 배포하는 절차를 설명합니다.

- UNIX, Docker 및 Node.js 런타임 환경이 필요합니다. 없는 경우 [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)을 사용할 수 있습니다.

> [!중요]
> 배포 중 로컬 환경의 저장 공간이 부족하면 CDK 부트스트래핑에서 오류가 발생할 수 있습니다. Cloud9 등에서 실행 중인 경우 배포 전에 인스턴스의 볼륨 크기를 확장하는 것이 좋습니다.

- 리포지토리 복제

```
git clone https://github.com/aws-samples/bedrock-chat
```

- npm 패키지 설치

```
cd bedrock-chat
cd cdk
npm ci
```

- 필요한 경우 [cdk.json](./cdk/cdk.json)의 다음 항목을 편집하세요.

  - `bedrockRegion`: Bedrock을 사용할 수 있는 리전. **참고: 현재 Bedrock은 모든 리전을 지원하지 않습니다.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: 허용된 IP 주소 범위.
  - `enableLambdaSnapStart`: 기본값은 true입니다. [Lambda SnapStart for Python 함수를 지원하지 않는 리전](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions)에 배포하는 경우 false로 설정하세요.

- CDK를 배포하기 전에 배포할 리전에 대해 한 번 부트스트랩해야 합니다.

```
npx cdk bootstrap
```

- 이 샘플 프로젝트 배포

```
npx cdk deploy --require-approval never --all
```

- 다음과 유사한 출력을 받게 됩니다. 웹 앱의 URL은 `BedrockChatStack.FrontendURL`에서 출력되므로 브라우저에서 접속하세요.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### 매개변수 정의

배포를 위한 매개변수는 두 가지 방법으로 정의할 수 있습니다: `cdk.json` 사용 또는 타입 안전한 `parameter.ts` 파일 사용.

#### cdk.json 사용 (기존 방법)

매개변수를 구성하는 기존 방법은 `cdk.json` 파일을 편집하는 것입니다. 이 방법은 간단하지만 타입 검사가 없습니다:

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

#### parameter.ts 사용 (권장되는 타입 안전한 방법)

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
  enableRagReplicas: false, // 개발 환경의 비용 절감
  enableBotStoreReplicas: false, // 개발 환경의 비용 절감
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 프로덕션을 위한 향상된 가용성
  enableBotStoreReplicas: true, // 프로덕션을 위한 향상된 가용성
});
```

> [!참고]
> 기존 사용자는 변경 없이 `cdk.json`을 계속 사용할 수 있습니다. `parameter.ts` 접근 방식은 새 배포 또는 여러 환경을 관리해야 할 때 권장됩니다.

### 여러 환경 배포

`parameter.ts` 파일과 `-c envName` 옵션을 사용하여 동일한 코드베이스에서 여러 환경을 배포할 수 있습니다.

#### 전제 조건

1. 위와 같이 `parameter.ts`에 환경 정의
2. 각 환경은 환경별 접두사가 있는 고유한 리소스 세트를 갖습니다.

#### 배포 명령

특정 환경 배포:

```bash
# dev 환경 배포
npx cdk deploy --all -c envName=dev

# prod 환경 배포
npx cdk deploy --all -c envName=prod
```

환경이 지정되지 않은 경우 "default" 환경이 사용됩니다:

```bash
# 기본 환경 배포
npx cdk deploy --all
```

#### 중요 참고 사항

1. **스택 이름**:
   - 각 환경의 주요 스택은 환경 이름으로 접두사가 붙습니다 (예: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - 그러나 사용자 정의 봇 스택(`BrChatKbStack*`)과 API 게시 스택(`ApiPublishmentStack*`)은 런타임에 동적으로 생성되므로 환경 접두사를 받지 않습니다.

2. **리소스 이름**:
   - 일부 리소스만 이름에 환경 접두사를 받습니다 (예: `dev_ddb_export` 테이블, `dev-FrontendWebAcl`)
   - 대부분의 리소스는 원래 이름을 유지하지만 다른 스택에 격리됩니다.

3. **환경 식별**:
   - 모든 리소스에는 환경 이름을 포함하는 `CDKEnvironment` 태그가 지정됩니다.
   - 이 태그를 사용하여 리소스가 속한 환경을 식별할 수 있습니다.
   - 예: `CDKEnvironment: dev` 또는 `CDKEnvironment: prod`

4. **기본 환경 재정의**: `parameter.ts`에 "default" 환경을 정의하면 `cdk.json`의 설정을 재정의합니다. `cdk.json`을 계속 사용하려면 `parameter.ts`에 "default" 환경을 정의하지 마세요.

5. **환경 요구 사항**: "default" 이외의 환경을 생성하려면 `parameter.ts`를 사용해야 합니다. `-c envName` 옵션만으로는 해당 환경 정의 없이는 충분하지 않습니다.

6. **리소스 격리**: 각 환경은 고유한 리소스 세트를 생성하여 동일한 AWS 계정에서 개발, 테스트 및 프로덕션 환경을 충돌 없이 가질 수 있습니다.

## 기타

배포에 대한 매개변수를 두 가지 방법으로 정의할 수 있습니다: `cdk.json`을 사용하거나 타입 안전한 `parameter.ts` 파일을 사용합니다.

#### cdk.json 사용 (기존 방법)

매개변수를 구성하는 기존 방법은 `cdk.json` 파일을 편집하는 것입니다. 이 방법은 간단하지만 타입 검사가 부족합니다:

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

#### parameter.ts 사용 (권장되는 타입 안전한 방법)

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
  enableRagReplicas: false, // 개발 환경의 비용 절감
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 프로덕션을 위한 향상된 가용성
});
```

> [!참고]
> 기존 사용자는 변경 없이 `cdk.json`을 계속 사용할 수 있습니다. `parameter.ts` 접근 방식은 새로운 배포나 여러 환경을 관리해야 할 때 권장됩니다.

### 여러 환경 배포

`parameter.ts` 파일과 `-c envName` 옵션을 사용하여 동일한 코드베이스에서 여러 환경을 배포할 수 있습니다.

#### 전제 조건

1. 위에 표시된 대로 `parameter.ts`에서 환경 정의
2. 각 환경은 환경별 접두사가 있는 고유한 리소스 세트를 가집니다

#### 배포 명령어

특정 환경 배포:

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

#### 중요 참고 사항

1. **스택 이름**:

   - 각 환경의 주요 스택은 환경 이름으로 접두사가 붙습니다 (예: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - 그러나 사용자 지정 봇 스택(`BrChatKbStack*`)과 API 게시 스택(`ApiPublishmentStack*`)은 런타임에 동적으로 생성되므로 환경 접두사를 받지 않습니다

2. **리소스 이름**:

   - 일부 리소스만 이름에 환경 접두사를 받습니다 (예: `dev_ddb_export` 테이블, `dev-FrontendWebAcl`)
   - 대부분의 리소스는 원래 이름을 유지하지만 다른 스택에 격리됩니다

3. **환경 식별**:

   - 모든 리소스에는 환경 이름을 포함하는 `CDKEnvironment` 태그가 있습니다
   - 이 태그를 사용하여 리소스가 어떤 환경에 속하는지 식별할 수 있습니다
   - 예: `CDKEnvironment: dev` 또는 `CDKEnvironment: prod`

4. **기본 환경 재정의**: `parameter.ts`에 "default" 환경을 정의하면 `cdk.json`의 설정을 재정의합니다. `cdk.json`을 계속 사용하려면 `parameter.ts`에 "default" 환경을 정의하지 마세요.

5. **환경 요구 사항**: "default" 이외의 환경을 생성하려면 `parameter.ts`를 사용해야 합니다. `-c envName` 옵션만으로는 충분하지 않습니다.

6. **리소스 격리**: 각 환경은 고유한 리소스 세트를 생성하여 동일한 AWS 계정에서 개발, 테스트, 프로덕션 환경을 충돌 없이 가질 수 있습니다.

## 기타

### 리소스 제거

CLI와 CDK를 사용하는 경우 `npx cdk destroy`를 실행하세요. 그렇지 않으면 [CloudFormation](https://console.aws.amazon.com/cloudformation/home)에 접속하여 `BedrockChatStack`과 `FrontendWafStack`을 수동으로 삭제하세요. `FrontendWafStack`은 `us-east-1` 리전에 있습니다.

### 언어 설정

이 애셋은 [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector)를 사용하여 자동으로 언어를 감지합니다. 애플리케이션 메뉴에서 언어를 전환할 수 있습니다. 또는 아래와 같이 쿼리 문자열을 사용하여 언어를 설정할 수 있습니다.

> `https://example.com?lng=ja`

### 자체 회원가입 비활성화

이 샘플은 기본적으로 자체 회원가입이 활성화되어 있습니다. 자체 회원가입을 비활성화하려면 [cdk.json](./cdk/cdk.json)을 열고 `selfSignUpEnabled`를 `false`로 변경하세요. [외부 ID 공급자](#외부-id-공급자)를 구성하면 이 값은 무시되고 자동으로 비활성화됩니다.

### 회원가입 이메일 주소의 도메인 제한

기본적으로 이 샘플은 회원가입 이메일 주소의 도메인을 제한하지 않습니다. 특정 도메인에서만 회원가입을 허용하려면 `cdk.json`을 열고 `allowedSignUpEmailDomains`에 도메인 목록을 지정하세요.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### 외부 ID 공급자

이 샘플은 외부 ID 공급자를 지원합니다. 현재 [Google](./idp/SET_UP_GOOGLE_ko-KR.md)과 [사용자 정의 OIDC 공급자](./idp/SET_UP_CUSTOM_OIDC_ko-KR.md)를 지원합니다.

### 새 사용자를 그룹에 자동으로 추가

이 샘플은 사용자에게 권한을 부여하기 위해 다음 그룹을 가지고 있습니다:

- [`관리자`](./ADMINISTRATOR_ko-KR.md)
- [`봇 생성 허용`](#봇-개인화)
- [`게시 허용`](./PUBLISH_API_ko-KR.md)

새로 생성된 사용자가 자동으로 그룹에 가입하도록 하려면 [cdk.json](./cdk/cdk.json)에서 지정할 수 있습니다.

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

기본적으로 새로 생성된 사용자는 `CreatingBotAllowed` 그룹에 가입됩니다.

### RAG 복제본 구성

[cdk.json](./cdk/cdk.json)의 `enableRagReplicas`는 Amazon OpenSearch Serverless를 사용하는 Knowledge Bases의 복제본 설정을 제어하는 옵션입니다.

- **기본값**: true
- **true**: 추가 복제본을 활성화하여 가용성을 향상시키며, 프로덕션 환경에 적합하지만 비용이 증가합니다.
- **false**: 복제본을 줄여 비용을 절감하며, 개발 및 테스트에 적합합니다.

이는 계정/리전 수준 설정으로, 개별 봇이 아닌 전체 애플리케이션에 영향을 미칩니다.

> [!참고]
> 2024년 6월 현재, Amazon OpenSearch Serverless는 0.5 OCU를 지원하여 소규모 워크로드의 진입 비용을 낮추었습니다. 프로덕션 배포는 2 OCU로 시작할 수 있고, 개발/테스트 워크로드는 1 OCU를 사용할 수 있습니다. OpenSearch Serverless는 워크로드 요구에 따라 자동으로 확장됩니다. 자세한 내용은 [공지](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/)를 참조하세요.

### 봇 스토어 구성

봇 스토어 기능을 통해 사용자는 맞춤형 봇을 공유하고 발견할 수 있습니다. [cdk.json](./cdk/cdk.json)의 다음 설정을 통해 봇 스토어를 구성할 수 있습니다:

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: 봇 스토어 기능 활성화 여부 제어 (기본값: `true`)
- **botStoreLanguage**: 봇 검색 및 발견을 위한 기본 언어 설정 (기본값: `"en"`). 이는 봇 색인 및 검색 시 지정된 언어에 대한 텍스트 분석에 영향을 미칩니다.
- **enableBotStoreReplicas**: 봇 스토어에서 사용하는 OpenSearch Serverless 컬렉션의 대기 복제본 활성화 여부 제어 (기본값: `false`). `true`로 설정하면 가용성이 향상되지만 비용이 증가하고, `false`로 설정하면 비용이 절감되지만 가용성에 영향을 줄 수 있습니다.
  > **중요**: 컬렉션이 이미 생성된 후에는 이 속성을 업데이트할 수 없습니다. 이 속성을 수정하려고 시도하면 컬렉션은 원래 값을 계속 사용합니다.

### 교차 리전 추론

[교차 리전 추론](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)을 통해 Amazon Bedrock은 여러 AWS 리전에서 모델 추론 요청을 동적으로 라우팅하여 피크 수요 기간 동안 처리량과 복원력을 향상시킬 수 있습니다. 구성하려면 `cdk.json`을 편집하세요.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)는 Lambda 함수의 콜드 스타트 시간을 개선하여 사용자 경험을 향상시키는 더 빠른 응답 시간을 제공합니다. 반면에 Python 함수의 경우 [캐시 크기에 따른 요금](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing)이 있고 [일부 리전에서는 사용할 수 없습니다](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions). SnapStart를 비활성화하려면 `cdk.json`을 편집하세요.

```json
"enableLambdaSnapStart": false
```

### 사용자 정의 도메인 구성

[cdk.json](./cdk/cdk.json)에서 다음 매개변수를 설정하여 CloudFront 배포의 사용자 정의 도메인을 구성할 수 있습니다:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: 채팅 애플리케이션의 사용자 정의 도메인 이름 (예: chat.example.com)
- `hostedZoneId`: DNS 레코드가 생성될 Route 53 호스팅 영역의 ID

이러한 매개변수가 제공되면 배포 시 자동으로 다음을 수행합니다:

- us-east-1 리전에 DNS 검증이 있는 ACM 인증서 생성
- Route 53 호스팅 영역에 필요한 DNS 레코드 생성
- CloudFront를 사용자 정의 도메인을 사용하도록 구성

> [!참고]
> 도메인은 AWS 계정의 Route 53에서 관리해야 합니다. 호스팅 영역 ID는 Route 53 콘솔에서 찾을 수 있습니다.

### 로컬 개발

[로컬 개발](./LOCAL_DEVELOPMENT_ko-KR.md)을 참조하세요.

### 기여

이 저장소에 기여를 고려해 주셔서 감사합니다! 버그 수정, 언어 번역(i18n), 기능 개선, [에이전트 도구](./docs/AGENT.md#how-to-develop-your-own-tools) 등을 환영합니다.

기능 개선 및 기타 개선 사항의 경우, **풀 리퀘스트를 생성하기 전에 구현 접근 방식과 세부 사항을 논의하기 위해 기능 요청 이슈를 생성해 주시면 감사하겠습니다. 버그 수정 및 언어 번역(i18n)의 경우 직접 풀 리퀘스트를 생성하세요.**

기여하기 전에 다음 지침을 참조하세요:

- [로컬 개발](./LOCAL_DEVELOPMENT_ko-KR.md)
- [기여하기](./CONTRIBUTING_ko-KR.md)

## 연락처

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 주요 기여자

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## 기여자

[![bedrock chat 기여자](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## 라이선스

이 라이브러리는 MIT-0 라이선스 하에 배포됩니다. [LICENSE 파일](./LICENSE)을 참조하세요.