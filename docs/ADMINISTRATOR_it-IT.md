# Funzionalità di amministrazione

Le funzionalità di amministrazione sono uno strumento essenziale poiché forniscono approfondimenti cruciali sull'utilizzo dei bot personalizzati e sul comportamento degli utenti. Senza questa funzionalità, sarebbe difficile per gli amministratori comprendere quali bot personalizzati sono più diffusi, perché lo sono, e chi li sta utilizzando. Queste informazioni sono fondamentali per ottimizzare i prompt di istruzione, personalizzare le fonti di dati RAG e identificare gli utenti più attivi che potrebbero diventare influencer.

## Loop di feedback

L'output di un LLM potrebbe non soddisfare sempre le aspettative dell'utente. A volte non riesce a soddisfare le sue esigenze. Per "integrare" efficacemente gli LLM nelle operazioni aziendali e nella vita quotidiana, implementare un loop di feedback è essenziale. Bedrock Claude Chat è dotato di una funzione di feedback progettata per consentire agli utenti di analizzare le ragioni dell'insoddisfazione. Sulla base dei risultati dell'analisi, gli utenti possono regolare di conseguenza i prompt, le fonti di dati RAG e i parametri.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Gli analisti di dati possono accedere ai log delle conversazioni utilizzando [Amazon Athena](https://aws.amazon.com/jp/athena/). Se desiderano analizzare i dati con [Jupyter Notebook](https://jupyter.org/), [questo esempio di notebook](../examples/notebooks/feedback_analysis_example.ipynb) può essere un riferimento.

## Dashboard dell'Amministratore

Attualmente fornisce una panoramica di base sull'utilizzo del chatbot e degli utenti, concentrandosi sull'aggregazione dei dati per ciascun bot e utente in periodi di tempo specifici e ordinando i risultati in base alle spese di utilizzo.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Le analitiche sull'utilizzo degli utenti saranno presto disponibili.

### Prerequisiti

L'utente amministratore deve essere un membro del gruppo chiamato `Admin`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o aws cli. Si noti che l'ID del pool utenti può essere recuperato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Note

- Come indicato nell'[architettura](../README.md#architecture), le funzionalità di amministrazione faranno riferimento al bucket S3 esportato da DynamoDB. Si tenga presente che poiché l'esportazione viene eseguita ogni ora, le conversazioni più recenti potrebbero non essere immediatamente riflesse.

- Negli utilizzi dei bot pubblici, i bot che non sono stati utilizzati affatto durante il periodo specificato non verranno elencati.

- Negli utilizzi degli utenti, gli utenti che non hanno utilizzato il sistema durante il periodo specificato non verranno elencati.

## Scarica dati conversazione

Puoi eseguire query sui registri delle conversazioni tramite Athena, utilizzando SQL. Per scaricare i log, apri l'Editor Query di Athena dalla console di gestione ed esegui SQL. Di seguito sono riportate alcune query di esempio utili per analizzare i casi d'uso. Il feedback può essere trovato nell'attributo `MessageMap`.

### Query per ID Bot

Modifica `bot-id` e `datehour`. `bot-id` può essere trovato nella schermata di Gestione Bot, accessibile tramite Bot Publish APIs, mostrato nella barra laterale sinistra. Nota l'ultima parte dell'URL come `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

### Query per ID Utente

Modifica `user-id` e `datehour`. `user-id` può essere trovato nella schermata di Gestione Bot.

> [!Note]
> Analisi dell'utilizzo degli utenti in arrivo presto.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```