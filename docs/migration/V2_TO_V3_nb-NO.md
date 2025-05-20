# Migreringsguide (v2 til v3)

Would you like me to continue translating the rest of the document? I'm ready to proceed with the next section while carefully following the critical requirements you specified.

## TL;DR

- V3 introduserer finkornet tilgangskontroll og Bot Store-funksjonalitet, som krever endringer i DynamoDB-skjemaet
- **Sikkerhetskopier DynamoDB ConversationTable før migrasjon**
- Oppdater repositoryens URL fra `bedrock-claude-chat` til `bedrock-chat`
- Kjør migrasjonsskriptet for å konvertere dataene til det nye skjemaet
- Alle dine bots og samtaler vil bli bevart med den nye tilgangsmodellen
- **VIKTIG: Under migrasjonsprosessen vil applikasjonen være utilgjengelig for alle brukere inntil migrasjonen er fullført. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen til utviklingsmiljøet.**
- **VIKTIG: Alle publiserte APIer må slettes under migrasjonsprosessen.**
- **ADVARSEL: Migrasjonsprosessen kan ikke garantere 100% suksess for alle bots. Dokumenter viktige bot-konfigurasjoner før migrasjon i tilfelle du må rekonstruere dem manuelt**

## Introduksjon

### Hva Er Nytt i V3

V3 introduserer betydelige forbedringer til Bedrock Chat:

1. **Detaljert tillatelseskontroll**: Kontroller tilgang til dine bots med brukergruppe-baserte tillatelser
2. **Bot-butikk**: Del og oppdag bots gjennom et sentralisert marked
3. **Administrative funksjoner**: Administrer APIer, marker bots som essensielle, og analyser bot-bruk

Disse nye funksjonene krevde endringer i DynamoDB-skjemaet, noe som nødvendiggjør en migrasjonsprosess for eksisterende brukere.

### Hvorfor Denne Migrasjonen Er Nødvendig

Den nye tillatelsesmodellen og Bot Store-funksjonaliteten krevde omstrukturering av hvordan bot-data lagres og aksesseres. Migrasjonsprosessen konverterer dine eksisterende bots og samtaler til det nye skjemaet samtidig som all din data bevares.

> [!ADVARSEL]
> Varsel om Tjenesteavbrudd: **Under migrasjonsprosessen vil applikasjonen være utilgjengelig for alle brukere.** Planlegg å utføre denne migrasjonen under et vedlikeholdsvindu når brukere ikke trenger tilgang til systemet. Applikasjonen vil kun bli tilgjengelig igjen etter at migrasjonsskriptet har fullført vellykket og all data er korrekt konvertert til det nye skjemaet. Denne prosessen tar vanligvis rundt 60 minutter, avhengig av datamengden og ytelsen til ditt utviklingsmiljø.

> [!VIKTIG]
> Før du fortsetter med migrasjonen: **Migrasjonsprosessen kan ikke garantere 100% suksess for alle bots**, spesielt de som er opprettet med eldre versjoner eller med tilpassede konfigurasjoner. Vennligst dokumenter dine viktige bot-konfigurasjoner (instruksjoner, kunnskapskilder, innstillinger) før du starter migrasjonsprosessen i tilfelle du må gjenskape dem manuelt.

## Migrasjonsprosess

### Viktig melding om botsynlighet i V3

I V3 vil **alle v2-boter med offentlig deling være søkbare i Bot Store.** Hvis du har boter som inneholder sensitiv informasjon som du ikke vil at skal kunne oppdages, bør du gjøre dem private før du migrerer til V3.

### Trinn 1: Identifiser miljønavnet ditt

I denne prosedyren er `{YOUR_ENV_PREFIX}` angitt for å identifisere navnet på dine CloudFormation Stacks. Hvis du bruker [Deploying Multiple Environments](../../README.md#deploying-multiple-environments)-funksjonen, erstatter du den med navnet på miljøet som skal migreres. Hvis ikke, erstatter du den med en tom streng.

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

### Trinn 3: Sikre at du er på siste V2-versjon

> [!ADVARSEL]
> Du MÅ oppdatere til v2.10.0 før du migrerer til V3. **Å hoppe over dette trinnet kan føre til datatap under migreringen.**

Før du starter migreringen, pass på at du kjører den siste versjonen av V2 (**v2.10.0**). Dette sikrer at du har alle nødvendige feilrettinger og forbedringer før oppgradering til V3:

```bash
# Hent de siste tagene
git fetch --tags

# Bytt til siste V2-versjon
git checkout v2.10.0

# Distribuer siste V2-versjon
cd cdk
npm ci
npx cdk deploy --all
```

### Trinn 4: Registrer V2 DynamoDB-tabellnavn

Hent V2 ConversationTable-navnet fra CloudFormation-output:

```bash
# Hent V2 ConversationTable-navnet
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Sørg for å lagre dette tabellnavnet på et sikkert sted, da du vil trenge det for migreringsscriptet senere.

### Trinn 5: Sikkerhetskopier DynamoDB-tabellen

Før du fortsetter, opprett en sikkerhetskopi av DynamoDB ConversationTable ved hjelp av navnet du nettopp registrerte:

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
> Før du distribuerer V3, må du slette alle publiserte APIer for å unngå konflikter med Cloudformation-outputverdier under oppgraderingsprosessen.

1. Logg inn i applikasjonen som administrator
2. Naviger til Admin-seksjonen og velg "API-administrasjon"
3. Gjennomgå listen over alle publiserte APIer
4. Slett hver publiserte API ved å klikke på sletteknappen ved siden av den

Du kan finne mer informasjon om API-publisering og -administrasjon i [PUBLISH_API.md](../PUBLISH_API_nb-NO.md), [ADMINISTRATOR.md](../ADMINISTRATOR_nb-NO.md) dokumentasjonen.

### Trinn 7: Hent V3 og distribuer

Hent den siste V3-koden og distribuer:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!VIKTIG]
> Når du distribuerer V3, vil applikasjonen være utilgjengelig for alle brukere til migrasjonsprosessen er fullført. Den nye skjemaet er inkompatibel med det gamle dataformatet, så brukerne vil ikke kunne få tilgang til botene eller samtalene sine før du fullfører migreringsscriptet i de neste trinnene.

### Trinn 8: Registrer V3 DynamoDB-tabellnavn

Etter at du har distribuert V3, må du hente både de nye ConversationTable- og BotTable-navnene:

```bash
# Hent V3 ConversationTable-navnet
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Hent V3 BotTable-navnet
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Viktig]
> Sørg for å lagre disse V3-tabellnavnene sammen med ditt tidligere lagrede V2-tabellnavn, da du vil trenge alle dem for migreringsscriptet.

### Trinn 9: Kjør migreringsscriptet

Migreringsscriptet vil konvertere dine V2-data til V3-skjemaet. Rediger først migreringsscriptet `docs/migration/migrate_v2_v3.py` for å angi dine tabellnavn og region:

```python
# Region hvor dynamodb er plassert
REGION = "ap-northeast-1" # Erstatt med din region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Erstatt med din verdi registrert i Trinn 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Erstatt med din verdi registrert i Trinn 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Erstatt med din verdi registrert i Trinn 8
```

Kjør så scriptet ved hjelp av Poetry fra backend-katalogen:

> [!MERK]
> Python-kravene ble endret til 3.13.0 eller nyere (Muligens endret i fremtidig utvikling. Se pyproject.toml). Hvis du har venv installert med en annen Python-versjon, må du fjerne den én gang.

```bash
# Naviger til backend-katalogen
cd backend

# Installer avhengigheter hvis du ikke allerede har gjort det
poetry install

# Kjør en tørrkjøring først for å se hva som vil bli migrert
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Hvis alt ser bra ut, kjør den faktiske migreringen
poetry run python ../docs/migration/migrate_v2_v3.py

# Bekreft at migreringen var vellykket
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Migreringsscriptet vil generere en rapportfil i din gjeldende katalog med detaljer om migrasjonsprosessen. Sjekk denne filen for å sikre at alle dine data ble migrert korrekt.

#### Håndtering av store datamengder

For miljøer med mange brukere eller store datamengder, vurder disse tilnærmingene:

1. **Migrer brukere individuelt**: For brukere med store datamengder, migrer dem én om gangen:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users bruker-id-1 bruker-id-2
   ```

2. **Minnehensyn**: Migrasjonsprosessen laster data i minnet. Hvis du støter på Out-Of-Memory (OOM)-feil, prøv:

   - Migrer én bruker om gangen
   - Kjør migreringen på en maskin med mer minne
   - Del opp migreringen i mindre brukerbatcher

3. **Overvåk migreringen**: Sjekk de genererte rapportfilene for å sikre at alle data er migrert korrekt, spesielt for store datasett.

### Trinn 10: Bekreft applikasjonen

Etter migreringen, åpne applikasjonen og bekreft:

- Alle botene dine er tilgjengelige
- Samtaler er bevart
- Nye tillatelseskontroller fungerer

### Opprydding (Valgfritt)

Etter å ha bekreftet at migreringen var vellykket og at alle dine data er riktig tilgjengelig i V3, kan du eventuelt slette V2-samtaletabellen for å spare kostnader:

```bash
# Slett V2-samtaletabellen (KUN etter å ha bekreftet vellykket migrasjon)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!VIKTIG]
> Slett kun V2-tabellen etter grundig å ha verifisert at all viktig data har blitt vellykket migrert til V3. Vi anbefaler å beholde sikkerhetskopien opprettet i Trinn 2 i minst noen uker etter migreringen, selv om du sletter den opprinnelige tabellen.

## V3 Ofte stilte spørsmål

### Botadgang og tillatelser

**Q: Hva skjer hvis en bot jeg bruker blir slettet eller min tilgangsrettighet blir fjernet?**
A: Autorisasjon sjekkes ved chattidspunkt, så du mister tilgang umiddelbart.

**Q: Hva skjer hvis en bruker slettes (f.eks. ansatt slutter)?**
A: Deres data kan fullstendig fjernes ved å slette alle elementer fra DynamoDB med deres bruker-ID som partisjonsnøkkel (PK).

**Q: Kan jeg slå av deling for en vesentlig offentlig bot?**
A: Nei, administrator må først merke boten som ikke-vesentlig før deling kan slås av.

**Q: Kan jeg slette en vesentlig offentlig bot?**
A: Nei, administrator må først merke boten som ikke-vesentlig før sletting.

### Sikkerhet og implementering

**Q: Er rad-nivå sikkerhet (RLS) implementert for bottabell?**
A: Nei, på grunn av mangfoldet av tilgangsmønstre. Autorisasjon utføres ved tilgang til bots, og risikoen for metadatalekkasje anses som minimal sammenlignet med samtalehistorikk.

**Q: Hva er kravene for å publisere et API?**
A: Boten må være offentlig.

**Q: Vil det være en administrasjonsskjerm for alle private bots?**
A: Ikke i den første V3-versjonen. Elementer kan likevel slettes ved å søke med bruker-ID etter behov.

**Q: Vil det være bot-merking for bedre søke-UX?**
A: Ikke i den første V3-versjonen, men LLM-basert automatisk merking kan legges til i fremtidige oppdateringer.

### Administrasjon

**Q: Hva kan administratorer gjøre?**
A: Administratorer kan:

- Administrere offentlige bots (inkludert sjekke høykostbots)
- Administrere API-er
- Merke offentlige bots som vesentlige

**Q: Kan jeg gjøre delvis delte bots som vesentlige?**
A: Nei, kun offentlige bots støttes.

**Q: Kan jeg sette prioritet for festede bots?**
A: Ved første lansering, nei.

### Autorisasjonskonfigurasjon

**Q: Hvordan setter jeg opp autorisasjon?**
A:

1. Åpne Amazon Cognito-konsollen og opprett brukergrupper i BrChat-brukergruppen
2. Legg til brukere i disse gruppene etter behov
3. I BrChat, velg brukergruppene du vil tillate tilgang til når du konfigurerer bot-delingsinnstillinger

Merk: Gruppemedlemskapsendringer krever ny innlogging for å tre i kraft. Endringer gjenspeiles ved token-oppdatering, men ikke i løpet av ID-tokenets gyldighetsperiode (standard 30 minutter i V3, konfigurerbar av `tokenValidMinutes` i `cdk.json` eller `parameter.ts`).

**Q: Sjekker systemet med Cognito hver gang en bot åpnes?**
A: Nei, autorisasjon sjekkes ved bruk av JWT-token for å unngå unødvendige I/O-operasjoner.

### Søkefunksjonalitet

**Q: Støtter bot-søk semantisk søk?**
A: Nei, kun delvis tekstsamsvar støttes. Semantisk søk (f.eks. "automobil" → "bil", "EV", "kjøretøy") er ikke tilgjengelig på grunn av gjeldende OpenSearch Serverless-begrensninger (mars 2025).