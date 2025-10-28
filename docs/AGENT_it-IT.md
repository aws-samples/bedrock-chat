# Agente basato su LLM (ReAct)

## Che cos'è l'Agente (ReAct)?

Un Agente è un sistema di IA avanzato che utilizza i modelli linguistici di grandi dimensioni (LLM) come motore computazionale centrale. Combina le capacità di ragionamento degli LLM con funzionalità aggiuntive come la pianificazione e l'uso di strumenti per eseguire autonomamente compiti complessi. Gli Agenti possono scomporre query complicate, generare soluzioni passo dopo passo e interagire con strumenti esterni o API per raccogliere informazioni o eseguire attività secondarie.

Questo esempio implementa un Agente utilizzando l'approccio [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct permette all'agente di risolvere compiti complessi combinando ragionamento e azioni in un ciclo di feedback iterativo. L'agente attraversa ripetutamente tre passaggi chiave: Pensiero, Azione e Osservazione. Analizza la situazione attuale utilizzando l'LLM, decide quale azione intraprendere successivamente, esegue l'azione utilizzando strumenti o API disponibili e apprende dai risultati osservati. Questo processo continuo permette all'agente di adattarsi a ambienti dinamici, migliorare la precisione nella risoluzione dei compiti e fornire soluzioni contestualizzate.

L'implementazione è basata su [Strands Agents](https://strandsagents.com/), un SDK open-source che adotta un approccio model-driven per la costruzione di agenti IA. Strands fornisce un framework leggero e flessibile per creare strumenti personalizzati utilizzando i decoratori Python e supporta diversi provider di modelli, incluso Amazon Bedrock.

## Esempio di Caso d'Uso

Un Agente che utilizza ReAct può essere applicato in vari scenari, fornendo soluzioni accurate ed efficienti.

### Da Testo a SQL

Un utente chiede "il totale delle vendite dell'ultimo trimestre". L'Agente interpreta questa richiesta, la converte in una query SQL, la esegue sul database e presenta i risultati.

### Previsioni Finanziarie

Un analista finanziario deve prevedere i ricavi del prossimo trimestre. L'Agente raccoglie i dati pertinenti, esegue i calcoli necessari utilizzando modelli finanziari e genera un rapporto dettagliato delle previsioni, garantendo l'accuratezza delle proiezioni.

## Per utilizzare la funzionalità Agent

Per abilitare la funzionalità Agent per il tuo chatbot personalizzato, segui questi passaggi:

Ci sono due modi per utilizzare la funzionalità Agent:

### Utilizzo degli Strumenti (Tool Use)

Per abilitare la funzionalità Agent con l'utilizzo degli strumenti per il tuo chatbot personalizzato, segui questi passaggi:

1. Vai alla sezione Agent nella schermata del bot personalizzato.

2. Nella sezione Agent, troverai un elenco di strumenti disponibili che possono essere utilizzati dall'Agent. Per impostazione predefinita, tutti gli strumenti sono disabilitati.

3. Per attivare uno strumento, basta attivare l'interruttore accanto allo strumento desiderato. Una volta abilitato uno strumento, l'Agent avrà accesso ad esso e potrà utilizzarlo durante l'elaborazione delle richieste degli utenti.

![](./imgs/agent_tools.png)

4. Per esempio, lo strumento "Internet Search" permette all'Agent di recuperare informazioni da internet per rispondere alle domande degli utenti.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Puoi sviluppare e aggiungere i tuoi strumenti personalizzati per estendere le capacità dell'Agent. Consulta la sezione [How to develop your own tools](#how-to-develop-your-own-tools) per maggiori informazioni sulla creazione e l'integrazione di strumenti personalizzati.

### Utilizzo di Bedrock Agent

Puoi utilizzare un [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) creato in Amazon Bedrock.

Prima, crea un Agent in Bedrock (ad esempio, tramite la Management Console). Quindi, specifica l'ID dell'Agent nella schermata delle impostazioni del bot personalizzato. Una volta impostato, il tuo chatbot utilizzerà il Bedrock Agent per elaborare le richieste degli utenti.

![](./imgs/bedrock_agent_tool.png)

## Come sviluppare i propri strumenti

Per sviluppare i tuoi strumenti personalizzati per l'Agent utilizzando Strands SDK, segui queste linee guida:

### Informazioni sugli Strumenti Strands

Strands fornisce un semplice decoratore `@tool` che trasforma le normali funzioni Python in strumenti per l'agente AI. Il decoratore estrae automaticamente le informazioni dalla docstring della tua funzione e dai type hints per creare specifiche dello strumento che l'LLM può comprendere e utilizzare. Questo approccio sfrutta le funzionalità native di Python per un'esperienza di sviluppo degli strumenti pulita e funzionale.

Per informazioni dettagliate sugli strumenti Strands, consulta la [documentazione Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Creazione Base di uno Strumento

Crea una nuova funzione decorata con il decoratore `@tool` di Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Esegue calcoli matematici in modo sicuro.

    Args:
        expression: Espressione matematica da valutare (es. "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Risultato in formato Strands con toolUseId, status e content
    """
    try:
        # La tua logica di calcolo qui
        result = eval(expression)  # Nota: Usa una valutazione sicura in produzione
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

### Strumenti con Contesto Bot (Pattern Closure)

Per accedere alle informazioni del bot (BotModel), usa un pattern closure che cattura il contesto del bot:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Crea uno strumento calcolatrice con closure del contesto bot."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Esegue calcoli matematici in modo sicuro.

        Args:
            expression: Espressione matematica da valutare (es. "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Risultato in formato Strands con toolUseId, status e content
        """
        # Accedi al contesto del bot all'interno dello strumento
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Usa una valutazione sicura in produzione
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

### Requisiti del Formato di Ritorno

Tutti gli strumenti Strands devono restituire un dizionario con la seguente struttura:

```python
{
    "toolUseId": "placeholder",  # Sarà sostituito da Strands
    "status": "success" | "error",
    "content": [
        {"text": "Risposta testuale semplice"} |
        {"json": {"key": "Oggetto dati complesso"}}
    ]
}
```

- Usa `{"text": "messaggio"}` per risposte testuali semplici
- Usa `{"json": data}` per dati complessi che devono essere preservati come informazioni strutturate
- Imposta sempre `status` su `"success"` o `"error"`

### Linee Guida per l'Implementazione

- Il nome della funzione e la docstring vengono utilizzati quando l'LLM considera quale strumento utilizzare. La docstring viene incorporata nel prompt, quindi descrivi lo scopo e i parametri dello strumento con precisione.

- Fai riferimento all'implementazione di esempio di uno [strumento per il calcolo del BMI](../examples/agents/tools/bmi/bmi_strands.py). Questo esempio dimostra come creare uno strumento che calcola l'Indice di Massa Corporea (BMI) utilizzando il decoratore `@tool` di Strands e il pattern closure.

- Dopo aver completato lo sviluppo, posiziona il tuo file di implementazione nella directory [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Quindi apri [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) e modifica `get_strands_registered_tools` per includere il tuo nuovo strumento.

- [Opzionale] Aggiungi nomi e descrizioni chiari per il frontend. Questo passaggio è opzionale, ma se non lo fai, verranno utilizzati il nome e la descrizione della funzione. Poiché questi sono per il consumo dell'LLM, si raccomanda di aggiungere spiegazioni user-friendly per una migliore UX.

  - Modifica i file i18n. Apri [en/index.ts](../frontend/src/i18n/en/index.ts) e aggiungi il tuo `name` e `description` su `agent.tools`.
  - Modifica anche `xx/index.ts`. Dove `xx` rappresenta il codice paese che desideri.

- Esegui `npx cdk deploy` per distribuire le tue modifiche. Questo renderà il tuo strumento personalizzato disponibile nella schermata dei bot personalizzati.