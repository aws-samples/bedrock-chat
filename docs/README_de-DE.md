<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Eine mehrsprachige generative KI-Plattform, die von [Amazon Bedrock](https://aws.amazon.com/bedrock/) betrieben wird.
Unterstützt Chat, benutzerdefinierte Bots mit Wissen (RAG), Bot-Sharing über einen Bot-Store und Aufgabenautomatisierung mittels Agenten.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 veröffentlicht. Bitte lesen Sie für ein Update sorgfältig die [Migrationsanleitung](./migration/V2_TO_V3_de-DE.md).** Ohne entsprechende Vorsicht **WERDEN BOTS AUS V2 UNBRAUCHBAR.**

### Bot-Personalisierung / Bot-Store

Fügen Sie Ihre eigenen Anweisungen und Wissen hinzu (auch bekannt als [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Der Bot kann über den Bot-Store-Marktplatz unter Anwendungsnutzern geteilt werden. Der angepasste Bot kann auch als eigenständige API veröffentlicht werden (Siehe [Details](./PUBLISH_API_de-DE.md)).

<details>
<summary>Screenshots</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Sie können auch bestehende [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/) importieren.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Aus Governance-Gründen können nur berechtigte Benutzer benutzerdefinierte Bots erstellen. Um die Erstellung von benutzerdefinierten Bots zu erlauben, muss der Benutzer Mitglied der Gruppe `CreatingBotAllowed` sein, die über die Management-Konsole > Amazon Cognito User pools oder aws cli eingerichtet werden kann. Beachten Sie, dass die User Pool ID über CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` eingesehen werden kann.

### Administrative Funktionen

API-Verwaltung, Markierung von Bots als essentiell, Analyse der Bot-Nutzung. [Details](./ADMINISTRATOR_de-DE.md)

<details>
<summary>Screenshots</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agent

Durch die Nutzung der [Agent-Funktionalität](./AGENT_de-DE.md) kann Ihr Chatbot automatisch komplexere Aufgaben bewältigen. Um beispielsweise eine Benutzerfrage zu beantworten, kann der Agent notwendige Informationen aus externen Tools abrufen oder die Aufgabe in mehrere Schritte zur Verarbeitung unterteilen.

<details>
<summary>Screenshots</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Supereinfache Bereitstellung

- Öffnen Sie in der Region us-east-1 [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Wählen Sie alle Modelle aus, die Sie nutzen möchten, und klicken Sie dann auf `Save changes`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

### Unterstützte Regionen

Bitte stellen Sie sicher, dass Sie Bedrock Chat in einer Region bereitstellen, [in der OpenSearch Serverless und Ingestion APIs verfügbar sind](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), wenn Sie Bots verwenden und Wissensdatenbanken erstellen möchten (OpenSearch Serverless ist die Standardwahl). Stand August 2025 werden folgende Regionen unterstützt: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Für den Parameter **bedrock-region** müssen Sie eine Region wählen, [in der Bedrock verfügbar ist](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Öffnen Sie [CloudShell](https://console.aws.amazon.com/cloudshell/home) in der Region, in der Sie die Bereitstellung durchführen möchten
- Führen Sie die Bereitstellung mit den folgenden Befehlen durch. Wenn Sie eine bestimmte Version bereitstellen oder Sicherheitsrichtlinien anwenden möchten, geben Sie bitte die entsprechenden Parameter aus [Optionale Parameter](#optional-parameters) an.

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Sie werden gefragt, ob Sie ein neuer Benutzer sind oder v3 verwenden. Wenn Sie kein bestehender Benutzer von v0 sind, geben Sie bitte `y` ein.

### Optionale Parameter

Sie können während der Bereitstellung die folgenden Parameter angeben, um die Sicherheit und Anpassung zu verbessern:

- **--disable-self-register**: Deaktiviert die Selbstregistrierung (Standard: aktiviert). Wenn dieser Flag gesetzt ist, müssen Sie alle Benutzer in Cognito erstellen und Benutzer können sich nicht selbst registrieren.
- **--enable-lambda-snapstart**: Aktiviert [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (Standard: deaktiviert). Wenn dieser Flag gesetzt ist, verbessert es die Kaltstartzeiten für Lambda-Funktionen und bietet schnellere Antwortzeiten für eine bessere Benutzererfahrung.
- **--ipv4-ranges**: Kommagetrennte Liste erlaubter IPv4-Bereiche. (Standard: alle IPv4-Adressen erlaubt)
- **--ipv6-ranges**: Kommagetrennte Liste erlaubter IPv6-Bereiche. (Standard: alle IPv6-Adressen erlaubt)
- **--disable-ipv6**: Deaktiviert Verbindungen über IPv6. (Standard: aktiviert)
- **--allowed-signup-email-domains**: Kommagetrennte Liste erlaubter E-Mail-Domains für die Registrierung. (Standard: keine Domain-Einschränkung)
- **--bedrock-region**: Definiert die Region, in der Bedrock verfügbar ist. (Standard: us-east-1)
- **--repo-url**: Das benutzerdefinierte Repository von Bedrock Chat für die Bereitstellung, falls geforkt oder mit benutzerdefinierten Quellcode. (Standard: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Die Version von Bedrock Chat, die bereitgestellt werden soll. (Standard: neueste Version in Entwicklung)
- **--cdk-json-override**: Sie können während der Bereitstellung beliebige CDK-Kontextwerte mit dem Override-JSON-Block überschreiben. Dies ermöglicht die Änderung der Konfiguration ohne direkte Bearbeitung der cdk.json-Datei.

Beispielverwendung:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

Das Override-JSON muss der gleichen Struktur wie cdk.json folgen. Sie können beliebige Kontextwerte überschreiben, einschließlich:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: akzeptiert eine Liste von Modell-IDs zur Aktivierung. Der Standardwert ist eine leere Liste, die alle Modelle aktiviert.
- `logoPath`: relativer Pfad zum Logo-Asset innerhalb des Frontend `public/` Verzeichnisses, das oben in der Navigationsleiste erscheint.
- Und andere in cdk.json definierte Kontextwerte

> [!Note]
> Die Override-Werte werden während der Bereitstellungszeit im AWS Code Build mit der bestehenden cdk.json-Konfiguration zusammengeführt. Die im Override angegebenen Werte haben Vorrang vor den Werten in cdk.json.

#### Beispielbefehl mit Parametern:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Nach etwa 35 Minuten erhalten Sie die folgende Ausgabe, auf die Sie über Ihren Browser zugreifen können

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Der Anmeldebildschirm erscheint wie oben gezeigt, wo Sie Ihre E-Mail registrieren und sich anmelden können.

> [!Important]
> Ohne Einstellung der optionalen Parameter erlaubt diese Bereitstellungsmethode jedem, der die URL kennt, sich zu registrieren. Für den Produktionseinsatz wird dringend empfohlen, IP-Adressbeschränkungen hinzuzufügen und die Selbstregistrierung zu deaktivieren, um Sicherheitsrisiken zu minimieren (Sie können allowed-signup-email-domains definieren, um Benutzer so einzuschränken, dass sich nur E-Mail-Adressen aus der Domain Ihres Unternehmens registrieren können). Verwenden Sie sowohl ipv4-ranges als auch ipv6-ranges für IP-Adressbeschränkungen und deaktivieren Sie die Selbstregistrierung mit disable-self-register bei der Ausführung von ./bin.

> [!TIP]
> Wenn die `Frontend URL` nicht erscheint oder Bedrock Chat nicht richtig funktioniert, könnte es ein Problem mit der neuesten Version sein. Fügen Sie in diesem Fall `--version "v3.0.0"` zu den Parametern hinzu und versuchen Sie die Bereitstellung erneut.

## Architektur

Es handelt sich um eine auf AWS-verwalteten Diensten aufgebaute Architektur, die keine Infrastrukturverwaltung erfordert. Durch die Nutzung von Amazon Bedrock ist keine Kommunikation mit APIs außerhalb von AWS erforderlich. Dies ermöglicht die Bereitstellung skalierbarer, zuverlässiger und sicherer Anwendungen.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL-Datenbank zur Speicherung des Gesprächsverlaufs
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend-API-Endpunkt ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Frontend-Anwendungsbereitstellung ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP-Adressbeschränkung
- [Amazon Cognito](https://aws.amazon.com/cognito/): Benutzerauthentifizierung
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Verwalteter Dienst zur Nutzung von Grundlagenmodellen über APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Bietet eine verwaltete Schnittstelle für Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) und Dienste für das Einbetten und Parsen von Dokumenten
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Empfang von Events aus dem DynamoDB-Stream und Start von Step Functions zum Einbetten externen Wissens
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrierung der Ingestion-Pipeline zum Einbetten externen Wissens in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Dient als Backend-Datenbank für Bedrock Knowledge Bases, bietet Volltextsuche und Vektorsuche und ermöglicht die genaue Abrufung relevanter Informationen
- [Amazon Athena](https://aws.amazon.com/athena/): Abfragedienst zur Analyse von S3-Buckets

![](./imgs/arch.png)

## Deployment mit CDK

Die besonders einfache Deployment-Methode verwendet intern [AWS CodeBuild](https://aws.amazon.com/codebuild/) für das Deployment via CDK. Dieser Abschnitt beschreibt das Verfahren für die direkte Deployment mit CDK.

- Bitte stellen Sie sicher, dass UNIX, Docker und eine Node.js-Laufzeitumgebung vorhanden sind.

> [!Important]
> Wenn während des Deployments nicht genügend Speicherplatz in der lokalen Umgebung verfügbar ist, kann das CDK-Bootstrapping zu einem Fehler führen. Wir empfehlen, die Volume-Größe der Instanz vor dem Deployment zu erweitern.

- Klonen Sie dieses Repository

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Installieren Sie die npm-Pakete

```
cd bedrock-chat
cd cdk
npm ci
```

- Bei Bedarf bearbeiten Sie die folgenden Einträge in [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Region, in der Bedrock verfügbar ist. **HINWEIS: Bedrock unterstützt derzeit NICHT alle Regionen.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Erlaubte IP-Adressbereiche.
  - `enableLambdaSnapStart`: Standardmäßig true. Auf false setzen, wenn das Deployment in einer [Region erfolgt, die Lambda SnapStart für Python-Funktionen nicht unterstützt](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Standardmäßig alle. Wenn gesetzt (Liste von Modell-IDs), steuert global, welche Modelle in Dropdown-Menüs über alle Chats für alle Benutzer und während der Bot-Erstellung in der Bedrock Chat-Anwendung erscheinen.
  - `logoPath`: Relativer Pfad unter `frontend/public`, der auf das Bild zeigt, das oben in der Anwendungsleiste angezeigt wird.
Die folgenden Modell-IDs werden unterstützt (bitte stellen Sie sicher, dass diese auch in der Bedrock-Konsole unter Model access in Ihrer Deployment-Region aktiviert sind):
- **Claude Models:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Amazon Nova Models:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Mistral Models:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **DeepSeek Models:** `deepseek-r1`
- **Meta Llama Models:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

Die vollständige Liste finden Sie in [index.ts](./frontend/src/constants/index.ts).

- Vor dem Deployment des CDK müssen Sie einmalig das Bootstrap für die Region durchführen, in der Sie deployen möchten.

```
npx cdk bootstrap
```

- Deployen Sie dieses Beispielprojekt

```
npx cdk deploy --require-approval never --all
```

- Sie erhalten eine ähnliche Ausgabe wie die folgende. Die URL der Web-App wird in `BedrockChatStack.FrontendURL` ausgegeben, bitte rufen Sie diese in Ihrem Browser auf.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Parameter definieren

Sie können Parameter für Ihr Deployment auf zwei Arten definieren: mit `cdk.json` oder mit der typsicheren `parameter.ts`-Datei.

#### Verwendung von cdk.json (Traditionelle Methode)

Die traditionelle Art, Parameter zu konfigurieren, ist die Bearbeitung der `cdk.json`-Datei. Dieser Ansatz ist einfach, bietet aber keine Typenprüfung:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
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
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Parameter für zusätzliche Umgebungen definieren
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Kosteneinsparung für Entwicklungsumgebung
  enableBotStoreReplicas: false, // Kosteneinsparung für Entwicklungsumgebung
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Verbesserte Verfügbarkeit für Produktion
  enableBotStoreReplicas: true, // Verbesserte Verfügbarkeit für Produktion
});
```

> [!Note]
> Bestehende Benutzer können `cdk.json` weiterhin ohne Änderungen verwenden. Der `parameter.ts`-Ansatz wird für neue Deployments oder bei der Verwaltung mehrerer Umgebungen empfohlen.

### Deployment mehrerer Umgebungen

Sie können mehrere Umgebungen aus demselben Codebase mit der `parameter.ts`-Datei und der Option `-c envName` deployen.

#### Voraussetzungen

1. Definieren Sie Ihre Umgebungen in `parameter.ts` wie oben gezeigt
2. Jede Umgebung wird ihre eigenen Ressourcen mit umgebungsspezifischen Präfixen haben

#### Deployment-Befehle

Um eine bestimmte Umgebung zu deployen:

```bash
# Deployment der Entwicklungsumgebung
npx cdk deploy --all -c envName=dev

# Deployment der Produktionsumgebung
npx cdk deploy --all -c envName=prod
```

Wenn keine Umgebung angegeben wird, wird die "default"-Umgebung verwendet:

```bash
# Deployment der Standardumgebung
npx cdk deploy --all
```

#### Wichtige Hinweise

1. **Stack-Benennung**:

   - Die Hauptstacks für jede Umgebung werden mit dem Umgebungsnamen präfixiert (z.B. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Allerdings erhalten benutzerdefinierte Bot-Stacks (`BrChatKbStack*`) und API-Publishing-Stacks (`ApiPublishmentStack*`) keine Umgebungspräfixe, da sie zur Laufzeit dynamisch erstellt werden

2. **Ressourcen-Benennung**:

   - Nur einige Ressourcen erhalten Umgebungspräfixe in ihren Namen (z.B. `dev_ddb_export` Tabelle, `dev-FrontendWebAcl`)
   - Die meisten Ressourcen behalten ihre ursprünglichen Namen bei, sind aber durch die Zugehörigkeit zu verschiedenen Stacks isoliert

3. **Umgebungsidentifikation**:

   - Alle Ressourcen werden mit einem `CDKEnvironment`-Tag versehen, der den Umgebungsnamen enthält
   - Sie können diesen Tag verwenden, um zu identifizieren, zu welcher Umgebung eine Ressource gehört
   - Beispiel: `CDKEnvironment: dev` oder `CDKEnvironment: prod`

4. **Überschreiben der Standardumgebung**: Wenn Sie eine "default"-Umgebung in `parameter.ts` definieren, überschreibt diese die Einstellungen in `cdk.json`. Um `cdk.json` weiterhin zu verwenden, definieren Sie keine "default"-Umgebung in `parameter.ts`.

5. **Umgebungsanforderungen**: Um andere Umgebungen als "default" zu erstellen, müssen Sie `parameter.ts` verwenden. Die Option `-c envName` allein reicht ohne entsprechende Umgebungsdefinitionen nicht aus.

6. **Ressourcenisolierung**: Jede Umgebung erstellt ihre eigenen Ressourcen, sodass Sie Entwicklungs-, Test- und Produktionsumgebungen im selben AWS-Konto ohne Konflikte haben können.

## Sonstiges

Sie können Parameter für Ihr Deployment auf zwei Arten definieren: über `cdk.json` oder über die typsichere `parameter.ts` Datei.

#### Verwendung von cdk.json (Traditionelle Methode)

Die traditionelle Art, Parameter zu konfigurieren, erfolgt durch Bearbeitung der `cdk.json` Datei. Dieser Ansatz ist einfach, bietet aber keine Typenprüfung:

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

Für bessere Typsicherheit und Entwicklererfahrung können Sie die `parameter.ts` Datei verwenden, um Ihre Parameter zu definieren:

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Bestehende Benutzer können `cdk.json` weiterhin ohne Änderungen verwenden. Der `parameter.ts` Ansatz wird für neue Deployments oder bei der Verwaltung mehrerer Umgebungen empfohlen.

### Deployment mehrerer Umgebungen

Sie können mehrere Umgebungen aus demselben Quellcode mithilfe der `parameter.ts` Datei und der Option `-c envName` deployen.

#### Voraussetzungen

1. Definieren Sie Ihre Umgebungen in `parameter.ts` wie oben gezeigt
2. Jede Umgebung wird über eigene Ressourcen mit umgebungsspezifischen Präfixen verfügen

#### Deployment-Befehle

So deployen Sie eine bestimmte Umgebung:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Wenn keine Umgebung angegeben wird, wird die "default"-Umgebung verwendet:

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Wichtige Hinweise

1. **Stack-Benennung**:

   - Die Haupt-Stacks für jede Umgebung erhalten ein Präfix mit dem Umgebungsnamen (z.B. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Allerdings erhalten Custom Bot Stacks (`BrChatKbStack*`) und API-Publishing-Stacks (`ApiPublishmentStack*`) keine Umgebungspräfixe, da sie zur Laufzeit dynamisch erstellt werden

2. **Ressourcen-Benennung**:

   - Nur einige Ressourcen erhalten Umgebungspräfixe in ihren Namen (z.B. `dev_ddb_export` Tabelle, `dev-FrontendWebAcl`)
   - Die meisten Ressourcen behalten ihre ursprünglichen Namen bei, sind aber durch verschiedene Stacks isoliert

3. **Umgebungsidentifikation**:

   - Alle Ressourcen werden mit einem `CDKEnvironment`-Tag versehen, der den Umgebungsnamen enthält
   - Sie können diesen Tag verwenden, um zu identifizieren, zu welcher Umgebung eine Ressource gehört
   - Beispiel: `CDKEnvironment: dev` oder `CDKEnvironment: prod`

4. **Standard-Umgebungs-Override**: Wenn Sie eine "default"-Umgebung in `parameter.ts` definieren, überschreibt diese die Einstellungen in `cdk.json`. Um `cdk.json` weiterhin zu verwenden, definieren Sie keine "default"-Umgebung in `parameter.ts`.

5. **Umgebungsanforderungen**: Um andere Umgebungen als "default" zu erstellen, müssen Sie `parameter.ts` verwenden. Die Option `-c envName` allein reicht ohne entsprechende Umgebungsdefinitionen nicht aus.

6. **Ressourcenisolierung**: Jede Umgebung erstellt ihre eigenen Ressourcen, sodass Sie Entwicklungs-, Test- und Produktionsumgebungen im selben AWS-Konto ohne Konflikte haben können.

## Sonstiges

### Ressourcen entfernen

Bei Verwendung von CLI und CDK bitte `npx cdk destroy` ausführen. Andernfalls greifen Sie auf [CloudFormation](https://console.aws.amazon.com/cloudformation/home) zu und löschen Sie `BedrockChatStack` und `FrontendWafStack` manuell. Bitte beachten Sie, dass sich `FrontendWafStack` in der Region `us-east-1` befindet.

### Spracheinstellungen

Dieses Asset erkennt die Sprache automatisch mit [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Sie können die Sprache über das Anwendungsmenü wechseln. Alternativ können Sie die Sprache auch über Query String wie unten gezeigt festlegen.

> `https://example.com?lng=ja`

### Selbstregistrierung deaktivieren

Diese Beispielanwendung hat die Selbstregistrierung standardmäßig aktiviert. Um die Selbstregistrierung zu deaktivieren, öffnen Sie [cdk.json](./cdk/cdk.json) und setzen Sie `selfSignUpEnabled` auf `false`. Wenn Sie einen [externen Identitätsanbieter](#external-identity-provider) konfigurieren, wird dieser Wert ignoriert und automatisch deaktiviert.

### Domains für Registrierungs-E-Mail-Adressen einschränken

Standardmäßig schränkt dieses Beispiel die Domains für Registrierungs-E-Mail-Adressen nicht ein. Um Registrierungen nur von bestimmten Domains zu erlauben, öffnen Sie `cdk.json` und geben Sie die Domains als Liste in `allowedSignUpEmailDomains` an.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Externer Identitätsanbieter

Dieses Beispiel unterstützt externe Identitätsanbieter. Derzeit unterstützen wir [Google](./idp/SET_UP_GOOGLE_de-DE.md) und [benutzerdefinierte OIDC-Provider](./idp/SET_UP_CUSTOM_OIDC_de-DE.md).

### Optionale Frontend WAF

Für CloudFront-Distributionen müssen AWS WAF WebACLs in der Region us-east-1 erstellt werden. In manchen Organisationen ist das Erstellen von Ressourcen außerhalb der primären Region durch Richtlinien eingeschränkt. In solchen Umgebungen kann die CDK-Bereitstellung fehlschlagen, wenn versucht wird, die Frontend WAF in us-east-1 bereitzustellen.

Um diese Einschränkungen zu berücksichtigen, ist der Frontend WAF Stack optional. Wenn deaktiviert, wird die CloudFront-Distribution ohne WebACL bereitgestellt. Das bedeutet, dass Sie keine IP-Allow/Deny-Kontrollen am Frontend-Edge haben. Authentifizierung und alle anderen Anwendungskontrollen funktionieren wie gewohnt weiter. Beachten Sie, dass diese Einstellung nur die Frontend WAF (CloudFront-Scope) betrifft; die Published API WAF (regional) bleibt unberührt.

Um die Frontend WAF zu deaktivieren, setzen Sie Folgendes in `parameter.ts` (Empfohlene typsichere Methode):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Oder wenn Sie das Legacy `cdk/cdk.json` verwenden, setzen Sie:

```json
"enableFrontendWaf": false
```

### Neue Benutzer automatisch zu Gruppen hinzufügen

Dieses Beispiel hat die folgenden Gruppen, um Benutzern Berechtigungen zu geben:

- [`Admin`](./ADMINISTRATOR_de-DE.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_de-DE.md)

Wenn Sie möchten, dass neu erstellte Benutzer automatisch Gruppen beitreten, können Sie diese in [cdk.json](./cdk/cdk.json) angeben.

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Standardmäßig werden neu erstellte Benutzer der Gruppe `CreatingBotAllowed` hinzugefügt.

### RAG-Replikate konfigurieren

`enableRagReplicas` ist eine Option in [cdk.json](./cdk/cdk.json), die die Replikateinstellungen für die RAG-Datenbank steuert, insbesondere die Knowledge Bases mit Amazon OpenSearch Serverless.

- **Standard**: true
- **true**: Verbessert die Verfügbarkeit durch Aktivierung zusätzlicher Replikate, was für Produktionsumgebungen geeignet ist, aber die Kosten erhöht.
- **false**: Reduziert die Kosten durch weniger Replikate, was für Entwicklung und Tests geeignet ist.

Dies ist eine Einstellung auf Account/Region-Ebene, die die gesamte Anwendung und nicht einzelne Bots betrifft.

> [!Note]
> Ab Juni 2024 unterstützt Amazon OpenSearch Serverless 0,5 OCU, was die Einstiegskosten für kleine Workloads senkt. Produktionsbereitstellungen können mit 2 OCUs beginnen, während Entwicklungs-/Testworkloads 1 OCU verwenden können. OpenSearch Serverless skaliert automatisch basierend auf Workload-Anforderungen. Weitere Details finden Sie in der [Ankündigung](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Bot Store konfigurieren

Die Bot Store-Funktion ermöglicht es Benutzern, benutzerdefinierte Bots zu teilen und zu entdecken. Sie können den Bot Store über die folgenden Einstellungen in [cdk.json](./cdk/cdk.json) konfigurieren:

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Steuert, ob die Bot Store-Funktion aktiviert ist (Standard: `true`)
- **botStoreLanguage**: Legt die Hauptsprache für Bot-Suche und -Entdeckung fest (Standard: `"en"`). Dies beeinflusst, wie Bots im Bot Store indiziert und durchsucht werden, und optimiert die Textanalyse für die angegebene Sprache.
- **enableBotStoreReplicas**: Steuert, ob Standby-Replikate für die vom Bot Store verwendete OpenSearch Serverless-Sammlung aktiviert sind (Standard: `false`). Die Einstellung auf `true` verbessert die Verfügbarkeit, erhöht aber die Kosten, während `false` die Kosten reduziert, aber die Verfügbarkeit beeinträchtigen kann.
  > **Wichtig**: Sie können diese Eigenschaft nicht aktualisieren, nachdem die Sammlung bereits erstellt wurde. Wenn Sie versuchen, diese Eigenschaft zu ändern, verwendet die Sammlung weiterhin den ursprünglichen Wert.

### Cross-Region und Global Inference

[Cross-Region und Global Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ermöglicht es Amazon Bedrock, Modellinferenz-Anfragen dynamisch über mehrere AWS-Regionen zu leiten, was den Durchsatz und die Widerstandsfähigkeit während Spitzenlastzeiten verbessert. Global Inference leitet die Anfragen basierend auf Latenz und Verfügbarkeit weltweit an die optimale Region weiter, während Cross-Region Inference Anfragen innerhalb derselben AWS-Region leitet, zum Beispiel innerhalb der USA. Einige SCPs können das eine oder andere oder beides einschränken, daher können Sie sie unabhängig voneinander konfigurieren. Standardmäßig sind beide aktiviert.

Um die Konfiguration zu ändern, ändern Sie die folgenden Einstellungen in `cdk.json` oder `parameters.ts`:

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) verbessert die Kaltstartzeiten für Lambda-Funktionen und bietet schnellere Antwortzeiten für eine bessere Benutzererfahrung. Für Python-Funktionen gibt es allerdings eine [Gebühr abhängig von der Cache-Größe](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) und ist [derzeit nicht in allen Regionen verfügbar](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions). Um SnapStart zu deaktivieren, bearbeiten Sie `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Benutzerdefinierte Domain konfigurieren

Sie können eine benutzerdefinierte Domain für die CloudFront-Distribution konfigurieren, indem Sie die folgenden Parameter in [cdk.json](./cdk/cdk.json) setzen:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Der benutzerdefinierte Domainname für Ihre Chat-Anwendung (z.B. chat.example.com)
- `hostedZoneId`: Die ID Ihrer Route 53 Hosted Zone, in der die Domain-Einträge erstellt werden

Wenn diese Parameter angegeben werden, wird die Bereitstellung automatisch:

- Ein ACM-Zertifikat mit DNS-Validierung in der Region us-east-1 erstellen
- Die notwendigen DNS-Einträge in Ihrer Route 53 Hosted Zone erstellen
- CloudFront für die Verwendung Ihrer benutzerdefinierten Domain konfigurieren

> [!Note]
> Die Domain muss von Route 53 in Ihrem AWS-Account verwaltet werden. Die Hosted Zone ID finden Sie in der Route 53-Konsole.

### Erlaubte Länder konfigurieren (Geo-Beschränkung)

Sie können den Zugriff auf Bedrock-Chat basierend auf dem Land, aus dem der Client zugreift, einschränken.
Verwenden Sie den Parameter `allowedCountries` in [cdk.json](./cdk/cdk.json), der eine Liste von [ISO-3166 Länder-Codes](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) akzeptiert.
Ein Unternehmen aus Neuseeland könnte zum Beispiel entscheiden, dass nur IP-Adressen aus Neuseeland (NZ) und Australien (AU) auf das Portal zugreifen dürfen und allen anderen der Zugriff verweigert wird.
Um dieses Verhalten zu konfigurieren, verwenden Sie die folgende Einstellung in [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Oder mit `parameter.ts` (Empfohlene typsichere Methode):

```ts
// Parameter für die Standardumgebung definieren
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### IPv6-Unterstützung deaktivieren

Das Frontend erhält standardmäßig sowohl IP- als auch IPv6-Adressen. In seltenen
Fällen müssen Sie möglicherweise die IPv6-Unterstützung explizit deaktivieren. Setzen Sie
dazu den folgenden Parameter in [parameter.ts](./cdk/parameter.ts) oder ähnlich in [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Wenn nicht gesetzt, ist die IPv6-Unterstützung standardmäßig aktiviert.

### Lokale Entwicklung

Siehe [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_de-DE.md).

### Mitwirkung

Vielen Dank, dass Sie erwägen, zu diesem Repository beizutragen! Wir begrüßen Fehlerbehebungen, Sprachübersetzungen (i18n), Funktionsverbesserungen, [Agent-Tools](./docs/AGENT.md#how-to-develop-your-own-tools) und andere Verbesserungen.

Für Funktionsverbesserungen und andere Verbesserungen **würden wir es sehr schätzen, wenn Sie vor der Erstellung eines Pull Requests ein Feature Request Issue erstellen könnten, um den Implementierungsansatz und die Details zu diskutieren. Für Fehlerbehebungen und Sprachübersetzungen (i18n) können Sie direkt einen Pull Request erstellen.**

Bitte beachten Sie auch die folgenden Richtlinien vor dem Beitragen:

- [Lokale Entwicklung](./LOCAL_DEVELOPMENT_de-DE.md)
- [CONTRIBUTING](./CONTRIBUTING_de-DE.md)

## Kontakte

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Wichtige Mitwirkende

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Mitwirkende

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Lizenz

Diese Bibliothek steht unter der MIT-0 Lizenz. Siehe [die LICENSE-Datei](./LICENSE).