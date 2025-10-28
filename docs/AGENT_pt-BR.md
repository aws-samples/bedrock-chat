# Agente Baseado em LLM (ReAct)

## O que é o Agente (ReAct)?

Um Agente é um sistema avançado de IA que utiliza grandes modelos de linguagem (LLMs) como seu motor computacional central. Ele combina as capacidades de raciocínio dos LLMs com funcionalidades adicionais como planejamento e uso de ferramentas para executar tarefas complexas de forma autônoma. Os Agentes podem decompor consultas complicadas, gerar soluções passo a passo e interagir com ferramentas externas ou APIs para coletar informações ou executar subtarefas.

Esta amostra implementa um Agente usando a abordagem [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). O ReAct permite que o agente resolva tarefas complexas combinando raciocínio e ações em um ciclo de feedback iterativo. O agente passa repetidamente por três etapas principais: Pensamento, Ação e Observação. Ele analisa a situação atual usando o LLM, decide sobre a próxima ação a tomar, executa a ação usando ferramentas ou APIs disponíveis e aprende com os resultados observados. Este processo contínuo permite que o agente se adapte a ambientes dinâmicos, melhore sua precisão na resolução de tarefas e forneça soluções contextualizadas.

A implementação é alimentada pelo [Strands Agents](https://strandsagents.com/), um SDK de código aberto que adota uma abordagem orientada a modelos para construir agentes de IA. O Strands fornece um framework leve e flexível para criar ferramentas personalizadas usando decoradores Python e suporta múltiplos provedores de modelos, incluindo o Amazon Bedrock.

## Exemplo de Caso de Uso

Um Agente usando ReAct pode ser aplicado em vários cenários, fornecendo soluções precisas e eficientes.

### Texto para SQL

Um usuário solicita "o total de vendas do último trimestre." O Agente interpreta essa solicitação, converte-a em uma consulta SQL, executa-a no banco de dados e apresenta os resultados.

### Previsão Financeira

Um analista financeiro precisa prever a receita do próximo trimestre. O Agente coleta dados relevantes, realiza os cálculos necessários usando modelos financeiros e gera um relatório detalhado de previsão, garantindo a precisão das projeções.

## Para usar o recurso de Agente

Para habilitar a funcionalidade de Agente para seu chatbot personalizado, siga estas etapas:

Existem duas maneiras de usar o recurso de Agente:

### Usando Ferramentas

Para habilitar a funcionalidade de Agente com Ferramentas para seu chatbot personalizado, siga estas etapas:

1. Navegue até a seção Agente na tela do bot personalizado.

2. Na seção Agente, você encontrará uma lista de ferramentas disponíveis que podem ser usadas pelo Agente. Por padrão, todas as ferramentas estão desativadas.

3. Para ativar uma ferramenta, simplesmente alterne o botão ao lado da ferramenta desejada. Uma vez que uma ferramenta é habilitada, o Agente terá acesso a ela e poderá utilizá-la ao processar consultas do usuário.

![](./imgs/agent_tools.png)

4. Por exemplo, a ferramenta "Pesquisa na Internet" permite que o Agente busque informações da internet para responder às perguntas do usuário.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Você pode desenvolver e adicionar suas próprias ferramentas personalizadas para estender as capacidades do Agente. Consulte a seção [Como desenvolver suas próprias ferramentas](#how-to-develop-your-own-tools) para mais informações sobre como criar e integrar ferramentas personalizadas.

### Usando Bedrock Agent

Você pode utilizar um [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) criado no Amazon Bedrock.

Primeiro, crie um Agente no Bedrock (por exemplo, via Console de Gerenciamento). Em seguida, especifique o ID do Agente na tela de configurações do bot personalizado. Uma vez configurado, seu chatbot utilizará o Bedrock Agent para processar consultas do usuário.

![](./imgs/bedrock_agent_tool.png)

## Como desenvolver suas próprias ferramentas

Para desenvolver suas próprias ferramentas personalizadas para o Agent usando o Strands SDK, siga estas diretrizes:

### Sobre as Ferramentas Strands

O Strands fornece um decorador `@tool` simples que transforma funções Python regulares em ferramentas do agente de IA. O decorador extrai automaticamente informações da docstring e das dicas de tipo da sua função para criar especificações de ferramentas que o LLM pode entender e usar. Esta abordagem aproveita os recursos nativos do Python para uma experiência limpa e funcional no desenvolvimento de ferramentas.

Para informações detalhadas sobre as ferramentas Strands, consulte a [documentação de Ferramentas Python](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Criação Básica de Ferramentas

Crie uma nova função decorada com o decorador `@tool` do Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Realiza cálculos matemáticos com segurança.

    Args:
        expression: Expressão matemática para avaliar (ex: "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Resultado no formato Strands com toolUseId, status e content
    """
    try:
        # Sua lógica de cálculo aqui
        result = eval(expression)  # Nota: Use avaliação segura em produção
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

### Ferramentas com Contexto do Bot (Padrão Closure)

Para acessar informações do bot (BotModel), use um padrão closure que captura o contexto do bot:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Cria ferramenta de calculadora com closure de contexto do bot."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Realiza cálculos matemáticos com segurança.

        Args:
            expression: Expressão matemática para avaliar (ex: "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Resultado no formato Strands com toolUseId, status e content
        """
        # Acessa o contexto do bot dentro da ferramenta
        if bot:
            print(f"Ferramenta usada pelo bot: {bot.id}")

        try:
            result = eval(expression)  # Use avaliação segura em produção
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

### Requisitos do Formato de Retorno

Todas as ferramentas Strands devem retornar um dicionário com a seguinte estrutura:

```python
{
    "toolUseId": "placeholder",  # Será substituído pelo Strands
    "status": "success" | "error",
    "content": [
        {"text": "Resposta em texto simples"} |
        {"json": {"key": "Objeto de dados complexo"}}
    ]
}
```

- Use `{"text": "mensagem"}` para respostas em texto simples
- Use `{"json": data}` para dados complexos que devem ser preservados como informação estruturada
- Sempre defina `status` como `"success"` ou `"error"`

### Diretrizes de Implementação

- O nome da função e a docstring são usados quando o LLM considera qual ferramenta usar. A docstring é incorporada no prompt, então descreva o propósito e os parâmetros da ferramenta com precisão.

- Consulte a implementação de exemplo de uma [ferramenta de cálculo de IMC](../examples/agents/tools/bmi/bmi_strands.py). Este exemplo demonstra como criar uma ferramenta que calcula o Índice de Massa Corporal (IMC) usando o decorador `@tool` do Strands e o padrão closure.

- Após completar o desenvolvimento, coloque seu arquivo de implementação no diretório [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Em seguida, abra [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) e edite `get_strands_registered_tools` para incluir sua nova ferramenta.

- [Opcional] Adicione nomes e descrições claros para o frontend. Este passo é opcional, mas se você não fizer isso, o nome e a descrição da ferramenta da sua função serão usados. Como estes são para consumo do LLM, é recomendado adicionar explicações amigáveis para melhor UX.

  - Edite os arquivos i18n. Abra [en/index.ts](../frontend/src/i18n/en/index.ts) e adicione seu próprio `name` e `description` em `agent.tools`.
  - Edite `xx/index.ts` também. Onde `xx` representa o código do país desejado.

- Execute `npx cdk deploy` para implantar suas alterações. Isso tornará sua ferramenta personalizada disponível na tela de bot personalizado.