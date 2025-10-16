# LLM-gesteuerter Agent (ReAct)

## Was ist der Agent (ReAct)?

Ein Agent ist ein fortschrittliches KI-System, das große Sprachmodelle (LLMs) als zentrale Recheneinheit nutzt. Er kombiniert die Reasoning-Fähigkeiten von LLMs mit zusätzlichen Funktionen wie Planung und Werkzeugnutzung, um eigenständig komplexe Aufgaben auszuführen. Agenten können komplizierte Anfragen aufschlüsseln, schrittweise Lösungen generieren und mit externen Tools oder APIs interagieren, um Informationen zu sammeln oder Teilaufgaben auszuführen.

Dieses Beispiel implementiert einen Agenten unter Verwendung des [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) Ansatzes. ReAct ermöglicht es dem Agenten, komplexe Aufgaben durch die Kombination von Reasoning und Aktionen in einer iterativen Feedback-Schleife zu lösen. Der Agent durchläuft wiederholt drei wichtige Schritte: Thought (Denken), Action (Handeln) und Observation (Beobachten). Er analysiert die aktuelle Situation mithilfe des LLM, entscheidet über die nächste auszuführende Aktion, führt die Aktion mit verfügbaren Tools oder APIs aus und lernt aus den beobachteten Ergebnissen. Dieser kontinuierliche Prozess ermöglicht es dem Agenten, sich an dynamische Umgebungen anzupassen, seine Problemlösungsgenauigkeit zu verbessern und kontextbezogene Lösungen anzubieten.

Die Implementierung basiert auf [Strands Agents](https://strandsagents.com/), einem Open-Source-SDK, das einen modellgetriebenen Ansatz zum Aufbau von KI-Agenten verfolgt. Strands bietet ein leichtgewichtiges, flexibles Framework für die Erstellung benutzerdefinierter Tools mithilfe von Python-Dekoratoren und unterstützt mehrere Modellanbieter, einschließlich Amazon Bedrock.

## Anwendungsbeispiel

Ein Agent, der ReAct verwendet, kann in verschiedenen Szenarien eingesetzt werden und bietet präzise und effiziente Lösungen.

### Text-zu-SQL

Ein Benutzer fragt nach "dem Gesamtumsatz des letzten Quartals". Der Agent interpretiert diese Anfrage, wandelt sie in eine SQL-Abfrage um, führt diese in der Datenbank aus und präsentiert die Ergebnisse.

### Finanzprognosen

Ein Finanzanalyst muss den Umsatz für das nächste Quartal prognostizieren. Der Agent sammelt relevante Daten, führt die erforderlichen Berechnungen mithilfe von Finanzmodellen durch und erstellt einen detaillierten Prognosebericht, wobei er die Genauigkeit der Projektionen sicherstellt.

## Verwendung der Agent-Funktion

Um die Agent-Funktionalität für Ihren angepassten Chatbot zu aktivieren, folgen Sie diesen Schritten:

Es gibt zwei Möglichkeiten, die Agent-Funktion zu nutzen:

### Verwendung von Tool Use

Um die Agent-Funktionalität mit Tool Use für Ihren angepassten Chatbot zu aktivieren, folgen Sie diesen Schritten:

1. Navigieren Sie zum Agent-Bereich im Bildschirm des benutzerdefinierten Bots.

2. Im Agent-Bereich finden Sie eine Liste der verfügbaren Tools, die vom Agent genutzt werden können. Standardmäßig sind alle Tools deaktiviert.

3. Um ein Tool zu aktivieren, schalten Sie einfach den Schalter neben dem gewünschten Tool um. Sobald ein Tool aktiviert ist, hat der Agent Zugriff darauf und kann es bei der Verarbeitung von Benutzeranfragen nutzen.

![](./imgs/agent_tools.png)

4. Zum Beispiel ermöglicht das "Internet Search"-Tool dem Agent, Informationen aus dem Internet abzurufen, um Benutzerfragen zu beantworten.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Sie können eigene benutzerdefinierte Tools entwickeln und hinzufügen, um die Fähigkeiten des Agents zu erweitern. Weitere Informationen zum Erstellen und Integrieren benutzerdefinierter Tools finden Sie im Abschnitt [How to develop your own tools](#how-to-develop-your-own-tools).

### Verwendung von Bedrock Agent

Sie können einen [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) verwenden, der in Amazon Bedrock erstellt wurde.

Erstellen Sie zunächst einen Agent in Bedrock (z.B. über die Management Console). Geben Sie dann die Agent-ID im Einstellungsbildschirm des benutzerdefinierten Bots an. Sobald dies eingerichtet ist, wird Ihr Chatbot den Bedrock Agent nutzen, um Benutzeranfragen zu verarbeiten.

![](./imgs/bedrock_agent_tool.png)

## So entwickeln Sie Ihre eigenen Tools

Um eigene benutzerdefinierte Tools für den Agent mit dem Strands SDK zu entwickeln, befolgen Sie diese Richtlinien:

### Über Strands Tools

Strands bietet einen einfachen `@tool` Decorator, der reguläre Python-Funktionen in AI-Agent-Tools umwandelt. Der Decorator extrahiert automatisch Informationen aus dem Docstring und den Type-Hints Ihrer Funktion, um Tool-Spezifikationen zu erstellen, die das LLM verstehen und nutzen kann. Dieser Ansatz nutzt die nativen Python-Funktionen für eine saubere, funktionale Tool-Entwicklungserfahrung.

Detaillierte Informationen zu Strands Tools finden Sie in der [Python Tools Dokumentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Grundlegende Tool-Erstellung

Erstellen Sie eine neue Funktion, die mit dem `@tool` Decorator von Strands versehen ist:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Führt mathematische Berechnungen sicher aus.

    Args:
        expression: Mathematischer Ausdruck zur Auswertung (z.B. "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Ergebnis im Strands-Format mit toolUseId, status und content
    """
    try:
        # Ihre Berechnungslogik hier
        result = eval(expression)  # Hinweis: Verwenden Sie sichere Auswertung in Produktion
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

### Tools mit Bot-Kontext (Closure-Pattern)

Um auf Bot-Informationen (BotModel) zuzugreifen, verwenden Sie ein Closure-Pattern, das den Bot-Kontext erfasst:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Erstellt Calculator-Tool mit Bot-Kontext-Closure."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Führt mathematische Berechnungen sicher aus.

        Args:
            expression: Mathematischer Ausdruck zur Auswertung (z.B. "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Ergebnis im Strands-Format mit toolUseId, status und content
        """
        # Zugriff auf Bot-Kontext innerhalb des Tools
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Verwenden Sie sichere Auswertung in Produktion
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

### Anforderungen an das Rückgabeformat

Alle Strands Tools müssen ein Dictionary mit folgender Struktur zurückgeben:

```python
{
    "toolUseId": "placeholder",  # Wird von Strands ersetzt
    "status": "success" | "error",
    "content": [
        {"text": "Einfache Textantwort"} |
        {"json": {"key": "Komplexes Datenobjekt"}}
    ]
}
```

- Verwenden Sie `{"text": "message"}` für einfache Textantworten
- Verwenden Sie `{"json": data}` für komplexe Daten, die als strukturierte Information erhalten bleiben sollen
- Setzen Sie `status` immer entweder auf `"success"` oder `"error"`

### Implementierungsrichtlinien

- Der Funktionsname und Docstring werden verwendet, wenn das LLM entscheidet, welches Tool zu verwenden ist. Der Docstring wird in den Prompt eingebettet, beschreiben Sie daher den Zweck und die Parameter des Tools präzise.

- Siehe die Beispielimplementierung eines [BMI-Berechnungstools](../examples/agents/tools/bmi/bmi_strands.py). Dieses Beispiel zeigt, wie man ein Tool erstellt, das den Body Mass Index (BMI) mit dem Strands `@tool` Decorator und Closure-Pattern berechnet.

- Nach Abschluss der Entwicklung platzieren Sie Ihre Implementierungsdatei im Verzeichnis [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Öffnen Sie dann [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) und bearbeiten Sie `get_strands_registered_tools`, um Ihr neues Tool einzubinden.

- [Optional] Fügen Sie klare Namen und Beschreibungen für das Frontend hinzu. Dieser Schritt ist optional, aber wenn Sie ihn nicht durchführen, werden der Tool-Name und die Beschreibung aus Ihrer Funktion verwendet. Da diese für den LLM-Konsum gedacht sind, wird empfohlen, benutzerfreundliche Erklärungen für eine bessere UX hinzuzufügen.

  - Bearbeiten Sie i18n-Dateien. Öffnen Sie [en/index.ts](../frontend/src/i18n/en/index.ts) und fügen Sie Ihren eigenen `name` und `description` unter `agent.tools` hinzu.
  - Bearbeiten Sie auch `xx/index.ts`. Wobei `xx` für den gewünschten Ländercode steht.

- Führen Sie `npx cdk deploy` aus, um Ihre Änderungen zu deployen. Dadurch wird Ihr benutzerdefiniertes Tool im Custom-Bot-Bildschirm verfügbar.