# Configurare un provider di identità esterno

## Passaggio 1: Creare un Client OIDC

Segui le procedure per il provider OIDC di destinazione e annota i valori per l'ID client OIDC e il segreto. Inoltre, l'URL dell'emittente è necessario nei passaggi successivi. Se durante il processo di configurazione è richiesto un URI di reindirizzamento, inserisci un valore fittizio che verrà sostituito dopo il completamento della distribuzione.

## Passaggio 2: Archiviare le Credenziali in AWS Secrets Manager

1. Accedere alla Console di Gestione AWS.
2. Navigare in Secrets Manager e scegliere "Archivia un nuovo segreto".
3. Selezionare "Altro tipo di segreti".
4. Inserire l'ID client e il segreto client come coppie chiave-valore.

   - Chiave: `clientId`, Valore: <YOUR_GOOGLE_CLIENT_ID>
   - Chiave: `clientSecret`, Valore: <YOUR_GOOGLE_CLIENT_SECRET>
   - Chiave: `issuerUrl`, Valore: <ISSUER_URL_OF_THE_PROVIDER>

5. Seguire le istruzioni per assegnare un nome e una descrizione al segreto. Annotare il nome del segreto poiché sarà necessario nel codice CDK (Utilizzato nel Passaggio 3 con il nome della variabile <YOUR_SECRET_NAME>).
6. Rivedere e archiviare il segreto.

### Attenzione

I nomi delle chiavi devono corrispondere esattamente alle stringhe `clientId`, `clientSecret` e `issuerUrl`.

## Passaggio 3: Aggiornare cdk.json

Nel file cdk.json, aggiungi il Provider di Identità e il Nome del Segreto al file cdk.json.

in questo modo:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Non modificare
        "serviceName": "<TUO_NOME_SERVIZIO>", // Imposta un valore a tuo piacimento
        "secretName": "<TUO_NOME_SEGRETO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFISSO_DOMINIO_UNIVOCO_PER_IL_TUO_USER_POOL>"
  }
}
```

### Attenzione

#### Univocità

Il `userPoolDomainPrefix` deve essere globalmente univoco tra tutti gli utenti Amazon Cognito. Se scegli un prefisso già utilizzato da un altro account AWS, la creazione del dominio del user pool non riuscirà. È una buona pratica includere identificatori, nomi di progetti o nomi di ambienti nel prefisso per garantire l'univocità.

## Passaggio 4: Distribuire lo Stack CDK

Distribuisci il tuo stack CDK su AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Passaggio 5: Aggiornare il Client OIDC con gli URI di Reindirizzamento di Cognito

Dopo aver distribuito lo stack, `AuthApprovedRedirectURI` sarà visibile negli output di CloudFormation. Torna alla configurazione OIDC e aggiorna gli URI di reindirizzamento corretti.