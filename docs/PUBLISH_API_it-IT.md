# Pubblicazione API

## Panoramica

Questo esempio include una funzionalità per la pubblicazione di API. Mentre un'interfaccia di chat può essere conveniente per la validazione preliminare, l'implementazione effettiva dipende dal caso d'uso specifico e dall'esperienza utente (UX) desiderata per l'utente finale. In alcuni scenari, un'interfaccia di chat potrebbe essere la scelta preferita, mentre in altri, un'API autonoma potrebbe essere più adatta. Dopo la validazione iniziale, questo esempio fornisce la capacità di pubblicare bot personalizzati in base alle esigenze del progetto. Inserendo le impostazioni per quote, limitazioni, origini, ecc., è possibile pubblicare un endpoint insieme a una chiave API, offrendo flessibilità per diverse opzioni di integrazione.

## Sicurezza

L'utilizzo della sola chiave API non è raccomandato come descritto in: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Di conseguenza, questo esempio implementa una semplice restrizione degli indirizzi IP tramite AWS WAF. La regola WAF viene applicata in modo uniforme all'intera applicazione per considerazioni di costo, assumendo che le fonti che si vorrebbero limitare siano probabilmente le stesse per tutte le API pubblicate. **Si prega di attenersi alle policy di sicurezza della propria organizzazione per l'implementazione effettiva.** Vedere anche la sezione [Architecture](#architecture).

## Come pubblicare un'API bot personalizzata

### Prerequisiti

Per ragioni di governance, solo un numero limitato di utenti può pubblicare i bot. Prima della pubblicazione, l'utente deve essere membro del gruppo chiamato `PublishAllowed`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o tramite aws cli. Si noti che l'ID del pool di utenti può essere consultato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Impostazioni di pubblicazione API

Dopo aver effettuato l'accesso come utente `PublishedAllowed` e creato un bot, selezionare `API PublishSettings`. Si noti che solo un bot condiviso può essere pubblicato.
![](./imgs/bot_api_publish_screenshot.png)

Nella schermata successiva, è possibile configurare diversi parametri relativi alla limitazione delle richieste. Per i dettagli, consultare anche: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Dopo il deployment, apparirà la seguente schermata dove è possibile ottenere l'URL dell'endpoint e una chiave API. È inoltre possibile aggiungere ed eliminare chiavi API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architettura

L'API è pubblicata secondo il seguente diagramma:

![](./imgs/published_arch.png)

Il WAF viene utilizzato per la restrizione degli indirizzi IP. Gli indirizzi possono essere configurati impostando i parametri `publishedApiAllowedIpV4AddressRanges` e `publishedApiAllowedIpV6AddressRanges` nel file `cdk.json`.

Quando un utente clicca per pubblicare il bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) avvia un'attività di deployment CDK per provisioning dello stack API (Vedi anche: [Definizione CDK](../cdk/lib/api-publishment-stack.ts)) che contiene API Gateway, Lambda e SQS. SQS viene utilizzato per disaccoppiare la richiesta dell'utente e l'operazione LLM poiché la generazione dell'output potrebbe superare i 30 secondi, che è il limite della quota di API Gateway. Per recuperare l'output, è necessario accedere all'API in modo asincrono. Per maggiori dettagli, consultare la [Specifica API](#api-specification).

Il client deve impostare `x-api-key` nell'header della richiesta.

## Specifiche API

Vedi [qui](https://aws-samples.github.io/bedrock-chat).