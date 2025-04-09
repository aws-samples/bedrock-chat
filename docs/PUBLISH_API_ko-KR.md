# API 게시

## 개요

이 샘플에는 API 게시 기능이 포함되어 있습니다. 채팅 인터페이스는 예비 검증에 편리할 수 있지만, 실제 구현은 최종 사용자를 위한 특정 사용 사례와 사용자 경험(UX)에 따라 달라집니다. 일부 시나리오에서는 채팅 UI가 선호될 수 있는 반면, 다른 경우에는 독립형 API가 더 적합할 수 있습니다. 초기 검증 후, 이 샘플은 프로젝트의 요구 사항에 따라 맞춤형 봇을 게시할 수 있는 기능을 제공합니다. 할당량, 스로틀링, 출처 등에 대한 설정을 입력함으로써, API 키와 함께 엔드포인트를 게시할 수 있어 다양한 통합 옵션에 유연성을 제공합니다.

## 보안

[AWS API Gateway 개발자 가이드](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)에 설명된 대로 API 키만 사용하는 것은 권장되지 않습니다. 결과적으로, 이 샘플은 AWS WAF를 통한 간단한 IP 주소 제한을 구현합니다. WAF 규칙은 비용 고려 사항으로 인해 애플리케이션 전체에 공통적으로 적용되며, 제한하려는 소스가 발급된 모든 API에서 동일할 가능성이 높다는 가정 하에 적용됩니다. **실제 구현에서는 조직의 보안 정책을 준수해야 합니다.** [아키텍처](#architecture) 섹션도 참조하세요.

## 사용자 정의 봇 API 게시 방법

### 사전 요구 사항

거버넌스 이유로, 제한된 사용자만 봇을 게시할 수 있습니다. 게시 전에 사용자는 `PublishAllowed`라는 그룹의 구성원이어야 하며, 이는 관리 콘솔 > Amazon Cognito 사용자 풀 또는 AWS CLI를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > 출력 > `AuthUserPoolIdxxxx`에 액세스하여 참조할 수 있습니다.

![](./imgs/group_membership_publish_allowed.png)

### API 게시 설정

`PublishedAllowed` 사용자로 로그인하고 봇을 생성한 후, `API 게시 설정`을 선택합니다. 공유 봇만 게시할 수 있습니다.
![](./imgs/bot_api_publish_screenshot.png)

다음 화면에서 스로틀링과 관련된 여러 매개변수를 구성할 수 있습니다. 자세한 내용은 다음을 참조하세요: [더 나은 처리량을 위해 API 요청 스로틀링](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

배포 후 다음 화면이 나타나며, 여기서 엔드포인트 URL과 API 키를 얻을 수 있습니다. API 키를 추가하고 삭제할 수도 있습니다.

![](./imgs/bot_api_publish_screenshot3.png)

## 아키텍처

API는 다음 다이어그램과 같이 게시됩니다:

![](./imgs/published_arch.png)

WAF는 IP 주소 제한에 사용됩니다. 주소는 `cdk.json`의 `publishedApiAllowedIpV4AddressRanges` 및 `publishedApiAllowedIpV6AddressRanges` 매개변수를 설정하여 구성할 수 있습니다.

사용자가 봇을 게시하면 [AWS CodeBuild](https://aws.amazon.com/codebuild/)가 CDK 배포 작업을 시작하여 API 스택(참조: [CDK 정의](../cdk/lib/api-publishment-stack.ts))을 프로비저닝합니다. 이 스택에는 API Gateway, Lambda, SQS가 포함됩니다. SQS는 사용자 요청과 LLM 작업을 분리하는 데 사용됩니다. 출력 생성에 30초 이상이 걸릴 수 있으며, 이는 API Gateway 할당량의 제한을 초과합니다. 출력을 가져오려면 API에 비동기적으로 액세스해야 합니다. 자세한 내용은 [API 사양](#api-specification)을 참조하세요.

클라이언트는 요청 헤더에 `x-api-key`를 설정해야 합니다.

## API 사양

[여기](https://aws-samples.github.io/bedrock-chat)를 참조하세요.