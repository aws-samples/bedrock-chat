# Configurare un provider di identità esterno per Google

## Passaggio 1: Creare un Client OAuth 2.0 di Google

1. Vai nella Console per Sviluppatori di Google.
2. Crea un nuovo progetto o seleziona un progetto esistente.
3. Vai su "Credenziali", poi fai clic su "Crea credenziali" e scegli "ID client OAuth".
4. Configura la schermata di consenso se richiesto.
5. Per il tipo di applicazione, seleziona "Applicazione web".
6. Lascia l'URI di reindirizzamento vuoto per ora per impostarlo successivamente. [Vedi Passaggio 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una volta creato, annota l'ID client e il Segreto client.

Per i dettagli, visita [documento ufficiale di Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Passaggio 2: Archiviare le Credenziali Google OAuth in AWS Secrets Manager

1. Accedere alla Console di Gestione AWS.
2. Navigare in Secrets Manager e scegliere "Archivia un nuovo segreto".
3. Selezionare "Altro tipo di segreti".
4. Inserire il clientId e il clientSecret di Google OAuth come coppie chiave-valore.

   1. Chiave: clientId, Valore: <YOUR_GOOGLE_CLIENT_ID>
   2. Chiave: clientSecret, Valore: <YOUR_GOOGLE_CLIENT_SECRET>

5. Seguire le istruzioni per denominare e descrivere il segreto. Annotare il nome del segreto poiché sarà necessario nel codice CDK. Ad esempio, googleOAuthCredentials. (Utilizzare nel nome della variabile del Passaggio 3 <YOUR_SECRET_NAME>)
6. Rivedere e archiviare il segreto.

### Attenzione

I nomi delle chiavi devono corrispondere esattamente alle stringhe 'clientId' e 'clientSecret'.

## Passaggio 3: Aggiornare cdk.json

Nel file cdk.json, aggiungi il Provider di Identità e il Nome del Segreto al file cdk.json.

come segue:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<TUO_NOME_SEGRETO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFISSO_DOMINIO_UNIVOCO_PER_IL_TUO_USER_POOL>"
  }
}
```

### Attenzione

#### Univocità

Il userPoolDomainPrefix deve essere globalmente univoco tra tutti gli utenti Amazon Cognito. Se scegli un prefisso già utilizzato da un altro account AWS, la creazione del dominio del pool di utenti non riuscirà. È una buona pratica includere identificatori, nomi di progetto o nomi di ambienti nel prefisso per garantire l'univocità.

## Passaggio 4: Distribuisci il tuo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Passaggio 5: Aggiornare il Client OAuth di Google con gli URI di Reindirizzamento di Cognito

Dopo aver distribuito lo stack, AuthApprovedRedirectURI sarà visibile negli output di CloudFormation. Torna nella Console degli Sviluppatori Google e aggiorna il client OAuth con gli URI di reindirizzamento corretti.