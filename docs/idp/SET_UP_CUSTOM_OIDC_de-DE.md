# Einrichten eines externen Identitätsanbieters

## Schritt 1: OIDC-Client erstellen

Befolgen Sie die Verfahren des jeweiligen OIDC-Anbieters und notieren Sie die Werte für die OIDC-Client-ID und das Geheimnis. Außerdem wird die Aussteller-URL (Issuer URL) für die folgenden Schritte benötigt. Falls für den Einrichtungsprozess eine Umleitungs-URI erforderlich ist, geben Sie einen Platzhalter-Wert ein, der nach Abschluss der Bereitstellung ersetzt wird.

## Schritt 2: Anmeldeinformationen in AWS Secrets Manager speichern

1. Gehen Sie zur AWS Management Console.
2. Navigieren Sie zu Secrets Manager und wählen Sie "Neuen Geheimschlüssel speichern".
3. Wählen Sie "Anderer Typ von Geheimnissen".
4. Geben Sie die Client-ID und den Client-Schlüssel als Schlüssel-Wert-Paare ein.

   - Schlüssel: `clientId`, Wert: <YOUR_GOOGLE_CLIENT_ID>
   - Schlüssel: `clientSecret`, Wert: <YOUR_GOOGLE_CLIENT_SECRET>
   - Schlüssel: `issuerUrl`, Wert: <ISSUER_URL_OF_THE_PROVIDER>

5. Folgen Sie den Aufforderungen, um den Geheimschlüssel zu benennen und zu beschreiben. Notieren Sie sich den Geheimschlüsselnamen, da Sie ihn in Ihrem CDK-Code benötigen (Verwendet in Schritt 3 Variablenname <YOUR_SECRET_NAME>).
6. Überprüfen und speichern Sie den Geheimschlüssel.

### Achtung

Die Schlüsselnamen müssen genau den Zeichenfolgen `clientId`, `clientSecret` und `issuerUrl` entsprechen.

## Schritt 3: Aktualisieren der cdk.json

Fügen Sie in Ihrer cdk.json-Datei die ID-Anbieter und den Geheimnisnamen hinzu.

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
    "userPoolDomainPrefix": "<EINDEUTIGES_DOMAIN_PRÄFIX_FÜR_IHREN_BENUTZERPOOL>"
  }
}
```

### Achtung

#### Eindeutigkeit

Das `userPoolDomainPrefix` muss global eindeutig sein und darf nicht von einem anderen AWS-Konto verwendet werden. Wenn Sie ein Präfix wählen, das bereits von einem anderen AWS-Konto genutzt wird, schlägt die Erstellung der Benutzerpooldomäne fehl. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in das Präfix einzubeziehen, um die Eindeutigkeit sicherzustellen.

## Schritt 4: Bereitstellen Ihres CDK-Stacks

Stellen Sie Ihren CDK-Stack in AWS bereit:

```sh
npx cdk deploy --require-approval never --all
```

## Schritt 5: OIDC-Client mit Cognito-Weiterleitungs-URIs aktualisieren

Nach der Bereitstellung des Stacks wird `AuthApprovedRedirectURI` in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zu Ihrer OIDC-Konfiguration und aktualisieren Sie diese mit den korrekten Weiterleitungs-URIs.