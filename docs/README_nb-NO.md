<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md)

En flerspråklig generativ AI-plattform drevet av [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Støtter chat, tilpassede bots med kunnskap (RAG), deling av bots via en bot-butikk og automatisering av oppgaver ved hjelp av agenter.

![](./imgs/demo.gif)

> [!Advarsel]
>
> **V3 er lansert. For å oppdatere, vennligst les grundig gjennom [migreringsveiledningen](./migration/V2_TO_V3_nb-NO.md).** Uten forsiktighet vil **BOTS FRA V2 BLI UBRUKELIGE.**

### Bot-personalisering / Bot-butikk

Legg til din egen instruksjon og kunnskap (også kjent som [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Boten kan deles blant applikasjonens brukere via bot-butikkens markedsplass. Den tilpassede boten kan også publiseres som en frittstående API (Se [detaljer](./PUBLISH_API_nb-NO.md)).

<details>
<summary>Skjermbilder</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Du kan også importere eksisterende [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/).

![](./imgs/import_existing_kb.png)

</details>

> [!Viktig]
> Av styringshensyn kan kun tillatte brukere opprette tilpassede bots. For å tillate opprettelse av tilpassede bots, må brukeren være medlem av gruppen kalt `CreatingBotAllowed`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at brukergruppe-ID-en kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Administrative funksjoner

API-administrasjon, merke bots som essensielle, analysere bruk for bots. [detaljer](./ADMINISTRATOR_nb-NO.md)

<details>
<summary>Skjermbilder</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agent

Ved å bruke [Agent-funksjonaliteten](./AGENT_nb-NO.md) kan din chatbot automatisk håndtere mer komplekse oppgaver. For eksempel kan Agenten hente nødvendig informasjon fra eksterne verktøy eller dele opp oppgaven i flere trinn for behandling.

<details>
<summary>Skjermbilder</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Superkjapp Distribusjon

- I us-east-1-regionen, åpne [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Administrer modelltilgang` > Merk alle modeller du ønsker å bruke og klikk så `Lagre endringer`.

<details>
<summary>Skjermbilde</summary>

![](./imgs/model_screenshot.png)

</details>

- Åpne [CloudShell](https://console.aws.amazon.com/cloudshell/home) i regionen der du vil distribuere
- Kjør distribusjon via følgende kommandoer. Hvis du vil spesifisere versjonen som skal distribueres eller trenger å legge til sikkerhetspolicyer, kan du angi de aktuelle parameterne fra [Valgfrie parametere](#valgfrie-parametere).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Du vil bli spurt om du er en ny bruker eller bruker v3. Hvis du ikke er en fortsettende bruker fra v0, vennligst skriv `y`.

### Valgfrie parametere

Du kan spesifisere følgende parametere under distribusjon for å forbedre sikkerhet og tilpasning:

- **--disable-self-register**: Deaktiver selvregistrering (standard: aktivert). Hvis dette flagget er satt, må du opprette alle brukere på Cognito, og det vil ikke tillate brukere å registrere seg selv.
- **--enable-lambda-snapstart**: Aktiver [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (standard: deaktivert). Hvis dette flagget er satt, forbedres oppstartstider for Lambda-funksjoner, noe som gir raskere responstider for bedre brukeropplevelse.
- **--ipv4-ranges**: Kommaseparert liste over tillatte IPv4-områder. (standard: tillat alle IPv4-adresser)
- **--ipv6-ranges**: Kommaseparert liste over tillatte IPv6-områder. (standard: tillat alle IPv6-adresser)
- **--disable-ipv6**: Deaktiver tilkoblinger over IPv6. (standard: aktivert)
- **--allowed-signup-email-domains**: Kommaseparert liste over tillatte e-postdomener for påmelding. (standard: ingen domenebegrensning)
- **--bedrock-region**: Definer regionen der Bedrock er tilgjengelig. (standard: us-east-1)
- **--repo-url**: Den egendefinerte repositoryen til Bedrock Chat som skal distribueres, hvis den er forket eller har egendefinert kildekontroll. (standard: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Versjonen av Bedrock Chat som skal distribueres. (standard: nyeste versjon under utvikling)
- **--cdk-json-override**: Du kan overstyre CDK-kontekstverdier under distribusjon ved å bruke overstyrings-JSON-blokken. Dette lar deg endre konfigurasjonen uten å redigere cdk.json-filen direkte.

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
> Overstyringsparameterne vil bli slått sammen med den eksisterende cdk.json-konfigurasjonen under distribusjonstiden i AWS-kodebygningen. Verdier som er angitt i overstyringen vil ha forrang fremfor verdiene i cdk.json.

#### Eksempelkommando med parametere:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Etter omtrent 35 minutter vil du få følgende utdata, som du kan åpne i nettleseren din

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Påmeldingsskjermen vil vises som vist over, hvor du kan registrere e-posten din og logge deg på.

> [!Viktig]
> Uten å sette valgfri parameter vil denne distribusjonsmåten tillate hvem som helst som kjenner URL-en å registrere seg. For produksjonsbruk anbefales det sterkt å legge til IP-adressebegrensninger og deaktivere selvregistrering for å redusere sikkerhetsrisikoer (du kan definere allowed-signup-email-domains for å begrense brukere slik at kun e-postadresser fra bedriftens domene kan registrere seg). Bruk både ipv4-ranges og ipv6-ranges for IP-adressebegrensninger, og deaktiver selvregistrering ved å bruke disable-self-register når du kjører ./bin.

> [!TIPS]
> Hvis `Frontend URL` ikke vises eller Bedrock Chat ikke fungerer som den skal, kan det være et problem med den nyeste versjonen. I så fall kan du legge til `--version "v3.0.0"` i parameterne og prøve distribusjon på nytt.

## Arkitektur

Det er en arkitektur bygget på AWS-administrerte tjenester, som eliminerer behovet for infrastrukturhåndtering. Ved å bruke Amazon Bedrock er det ikke nødvendig å kommunisere med API-er utenfor AWS. Dette muliggjør distribusjon av skalerbare, pålitelige og sikre applikasjoner.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL-database for lagring av samtalehistorikk
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend API-endepunkt ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Frontend-applikasjonsleveranse ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP-adressebegrensning
- [Amazon Cognito](https://aws.amazon.com/cognito/): Brukerautentisering
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Administrert tjeneste for å utnytte grunnleggende modeller via API-er
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Gir et administrert grensesnitt for Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), som tilbyr tjenester for embedding og parsing av dokumenter
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Mottar hendelse fra DynamoDB-strøm og starter Step Functions for å bygge inn ekstern kunnskap
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orkestrerer inngangspipeline for å bygge inn ekstern kunnskap i Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Fungerer som backend-database for Bedrock Knowledge Bases, og gir full tekst-søk og vektor-søk-muligheter, som muliggjør nøyaktig henting av relevante opplysninger
- [Amazon Athena](https://aws.amazon.com/athena/): Spørretjeneste for å analysere S3-bøtte

![](./imgs/arch.png)

## Distribuer ved hjelp av CDK

Super-enkel distribusjon bruker [AWS CodeBuild](https://aws.amazon.com/codebuild/) til å utføre distribusjon med CDK internt. Denne seksjonen beskriver fremgangsmåten for å distribuere direkte med CDK.

- Vennligst ha UNIX, Docker og et Node.js-kjøretidsmiljø. Hvis ikke, kan du også bruke [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Viktig]
> Hvis det er utilstrekkelig lagringskapasitet i det lokale miljøet under distribusjon, kan CDK-bootstrapping resultere i en feil. Hvis du kjører i Cloud9 osv., anbefaler vi å utvide volumstørrelsen på instansen før distribusjon.

- Klone dette repositoriet

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Installer npm-pakker

```
cd bedrock-chat
cd cdk
npm ci
```

- Rediger om nødvendig følgende oppføringer i [cdk.json](./cdk/cdk.json) ved behov.

  - `bedrockRegion`: Region hvor Bedrock er tilgjengelig. **MERK: Bedrock støtter IKKE alle regioner for øyeblikket.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Tillatte IP-adresseområder.
  - `enableLambdaSnapStart`: Standard er true. Sett til false hvis du distribuerer til en [region som ikke støtter Lambda SnapStart for Python-funksjoner](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Før du distribuerer CDK, må du bootstrappe én gang for regionen du distribuerer til.

```
npx cdk bootstrap
```

- Distribuer dette eksempelprosjektet

```
npx cdk deploy --require-approval never --all
```

- Du vil få en output som ligner følgende. URL-en til web-appen vil bli vist i `BedrockChatStack.FrontendURL`, så vennligst åpne den i nettleseren.

```sh
 ✅  BedrockChatStack

✨  Distribusjonstid: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definere parametere

Du kan definere parametere for distribusjonen på to måter: ved å bruke `cdk.json` eller ved å bruke den typesikre `parameter.ts`-filen.

#### Bruke cdk.json (Tradisjonell metode)

Den tradisjonelle måten å konfigurere parametere på er ved å redigere `cdk.json`-filen. Denne tilnærmingen er enkel, men mangler typekontroll:

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

#### Bruke parameter.ts (Anbefalt typesikker metode)

For bedre typesikkerhet og utvikleropplevelse kan du bruke `parameter.ts`-filen til å definere parameterne dine:

```typescript
// Definer parametere for standardmiljøet
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definer parametere for tilleggsmiljøer
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Kostnadsbesparende for dev-miljø
  enableBotStoreReplicas: false, // Kostnadsbesparende for dev-miljø
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Forbedret tilgjengelighet for produksjon
  enableBotStoreReplicas: true, // Forbedret tilgjengelighet for produksjon
});
```

> [!Merk]
> Eksisterende brukere kan fortsette å bruke `cdk.json` uten endringer. `parameter.ts`-tilnærmingen anbefales for nye distribusjoner eller når du trenger å administrere flere miljøer.

### Distribuere flere miljøer

Du kan distribuere flere miljøer fra samme kodebase ved å bruke `parameter.ts`-filen og `-c envName`-alternativet.

#### Forutsetninger

1. Definer miljøene dine i `parameter.ts` som vist ovenfor
2. Hvert miljø vil ha sine egne ressurser med miljøspesifikke prefikser

#### Distribusjonskommandoer

For å distribuere et bestemt miljø:

```bash
# Distribuer dev-miljøet
npx cdk deploy --all -c envName=dev

# Distribuer prod-miljøet
npx cdk deploy --all -c envName=prod
```

Hvis intet miljø er angitt, brukes "default"-miljøet:

```bash
# Distribuer standardmiljøet
npx cdk deploy --all
```

#### Viktige merknader

1. **Stabelnavn**:

   - Hovedstablene for hvert miljø vil være prefiks med miljønavnet (f.eks. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Imidlertid vil ikke tilpassede botstaber (`BrChatKbStack*`) og API-publiseringsstaber (`ApiPublishmentStack*`) motta miljøprefikser da de opprettes dynamisk ved kjøretid

2. **Ressursnavn**:

   - Bare noen ressurser får miljøprefikser i navnene sine (f.eks. `dev_ddb_export`-tabell, `dev-FrontendWebAcl`)
   - De fleste ressurser beholder sine opprinnelige navn, men er isolert ved å være i forskjellige stabler

3. **Miljøidentifikasjon**:

   - Alle ressurser er merket med en `CDKEnvironment`-tag som inneholder miljønavnet
   - Du kan bruke denne taggen til å identifisere hvilket miljø en ressurs tilhører
   - Eksempel: `CDKEnvironment: dev` eller `CDKEnvironment: prod`

4. **Overstyring av standardmiljø**: Hvis du definerer et "default"-miljø i `parameter.ts`, vil det overstyre innstillingene i `cdk.json`. For å fortsette å bruke `cdk.json`, ikke definer et "default"-miljø i `parameter.ts`.

5. **Miljøkrav**: For å opprette andre miljøer enn "default", må du bruke `parameter.ts`. `-c envName`-alternativet alene er ikke tilstrekkelig uten tilsvarende miljødefinisjon.

6. **Ressursisolasjon**: Hvert miljø oppretter sitt eget sett med ressurser, slik at du kan ha utviklings-, test- og produksjonsmiljøer i samme AWS-konto uten konflikter.

## Andre

Du kan definere parametere for distribusjonen din på to måter: ved å bruke `cdk.json` eller ved å bruke den typesikre `parameter.ts`-filen.

#### Bruke cdk.json (Tradisjonell metode)

Den tradisjonelle måten å konfigurere parametere på er ved å redigere `cdk.json`-filen. Denne tilnærmingen er enkel, men mangler typekontroll:

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

#### Bruke parameter.ts (Anbefalt typesikker metode)

For bedre typesikkerhet og utvikleropplevelse kan du bruke `parameter.ts`-filen til å definere parameterne dine:

```typescript
// Definer parametere for standardmiljøet
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definer parametere for tilleggsmiljøer
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Kostnadsbesparende for utviklingsmiljø
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Forbedret tilgjengelighet for produksjon
});
```

> [!Merk]
> Eksisterende brukere kan fortsette å bruke `cdk.json` uten endringer. `parameter.ts`-tilnærmingen anbefales for nye distribusjoner eller når du trenger å administrere flere miljøer.

### Distribuere flere miljøer

Du kan distribuere flere miljøer fra samme kodebase ved å bruke `parameter.ts`-filen og `-c envName`-alternativet.

#### Forutsetninger

1. Definer miljøene dine i `parameter.ts` som vist ovenfor
2. Hvert miljø vil ha sine egne ressurser med miljøspesifikke prefikser

#### Distribusjonskommandoer

For å distribuere et bestemt miljø:

```bash
# Distribuer utviklingsmiljøet
npx cdk deploy --all -c envName=dev

# Distribuer produksjonsmiljøet
npx cdk deploy --all -c envName=prod
```

Hvis ingen miljø er spesifisert, brukes "default"-miljøet:

```bash
# Distribuer standardmiljøet
npx cdk deploy --all
```

#### Viktige merknader

1. **Stabelnavn**:

   - Hovedstablene for hvert miljø vil ha et prefiks med miljønavnet (f.eks. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Imidlertid får egendefinerte botstaber (`BrChatKbStack*`) og API-publiseringsstaber (`ApiPublishmentStack*`) ikke miljøprefikser da de opprettes dynamisk under kjøring

2. **Ressursnavn**:

   - Bare noen ressurser får miljøprefikser i navnene (f.eks. `dev_ddb_export`-tabell, `dev-FrontendWebAcl`)
   - De fleste ressurser beholder sine opprinnelige navn, men er isolert ved å være i forskjellige stabler

3. **Miljøidentifikasjon**:

   - Alle ressurser merkes med en `CDKEnvironment`-tag som inneholder miljønavnet
   - Du kan bruke denne taggen til å identifisere hvilket miljø en ressurs tilhører
   - Eksempel: `CDKEnvironment: dev` eller `CDKEnvironment: prod`

4. **Overstyring av standardmiljø**: Hvis du definerer et "default"-miljø i `parameter.ts`, vil det overstyre innstillingene i `cdk.json`. For å fortsette å bruke `cdk.json`, ikke definer et "default"-miljø i `parameter.ts`.

5. **Miljøkrav**: For å opprette andre miljøer enn "default", må du bruke `parameter.ts`. `-c envName`-alternativet alene er ikke tilstrekkelig uten tilsvarende miljødefinisjon.

6. **Ressursisolasjon**: Hvert miljø oppretter sitt eget sett med ressurser, slik at du kan ha utviklings-, test- og produksjonsmiljøer i samme AWS-konto uten konflikter.

## Andre

### Fjern ressurser

Hvis du bruker CLI og CDK, kan du kjøre `npx cdk destroy`. Hvis ikke, gå til [CloudFormation](https://console.aws.amazon.com/cloudformation/home) og slett `BedrockChatStack` og `FrontendWafStack` manuelt. Vær oppmerksom på at `FrontendWafStack` er i `us-east-1`-regionen.

### Språkinnstillinger

Denne ressursen oppdager automatisk språket ved hjelp av [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Du kan bytte språk fra programmenyen. Alternativt kan du bruke Query String for å angi språket som vist nedenfor.

> `https://example.com?lng=ja`

### Deaktiver selvregistrering

Denne malen har selvregistrering aktivert som standard. For å deaktivere selvregistrering, åpne [cdk.json](./cdk/cdk.json) og sett `selfSignUpEnabled` til `false`. Hvis du konfigurerer [ekstern identitetsleverandør](#external-identity-provider), vil verdien bli ignorert og automatisk deaktivert.

### Begrens domener for påmeldingse-postadresser

Som standard begrenser denne malen ikke domenene for påmeldingse-postadresser. For å tillate påmelding kun fra bestemte domener, åpne `cdk.json` og angi domenene som en liste i `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Ekstern identitetsleverandør

Denne malen støtter ekstern identitetsleverandør. For øyeblikket støtter vi [Google](./idp/SET_UP_GOOGLE_nb-NO.md) og [egendefinert OIDC-leverandør](./idp/SET_UP_CUSTOM_OIDC_nb-NO.md).

### Legg til nye brukere i grupper automatisk

Denne malen har følgende grupper for å gi tillatelser til brukere:

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
- **false**: Reduserer kostnader ved å bruke færre replikaer, egnet for utvikling og testing.

Dette er en konto-/regioninnstilling som påvirker hele applikasjonen, ikke individuelle bots.

> [!Merk]
> Per juni 2024 støtter Amazon OpenSearch Serverless 0,5 OCU, noe som senker inngangskostnadene for små arbeidsbelastninger. Produksjonsdistribusjoner kan starte med 2 OCU, mens dev/test-arbeidsbelastninger kan bruke 1 OCU. OpenSearch Serverless skaleres automatisk basert på arbeidsbelastningskrav. For mer informasjon, besøk [kunngjøringen](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Konfigurer Bot Store

Bot store-funksjonen lar brukere dele og oppdage tilpassede bots. Du kan konfigurere bot store gjennom følgende innstillinger i [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Styrer om bot store-funksjonen er aktivert (standard: `true`)
- **botStoreLanguage**: Setter hovedspråket for bot-søk og -oppdagelse (standard: `"en"`). Dette påvirker hvordan bots indekseres og søkes i bot store, og optimaliserer tekstanalyse for det angitte språket.
- **enableBotStoreReplicas**: Styrer om standby-replikaer er aktivert for OpenSearch Serverless-samlingen som brukes av bot store (standard: `false`). Å sette den til `true` forbedrer tilgjengelighet, men øker kostnadene, mens `false` reduserer kostnadene, men kan påvirke tilgjengeligheten.
  > **Viktig**: Du kan ikke oppdatere denne egenskapen etter at samlingen allerede er opprettet. Hvis du prøver å endre denne egenskapen, vil samlingen fortsette å bruke den opprinnelige verdien.

### Kryssregional inferens

[Kryssregional inferens](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) lar Amazon Bedrock dynamisk rute modellinferensforespørsler på tvers av flere AWS-regioner, noe som forbedrer gjennomstrømning og motstandsdyktighet under perioder med høy etterspørsel. For å konfigurere, rediger `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) forbedrer kalde oppstartstider for Lambda-funksjoner og gir raskere svartider for bedre brukeropplevelse. På den annen side er det for Python-funksjoner en [avgift avhengig av cachestørrelse](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) og [ikke tilgjengelig i noen regioner](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) for øyeblikket. For å deaktivere SnapStart, rediger `cdk.json`.

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

- `alternateDomainName`: Det egendefinerte domenenavnet for chatteprogrammet (f.eks. chat.example.com)
- `hostedZoneId`: ID-en til Route 53-sonen der domeneopptegnelsene vil bli opprettet

Når disse parameterne er angitt, vil distribusjonen automatisk:

- Opprette et ACM-sertifikat med DNS-validering i us-east-1-regionen
- Opprette de nødvendige DNS-oppføringene i Route 53-sonen
- Konfigurere CloudFront til å bruke ditt egendefinerte domene

> [!Merk]
> Domenet må administreres av Route 53 i AWS-kontoen din. Vertssonens ID kan finnes i Route 53-konsollen.

### Lokal utvikling

Se [LOKAL UTVIKLING](./LOCAL_DEVELOPMENT_nb-NO.md).

### Bidrag

Takk for at du vurderer å bidra til dette repositoriet! Vi ønsker velkommen feilrettinger, språkoversettelser (i18n), forbedringer av funksjoner, [agent-verktøy](./docs/AGENT.md#how-to-develop-your-own-tools) og andre forbedringer.

For forbedringer av funksjoner og andre forbedringer, **før du oppretter en Pull Request, setter vi stor pris på om du kan opprette en Feature Request-sak for å diskutere implementeringsmetoden og detaljene. For feilrettinger og språkoversettelser (i18n) kan du gå videre med å opprette en Pull Request direkte.**

Ta også en titt på følgende retningslinjer før du bidrar:

- [Lokal utvikling](./LOCAL_DEVELOPMENT_nb-NO.md)
- [BIDRAG](./CONTRIBUTING_nb-NO.md)

## Kontakter

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Betydelige bidragsytere

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Bidragsytere

[![bedrock chat bidragsytere](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Lisens

Dette biblioteket er lisensiert under MIT-0-lisensen. Se [LICENSE-filen](./LICENSE).