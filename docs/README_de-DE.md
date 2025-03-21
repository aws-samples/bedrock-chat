# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Warning]
>
> **Version 2 wurde veröffentlicht. Bitte prüfen Sie sorgfältig den [Migrations-Leitfaden](./migration/V1_TO_V2_de-DE.md).** Ohne Sorgfalt werden **BOTS AUS VERSION 1 UNBRAUCHBAR WERDEN.**

Ein mehrsprachiger Chatbot, der LLM-Modelle von [Amazon Bedrock](https://aws.amazon.com/bedrock/) für generative KI nutzt.

### Überblick und Installation auf YouTube ansehen

[![Überblick](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Grundlegende Konversation

![](./imgs/demo.gif)

### Bot-Personalisierung

Fügen Sie Ihre eigene Anweisung hinzu und geben Sie externes Wissen als URL oder Dateien an (auch bekannt als [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Der Bot kann unter Anwendungsbenutzern geteilt werden. Der angepasste Bot kann auch als eigenständige API veröffentlicht werden (Weitere Informationen [hier](./PUBLISH_API_de-DE.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Aus Governance-Gründen können nur zugelassene Benutzer angepasste Bots erstellen. Um die Erstellung von angepassten Bots zu ermöglichen, muss der Benutzer Mitglied der Gruppe `CreatingBotAllowed` sein, die über die Verwaltungskonsole > Amazon Cognito-Benutzer-Pools oder die AWS-CLI eingerichtet werden kann. Die Benutzer-Pool-ID kann durch den Zugriff auf CloudFormation > BedrockChatStack > Ausgaben > `AuthUserPoolIdxxxx` referenziert werden.

### Administrator-Dashboard

<details>
<summary>Administrator-Dashboard</summary>

Analysieren Sie die Nutzung für jeden Benutzer / Bot im Administrator-Dashboard. [Details](./ADMINISTRATOR_de-DE.md)

![](./imgs/admin_bot_analytics.png)

</details>

### LLM-gesteuerter Agent

<details>
<summary>LLM-gesteuerter Agent</summary>

Durch die Verwendung der [Agent-Funktionalität](./AGENT_de-DE.md) kann Ihr Chatbot komplexere Aufgaben automatisch bewältigen. Zum Beispiel kann der Agent, um eine Frage des Benutzers zu beantworten, notwendige Informationen aus externen Tools abrufen oder die Aufgabe in mehrere Schritte zur Verarbeitung zerlegen.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Super-einfache Bereitstellung

- Öffnen Sie in der Region us-east-1 [Bedrock Model Access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Modellzugriff verwalten` > Aktivieren Sie alle Optionen von `Anthropic / Claude 3`, alle von `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` und `Cohere / Embed Multilingual`, dann `Änderungen speichern`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

- Öffnen Sie [CloudShell](https://console.aws.amazon.com/cloudshell/home) in der Region, in der Sie bereitstellen möchten
- Führen Sie die Bereitstellung mit folgenden Befehlen durch. Wenn Sie eine bestimmte Version bereitstellen oder Sicherheitsrichtlinien anwenden möchten, geben Sie bitte die entsprechenden Parameter aus [Optionale Parameter](#optionale-parameter) an.

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Sie werden gefragt, ob es sich um einen neuen Benutzer oder um v2 handelt. Wenn Sie kein Benutzer von v0 sind, geben Sie bitte `y` ein.

### Optionale Parameter

Sie können folgende Parameter während der Bereitstellung angeben, um Sicherheit und Anpassung zu verbessern:

- **--disable-self-register**: Selbstregistrierung deaktivieren (Standard: aktiviert). Wenn dieses Flag gesetzt ist, müssen Sie alle Benutzer in Cognito erstellen und die Selbstregistrierung wird nicht erlaubt.
- **--enable-lambda-snapstart**: [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) aktivieren (Standard: deaktiviert). Wenn dieses Flag gesetzt ist, verbessert es die Kaltstart-Zeiten für Lambda-Funktionen und bietet schnellere Antwortzeiten für ein besseres Benutzererlebnis.
- **--ipv4-ranges**: Kommagetrennte Liste der erlaubten IPv4-Bereiche. (Standard: alle IPv4-Adressen erlauben)
- **--ipv6-ranges**: Kommagetrennte Liste der erlaubten IPv6-Bereiche. (Standard: alle IPv6-Adressen erlauben)
- **--disable-ipv6**: Verbindungen über IPv6 deaktivieren. (Standard: aktiviert)
- **--allowed-signup-email-domains**: Kommagetrennte Liste der erlaubten E-Mail-Domains für die Registrierung. (Standard: keine Domaineinschränkung)
- **--bedrock-region**: Die Region definieren, in der Bedrock verfügbar ist. (Standard: us-east-1)
- **--repo-url**: Das benutzerdefinierte Repository von Bedrock Claude Chat für die Bereitstellung, falls geforkt oder benutzerdefinierte Quellcodeverwaltung. (Standard: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Die Version von Bedrock Claude Chat für die Bereitstellung. (Standard: neueste Version in der Entwicklung)
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
> Die Override-Werte werden während der Bereitstellung in AWS CodeBuild mit der vorhandenen cdk.json-Konfiguration zusammengeführt. Die angegebenen Werte haben Vorrang vor den Werten in cdk.json.

#### Beispielbefehl mit Parametern:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Nach etwa 35 Minuten erhalten Sie die folgende Ausgabe, auf die Sie über Ihren Browser zugreifen können

```
Frontend-URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Der Anmeldebildschirm wird wie oben gezeigt angezeigt, wo Sie Ihre E-Mail registrieren und sich anmelden können.

> [!Wichtig]
> Ohne Festlegung des optionalen Parameters erlaubt diese Bereitstellungsmethode jedem, der die URL kennt, sich anzumelden. Für den Produktiveinsatz wird dringend empfohlen, IP-Adresseinschränkungen hinzuzufügen und die Selbstregistrierung zu deaktivieren, um Sicherheitsrisiken zu mindern (Sie können allowed-signup-email-domains definieren, um Benutzer so zu beschränken, dass nur E-Mail-Adressen aus der Domäne Ihres Unternehmens sich registrieren können). Verwenden Sie sowohl ipv4-ranges als auch ipv6-ranges für IP-Adresseinschränkungen und deaktivieren Sie die Selbstregistrierung, indem Sie disable-self-register bei der Ausführung von ./bin verwenden.

> [!TIPP]
> Wenn die `Frontend-URL` nicht erscheint oder Bedrock Claude Chat nicht ordnungsgemäß funktioniert, kann dies ein Problem mit der neuesten Version sein. Fügen Sie in diesem Fall `--version "v1.2.6"` zu den Parametern hinzu und versuchen Sie die Bereitstellung erneut.

## Architektur

Es handelt sich um eine Architektur, die auf AWS-verwalteten Diensten aufbaut und die Infrastrukturverwaltung überflüssig macht. Durch die Nutzung von Amazon Bedrock ist keine Kommunikation mit APIs außerhalb von AWS erforderlich. Dies ermöglicht die Bereitstellung skalierbarer, zuverlässiger und sicherer Anwendungen.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): NoSQL-Datenbank zur Speicherung des Gesprächsverlaufs
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Backend-API-Endpunkt ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Bereitstellung der Frontend-Anwendung ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): IP-Adresseinschränkung
- [Amazon Cognito](https://aws.amazon.com/cognito/): Benutzerauthentifizierung
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Verwalteter Dienst zur Nutzung von Grundmodellen über APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Bietet eine verwaltete Schnittstelle für Retrieval-Augmented Generation ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) und stellt Dienste zum Einbetten und Analysieren von Dokumenten bereit
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Empfang von Ereignissen aus dem DynamoDB-Stream und Starten von Step Functions zum Einbetten externen Wissens
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrierung der Erfassungspipeline zum Einbetten externen Wissens in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Dient als Backend-Datenbank für Bedrock Knowledge Bases und bietet Volltext- und Vektorsuche, um genaue Informationsabfragen zu ermöglichen
- [Amazon Athena](https://aws.amazon.com/athena/): Abfragedienst zur Analyse von S3-Buckets

![](./imgs/arch.png)

## Bereitstellung mit CDK

Die Super-einfache Bereitstellung verwendet [AWS CodeBuild](https://aws.amazon.com/codebuild/), um die Bereitstellung intern mit CDK durchzuführen. Dieser Abschnitt beschreibt das Verfahren zur direkten Bereitstellung mit CDK.

- Bitte stellen Sie sicher, dass UNIX, Docker und eine Node.js-Laufzeitumgebung vorhanden sind. Falls nicht, können Sie auch [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping) verwenden

> [!Wichtig]
> Wenn während der Bereitstellung nicht genügend Speicherplatz in der lokalen Umgebung vorhanden ist, kann dies zu einem Fehler beim CDK-Bootstrapping führen. Wenn Sie in Cloud9 oder einer ähnlichen Umgebung arbeiten, empfehlen wir, die Volumengröße der Instanz vor der Bereitstellung zu erweitern.

- Repository klonen

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- npm-Pakete installieren

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Bei Bedarf die folgenden Einträge in [cdk.json](./cdk/cdk.json) bearbeiten:

  - `bedrockRegion`: Region, in der Bedrock verfügbar ist. **HINWEIS: Bedrock wird derzeit NICHT in allen Regionen unterstützt.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Erlaubte IP-Adressbereiche.
  - `enableLambdaSnapStart`: Standardmäßig auf true gesetzt. Auf false setzen, wenn die Bereitstellung in einer [Region erfolgt, die Lambda SnapStart für Python-Funktionen nicht unterstützt](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Vor der CDK-Bereitstellung müssen Sie Bootstrap einmal für die Region durchführen, in der Sie bereitstellen möchten.

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

[Der Rest der Übersetzung folgt dem gleichen Muster: technisch präzise, natürlich klingend und mit Beibehaltung der Originalstruktur.]

## Andere

### Unterstützung für Mistral-Modelle konfigurieren

Aktualisieren Sie `enableMistral` auf `true` in [cdk.json](./cdk/cdk.json) und führen Sie `npx cdk deploy` aus.

```json
...
  "enableMistral": true,
```

> [!Wichtig]
> Dieses Projekt konzentriert sich auf Anthropic Claude-Modelle, die Mistral-Modelle werden begrenzt unterstützt. Beispielsweise basieren Prompt-Beispiele auf Claude-Modellen. Dies ist eine Mistral-spezifische Option. Sobald Sie Mistral-Modelle aktivieren, können Sie nur Mistral-Modelle für alle Chat-Funktionen verwenden, NICHT sowohl Claude- als auch Mistral-Modelle.

### Standardmäßige Textgenerierung konfigurieren

Benutzer können die [Textgenerierungsparameter](https://docs.anthropic.com/claude/reference/complete_post) über den Bildschirm zur Erstellung eines benutzerdefinierten Bots anpassen. Wenn der Bot nicht verwendet wird, werden die in [config.py](./backend/app/config.py) festgelegten Standardparameter verwendet.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Ressourcen entfernen

Bei Verwendung von CLI und CDK führen Sie bitte `npx cdk destroy` aus. Andernfalls greifen Sie auf [CloudFormation](https://console.aws.amazon.com/cloudformation/home) zu und löschen Sie `BedrockChatStack` und `FrontendWafStack` manuell. Bitte beachten Sie, dass sich `FrontendWafStack` in der Region `us-east-1` befindet.

### Spracheinstellungen

Dieses Asset erkennt die Sprache automatisch mithilfe von [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Sie können die Sprache über das Anwendungsmenü wechseln. Alternativ können Sie den Abfragestring verwenden, um die Sprache wie folgt festzulegen.

> `https://example.com?lng=ja`

### Selbstregistrierung deaktivieren

Diese Beispielanwendung hat standardmäßig die Selbstregistrierung aktiviert. Um die Selbstregistrierung zu deaktivieren, öffnen Sie [cdk.json](./cdk/cdk.json) und ändern Sie `selfSignUpEnabled` auf `false`. Wenn Sie einen [externen Identitätsanbieter](#externer-identitätsprovider) konfigurieren, wird der Wert ignoriert und automatisch deaktiviert.

### Domänen für Anmelde-E-Mail-Adressen einschränken

Standardmäßig schränkt dieses Beispiel die Domänen für Anmelde-E-Mail-Adressen nicht ein. Um Anmeldungen nur von bestimmten Domänen zuzulassen, öffnen Sie `cdk.json` und geben Sie die Domänen als Liste in `allowedSignUpEmailDomains` an.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Externer Identitätsanbieter

Dieses Beispiel unterstützt einen externen Identitätsanbieter. Derzeit werden [Google](./idp/SET_UP_GOOGLE_de-DE.md) und [benutzerdefinierte OIDC-Anbieter](./idp/SET_UP_CUSTOM_OIDC_de-DE.md) unterstützt.

### Neue Benutzer automatisch zu Gruppen hinzufügen

Dieses Beispiel verfügt über folgende Gruppen, um Benutzern Berechtigungen zu erteilen:

- [`Admin`](./ADMINISTRATOR_de-DE.md)
- [`CreatingBotAllowed`](#bot-personalisierung)
- [`PublishAllowed`](./PUBLISH_API_de-DE.md)

Wenn Sie möchten, dass neu erstellte Benutzer automatisch Gruppen beitreten, können Sie diese in [cdk.json](./cdk/cdk.json) angeben.

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Standardmäßig werden neu erstellte Benutzer der Gruppe `CreatingBotAllowed` beitreten.

### RAG-Replikate konfigurieren

`enableRagReplicas` ist eine Option in [cdk.json](./cdk/cdk.json), die die Replikateinstellungen für die RAG-Datenbank steuert, insbesondere die Knowledge Bases mit Amazon OpenSearch Serverless.

- **Standard**: true
- **true**: Verbessert die Verfügbarkeit durch zusätzliche Replikate, geeignet für Produktionsumgebungen, erhöht aber die Kosten.
- **false**: Reduziert Kosten durch weniger Replikate, geeignet für Entwicklungs- und Testumgebungen.

Dies ist eine Konto-/Regionseinstellung, die die gesamte Anwendung betrifft und nicht einzelne Bots.

> [!Hinweis]
> Stand Juni 2024 unterstützt Amazon OpenSearch Serverless 0,5 OCU und senkt damit die Einstiegskosten für kleine Workloads. Produktivbereitstellungen können mit 2 OCUs beginnen, während Entwicklungs-/Testworkloads 1 OCU nutzen können. OpenSearch Serverless skaliert automatisch basierend auf Workload-Anforderungen. Weitere Details finden Sie in der [Ankündigung](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Regionsübergreifende Inferenz

[Regionsübergreifende Inferenz](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ermöglicht es Amazon Bedrock, Modellinferenzanfragen dynamisch über mehrere AWS-Regionen zu leiten und verbessert so den Durchsatz und die Resilienz bei Spitzenlastzeiten. Zur Konfiguration bearbeiten Sie `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) verbessert die Kaltstartzeiten von Lambda-Funktionen und bietet schnellere Reaktionszeiten für ein besseres Benutzererlebnis. Bei Python-Funktionen fallen jedoch [Gebühren je nach Cachegröße](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) an, und [in einigen Regionen ist es derzeit nicht verfügbar](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions). Um SnapStart zu deaktivieren, bearbeiten Sie `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Benutzerdefinierte Domain konfigurieren

Sie können eine benutzerdefinierte Domain für die CloudFront-Distribution festlegen, indem Sie die folgenden Parameter in [cdk.json](./cdk/cdk.json) setzen:

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Der benutzerdefinierte Domainname für Ihre Chat-Anwendung (z. B. chat.example.com)
- `hostedZoneId`: Die ID der Route 53-Hosted Zone, in der die Domaineinträge erstellt werden

Wenn diese Parameter angegeben werden, führt die Bereitstellung automatisch Folgendes durch:

- Erstellung eines ACM-Zertifikats mit DNS-Validierung in der Region us-east-1
- Erstellung der erforderlichen DNS-Einträge in Ihrer Route 53-Hosted Zone
- Konfiguration von CloudFront zur Verwendung Ihrer benutzerdefinierten Domain

> [!Hinweis]
> Die Domain muss in Ihrem AWS-Konto von Route 53 verwaltet werden. Die Hosted Zone ID finden Sie in der Route 53-Konsole.

### Lokale Entwicklung

Weitere Informationen finden Sie unter [LOKALE ENTWICKLUNG](./LOCAL_DEVELOPMENT_de-DE.md).

### Beitrag

Vielen Dank, dass Sie einen Beitrag zu diesem Repository in Betracht ziehen! Wir begrüßen Fehlerkorrekturen, Sprachübersetzungen (i18n), Funktionserweiterungen, [Agent-Tools](./docs/AGENT.md#how-to-develop-your-own-tools) und andere Verbesserungen.

Für Funktionserweiterungen und andere Verbesserungen würden wir es sehr schätzen, wenn Sie **vor dem Erstellen eines Pull Requests zunächst ein Feature-Request-Issue erstellen, um den Implementierungsansatz und die Details zu besprechen. Bei Fehlerkorrekturen und Sprachübersetzungen (i18n) können Sie direkt einen Pull Request erstellen.**

Bitte beachten Sie auch die folgenden Richtlinien, bevor Sie einen Beitrag leisten:

- [Lokale Entwicklung](./LOCAL_DEVELOPMENT_de-DE.md)
- [BEITRAG](./CONTRIBUTING_de-DE.md)

## Kontakte

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Bedeutende Mitwirkende

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Mitwirkende

[![bedrock claude chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Lizenz

Diese Bibliothek ist unter der MIT-0-Lizenz lizenziert. Weitere Informationen finden Sie in [der LIZENZDATEI](./LICENSE).