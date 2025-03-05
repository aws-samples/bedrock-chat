# Configurare un provider di identità esterno per Google

## Passaggio 1: Creare un Client OAuth 2.0 di Google

1. Vai nella Console per Sviluppatori di Google.
2. Crea un nuovo progetto o seleziona un progetto esistente.
3. Naviga su "Credenziali", poi fai clic su "Crea credenziali" e scegli "ID client OAuth".
4. Configura la schermata di consenso se richiesto.
5. Per il tipo di applicazione, seleziona "Applicazione web".
6. Lascia l'URI di reindirizzamento vuoto al momento per impostarlo successivamente, e salva temporaneamente.[Vedi Passaggio 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una volta creato, annota l'ID Client e il Segreto Client.

Per i dettagli, visita [Documento ufficiale di Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Passaggio 2: Archiviare le Credenziali Google OAuth in AWS Secrets Manager

1. Accedi alla Console di Gestione AWS.
2. Vai su Secrets Manager e scegli "Archivia un nuovo segreto".
3. Seleziona "Altro tipo di segreti".
4. Inserisci il clientId e clientSecret di Google OAuth come coppie chiave-valore.

   1. Chiave: clientId, Valore: <YOUR_GOOGLE_CLIENT_ID>
   2. Chiave: clientSecret, Valore: <YOUR_GOOGLE_CLIENT_SECRET>

5. Segui le istruzioni per denominare e descrivere il segreto. Prendi nota del nome del segreto poiché ti servirà nel codice CDK. Ad esempio, googleOAuthCredentials. (Utilizzare nel nome della variabile del Passaggio 3 <YOUR_SECRET_NAME>)
6. Rivedi e archivia il segreto.

### Attenzione

I nomi delle chiavi devono corrispondere esattamente alle stringhe 'clientId' e 'clientSecret'.

## Passaggio 3: Aggiornare cdk.json

Nel file cdk.json, aggiungi il Provider di Identità e il Nome del Segreto al file cdk.json.

in questo modo:

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

Il userPoolDomainPrefix deve essere globalmente univoco tra tutti gli utenti Amazon Cognito. Se scegli un prefisso già utilizzato da un altro account AWS, la creazione del dominio del pool di utenti non riuscirà. È una buona prassi includere identificatori, nomi di progetto o nomi di ambienti nel prefisso per garantire l'univocità.

## Passaggio 4: Distribuisci il Tuo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Passaggio 5: Aggiornare il Client Google OAuth con gli URI di Reindirizzamento di Cognito

Dopo aver distribuito lo stack, AuthApprovedRedirectURI sarà visibile negli output di CloudFormation. Torna nella Console per Sviluppatori di Google e aggiorna il client OAuth con gli URI di reindirizzamento corretti.