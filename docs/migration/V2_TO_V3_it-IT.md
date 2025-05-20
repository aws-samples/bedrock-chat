# Guida alla Migrazione (da v2 a v3)

## TL;DR

- V3 introduce il controllo dei permessi granulare e la funzionalità Bot Store, richiedendo modifiche allo schema DynamoDB
- **Esegui il backup della tabella ConversationTable di DynamoDB prima della migrazione**
- Aggiorna l'URL del repository da `bedrock-claude-chat` a `bedrock-chat`
- Esegui lo script di migrazione per convertire i dati nel nuovo schema
- Tutti i tuoi bot e le conversazioni verranno preservati con il nuovo modello di autorizzazione
- **IMPORTANTE: Durante il processo di migrazione, l'applicazione sarà indisponibile per tutti gli utenti fino al completamento della migrazione. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni dell'ambiente di sviluppo.**
- **IMPORTANTE: Tutti gli API Pubblicati devono essere eliminati durante il processo di migrazione.**
- **ATTENZIONE: Il processo di migrazione non può garantire il 100% di successo per tutti i bot. Si consiglia di documentare le configurazioni dei bot importanti prima della migrazione nel caso in cui sia necessario ricrearle manualmente**

## Introduzione

### Novità nella V3

V3 introduce miglioramenti significativi per Bedrock Chat:

1. **Controllo granulare delle autorizzazioni**: Controlla l'accesso ai tuoi bot con autorizzazioni basate su gruppi di utenti
2. **Bot Store**: Condividi e scopri bot attraverso un marketplace centralizzato
3. **Funzionalità amministrative**: Gestisci API, contrassegna bot come essenziali e analizza l'utilizzo dei bot

Queste nuove funzionalità hanno richiesto modifiche allo schema DynamoDB, rendendo necessario un processo di migrazione per gli utenti esistenti.

### Perché Questa Migrazione È Necessaria

Il nuovo modello di autorizzazioni e la funzionalità del Bot Store hanno richiesto la ristrutturazione di come i dati dei bot vengono archiviati e accessibili. Il processo di migrazione converte i tuoi bot e conversazioni esistenti nel nuovo schema preservando tutti i tuoi dati.

> [!WARNING]
> Avviso di Interruzione del Servizio: **Durante il processo di migrazione, l'applicazione sarà inaccessibile a tutti gli utenti.** Pianifica di eseguire questa migrazione durante una finestra di manutenzione quando gli utenti non necessitano di accedere al sistema. L'applicazione tornerà disponibile solo dopo che lo script di migrazione avrà completato con successo e tutti i dati saranno stati correttamente convertiti nel nuovo schema. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni del proprio ambiente di sviluppo.

> [!IMPORTANT]
> Prima di procedere con la migrazione: **Il processo di migrazione non può garantire un successo del 100% per tutti i bot**, specialmente quelli creati con versioni precedenti o con configurazioni personalizzate. Si prega di documentare le configurazioni dei bot importanti (istruzioni, fonti di conoscenza, impostazioni) prima di avviare il processo di migrazione nel caso in cui sia necessario ricrearli manualmente.

## Processo di Migrazione

### Avviso Importante sulla Visibilità dei Bot nella V3

Nella V3, **tutti i bot v2 con condivisione pubblica abilitata saranno ricercabili nel Bot Store.** Se hai bot contenenti informazioni sensibili che non vuoi siano individuabili, considera di renderli privati prima di migrare a V3.

### Passaggio 1: Identificare il nome del proprio ambiente

In questa procedura, `{YOUR_ENV_PREFIX}` è specificato per identificare il nome dei tuoi Stack CloudFormation. Se stai utilizzando la funzione [Distribuzione di Più Ambienti](../../README.md#deploying-multiple-environments), sostituiscilo con il nome dell'ambiente da migrare. In caso contrario, sostituiscilo con una stringa vuota.

### Passaggio 2: Aggiornare l'URL del Repository (Consigliato)

Il repository è stato rinominato da `bedrock-claude-chat` a `bedrock-chat`. Aggiorna il tuo repository locale:

```bash
# Verifica l'URL remoto corrente
git remote -v

# Aggiorna l'URL remoto
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verifica la modifica
git remote -v
```

### Passaggio 3: Assicurarsi di Essere sull'Ultima Versione V2

> [!ATTENZIONE]
> È NECESSARIO aggiornare a v2.10.0 prima di migrare a V3. **Saltare questo passaggio potrebbe causare perdita di dati durante la migrazione.**

Prima di iniziare la migrazione, assicurati di utilizzare l'ultima versione di V2 (**v2.10.0**). Questo garantisce che tu abbia tutte le correzioni di bug e i miglioramenti necessari prima di eseguire l'aggiornamento a V3:

```bash
# Recupera gli ultimi tag
git fetch --tags

# Passa all'ultima versione V2
git checkout v2.10.0

# Distribuisci l'ultima versione V2
cd cdk
npm ci
npx cdk deploy --all
```

### Passaggio 4: Registrare il Nome della Tabella DynamoDB V2

Ottieni il nome della ConversationTable V2 dagli output di CloudFormation:

```bash
# Ottieni il nome della ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Assicurati di salvare questo nome di tabella in un luogo sicuro, poiché ti servirà per lo script di migrazione successivamente.

### Passaggio 5: Eseguire il Backup della Tabella DynamoDB

Prima di procedere, crea un backup della tua ConversationTable DynamoDB utilizzando il nome appena registrato:

```bash
# Crea un backup della tua tabella V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Verifica che lo stato del backup sia disponibile
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Passaggio 6: Eliminare Tutte le API Pubblicate

> [!IMPORTANTE]
> Prima di distribuire V3, è necessario eliminare tutte le API pubblicate per evitare conflitti nei valori di output di Cloudformation durante il processo di aggiornamento.

1. Accedi all'applicazione come amministratore
2. Vai nella sezione Admin e seleziona "Gestione API"
3. Esamina l'elenco di tutte le API pubblicate
4. Elimina ogni API pubblicata facendo clic sul pulsante di eliminazione accanto a essa

Puoi trovare ulteriori informazioni sulla pubblicazione e la gestione delle API nella documentazione [PUBLISH_API.md](../PUBLISH_API_it-IT.md), [ADMINISTRATOR.md](../ADMINISTRATOR_it-IT.md) rispettivamente.

### Passaggio 7: Scaricare V3 e Distribuire

Scarica l'ultimo codice V3 e distribuiscilo:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANTE]
> Una volta distribuita V3, l'applicazione sarà inaccessibile a tutti gli utenti fino al completamento del processo di migrazione. Il nuovo schema non è compatibile con il formato dati precedente, quindi gli utenti non potranno accedere ai loro bot o conversazioni fino a quando non completerai lo script di migrazione nei passaggi successivi.

### Passaggio 8: Registrare i Nomi delle Tabelle DynamoDB V3

Dopo aver distribuito V3, devi ottenere sia il nome della nuova ConversationTable che della BotTable:

```bash
# Ottieni il nome della ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Ottieni il nome della BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Importante]
> Assicurati di salvare questi nomi di tabelle V3 insieme al nome della tabella V2 precedentemente salvato, poiché ti serviranno tutti per lo script di migrazione.

### Passaggio 9: Eseguire lo Script di Migrazione

Lo script di migrazione convertirà i tuoi dati V2 nello schema V3. Per prima cosa, modifica lo script di migrazione `docs/migration/migrate_v2_v3.py` per impostare i nomi delle tabelle e la regione:

```python
# Regione in cui si trova dynamodb
REGION = "ap-northeast-1" # Sostituisci con la tua regione

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Sostituisci con il valore registrato nel Passaggio 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Sostituisci con il valore registrato nel Passaggio 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Sostituisci con il valore registrato nel Passaggio 8
```

Quindi esegui lo script utilizzando Poetry dalla directory backend:

> [!NOTA]
> La versione dei requisiti Python è stata modificata in 3.13.0 o successiva (Possibilmente modificata nello sviluppo futuro. Vedi pyproject.toml). Se hai installato venv con una versione Python diversa, dovrai rimuoverlo una volta.

```bash
# Vai alla directory backend
cd backend

# Installa le dipendenze se non lo hai già fatto
poetry install

# Esegui prima un test a secco per vedere cosa verrebbe migrato
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Se tutto sembra a posto, esegui la migrazione effettiva
poetry run python ../docs/migration/migrate_v2_v3.py

# Verifica che la migrazione sia avvenuta con successo
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Lo script di migrazione genererà un file di report nella directory corrente con i dettagli del processo di migrazione. Controlla questo file per assicurarti che tutti i tuoi dati siano stati migrati correttamente.

#### Gestione di Grandi Volumi di Dati

Per ambienti con utenti intensivi o grandi quantità di dati, considera questi approcci:

1. **Migrare gli utenti singolarmente**: Per utenti con grandi volumi di dati, migra loro uno alla volta:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Considerazioni sulla memoria**: Il processo di migrazione carica i dati in memoria. Se riscontri errori Out-Of-Memory (OOM), prova:

   - Migrare un utente alla volta
   - Eseguire la migrazione su una macchina con più memoria
   - Suddividere la migrazione in batch più piccoli di utenti

3. **Monitorare la migrazione**: Controlla i file di report generati per assicurarti che tutti i dati siano migrati correttamente, specialmente per set di dati di grandi dimensioni.

### Passaggio 10: Verificare l'Applicazione

Dopo la migrazione, apri la tua applicazione e verifica:

- Tutti i tuoi bot siano disponibili
- Le conversazioni siano preservate
- I nuovi controlli di autorizzazione funzionino

### Pulizia (Facoltativo)

Dopo aver confermato che la migrazione è avvenuta con successo e che tutti i tuoi dati sono correttamente accessibili in V3, puoi facoltativamente eliminare la tabella delle conversazioni V2 per risparmiare sui costi:

```bash
# Elimina la tabella delle conversazioni V2 (SOLO dopo aver confermato la migrazione riuscita)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANTE]
> Elimina la tabella V2 solo dopo aver verificato accuratamente che tutti i tuoi dati importanti siano stati migrati con successo in V3. Consigliamo di mantenere il backup creato nel Passaggio 2 per almeno alcune settimane dopo la migrazione, anche se elimini la tabella originale.

## V3 FAQ

### Accesso e Autorizzazioni Bot

**D: Cosa succede se un bot che sto utilizzando viene eliminato o mi viene rimosso il permesso di accesso?**
R: L'autorizzazione viene verificata al momento della chat, quindi perderai l'accesso immediatamente.

**D: Cosa succede se un utente viene eliminato (ad esempio, un dipendente lascia l'azienda)?**
R: I suoi dati possono essere completamente rimossi eliminando tutti gli elementi da DynamoDB con il suo ID utente come chiave di partizione (PK).

**D: Posso disattivare la condivisione per un bot pubblico essenziale?**
R: No, l'amministratore deve prima contrassegnare il bot come non essenziale prima di disattivare la condivisione.

**D: Posso eliminare un bot pubblico essenziale?**
R: No, l'amministratore deve prima contrassegnare il bot come non essenziale prima di eliminarlo.

### Sicurezza e Implementazione

**D: È implementata la sicurezza a livello di riga (RLS) per la tabella dei bot?**
R: No, considerando la diversità dei modelli di accesso. L'autorizzazione viene eseguita durante l'accesso ai bot e il rischio di perdita di metadati è considerato minimo rispetto alla cronologia delle conversazioni.

**D: Quali sono i requisiti per pubblicare un'API?**
R: Il bot deve essere pubblico.

**D: Ci sarà una schermata di gestione per tutti i bot privati?**
R: Non nella versione iniziale di V3. Tuttavia, gli elementi possono comunque essere eliminati eseguendo query con l'ID utente secondo necessità.

**D: Ci sarà una funzionalità di tag per i bot per migliorare l'esperienza di ricerca?**
R: Non nella versione iniziale di V3, ma potrebbe essere aggiunto il tagging automatico basato su LLM in aggiornamenti futuri.

### Amministrazione

**D: Cosa possono fare gli amministratori?**
R: Gli amministratori possono:

- Gestire bot pubblici (incluso il controllo dei bot ad alto costo)
- Gestire API
- Contrassegnare bot pubblici come essenziali

**D: Posso rendere essenziali i bot parzialmente condivisi?**
R: No, sono supportati solo i bot pubblici.

**D: Posso impostare la priorità per i bot fissati?**
R: Nella versione iniziale, no.

### Configurazione Autorizzazioni

**D: Come imposto l'autorizzazione?**
R:

1. Aprire la console di Amazon Cognito e creare gruppi utenti nel pool utenti BrChat
2. Aggiungere gli utenti a questi gruppi secondo necessità
3. In BrChat, selezionare i gruppi utenti che si desidera autorizzare durante la configurazione delle impostazioni di condivisione bot

Nota: Le modifiche all'appartenenza al gruppo richiedono un nuovo accesso per avere effetto. Le modifiche vengono riflesse all'aggiornamento del token, ma non durante il periodo di validità del token ID (per impostazione predefinita 30 minuti in V3, configurabile tramite `tokenValidMinutes` in `cdk.json` o `parameter.ts`).

**D: Il sistema verifica con Cognito ogni volta che si accede a un bot?**
R: No, l'autorizzazione viene verificata utilizzando il token JWT per evitare operazioni di I/O non necessarie.

### Funzionalità di Ricerca

**D: La ricerca dei bot supporta la ricerca semantica?**
R: No, è supportata solo la corrispondenza parziale del testo. La ricerca semantica (ad es. "automobile" → "auto", "EV", "veicolo") non è disponibile a causa degli attuali vincoli di OpenSearch Serverless (Mar 2025).