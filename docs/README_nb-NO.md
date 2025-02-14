# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_no.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi.md)

> [!Advarsel]  
> **V2 er lansert. For å oppdatere, vennligst les nøye gjennom [migrasjonsveiledningen](./migration/V1_TO_V2_nb-NO.md).** Uten forsiktighet vil **ROBOTER FRA V1 BLI UBRUKELIGE.**

En flerspråklig chatbot som bruker LLM-modeller levert av [Amazon Bedrock](https://aws.amazon.com/bedrock/) for generativ AI.

### Se oversikt og installasjon på YouTube

[![Oversikt](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Grunnleggende samtale

![](./imgs/demo.gif)

### Bot-personalisering

Legg til din egen instruksjon og gi ekstern kunnskap som URL eller filer (også kjent som [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Roboten kan deles blant applikasjonsbrukere. Den tilpassede roboten kan også publiseres som en frittstående API (Se [detaljer](./PUBLISH_API_nb-NO.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Viktig]
> Av styringsmessige årsaker kan kun tillatte brukere opprette tilpassede roboter. For å tillate opprettelse av tilpassede roboter, må brukeren være medlem av gruppen kalt `CreatingBotAllowed`, som kan settes opp via administrasjonskonsollen > Amazon Cognito brukergrupper eller AWS CLI. Merk at brukergruppens ID kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Administratorpanel

<details>
<summary>Administratorpanel</summary>

Analyser bruk for hver bruker / robot på administratorpanelet. [detaljer](./ADMINISTRATOR_nb-NO.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLM-drevet Agent

<details>
<summary>LLM-drevet Agent</summary>

Ved å bruke [Agent-funksjonaliteten](./AGENT_nb-NO.md) kan chatboten automatisk håndtere mer komplekse oppgaver. For eksempel kan Agenten, for å svare på en brukers spørsmål, hente nødvendig informasjon fra eksterne verktøy eller dele opp oppgaven i flere trinn for behandling.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Superkjapp Distribusjon

- I us-east-1-regionen, åpne [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Administrer modelltilgang` > Merk alle `Anthropic / Claude 3`, alle `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` og `Cohere / Embed Multilingual`, og trykk så `Lagre endringer`.

<details>
<summary>Skjermbilde</summary>

![](./imgs/model_screenshot.png)

</details>

- Åpne [CloudShell](https://console.aws.amazon.com/cloudshell/home) i regionen der du vil distribuere
- Kjør distribusjon via følgende kommandoer. Hvis du vil spesifisere versjonen som skal distribueres eller trenger å bruke sikkerhetspolicyer, kan du angi egnede parametere fra [Valgfrie parametere](#valgfrie-parametere).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Du vil bli spurt om du er en ny bruker eller bruker v2. Hvis du ikke er en fortsatt bruker fra v0, kan du skrive `y`.

### Valgfrie parametere

Du kan spesifisere følgende parametere under distribusjon for å forbedre sikkerhet og tilpasning:

- **--disable-self-register**: Deaktiver selvregistrering (standard: aktivert). Hvis dette flagget er satt, må du opprette alle brukere på Cognito, og det vil ikke tillate brukere å registrere seg selv.
- **--enable-lambda-snapstart**: Aktiver [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (standard: deaktivert). Hvis dette flagget er satt, forbedres oppstartstider for Lambda-funksjoner, noe som gir raskere responstider for bedre brukeropplevelse.
- **--ipv4-ranges**: Kommaseparert liste over tillatte IPv4-områder. (standard: tillat alle IPv4-adresser)
- **--ipv6-ranges**: Kommaseparert liste over tillatte IPv6-områder. (standard: tillat alle IPv6-adresser)
- **--disable-ipv6**: Deaktiver tilkoblinger over IPv6. (standard: aktivert)
- **--allowed-signup-email-domains**: Kommaseparert liste over tillatte e-postdomener for påmelding. (standard: ingen domenebegrensning)
- **--bedrock-region**: Definer regionen der Bedrock er tilgjengelig. (standard: us-east-1)
- **--repo-url**: Den egendefinerte repositoryen til Bedrock Claude Chat som skal distribueres, hvis den er forket eller har egendefinert kildekontroll. (standard: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Versjonen av Bedrock Claude Chat som skal distribueres. (standard: siste versjon under utvikling)
- **--cdk-json-override**: Du kan overstyre alle CDK-kontekstverdier under distribusjon ved å bruke overstyrings-JSON-blokken. Dette lar deg endre konfigurasjonen uten å redigere cdk.json-filen direkte.

Eksempel på bruk:

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

Overstyrings-JSON-en må følge samme struktur som cdk.json. Du kan overstyre alle kontekstverdier, inkludert:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Og andre kontekstverdier definert i cdk.json

> [!Merk]
> Overstyringsverdiene vil bli slått sammen med eksisterende cdk.json-konfigurasjon under distribusjon i AWS-kodebygning. Verdier som er angitt i overstyrings-JSON-en, vil ha forrang fremfor verdiene i cdk.json.

#### Eksempelkommando med parametere:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Etter omtrent 35 minutter vil du få følgende utdata, som du kan åpne i nettleseren din

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Påmeldingsskjermen vil vises som vist ovenfor, hvor du kan registrere e-posten din og logge inn.

> [!Viktig]
> Uten å sette den valgfrie parameteren tillater denne distribusjonsmetoden at alle som kjenner URL-en kan registrere seg. For produksjonsbruk anbefales det sterkt å legge til IP-adressebegrensninger og deaktivere selvregistrering for å redusere sikkerhetsrisikoer (du kan definere allowed-signup-email-domains for å begrense brukere slik at kun e-postadresser fra selskapets domene kan registrere seg). Bruk både ipv4-ranges og ipv6-ranges for IP-adressebegrensninger, og deaktiver selvregistrering ved å bruke disable-self-register når du kjører ./bin.

> [!TIPS]
> Hvis `Frontend URL` ikke vises eller Bedrock Claude Chat ikke fungerer som den skal, kan det være et problem med den siste versjonen. I så fall kan du legge til `--version "v1.2.6"` i parameterne og prøve distribusjon på nytt.

## Arkitektur

Det er en arkitektur bygget på AWS-administrerte tjenester, som eliminerer behovet for infrastrukturhåndtering. Ved å bruke Amazon Bedrock er det ikke nødvendig å kommunisere med APIer utenfor AWS. Dette muliggjør distribusjon av skalerbare, pålitelige og sikre applikasjoner.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL-database for lagring av samtalehistorikk
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend API-endepunkt ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Frontend-applikasjonsleveranse ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP-adressebegrensning
- [Amazon Cognito](https://aws.amazon.com/cognito/): Brukerautentisering
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Administrert tjeneste for å utnytte grunnleggende modeller via APIer
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Tilbyr et administrert grensesnitt for Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), som tilbyr tjenester for embedding og parsing av dokumenter
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Mottar hendelse fra DynamoDB-strøm og starter Step Functions for å legge til ekstern kunnskap
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orkestrerer inntaksrørledning for å legge til ekstern kunnskap i Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Fungerer som backend-database for Bedrock Knowledge Bases, og gir full tekst-søk og vektorsøkemuligheter, som muliggjør nøyaktig henting av relevant informasjon
- [Amazon Athena](https://aws.amazon.com/athena/): Spørretjeneste for å analysere S3-bøtte

![](./imgs/arch.png)

## Distribuer ved bruk av CDK

Super-enkel distribusjon bruker [AWS CodeBuild](https://aws.amazon.com/codebuild/) til å utføre distribusjon med CDK internt. Denne seksjonen beskriver prosedyren for å distribuere direkte med CDK.

- Vennligst ha UNIX, Docker og et Node.js kjøretidsmiljø. Hvis ikke, kan du også bruke [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Viktig]
> Hvis det er utilstrekkelig lagringskapasitet i det lokale miljøet under distribusjon, kan CDK-bootstrapping resultere i en feil. Hvis du kjører i Cloud9 osv., anbefaler vi å utvide volumstørrelsen på instansen før distribusjon.

- Klone dette repositoriet

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Installer npm-pakker

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Rediger om nødvendig følgende oppføringer i [cdk.json](./cdk/cdk.json)

  - `bedrockRegion`: Region hvor Bedrock er tilgjengelig. **MERK: Bedrock støtter IKKE alle regioner for øyeblikket.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Tillatte IP-adresseområder.
  - `enableLambdaSnapStart`: Standard er true. Sett til false hvis du distribuerer til en [region som ikke støtter Lambda SnapStart for Python-funksjoner](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Før du distribuerer CDK, må du arbeide med Bootstrap én gang for regionen du distribuerer til.

```
npx cdk bootstrap
```

- Distribuer dette eksempelprosjektet

```
npx cdk deploy --require-approval never --all
```

- Du vil få en utdata som ligner følgende. URL-en til web-appen vil bli vist i `BedrockChatStack.FrontendURL`, så vennligst åpne den i nettleseren.

```sh
 ✅  BedrockChatStack

✨  Distribusjonstid: 78.57s

Utdata:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Andre

### Konfigurer støtte for Mistral-modeller

Oppdater `enableMistral` til `true` i [cdk.json](./cdk/cdk.json), og kjør `npx cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Viktig]
> Dette prosjektet fokuserer på Anthropic Claude-modeller, Mistral-modellene er begrenset støttet. For eksempel er prompteksempler basert på Claude-modeller. Dette er et Mistral-spesifikt alternativ, når du har slått på Mistral-modeller, kan du bare bruke Mistral-modeller for alle chat-funksjonene, IKKE både Claude og Mistral-modeller.

### Konfigurer standard tekstgenerering

Brukere kan justere [tekstgeneringsparameterne](https://docs.anthropic.com/claude/reference/complete_post) fra skjermen for oppretting av tilpasset bot. Hvis boten ikke brukes, vil standard parametere satt i [config.py](./backend/app/config.py) bli brukt.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Fjern ressurser

Hvis du bruker cli og CDK, kjør `npx cdk destroy`. Hvis ikke, åpne [CloudFormation](https://console.aws.amazon.com/cloudformation/home) og slett `BedrockChatStack` og `FrontendWafStack` manuelt. Merk at `FrontendWafStack` er i `us-east-1`-regionen.

### Språkinnstillinger

Denne ressursen oppdager automatisk språk ved hjelp av [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Du kan bytte språk fra applikasjonens meny. Alternativt kan du bruke Query String for å angi språk som vist nedenfor.

> `https://example.com?lng=ja`

### Deaktiver selvregistrering

Dette eksempelet har selvregistrering aktivert som standard. For å deaktivere selvregistrering, åpne [cdk.json](./cdk/cdk.json) og endre `selfSignUpEnabled` til `false`. Hvis du konfigurerer [ekstern identitetsleverandør](#external-identity-provider), vil verdien bli ignorert og automatisk deaktivert.

### Begrens domener for påmeldingse-postadresser

Som standard begrenser ikke dette eksempelet domenene for påmeldingse-postadresser. For å tillate påmelding kun fra bestemte domener, åpne `cdk.json` og angi domenene som en liste i `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Ekstern identitetsleverandør

Dette eksempelet støtter ekstern identitetsleverandør. For øyeblikket støtter vi [Google](./idp/SET_UP_GOOGLE_nb-NO.md) og [egen OIDC-leverandør](./idp/SET_UP_CUSTOM_OIDC_nb-NO.md).

### Legg til nye brukere i grupper automatisk

Dette eksempelet har følgende grupper for å gi tillatelser til brukere:

- [`Admin`](./ADMINISTRATOR_nb-NO.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_nb-NO.md)

Hvis du vil at nyopprettede brukere automatisk skal bli med i grupper, kan du angi dem i [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Som standard vil nyopprettede brukere bli med i `CreatingBotAllowed`-gruppen.

### Konfigurer RAG-replikaer

`enableRagReplicas` er et alternativ i [cdk.json](./cdk/cdk.json) som styrer replikainnstillingene for RAG-databasen, spesifikt Knowledge Bases som bruker Amazon OpenSearch Serverless.

- **Standard**: true
- **true**: Forbedrer tilgjengelighet ved å aktivere flere replikaer, egnet for produksjonsmiljøer, men øker kostnadene.
- **false**: Reduserer kostnadene ved å bruke færre replikaer, egnet for utvikling og testing.

Dette er en konto-/regioninnstilling som påvirker hele applikasjonen, ikke individuelle bots.

> [!Merk]
> Per juni 2024 støtter Amazon OpenSearch Serverless 0,5 OCU, noe som senker inngangskostnadene for små arbeidsbelastninger. Produksjonsdistribusjoner kan starte med 2 OCU, mens dev/test-arbeidsbelastninger kan bruke 1 OCU. OpenSearch Serverless skalerer automatisk basert på arbeidsbelastningskrav. For mer detaljer, besøk [kunngjøringen](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Kryssregional inferens

[Kryssregional inferens](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) lar Amazon Bedrock dynamisk rute modellinferensforespørsler på tvers av flere AWS-regioner, noe som forbedrer gjennomstrømning og motstandsdyktighet under perioder med høy etterspørsel. For å konfigurere, rediger `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) forbedrer kalde oppstartstider for Lambda-funksjoner, noe som gir raskere responstider for bedre brukeropplevelse. For Python-funksjoner er det imidlertid en [avgift avhengig av cachestørrelse](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) og [ikke tilgjengelig i noen regioner](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) for øyeblikket. For å deaktivere SnapStart, rediger `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Konfigurer egendefinert domene

Du kan konfigurere et egendefinert domene for CloudFront-distribusjonen ved å angi følgende parametere i [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Det egendefinerte domenenavnet for chat-applikasjonen din (f.eks. chat.example.com)
- `hostedZoneId`: ID-en til Route 53-hosted sonen der domenepostene vil bli opprettet

Når disse parameterne er oppgitt, vil distribusjonen automatisk:

- Opprette et ACM-sertifikat med DNS-validering i us-east-1-regionen
- Opprette de nødvendige DNS-postene i Route 53-hosted sonen din
- Konfigurere CloudFront til å bruke ditt egendefinerte domene

> [!Merk]
> Domenet må administreres av Route 53 i AWS-kontoen din. Hosted sone-ID-en kan finnes i Route 53-konsollen.

### Lokal utvikling

Se [LOKAL UTVIKLING](./LOCAL_DEVELOPMENT_nb-NO.md).

### Bidrag

Takk for at du vurderer å bidra til dette repositoriet! Vi ønsker velkommen feilrettinger, språkoversettelser (i18n), forbedringer av funksjoner, [agent-verktøy](./docs/AGENT.md#how-to-develop-your-own-tools) og andre forbedringer.

For funksjonsforbedringer og andre forbedringer, **før du oppretter en Pull Request, setter vi stor pris på om du oppretter en Feature Request-sak for å diskutere implementeringsmetoden og detaljene. For feilrettinger og språkoversettelser (i18n), gå videre med å opprette en Pull Request direkte.**

Ta også en titt på følgende retningslinjer før du bidrar:

- [Lokal utvikling](./LOCAL_DEVELOPMENT_nb-NO.md)
- [BIDRAG](./CONTRIBUTING_nb-NO.md)

## Kontakter

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Betydelige bidragsytere

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Bidragsytere

[![bedrock claude chat bidragsytere](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Lisens

Dette biblioteket er lisensiert under MIT-0-lisensen. Se [LICENSE-filen](./LICENSE).