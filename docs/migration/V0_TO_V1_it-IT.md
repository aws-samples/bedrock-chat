# Guida alla Migrazione (da v0 a v1)

Se stai già utilizzando Bedrock Chat con una versione precedente (~`0.4.x`), devi seguire i passaggi indicati di seguito per effettuare la migrazione.

## Perché devo farlo?

Questo importante aggiornamento include aggiornamenti di sicurezza fondamentali.

- L'archivio del database vettoriale (cioè pgvector su Aurora PostgreSQL) è ora criptato, il che causa una sostituzione durante la distribuzione. Questo significa che gli elementi vettoriali esistenti verranno eliminati.
- Abbiamo introdotto il gruppo utenti Cognito `CreatingBotAllowed` per limitare gli utenti che possono creare bot. Gli utenti esistenti non fanno parte di questo gruppo, quindi è necessario assegnare manualmente i permessi se si desidera che abbiano la capacità di creare bot. Vedi: [Bot Personalization](../../README.md#bot-personalization)

## Prerequisiti

Leggere la [Database Migration Guide](./DATABASE_MIGRATION_it-IT.md) e determinare il metodo per il ripristino degli elementi.

## Passaggi

### Migrazione del vector store

- Apri il terminale e naviga nella directory del progetto
- Effettua il pull del branch che desideri distribuire. Di seguito per il branch desiderato (in questo caso, `v1`) e scarica le ultime modifiche:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Se desideri ripristinare gli elementi con DMS, NON DIMENTICARE di disabilitare la rotazione della password e annotare la password per accedere al database. Se stai ripristinando con lo script di migrazione ([migrate_v0_v1.py](./migrate_v0_v1.py)), non è necessario annotare la password.
- Rimuovi tutte le [API pubblicate](../PUBLISH_API_it-IT.md) in modo che CloudFormation possa rimuovere il cluster Aurora esistente.
- Esegui [npx cdk deploy](../README.md#deploy-using-cdk) che attiva la sostituzione del cluster Aurora e ELIMINA TUTTI GLI ELEMENTI VETTORIALI.
- Segui la [Guida alla Migrazione del Database](./DATABASE_MIGRATION_it-IT.md) per ripristinare gli elementi vettoriali.
- Verifica che gli utenti possano utilizzare i bot esistenti che hanno conoscenze, ad esempio i bot RAG.

### Assegnazione del permesso CreatingBotAllowed

- Dopo la distribuzione, tutti gli utenti non potranno creare nuovi bot.
- Se desideri che specifici utenti possano creare bot, aggiungi questi utenti al gruppo `CreatingBotAllowed` utilizzando la console di gestione o la CLI.
- Verifica se l'utente può creare un bot. Nota che gli utenti devono effettuare nuovamente l'accesso.