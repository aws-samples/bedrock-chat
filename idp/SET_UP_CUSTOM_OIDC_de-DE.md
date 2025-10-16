# Externen Identitätsanbieter einrichten

## Schritt 1: Erstellen eines OIDC-Clients

Folgen Sie den Verfahren für den gewünschten OIDC-Provider und notieren Sie sich die Werte für die OIDC-Client-ID und das Client-Secret. Außerdem wird die Issuer-URL für die folgenden Schritte benötigt. Falls während des Einrichtungsprozesses eine Redirect-URI erforderlich ist, geben Sie einen vorläufigen Wert ein, der nach Abschluss der Bereitstellung ersetzt wird.

## Schritt 2: Anmeldedaten im AWS Secrets Manager speichern

1. Öffnen Sie die AWS Management Console.
2. Navigieren Sie zum Secrets Manager und wählen Sie "Neues Geheimnis speichern".
3. Wählen Sie "Anderer Geheimnistyp".
4. Geben Sie die Client-ID und das Client-Secret als Schlüssel-Wert-Paare ein.

   - Schlüssel: `clientId`, Wert: <YOUR_GOOGLE_CLIENT_ID>
   - Schlüssel: `clientSecret`, Wert: <YOUR_GOOGLE_CLIENT_SECRET>
   - Schlüssel: `issuerUrl`, Wert: <ISSUER_URL_OF_THE_PROVIDER>

5. Folgen Sie den Anweisungen, um das Geheimnis zu benennen und zu beschreiben. Notieren Sie sich den Namen des Geheimnisses, da Sie ihn in Ihrem CDK-Code benötigen werden (Wird in Schritt 3 als Variable <YOUR_SECRET_NAME> verwendet).
6. Überprüfen und speichern Sie das Geheimnis.

### Achtung

Die Schlüsselnamen müssen exakt mit den Zeichenketten `clientId`, `clientSecret` und `issuerUrl` übereinstimmen.

## Schritt 3: cdk.json aktualisieren

Fügen Sie in Ihrer cdk.json-Datei die ID Provider und SecretName zur cdk.json-Datei hinzu.

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

Der `userPoolDomainPrefix` muss global einzigartig unter allen Amazon Cognito-Benutzern sein. Wenn Sie einen Präfix wählen, der bereits von einem anderen AWS-Konto verwendet wird, wird die Erstellung der User Pool-Domain fehlschlagen. Es ist eine gute Praxis, Bezeichner, Projektnamen oder Umgebungsnamen in den Präfix aufzunehmen, um die Einzigartigkeit sicherzustellen.

## Step 4: Deployen Sie Ihren CDK-Stack

Deployen Sie Ihren CDK-Stack in AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: OIDC-Client mit Cognito-Weiterleitungs-URIs aktualisieren

Nach der Bereitstellung des Stacks wird `AuthApprovedRedirectURI` in den CloudFormation-Ausgaben angezeigt. Gehen Sie zurück zu Ihrer OIDC-Konfiguration und aktualisieren Sie diese mit den korrekten Weiterleitungs-URIs.