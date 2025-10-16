# Funzionalità amministrative

## Prerequisiti

L'utente amministratore deve essere membro di un gruppo chiamato `Admin`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o tramite aws cli. Si noti che l'id del pool di utenti può essere consultato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Contrassegnare i bot pubblici come Essenziali

I bot pubblici possono ora essere contrassegnati come "Essenziali" dagli amministratori. I bot marcati come Essenziali saranno mostrati nella sezione "Essenziali" del bot store, rendendoli facilmente accessibili agli utenti. Questo permette agli amministratori di mettere in evidenza i bot importanti che vogliono che tutti gli utenti utilizzino.

### Esempi

- Bot Assistente HR: Aiuta i dipendenti con domande e compiti relativi alle risorse umane.
- Bot Supporto IT: Fornisce assistenza per problemi tecnici interni e gestione degli account.
- Bot Guida alle Policy Interne: Risponde alle domande frequenti su regole di presenza, politiche di sicurezza e altri regolamenti interni.
- Bot Onboarding Nuovi Dipendenti: Guida i nuovi assunti attraverso procedure e utilizzo dei sistemi durante il loro primo giorno.
- Bot Informazioni sui Benefit: Spiega i programmi di benefit aziendali e i servizi di welfare.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Loop di feedback

L'output dell'LLM potrebbe non sempre soddisfare le aspettative dell'utente. A volte non riesce a soddisfare le esigenze dell'utente. Per "integrare" efficacemente gli LLM nelle operazioni aziendali e nella vita quotidiana, è essenziale implementare un loop di feedback. Bedrock Chat è dotato di una funzionalità di feedback progettata per consentire agli utenti di analizzare il motivo dell'insoddisfazione. In base ai risultati dell'analisi, gli utenti possono regolare di conseguenza i prompt, le fonti di dati RAG e i parametri.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Gli analisti dei dati possono accedere ai log delle conversazioni utilizzando [Amazon Athena](https://aws.amazon.com/jp/athena/). Se desiderano analizzare i dati tramite [Jupyter Notebook](https://jupyter.org/), [questo esempio di notebook](../examples/notebooks/feedback_analysis_example.ipynb) può essere un riferimento.

## Dashboard

Attualmente fornisce una panoramica di base sull'utilizzo dei chatbot e degli utenti, concentrandosi sull'aggregazione dei dati per ciascun bot e utente in periodi di tempo specifici e ordinando i risultati in base ai costi di utilizzo.

![](./imgs/admin_bot_analytics.png)

## Note

- Come indicato nell'[architettura](../README.md#architecture), le funzionalità di amministrazione faranno riferimento al bucket S3 esportato da DynamoDB. Si prega di notare che poiché l'esportazione viene eseguita una volta ogni ora, le conversazioni più recenti potrebbero non essere riflesse immediatamente.

- Negli utilizzi dei bot pubblici, i bot che non sono stati utilizzati affatto durante il periodo specificato non verranno elencati.

- Negli utilizzi degli utenti, gli utenti che non hanno utilizzato affatto il sistema durante il periodo specificato non verranno elencati.

> [!Important]
> Se si utilizzano più ambienti (dev, prod, ecc.), il nome del database Athena includerà il prefisso dell'ambiente. Invece di `bedrockchatstack_usage_analysis`, il nome del database sarà:
>
> - Per l'ambiente predefinito: `bedrockchatstack_usage_analysis`
> - Per gli ambienti con nome: `<env-prefix>_bedrockchatstack_usage_analysis` (es. `dev_bedrockchatstack_usage_analysis`)
>
> Inoltre, il nome della tabella includerà il prefisso dell'ambiente:
>
> - Per l'ambiente predefinito: `ddb_export`
> - Per gli ambienti con nome: `<env-prefix>_ddb_export` (es. `dev_ddb_export`)
>
> Assicurati di modificare le tue query di conseguenza quando lavori con più ambienti.

## Scaricare i dati delle conversazioni

È possibile interrogare i log delle conversazioni tramite Athena, utilizzando SQL. Per scaricare i log, aprire Athena Query Editor dalla console di gestione ed eseguire SQL. Di seguito alcuni esempi di query utili per analizzare i casi d'uso. Il feedback può essere consultato nell'attributo `MessageMap`.

### Query per ID Bot

Modificare `bot-id` e `datehour`. Il `bot-id` può essere consultato nella schermata di gestione del Bot, accessibile dalle API Bot Publish, mostrate nella barra laterale sinistra. Notare la parte finale dell'URL del tipo `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

> [!Note]
> Se si utilizza un ambiente con nome (es. "dev"), sostituire `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` nella query sopra.

### Query per ID Utente

Modificare `user-id` e `datehour`. Il `user-id` può essere consultato nella schermata di gestione del Bot.

> [!Note]
> Le analitiche sull'utilizzo degli utenti saranno disponibili a breve.

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

> [!Note]
> Se si utilizza un ambiente con nome (es. "dev"), sostituire `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` nella query sopra.