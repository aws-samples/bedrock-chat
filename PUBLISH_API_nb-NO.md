# API-publisering

## Oversikt

Dette eksempelet inkluderer en funksjon for publisering av API-er. Selv om et chat-grensesnitt kan være praktisk for innledende validering, avhenger den faktiske implementeringen av den spesifikke brukssituasjonen og brukeropplevelsen (UX) som er ønsket for sluttbrukeren. I noen scenarioer kan et chat-grensesnitt være det foretrukne valget, mens i andre kan et frittstående API være mer egnet. Etter den innledende valideringen gir dette eksempelet muligheten til å publisere tilpassede boter i henhold til prosjektets behov. Ved å legge inn innstillinger for kvoter, begrensninger, opprinnelser osv., kan et endepunkt publiseres sammen med en API-nøkkel, noe som gir fleksibilitet for ulike integrasjonsmuligheter.

## Sikkerhet

Å kun bruke en API-nøkkel anbefales ikke, som beskrevet i: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Derfor implementerer dette eksempelet en enkel IP-adressebegrensning via AWS WAF. WAF-regelen anvendes felles på tvers av applikasjonen av kostnadshensyn, under antakelsen om at kildene man ønsker å begrense sannsynligvis er de samme på tvers av alle utstedte API-er. **Vennligst følg din organisasjons sikkerhetspolicy for faktisk implementering.** Se også [Arkitektur](#architecture)-seksjonen.

## Hvordan publisere tilpasset bot-API

### Forutsetninger

Av styringsmessige årsaker kan kun et begrenset antall brukere publisere boter. Før publisering må brukeren være medlem av gruppen kalt `PublishAllowed`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at bruker-pool-ID-en kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### API-publiseringsinnstillinger

Etter å ha logget inn som en `PublishedAllowed`-bruker og opprettet en bot, velg `API PublishSettings`. Merk at kun en delt bot kan publiseres.
![](./imgs/bot_api_publish_screenshot.png)

På følgende skjerm kan vi konfigurere flere parametere for begrensning av forespørsler. For mer informasjon, se også: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Etter distribusjon vil følgende skjerm vises hvor du kan få endepunkt-URL-en og en API-nøkkel. Vi kan også legge til og slette API-nøkler.

![](./imgs/bot_api_publish_screenshot3.png)

## Arkitektur

API-et er publisert som følgende diagram:

![](./imgs/published_arch.png)

WAF brukes for IP-adressebegrensning. Adressen kan konfigureres ved å sette parameterne `publishedApiAllowedIpV4AddressRanges` og `publishedApiAllowedIpV6AddressRanges` i `cdk.json`.

Når en bruker klikker for å publisere boten, starter [AWS CodeBuild](https://aws.amazon.com/codebuild/) en CDK-distribueringsoppgave for å klargjøre API-stakken (Se også: [CDK-definisjon](../cdk/lib/api-publishment-stack.ts)) som inneholder API Gateway, Lambda og SQS. SQS brukes for å koble fra brukerforespørselen og LLM-operasjonen fordi generering av output kan overstige 30 sekunder, som er grensen for API Gateway-kvoten. For å hente output må man få tilgang til API-et asynkront. For mer detaljer, se [API-spesifikasjon](#api-specification).

Klienten må sette `x-api-key` i forespørselens header.

## API-spesifikasjon

Se [her](https://aws-samples.github.io/bedrock-chat).