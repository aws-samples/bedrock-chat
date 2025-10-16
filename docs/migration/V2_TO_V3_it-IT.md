# Guida alla Migrazione (da v2 a v3)

## TL;DR

- V3 introduce il controllo dettagliato dei permessi e la funzionalità del Bot Store, richiedendo modifiche allo schema DynamoDB
- **Esegui il backup della tua DynamoDB ConversationTable prima della migrazione**
- Aggiorna l'URL del repository da `bedrock-claude-chat` a `bedrock-chat`
- Esegui lo script di migrazione per convertire i tuoi dati al nuovo schema
- Tutti i tuoi bot e le conversazioni saranno preservati con il nuovo modello di permessi
- **IMPORTANTE: Durante il processo di migrazione, l'applicazione non sarà disponibile per nessun utente fino al completamento della migrazione. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni del tuo ambiente di sviluppo.**
- **IMPORTANTE: Tutte le API Pubblicate devono essere eliminate durante il processo di migrazione.**
- **ATTENZIONE: Il processo di migrazione non può garantire il successo al 100% per tutti i bot. Si prega di documentare le configurazioni importanti dei bot prima della migrazione nel caso sia necessario ricrearle manualmente**

## Introduzione

### Novità in V3

V3 introduce miglioramenti significativi a Bedrock Chat:

1. **Controllo granulare dei permessi**: Controlla l'accesso ai tuoi bot con permessi basati su gruppi di utenti
2. **Bot Store**: Condividi e scopri bot attraverso un marketplace centralizzato
3. **Funzionalità amministrative**: Gestisci le API, contrassegna i bot come essenziali e analizza l'utilizzo dei bot

Queste nuove funzionalità hanno richiesto modifiche allo schema DynamoDB, rendendo necessario un processo di migrazione per gli utenti esistenti.

### Perché Questa Migrazione È Necessaria

Il nuovo modello di permessi e le funzionalità del Bot Store hanno richiesto una ristrutturazione del modo in cui i dati dei bot vengono archiviati e accessibili. Il processo di migrazione converte i tuoi bot e conversazioni esistenti nel nuovo schema mantenendo tutti i tuoi dati.

> [!WARNING]
> Avviso di Interruzione del Servizio: **Durante il processo di migrazione, l'applicazione non sarà disponibile per tutti gli utenti.** Pianifica di eseguire questa migrazione durante una finestra di manutenzione quando gli utenti non necessitano di accedere al sistema. L'applicazione tornerà disponibile solo dopo che lo script di migrazione sarà stato completato con successo e tutti i dati saranno stati correttamente convertiti nel nuovo schema. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni del tuo ambiente di sviluppo.

> [!IMPORTANT]
> Prima di procedere con la migrazione: **Il processo di migrazione non può garantire il 100% di successo per tutti i bot**, specialmente quelli creati con versioni precedenti o con configurazioni personalizzate. Si prega di documentare le configurazioni importanti dei bot (istruzioni, fonti di conoscenza, impostazioni) prima di iniziare il processo di migrazione nel caso sia necessario ricrearle manualmente.

## Processo di Migrazione

### Avviso Importante sulla Visibilità dei Bot in V3

In V3, **tutti i bot v2 con condivisione pubblica abilitata saranno ricercabili nel Bot Store.** Se hai bot contenenti informazioni sensibili che non vuoi rendere individuabili, considera di renderli privati prima di migrare a V3.

### Fase 1: Identificare il nome dell'ambiente

In questa procedura, `{YOUR_ENV_PREFIX}` viene specificato per identificare il nome dei tuoi Stack CloudFormation. Se stai utilizzando la funzionalità [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), sostituiscilo con il nome dell'ambiente da migrare. In caso contrario, sostituiscilo con una stringa vuota.

### Fase 2: Aggiornare l'URL del Repository (Raccomandato)

Il repository è stato rinominato da `bedrock-claude-chat` a `bedrock-chat`. Aggiorna il tuo repository locale:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Fase 3: Assicurarsi di Essere sull'Ultima Versione V2

> [!WARNING]
> DEVI aggiornare alla versione v2.10.0 prima di migrare a V3. **Saltare questo passaggio potrebbe causare perdita di dati durante la migrazione.**

Prima di iniziare la migrazione, assicurati di utilizzare l'ultima versione di V2 (**v2.10.0**). Questo garantisce di avere tutte le correzioni di bug e i miglioramenti necessari prima di passare a V3:

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

### Fase 4: Registrare il Nome della Tabella DynamoDB V2

Ottieni il nome della ConversationTable V2 dagli output di CloudFormation:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Assicurati di salvare questo nome della tabella in un luogo sicuro, poiché ti servirà per lo script di migrazione più tardi.

### Fase 5: Backup della Tabella DynamoDB

Prima di procedere, crea un backup della tua ConversationTable DynamoDB utilizzando il nome appena registrato:

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

### Fase 6: Eliminare Tutte le API Pubblicate

> [!IMPORTANT]
> Prima di distribuire V3, devi eliminare tutte le API pubblicate per evitare conflitti nei valori di output di CloudFormation durante il processo di aggiornamento.

1. Accedi alla tua applicazione come amministratore
2. Vai alla sezione Admin e seleziona "API Management"
3. Esamina l'elenco di tutte le API pubblicate
4. Elimina ogni API pubblicata cliccando sul pulsante di eliminazione accanto ad essa

Puoi trovare maggiori informazioni sulla pubblicazione e gestione delle API nella documentazione [PUBLISH_API.md](../PUBLISH_API_it-IT.md), [ADMINISTRATOR.md](../ADMINISTRATOR_it-IT.md).

### Fase 7: Pull di V3 e Deploy

Scarica l'ultimo codice V3 e distribuiscilo:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Una volta distribuito V3, l'applicazione non sarà disponibile per tutti gli utenti fino al completamento del processo di migrazione. Il nuovo schema è incompatibile con il vecchio formato dei dati, quindi gli utenti non potranno accedere ai loro bot o conversazioni fino al completamento dello script di migrazione nei passaggi successivi.

### Fase 8: Registrare i Nomi delle Tabelle DynamoDB V3

Dopo aver distribuito V3, devi ottenere sia il nome della nuova ConversationTable che della BotTable:

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
> Assicurati di salvare questi nomi delle tabelle V3 insieme al nome della tabella V2 precedentemente salvato, poiché ti serviranno tutti per lo script di migrazione.

### Fase 9: Eseguire lo Script di Migrazione

Lo script di migrazione convertirà i tuoi dati V2 nello schema V3. Prima, modifica lo script di migrazione `docs/migration/migrate_v2_v3.py` per impostare i nomi delle tue tabelle e la regione:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Quindi esegui lo script utilizzando Poetry dalla directory backend:

> [!NOTE]
> La versione dei requisiti Python è stata modificata a 3.13.0 o successiva (Potrebbe cambiare in sviluppi futuri. Vedi pyproject.toml). Se hai installato venv con una versione Python diversa, dovrai rimuoverlo una volta.

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

Lo script di migrazione genererà un file di report nella tua directory corrente con i dettagli sul processo di migrazione. Controlla questo file per assicurarti che tutti i tuoi dati siano stati migrati correttamente.

#### Gestione di Grandi Volumi di Dati

Per ambienti con utenti intensivi o grandi quantità di dati, considera questi approcci:

1. **Migrare gli utenti individualmente**: Per utenti con grandi volumi di dati, migra uno alla volta:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Considerazioni sulla memoria**: Il processo di migrazione carica i dati in memoria. Se incontri errori di Out-Of-Memory (OOM), prova:

   - Migrare un utente alla volta
   - Eseguire la migrazione su una macchina con più memoria
   - Suddividere la migrazione in lotti più piccoli di utenti

3. **Monitorare la migrazione**: Controlla i file di report generati per assicurarti che tutti i dati siano migrati correttamente, specialmente per dataset di grandi dimensioni.

### Fase 10: Verificare l'Applicazione

Dopo la migrazione, apri la tua applicazione e verifica:

- Tutti i tuoi bot sono disponibili
- Le conversazioni sono preservate
- I nuovi controlli dei permessi funzionano

### Pulizia (Opzionale)

Dopo aver confermato che la migrazione è stata completata con successo e tutti i tuoi dati sono correttamente accessibili in V3, puoi opzionalmente eliminare la tabella delle conversazioni V2 per risparmiare sui costi:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Elimina la tabella V2 solo dopo aver verificato accuratamente che tutti i tuoi dati importanti sono stati migrati con successo a V3. Raccomandiamo di conservare il backup creato nella Fase 2 per almeno alcune settimane dopo la migrazione, anche se elimini la tabella originale.

## FAQ V3

### Accesso e Permessi dei Bot

**Q: Cosa succede se un bot che sto utilizzando viene eliminato o il mio permesso di accesso viene rimosso?**
A: L'autorizzazione viene verificata al momento della chat, quindi perderai l'accesso immediatamente.

**Q: Cosa succede se un utente viene eliminato (es. un dipendente lascia l'azienda)?**
A: I suoi dati possono essere completamente rimossi eliminando tutti gli elementi da DynamoDB con il suo ID utente come chiave di partizione (PK).

**Q: Posso disattivare la condivisione per un bot pubblico essenziale?**
A: No, l'amministratore deve prima contrassegnare il bot come non essenziale prima di poter disattivare la condivisione.

**Q: Posso eliminare un bot pubblico essenziale?**
A: No, l'amministratore deve prima contrassegnare il bot come non essenziale prima di poterlo eliminare.

### Sicurezza e Implementazione

**Q: È implementata la sicurezza a livello di riga (RLS) per la tabella dei bot?**
A: No, considerando la diversità dei modelli di accesso. L'autorizzazione viene eseguita durante l'accesso ai bot, e il rischio di perdita di metadati è considerato minimo rispetto alla cronologia delle conversazioni.

**Q: Quali sono i requisiti per pubblicare un'API?**
A: Il bot deve essere pubblico.

**Q: Ci sarà una schermata di gestione per tutti i bot privati?**
A: Non nella release iniziale V3. Tuttavia, gli elementi possono ancora essere eliminati interrogando l'ID utente secondo necessità.

**Q: Ci sarà una funzionalità di tagging dei bot per una migliore esperienza di ricerca?**
A: Non nella release iniziale V3, ma il tagging automatico basato su LLM potrebbe essere aggiunto in futuri aggiornamenti.

### Amministrazione

**Q: Cosa possono fare gli amministratori?**
A: Gli amministratori possono:

- Gestire i bot pubblici (incluso il controllo dei bot ad alto costo)
- Gestire le API
- Contrassegnare i bot pubblici come essenziali

**Q: Posso rendere essenziali i bot parzialmente condivisi?**
A: No, è supportato solo per i bot pubblici.

**Q: Posso impostare una priorità per i bot fissati?**
A: Non nella release iniziale.

### Configurazione dell'Autorizzazione

**Q: Come configuro l'autorizzazione?**
A:

1. Aprire la console Amazon Cognito e creare gruppi di utenti nel pool utenti BrChat
2. Aggiungere gli utenti a questi gruppi secondo necessità
3. In BrChat, selezionare i gruppi di utenti a cui si vuole consentire l'accesso durante la configurazione delle impostazioni di condivisione del bot

Nota: Le modifiche all'appartenenza ai gruppi richiedono un nuovo accesso per avere effetto. Le modifiche si riflettono al rinnovo del token, ma non durante il periodo di validità del token ID (predefinito 30 minuti in V3, configurabile tramite `tokenValidMinutes` in `cdk.json` o `parameter.ts`).

**Q: Il sistema verifica con Cognito ogni volta che si accede a un bot?**
A: No, l'autorizzazione viene verificata utilizzando il token JWT per evitare operazioni I/O non necessarie.

### Funzionalità di Ricerca

**Q: La ricerca dei bot supporta la ricerca semantica?**
A: No, è supportata solo la corrispondenza parziale del testo. La ricerca semantica (es. "automobile" → "auto", "VE", "veicolo") non è disponibile a causa degli attuali vincoli di OpenSearch Serverless (marzo 2025).