# Externen Identitätsanbieter für Google einrichten

## Schritt 1: Erstellen eines Google OAuth 2.0 Clients

1. Gehen Sie zur Google Developer Console.
2. Erstellen Sie ein neues Projekt oder wählen Sie ein bestehendes aus.
3. Navigieren Sie zu "Anmeldedaten", klicken Sie dann auf "Anmeldedaten erstellen" und wählen Sie "OAuth-Client-ID".
4. Konfigurieren Sie den Zustimmungsbildschirm, wenn Sie dazu aufgefordert werden.
5. Wählen Sie als Anwendungstyp "Webanwendung" aus.
6. Lassen Sie die Weiterleitungs-URI vorerst leer, um sie später einzurichten.[Siehe Schritt 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Notieren Sie sich nach der Erstellung die Client-ID und das Client-Secret.

Für Details besuchen Sie die [offizielle Google-Dokumentation](https://support.google.com/cloud/answer/6158849?hl=en)

## Schritt 2: Google OAuth-Anmeldeinformationen im AWS Secrets Manager speichern

1. Gehen Sie zur AWS Management Console.
2. Navigieren Sie zum Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Anderer Geheimnistyp".
4. Geben Sie die Google OAuth clientId und clientSecret als Schlüssel-Wert-Paare ein.

   1. Schlüssel: clientId, Wert: <YOUR_GOOGLE_CLIENT_ID>
   2. Schlüssel: clientSecret, Wert: <YOUR_GOOGLE_CLIENT_SECRET>

5. Folgen Sie den Anweisungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Namen des Geheimnisses, da Sie ihn in Ihrem CDK-Code benötigen werden. Zum Beispiel: googleOAuthCredentials. (Verwenden Sie in Schritt 3 den Variablennamen <YOUR_SECRET_NAME>)
6. Überprüfen und speichern Sie das Geheimnis.

### Achtung

Die Schlüsselnamen müssen exakt mit den Zeichenfolgen 'clientId' und 'clientSecret' übereinstimmen.

## Schritt 3: cdk.json aktualisieren

Fügen Sie in Ihrer cdk.json-Datei die ID Provider und SecretName zur cdk.json-Datei hinzu.

Wie folgt:

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

### Achtung

#### Einzigartigkeit

Der userPoolDomainPrefix muss global einzigartig über alle Amazon Cognito-Benutzer hinweg sein. Wenn Sie einen Präfix wählen, der bereits von einem anderen AWS-Konto verwendet wird, wird die Erstellung der User Pool-Domain fehlschlagen. Es ist eine gute Praxis, Identifikatoren, Projektnamen oder Umgebungsnamen in den Präfix einzubauen, um die Einzigartigkeit sicherzustellen.

## Step 4: Deployen Sie Ihren CDK-Stack

Deployen Sie Ihren CDK-Stack in AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Schritt 5: Aktualisierung des Google OAuth-Clients mit Cognito Redirect-URIs

Nach der Bereitstellung des Stacks wird AuthApprovedRedirectURI in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zur Google Developer Console und aktualisieren Sie den OAuth-Client mit den korrekten Redirect-URIs.