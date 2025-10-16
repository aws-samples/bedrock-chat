# Agent oparty na LLM (ReAct)

## Czym jest Agent (ReAct)?

Agent to zaawansowany system AI wykorzystujący duże modele językowe (LLM) jako główny silnik obliczeniowy. Łączy on możliwości rozumowania LLM z dodatkowymi funkcjonalnościami, takimi jak planowanie i używanie narzędzi, aby autonomicznie wykonywać złożone zadania. Agenty potrafią rozkładać skomplikowane zapytania na części, generować rozwiązania krok po kroku oraz wchodzić w interakcję z zewnętrznymi narzędziami lub API w celu gromadzenia informacji lub wykonywania podzadań.

Ten przykład implementuje Agenta wykorzystując podejście [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct umożliwia agentowi rozwiązywanie złożonych zadań poprzez łączenie rozumowania i działań w iteracyjnej pętli sprzężenia zwrotnego. Agent wielokrotnie przechodzi przez trzy kluczowe etapy: Myślenie, Działanie i Obserwację. Analizuje bieżącą sytuację przy użyciu LLM, decyduje o następnym działaniu do podjęcia, wykonuje działanie przy użyciu dostępnych narzędzi lub API i uczy się z zaobserwowanych wyników. Ten ciągły proces pozwala agentowi adaptować się do dynamicznych środowisk, poprawiać dokładność rozwiązywania zadań i dostarczać rozwiązania dostosowane do kontekstu.

Implementacja jest oparta na [Strands Agents](https://strandsagents.com/), open-source'owym SDK, które przyjmuje podejście oparte na modelach do budowania agentów AI. Strands zapewnia lekki, elastyczny framework do tworzenia niestandardowych narzędzi przy użyciu dekoratorów Pythona i wspiera wielu dostawców modeli, w tym Amazon Bedrock.

## Przykład Zastosowania

Agent wykorzystujący ReAct może być stosowany w różnych scenariuszach, zapewniając dokładne i wydajne rozwiązania.

### Text-to-SQL

Użytkownik pyta o "całkowitą sprzedaż z ostatniego kwartału." Agent interpretuje to zapytanie, przekształca je w zapytanie SQL, wykonuje je w bazie danych i przedstawia wyniki.

### Prognozowanie Finansowe

Analityk finansowy potrzebuje prognozować przychody na następny kwartał. Agent zbiera odpowiednie dane, wykonuje niezbędne obliczenia przy użyciu modeli finansowych i generuje szczegółowy raport prognozy, zapewniając dokładność przewidywań.

## Korzystanie z funkcji Agent

Aby włączyć funkcjonalność Agenta dla swojego spersonalizowanego chatbota, wykonaj następujące kroki:

Istnieją dwa sposoby korzystania z funkcji Agent:

### Korzystanie z narzędzi

Aby włączyć funkcjonalność Agenta z wykorzystaniem narzędzi dla swojego spersonalizowanego chatbota, wykonaj następujące kroki:

1. Przejdź do sekcji Agent na ekranie konfiguracji bota.

2. W sekcji Agent znajdziesz listę dostępnych narzędzi, które mogą być używane przez Agenta. Domyślnie wszystkie narzędzia są wyłączone.

3. Aby aktywować narzędzie, po prostu przełącz przełącznik obok wybranego narzędzia. Po włączeniu narzędzia Agent będzie miał do niego dostęp i będzie mógł z niego korzystać podczas przetwarzania zapytań użytkownika.

![](./imgs/agent_tools.png)

4. Na przykład, narzędzie "Internet Search" pozwala Agentowi pobierać informacje z internetu, aby odpowiadać na pytania użytkowników.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Możesz tworzyć i dodawać własne niestandardowe narzędzia, aby rozszerzyć możliwości Agenta. Więcej informacji na temat tworzenia i integracji własnych narzędzi znajdziesz w sekcji [How to develop your own tools](#how-to-develop-your-own-tools).

### Korzystanie z Bedrock Agent

Możesz wykorzystać [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) utworzonego w Amazon Bedrock.

Najpierw utwórz Agenta w Bedrock (np. przez Management Console). Następnie określ ID Agenta w ekranie ustawień niestandardowego bota. Po skonfigurowaniu Twój chatbot będzie wykorzystywał Bedrock Agent do przetwarzania zapytań użytkowników.

![](./imgs/bedrock_agent_tool.png)

## Jak tworzyć własne narzędzia

Aby stworzyć własne narzędzia dla Agenta przy użyciu Strands SDK, postępuj zgodnie z poniższymi wytycznymi:

### O narzędziach Strands

Strands dostarcza prosty dekorator `@tool`, który przekształca zwykłe funkcje Pythona w narzędzia agenta AI. Dekorator automatycznie wyodrębnia informacje z docstringa i podpowiedzi typów Twojej funkcji, aby stworzyć specyfikacje narzędzi, które LLM może zrozumieć i wykorzystać. To podejście wykorzystuje natywne funkcje Pythona dla przejrzystego, funkcjonalnego doświadczenia w tworzeniu narzędzi.

Szczegółowe informacje o narzędziach Strands znajdziesz w [dokumentacji Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Podstawowe tworzenie narzędzia

Utwórz nową funkcję ozdobioną dekoratorem `@tool` ze Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Wykonuj bezpieczne obliczenia matematyczne.

    Args:
        expression: Wyrażenie matematyczne do obliczenia (np. "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Wynik w formacie Strands z toolUseId, status i content
    """
    try:
        # Tutaj logika obliczeniowa
        result = eval(expression)  # Uwaga: W produkcji użyj bezpiecznej ewaluacji
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

### Narzędzia z kontekstem bota (wzorzec domknięcia)

Aby uzyskać dostęp do informacji o bocie (BotModel), użyj wzorca domknięcia, który przechwytuje kontekst bota:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Tworzy narzędzie kalkulatora z domknięciem kontekstu bota."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Wykonuj bezpieczne obliczenia matematyczne.

        Args:
            expression: Wyrażenie matematyczne do obliczenia (np. "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Wynik w formacie Strands z toolUseId, status i content
        """
        # Dostęp do kontekstu bota w narzędziu
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # W produkcji użyj bezpiecznej ewaluacji
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

### Wymagania dotyczące formatu zwracanego

Wszystkie narzędzia Strands muszą zwracać słownik o następującej strukturze:

```python
{
    "toolUseId": "placeholder",  # Zostanie zastąpione przez Strands
    "status": "success" | "error",
    "content": [
        {"text": "Prosta odpowiedź tekstowa"} |
        {"json": {"key": "Złożony obiekt danych"}}
    ]
}
```

- Użyj `{"text": "wiadomość"}` dla prostych odpowiedzi tekstowych
- Użyj `{"json": data}` dla złożonych danych, które powinny zachować strukturę
- Zawsze ustawiaj `status` na `"success"` lub `"error"`

### Wytyczne implementacji

- Nazwa funkcji i docstring są używane, gdy LLM rozważa, którego narzędzia użyć. Docstring jest osadzony w promptcie, więc dokładnie opisz cel i parametry narzędzia.

- Zapoznaj się z przykładową implementacją [narzędzia do obliczania BMI](../examples/agents/tools/bmi/bmi_strands.py). Ten przykład pokazuje, jak stworzyć narzędzie obliczające Wskaźnik Masy Ciała (BMI) przy użyciu dekoratora `@tool` i wzorca domknięcia Strands.

- Po zakończeniu tworzenia umieść plik implementacji w katalogu [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Następnie otwórz [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) i edytuj `get_strands_registered_tools`, aby dodać swoje nowe narzędzie.

- [Opcjonalnie] Dodaj czytelne nazwy i opisy dla frontendu. Ten krok jest opcjonalny, ale jeśli go nie wykonasz, zostanie użyta nazwa i opis funkcji. Ponieważ są one przeznaczone dla LLM, zaleca się dodanie przyjaznych dla użytkownika objaśnień dla lepszego UX.

  - Edytuj pliki i18n. Otwórz [en/index.ts](../frontend/src/i18n/en/index.ts) i dodaj własną `name` i `description` w `agent.tools`.
  - Edytuj również `xx/index.ts`. Gdzie `xx` reprezentuje kod kraju, który chcesz.

- Uruchom `npx cdk deploy`, aby wdrożyć zmiany. Spowoduje to udostępnienie Twojego niestandardowego narzędzia na ekranie niestandardowego bota.