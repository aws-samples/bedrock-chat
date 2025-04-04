# Externe Identitätsanbieter für Google einrichten

## Schritt 1: Erstellen eines Google OAuth 2.0-Clients

1. Gehen Sie zur Google Developer Console.
2. Erstellen Sie ein neues Projekt oder wählen Sie ein vorhandenes aus.
3. Navigieren Sie zu "Anmeldeinformationen" und klicken Sie dann auf "Anmeldeinformationen erstellen" und wählen Sie "OAuth-Client-ID".
4. Konfigurieren Sie den Zustimmungsbildschirm, falls aufgefordert.
5. Wählen Sie als Anwendungstyp "Webanwendung".
6. Lassen Sie die Umleitungs-URI vorerst leer, um sie später festzulegen, und speichern Sie vorläufig.[Siehe Schritt 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Notieren Sie sich nach der Erstellung die Client-ID und den Client-Schlüssel.

Weitere Details finden Sie in [Googles offizieller Dokumentation](https://support.google.com/cloud/answer/6158849?hl=en)

## Schritt 2: Google OAuth-Anmeldedaten in AWS Secrets Manager speichern

1. Rufen Sie die AWS Management Console auf.
2. Navigieren Sie zu Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Anderer Typ von Geheimnis".
4. Geben Sie die Google OAuth clientId und clientSecret als Schlüssel-Wert-Paare ein.

   1. Schlüssel: clientId, Wert: <YOUR_GOOGLE_CLIENT_ID>
   2. Schlüssel: clientSecret, Wert: <YOUR_GOOGLE_CLIENT_SECRET>

5. Folgen Sie den Eingabeaufforderungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Geheimnsnamen, da Sie ihn in Ihrem CDK-Code benötigen werden. Zum Beispiel: googleOAuthCredentials. (Verwenden Sie in Schritt 3 den Variablennamen <YOUR_SECRET_NAME>)
6. Überprüfen Sie das Geheimnis und speichern Sie es.

### Achtung

Die Schlüsselnamen müssen genau den Zeichenfolgen 'clientId' und 'clientSecret' entsprechen.

## Schritt 3: cdk.json aktualisieren

Fügen Sie in Ihrer cdk.json-Datei den ID-Anbieter und den Geheimnisnamen zur cdk.json-Datei hinzu.

wie folgt:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<IHR_GEHEIMER_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<EINDEUTIGER_DOMÄNEN-PRÄFIX_FÜR_IHREN_BENUTZER-POOL>"
  }
}
```

### Achtung

#### Eindeutigkeit

Der userPoolDomainPrefix muss global eindeutig für alle Amazon Cognito-Benutzer sein. Wenn Sie einen Präfix wählen, der bereits von einem anderen AWS-Konto verwendet wird, schlägt die Erstellung der Benutzer-Pool-Domäne fehl. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in den Präfix einzubeziehen, um Eindeutigkeit zu gewährleisten.

## Schritt 4: Bereitstellen Ihres CDK-Stacks

Stellen Sie Ihren CDK-Stack in AWS bereit:

```sh
npx cdk deploy --require-approval never --all
```

## Schritt 5: Google OAuth-Client mit Cognito-Redirect-URIs aktualisieren

Nach der Bereitstellung des Stacks wird AuthApprovedRedirectURI in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zur Google Developer Console und aktualisieren Sie den OAuth-Client mit den korrekten Redirect-URIs.