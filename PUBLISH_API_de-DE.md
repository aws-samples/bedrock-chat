# API-Veröffentlichung

## Überblick

Dieses Beispiel umfasst eine Funktion zum Veröffentlichen von APIs. Während eine Chat-Schnittstelle für eine vorläufige Validierung praktisch sein kann, hängt die tatsächliche Implementierung vom spezifischen Anwendungsfall und der gewünschten Benutzererfahrung (UX) ab. In manchen Szenarien kann eine Chat-Benutzeroberfläche die bevorzugte Wahl sein, während in anderen Fällen eine eigenständige API geeigneter sein kann. Nach der ersten Validierung bietet dieses Beispiel die Möglichkeit, angepasste Bots entsprechend den Projektanforderungen zu veröffentlichen. Durch die Eingabe von Einstellungen für Kontingente, Drosselung, Ursprünge usw. kann ein Endpunkt zusammen mit einem API-Schlüssel veröffentlicht werden, was Flexibilität für verschiedene Integrationsmöglichkeiten bietet.

## Sicherheit

Die Verwendung nur eines API-Schlüssels wird wie in der [AWS API Gateway Entwickleranleitung](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) beschrieben nicht empfohlen. Daher implementiert dieses Beispiel eine einfache IP-Adresseinschränkung über AWS WAF. Die WAF-Regel wird aufgrund von Kostenüberlegungen einheitlich über die Anwendung angewendet, unter der Annahme, dass die Quellen, die man einschränken möchte, wahrscheinlich über alle ausgegebenen APIs hinweg gleich sind. **Bitte halten Sie sich bei der tatsächlichen Implementierung an die Sicherheitsrichtlinien Ihrer Organisation.** Weitere Informationen finden Sie auch im [Architektur](#architektur)-Abschnitt.

## Wie man einen benutzerdefinierten Bot-API veröffentlicht

### Voraussetzungen

Aus Governance-Gründen können nur begrenzte Benutzer Bots veröffentlichen. Vor der Veröffentlichung muss der Benutzer Mitglied der Gruppe `PublishAllowed` sein, die über die Verwaltungskonsole > Amazon Cognito User Pools oder die AWS CLI eingerichtet werden kann. Die Benutzer-Pool-ID kann durch Zugriff auf CloudFormation > BedrockChatStack > Ausgaben > `AuthUserPoolIdxxxx` referenziert werden.

![](./imgs/group_membership_publish_allowed.png)

### API-Veröffentlichungseinstellungen

Melden Sie sich als `PublishedAllowed`-Benutzer an und erstellen Sie einen Bot. Wählen Sie dann `API-Veröffentlichungseinstellungen`. Beachten Sie, dass nur ein freigegebener Bot veröffentlicht werden kann.
![](./imgs/bot_api_publish_screenshot.png)

Auf dem folgenden Bildschirm können mehrere Parameter bezüglich Drosselung konfiguriert werden. Weitere Details finden Sie unter: [API-Anfragen für besseren Durchsatz drosseln](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Nach der Bereitstellung erscheint der folgende Bildschirm, auf dem Sie die Endpunkt-URL und einen API-Schlüssel abrufen können. Es können auch API-Schlüssel hinzugefügt und gelöscht werden.

![](./imgs/bot_api_publish_screenshot3.png)

## Architektur

Die API wird wie folgt veröffentlicht:

![](./imgs/published_arch.png)

Die WAF wird für IP-Adresseinschränkungen verwendet. Die Adresse kann durch Festlegen der Parameter `publishedApiAllowedIpV4AddressRanges` und `publishedApiAllowedIpV6AddressRanges` in `cdk.json` konfiguriert werden.

Sobald ein Benutzer auf "Bot veröffentlichen" klickt, startet [AWS CodeBuild](https://aws.amazon.com/codebuild/) eine CDK-Bereitstellungsaufgabe, um den API-Stack bereitzustellen (Siehe auch: [CDK-Definition](../cdk/lib/api-publishment-stack.ts)), der API Gateway, Lambda und SQS enthält. SQS wird verwendet, um Benutzeranfragen und LLM-Operationen zu entkoppeln, da die Ausgabegenerierung 30 Sekunden überschreiten kann, was dem Grenzwert des API Gateway-Kontingents entspricht. Um die Ausgabe abzurufen, muss auf die API asynchron zugegriffen werden. Weitere Details finden Sie in der [API-Spezifikation](#api-specification).

Der Client muss `x-api-key` im Anforderungs-Header setzen.

## API-Spezifikation

Siehe [hier](https://aws-samples.github.io/bedrock-chat).