# Pubblicazione API

## Panoramica

Questo esempio include una funzionalità per la pubblicazione di API. Sebbene un'interfaccia chat possa essere comoda per la convalida preliminare, l'implementazione effettiva dipende dal caso d'uso specifico e dall'esperienza utente (UX) desiderata per l'utente finale. In alcuni scenari, un'interfaccia chat potrebbe essere la scelta preferita, mentre in altri, un'API autonoma potrebbe essere più adatta. Dopo la convalida iniziale, questo esempio offre la capacità di pubblicare bot personalizzati in base alle esigenze del progetto. Inserendo impostazioni per quote, limitazione delle richieste, origini e altro, è possibile pubblicare un endpoint insieme a una chiave API, offrendo flessibilità per diverse opzioni di integrazione.

## Sicurezza

L'utilizzo di un solo API key non è consigliato, come descritto in: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Di conseguenza, questo esempio implementa una semplice restrizione degli indirizzi IP tramite AWS WAF. La regola WAF viene applicata comunemente in tutta l'applicazione per considerazioni di costi, partendo dal presupposto che le origini che si desidera limitare siano probabilmente le stesse per tutte le API emesse. **Si prega di attenersi alla policy di sicurezza della propria organizzazione per l'implementazione effettiva.** Vedere anche la sezione [Architettura](#architettura).

## Come pubblicare un'API bot personalizzata

### Prerequisiti

Per ragioni di governance, solo alcuni utenti limitati possono pubblicare bot. Prima della pubblicazione, l'utente deve essere membro del gruppo chiamato `PublishAllowed`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o aws cli. Nota che l'ID del pool utenti può essere trovato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Impostazioni di Pubblicazione API

Dopo aver effettuato l'accesso come utente `PublishedAllowed` e aver creato un bot, scegliere `API PublishSettings`. Nota che solo un bot condiviso può essere pubblicato.
![](./imgs/bot_api_publish_screenshot.png)

Nella schermata seguente, è possibile configurare diversi parametri relativi alla limitazione delle richieste. Per i dettagli, consultare anche: [Limitare le richieste API per migliorare la velocità effettiva](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Dopo la distribuzione, apparirà la schermata seguente dove è possibile ottenere l'URL dell'endpoint e una chiave API. È inoltre possibile aggiungere ed eliminare chiavi API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architettura

L'API viene pubblicata secondo il seguente diagramma:

![](./imgs/published_arch.png)

Il WAF viene utilizzato per la restrizione degli indirizzi IP. L'indirizzo può essere configurato impostando i parametri `publishedApiAllowedIpV4AddressRanges` e `publishedApiAllowedIpV6AddressRanges` in `cdk.json`.

Quando un utente fa clic per pubblicare il bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) avvia un'attività di distribuzione CDK per eseguire il provisioning dello stack API (vedi anche: [Definizione CDK](../cdk/lib/api-publishment-stack.ts)) che contiene API Gateway, Lambda e SQS. SQS viene utilizzato per disaccoppiare la richiesta dell'utente dall'operazione LLM poiché la generazione dell'output può superare i 30 secondi, che è il limite della quota di API Gateway. Per recuperare l'output, è necessario accedere all'API in modo asincrono. Per ulteriori dettagli, consulta [Specifiche API](#api-specification).

Il client deve impostare `x-api-key` nell'intestazione della richiesta.

## Specifica API

Vedi [qui](https://aws-samples.github.io/bedrock-chat).