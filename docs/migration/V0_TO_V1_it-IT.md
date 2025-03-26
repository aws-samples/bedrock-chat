# Guida alla Migrazione (da v0 a v1)

Se stai già utilizzando Bedrock Claude Chat con una versione precedente (~`0.4.x`), devi seguire i passaggi qui sotto per eseguire la migrazione.

## Perché devo farlo?

Questo aggiornamento principale include importanti aggiornamenti sulla sicurezza.

- Lo storage del database vettoriale (ovvero, pgvector su Aurora PostgreSQL) è ora crittografato, il che innesca una sostituzione durante la distribuzione. Questo significa che gli elementi vettoriali esistenti verranno eliminati.
- Abbiamo introdotto il gruppo di utenti Cognito `CreatingBotAllowed` per limitare gli utenti che possono creare bot. Gli utenti esistenti attuali non sono in questo gruppo, quindi dovrai allegare manualmente l'autorizzazione se desideri che abbiano la capacità di creare bot. Vedi: [Personalizzazione Bot](../../README.md#bot-personalization)

## Prerequisiti

Leggere la [Guida alla Migrazione del Database](./DATABASE_MIGRATION_it-IT.md) e determinare il metodo per ripristinare gli elementi.

## Passaggi

### Migrazione dell'archivio vettoriale

- Apri il terminale e naviga nella directory del progetto
- Estrai il branch che desideri distribuire. Passa al branch desiderato (in questo caso, `v1`) ed estrai gli ultimi cambiamenti:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Se desideri ripristinare gli elementi con DMS, NON DIMENTICARE di disabilitare la rotazione della password e annotare la password per accedere al database. Se ripristini con lo script di migrazione([migrate.py](./migrate.py)), non è necessario annotare la password.
- Rimuovi tutte le [API pubblicate](../PUBLISH_API_it-IT.md) in modo che CloudFormation possa rimuovere il cluster Aurora esistente.
- Esegui [npx cdk deploy](../README.md#deploy-using-cdk) che attiva la sostituzione del cluster Aurora e CANCELLA TUTTI GLI ELEMENTI VETTORIALI.
- Segui la [Guida alla Migrazione del Database](./DATABASE_MIGRATION_it-IT.md) per ripristinare gli elementi vettoriali.
- Verifica che l'utente possa utilizzare i bot esistenti che hanno conoscenza, ovvero i bot RAG.

### Allegare l'autorizzazione CreatingBotAllowed

- Dopo la distribuzione, tutti gli utenti non saranno in grado di creare nuovi bot.
- Se vuoi che utenti specifici possano creare bot, aggiungi tali utenti al gruppo `CreatingBotAllowed` utilizzando la console di gestione o la CLI.
- Verifica se l'utente può creare un bot. Nota che gli utenti devono effettuare nuovamente l'accesso.