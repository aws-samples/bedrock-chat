# 관리자 기능

관리자 기능은 맞춤형 봇 사용과 사용자 행동에 대한 핵심적인 통찰력을 제공하는 중요한 도구입니다. 이 기능이 없다면 관리자가 어떤 맞춤형 봇이 인기 있는지, 그 이유는 무엇인지, 그리고 누가 사용하고 있는지를 파악하기 어려울 것입니다. 이 정보는 지시 프롬프트 최적화, RAG 데이터 소스 맞춤화, 그리고 잠재적 영향력 있는 헤비 사용자를 식별하는 데 매우 중요합니다.

## 피드백 루프

LLM의 출력이 항상 사용자의 기대에 부합하는 것은 아닙니다. 때때로 사용자의 요구를 만족시키지 못할 수 있습니다. LLM을 비즈니스 운영 및 일상생활에 효과적으로 "통합"하기 위해서는 피드백 루프를 구현하는 것이 필수적입니다. Bedrock Claude Chat은 사용자가 불만족의 원인을 분석할 수 있도록 설계된 피드백 기능을 갖추고 있습니다. 분석 결과를 바탕으로 사용자는 프롬프트, RAG 데이터 소스 및 매개변수를 적절히 조정할 수 있습니다.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

데이터 분석가들은 [Amazon Athena](https://aws.amazon.com/jp/athena/)를 사용하여 대화 로그에 접근할 수 있습니다. [Jupyter Notebook](https://jupyter.org/)으로 데이터를 분석하고 싶다면, [이 노트북 예시](../examples/notebooks/feedback_analysis_example.ipynb)를 참고할 수 있습니다.

## 관리자 대시보드

현재 챗봇 및 사용자 사용량에 대한 기본적인 개요를 제공하며, 지정된 기간 동안 각 봇과 사용자의 데이터를 집계하고 사용 요금별로 결과를 정렬합니다.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> 사용자 사용량 분석은 곧 제공될 예정입니다.

### 전제 조건

관리자 사용자는 `Admin`이라는 그룹의 구성원이어야 하며, 이는 관리 콘솔 > Amazon Cognito 사용자 풀 또는 AWS CLI를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > 출력 > `AuthUserPoolIdxxxx`에 액세스하여 참조할 수 있습니다.

![](./imgs/group_membership_admin.png)

## 참고사항

- [아키텍처](../README.md#architecture)에서 언급된 바와 같이, 관리자 기능은 DynamoDB에서 내보낸 S3 버킷을 참조합니다. 내보내기가 매시간 한 번 수행되므로 최신 대화가 즉시 반영되지 않을 수 있습니다.

- 공개 봇 사용량에서는 지정된 기간 동안 전혀 사용되지 않은 봇은 나열되지 않습니다.

- 사용자 사용량에서는 지정된 기간 동안 시스템을 전혀 사용하지 않은 사용자는 나열되지 않습니다.

> [!중요] > **다중 환경 데이터베이스 이름**
>
> 여러 환경(dev, prod 등)을 사용하는 경우, Athena 데이터베이스 이름에 환경 접두사가 포함됩니다. `bedrockchatstack_usage_analysis` 대신 데이터베이스 이름은 다음과 같습니다:
>
> - 기본 환경의 경우: `bedrockchatstack_usage_analysis`
> - 명명된 환경의 경우: `<env-prefix>_bedrockchatstack_usage_analysis` (예: `dev_bedrockchatstack_usage_analysis`)
>
> 또한 테이블 이름에도 환경 접두사가 포함됩니다:
>
> - 기본 환경의 경우: `ddb_export`
> - 명명된 환경의 경우: `<env-prefix>_ddb_export` (예: `dev_ddb_export`)
>
> 여러 환경에서 작업할 때는 쿼리를 적절히 조정해야 합니다.

## 대화 데이터 다운로드

Athena를 사용하여 SQL로 대화 로그를 조회할 수 있습니다. 로그를 다운로드하려면 관리 콘솔에서 Athena 쿼리 편집기를 열고 SQL을 실행하세요. 다음은 사용 사례를 분석하는 데 유용한 예제 쿼리입니다. 피드백은 `MessageMap` 속성에서 참조할 수 있습니다.

### 봇 ID별 쿼리

`bot-id`와 `datehour`를 편집하세요. `bot-id`는 봇 관리 화면에서 참조할 수 있으며, Bot Publish API를 통해 왼쪽 사이드바에 표시됩니다. URL의 끝 부분(예: `https://xxxx.cloudfront.net/admin/bot/<bot-id>`)을 참고하세요.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!참고]
> 명명된 환경(예: "dev")을 사용하는 경우, 위 쿼리의 `bedrockchatstack_usage_analysis.ddb_export`를 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`로 대체하세요.

### 사용자 ID별 쿼리

`user-id`와 `datehour`를 편집하세요. `user-id`는 봇 관리 화면에서 참조할 수 있습니다.

> [!참고]
> 사용자 사용 분석은 곧 제공될 예정입니다.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!참고]
> 명명된 환경(예: "dev")을 사용하는 경우, 위 쿼리의 `bedrockchatstack_usage_analysis.ddb_export`를 `dev_bedrockchatstack_usage_analysis.dev_ddb_export`로 대체하세요.