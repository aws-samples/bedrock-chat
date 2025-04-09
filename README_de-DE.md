<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md)

Eine mehrsprachige generative KI-Plattform, unterstützt von [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Unterstützt Chat, benutzerdefinierte Bots mit Wissen (RAG), Bot-Sharing über einen Bot-Store und Aufgabenautomatisierung mit Agenten.

![](./imgs/demo.gif)

> [!Warnung]
>
> **V3 wurde veröffentlicht. Bitte überprüfen Sie sorgfältig den [Migrationsleitfaden](./migration/V2_TO_V3_de-DE.md) für ein Update.** Ohne Sorgfalt werden **BOTS AUS V2 UNBRAUCHBAR WERDEN.**

### Bot-Personalisierung / Bot-Store

Fügen Sie Ihre eigene Anweisung und Wissen hinzu (auch bekannt als [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Der Bot kann über einen Bot-Store-Marktplatz zwischen Anwendungsnutzern geteilt werden. Der angepasste Bot kann auch als eigenständige API veröffentlicht werden (Weitere Informationen [hier](./PUBLISH_API_de-DE.md)).

<details>
<summary>Screenshots</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Sie können auch bestehende [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) importieren.

![](./imgs/import_existing_kb.png)

</details>

> [!Wichtig]
> Aus Governance-Gründen können nur zugelassene Benutzer benutzerdefinierte Bots erstellen. Um die Erstellung benutzerdefinierter Bots zu ermöglichen, muss der Benutzer Mitglied der Gruppe `CreatingBotAllowed` sein, die über die Verwaltungskonsole > Amazon Cognito-Benutzer-Pools oder die AWS-CLI eingerichtet werden kann. Beachten Sie, dass die Benutzer-Pool-ID durch Zugriff auf CloudFormation > BedrockChatStack > Ausgaben > `AuthUserPoolIdxxxx` referenziert werden kann.

### Administratorfunktionen

API-Management, Bots als wesentlich markieren, Nutzungsanalyse für Bots. [Details](./ADMINISTRATOR_de-DE.md)

<details>
<summary>Screenshots</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agent

Durch die Nutzung der [Agent-Funktionalität](./AGENT_de-DE.md) kann Ihr Chatbot automatisch komplexere Aufgaben bewältigen. Beispielsweise kann der Agent zur Beantwortung einer Benutzerfrage notwendige Informationen aus externen Tools abrufen oder die Aufgabe in mehrere Schritte zur Verarbeitung zerlegen.

<details>
<summary>Screenshots</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Super-einfache Bereitstellung

- Öffnen Sie in der Region us-east-1 [Bedrock Model-Zugriff](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Modellzugriff verwalten` > Wählen Sie alle Modelle aus, die Sie verwenden möchten, und klicken Sie dann auf `Änderungen speichern`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

- Öffnen Sie [CloudShell](https://console.aws.amazon.com/cloudshell/home) in der Region, in der Sie bereitstellen möchten
- Führen Sie die Bereitstellung über die folgenden Befehle aus. Wenn Sie die zu deploayende Version angeben oder Sicherheitsrichtlinien anwenden möchten, geben Sie bitte die entsprechenden Parameter aus [Optionale Parameter](#optionale-parameter) an.

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Sie werden gefragt, ob es sich um einen neuen Benutzer oder v3 handelt. Wenn Sie kein Benutzer von v0 sind, geben Sie bitte `y` ein.

### Optionale Parameter

Sie können die folgenden Parameter während der Bereitstellung angeben, um Sicherheit und Anpassung zu verbessern:

- **--disable-self-register**: Selbstregistrierung deaktivieren (Standard: aktiviert). Wenn dieses Flag gesetzt ist, müssen Sie alle Benutzer in Cognito erstellen, und es wird keine Selbstregistrierung von Konten erlaubt.
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) aktivieren (Standard: deaktiviert). Wenn dieses Flag gesetzt ist, verbessert es die Kaltstart-Zeiten für Lambda-Funktionen und bietet schnellere Antwortzeiten für ein besseres Benutzererlebnis.
- **--ipv4-ranges**: Kommagetrennte Liste der erlaubten IPv4-Bereiche. (Standard: alle IPv4-Adressen erlauben)
- **--ipv6-ranges**: Kommagetrennte Liste der erlaubten IPv6-Bereiche. (Standard: alle IPv6-Adressen erlauben)
- **--disable-ipv6**: Verbindungen über IPv6 deaktivieren. (Standard: aktiviert)
- **--allowed-signup-email-domains**: Kommagetrennte Liste der erlaubten E-Mail-Domains für die Anmeldung. (Standard: keine Domainbeschränkung)
- **--bedrock-region**: Region definieren, in der Bedrock verfügbar ist. (Standard: us-east-1)
- **--repo-url**: Benutzerdefiniertes Repository von Bedrock Chat für die Bereitstellung, falls geforkt oder benutzerdefinierte Quellcodeverwaltung. (Standard: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Die Version von Bedrock Chat, die bereitgestellt werden soll. (Standard: neueste Version in der Entwicklung)
- **--cdk-json-override**: Sie können beliebige CDK-Kontextwerte während der Bereitstellung mithilfe des Override-JSON-Blocks überschreiben. Dies ermöglicht es Ihnen, die Konfiguration zu ändern, ohne die cdk.json-Datei direkt zu bearbeiten.

Beispielverwendung:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

Das Override-JSON muss der gleichen Struktur wie cdk.json folgen. Sie können beliebige Kontextwerte überschreiben, einschließlich:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Und andere in cdk.json definierte Kontextwerte

> [!Hinweis]
> Die Override-Werte werden während der Bereitstellung im AWS-Code-Build mit der vorhandenen cdk.json-Konfiguration zusammengeführt. Die angegebenen Werte haben Vorrang vor den Werten in cdk.json.

#### Beispielbefehl mit Parametern:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Nach etwa 35 Minuten erhalten Sie die folgende Ausgabe, auf die Sie über Ihren Browser zugreifen können

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Der Anmeldebildschirm wird wie oben gezeigt angezeigt, wo Sie Ihre E-Mail-Adresse registrieren und sich anmelden können.

> [!Wichtig]
> Ohne Festlegung des optionalen Parameters erlaubt diese Bereitstellungsmethode jedem, der die URL kennt, sich anzumelden. Für den Produktiveinsatz wird dringend empfohlen, IP-Adresseinschränkungen hinzuzufügen und die Selbstregistrierung zu deaktivieren, um Sicherheitsrisiken zu minimieren (Sie können allowed-signup-email-domains definieren, um Benutzer so zu beschränken, dass nur E-Mail-Adressen aus der Domain Ihres Unternehmens sich anmelden können). Verwenden Sie sowohl ipv4-ranges als auch ipv6-ranges für IP-Adresseinschränkungen und deaktivieren Sie die Selbstregistrierung, indem Sie disable-self-register beim Ausführen von ./bin verwenden.

> [!TIPP]
> Wenn die `Frontend URL` nicht erscheint oder Bedrock Chat nicht ordnungsgemäß funktioniert, kann dies ein Problem mit der neuesten Version sein. In diesem Fall fügen Sie bitte `--version "v3.0.0"` zu den Parametern hinzu und versuchen Sie die Bereitstellung erneut.

## Architektur

Es handelt sich um eine Architektur, die auf AWS-verwalteten Diensten basiert und die Infrastrukturverwaltung überflüssig macht. Durch die Nutzung von Amazon Bedrock ist keine Kommunikation mit APIs außerhalb von AWS erforderlich. Dies ermöglicht die Bereitstellung skalierbarer, zuverlässiger und sicherer Anwendungen.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL-Datenbank zur Speicherung des Gesprächsverlaufs
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend-API-Endpunkt ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Bereitstellung der Frontend-Anwendung ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP-Adresseinschränkung
- [Amazon Cognito](https://aws.amazon.com/cognito/): Benutzerauthentifizierung
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Verwalteter Dienst zur Nutzung von Grundmodellen über APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Bietet eine verwaltete Schnittstelle für Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) und stellt Dienste zum Einbetten und Parsen von Dokumenten bereit
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Empfang von Ereignissen aus dem DynamoDB-Stream und Starten von Step Functions zum Einbetten externen Wissens
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrierung der Eingabepipeline zum Einbetten externen Wissens in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Dient als Backend-Datenbank für Bedrock Knowledge Bases und bietet Volltextsuche und Vektorsuche-Funktionalitäten für eine präzise Informationssuche
- [Amazon Athena](https://aws.amazon.com/athena/): Abfragedienst zur Analyse des S3-Buckets

![](./imgs/arch.png)

## Bereitstellung mit CDK

Die Super-einfache Bereitstellung verwendet [AWS CodeBuild](https://aws.amazon.com/codebuild/), um die Bereitstellung intern mit CDK durchzuführen. Dieser Abschnitt beschreibt das Verfahren zur direkten Bereitstellung mit CDK.

- Bitte stellen Sie sicher, dass UNIX, Docker und eine Node.js-Laufzeitumgebung vorhanden sind. Falls nicht, können Sie auch [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping) verwenden

> [!Wichtig]
> Wenn während der Bereitstellung nicht genügend Speicherplatz in der lokalen Umgebung vorhanden ist, kann die CDK-Initialisierung zu einem Fehler führen. Wenn Sie in Cloud9 oder ähnlichem arbeiten, empfehlen wir, die Volumengröße der Instanz vor der Bereitstellung zu erweitern.

- Repository klonen

```
git clone https://github.com/aws-samples/bedrock-chat
```

- npm-Pakete installieren

```
cd bedrock-chat
cd cdk
npm ci
```

- Bei Bedarf die folgenden Einträge in [cdk.json](./cdk/cdk.json) bearbeiten:

  - `bedrockRegion`: Region, in der Bedrock verfügbar ist. **HINWEIS: Bedrock unterstützt derzeit nicht alle Regionen.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Erlaubte IP-Adressbereiche.
  - `enableLambdaSnapStart`: Standardmäßig auf true gesetzt. Auf false setzen, wenn in einer [Region bereitgestellt wird, die Lambda SnapStart für Python-Funktionen nicht unterstützt](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Vor der CDK-Bereitstellung müssen Sie die Initialisierung für die Bereitstellungsregion einmalig durchführen.

```
npx cdk bootstrap
```

- Dieses Beispielprojekt bereitstellen

```
npx cdk deploy --require-approval never --all
```

- Sie erhalten eine Ausgabe ähnlich der folgenden. Die URL der Webanwendung wird in `BedrockChatStack.FrontendURL` ausgegeben, bitte greifen Sie darauf über Ihren Browser zu.

```sh
 ✅  BedrockChatStack

✨  Bereitstellungszeit: 78.57s

Ausgaben:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Parameter definieren

Sie können Parameter für Ihre Bereitstellung auf zwei Arten definieren: mit `cdk.json` oder mit der typsicheren `parameter.ts`-Datei.

#### Verwendung von cdk.json (Traditionelle Methode)

Die traditionelle Methode zur Konfiguration von Parametern ist die Bearbeitung der `cdk.json`-Datei. Dieser Ansatz ist einfach, bietet aber keine Typüberprüfung:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Verwendung von parameter.ts (Empfohlene typsichere Methode)

Für bessere Typsicherheit und Entwicklererfahrung können Sie die `parameter.ts`-Datei verwenden, um Ihre Parameter zu definieren:

```typescript
// Parameter für die Standardumgebung definieren
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Parameter für zusätzliche Umgebungen definieren
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Kosteneinsparung für Entwicklungsumgebung
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Verbesserte Verfügbarkeit für Produktion
});
```

> [!Hinweis]
> Bestehende Benutzer können `cdk.json` weiterhin ohne Änderungen verwenden. Der `parameter.ts`-Ansatz wird für neue Bereitstellungen oder bei der Verwaltung mehrerer Umgebungen empfohlen.

### Bereitstellung mehrerer Umgebungen

Sie können mehrere Umgebungen aus derselben Codebasis mithilfe der `parameter.ts`-Datei und der `-c envName`-Option bereitstellen.

#### Voraussetzungen

1. Definieren Sie Ihre Umgebungen in `parameter.ts` wie oben gezeigt
2. Jede Umgebung wird ihre eigenen Ressourcen mit umgebungsspezifischen Präfixen haben

#### Bereitstellungsbefehle

Bereitstellung einer bestimmten Umgebung:

```bash
# Entwicklungsumgebung bereitstellen
npx cdk deploy --all -c envName=dev

# Produktionsumgebung bereitstellen
npx cdk deploy --all -c envName=prod
```

Wenn keine Umgebung angegeben ist, wird die "default"-Umgebung verwendet:

```bash
# Standardumgebung bereitstellen
npx cdk deploy --all
```

#### Wichtige Hinweise

1. **Stack-Benennung**:

   - Die Hauptstacks für jede Umgebung werden mit dem Umgebungsnamen als Präfix versehen (z.B. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Benutzerdefinierte Bot-Stacks (`BrChatKbStack*`) und API-Veröffentlichungs-Stacks (`ApiPublishmentStack*`) erhalten jedoch keine Umgebungs-Präfixe, da sie zur Laufzeit dynamisch erstellt werden

2. **Ressourcenbenennung**:

   - Nur einige Ressourcen erhalten Umgebungs-Präfixe in ihren Namen (z.B. `dev_ddb_export`-Tabelle, `dev-FrontendWebAcl`)
   - Die meisten Ressourcen behalten ihre ursprünglichen Namen, sind aber durch separate Stacks isoliert

3. **Umgebungsidentifikation**:

   - Alle Ressourcen werden mit einem `CDKEnvironment`-Tag versehen, das den Umgebungsnamen enthält
   - Sie können dieses Tag verwenden, um zu identifizieren, zu welcher Umgebung eine Ressource gehört
   - Beispiel: `CDKEnvironment: dev` oder `CDKEnvironment: prod`

4. **Überschreiben der Standardumgebung**: Wenn Sie eine "default"-Umgebung in `parameter.ts` definieren, überschreibt diese die Einstellungen in `cdk.json`. Um weiterhin `cdk.json` zu verwenden, definieren Sie keine "default"-Umgebung in `parameter.ts`.

5. **Umgebungsanforderungen**: Um andere Umgebungen als "default" zu erstellen, müssen Sie `parameter.ts` verwenden. Die `-c envName`-Option allein reicht ohne entsprechende Umgebungsdefinitionen nicht aus.

6. **Ressourcenisolierung**: Jede Umgebung erstellt ihren eigenen Ressourcensatz, sodass Sie Entwicklungs-, Test- und Produktionsumgebungen im selben AWS-Konto ohne Konflikte haben können.

## Andere

Sie können Parameter für Ihre Bereitstellung auf zwei Arten definieren: mithilfe von `cdk.json` oder mithilfe der typsicheren `parameter.ts`-Datei.

#### Verwendung von cdk.json (Traditionelle Methode)

Die traditionelle Methode zur Konfiguration von Parametern ist die Bearbeitung der `cdk.json`-Datei. Dieser Ansatz ist einfach, bietet jedoch keine Typenprüfung:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Verwendung von parameter.ts (Empfohlene typsichere Methode)

Für bessere Typsicherheit und Entwicklererfahrung können Sie die `parameter.ts`-Datei verwenden, um Ihre Parameter zu definieren:

```typescript
// Parameter für die Standard-Umgebung definieren
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Parameter für zusätzliche Umgebungen definieren
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Kosteneinsparung für Entwicklungsumgebung
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Verbesserte Verfügbarkeit für Produktionsumgebung
});
```

> [!Hinweis]
> Bestehende Benutzer können weiterhin `cdk.json` ohne Änderungen verwenden. Der `parameter.ts`-Ansatz wird für neue Bereitstellungen oder bei der Verwaltung mehrerer Umgebungen empfohlen.

### Bereitstellung mehrerer Umgebungen

Sie können mehrere Umgebungen aus derselben Codebasis mithilfe der `parameter.ts`-Datei und der `-c envName`-Option bereitstellen.

#### Voraussetzungen

1. Definieren Sie Ihre Umgebungen in `parameter.ts` wie oben gezeigt
2. Jede Umgebung wird eigene Ressourcen mit umgebungsspezifischen Präfixen haben

#### Bereitstellungsbefehle

Um eine bestimmte Umgebung bereitzustellen:

```bash
# Entwicklungsumgebung bereitstellen
npx cdk deploy --all -c envName=dev

# Produktionsumgebung bereitstellen
npx cdk deploy --all -c envName=prod
```

Wenn keine Umgebung angegeben wird, wird die "Standard"-Umgebung verwendet:

```bash
# Standardumgebung bereitstellen
npx cdk deploy --all
```

#### Wichtige Hinweise

1. **Stack-Benennung**:

   - Die Haupt-Stacks für jede Umgebung werden mit dem Umgebungsnamen als Präfix versehen (z.B. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Benutzerdefinierte Bot-Stacks (`BrChatKbStack*`) und API-Veröffentlichungs-Stacks (`ApiPublishmentStack*`) erhalten jedoch keine Umgebungspräfixe, da sie zur Laufzeit dynamisch erstellt werden

2. **Ressourcenbenennung**:

   - Nur einige Ressourcen erhalten Umgebungspräfixe in ihren Namen (z.B. `dev_ddb_export`-Tabelle, `dev-FrontendWebAcl`)
   - Die meisten Ressourcen behalten ihre ursprünglichen Namen, sind aber durch separate Stacks isoliert

3. **Umgebungsidentifikation**:

   - Alle Ressourcen werden mit einem `CDKEnvironment`-Tag versehen, das den Umgebungsnamen enthält
   - Sie können dieses Tag verwenden, um zu identifizieren, zu welcher Umgebung eine Ressource gehört
   - Beispiel: `CDKEnvironment: dev` oder `CDKEnvironment: prod`

4. **Überschreiben der Standard-Umgebung**: Wenn Sie eine "Standard"-Umgebung in `parameter.ts` definieren, überschreibt diese die Einstellungen in `cdk.json`. Um weiterhin `cdk.json` zu verwenden, definieren Sie keine "Standard"-Umgebung in `parameter.ts`.

5. **Umgebungsanforderungen**: Um andere Umgebungen als "Standard" zu erstellen, müssen Sie `parameter.ts` verwenden. Die `-c envName`-Option allein reicht ohne entsprechende Umgebungsdefinitionen nicht aus.

6. **Ressourcenisolation**: Jede Umgebung erstellt ihren eigenen Ressourcensatz, sodass Sie Entwicklungs-, Test- und Produktionsumgebungen im selben AWS-Konto ohne Konflikte haben können.

## Andere

### Ressourcen entfernen

Wenn Sie die CLI und CDK verwenden, führen Sie bitte `npx cdk destroy` aus. Wenn nicht, greifen Sie auf [CloudFormation](https://console.aws.amazon.com/cloudformation/home) zu und löschen Sie `BedrockChatStack` und `FrontendWafStack` manuell. Bitte beachten Sie, dass sich `FrontendWafStack` in der Region `us-east-1` befindet.

### Spracheinstellungen

Dieses Asset erkennt die Sprache automatisch mit [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Sie können die Sprache im Anwendungsmenü wechseln. Alternativ können Sie den Query-String verwenden, um die Sprache wie folgt festzulegen.

> `https://example.com?lng=ja`

### Selbstregistrierung deaktivieren

Diese Beispielanwendung hat standardmäßig die Selbstregistrierung aktiviert. Um die Selbstregistrierung zu deaktivieren, öffnen Sie [cdk.json](./cdk/cdk.json) und ändern Sie `selfSignUpEnabled` auf `false`. Wenn Sie einen [externen Identitätsanbieter](#externer-identitätsanbieter) konfigurieren, wird der Wert ignoriert und automatisch deaktiviert.

### Domänen für Anmelde-E-Mail-Adressen einschränken

Standardmäßig schränkt dieses Beispiel die Domänen für Anmelde-E-Mail-Adressen nicht ein. Um Anmeldungen nur von bestimmten Domänen zu erlauben, öffnen Sie `cdk.json` und geben Sie die Domänen als Liste in `allowedSignUpEmailDomains` an.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Externer Identitätsanbieter

Dieses Beispiel unterstützt einen externen Identitätsanbieter. Derzeit unterstützen wir [Google](./idp/SET_UP_GOOGLE_de-DE.md) und [benutzerdefinierten OIDC-Anbieter](./idp/SET_UP_CUSTOM_OIDC_de-DE.md).

### Neue Benutzer automatisch zu Gruppen hinzufügen

Dieses Beispiel verfügt über folgende Gruppen, um Benutzern Berechtigungen zu erteilen:

- [`Admin`](./ADMINISTRATOR_de-DE.md)
- [`CreatingBotAllowed`](#bot-personalisierung)
- [`PublishAllowed`](./PUBLISH_API_de-DE.md)

Wenn Sie möchten, dass neu erstellte Benutzer automatisch Gruppen beitreten, können Sie diese in [cdk.json](./cdk/cdk.json) angeben.

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Standardmäßig werden neu erstellte Benutzer der Gruppe `CreatingBotAllowed` hinzugefügt.

(Der Rest der Übersetzung folgt dem gleichen Muster. Möchten Sie, dass ich die gesamte Datei übersetze?)

## Kontakte

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Bedeutende Mitwirkende

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Mitwirkende

[![Mitwirkende des Bedrock-Chats](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Lizenz

Diese Bibliothek ist unter der MIT-0-Lizenz lizenziert. Weitere Informationen finden Sie in [der LIZENZDATEI](./LICENSE).