# Configurazione del provider di identità esterno

## Step 1: Creare un Client OIDC

Segui le procedure per il provider OIDC di destinazione e prendi nota dei valori dell'ID client OIDC e del segreto. Anche l'URL dell'issuer sarà necessario nei passaggi successivi. Se durante il processo di configurazione è richiesto un URI di reindirizzamento, inserisci un valore temporaneo, che verrà sostituito dopo il completamento della distribuzione.

## Step 2: Memorizza le Credenziali in AWS Secrets Manager

1. Vai alla Console di Gestione AWS.
2. Naviga su Secrets Manager e seleziona "Store a new secret".
3. Seleziona "Other type of secrets".
4. Inserisci l'ID cliente e il segreto cliente come coppie chiave-valore.

   - Chiave: `clientId`, Valore: <YOUR_GOOGLE_CLIENT_ID>
   - Chiave: `clientSecret`, Valore: <YOUR_GOOGLE_CLIENT_SECRET>
   - Chiave: `issuerUrl`, Valore: <ISSUER_URL_OF_THE_PROVIDER>

5. Segui le istruzioni per nominare e descrivere il segreto. Prendi nota del nome del segreto poiché ti servirà nel codice CDK (Utilizzato nella variabile Step 3 <YOUR_SECRET_NAME>).
6. Rivedi e memorizza il segreto.

### Attenzione

I nomi delle chiavi devono corrispondere esattamente alle stringhe `clientId`, `clientSecret` e `issuerUrl`.

## Step 3: Aggiornare cdk.json

Nel file cdk.json, aggiungi l'ID Provider e il SecretName al file cdk.json.

in questo modo:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Non modificare
        "serviceName": "<YOUR_SERVICE_NAME>", // Imposta il valore che preferisci
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Attenzione

#### Unicità

Il `userPoolDomainPrefix` deve essere globalmente univoco tra tutti gli utenti di Amazon Cognito. Se scegli un prefisso già in uso da un altro account AWS, la creazione del dominio del pool di utenti fallirà. È una buona pratica includere identificatori, nomi di progetto o nomi di ambiente nel prefisso per garantirne l'unicità.

## Step 4: Distribuisci il tuo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Aggiornare il Client OIDC con gli URI di Redirect di Cognito

Dopo aver distribuito lo stack, `AuthApprovedRedirectURI` viene mostrato negli output di CloudFormation. Torna alla tua configurazione OIDC e aggiorna con gli URI di redirect corretti.