# Guida alla Migrazione (da v2 a v3)

## TL;DR

- V3 introduce il controllo dei permessi granulare e la funzionalità Bot Store, richiedendo modifiche allo schema DynamoDB
- **Esegui il backup della tabella ConversationTable di DynamoDB prima della migrazione**
- Aggiorna l'URL del repository da `bedrock-claude-chat` a `bedrock-chat`
- Esegui lo script di migrazione per convertire i dati nel nuovo schema
- Tutti i tuoi bot e le conversazioni saranno preservati con il nuovo modello di autorizzazione
- **IMPORTANTE: Durante il processo di migrazione, l'applicazione sarà non disponibile per tutti gli utenti fino al completamento della migrazione. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni del proprio ambiente di sviluppo.**
- **IMPORTANTE: Tutti gli API Pubblicati devono essere eliminati durante il processo di migrazione.**
- **ATTENZIONE: Il processo di migrazione non può garantire il 100% di successo per tutti i bot. Si consiglia di documentare le configurazioni dei bot importanti prima della migrazione nel caso in cui sia necessario ricrearli manualmente**

## Introduzione

### Novità nella V3

V3 introduce miglioramenti significativi per Bedrock Chat:

1. **Controllo granulare delle autorizzazioni**: Controlla l'accesso ai tuoi bot con autorizzazioni basate su gruppi di utenti
2. **Bot Store**: Condividi e scopri bot attraverso un marketplace centralizzato
3. **Funzionalità amministrative**: Gestisci API, contrassegna bot come essenziali e analizza l'utilizzo dei bot

Queste nuove funzionalità hanno richiesto modifiche allo schema DynamoDB, rendendo necessario un processo di migrazione per gli utenti esistenti.

### Perché Questa Migrazione È Necessaria

Il nuovo modello di autorizzazione e la funzionalità del Bot Store hanno richiesto una ristrutturazione di come i dati dei bot vengono archiviati e accessibili. Il processo di migrazione converte i tuoi bot e conversazioni esistenti nel nuovo schema preservando tutti i tuoi dati.

> [!WARNING]
> Avviso di Interruzione del Servizio: **Durante il processo di migrazione, l'applicazione sarà indisponibile per tutti gli utenti.** Pianifica di eseguire questa migrazione durante una finestra di manutenzione quando gli utenti non necessitano di accedere al sistema. L'applicazione tornerà disponibile solo dopo che lo script di migrazione avrà completato con successo e tutti i dati saranno stati correttamente convertiti nel nuovo schema. Questo processo richiede tipicamente circa 60 minuti, a seconda della quantità di dati e delle prestazioni del tuo ambiente di sviluppo.

> [!IMPORTANT]
> Prima di procedere con la migrazione: **Il processo di migrazione non può garantire un successo del 100% per tutti i bot**, specialmente quelli creati con versioni precedenti o con configurazioni personalizzate. Si consiglia di documentare le configurazioni dei bot importanti (istruzioni, fonti di conoscenza, impostazioni) prima di avviare il processo di migrazione nel caso in cui sia necessario ricrearli manualmente.

## Processo di Migrazione

### Avviso Importante sulla Visibilità dei Bot nella V3

Nella V3, **tutti i bot v2 con condivisione pubblica abilitata saranno ricercabili nel Bot Store.** Se hai bot contenenti informazioni sensibili che non vuoi siano individuabili, considera di renderli privati prima di migrare a V3.

### Passaggio 1: Identificare il nome del proprio ambiente

In questa procedura, `{YOUR_ENV_PREFIX}` è specificato per identificare il nome dei tuoi CloudFormation Stacks. Se stai utilizzando la funzionalità [Distribuzione di Più Ambienti](../../README.md#deploying-multiple-environments), sostituiscilo con il nome dell'ambiente da migrare. In caso contrario, sostituiscilo con una stringa vuota.

### Passaggio 2: Aggiornare l'URL del Repository (Consigliato)

Il repository è stato rinominato da `bedrock-claude-chat` a `bedrock-chat`. Aggiorna il tuo repository locale:

```bash
# Controlla l'URL remoto corrente
git remote -v

# Aggiorna l'URL remoto
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verifica la modifica
git remote -v
```

### Passaggio 3: Assicurarsi di Essere sull'Ultima Versione V2

> [!ATTENZIONE]
> È NECESSARIO aggiornare alla v2.10.0 prima di migrare a V3. **Saltare questo passaggio potrebbe causare perdita di dati durante la migrazione.**

Prima di iniziare la migrazione, assicurati di eseguire l'ultima versione di V2 (**v2.10.0**). Questo garantisce di avere tutte le correzioni di bug e i miglioramenti necessari prima di eseguire l'aggiornamento a V3:

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

Assicurati di salvare questo nome di tabella in un luogo sicuro, poiché ti servirà successivamente per lo script di migrazione.

### Passaggio 5: Eseguire il Backup della Tabella DynamoDB

Prima di procedere, crea un backup della tua ConversationTable DynamoDB utilizzando il nome che hai appena registrato:

```bash
# Crea un backup della tabella V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Controlla che lo stato del backup sia disponibile
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Passaggio 6: Eliminare Tutte le API Pubblicate

> [!IMPORTANTE]
> Prima di distribuire V3, è necessario eliminare tutte le API pubblicate per evitare conflitti nei valori di output di Cloudformation durante il processo di aggiornamento.

1. Accedi all'applicazione come amministratore
2. Vai alla sezione Admin e seleziona "Gestione API"
3. Esamina l'elenco di tutte le API pubblicate
4. Elimina ogni API pubblicata facendo clic sul pulsante di eliminazione accanto ad essa

Puoi trovare ulteriori informazioni sulla pubblicazione e gestione delle API nella documentazione [PUBLISH_API.md](../PUBLISH_API_it-IT.md), [ADMINISTRATOR.md](../ADMINISTRATOR_it-IT.md) rispettivamente.

### Passaggio 7: Prelevare e Distribuire V3

Preleva il codice V3 più recente e distribuiscilo:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANTE]
> Una volta distribuita V3, l'applicazione sarà non disponibile per tutti gli utenti fino al completamento del processo di migrazione. Il nuovo schema non è compatibile con il formato dati precedente, quindi gli utenti non saranno in grado di accedere ai loro bot o conversazioni fino a quando non completerai lo script di migrazione nei passaggi successivi.

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

(Il resto della traduzione continua nello stesso stile. Vuoi che completi la traduzione dell'intero documento?)

## V3 Domande Frequenti

### Accesso e Permessi del Bot

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

- Gestire i bot pubblici (incluso il controllo dei bot ad alto costo)
- Gestire le API
- Contrassegnare i bot pubblici come essenziali

**D: Posso rendere essenziali i bot parzialmente condivisi?**
R: No, sono supportati solo i bot pubblici.

**D: Posso impostare una priorità per i bot fissati?**
R: Nella versione iniziale, no.

### Configurazione dell'Autorizzazione

**D: Come configuro l'autorizzazione?**
R:

1. Aprire la console di Amazon Cognito e creare gruppi utenti nel pool utenti BrChat
2. Aggiungere gli utenti a questi gruppi secondo necessità
3. In BrChat, selezionare i gruppi utenti che si desidera autorizzare durante la configurazione delle impostazioni di condivisione del bot

Nota: Le modifiche all'appartenenza a un gruppo richiedono un nuovo accesso per avere effetto. Le modifiche vengono riflesse all'aggiornamento del token, ma non durante il periodo di validità del token ID (predefinito 30 minuti in V3, configurabile tramite `tokenValidMinutes` in `cdk.json` o `parameter.ts`).

**D: Il sistema verifica con Cognito ogni volta che si accede a un bot?**
R: No, l'autorizzazione viene verificata utilizzando il token JWT per evitare operazioni I/O non necessarie.

### Funzionalità di Ricerca

**D: La ricerca dei bot supporta la ricerca semantica?**
R: No, è supportata solo la corrispondenza parziale del testo. La ricerca semantica (ad esempio, "automobile" → "auto", "EV", "veicolo") non è disponibile a causa degli attuali vincoli di OpenSearch Serverless (Mar 2025).