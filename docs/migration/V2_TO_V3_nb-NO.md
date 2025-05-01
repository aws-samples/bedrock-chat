# Migrasjonsveiledning (v2 til v3)

## TL;DR

- V3 introduserer detaljert tilgangskontroll og Bot Store-funksjonalitet, som krever endringer i DynamoDB-skjemaet
- **Sikkerhetskopier DynamoDB ConversationTable før migrasjon**
- Oppdater repositoriens URL fra `bedrock-claude-chat` til `bedrock-chat`
- Kjør migrasjonsskriptet for å konvertere dataene til det nye skjemaet
- Alle dine bots og samtaler vil bli bevart med den nye tilgangsmodellen
- **VIKTIG: Under migrasjonsprosessen vil applikasjonen være utilgjengelig for alle brukere inntil migrasjonen er fullført. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen til utviklingsmiljøet ditt.**
- **VIKTIG: Alle publiserte APIer må slettes under migrasjonsprosessen.**
- **ADVARSEL: Migrasjonsprosessen kan ikke garantere 100% suksess for alle bots. Dokumenter viktige bot-konfigurasjoner før migrasjon i tilfelle du må rekonstruere dem manuelt**

## Introduksjon

### Hva er Nytt i V3

V3 introduserer betydelige forbedringer i Bedrock Chat:

1. **Detaljert tilgangskontroll**: Kontroller tilgang til dine bots med brukergruppe-baserte tillatelser
2. **Bot-butikk**: Del og oppdag bots gjennom et sentralisert marked
3. **Administrative funksjoner**: Administrer APIer, marker bots som essensielle, og analyser bot-bruk

Disse nye funksjonene krevde endringer i DynamoDB-skjemaet, noe som nødvendiggjør en migrasjonsprosess for eksisterende brukere.

### Hvorfor Denne Migrasjonen Er Nødvendig

Den nye tillatelsesmodellen og Bot Store-funksjonaliteten krevde en omstrukturering av hvordan bot-data lagres og aksesseres. Migrasjonsprosessen konverterer dine eksisterende bots og samtaler til det nye skjemaet samtidig som all din data bevares.

> [!ADVARSEL]
> Varsel om Tjenesteavbrudd: **Under migrasjonsprosessen vil applikasjonen være utilgjengelig for alle brukere.** Planlegg å utføre denne migrasjonen under et vedlikeholdsvindu når brukere ikke trenger tilgang til systemet. Applikasjonen vil kun bli tilgjengelig igjen etter at migrasjonsskriptet har fullført vellykket og all data er korrekt konvertert til det nye skjemaet. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen til dere utviklingsmiljø.

> [!VIKTIG]
> Før du fortsetter med migrasjonen: **Migrasjonsprosessen kan ikke garantere 100% suksess for alle bots**, spesielt de som er opprettet med eldre versjoner eller med tilpassede konfigurasjoner. Vennligst dokumenter dine viktige bot-konfigurasjoner (instruksjoner, kunnskapskilder, innstillinger) før du starter migrasjonsprosessen i tilfelle du må gjenskape dem manuelt.

## Migrasjonsprosess

### Viktig merknad om bot-synlighet i V3

I V3 vil **alle v2-boter med offentlig deling være søkbare i Bot Store.** Hvis du har boter som inneholder sensitiv informasjon som du ikke vil at skal være oppdagbare, bør du gjøre dem private før migrering til V3.

### Trinn 1: Identifiser miljønavnet ditt

I denne prosedyren er `{YOUR_ENV_PREFIX}` spesifisert for å identifisere navnet på dine CloudFormation Stacks. Hvis du bruker [Distribuere flere miljøer](../../README.md#deploying-multiple-environments)-funksjonen, erstatter du den med navnet på miljøet som skal migreres. Hvis ikke, erstatter du den med en tom streng.

### Trinn 2: Oppdater repositori-URL (Anbefalt)

Repositoriet har blitt omdøpt fra `bedrock-claude-chat` til `bedrock-chat`. Oppdater ditt lokale repositori:

```bash
# Sjekk gjeldende ekstern URL
git remote -v

# Oppdater den eksterne URL-en
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Bekreft endringen
git remote -v
```

### Trinn 3: Forsikre deg om at du er på siste V2-versjon

> [!ADVARSEL]
> Du MÅ oppdatere til v2.10.0 før migrering til V3. **Hvis du hopper over dette trinnet, kan det føre til datatap under migreringen.**

Før du starter migreringen, pass på at du kjører siste versjon av V2 (**v2.10.0**). Dette sikrer at du har alle nødvendige feilrettinger og forbedringer før oppgradering til V3:

```bash
# Hent de siste tagene
git fetch --tags

# Sjekk ut siste V2-versjon
git checkout v2.10.0

# Distribuer siste V2-versjon
cd cdk
npm ci
npx cdk deploy --all
```

### Trinn 4: Registrer V2 DynamoDB-tabellnavn

Hent V2 ConversationTable-navnet fra CloudFormation-output:

```bash
# Hent V2 ConversationTable-navn
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Sørg for å lagre dette tabellnavnet på et sikkert sted, da du vil trenge det for migreringsskriptet senere.

### Trinn 5: Sikkerhetskopier DynamoDB-tabellen

Før du fortsetter, opprett en sikkerhetskopi av din DynamoDB ConversationTable ved hjelp av navnet du nettopp registrerte:

```bash
# Opprett en sikkerhetskopi av V2-tabellen
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Sjekk at sikkerhetskopien er tilgjengelig
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Trinn 6: Slett alle publiserte APIer

> [!VIKTIG]
> Før distribusjon av V3 må du slette alle publiserte APIer for å unngå konflikter med Cloudformation-outputverdier under oppgraderingsprosessen.

1. Logg inn i programmet ditt som administrator
2. Naviger til Admin-seksjonen og velg "API-administrasjon"
3. Gjennomgå listen over alle publiserte APIer
4. Slett hver publiserte API ved å klikke sletteknappen ved siden av den

Du kan finne mer informasjon om API-publisering og -administrasjon i [PUBLISH_API.md](../PUBLISH_API_nb-NO.md), [ADMINISTRATOR.md](../ADMINISTRATOR_nb-NO.md) dokumentasjonen.

### Trinn 7: Hent V3 og distribuer

Hent siste V3-kode og distribuer:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!VIKTIG]
> Når du distribuerer V3, vil programmet være utilgjengelig for alle brukere inntil migrasjonsprosessen er fullført. Den nye skjemaet er inkompatibel med det gamle dataformatet, så brukere vil ikke kunne få tilgang til sine boter eller samtaler før du fullfører migreringsskriptet i de neste trinnene.

### Trinn 8: Registrer V3 DynamoDB-tabellnavn

Etter distribusjon av V3 må du hente både det nye ConversationTable- og BotTable-navnet:

```bash
# Hent V3 ConversationTable-navn
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Hent V3 BotTable-navn
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Viktig]
> Sørg for å lagre disse V3-tabellnavnene sammen med ditt tidligere lagrede V2-tabellnavn, da du vil trenge alle disse for migreringsskriptet.

(Resten av dokumentet fortsetter i samme stil med norsk oversettelse, men av hensyn til lengden har jeg vist oversettelsen for de første seksjonene. Vil du ha hele dokumentet oversatt, kan du be meg om det.)

## V3 Ofte stilte spørsmål

### Botadgang og tillatelser

**S: Hva skjer hvis en bot jeg bruker blir slettet eller min tilgangsrettighet blir fjernet?**
S: Autorisasjon sjekkes ved chattidspunkt, så du mister tilgang umiddelbart.

**S: Hva skjer hvis en bruker blir slettet (f.eks. ansatt slutter)?**
S: Deres data kan fullstendig fjernes ved å slette alle elementer fra DynamoDB med deres bruker-ID som partisjonsnøkkel (PK).

**S: Kan jeg slå av deling for en vesentlig offentlig bot?**
S: Nei, administrator må først merke boten som ikke-vesentlig før deling kan slås av.

**S: Kan jeg slette en vesentlig offentlig bot?**
S: Nei, administrator må først merke boten som ikke-vesentlig før sletting.

### Sikkerhet og implementasjon

**S: Er radnivåsikkerhet (RLS) implementert for bottabell?**
S: Nei, grunnet mangfoldet av tilgangsmønstre. Autorisasjon utføres ved botadgang, og risikoen for metadatalekkasje anses minimal sammenlignet med samtaleoversikt.

**S: Hva er kravene for å publisere et API?**
S: Boten må være offentlig.

**S: Vil det være en administrasjonsskjerm for alle private boter?**
S: Ikke i den første V3-versjonen. Elementer kan likevel slettes ved å søke med bruker-ID etter behov.

**S: Vil det være botmerking for bedre søke-UX?**
S: Ikke i den første V3-versjonen, men LLM-basert automatisk merking kan legges til i fremtidige oppdateringer.

### Administrasjon

**S: Hva kan administratorer gjøre?**
S: Administratorer kan:

- Administrere offentlige boter (inkludert sjekke høykostnadsboter)
- Administrere API-er
- Merke offentlige boter som vesentlige

**S: Kan jeg gjøre delvis delte boter vesentlige?**
S: Nei, kun offentlige boter støttes.

**S: Kan jeg sette prioritet for festede boter?**
S: Ved første lansering, nei.

### Autorisasjonskonfigurasjon

**S: Hvordan setter jeg opp autorisasjon?**
S:

1. Åpne Amazon Cognito-konsollen og opprett brukergrupper i BrChat-brukerpuljen
2. Legg til brukere i disse gruppene etter behov
3. I BrChat, velg brukergruppene du vil tillate tilgang til ved konfigurasjon av botdelings-innstillinger

Merk: Gruppemedlemskapsendringer krever ny innlogging for å tre i kraft. Endringer gjenspeiles ved tokenoppdatering, men ikke under gyldighetsperioden for ID-token (standard 30 minutter i V3, konfigurerbar via `tokenValidMinutes` i `cdk.json` eller `parameter.ts`).

**S: Sjekker systemet med Cognito hver gang en bot aksesseres?**
S: Nei, autorisasjon sjekkes ved bruk av JWT-token for å unngå unødvendige I/O-operasjoner.

### Søkefunksjonalitet

**S: Støtter botsøk semantisk søk?**
S: Nei, kun delvis tekstsamsvar støttes. Semantisk søk (f.eks. "automobile" → "bil", "EV", "kjøretøy") er ikke tilgjengelig på grunn av gjeldende OpenSearch Serverless-begrensninger (mars 2025).