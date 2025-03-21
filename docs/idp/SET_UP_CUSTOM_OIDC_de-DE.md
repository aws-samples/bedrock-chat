# Einrichten eines externen Identitätsanbieters

## Schritt 1: OIDC-Client erstellen

Folgen Sie den Verfahren des Ziel-OIDC-Providers und notieren Sie die Werte für die OIDC-Client-ID und das Geheimnis. Auch die Aussteller-URL (Issuer URL) wird in den folgenden Schritten benötigt. Falls für den Einrichtungsprozess eine Umleitungs-URI (Redirect URI) erforderlich ist, geben Sie einen Platzhalter-Wert ein, der nach Abschluss der Bereitstellung ersetzt wird.

## Schritt 2: Anmeldedaten in AWS Secrets Manager speichern

1. Öffnen Sie die AWS Management Console.
2. Navigieren Sie zu Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Anderer Typ von Geheimnissen".
4. Geben Sie die Client-ID und den Client-Schlüssel als Schlüssel-Wert-Paare ein.

   - Schlüssel: `clientId`, Wert: <YOUR_GOOGLE_CLIENT_ID>
   - Schlüssel: `clientSecret`, Wert: <YOUR_GOOGLE_CLIENT_SECRET>
   - Schlüssel: `issuerUrl`, Wert: <ISSUER_URL_OF_THE_PROVIDER>

5. Folgen Sie den Aufforderungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Geheimnsnamen, da Sie ihn in Ihrem CDK-Code benötigen (Wird in Schritt 3 als Variable <YOUR_SECRET_NAME> verwendet).
6. Überprüfen und speichern Sie das Geheimnis.

### Achtung

Die Schlüsselnamen müssen genau den Zeichenfolgen `clientId`, `clientSecret` und `issuerUrl` entsprechen.

## Schritt 3: Aktualisieren von cdk.json

Fügen Sie in Ihrer cdk.json-Datei die ID-Anbieter und den Geheimnisnamen zur cdk.json-Datei hinzu.

wie folgt:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Nicht ändern
        "serviceName": "<IHR_DIENSTNAME>", // Wählen Sie einen beliebigen Wert
        "secretName": "<IHR_GEHEIMER_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<EINDEUTIGES_DOMAIN-PRÄFIX_FÜR_IHREN_BENUTZER-POOL>"
  }
}
```

### Achtung

#### Eindeutigkeit

Das `userPoolDomainPrefix` muss global über alle Amazon Cognito-Benutzer hinweg eindeutig sein. Wenn Sie ein Präfix wählen, das bereits von einem anderen AWS-Konto verwendet wird, schlägt die Erstellung der Benutzer-Pool-Domäne fehl. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in das Präfix einzubeziehen, um Eindeutigkeit zu gewährleisten.

## Schritt 4: Bereitstellen Ihres CDK-Stacks

Stellen Sie Ihren CDK-Stack in AWS bereit:

```sh
npx cdk deploy --require-approval never --all
```

## Schritt 5: OIDC-Client mit Cognito-Weiterleitungs-URIs aktualisieren

Nach der Bereitstellung des Stacks wird `AuthApprovedRedirectURI` in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zu Ihrer OIDC-Konfiguration und aktualisieren Sie diese mit den korrekten Weiterleitungs-URIs.