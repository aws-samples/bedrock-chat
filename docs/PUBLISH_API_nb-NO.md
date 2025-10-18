# API-publisering

## Oversikt

Dette eksempelet inkluderer en funksjon for å publisere API-er. Selv om et chatgrensesnitt kan være praktisk for innledende validering, avhenger den faktiske implementeringen av den spesifikke brukssituasjonen og brukeropplevelsen (UX) som ønskes for sluttbrukeren. I noen scenarioer kan et chat-grensesnitt være det foretrukne valget, mens i andre tilfeller kan et frittstående API være mer egnet. Etter innledende validering gir dette eksempelet muligheten til å publisere tilpassede boter i henhold til prosjektets behov. Ved å legge inn innstillinger for kvoter, begrensninger, opprinnelser osv., kan et endepunkt publiseres sammen med en API-nøkkel, noe som gir fleksibilitet for ulike integrasjonsmuligheter.

## Sikkerhet

Bruk av kun en API-nøkkel anbefales ikke, som beskrevet i: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Derfor implementerer dette eksempelet en enkel IP-adressebegrensning via AWS WAF. WAF-regelen brukes felles på tvers av applikasjonen av kostnadshensyn, under antagelsen om at kildene man ønsker å begrense sannsynligvis er de samme på tvers av alle utstedte API-er. **Vennligst følg din organisasjons sikkerhetspolicy for faktisk implementering.** Se også [Arkitektur](#architecture)-seksjonen.

## Hvordan publisere tilpasset bot-API

### Forutsetninger

Av styringsmessige årsaker kan bare et begrenset antall brukere publisere boter. Før publisering må brukeren være medlem av gruppen kalt `PublishAllowed`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at brukergruppe-ID-en kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### API-publiseringsinnstillinger

Etter å ha logget inn som en `PublishedAllowed`-bruker og opprettet en bot, velg `API PublishSettings`. Merk at bare en delt bot kan publiseres.
![](./imgs/bot_api_publish_screenshot.png)

På følgende skjerm kan vi konfigurere flere parametere angående begrensning. For detaljer, se også: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Etter distribusjon vil følgende skjerm vises hvor du kan få endepunkt-URL-en og en API-nøkkel. Vi kan også legge til og slette API-nøkler.

![](./imgs/bot_api_publish_screenshot3.png)

## Arkitektur

APIet er publisert som følgende diagram:

![](./imgs/published_arch.png)

WAF brukes for IP-adressebegrensning. Adressen kan konfigureres ved å sette parameterne `publishedApiAllowedIpV4AddressRanges` og `publishedApiAllowedIpV6AddressRanges` i `cdk.json`.

Når en bruker klikker for å publisere boten, starter [AWS CodeBuild](https://aws.amazon.com/codebuild/) en CDK-distribueringsoppgave for å klargjøre API-stacken (Se også: [CDK-definisjon](../cdk/lib/api-publishment-stack.ts)) som inneholder API Gateway, Lambda og SQS. SQS brukes for å skille brukerforespørselen fra LLM-operasjonen fordi generering av output kan overskride 30 sekunder, som er grensen for API Gateway-kvoten. For å hente outputen må man få tilgang til APIet asynkront. For mer detaljer, se [API-spesifikasjon](#api-specification).

Klienten må sette `x-api-key` i forespørselens header.

## API-spesifikasjon

Se [her](https://aws-samples.github.io/bedrock-chat).