# Einrichten eines externen Identitätsanbieters

## Schritt 1: OIDC-Client erstellen

Folgen Sie den Verfahren des jeweiligen OIDC-Providers und notieren Sie sich die Werte für die OIDC-Client-ID und das Geheimnis. Auch die Aussteller-URL (Issuer URL) wird in den folgenden Schritten benötigt. Falls für den Einrichtungsprozess eine Umleitungs-URI (Redirect URI) erforderlich ist, geben Sie einen Platzhalter-Wert ein, der nach Abschluss der Bereitstellung ersetzt wird.

## Schritt 2: Anmeldeinformationen in AWS Secrets Manager speichern

1. Öffnen Sie die AWS Management Console.
2. Navigieren Sie zu Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Anderer Typ von Geheimnissen".
4. Geben Sie die Client-ID und den Client-Schlüssel als Schlüssel-Wert-Paare ein.

   - Schlüssel: `clientId`, Wert: <YOUR_GOOGLE_CLIENT_ID>
   - Schlüssel: `clientSecret`, Wert: <YOUR_GOOGLE_CLIENT_SECRET>
   - Schlüssel: `issuerUrl`, Wert: <ISSUER_URL_OF_THE_PROVIDER>

5. Folgen Sie den Aufforderungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Geheimnsnamen, da Sie ihn in Ihrem CDK-Code benötigen (Verwendet in Schritt 3 Variablenname <YOUR_SECRET_NAME>).
6. Überprüfen und speichern Sie das Geheimnis.

### Aufmerksamkeit

Die Schlüsselnamen müssen genau mit den Zeichenfolgen `clientId`, `clientSecret` und `issuerUrl` übereinstimmen.

## Schritt 3: Aktualisieren der cdk.json

Fügen Sie in Ihrer cdk.json-Datei die ID des Anbieters und den Geheimnisnamen hinzu.

wie folgt:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Nicht ändern
        "serviceName": "<IHR_DIENSTNAME>", // Wählen Sie einen beliebigen Wert
        "secretName": "<IHR_GEHEIMNIS_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<EINDEUTIGER_DOMAIN_PRÄFIX_FÜR_IHREN_BENUTZERPOOL>"
  }
}
```

### Achtung

#### Eindeutigkeit

Der `userPoolDomainPrefix` muss global eindeutig über alle Amazon Cognito-Benutzer hinweg sein. Wenn Sie einen Präfix wählen, der bereits von einem anderen AWS-Konto verwendet wird, schlägt die Erstellung der Benutzerpool-Domäne fehl. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in den Präfix einzubeziehen, um Eindeutigkeit zu gewährleisten.

## Schritt 4: Bereitstellen Ihres CDK-Stacks

Stellen Sie Ihren CDK-Stack in AWS bereit:

```sh
npx cdk deploy --require-approval never --all
```

## Schritt 5: OIDC-Client mit Cognito-Weiterleitungs-URIs aktualisieren

Nach der Bereitstellung des Stacks wird `AuthApprovedRedirectURI` in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zu Ihrer OIDC-Konfiguration und aktualisieren Sie diese mit den korrekten Weiterleitungs-URIs.