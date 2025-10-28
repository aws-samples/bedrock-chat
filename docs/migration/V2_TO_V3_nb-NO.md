# Migrasjonsguide (v2 til v3)

## TL;DR

- V3 introduserer finkornede tilgangskontroller og Bot Store-funksjonalitet, som krever endringer i DynamoDB-skjemaet
- **Sikkerhetskopier DynamoDB ConversationTable før migrering**
- Oppdater repository-URL-en din fra `bedrock-claude-chat` til `bedrock-chat`
- Kjør migreringsscriptet for å konvertere dataene dine til det nye skjemaet
- Alle botene og samtalene dine vil bli bevart med den nye tilgangsmodellen
- **VIKTIG: Under migreringsprosessen vil applikasjonen være utilgjengelig for alle brukere til migreringen er fullført. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen til utviklingsmiljøet ditt.**
- **VIKTIG: Alle publiserte API-er må slettes under migreringsprosessen.**
- **ADVARSEL: Migreringsprosessen kan ikke garantere 100% suksess for alle boter. Vennligst dokumenter dine viktige bot-konfigurasjoner før migrering i tilfelle du må opprette dem på nytt manuelt**

## Introduksjon

### Hva er nytt i V3

V3 introduserer betydelige forbedringer til Bedrock Chat:

1. **Finjustert tilgangskontroll**: Kontroller tilgang til botene dine med gruppebaserte tillatelser
2. **Bot-butikk**: Del og oppdag boter gjennom en sentralisert markedsplass
3. **Administrative funksjoner**: Administrer API-er, merk boter som essensielle, og analyser bot-bruk

Disse nye funksjonene krevde endringer i DynamoDB-skjemaet, noe som nødvendiggjør en migrasjonsprosess for eksisterende brukere.

### Hvorfor denne migrasjonen er nødvendig

Den nye tilgangsmodellen og Bot-butikk-funksjonaliteten krevde restrukturering av hvordan bot-data lagres og aksesseres. Migrasjonsprosessen konverterer dine eksisterende boter og samtaler til det nye skjemaet mens alle dataene dine bevares.

> [!WARNING]
> Varsel om tjenesteavbrudd: **Under migrasjonsprosessen vil applikasjonen være utilgjengelig for alle brukere.** Planlegg å utføre denne migrasjonen i et vedlikeholdsvindu når brukere ikke trenger tilgang til systemet. Applikasjonen vil først bli tilgjengelig igjen etter at migrasjonsskriptet er fullført og alle data er korrekt konvertert til det nye skjemaet. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen i utviklingsmiljøet ditt.

> [!IMPORTANT]
> Før du fortsetter med migrasjonen: **Migrasjonsprosessen kan ikke garantere 100% suksess for alle boter**, spesielt de som ble opprettet med eldre versjoner eller med tilpassede konfigurasjoner. Vennligst dokumenter dine viktige bot-konfigurasjoner (instruksjoner, kunnskapskilder, innstillinger) før du starter migrasjonsprosessen i tilfelle du må gjenskape dem manuelt.

## Migrasjonsprosess

### Viktig merknad om bot-synlighet i V3

I V3 vil **alle v2-boter med offentlig deling aktivert være søkbare i Bot Store.** Hvis du har boter som inneholder sensitiv informasjon som du ikke ønsker skal være synlige, bør du vurdere å gjøre dem private før du migrerer til V3.

### Trinn 1: Identifiser miljønavnet ditt

I denne prosedyren brukes `{YOUR_ENV_PREFIX}` for å identifisere navnet på dine CloudFormation Stacks. Hvis du bruker funksjonen [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), erstatt det med navnet på miljøet som skal migreres. Hvis ikke, erstatt det med en tom streng.

### Trinn 2: Oppdater Repository URL (Anbefalt)

Repository har blitt omdøpt fra `bedrock-claude-chat` til `bedrock-chat`. Oppdater ditt lokale repository:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Trinn 3: Sørg for at du har den nyeste V2-versjonen

> [!WARNING]
> Du MÅ oppdatere til v2.10.0 før migrering til V3. **Å hoppe over dette trinnet kan føre til tap av data under migreringen.**

Før du starter migreringen, sørg for at du kjører den nyeste versjonen av V2 (**v2.10.0**). Dette sikrer at du har alle nødvendige feilrettinger og forbedringer før oppgradering til V3:

```bash
# Fetch the latest tags
git fetch --tags

# Checkout the latest V2 version
git checkout v2.10.0

# Deploy the latest V2 version
cd cdk
npm ci
npx cdk deploy --all
```

### Trinn 4: Noter ned V2 DynamoDB-tabellnavnet ditt

Hent V2 ConversationTable-navnet fra CloudFormation-outputs:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Sørg for å lagre dette tabellnavnet på et sikkert sted, da du vil trenge det for migreringsscriptet senere.

### Trinn 5: Ta backup av DynamoDB-tabellen din

Før du fortsetter, opprett en backup av DynamoDB ConversationTable ved å bruke navnet du nettopp noterte:

```bash
# Create a backup of your V2 table
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Check the backup status is available
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Trinn 6: Slett alle publiserte API-er

> [!IMPORTANT]
> Før du distribuerer V3, må du slette alle publiserte API-er for å unngå konflikter med Cloudformation output-verdier under oppgraderingsprosessen.

1. Logg inn i applikasjonen din som administrator
2. Naviger til Admin-seksjonen og velg "API Management"
3. Gjennomgå listen over alle publiserte API-er
4. Slett hver publiserte API ved å klikke på sletteknappen ved siden av den

Du kan finne mer informasjon om API-publisering og administrasjon i henholdsvis [PUBLISH_API.md](../PUBLISH_API_nb-NO.md), [ADMINISTRATOR.md](../ADMINISTRATOR_nb-NO.md) dokumentasjonen.

### Trinn 7: Hent V3 og distribuer

Hent den nyeste V3-koden og distribuer:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Når du distribuerer V3, vil applikasjonen være utilgjengelig for alle brukere til migrasjonsprosessen er fullført. Det nye skjemaet er ikke kompatibelt med det gamle dataformatet, så brukere vil ikke kunne få tilgang til botene eller samtalene sine før du fullfører migreringsscriptet i de neste trinnene.

### Trinn 8: Noter ned V3 DynamoDB-tabellnavnene dine

Etter distribusjon av V3 må du hente både det nye ConversationTable- og BotTable-navnet:

```bash
# Get the V3 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Get the V3 BotTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Sørg for å lagre disse V3-tabellnavnene sammen med ditt tidligere lagrede V2-tabellnavn, da du vil trenge alle disse for migreringsscriptet.

### Trinn 9: Kjør migreringsscriptet

Migreringsscriptet vil konvertere V2-dataene dine til V3-skjemaet. Først, rediger migreringsscriptet `docs/migration/migrate_v2_v3.py` for å sette tabellnavnene og regionen din:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Kjør deretter scriptet ved hjelp av Poetry fra backend-katalogen:

> [!NOTE]
> Python-kravversjonen ble endret til 3.13.0 eller senere (Kan bli endret i fremtidig utvikling. Se pyproject.toml). Hvis du har venv installert med en annen Python-versjon, må du fjerne den én gang.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies if you haven't already
poetry install

# Run a dry run first to see what would be migrated
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# If everything looks good, run the actual migration
poetry run python ../docs/migration/migrate_v2_v3.py

# Verify the migration was successful
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Migreringsscriptet vil generere en rapportfil i din nåværende katalog med detaljer om migrasjonsprosessen. Sjekk denne filen for å sikre at alle dataene dine ble migrert korrekt.

#### Håndtering av store datamengder

For miljøer med mange brukere eller store datamengder, vurder disse tilnærmingene:

1. **Migrer brukere individuelt**: For brukere med store datamengder, migrer dem én om gangen:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Minnehensyn**: Migrasjonsprosessen laster data inn i minnet. Hvis du støter på Out-Of-Memory (OOM)-feil, prøv:

   - Å migrere én bruker om gangen
   - Å kjøre migreringen på en maskin med mer minne
   - Å dele opp migreringen i mindre grupper av brukere

3. **Overvåk migreringen**: Sjekk de genererte rapportfilene for å sikre at alle data migreres korrekt, spesielt for store datasett.

### Trinn 10: Verifiser applikasjonen

Etter migrering, åpne applikasjonen din og verifiser:

- Alle botene dine er tilgjengelige
- Samtaler er bevart
- Nye tilgangskontroller fungerer

### Opprydding (Valgfritt)

Etter å ha bekreftet at migreringen var vellykket og alle dataene dine er riktig tilgjengelige i V3, kan du valgfritt slette V2-samtaletabellen for å spare kostnader:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Slett bare V2-tabellen etter grundig verifisering av at alle viktige data har blitt vellykket migrert til V3. Vi anbefaler å beholde backupen som ble opprettet i Trinn 2 i minst noen uker etter migreringen, selv om du sletter den originale tabellen.

## V3 FAQ

### Bot-tilgang og tillatelser

**Q: Hva skjer hvis en bot jeg bruker blir slettet eller tilgangstillatelsen min fjernes?**
A: Autorisasjon sjekkes ved chattid, så du vil miste tilgangen umiddelbart.

**Q: Hva skjer hvis en bruker slettes (f.eks. når en ansatt slutter)?**
A: Dataene deres kan fjernes fullstendig ved å slette alle elementer fra DynamoDB med deres bruker-ID som partisjonsnøkkel (PK).

**Q: Kan jeg slå av deling for en essensiell offentlig bot?**
A: Nei, administrator må først merke boten som ikke-essensiell før deling kan slås av.

**Q: Kan jeg slette en essensiell offentlig bot?**
A: Nei, administrator må først merke boten som ikke-essensiell før den kan slettes.

### Sikkerhet og implementering

**Q: Er rad-nivå sikkerhet (RLS) implementert for bot-tabellen?**
A: Nei, med tanke på mangfoldet av tilgangsmønstre. Autorisasjon utføres ved tilgang til boter, og risikoen for metadata-lekkasje anses som minimal sammenlignet med samtalehistorikk.

**Q: Hva er kravene for å publisere et API?**
A: Boten må være offentlig.

**Q: Vil det være en administrasjonsskjerm for alle private boter?**
A: Ikke i den første V3-utgivelsen. Elementer kan fortsatt slettes ved å spørre med bruker-ID etter behov.

**Q: Vil det være bot-tagging-funksjonalitet for bedre søkeopplevelse?**
A: Ikke i den første V3-utgivelsen, men LLM-basert automatisk tagging kan bli lagt til i fremtidige oppdateringer.

### Administrasjon

**Q: Hva kan administratorer gjøre?**
A: Administratorer kan:

- Administrere offentlige boter (inkludert sjekking av høykostnads-boter)
- Administrere API-er
- Merke offentlige boter som essensielle

**Q: Kan jeg gjøre delvis delte boter essensielle?**
A: Nei, støtter kun offentlige boter.

**Q: Kan jeg sette prioritet for festede boter?**
A: Ikke ved første utgivelse.

### Autorisasjonskonfigurasjon

**Q: Hvordan setter jeg opp autorisasjon?**
A:

1. Åpne Amazon Cognito-konsollen og opprett brukergrupper i BrChat-brukerpolen
2. Legg til brukere i disse gruppene etter behov
3. I BrChat, velg brukergruppene du vil gi tilgang til når du konfigurerer bot-delingsinnstillinger

Merk: Endringer i gruppemedlemskap krever ny innlogging for å tre i kraft. Endringer reflekteres ved token-fornyelse, men ikke under ID-tokenets gyldighetsperiode (standard 30 minutter i V3, konfigurerbar via `tokenValidMinutes` i `cdk.json` eller `parameter.ts`).

**Q: Sjekker systemet med Cognito hver gang en bot aksesseres?**
A: Nei, autorisasjon sjekkes ved hjelp av JWT-tokenet for å unngå unødvendige I/O-operasjoner.

### Søkefunksjonalitet

**Q: Støtter bot-søk semantisk søk?**
A: Nei, kun delvis tekstmatching støttes. Semantisk søk (f.eks. "automobil" → "bil", "EV", "kjøretøy") er ikke tilgjengelig på grunn av nåværende OpenSearch Serverless-begrensninger (mars 2025).