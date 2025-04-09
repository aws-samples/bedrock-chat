# API-publikasjon

## Oversikt

Denne prøven inkluderer en funksjon for publisering av APIer. Selv om et chat-grensesnitt kan være praktisk for foreløpig validering, avhenger den faktiske implementeringen av den spesifikke brukssaken og brukeropplevelsen (UX) som er ønsket for sluttbrukeren. I noen scenarioer kan en chat-UI være det foretrukne valget, mens i andre kan et frittstående API være mer egnet. Etter innledende validering gir denne prøven muligheten til å publisere skreddersydde bots i henhold til prosjektets behov. Ved å angi innstillinger for kvoter, begrensninger, opprinnelser osv. kan et endepunkt publiseres sammen med en API-nøkkel, noe som tilbyr fleksibilitet for ulike integrasjonsalternativer.

## Sikkerhet

Å bruke kun en API-nøkkel anbefales ikke, som beskrevet i: [AWS API Gateway Utviklerguide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Som følge av dette implementerer denne eksempelkoden en enkel IP-adressebegrensning via AWS WAF. WAF-regelen påføres vanligvis på tvers av applikasjonen av kostnadshensyn, med antakelsen om at kildene man ønsker å begrense sannsynligvis er de samme på tvers av alle utgitte API-er. **Vennligst følg din organisasjons sikkerhetsretningslinjer for faktisk implementasjon.** Se også [Arkitektur](#arkitektur)-seksjonen.

## Hvordan publisere tilpasset bot-API

### Forutsetninger

Av styringsgrunner kan kun et begrenset antall brukere publisere bots. Før publisering må brukeren være medlem av gruppen kalt `PublishAllowed`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at brukergruppe-ID-en kan refereres ved å åpne CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### API-publiseringsinnstillinger

Etter å ha logget inn som en `PublishedAllowed`-bruker og opprettet en bot, velg `API PublishSettings`. Merk at kun en delt bot kan publiseres.
![](./imgs/bot_api_publish_screenshot.png)

På følgende skjerm kan vi konfigurere flere parametere angående begrensning. For detaljer, se også: [Begrens API-forespørsler for bedre gjennomstrømning](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Etter distribusjon vil følgende skjerm vises hvor du kan hente ende-URL og en API-nøkkel. Vi kan også legge til og slette API-nøkler.

![](./imgs/bot_api_publish_screenshot3.png)

## Arkitektur

API-en publiseres som følgende diagram:

![](./imgs/published_arch.png)

WAF brukes for IP-adressebegrensning. Adressen kan konfigureres ved å sette parameterne `publishedApiAllowedIpV4AddressRanges` og `publishedApiAllowedIpV6AddressRanges` i `cdk.json`.

Når en bruker klikker publiser boten, starter [AWS CodeBuild](https://aws.amazon.com/codebuild/) en CDK-distribueringsoppgave for å etablere API-stakken (Se også: [CDK-definisjon](../cdk/lib/api-publishment-stack.ts)) som inneholder API Gateway, Lambda og SQS. SQS brukes til å koble fra brukerforespørsel og LLM-operasjon fordi generering av output kan overskride 30 sekunder, som er grensen for API Gateway-kvoten. For å hente output, må man aksessere API-en asynkront. For mer detaljer, se [API-spesifikasjon](#api-specification).

Klienten må sette `x-api-key` i forespørselhodet.

## API-spesifikasjon

Se [her](https://aws-samples.github.io/bedrock-chat).