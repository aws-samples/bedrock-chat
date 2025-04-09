# Configurare un provider di identità esterno per Google

## Passaggio 1: Creare un Client OAuth 2.0 di Google

1. Accedere alla Console per Sviluppatori di Google.
2. Creare un nuovo progetto o selezionare uno esistente.
3. Navigare su "Credenziali", quindi fare clic su "Crea credenziali" e scegliere "ID client OAuth".
4. Configurare la schermata di consenso se richiesto.
5. Per il tipo di applicazione, selezionare "Applicazione web".
6. Lasciare l'URI di reindirizzamento vuoto per ora per impostarlo successivamente, e salvare temporaneamente.[Vedi Passaggio 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una volta creato, annotare l'ID client e il Segreto client.

Per i dettagli, visitare [Documento ufficiale di Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Passaggio 2: Archiviare le Credenziali Google OAuth in AWS Secrets Manager

1. Accedi alla Console di Gestione AWS.
2. Vai su Secrets Manager e scegli "Archivia un nuovo segreto".
3. Seleziona "Altro tipo di segreti".
4. Inserisci il clientId e il clientSecret di Google OAuth come coppie chiave-valore.

   1. Chiave: clientId, Valore: <YOUR_GOOGLE_CLIENT_ID>
   2. Chiave: clientSecret, Valore: <YOUR_GOOGLE_CLIENT_SECRET>

5. Segui le istruzioni per denominare e descrivere il segreto. Prendi nota del nome del segreto poiché ti servirà nel codice CDK. Ad esempio, googleOAuthCredentials. (Usa nel nome della variabile del Passaggio 3 <YOUR_SECRET_NAME>)
6. Rivedi e archivia il segreto.

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

Il userPoolDomainPrefix deve essere globalmente univoco tra tutti gli utenti Amazon Cognito. Se scegli un prefisso già utilizzato da un altro account AWS, la creazione del dominio del user pool non riuscirà. È una buona pratica includere identificatori, nomi di progetto o nomi di ambiente nel prefisso per garantire l'univocità.

## Passaggio 4: Distribuisci il Tuo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Passaggio 5: Aggiornare il Client OAuth di Google con gli URI di Reindirizzamento di Cognito

Dopo aver distribuito lo stack, AuthApprovedRedirectURI è visibile negli output di CloudFormation. Torna nella Console per Sviluppatori di Google e aggiorna il client OAuth con gli URI di reindirizzamento corretti.