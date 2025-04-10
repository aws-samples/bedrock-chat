# Agente basato su LLM (ReAct)

## Cos'è l'Agente (ReAct)?

Un Agente è un sistema di intelligenza artificiale avanzato che utilizza i modelli di linguaggio di grandi dimensioni (LLM) come motore computazionale centrale. Combina le capacità di ragionamento degli LLM con funzionalità aggiuntive come pianificazione e utilizzo di strumenti per eseguire autonomamente compiti complessi. Gli Agenti possono scomporre query complicate, generare soluzioni passo dopo passo e interagire con strumenti o API esterne per raccogliere informazioni o eseguire sottoattività.

Questo esempio implementa un Agente utilizzando l'approccio [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct consente all'agente di risolvere compiti complessi combinando ragionamento e azioni in un ciclo di feedback iterativo. L'agente passa ripetutamente attraverso tre fasi chiave: Pensiero, Azione e Osservazione. Analizza la situazione corrente utilizzando l'LLM, decide l'azione successiva da intraprendere, esegue l'azione utilizzando strumenti o API disponibili e impara dai risultati osservati. Questo processo continuo permette all'agente di adattarsi ad ambienti dinamici, migliorare la precisione nella risoluzione dei compiti e fornire soluzioni consapevoli del contesto.

## Caso d'Uso Esemplificativo

Un Agente che utilizza ReAct può essere applicato in vari scenari, fornendo soluzioni accurate ed efficienti.

### Da Testo a SQL

Un utente chiede "il totale delle vendite dell'ultimo trimestre". L'Agente interpreta questa richiesta, la converte in una query SQL, la esegue sul database e presenta i risultati.

### Previsioni Finanziarie

Un analista finanziario necessita di prevedere il fatturato del prossimo trimestre. L'Agente raccoglie i dati rilevanti, esegue i calcoli necessari utilizzando modelli finanziari e genera un rapporto di previsione dettagliato, garantendo l'accuratezza delle proiezioni.

## Come utilizzare la funzionalità Agent

Per abilitare la funzionalità Agent per il tuo chatbot personalizzato, segui questi passaggi:

Esistono due modi per utilizzare la funzionalità Agent:

### Utilizzo di Tool Use

Per abilitare la funzionalità Agent con Tool Use per il tuo chatbot personalizzato, segui questi passaggi:

1. Naviga nella sezione Agent nella schermata del bot personalizzato.

2. Nella sezione Agent, troverai un elenco di strumenti disponibili che possono essere utilizzati dall'Agent. Per impostazione predefinita, tutti gli strumenti sono disabilitati.

3. Per attivare uno strumento, passa semplicemente l'interruttore accanto allo strumento desiderato. Una volta abilitato uno strumento, l'Agent avrà accesso ad esso e potrà utilizzarlo durante l'elaborazione delle query dell'utente.

![](./imgs/agent_tools.png)

4. Ad esempio, lo strumento "Ricerca Internet" consente all'Agent di recuperare informazioni da internet per rispondere alle domande degli utenti.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Puoi sviluppare e aggiungere i tuoi strumenti personalizzati per estendere le capacità dell'Agent. Consulta la sezione [Come sviluppare i tuoi strumenti](#how-to-develop-your-own-tools) per ulteriori informazioni sulla creazione e l'integrazione di strumenti personalizzati.

### Utilizzo di Bedrock Agent

Puoi utilizzare un [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) creato in Amazon Bedrock.

Innanzitutto, crea un Agent in Bedrock (ad esempio tramite la Console di Gestione). Quindi, specifica l'ID dell'Agent nelle impostazioni del bot personalizzato. Una volta impostato, il tuo chatbot sfrutterà il Bedrock Agent per elaborare le query degli utenti.

![](./imgs/bedrock_agent_tool.png)

## Come sviluppare i tuoi strumenti personalizzati

Per sviluppare strumenti personalizzati per l'Agent, segui queste linee guida:

- Crea una nuova classe che erediti dalla classe `AgentTool`. Anche se l'interfaccia è compatibile con LangChain, questa implementazione di esempio fornisce la propria classe `AgentTool`, dalla quale dovresti ereditare ([source](../backend/app/agents/tools/agent_tool.py)).

- Fai riferimento all'implementazione di esempio di uno [strumento di calcolo BMI](../examples/agents/tools/bmi/bmi.py). Questo esempio dimostra come creare uno strumento che calcola l'Indice di Massa Corporea (BMI) in base all'input dell'utente.

  - Il nome e la descrizione dichiarati sullo strumento vengono utilizzati quando l'LLM considera quale strumento dovrebbe essere usato per rispondere alla domanda dell'utente. In altre parole, vengono incorporati nel prompt quando si richiama l'LLM. Quindi è consigliabile descriverli il più precisamente possibile.

- [Facoltativo] Una volta implementato il tuo strumento personalizzato, è consigliabile verificarne la funzionalità utilizzando lo script di test ([esempio](../examples/agents/tools/bmi/test_bmi.py)). Questo script ti aiuterà a garantire che il tuo strumento funzioni come previsto.

- Dopo aver completato lo sviluppo e il test del tuo strumento personalizzato, sposta il file di implementazione nella directory [backend/app/agents/tools/](../backend/app/agents/tools/). Quindi apri [backend/app/agents/utils.py](../backend/app/agents/utils.py) e modifica `get_available_tools` in modo che l'utente possa selezionare lo strumento sviluppato.

- [Facoltativo] Aggiungi nomi e descrizioni chiari per il frontend. Questo passaggio è facoltativo, ma se non lo fai, verranno utilizzati il nome e la descrizione dello strumento dichiarati nel tuo strumento. Questi sono per l'LLM e non per l'utente, quindi è consigliabile aggiungere una spiegazione dedicata per migliorare l'esperienza utente.

  - Modifica i file i18n. Apri [en/index.ts](../frontend/src/i18n/en/index.ts) e aggiungi il tuo `name` e `description` su `agent.tools`.
  - Modifica anche `xx/index.ts`. Dove `xx` rappresenta il codice paese che desideri.

- Esegui `npx cdk deploy` per distribuire le tue modifiche. Questo renderà disponibile il tuo strumento personalizzato nella schermata del bot personalizzato.

## Contribuzione

**I contributi al repository degli strumenti sono ben accetti!** Se sviluppi uno strumento utile e ben implementato, considera di contribuirlo al progetto inviando un issue o una pull request.