# Guida alla Migrazione (da v1 a v2)

## TL;DR

- **Per gli utenti della versione 1.2 o precedenti**: Aggiornare alla versione 1.4 e ricreare i bot utilizzando Knowledge Base (KB). Dopo un periodo di transizione, una volta confermato il corretto funzionamento con KB, procedere con l'aggiornamento alla versione 2.
- **Per gli utenti della versione 1.3**: Anche se si sta già utilizzando KB, è **fortemente consigliato** aggiornarsi alla versione 1.4 e ricreare i bot. Se si sta ancora utilizzando pgvector, migrare ricreando i bot tramite KB nella versione 1.4.
- **Per gli utenti che intendono continuare a utilizzare pgvector**: L'aggiornamento alla versione 2 non è consigliato se si prevede di continuare a utilizzare pgvector. L'aggiornamento alla versione 2 eliminerà tutte le risorse correlate a pgvector e il supporto futuro non sarà più disponibile. In questo caso, continuare a utilizzare la versione 1.
- Si noti che **l'aggiornamento alla versione 2 comporterà l'eliminazione di tutte le risorse correlate ad Aurora.** Gli aggiornamenti futuri si concentreranno esclusivamente sulla versione 2, con la versione 1 che verrà progressivamente dismessa.

## Introduzione

### Cosa accadrà

L'aggiornamento v2 introduce un cambiamento importante sostituendo pgvector su Aurora Serverless ed embedding basati su ECS con [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Questo cambiamento non è retrocompatibile.

### Perché questo repository ha adottato Knowledge Bases e interrotto l'uso di pgvector

Ci sono diverse ragioni per questo cambiamento:

#### Miglioramento dell'accuratezza RAG

- Knowledge Bases utilizza OpenSearch Serverless come backend, consentendo ricerche ibride con ricerca full-text e vettoriale. Questo porta a una migliore accuratezza nel rispondere a domande che includono nomi propri, un aspetto in cui pgvector era carente.
- Offre inoltre più opzioni per migliorare l'accuratezza RAG, come frammentazione e analisi avanzate.
- Knowledge Bases è generalmente disponibile da quasi un anno a ottobre 2024, con funzionalità come la navigazione web già aggiunte. Sono previsti ulteriori aggiornamenti, rendendo più semplice adottare funzionalità avanzate a lungo termine. Ad esempio, mentre questo repository non ha implementato funzioni come l'importazione da bucket S3 esistenti (una funzionalità molto richiesta) in pgvector, è già supportata in KB (Knowledge Bases).

#### Manutenzione

- L'attuale configurazione ECS + Aurora dipende da numerose librerie, incluse quelle per l'analisi PDF, la navigazione web e l'estrazione di trascrizioni YouTube. In confronto, soluzioni gestite come Knowledge Bases riducono l'onere di manutenzione sia per gli utenti che per il team di sviluppo del repository.

## Processo di Migrazione (Riepilogo)

Raccomandiamo fortemente di eseguire l'upgrade alla versione 1.4 prima di passare alla versione 2. Nella versione 1.4, è possibile utilizzare sia pgvector che bot di Knowledge Base, consentendo un periodo di transizione per ricreare i bot pgvector esistenti in Knowledge Base e verificare che funzionino come previsto. Anche se i documenti RAG rimangono identici, si noti che le modifiche backend a OpenSearch potrebbero produrre risultati leggermente diversi, sebbene generalmente simili, a causa di differenze come gli algoritmi k-NN.

Impostando `useBedrockKnowledgeBasesForRag` su true in `cdk.json`, è possibile creare bot utilizzando Knowledge Bases. Tuttavia, i bot pgvector diventeranno di sola lettura, impedendo la creazione o la modifica di nuovi bot pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Nella versione 1.4, vengono introdotti anche [Guardrails per Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). A causa delle restrizioni regionali di Knowledge Bases, il bucket S3 per il caricamento dei documenti deve essere nella stessa regione di `bedrockRegion`. Raccomandiamo di eseguire il backup dei bucket dei documenti esistenti prima dell'aggiornamento, per evitare di dover caricare manualmente un gran numero di documenti in seguito (poiché è disponibile la funzionalità di importazione del bucket S3).

## Processo di Migrazione (Dettaglio)

I passaggi variano a seconda che si stia utilizzando v1.2 o precedente, oppure v1.3.

![](../imgs/v1_to_v2_arch.png)

### Passaggi per gli utenti di v1.2 o precedente

1. **Eseguire il backup del bucket dei documenti esistente (facoltativo ma consigliato).** Se il sistema è già in funzione, si consiglia vivamente questo passaggio. Eseguire il backup del bucket denominato `bedrockchatstack-documentbucketxxxx-yyyy`. Ad esempio, è possibile utilizzare [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Aggiornare a v1.4**: Recuperare il tag v1.4 più recente, modificare `cdk.json` e distribuire. Seguire questi passaggi:

   1. Recuperare l'ultimo tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modificare `cdk.json` come segue:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Distribuire le modifiche:
      ```bash
      npx cdk deploy
      ```

3. **Ricreare i bot**: Ricreare i bot su Knowledge Base con le stesse definizioni (documenti, dimensione dei chunk, ecc.) dei bot pgvector. Se si dispone di un gran numero di documenti, il ripristino dal backup nel passaggio 1 renderà questo processo più semplice. Per ripristinare, è possibile utilizzare il ripristino di copie tra regioni. Per maggiori dettagli, visitare [qui](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Per specificare il bucket ripristinato, impostare la sezione `S3 Data Source` come segue. La struttura del percorso è `s3://<nome-bucket>/<id-utente>/<id-bot>/documents/`. È possibile verificare l'ID utente nel pool utenti Cognito e l'ID bot nella barra degli indirizzi nella schermata di creazione del bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Nota che alcune funzionalità non sono disponibili su Knowledge Bases, come la ricerca web e il supporto per le trascrizioni YouTube (in programma il supporto per il web crawler ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Tenere inoltre presente che l'utilizzo di Knowledge Bases comporterà addebiti sia per Aurora che per Knowledge Bases durante la transizione.

4. **Rimuovere le API pubblicate**: Tutte le API precedentemente pubblicate dovranno essere ripubblicate prima di distribuire v2 a causa dell'eliminazione del VPC. A tale scopo, sarà necessario eliminare prima le API esistenti. L'utilizzo della [funzione di gestione API dell'amministratore](../ADMINISTRATOR_it-IT.md) può semplificare questo processo. Una volta completata l'eliminazione di tutti gli stack CloudFormation `APIPublishmentStackXXXX`, l'ambiente sarà pronto.

5. **Distribuire v2**: Dopo il rilascio di v2, recuperare il sorgente con tag e distribuire come segue (questo sarà possibile una volta rilasciato):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Avvertenza]
> Dopo aver distribuito v2, **TUTTI I BOT CON IL PREFISSO [Non supportato, Solo lettura] SARANNO NASCOSTI.** Assicurarsi di ricreare i bot necessari prima dell'aggiornamento per evitare perdite di accesso.

> [!Suggerimento]
> Durante gli aggiornamenti dello stack, è possibile incontrare messaggi ripetuti come: "Il gestore delle risorse ha restituito il messaggio: La subnet 'subnet-xxx' ha dipendenze e non può essere eliminata." In questi casi, accedere alla Console di gestione > EC2 > Interfacce di rete e cercare BedrockChatStack. Eliminare le interfacce associate a questo nome per facilitare un processo di distribuzione più fluido.

### Passaggi per gli utenti di v1.3

Come menzionato in precedenza, in v1.4, le Knowledge Bases devono essere create nella bedrockRegion a causa di restrizioni regionali. Pertanto, sarà necessario ricreare la KB. Se si è già testata la KB in v1.3, ricreare il bot in v1.4 con le stesse definizioni. Seguire i passaggi descritti per gli utenti di v1.2.