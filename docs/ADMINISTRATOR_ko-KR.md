# 관리 기능

## 전제 조건

관리자 사용자는 `Admin` 그룹의 구성원이어야 하며, 이 그룹은 관리 콘솔 > Amazon Cognito 사용자 풀 또는 AWS CLI를 통해 설정할 수 있습니다. 사용자 풀 ID는 CloudFormation > BedrockChatStack > 출력 > `AuthUserPoolIdxxxx`를 통해 확인할 수 있습니다.

![](./imgs/group_membership_admin.png)

## 공개 봇을 필수(Essential)로 표시

이제 관리자는 공개 봇을 "필수(Essential)"로 표시할 수 있습니다. 필수로 표시된 봇은 봇 스토어의 "필수" 섹션에 특별히 게재되어 사용자가 쉽게 접근할 수 있습니다. 이를 통해 관리자는 모든 사용자가 사용해야 할 중요한 봇을 고정할 수 있습니다.

### 예시

- HR 도우미 봇: 직원들의 HR 관련 질문과 업무를 지원합니다.
- IT 지원 봇: 내부 기술 문제 및 계정 관리에 대한 지원을 제공합니다.
- 내부 정책 가이드 봇: 출석 규칙, 보안 정책 및 기타 내부 규정에 대한 자주 묻는 질문에 답변합니다.
- 신입 사원 온보딩 봇: 첫날 신입 직원들에게 절차 및 시스템 사용법을 안내합니다.
- 복리후생 정보 봇: 회사의 복리후생 프로그램과 복지 서비스를 설명합니다.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## 피드백 루프

LLM의 출력이 항상 사용자의 기대를 충족시키는 것은 아닙니다. 때때로 사용자의 요구를 만족시키지 못할 수 있습니다. LLM을 비즈니스 운영 및 일상생활에 효과적으로 "통합"하기 위해서는 피드백 루프를 구현하는 것이 필수적입니다. Bedrock Chat은 사용자가 불만족의 원인을 분석할 수 있도록 설계된 피드백 기능을 갖추고 있습니다. 분석 결과를 바탕으로 사용자는 프롬프트, RAG 데이터 소스 및 매개변수를 적절히 조정할 수 있습니다.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

데이터 분석가는 [Amazon Athena](https://aws.amazon.com/jp/athena/)를 사용하여 대화 로그에 접근할 수 있습니다. [Jupyter Notebook](https://jupyter.org/)으로 데이터를 분석하고 싶다면, [이 노트북 예시](../examples/notebooks/feedback_analysis_example.ipynb)를 참고할 수 있습니다.

## 대시보드

현재는 챗봇과 사용자 사용량에 대한 기본적인 개요를 제공하며, 특정 기간 동안 각 봇과 사용자에 대한 데이터를 집계하고 사용 요금별로 결과를 정렬합니다.

![](./imgs/admin_bot_analytics.png)

## 참고사항

- [아키텍처](../README.md#architecture)에서 언급된 대로, 관리자 기능은 DynamoDB에서 내보낸 S3 버킷을 참조합니다. 내보내기가 매시간 한 번 수행되므로 최신 대화가 즉시 반영되지 않을 수 있습니다.

- 공개 봇 사용량에서는 지정된 기간 동안 전혀 사용되지 않은 봇은 나열되지 않습니다.

- 사용자 사용량에서는 지정된 기간 동안 시스템을 전혀 사용하지 않은 사용자는 나열되지 않습니다.

> [!중요]
> 여러 환경(개발, 운영 등)을 사용하는 경우, Athena 데이터베이스 이름에 환경 접두사가 포함됩니다. `bedrockchatstack_usage_analysis` 대신 데이터베이스 이름은 다음과 같습니다:
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

Athena를 사용하여 SQL로 대화 로그를 쿼리할 수 있습니다. 로그를 다운로드하려면 관리 콘솔에서 Athena 쿼리 편집기를 열고 SQL을 실행하세요. 다음은 사용 사례를 분석하는 데 유용한 예시 쿼리입니다. 피드백은 `MessageMap` 속성에서 참조할 수 있습니다.

### 봇 ID별 쿼리

`bot-id`와 `datehour`를 편집하세요. `bot-id`는 봇 관리 화면에서 참조할 수 있으며, 왼쪽 사이드바의 봇 게시 API에서 접근할 수 있습니다. URL의 마지막 부분(예: `https://xxxx.cloudfront.net/admin/bot/<bot-id>`)을 참고하세요.

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