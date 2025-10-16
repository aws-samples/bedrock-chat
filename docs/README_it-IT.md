<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Una piattaforma di IA generativa multilingue alimentata da [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Supporta chat, bot personalizzati con conoscenza (RAG), condivisione di bot tramite bot store e automazione delle attività utilizzando agenti.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 rilasciata. Per aggiornare, si prega di rivedere attentamente la [guida alla migrazione](./migration/V2_TO_V3_it-IT.md).** Senza alcuna attenzione, **I BOT DELLA V2 DIVENTERANNO INUTILIZZABILI.**

### Personalizzazione Bot / Bot store

Aggiungi le tue istruzioni e conoscenze (anche note come [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Il bot può essere condiviso tra gli utenti dell'applicazione tramite il marketplace del bot store. Il bot personalizzato può anche essere pubblicato come API autonoma (Vedi i [dettagli](./PUBLISH_API_it-IT.md)).

<details>
<summary>Screenshot</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Puoi anche importare [KnowledgeBase di Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/) esistenti.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Per motivi di governance, solo gli utenti autorizzati possono creare bot personalizzati. Per consentire la creazione di bot personalizzati, l'utente deve essere membro del gruppo chiamato `CreatingBotAllowed`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o aws cli. Nota che l'ID del pool di utenti può essere consultato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Funzionalità amministrative

Gestione API, Contrassegna bot come essenziali, Analizza l'utilizzo dei bot. [dettagli](./ADMINISTRATOR_it-IT.md)

<details>
<summary>Screenshot</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agente

Utilizzando la [funzionalità Agente](./AGENT_it-IT.md), il tuo chatbot può gestire automaticamente attività più complesse. Ad esempio, per rispondere alla domanda di un utente, l'Agente può recuperare le informazioni necessarie da strumenti esterni o suddividere l'attività in più passaggi per l'elaborazione.

<details>
<summary>Screenshot</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Distribuzione Super-semplice

- Nella regione us-east-1, apri [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Seleziona tutti i modelli che desideri utilizzare e poi `Save changes`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

### Regioni supportate

Assicurati di distribuire Bedrock Chat in una regione [dove OpenSearch Serverless e le API di Ingestion sono disponibili](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), se vuoi utilizzare i bot e creare basi di conoscenza (OpenSearch Serverless è la scelta predefinita). A partire da agosto 2025, sono supportate le seguenti regioni: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Per il parametro **bedrock-region** devi scegliere una regione [dove Bedrock è disponibile](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Apri [CloudShell](https://console.aws.amazon.com/cloudshell/home) nella regione in cui desideri effettuare la distribuzione
- Esegui la distribuzione con i seguenti comandi. Se vuoi specificare la versione da distribuire o hai bisogno di applicare policy di sicurezza, specifica i parametri appropriati da [Parametri Opzionali](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Ti verrà chiesto se sei un nuovo utente o stai usando v3. Se non sei un utente che proviene dalla v0, inserisci `y`.

### Parametri Opzionali

Puoi specificare i seguenti parametri durante la distribuzione per migliorare sicurezza e personalizzazione:

- **--disable-self-register**: Disabilita l'auto-registrazione (predefinito: abilitato). Se questo flag è impostato, dovrai creare tutti gli utenti su cognito e non sarà permesso agli utenti di registrare autonomamente i loro account.
- **--enable-lambda-snapstart**: Abilita [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (predefinito: disabilitato). Se questo flag è impostato, migliora i tempi di avvio a freddo delle funzioni Lambda, fornendo tempi di risposta più rapidi per una migliore esperienza utente.
- **--ipv4-ranges**: Lista separata da virgole degli intervalli IPv4 consentiti. (predefinito: consente tutti gli indirizzi ipv4)
- **--ipv6-ranges**: Lista separata da virgole degli intervalli IPv6 consentiti. (predefinito: consente tutti gli indirizzi ipv6)
- **--disable-ipv6**: Disabilita le connessioni tramite IPv6. (predefinito: abilitato)
- **--allowed-signup-email-domains**: Lista separata da virgole dei domini email consentiti per la registrazione. (predefinito: nessuna restrizione di dominio)
- **--bedrock-region**: Definisce la regione dove Bedrock è disponibile. (predefinito: us-east-1)
- **--repo-url**: Il repository personalizzato di Bedrock Chat da distribuire, se forkato o con controllo sorgente personalizzato. (predefinito: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: La versione di Bedrock Chat da distribuire. (predefinito: ultima versione in sviluppo)
- **--cdk-json-override**: Puoi sovrascrivere qualsiasi valore del contesto CDK durante la distribuzione utilizzando il blocco JSON di override. Questo ti permette di modificare la configurazione senza editare direttamente il file cdk.json.

Esempio di utilizzo:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

L'override JSON deve seguire la stessa struttura di cdk.json. Puoi sovrascrivere qualsiasi valore del contesto inclusi:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: accetta una lista di ID modello da abilitare. Il valore predefinito è una lista vuota, che abilita tutti i modelli.
- `logoPath`: percorso relativo all'asset del logo all'interno della directory frontend `public/` che appare in cima al drawer di navigazione.
- E altri valori di contesto definiti in cdk.json

> [!Note]
> I valori di override verranno uniti con la configurazione cdk.json esistente durante il tempo di distribuzione nell'AWS code build. I valori specificati nell'override avranno la precedenza sui valori in cdk.json.

#### Esempio di comando con parametri:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Dopo circa 35 minuti, otterrai il seguente output, a cui potrai accedere dal tuo browser

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Apparirà la schermata di registrazione come mostrato sopra, dove potrai registrare la tua email e accedere.

> [!Important]
> Senza impostare il parametro opzionale, questo metodo di distribuzione permette a chiunque conosca l'URL di registrarsi. Per l'uso in produzione, si raccomanda vivamente di aggiungere restrizioni degli indirizzi IP e disabilitare l'auto-registrazione per mitigare i rischi di sicurezza (puoi definire allowed-signup-email-domains per limitare gli utenti in modo che solo gli indirizzi email dal dominio della tua azienda possano registrarsi). Usa sia ipv4-ranges che ipv6-ranges per le restrizioni degli indirizzi IP, e disabilita l'auto-registrazione usando disable-self-register durante l'esecuzione di ./bin.

> [!TIP]
> Se il `Frontend URL` non appare o Bedrock Chat non funziona correttamente, potrebbe essere un problema con l'ultima versione. In questo caso, aggiungi `--version "v3.0.0"` ai parametri e prova nuovamente la distribuzione.

## Architettura

È un'architettura costruita su servizi gestiti AWS, eliminando la necessità di gestire l'infrastruttura. Utilizzando Amazon Bedrock, non c'è bisogno di comunicare con API esterne ad AWS. Questo permette di distribuire applicazioni scalabili, affidabili e sicure.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Database NoSQL per l'archiviazione della cronologia delle conversazioni
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Distribuzione dell'applicazione frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restrizione degli indirizzi IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticazione degli utenti
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servizio gestito per utilizzare modelli fondamentali tramite API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Fornisce un'interfaccia gestita per la Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offrendo servizi per l'embedding e l'analisi dei documenti
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Ricezione di eventi dal flusso DynamoDB e avvio di Step Functions per incorporare conoscenze esterne
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrazione della pipeline di ingestion per incorporare conoscenze esterne in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Funge da database backend per Bedrock Knowledge Bases, fornendo ricerca full-text e ricerca vettoriale, consentendo un recupero accurato delle informazioni pertinenti
- [Amazon Athena](https://aws.amazon.com/athena/): Servizio di query per analizzare il bucket S3

![](./imgs/arch.png)

## Deploy usando CDK

Il Deployment Super-facile utilizza [AWS CodeBuild](https://aws.amazon.com/codebuild/) per eseguire internamente il deployment tramite CDK. Questa sezione descrive la procedura per effettuare il deployment direttamente con CDK.

- È necessario disporre di UNIX, Docker e un ambiente runtime Node.js.

> [!Important]
> Se lo spazio di archiviazione nell'ambiente locale durante il deployment è insufficiente, il bootstrapping CDK potrebbe generare un errore. Si consiglia di espandere la dimensione del volume dell'istanza prima del deployment.

- Clonare questo repository

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Installare i pacchetti npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Se necessario, modificare le seguenti voci in [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Regione dove Bedrock è disponibile. **NOTA: Bedrock NON supporta tutte le regioni per ora.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Intervallo di indirizzi IP consentiti.
  - `enableLambdaSnapStart`: Predefinito a true. Impostare a false se si effettua il deployment in una [regione che non supporta Lambda SnapStart per le funzioni Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Predefinito a tutti. Se impostato (lista di ID modelli), permette di controllare globalmente quali modelli appaiono nei menu a tendina nelle chat per tutti gli utenti e durante la creazione del bot nell'applicazione Bedrock Chat.
  - `logoPath`: Percorso relativo sotto `frontend/public` che punta all'immagine visualizzata nella parte superiore del drawer dell'applicazione.
Sono supportati i seguenti ID modello (assicurarsi che siano abilitati anche nella console Bedrock sotto Model access nella regione di deployment):
- **Modelli Claude:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Modelli Amazon Nova:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Modelli Mistral:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **Modelli DeepSeek:** `deepseek-r1`
- **Modelli Meta Llama:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

La lista completa può essere trovata in [index.ts](./frontend/src/constants/index.ts).

- Prima di effettuare il deployment del CDK, sarà necessario eseguire il Bootstrap una volta per la regione in cui si sta effettuando il deployment.

```
npx cdk bootstrap
```

- Effettuare il deployment di questo progetto di esempio

```
npx cdk deploy --require-approval never --all
```

- Otterrai un output simile al seguente. L'URL dell'app web sarà mostrato in `BedrockChatStack.FrontendURL`, accedere da browser.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definizione dei Parametri

Puoi definire i parametri per il tuo deployment in due modi: usando `cdk.json` o usando il file `parameter.ts` type-safe.

#### Usando cdk.json (Metodo Tradizionale)

Il modo tradizionale per configurare i parametri è modificando il file `cdk.json`. Questo approccio è semplice ma manca del controllo dei tipi:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet", 
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Usando parameter.ts (Metodo Type-Safe Raccomandato)

Per una migliore sicurezza dei tipi e esperienza di sviluppo, puoi usare il file `parameter.ts` per definire i tuoi parametri:

```typescript
// Definire i parametri per l'ambiente predefinito
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Definire i parametri per ambienti aggiuntivi
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Risparmio costi per ambiente dev
  enableBotStoreReplicas: false, // Risparmio costi per ambiente dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilità migliorata per produzione
  enableBotStoreReplicas: true, // Disponibilità migliorata per produzione
});
```

> [!Note]
> Gli utenti esistenti possono continuare a usare `cdk.json` senza modifiche. L'approccio `parameter.ts` è raccomandato per nuovi deployment o quando è necessario gestire più ambienti.

### Deployment di Ambienti Multipli

Puoi effettuare il deployment di più ambienti dallo stesso codice base usando il file `parameter.ts` e l'opzione `-c envName`.

#### Prerequisiti

1. Definire gli ambienti in `parameter.ts` come mostrato sopra
2. Ogni ambiente avrà il proprio set di risorse con prefissi specifici per l'ambiente

#### Comandi di Deployment

Per effettuare il deployment di un ambiente specifico:

```bash
# Deploy dell'ambiente dev
npx cdk deploy --all -c envName=dev

# Deploy dell'ambiente prod
npx cdk deploy --all -c envName=prod
```

Se non viene specificato alcun ambiente, viene utilizzato l'ambiente "default":

```bash
# Deploy dell'ambiente default
npx cdk deploy --all
```

#### Note Importanti

1. **Denominazione Stack**:

   - Gli stack principali per ogni ambiente avranno il prefisso con il nome dell'ambiente (es. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuttavia, gli stack dei bot personalizzati (`BrChatKbStack*`) e gli stack di pubblicazione API (`ApiPublishmentStack*`) non ricevono prefissi dell'ambiente poiché vengono creati dinamicamente durante l'esecuzione

2. **Denominazione Risorse**:

   - Solo alcune risorse ricevono prefissi dell'ambiente nei loro nomi (es. tabella `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La maggior parte delle risorse mantiene i nomi originali ma è isolata essendo in stack diversi

3. **Identificazione Ambiente**:

   - Tutte le risorse sono taggate con un tag `CDKEnvironment` contenente il nome dell'ambiente
   - Puoi usare questo tag per identificare a quale ambiente appartiene una risorsa
   - Esempio: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Override Ambiente Default**: Se definisci un ambiente "default" in `parameter.ts`, questo sovrascriverà le impostazioni in `cdk.json`. Per continuare a usare `cdk.json`, non definire un ambiente "default" in `parameter.ts`.

5. **Requisiti Ambiente**: Per creare ambienti diversi da "default", devi usare `parameter.ts`. L'opzione `-c envName` da sola non è sufficiente senza le corrispondenti definizioni dell'ambiente.

6. **Isolamento Risorse**: Ogni ambiente crea il proprio set di risorse, permettendo di avere ambienti di sviluppo, test e produzione nello stesso account AWS senza conflitti.

## Altri

È possibile definire i parametri per il deployment in due modi: usando `cdk.json` oppure usando il file type-safe `parameter.ts`.

#### Uso di cdk.json (Metodo Tradizionale)

Il modo tradizionale per configurare i parametri è modificando il file `cdk.json`. Questo approccio è semplice ma manca del controllo dei tipi:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Uso di parameter.ts (Metodo Type-Safe Raccomandato)

Per una migliore sicurezza dei tipi ed esperienza di sviluppo, puoi utilizzare il file `parameter.ts` per definire i tuoi parametri:

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Gli utenti esistenti possono continuare a utilizzare `cdk.json` senza alcuna modifica. L'approccio `parameter.ts` è raccomandato per nuovi deployment o quando è necessario gestire più ambienti.

### Deploying di Ambienti Multipli

Puoi effettuare il deployment di più ambienti dallo stesso codice base utilizzando il file `parameter.ts` e l'opzione `-c envName`.

#### Prerequisiti

1. Definisci i tuoi ambienti in `parameter.ts` come mostrato sopra
2. Ogni ambiente avrà il proprio set di risorse con prefissi specifici per ambiente

#### Comandi di Deployment

Per effettuare il deployment di un ambiente specifico:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Se non viene specificato alcun ambiente, viene utilizzato l'ambiente "default":

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Note Importanti

1. **Denominazione degli Stack**:

   - Gli stack principali per ogni ambiente avranno il prefisso con il nome dell'ambiente (es. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Tuttavia, gli stack dei bot personalizzati (`BrChatKbStack*`) e gli stack di pubblicazione API (`ApiPublishmentStack*`) non ricevono prefissi dell'ambiente poiché vengono creati dinamicamente durante l'esecuzione

2. **Denominazione delle Risorse**:

   - Solo alcune risorse ricevono prefissi dell'ambiente nei loro nomi (es. tabella `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La maggior parte delle risorse mantiene i nomi originali ma è isolata essendo in stack diversi

3. **Identificazione dell'Ambiente**:

   - Tutte le risorse sono taggate con un tag `CDKEnvironment` contenente il nome dell'ambiente
   - Puoi utilizzare questo tag per identificare a quale ambiente appartiene una risorsa
   - Esempio: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Override dell'Ambiente Default**: Se definisci un ambiente "default" in `parameter.ts`, questo sovrascriverà le impostazioni in `cdk.json`. Per continuare a utilizzare `cdk.json`, non definire un ambiente "default" in `parameter.ts`.

5. **Requisiti dell'Ambiente**: Per creare ambienti diversi da "default", devi utilizzare `parameter.ts`. L'opzione `-c envName` da sola non è sufficiente senza le corrispondenti definizioni dell'ambiente.

6. **Isolamento delle Risorse**: Ogni ambiente crea il proprio set di risorse, permettendoti di avere ambienti di sviluppo, test e produzione nello stesso account AWS senza conflitti.

## Altri

### Rimuovere le risorse

Se si utilizza cli e CDK, eseguire `npx cdk destroy`. In alternativa, accedere a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) ed eliminare manualmente `BedrockChatStack` e `FrontendWafStack`. Si noti che `FrontendWafStack` si trova nella regione `us-east-1`.

### Impostazioni della lingua

Questa risorsa rileva automaticamente la lingua utilizzando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). È possibile cambiare lingua dal menu dell'applicazione. In alternativa, è possibile utilizzare la Query String per impostare la lingua come mostrato di seguito.

> `https://example.com?lng=ja`

### Disabilitare la registrazione autonoma

Questo esempio ha la registrazione autonoma abilitata per impostazione predefinita. Per disabilitarla, aprire [cdk.json](./cdk/cdk.json) e impostare `selfSignUpEnabled` su `false`. Se si configura un [provider di identità esterno](#external-identity-provider), il valore verrà ignorato e automaticamente disabilitato.

### Limitare i domini per gli indirizzi email di registrazione

Per impostazione predefinita, questo esempio non limita i domini per gli indirizzi email di registrazione. Per consentire le registrazioni solo da domini specifici, aprire `cdk.json` e specificare i domini come lista in `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Provider di identità esterno

Questo esempio supporta provider di identità esterni. Attualmente supportiamo [Google](./idp/SET_UP_GOOGLE_it-IT.md) e [provider OIDC personalizzati](./idp/SET_UP_CUSTOM_OIDC_it-IT.md).

### WAF Frontend opzionale

Per le distribuzioni CloudFront, i WebACL di AWS WAF devono essere creati nella regione us-east-1. In alcune organizzazioni, la creazione di risorse al di fuori della regione principale è limitata dalle policy. In tali ambienti, la distribuzione CDK può fallire quando si tenta di provisioning del Frontend WAF in us-east-1.

Per gestire queste restrizioni, lo stack Frontend WAF è opzionale. Quando disabilitato, la distribuzione CloudFront viene distribuita senza WebACL. Questo significa che non avrai controlli di allow/deny IP sul frontend edge. L'autenticazione e tutti gli altri controlli dell'applicazione continuano a funzionare normalmente. Nota che questa impostazione influisce solo sul Frontend WAF (ambito CloudFront); il WAF delle API pubblicate (regionale) rimane inalterato.

Per disabilitare il Frontend WAF impostare quanto segue in `parameter.ts` (Metodo raccomandato Type-Safe):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Oppure se si utilizza il legacy `cdk/cdk.json` impostare:

```json
"enableFrontendWaf": false
``` 

### Aggiungere automaticamente nuovi utenti ai gruppi

Questo esempio ha i seguenti gruppi per assegnare permessi agli utenti:

- [`Admin`](./ADMINISTRATOR_it-IT.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_it-IT.md)

Se si desidera che gli utenti appena creati si uniscano automaticamente ai gruppi, è possibile specificarli in [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Per impostazione predefinita, i nuovi utenti verranno aggiunti al gruppo `CreatingBotAllowed`.

### Configurare le repliche RAG

`enableRagReplicas` è un'opzione in [cdk.json](./cdk/cdk.json) che controlla le impostazioni delle repliche per il database RAG, in particolare le Knowledge Base che utilizzano Amazon OpenSearch Serverless.

- **Default**: true
- **true**: Migliora la disponibilità abilitando repliche aggiuntive, rendendolo adatto per ambienti di produzione ma aumentando i costi.
- **false**: Riduce i costi utilizzando meno repliche, rendendolo adatto per sviluppo e test.

Questa è un'impostazione a livello di account/regione che influenza l'intera applicazione anziché i singoli bot.

> [!Note]
> A partire da giugno 2024, Amazon OpenSearch Serverless supporta 0.5 OCU, riducendo i costi iniziali per carichi di lavoro di piccola scala. Le distribuzioni in produzione possono iniziare con 2 OCU, mentre i carichi di lavoro dev/test possono utilizzare 1 OCU. OpenSearch Serverless scala automaticamente in base alle esigenze del carico di lavoro. Per maggiori dettagli, visitare l'[annuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurare il Bot Store

La funzionalità bot store permette agli utenti di condividere e scoprire bot personalizzati. È possibile configurare il bot store attraverso le seguenti impostazioni in [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Controlla se la funzionalità bot store è abilitata (default: `true`)
- **botStoreLanguage**: Imposta la lingua principale per la ricerca e scoperta dei bot (default: `"en"`). Questo influenza come i bot vengono indicizzati e cercati nel bot store, ottimizzando l'analisi del testo per la lingua specificata.
- **enableBotStoreReplicas**: Controlla se le repliche di standby sono abilitate per la collezione OpenSearch Serverless utilizzata dal bot store (default: `false`). Impostandolo su `true` migliora la disponibilità ma aumenta i costi, mentre `false` riduce i costi ma può influire sulla disponibilità.
  > **Importante**: Non è possibile aggiornare questa proprietà dopo che la collezione è già stata creata. Se si tenta di modificare questa proprietà, la collezione continuerà a utilizzare il valore originale.

### Inferenza cross-region

[L'inferenza cross-region](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permette ad Amazon Bedrock di instradare dinamicamente le richieste di inferenza del modello attraverso più regioni AWS, migliorando il throughput e la resilienza durante i periodi di picco della domanda. Per configurare, modificare `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) migliora i tempi di avvio a freddo delle funzioni Lambda, fornendo tempi di risposta più rapidi per una migliore esperienza utente. D'altra parte, per le funzioni Python, c'è un [costo dipendente dalla dimensione della cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) e [non è disponibile in alcune regioni](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) attualmente. Per disabilitare SnapStart, modificare `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurare un dominio personalizzato

È possibile configurare un dominio personalizzato per la distribuzione CloudFront impostando i seguenti parametri in [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Il nome di dominio personalizzato per l'applicazione chat (es. chat.example.com)
- `hostedZoneId`: L'ID della zona ospitata Route 53 dove verranno creati i record DNS

Quando questi parametri vengono forniti, la distribuzione automaticamente:

- Creerà un certificato ACM con validazione DNS nella regione us-east-1
- Creerà i record DNS necessari nella tua zona ospitata Route 53
- Configurerà CloudFront per utilizzare il tuo dominio personalizzato

> [!Note]
> Il dominio deve essere gestito da Route 53 nel tuo account AWS. L'ID della zona ospitata può essere trovato nella console Route 53.

### Configurare i paesi consentiti (restrizione geografica)

È possibile limitare l'accesso a Bedrock-Chat in base al paese da cui il client sta accedendo.
Utilizzare il parametro `allowedCountries` in [cdk.json](./cdk/cdk.json) che accetta una lista di [Codici Paese ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Per esempio, un'azienda della Nuova Zelanda potrebbe decidere che solo gli indirizzi IP dalla Nuova Zelanda (NZ) e dall'Australia (AU) possono accedere al portale e tutti gli altri devono essere negati.
Per configurare questo comportamento utilizzare la seguente impostazione in [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Oppure, utilizzando `parameter.ts` (Metodo raccomandato Type-Safe):

```ts
// Definire i parametri per l'ambiente predefinito
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Disabilitare il supporto IPv6

Il frontend ottiene sia indirizzi IP che IPv6 per impostazione predefinita. In alcune rare
circostanze, potrebbe essere necessario disabilitare esplicitamente il supporto IPv6. Per farlo, impostare
il seguente parametro in [parameter.ts](./cdk/parameter.ts) o similmente in [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Se non impostato, il supporto IPv6 sarà abilitato per impostazione predefinita.

### Sviluppo locale

Vedere [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_it-IT.md).

### Contributi

Grazie per considerare di contribuire a questo repository! Accogliamo correzioni di bug, traduzioni linguistiche (i18n), miglioramenti delle funzionalità, [strumenti per agenti](./docs/AGENT.md#how-to-develop-your-own-tools), e altri miglioramenti.

Per miglioramenti delle funzionalità e altri miglioramenti, **prima di creare una Pull Request, apprezzeremmo molto se potessi creare una Issue di Richiesta Funzionalità per discutere l'approccio di implementazione e i dettagli. Per correzioni di bug e traduzioni linguistiche (i18n), procedere direttamente con la creazione di una Pull Request.**

Si prega di consultare anche le seguenti linee guida prima di contribuire:

- [Sviluppo Locale](./LOCAL_DEVELOPMENT_it-IT.md)
- [CONTRIBUTING](./CONTRIBUTING_it-IT.md)

## Contatti

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contributori Significativi

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Contributori

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Licenza

Questa libreria è concessa in licenza secondo i termini della Licenza MIT-0. Consultare [il file LICENSE](./LICENSE).