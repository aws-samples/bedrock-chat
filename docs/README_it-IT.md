# Chat Bedrock Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_no.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi.md)

> [!Warning]  
> **Rilasciata la versione V2. Per l'aggiornamento, consultare attentamente la [guida alla migrazione](./migration/V1_TO_V2_it-IT.md).** Senza alcuna attenzione, **I BOT DELLA V1 DIVENTERANNO INUTILIZZABILI.**

Un chatbot multilingua che utilizza modelli LLM forniti da [Amazon Bedrock](https://aws.amazon.com/bedrock/) per l'intelligenza artificiale generativa.

### Guarda la Panoramica e l'Installazione su YouTube

[![Panoramica](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Conversazione di Base

![](./imgs/demo.gif)

### Personalizzazione del Bot

Aggiungi le tue istruzioni e fornisci conoscenze esterne tramite URL o file (noto come [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Il bot può essere condiviso tra gli utenti dell'applicazione. Il bot personalizzato può anche essere pubblicato come API autonoma (Vedi [dettagli](./PUBLISH_API_it-IT.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Per ragioni di governance, solo gli utenti autorizzati possono creare bot personalizzati. Per consentire la creazione di bot personalizzati, l'utente deve essere un membro del gruppo chiamato `CreatingBotAllowed`, che può essere configurato tramite la console di gestione > Pool di utenti Amazon Cognito o aws cli. Si noti che l'ID del pool di utenti può essere reperito accedendo a CloudFormation > BedrockChatStack > Output > `AuthUserPoolIdxxxx`.

### Dashboard dell'Amministratore

<details>
<summary>Dashboard dell'Amministratore</summary>

Analizza l'utilizzo per ogni utente / bot nella dashboard dell'amministratore. [dettagli](./ADMINISTRATOR_it-IT.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Agente basato su LLM

<details>
<summary>Agente basato su LLM</summary>

Utilizzando la [funzionalità Agente](./AGENT_it-IT.md), il tuo chatbot può gestire automaticamente attività più complesse. Ad esempio, per rispondere a una domanda di un utente, l'Agente può recuperare le informazioni necessarie da strumenti esterni o suddividere l'attività in più passaggi per l'elaborazione.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Distribuzione Super-Facile

- Nella regione us-east-1, apri [Accesso al Modello Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Gestisci accesso modello` > Seleziona tutto di `Anthropic / Claude 3`, tutto di `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` e `Cohere / Embed Multilingual`, quindi `Salva modifiche`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

- Apri [CloudShell](https://console.aws.amazon.com/cloudshell/home) nella regione in cui desideri eseguire la distribuzione
- Esegui la distribuzione con i seguenti comandi. Se vuoi specificare la versione da distribuire o applicare criteri di sicurezza, specifica i parametri appropriati da [Parametri Facoltativi](#parametri-facoltativi).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Ti verrà chiesto se sei un nuovo utente o stai usando la v2. Se non sei un utente che continua dalla v0, inserisci `y`.

### Parametri Facoltativi

Puoi specificare i seguenti parametri durante la distribuzione per migliorare sicurezza e personalizzazione:

- **--disable-self-register**: Disabilita la registrazione autonoma (predefinito: abilitato). Se questo flag è impostato, dovrai creare tutti gli utenti su Cognito e non sarà consentita la registrazione autonoma degli account.
- **--enable-lambda-snapstart**: Abilita [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (predefinito: disabilitato). Se questo flag è impostato, migliora i tempi di avvio a freddo per le funzioni Lambda, fornendo tempi di risposta più veloci per una migliore esperienza utente.
- **--ipv4-ranges**: Elenco separato da virgole degli intervalli IPv4 consentiti. (predefinito: consenti tutti gli indirizzi ipv4)
- **--ipv6-ranges**: Elenco separato da virgole degli intervalli IPv6 consentiti. (predefinito: consenti tutti gli indirizzi ipv6)
- **--disable-ipv6**: Disabilita le connessioni su IPv6. (predefinito: abilitato)
- **--allowed-signup-email-domains**: Elenco separato da virgole dei domini email consentiti per la registrazione. (predefinito: nessuna restrizione di dominio)
- **--bedrock-region**: Definisce la regione in cui Bedrock è disponibile. (predefinito: us-east-1)
- **--repo-url**: L'URL del repository personalizzato di Bedrock Claude Chat da distribuire, se forked o con controllo sorgente personalizzato. (predefinito: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: La versione di Bedrock Claude Chat da distribuire. (predefinito: ultima versione in sviluppo)
- **--cdk-json-override**: Puoi sovrascrivere qualsiasi valore di contesto CDK durante la distribuzione utilizzando il blocco JSON di override. Questo consente di modificare la configurazione senza modificare direttamente il file cdk.json.

Esempio di utilizzo:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

Il JSON di override deve seguire la stessa struttura di cdk.json. Puoi sovrascrivere qualsiasi valore di contesto inclusi:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- E altri valori di contesto definiti in cdk.json

> [!Note]
> I valori di override verranno uniti con la configurazione cdk.json esistente durante il tempo di distribuzione in AWS code build. I valori specificati nell'override avranno la precedenza sui valori in cdk.json.

#### Esempio di comando con parametri:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Dopo circa 35 minuti, otterrai l'output seguente, che puoi raggiungere dal tuo browser

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Apparirà la schermata di registrazione come mostrato sopra, dove puoi registrare la tua email e accedere.

> [!Important]
> Senza impostare il parametro facoltativo, questo metodo di distribuzione consente a chiunque conosca l'URL di registrarsi. Per l'uso in produzione, è fortemente consigliato aggiungere restrizioni di indirizzi IP e disabilitare la registrazione autonoma per mitigare i rischi di sicurezza (puoi definire allowed-signup-email-domains per limitare gli utenti in modo che solo gli indirizzi email del dominio della tua azienda possano registrarsi). Usa sia ipv4-ranges che ipv6-ranges per le restrizioni degli indirizzi IP e disabilita la registrazione autonoma utilizzando disable-self-register durante l'esecuzione di ./bin.

> [!TIP]
> Se l'`URL Frontend` non appare o Bedrock Claude Chat non funziona correttamente, potrebbe esserci un problema con l'ultima versione. In questo caso, aggiungi `--version "v1.2.6"` ai parametri e riprova la distribuzione.

## Architettura

Un'architettura basata su servizi gestiti AWS, che elimina la necessità di gestione dell'infrastruttura. Utilizzando Amazon Bedrock, non è necessario comunicare con API esterne ad AWS. Questo permette di distribuire applicazioni scalabili, affidabili e sicure.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Database NoSQL per l'archiviazione della cronologia delle conversazioni
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Distribuzione dell'applicazione frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restrizione degli indirizzi IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticazione degli utenti
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servizio gestito per utilizzare modelli foundational tramite API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Fornisce un'interfaccia gestita per la Generazione Aumentata dal Recupero ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offrendo servizi per l'embedding e l'analisi dei documenti
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Ricezione di eventi dal flusso DynamoDB e avvio di Step Functions per l'embedding di conoscenze esterne
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrazione della pipeline di inserimento per l'embedding di conoscenze esterne in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Funge da database backend per Bedrock Knowledge Bases, fornendo funzionalità di ricerca full-text e ricerca vettoriale, consentendo il recupero accurato di informazioni rilevanti
- [Amazon Athena](https://aws.amazon.com/athena/): Servizio di query per analizzare bucket S3

![](./imgs/arch.png)

## Distribuisci utilizzando CDK

La distribuzione super-facile utilizza [AWS CodeBuild](https://aws.amazon.com/codebuild/) per eseguire la distribuzione tramite CDK internamente. Questa sezione descrive la procedura per distribuire direttamente con CDK.

- Assicurati di avere UNIX, Docker e un ambiente di runtime Node.js. In caso contrario, puoi utilizzare [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Importante]
> Se lo spazio di archiviazione nell'ambiente locale è insufficiente durante la distribuzione, il bootstrapping di CDK potrebbe generare un errore. Se si sta eseguendo su Cloud9 ecc., si consiglia di espandere la dimensione del volume dell'istanza prima della distribuzione.

- Clona questo repository

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Installa i pacchetti npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Se necessario, modifica le seguenti voci in [cdk.json](./cdk/cdk.json)

  - `bedrockRegion`: Regione in cui Bedrock è disponibile. **NOTA: Bedrock NON supporta tutte le regioni al momento.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Intervallo di indirizzi IP consentiti.
  - `enableLambdaSnapStart`: Per impostazione predefinita è true. Impostare su false se si distribuisce in una [regione che non supporta Lambda SnapStart per funzioni Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Prima di distribuire CDK, è necessario eseguire il Bootstrap una volta per la regione in cui si sta distribuendo.

```
npx cdk bootstrap
```

- Distribuisci questo progetto di esempio

```
npx cdk deploy --require-approval never --all
```

- Otterrai un output simile al seguente. L'URL dell'app web verrà visualizzato in `BedrockChatStack.FrontendURL`, quindi accedici dal tuo browser.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Altri

### Configurare il supporto per i modelli Mistral

Aggiorna `enableMistral` a `true` in [cdk.json](./cdk/cdk.json), e poi esegui `npx cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Importante]
> Questo progetto si concentra sui modelli Anthropic Claude, i modelli Mistral sono supportati in modo limitato. Ad esempio, gli esempi di prompt si basano sui modelli Claude. Questa è un'opzione solo per Mistral, una volta abilitati i modelli Mistral, potrai utilizzare solo i modelli Mistral per tutte le funzionalità di chat, NON sia Claude che Mistral.

### Configurare la generazione di testo predefinita

Gli utenti possono regolare i [parametri di generazione del testo](https://docs.anthropic.com/claude/reference/complete_post) dalla schermata di creazione del bot personalizzato. Se il bot non viene utilizzato, verranno utilizzati i parametri predefiniti impostati in [config.py](./backend/app/config.py).

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Rimuovere le risorse

Se si utilizza cli e CDK, eseguire `npx cdk destroy`. Altrimenti, accedere a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) e poi eliminare manualmente `BedrockChatStack` e `FrontendWafStack`. Nota che `FrontendWafStack` si trova nella regione `us-east-1`.

### Impostazioni Lingua

Questo asset rileva automaticamente la lingua utilizzando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). È possibile cambiare lingua dal menu dell'applicazione. In alternativa, è possibile utilizzare la stringa di query per impostare la lingua come mostrato di seguito.

> `https://example.com?lng=ja`

### Disabilitare l'iscrizione autonoma

Questo esempio ha l'iscrizione autonoma abilitata per impostazione predefinita. Per disabilitare l'iscrizione autonoma, aprire [cdk.json](./cdk/cdk.json) e impostare `selfSignUpEnabled` su `false`. Se si configura un [provider di identità esterno](#external-identity-provider), il valore verrà ignorato e automaticamente disabilitato.

### Limitare i Domini per gli Indirizzi Email di Iscrizione

Per impostazione predefinita, questo esempio non limita i domini per gli indirizzi email di iscrizione. Per consentire le iscrizioni solo da domini specifici, aprire `cdk.json` e specificare i domini come elenco in `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Provider di Identità Esterno

Questo esempio supporta un provider di identità esterno. Attualmente supportiamo [Google](./idp/SET_UP_GOOGLE_it-IT.md) e [provider OIDC personalizzato](./idp/SET_UP_CUSTOM_OIDC_it-IT.md).

### Aggiungere automaticamente nuovi utenti ai gruppi

Questo esempio ha i seguenti gruppi per dare autorizzazioni agli utenti:

- [`Admin`](./ADMINISTRATOR_it-IT.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_it-IT.md)

Se si desidera che i nuovi utenti si uniscano automaticamente ai gruppi, è possibile specificarli in [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Per impostazione predefinita, i nuovi utenti creati si uniranno al gruppo `CreatingBotAllowed`.

### Configurare Repliche RAG

`enableRagReplicas` è un'opzione in [cdk.json](./cdk/cdk.json) che controlla le impostazioni delle repliche per il database RAG, specificamente le Knowledge Bases che utilizzano Amazon OpenSearch Serverless.

- **Predefinito**: true
- **true**: Migliora la disponibilità abilitando repliche aggiuntive, adatto per ambienti di produzione ma aumentando i costi.
- **false**: Riduce i costi utilizzando meno repliche, adatto per sviluppo e test.

Questa è un'impostazione a livello di account/regione che interessa l'intera applicazione piuttosto che singoli bot.

> [!Nota]
> A giugno 2024, Amazon OpenSearch Serverless supporta 0,5 OCU, riducendo i costi di ingresso per carichi di lavoro su piccola scala. Le distribuzioni di produzione possono iniziare con 2 OCU, mentre i carichi di lavoro di sviluppo/test possono utilizzare 1 OCU. OpenSearch Serverless si ridimensiona automaticamente in base alle richieste di carico di lavoro. Per ulteriori dettagli, visitare [annuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Inferenza tra regioni

[Inferenza tra regioni](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) consente ad Amazon Bedrock di instradare dinamicamente le richieste di inferenza del modello tra più regioni AWS, migliorando la velocità effettiva e la resilienza durante i periodi di picco della domanda. Per configurare, modificare `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) migliora i tempi di avvio a freddo per le funzioni Lambda, fornendo tempi di risposta più veloci per una migliore esperienza utente. D'altra parte, per le funzioni Python, c'è un [addebito a seconda delle dimensioni della cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) e [non è disponibile in alcune regioni](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) attualmente. Per disabilitare SnapStart, modificare `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurare Dominio Personalizzato

È possibile configurare un dominio personalizzato per la distribuzione CloudFront impostando i seguenti parametri in [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Il nome di dominio personalizzato per la tua applicazione di chat (es. chat.example.com)
- `hostedZoneId`: L'ID della zona ospitata Route 53 in cui verranno create i record DNS

Quando questi parametri vengono forniti, la distribuzione eseguirà automaticamente:

- Creare un certificato ACM con convalida DNS nella regione us-east-1
- Creare i record DNS necessari nella zona Route 53
- Configurare CloudFront per utilizzare il dominio personalizzato

> [!Nota]
> Il dominio deve essere gestito da Route 53 nel proprio account AWS. L'ID della zona ospitata può essere trovato nella console Route 53.

### Sviluppo Locale

Vedi [SVILUPPO LOCALE](./LOCAL_DEVELOPMENT_it-IT.md).

### Contributo

Grazie per aver considerato di contribuire a questo repository! Accogliamo con favore correzioni di bug, traduzioni linguistiche (i18n), miglioramenti delle funzionalità, [strumenti per agenti](./docs/AGENT.md#how-to-develop-your-own-tools) e altri miglioramenti.

Per i miglioramenti delle funzionalità e altri miglioramenti, **prima di creare una Pull Request, apprezzeremmo molto se si potesse creare un'Issue di Richiesta Funzionalità per discutere l'approccio e i dettagli dell'implementazione. Per correzioni di bug e traduzioni linguistiche (i18n), procedere direttamente con la creazione di una Pull Request.**

Si prega inoltre di dare un'occhiata alle seguenti linee guida prima di contribuire:

- [Sviluppo Locale](./LOCAL_DEVELOPMENT_it-IT.md)
- [CONTRIBUTO](./CONTRIBUTING_it-IT.md)

## Contatti

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contributori Significativi

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Contributori

[![contributori di bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licenza

Questa libreria è licenziata sotto la Licenza MIT-0. Vedi [il file LICENSE](./LICENSE).