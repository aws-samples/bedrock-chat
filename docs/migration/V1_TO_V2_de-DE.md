# Migrationsleitfaden (v1 zu v2)

## Kurzfassung

- **Für Benutzer von v1.2 oder früher**: Aktualisieren Sie auf v1.4 und erstellen Sie Ihre Bots neu mit Knowledge Base (KB). Nach einer Übergangsphase, wenn Sie bestätigen, dass alles mit KB wie erwartet funktioniert, fahren Sie mit dem Upgrade auf v2 fort.
- **Für Benutzer von v1.3**: Auch wenn Sie bereits KB verwenden, wird **dringend empfohlen**, auf v1.4 zu aktualisieren und Ihre Bots neu zu erstellen. Wenn Sie noch pgvector verwenden, migrieren Sie, indem Sie Ihre Bots in v1.4 mit KB neu erstellen.
- **Für Benutzer, die pgvector weiterhin verwenden möchten**: Ein Upgrade auf v2 wird nicht empfohlen, wenn Sie planen, pgvector weiterhin zu verwenden. Ein Upgrade auf v2 wird alle mit pgvector zusammenhängenden Ressourcen entfernen, und zukünftige Unterstützung wird nicht mehr verfügbar sein. Bleiben Sie in diesem Fall bei v1.
- Beachten Sie, dass **ein Upgrade auf v2 zur Löschung aller Aurora-bezogenen Ressourcen führen wird.** Zukünftige Updates werden sich ausschließlich auf v2 konzentrieren, während v1 eingestellt wird.

## Einführung

### Was wird passieren

Das v2-Update führt eine wesentliche Änderung durch, indem pgvector auf Aurora Serverless und ECS-basierte Einbettung durch [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) ersetzt wird. Diese Änderung ist nicht abwärtskompatibel.

### Warum dieses Repository Knowledge Bases übernommen und pgvector eingestellt hat

Es gibt mehrere Gründe für diese Änderung:

#### Verbesserte RAG-Genauigkeit

- Knowledge Bases verwenden OpenSearch Serverless als Backend und ermöglichen Hybrid-Suchen mit Volltext- und Vektorsuche. Dies führt zu einer besseren Genauigkeit bei der Beantwortung von Fragen, die Eigennamen enthalten, bei denen pgvector Schwierigkeiten hatte.
- Es bietet auch mehr Optionen zur Verbesserung der RAG-Genauigkeit, wie fortschrittliches Chunking und Parsing.
- Knowledge Bases sind seit fast einem Jahr, also Oktober 2024, allgemein verfügbar, mit bereits hinzugefügten Funktionen wie Webcrawling. Zukünftige Updates werden erwartet, was die Übernahme fortschrittlicher Funktionen langfristig erleichtert. Während dieses Repository beispielsweise Funktionen wie das Importieren aus vorhandenen S3-Buckets (eine häufig gewünschte Funktion) bei pgvector nicht implementiert hat, wird dies in KB (KnowledgeBases) bereits unterstützt.

#### Wartung

- Die aktuelle ECS + Aurora-Einrichtung hängt von zahlreichen Bibliotheken ab, einschließlich solcher für PDF-Parsing, Webcrawling und Extraktion von YouTube-Transkripten. Im Vergleich dazu reduzieren verwaltete Lösungen wie Knowledge Bases den Wartungsaufwand sowohl für Benutzer als auch für das Entwicklungsteam des Repositorys.

## Migrationsprozess (Zusammenfassung)

Wir empfehlen dringend, zuerst auf v1.4 zu aktualisieren, bevor Sie zu v2 wechseln. In v1.4 können Sie sowohl pgvector als auch Knowledge Base Bots verwenden, was eine Übergangsphase ermöglicht, um Ihre bestehenden pgvector Bots in Knowledge Base zu übertragen und zu überprüfen, ob sie wie erwartet funktionieren. Auch wenn die RAG-Dokumente identisch bleiben, sollten Sie beachten, dass die Backend-Änderungen an OpenSearch aufgrund von Unterschieden wie k-NN-Algorithmen möglicherweise leicht abweichende Ergebnisse liefern, die jedoch im Allgemeinen ähnlich sind.

Durch die Einstellung von `useBedrockKnowledgeBasesForRag` auf true in `cdk.json` können Sie Bots mit Knowledge Bases erstellen. Allerdings werden pgvector Bots schreibgeschützt, sodass keine neuen pgvector Bots erstellt oder bearbeitet werden können.

![](../imgs/v1_to_v2_readonly_bot.png)

In v1.4 werden auch [Guardrails für Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) eingeführt. Aufgrund regionaler Einschränkungen von Knowledge Bases muss der S3-Bucket für das Hochladen von Dokumenten in derselben Region wie `bedrockRegion` liegen. Wir empfehlen, vorhandene Dokumenten-Buckets vor dem Update zu sichern, um das manuelle Hochladen großer Dokumentenmengen zu vermeiden (da die S3-Bucket-Importfunktionalität verfügbar ist).

## Migrationsprozess (Details)

Die Schritte unterscheiden sich je nachdem, ob Sie v1.2 oder eine frühere Version oder v1.3 verwenden.

![](../imgs/v1_to_v2_arch.png)

### Schritte für Benutzer von v1.2 oder früher

1. **Sichern Sie Ihren bestehenden Dokumenten-Bucket (optional, aber empfohlen).** Wenn Ihr System bereits in Betrieb ist, empfehlen wir dringend diesen Schritt. Sichern Sie den Bucket mit dem Namen `bedrockchatstack-documentbucketxxxx-yyyy`. Beispielsweise können wir [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html) verwenden.

2. **Aktualisieren auf v1.4**: Holen Sie den neuesten v1.4-Tag, ändern Sie `cdk.json` und deployen Sie. Folgen Sie diesen Schritten:

   1. Holen Sie den neuesten Tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Ändern Sie `cdk.json` wie folgt:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Deployen Sie die Änderungen:
      ```bash
      npx cdk deploy
      ```

3. **Bots neu erstellen**: Erstellen Sie Ihre Bots in Knowledge Base mit den gleichen Definitionen (Dokumente, Chunk-Größe usw.) wie die pgvector-Bots. Bei einer großen Dokumentenmenge erleichtert die Wiederherstellung aus der Sicherung in Schritt 1 diesen Prozess. Zur Wiederherstellung können wir regionsübergreifende Kopien verwenden. Weitere Details finden Sie [hier](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Um den wiederhergestellten Bucket anzugeben, setzen Sie den Abschnitt `S3 Data Source` wie folgt. Die Pfadstruktur lautet `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Die Benutzer-ID können Sie im Cognito-Benutzerpool und die Bot-ID in der Adressleiste auf dem Bot-Erstellungsbildschirm überprüfen.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Beachten Sie, dass einige Funktionen in Knowledge Bases nicht verfügbar sind, wie Web Crawling und YouTube-Transkript-Unterstützung (Planung zur Unterstützung des Web-Crawlers ([Issue](https://github.com/aws-samples/bedrock-claude-chat/issues/557))).** Beachten Sie auch, dass die Nutzung von Knowledge Bases Gebühren für sowohl Aurora als auch Knowledge Bases während des Übergangs verursacht.

4. **Veröffentlichte APIs entfernen**: Alle zuvor veröffentlichten APIs müssen vor dem Deployment von v2 aufgrund der VPC-Löschung neu veröffentlicht werden. Dazu müssen Sie zunächst die vorhandenen APIs löschen. Die Verwendung der [API-Verwaltungsfunktion des Administrators](../ADMINISTRATOR_de-DE.md) kann diesen Prozess vereinfachen. Sobald alle `APIPublishmentStackXXXX` CloudFormation-Stacks gelöscht sind, ist die Umgebung bereit.

5. **V2 deployen**: Nach der Veröffentlichung von v2 holen und deployen Sie den getaggten Quellcode wie folgt (dies wird möglich sein, sobald es veröffentlicht wird):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warnung]
> Nach dem Deployment von v2 werden **ALLE BOTS MIT DEM PRÄFIX [Nicht unterstützt, Nur Lesezugriff] AUSGEBLENDET.** Stellen Sie sicher, dass Sie notwendige Bots neu erstellen, bevor Sie upgraden, um den Zugriffsverlust zu vermeiden.

> [!Tipp]
> Während der Stack-Updates können Sie möglicherweise wiederholte Nachrichten wie diese erhalten: Ressourcen-Handler hat Nachricht zurückgegeben: "Das Subnetz 'subnet-xxx' hat Abhängigkeiten und kann nicht gelöscht werden." Navigieren Sie in solchen Fällen zur Verwaltungskonsole > EC2 > Netzwerkschnittstellen und suchen Sie nach BedrockChatStack. Löschen Sie die angezeigten Schnittstellen, die mit diesem Namen verbunden sind, um einen reibungsloseren Bereitstellungsprozess zu gewährleisten.

### Schritte für Benutzer von v1.3

Wie bereits erwähnt, müssen in v1.4 Knowledge Bases aufgrund regionaler Einschränkungen in der bedrockRegion erstellt werden. Daher müssen Sie die KB neu erstellen. Wenn Sie KB in v1.3 bereits getestet haben, erstellen Sie den Bot in v1.4 mit den gleichen Definitionen neu. Folgen Sie den Schritten für Benutzer von v1.2.
