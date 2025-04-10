# Funzionalità amministrative

## Prerequisiti

L'utente admin deve essere un membro del gruppo chiamato `Admin`, che può essere configurato tramite la console di gestione > Amazon Cognito User pools o aws cli. Nota che l'ID del user pool può essere recuperato accedendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Contrassegnare i bot pubblici come Essenziali

I bot pubblici possono ora essere contrassegnati come "Essenziali" dagli amministratori. I bot contrassegnati come Essenziali verranno presentati nella sezione "Essenziali" dello store dei bot, rendendoli facilmente accessibili agli utenti. Questo consente agli amministratori di evidenziare i bot importanti che vogliono che tutti gli utenti utilizzino.

### Esempi

- Bot Assistente HR: Aiuta i dipendenti con domande e attività relative alle risorse umane.
- Bot Supporto IT: Fornisce assistenza per problemi tecnici interni e gestione degli account.
- Bot Guida Politiche Interne: Risponde a domande frequenti su regole di presenza, politiche di sicurezza e altri regolamenti interni.
- Bot Onboarding Nuovi Dipendenti: Guida i nuovi assunti attraverso procedure e utilizzo dei sistemi nel loro primo giorno.
- Bot Informazioni sui Benefit: Spiega i programmi di benefit aziendali e i servizi di welfare.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Loop di feedback

L'output di un LLM potrebbe non soddisfare sempre le aspettative dell'utente. A volte non riesce a soddisfare le sue esigenze. Per "integrare" efficacemente gli LLM nelle operazioni aziendali e nella vita quotidiana, implementare un loop di feedback è essenziale. Bedrock Chat è dotato di una funzionalità di feedback progettata per consentire agli utenti di analizzare le ragioni dell'insoddisfazione. Sulla base dei risultati dell'analisi, gli utenti possono regolare i prompt, le fonti di dati RAG e i parametri di conseguenza.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Gli analisti di dati possono accedere ai log delle conversazioni tramite [Amazon Athena](https://aws.amazon.com/jp/athena/). Se desiderano analizzare i dati con [Jupyter Notebook](https://jupyter.org/), [questo esempio di notebook](../examples/notebooks/feedback_analysis_example.ipynb) può essere un riferimento.

## Dashboard

Attualmente fornisce una panoramica di base dell'utilizzo del chatbot e degli utenti, concentrandosi sull'aggregazione dei dati per ciascun bot e utente in periodi di tempo specifici e ordinando i risultati in base alle spese di utilizzo.

![](./imgs/admin_bot_analytics.png)

## Note

- Come indicato nell'[architettura](../README.md#architecture), le funzionalità di amministrazione faranno riferimento al bucket S3 esportato da DynamoDB. Si noti che poiché l'esportazione viene eseguita ogni ora, le conversazioni più recenti potrebbero non essere riflesse immediatamente.

- Negli utilizzi dei bot pubblici, i bot che non sono stati utilizzati affatto durante il periodo specificato non verranno elencati.

- Negli utilizzi degli utenti, gli utenti che non hanno utilizzato il sistema durante il periodo specificato non verranno elencati.

> [!Importante]
> Se si utilizzano più ambienti (dev, prod, ecc.), il nome del database Athena includerà il prefisso dell'ambiente. Invece di `bedrockchatstack_usage_analysis`, il nome del database sarà:
>
> - Per l'ambiente predefinito: `bedrockchatstack_usage_analysis`
> - Per gli ambienti denominati: `<prefisso-ambiente>_bedrockchatstack_usage_analysis` (ad esempio, `dev_bedrockchatstack_usage_analysis`)
>
> Inoltre, il nome della tabella includerà il prefisso dell'ambiente:
>
> - Per l'ambiente predefinito: `ddb_export`
> - Per gli ambienti denominati: `<prefisso-ambiente>_ddb_export` (ad esempio, `dev_ddb_export`)
>
> Assicurati di adattare le tue query di conseguenza quando lavori con più ambienti.

## Scarica dati conversazione

Puoi interrogare i registri delle conversazioni tramite Athena, utilizzando SQL. Per scaricare i log, apri l'Editor di Query Athena dalla console di gestione ed esegui SQL. Di seguito sono riportati alcuni esempi di query utili per analizzare i casi d'uso. Il feedback può essere consultato nell'attributo `MessageMap`.

### Query per Bot ID

Modifica `bot-id` e `datehour`. `bot-id` può essere trovato nella schermata di Gestione Bot, accessibile tramite le API di Pubblicazione Bot, mostrato nella barra laterale sinistra. Nota l'ultima parte dell'URL come `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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
> Se si utilizza un ambiente denominato (ad esempio "dev"), sostituire `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` nella query precedente.

### Query per User ID

Modifica `user-id` e `datehour`. `user-id` può essere trovato nella schermata di Gestione Bot.

> [!Note]
> Le analisi di utilizzo degli utenti sono in arrivo.

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
> Se si utilizza un ambiente denominato (ad esempio "dev"), sostituire `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` nella query precedente.