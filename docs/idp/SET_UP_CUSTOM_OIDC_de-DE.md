# Externen Identitätsanbieter einrichten

## Schritt 1: Einen OIDC-Client erstellen

Folgen Sie den Verfahren für den gewünschten OIDC-Provider und notieren Sie sich die Werte für die OIDC-Client-ID und das Geheimnis. Außerdem wird die Issuer-URL für die folgenden Schritte benötigt. Falls während des Einrichtungsprozesses eine Redirect-URI erforderlich ist, geben Sie einen vorläufigen Wert ein, der nach Abschluss der Bereitstellung ersetzt wird.

## Schritt 2: Anmeldeinformationen im AWS Secrets Manager speichern

1. Öffnen Sie die AWS Management Console.
2. Navigieren Sie zum Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Andere Art von Geheimnissen".
4. Geben Sie die Client-ID und das Client-Geheimnis als Schlüssel-Wert-Paare ein.

   - Schlüssel: `clientId`, Wert: <YOUR_GOOGLE_CLIENT_ID>
   - Schlüssel: `clientSecret`, Wert: <YOUR_GOOGLE_CLIENT_SECRET>
   - Schlüssel: `issuerUrl`, Wert: <ISSUER_URL_OF_THE_PROVIDER>

5. Folgen Sie den Anweisungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Namen des Geheimnisses, da Sie ihn in Ihrem CDK-Code benötigen werden (Wird in Schritt 3 als Variable <YOUR_SECRET_NAME> verwendet).
6. Überprüfen und speichern Sie das Geheimnis.

### Achtung

Die Schlüsselnamen müssen exakt mit den Zeichenfolgen `clientId`, `clientSecret` und `issuerUrl` übereinstimmen.

## Schritt 3: Aktualisierung der cdk.json

Fügen Sie in Ihrer cdk.json-Datei die ID-Provider und den SecretName zur cdk.json-Datei hinzu.

Wie folgt:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Nicht ändern
        "serviceName": "<YOUR_SERVICE_NAME>", // Setzen Sie einen beliebigen Wert
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Achtung

#### Einzigartigkeit

Der `userPoolDomainPrefix` muss global einzigartig über alle Amazon Cognito-Benutzer hinweg sein. Wenn Sie ein Präfix wählen, das bereits von einem anderen AWS-Konto verwendet wird, wird die Erstellung der User-Pool-Domain fehlschlagen. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in das Präfix aufzunehmen, um die Einzigartigkeit sicherzustellen.

## Step 4: Bereitstellen Ihres CDK-Stacks

Stellen Sie Ihren CDK-Stack in AWS bereit:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Aktualisieren des OIDC-Clients mit Cognito Redirect-URIs

Nach dem Bereitstellen des Stacks wird `AuthApprovedRedirectURI` in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zu Ihrer OIDC-Konfiguration und aktualisieren Sie diese mit den korrekten Redirect-URIs.