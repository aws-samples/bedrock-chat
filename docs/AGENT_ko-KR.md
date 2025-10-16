# LLM 기반 에이전트(ReAct)

## Agent(ReAct)란 무엇인가?

Agent는 대규모 언어 모델(LLM)을 중앙 연산 엔진으로 활용하는 고급 AI 시스템입니다. LLM의 추론 능력과 계획 수립 및 도구 사용과 같은 추가 기능을 결합하여 복잡한 작업을 자율적으로 수행합니다. Agent는 복잡한 쿼리를 분석하고, 단계별 해결책을 생성하며, 정보를 수집하거나 하위 작업을 실행하기 위해 외부 도구나 API와 상호작용할 수 있습니다.

이 샘플은 [ReAct(Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) 접근 방식을 사용하여 Agent를 구현합니다. ReAct는 추론과 행동을 반복적인 피드백 루프로 결합하여 복잡한 작업을 해결할 수 있게 합니다. Agent는 사고(Thought), 행동(Action), 관찰(Observation)이라는 세 가지 핵심 단계를 반복적으로 수행합니다. LLM을 사용하여 현재 상황을 분석하고, 다음에 취할 행동을 결정하며, 사용 가능한 도구나 API를 사용하여 행동을 실행하고, 관찰된 결과로부터 학습합니다. 이러한 지속적인 프로세스를 통해 Agent는 동적인 환경에 적응하고, 작업 해결의 정확도를 향상시키며, 상황에 맞는 솔루션을 제공할 수 있습니다.

이 구현은 AI 에이전트 구축을 위한 모델 중심 접근 방식을 취하는 오픈소스 SDK인 [Strands Agents](https://strandsagents.com/)를 기반으로 합니다. Strands는 Python 데코레이터를 사용하여 커스텀 도구를 만들 수 있는 경량의 유연한 프레임워크를 제공하며, Amazon Bedrock을 포함한 여러 모델 제공업체를 지원합니다.

## 사용 사례 예시

ReAct를 사용하는 에이전트는 다양한 시나리오에서 적용될 수 있으며, 정확하고 효율적인 솔루션을 제공합니다.

### Text-to-SQL

사용자가 "지난 분기의 총 매출"을 요청합니다. 에이전트는 이 요청을 해석하여 SQL 쿼리로 변환하고, 데이터베이스에서 실행한 후 결과를 제시합니다.

### 재무 예측

재무 분석가가 다음 분기의 수익을 예측해야 합니다. 에이전트는 관련 데이터를 수집하고, 재무 모델을 사용하여 필요한 계산을 수행한 후, 예측의 정확성을 보장하는 상세한 예측 보고서를 생성합니다.

## Agent 기능 사용하기

맞춤형 챗봇에 Agent 기능을 활성화하려면 다음 단계를 따르세요:

Agent 기능을 사용하는 두 가지 방법이 있습니다:

### Tool Use 사용하기

맞춤형 챗봇에 Tool Use를 통한 Agent 기능을 활성화하려면 다음 단계를 따르세요:

1. 맞춤형 봇 화면에서 Agent 섹션으로 이동합니다.

2. Agent 섹션에서 Agent가 사용할 수 있는 도구 목록을 확인할 수 있습니다. 기본적으로 모든 도구는 비활성화되어 있습니다.

3. 도구를 활성화하려면 원하는 도구 옆의 토글 스위치를 켜면 됩니다. 도구가 활성화되면 Agent는 해당 도구에 접근하여 사용자 질의를 처리할 때 활용할 수 있습니다.

![](./imgs/agent_tools.png)

4. 예를 들어, "인터넷 검색" 도구를 사용하면 Agent가 사용자 질문에 답변하기 위해 인터넷에서 정보를 가져올 수 있습니다.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Agent의 기능을 확장하기 위해 자체 맞춤형 도구를 개발하고 추가할 수 있습니다. 맞춤형 도구 생성 및 통합에 대한 자세한 내용은 [자체 도구 개발 방법](#how-to-develop-your-own-tools) 섹션을 참조하세요.

### Bedrock Agent 사용하기

Amazon Bedrock에서 생성된 [Bedrock Agent](https://aws.amazon.com/bedrock/agents/)를 활용할 수 있습니다.

먼저 Bedrock에서 Agent를 생성하고(예: Management Console을 통해), 맞춤형 봇 설정 화면에서 Agent ID를 지정합니다. 설정이 완료되면 챗봇은 사용자 질의를 처리하기 위해 Bedrock Agent를 활용하게 됩니다.

![](./imgs/bedrock_agent_tool.png)

## 자체 도구 개발 방법

Strands SDK를 사용하여 Agent용 커스텀 도구를 개발하려면 다음 가이드라인을 따르세요:

### Strands 도구 소개

Strands는 일반 Python 함수를 AI 에이전트 도구로 변환하는 간단한 `@tool` 데코레이터를 제공합니다. 이 데코레이터는 함수의 docstring과 타입 힌트에서 정보를 자동으로 추출하여 LLM이 이해하고 사용할 수 있는 도구 명세를 생성합니다. 이 접근 방식은 Python의 기본 기능을 활용하여 깔끔하고 기능적인 도구 개발 경험을 제공합니다.

Strands 도구에 대한 자세한 정보는 [Python Tools 문서](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)를 참조하세요.

### 기본 도구 생성

Strands의 `@tool` 데코레이터로 새 함수를 생성하세요:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    안전하게 수학 계산을 수행합니다.

    Args:
        expression: 계산할 수학 표현식 (예: "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: toolUseId, status, content가 포함된 Strands 형식의 결과
    """
    try:
        # 계산 로직 구현
        result = eval(expression)  # 참고: 실제 운영 환경에서는 안전한 평가 사용
        return {
            "toolUseId": "placeholder",
            "status": "success",
            "content": [{"text": str(result)}]
        }
    except Exception as e:
        return {
            "toolUseId": "placeholder",
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }
```

### 봇 컨텍스트가 있는 도구 (클로저 패턴)

봇 정보(BotModel)에 접근하려면 봇 컨텍스트를 캡처하는 클로저 패턴을 사용하세요:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """봇 컨텍스트 클로저로 계산기 도구를 생성합니다."""

    @tool
    def calculator(expression: str) -> dict:
        """
        안전하게 수학 계산을 수행합니다.

        Args:
            expression: 계산할 수학 표현식 (예: "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: toolUseId, status, content가 포함된 Strands 형식의 결과
        """
        # 도구 내에서 봇 컨텍스트 접근
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # 실제 운영 환경에서는 안전한 평가 사용
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"text": str(result)}]
            }
        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Error: {str(e)}"}]
            }

    return calculator
```

### 반환 형식 요구사항

모든 Strands 도구는 다음 구조의 딕셔너리를 반환해야 합니다:

```python
{
    "toolUseId": "placeholder",  # Strands가 대체할 예정
    "status": "success" | "error",
    "content": [
        {"text": "단순 텍스트 응답"} |
        {"json": {"key": "복잡한 데이터 객체"}}
    ]
}
```

- 단순 텍스트 응답에는 `{"text": "메시지"}`를 사용
- 구조화된 정보로 보존해야 하는 복잡한 데이터에는 `{"json": data}`를 사용
- `status`는 항상 `"success"` 또는 `"error"`로 설정

### 구현 가이드라인

- 함수 이름과 docstring은 LLM이 어떤 도구를 사용할지 고려할 때 사용됩니다. docstring은 프롬프트에 포함되므로 도구의 목적과 매개변수를 정확하게 설명하세요.

- [BMI 계산 도구](../examples/agents/tools/bmi/bmi_strands.py)의 샘플 구현을 참조하세요. 이 예제는 Strands `@tool` 데코레이터와 클로저 패턴을 사용하여 체질량 지수(BMI)를 계산하는 도구를 만드는 방법을 보여줍니다.

- 개발을 완료한 후 구현 파일을 [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) 디렉토리에 배치하세요. 그런 다음 [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py)를 열고 `get_strands_registered_tools`를 편집하여 새 도구를 포함시키세요.

- [선택사항] 프론트엔드용 명확한 이름과 설명을 추가하세요. 이 단계는 선택사항이지만, 수행하지 않으면 함수의 도구 이름과 설명이 사용됩니다. 이들은 LLM 소비용이므로 더 나은 UX를 위해 사용자 친화적인 설명을 추가하는 것이 좋습니다.

  - i18n 파일을 편집하세요. [en/index.ts](../frontend/src/i18n/en/index.ts)를 열고 `agent.tools`에 자신만의 `name`과 `description`을 추가하세요.
  - `xx/index.ts`도 편집하세요. 여기서 `xx`는 원하는 국가 코드를 나타냅니다.

- `npx cdk deploy`를 실행하여 변경 사항을 배포하세요. 이렇게 하면 커스텀 봇 화면에서 사용자 정의 도구를 사용할 수 있게 됩니다.