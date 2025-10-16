# Configurazione di un provider di identità esterno per Google

## Step 1: Creare un Client OAuth 2.0 di Google

1. Vai alla Console per Sviluppatori Google.
2. Crea un nuovo progetto o seleziona uno esistente.
3. Naviga su "Credenziali", poi clicca su "Crea credenziali" e scegli "ID client OAuth".
4. Configura la schermata di consenso se richiesto.
5. Per il tipo di applicazione, seleziona "Applicazione web".
6. Lascia l'URI di reindirizzamento vuoto per ora per impostarlo successivamente.[Vedi Step5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una volta creato, prendi nota dell'ID Client e del Client Secret.

Per i dettagli, visita il [documento ufficiale di Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Step 2: Memorizza le Credenziali Google OAuth in AWS Secrets Manager

1. Vai alla Console di Gestione AWS.
2. Naviga su Secrets Manager e seleziona "Store a new secret".
3. Seleziona "Other type of secrets".
4. Inserisci il clientId e clientSecret di Google OAuth come coppie chiave-valore.

   1. Key: clientId, Value: <YOUR_GOOGLE_CLIENT_ID>
   2. Key: clientSecret, Value: <YOUR_GOOGLE_CLIENT_SECRET>

5. Segui le istruzioni per assegnare un nome e descrivere il segreto. Prendi nota del nome del segreto poiché ti servirà nel codice CDK. Per esempio, googleOAuthCredentials. (Da usare nello Step 3 come variabile <YOUR_SECRET_NAME>)
6. Rivedi e salva il segreto.

### Attenzione

I nomi delle chiavi devono corrispondere esattamente alle stringhe 'clientId' e 'clientSecret'.

## Step 3: Aggiornare cdk.json

Nel file cdk.json, aggiungi l'ID Provider e il SecretName al file cdk.json.

in questo modo:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Attenzione

#### Unicità

Il userPoolDomainPrefix deve essere globalmente unico tra tutti gli utenti di Amazon Cognito. Se scegli un prefisso che è già in uso da un altro account AWS, la creazione del dominio del pool di utenti fallirà. È una buona pratica includere identificatori, nomi di progetti o nomi di ambiente nel prefisso per garantirne l'unicità.

## Step 4: Distribuisci il tuo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Aggiornare il Client OAuth di Google con gli URI di Reindirizzamento di Cognito

Dopo aver distribuito lo stack, l'AuthApprovedRedirectURI viene mostrato negli output di CloudFormation. Torna alla Console per Sviluppatori di Google e aggiorna il client OAuth con gli URI di reindirizzamento corretti.