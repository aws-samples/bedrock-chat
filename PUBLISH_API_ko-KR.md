# API 게시

## 개요

이 샘플에는 API를 게시하기 위한 기능이 포함되어 있습니다. 채팅 인터페이스가 초기 검증에는 편리할 수 있지만, 실제 구현은 특정 사용 사례와 최종 사용자를 위한 사용자 경험(UX)에 따라 달라집니다. 어떤 시나리오에서는 채팅 UI가 선호되는 선택일 수 있지만, 다른 경우에는 독립형 API가 더 적합할 수 있습니다. 초기 검증 후, 이 샘플은 프로젝트의 요구 사항에 따라 맞춤형 봇을 게시할 수 있는 기능을 제공합니다. 할당량, 스로틀링, 출처 등에 대한 설정을 입력하면, API 키와 함께 엔드포인트가 게시되어 다양한 통합 옵션에 대한 유연성을 제공합니다.

## 보안

[AWS API Gateway 개발자 가이드](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)에서 설명한 바와 같이 API 키만 사용하는 것은 권장되지 않습니다. 따라서 이 샘플에서는 AWS WAF를 통한 간단한 IP 주소 제한을 구현합니다. WAF 규칙은 비용을 고려하여 애플리케이션 전체에 공통적으로 적용되며, 제한하고자 하는 소스가 모든 발행된 API에서 동일할 것이라는 가정 하에 적용됩니다. **실제 구현 시에는 조직의 보안 정책을 준수하시기 바랍니다.** 또한 [아키텍처](#architecture) 섹션을 참조하십시오.

## 맞춤형 봇 API 게시 방법

### 사전 요구사항

거버넌스 상의 이유로 제한된 사용자만 봇을 게시할 수 있습니다. 게시하기 전에 사용자는 관리 콘솔 > Amazon Cognito 사용자 풀 또는 aws cli를 통해 설정할 수 있는 `PublishAllowed` 그룹의 멤버여야 합니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`를 통해 참조할 수 있습니다.

![](./imgs/group_membership_publish_allowed.png)

### API 게시 설정

`PublishedAllowed` 사용자로 로그인하고 봇을 생성한 후 `API PublishSettings`를 선택합니다. 공유된 봇만 게시할 수 있다는 점에 유의하세요.
![](./imgs/bot_api_publish_screenshot.png)

다음 화면에서 스로틀링과 관련된 여러 매개변수를 구성할 수 있습니다. 자세한 내용은 다음을 참조하세요: [더 나은 처리량을 위한 API 요청 스로틀링](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

배포 후에는 엔드포인트 URL과 API 키를 얻을 수 있는 다음 화면이 나타납니다. API 키를 추가하고 삭제할 수도 있습니다.

![](./imgs/bot_api_publish_screenshot3.png)

## 아키텍처

API는 다음 다이어그램과 같이 게시됩니다:

![](./imgs/published_arch.png)

WAF는 IP 주소 제한에 사용됩니다. 주소는 `cdk.json`의 `publishedApiAllowedIpV4AddressRanges` 및 `publishedApiAllowedIpV6AddressRanges` 매개변수를 설정하여 구성할 수 있습니다.

사용자가 봇 게시를 클릭하면 [AWS CodeBuild](https://aws.amazon.com/codebuild/)가 API 스택을 프로비저닝하기 위한 CDK 배포 작업을 시작합니다 (참고: [CDK 정의](../cdk/lib/api-publishment-stack.ts)). 이 스택에는 API Gateway, Lambda 및 SQS가 포함됩니다. SQS는 출력 생성이 API Gateway 할당량 제한인 30초를 초과할 수 있기 때문에 사용자 요청과 LLM 작업을 분리하는 데 사용됩니다. 출력을 가져오려면 API에 비동기적으로 접근해야 합니다. 자세한 내용은 [API 명세](#api-specification)를 참조하세요.

클라이언트는 요청 헤더에 `x-api-key`를 설정해야 합니다.

## API 사양

[여기](https://aws-samples.github.io/bedrock-chat)를 참조하세요.