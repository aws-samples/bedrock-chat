# API-Veröffentlichung

## Überblick

Dieses Beispiel enthält eine Funktion zum Veröffentlichen von APIs. Während eine Chat-Schnittstelle für die erste Validierung praktisch sein kann, hängt die tatsächliche Implementierung vom spezifischen Anwendungsfall und der gewünschten Benutzererfahrung (UX) für den Endbenutzer ab. In manchen Szenarien könnte eine Chat-Benutzeroberfläche die bevorzugte Wahl sein, während in anderen eine eigenständige API geeigneter sein könnte. Nach der ersten Validierung bietet dieses Beispiel die Möglichkeit, maßgeschneiderte Bots entsprechend den Projektanforderungen zu veröffentlichen. Durch die Eingabe von Einstellungen für Kontingente, Drosselung, Ursprünge usw. kann ein Endpunkt zusammen mit einem API-Schlüssel veröffentlicht werden, was Flexibilität für verschiedene Integrationsmöglichkeiten bietet.

## Sicherheit

Die ausschließliche Verwendung eines API-Schlüssels wird nicht empfohlen, wie im [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) beschrieben. Daher implementiert dieses Beispiel eine einfache IP-Adresseinschränkung über AWS WAF. Die WAF-Regel wird aus Kostengründen einheitlich für die gesamte Anwendung angewendet, unter der Annahme, dass die Quellen, die man einschränken möchte, wahrscheinlich für alle bereitgestellten APIs gleich sind. **Bitte halten Sie sich bei der tatsächlichen Implementierung an die Sicherheitsrichtlinien Ihrer Organisation.** Siehe auch den Abschnitt [Architecture](#architecture).

## So veröffentlichen Sie eine angepasste Bot-API

### Voraussetzungen

Aus Governance-Gründen können nur bestimmte Benutzer Bots veröffentlichen. Vor der Veröffentlichung muss der Benutzer Mitglied der Gruppe `PublishAllowed` sein, die über die Management-Konsole > Amazon Cognito User Pools oder aws cli eingerichtet werden kann. Beachten Sie, dass die Benutzer-Pool-ID durch Zugriff auf CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` referenziert werden kann.

![](./imgs/group_membership_publish_allowed.png)

### API-Veröffentlichungseinstellungen

Nach der Anmeldung als `PublishedAllowed`-Benutzer und der Erstellung eines Bots wählen Sie `API PublishSettings`. Beachten Sie, dass nur ein freigegebener Bot veröffentlicht werden kann.
![](./imgs/bot_api_publish_screenshot.png)

Auf dem folgenden Bildschirm können wir verschiedene Parameter bezüglich der Drosselung konfigurieren. Weitere Details finden Sie auch unter: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Nach der Bereitstellung erscheint der folgende Bildschirm, auf dem Sie die Endpunkt-URL und einen API-Schlüssel erhalten. Wir können auch API-Schlüssel hinzufügen und löschen.

![](./imgs/bot_api_publish_screenshot3.png)

## Architektur

Die API wird wie im folgenden Diagramm veröffentlicht:

![](./imgs/published_arch.png)

Die WAF wird für die IP-Adresseinschränkung verwendet. Die Adresse kann durch Setzen der Parameter `publishedApiAllowedIpV4AddressRanges` und `publishedApiAllowedIpV6AddressRanges` in `cdk.json` konfiguriert werden.

Wenn ein Benutzer den Bot veröffentlicht, startet [AWS CodeBuild](https://aws.amazon.com/codebuild/) eine CDK-Bereitstellungsaufgabe, um den API-Stack bereitzustellen (siehe auch: [CDK-Definition](../cdk/lib/api-publishment-stack.ts)), der API Gateway, Lambda und SQS enthält. SQS wird verwendet, um Benutzeranfragen und LLM-Operationen zu entkoppeln, da die Generierung der Ausgabe 30 Sekunden überschreiten kann, was das Limit des API Gateway-Kontingents ist. Um die Ausgabe abzurufen, muss auf die API asynchron zugegriffen werden. Weitere Details finden Sie unter [API-Spezifikation](#api-specification).

Der Client muss `x-api-key` im Anfrage-Header setzen.

## API-Spezifikation

Siehe [hier](https://aws-samples.github.io/bedrock-chat).