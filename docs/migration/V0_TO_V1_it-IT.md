# Guida alla Migrazione (da v0 a v1)

Se stai già utilizzando Bedrock Chat con una versione precedente (~`0.4.x`), dovrai seguire i passaggi riportati di seguito per eseguire la migrazione.

## Perché devo farlo?

Questo importante aggiornamento include importanti aggiornamenti per la sicurezza.

- L'archiviazione del database vettoriale (ovvero, pgvector su Aurora PostgreSQL) è ora crittografata, il che attiva una sostituzione durante la distribuzione. Questo significa che gli elementi vettoriali esistenti verranno eliminati.
- Abbiamo introdotto il gruppo di utenti Cognito `CreatingBotAllowed` per limitare gli utenti che possono creare bot. Gli utenti esistenti attuali non sono in questo gruppo, quindi dovrai allegare manualmente l'autorizzazione se vuoi che abbiano la capacità di creare bot. Vedi: [Personalizzazione Bot](../../README.md#bot-personalization)

## Prerequisiti

Leggere la [Guida alla Migrazione del Database](./DATABASE_MIGRATION_it-IT.md) e determinare il metodo per il ripristino degli elementi.

## Passaggi

### Migrazione dell'archivio vettoriale

- Apri il terminale e naviga nella directory del progetto
- Estrai il branch che desideri distribuire. Di seguito è riportato il passaggio al branch desiderato (in questo caso, `v1`) e il pull degli ultimi cambiamenti:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Se desideri ripristinare gli elementi con DMS, NON DIMENTICARE di disabilitare la rotazione della password e annotare la password per accedere al database. Se si ripristina con lo script di migrazione([migrate_v0_v1.py](./migrate_v0_v1.py)), non è necessario annotare la password.
- Rimuovi tutte le [API pubblicate](../PUBLISH_API_it-IT.md) in modo che CloudFormation possa rimuovere il cluster Aurora esistente.
- Esegui [npx cdk deploy](../README.md#deploy-using-cdk) che attiva la sostituzione del cluster Aurora e CANCELLA TUTTI GLI ELEMENTI VETTORIALI.
- Segui la [Guida alla Migrazione del Database](./DATABASE_MIGRATION_it-IT.md) per ripristinare gli elementi vettoriali.
- Verifica che l'utente possa utilizzare i bot esistenti con conoscenza, ovvero i bot RAG.

### Associare l'autorizzazione CreatingBotAllowed

- Dopo la distribuzione, tutti gli utenti non saranno in grado di creare nuovi bot.
- Se si desidera che utenti specifici possano creare bot, aggiungi tali utenti al gruppo `CreatingBotAllowed` utilizzando la console di gestione o la CLI.
- Verifica se l'utente può creare un bot. Nota che gli utenti devono effettuare nuovamente l'accesso.