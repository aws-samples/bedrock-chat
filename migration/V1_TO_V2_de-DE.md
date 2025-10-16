# Migrationsanleitung (v1 zu v2)

## Zusammenfassung

- **Für Benutzer von v1.2 oder früher**: Aktualisieren Sie auf v1.4 und erstellen Sie Ihre Bots mit Knowledge Base (KB) neu. Nach einer Übergangsphase, sobald Sie bestätigt haben, dass alles mit KB wie erwartet funktioniert, fahren Sie mit dem Upgrade auf v2 fort.
- **Für Benutzer von v1.3**: Auch wenn Sie KB bereits verwenden, wird **dringend empfohlen**, auf v1.4 zu aktualisieren und Ihre Bots neu zu erstellen. Wenn Sie noch pgvector verwenden, migrieren Sie, indem Sie Ihre Bots mit KB in v1.4 neu erstellen.
- **Für Benutzer, die pgvector weiterhin nutzen möchten**: Ein Upgrade auf v2 wird nicht empfohlen, wenn Sie pgvector weiterhin nutzen möchten. Das Upgrade auf v2 wird alle pgvector-bezogenen Ressourcen entfernen, und zukünftiger Support wird nicht mehr verfügbar sein. Verwenden Sie in diesem Fall weiterhin v1.
- Beachten Sie, dass **das Upgrade auf v2 zur Löschung aller Aurora-bezogenen Ressourcen führt.** Zukünftige Updates werden sich ausschließlich auf v2 konzentrieren, wobei v1 als veraltet gekennzeichnet wird.

## Einführung

### Was passieren wird

Das v2-Update führt eine wichtige Änderung ein, indem pgvector auf Aurora Serverless und ECS-basiertes Embedding durch [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) ersetzt wird. Diese Änderung ist nicht abwärtskompatibel.

### Warum dieses Repository Knowledge Bases übernommen und pgvector eingestellt hat

Es gibt mehrere Gründe für diese Änderung:

#### Verbesserte RAG-Genauigkeit

- Knowledge Bases nutzen OpenSearch Serverless als Backend und ermöglichen hybride Suchen mit sowohl Volltext- als auch Vektorsuche. Dies führt zu einer besseren Genauigkeit bei der Beantwortung von Fragen, die Eigennamen enthalten, womit pgvector Schwierigkeiten hatte.
- Es unterstützt auch mehr Optionen zur Verbesserung der RAG-Genauigkeit, wie fortgeschrittenes Chunking und Parsing.
- Knowledge Bases sind seit Oktober 2024 seit fast einem Jahr allgemein verfügbar, wobei bereits Funktionen wie Web-Crawling hinzugefügt wurden. Weitere Updates werden erwartet, wodurch es langfristig einfacher wird, fortgeschrittene Funktionalitäten zu übernehmen. Während dieses Repository beispielsweise Funktionen wie den Import aus bestehenden S3-Buckets (eine häufig gewünschte Funktion) in pgvector nicht implementiert hat, wird dies in KB (KnowledgeBases) bereits unterstützt.

#### Wartung

- Das aktuelle ECS + Aurora Setup ist von zahlreichen Bibliotheken abhängig, einschließlich solcher für PDF-Parsing, Web-Crawling und das Extrahieren von YouTube-Transkripten. Im Vergleich dazu reduzieren verwaltete Lösungen wie Knowledge Bases den Wartungsaufwand sowohl für Benutzer als auch für das Entwicklungsteam des Repositories.

## Migrationsprozess (Zusammenfassung)

Wir empfehlen dringend, vor dem Umstieg auf v2 ein Upgrade auf v1.4 durchzuführen. In v1.4 können Sie sowohl pgvector als auch Knowledge Base Bots nutzen, was eine Übergangsphase ermöglicht, um Ihre bestehenden pgvector Bots in Knowledge Base neu zu erstellen und zu überprüfen, ob sie wie erwartet funktionieren. Auch wenn die RAG-Dokumente identisch bleiben, beachten Sie, dass die Backend-Änderungen zu OpenSearch aufgrund von Unterschieden wie k-NN-Algorithmen möglicherweise leicht abweichende, wenn auch im Allgemeinen ähnliche Ergebnisse liefern können.

Durch das Setzen von `useBedrockKnowledgeBasesForRag` auf true in `cdk.json` können Sie Bots mit Knowledge Bases erstellen. Allerdings werden pgvector Bots dann schreibgeschützt, wodurch die Erstellung oder Bearbeitung neuer pgvector Bots verhindert wird.

![](../imgs/v1_to_v2_readonly_bot.png)

In v1.4 werden auch [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) eingeführt. Aufgrund regionaler Einschränkungen von Knowledge Bases muss sich der S3-Bucket zum Hochladen von Dokumenten in derselben Region wie `bedrockRegion` befinden. Wir empfehlen, vor der Aktualisierung eine Sicherung der vorhandenen Dokumenten-Buckets durchzuführen, um zu vermeiden, dass später eine große Anzahl von Dokumenten manuell hochgeladen werden muss (da die S3-Bucket-Importfunktion verfügbar ist).

## Migrationsprozess (Detail)

Die Schritte unterscheiden sich je nachdem, ob Sie v1.2 oder früher bzw. v1.3 verwenden.

![](../imgs/v1_to_v2_arch.png)

### Schritte für Benutzer von v1.2 oder früher

1. **Sichern Sie Ihren bestehenden Dokumenten-Bucket (optional, aber empfohlen).** Wenn Ihr System bereits in Betrieb ist, empfehlen wir diesen Schritt dringend. Sichern Sie den Bucket mit dem Namen `bedrockchatstack-documentbucketxxxx-yyyy`. Wir können zum Beispiel [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html) verwenden.

2. **Aktualisierung auf v1.4**: Laden Sie den neuesten v1.4 Tag herunter, modifizieren Sie `cdk.json` und führen Sie das Deployment durch. Folgen Sie diesen Schritten:

   1. Laden Sie den neuesten Tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifizieren Sie `cdk.json` wie folgt:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Deployment der Änderungen:
      ```bash
      npx cdk deploy
      ```

3. **Bots neu erstellen**: Erstellen Sie Ihre Bots in Knowledge Base mit den gleichen Definitionen (Dokumente, Chunk-Größe etc.) wie die pgvector-Bots neu. Bei einer großen Dokumentenmenge wird dieser Prozess durch die Wiederherstellung aus dem Backup aus Schritt 1 erleichtert. Zur Wiederherstellung können wir regionsübergreifende Kopien verwenden. Weitere Details finden Sie [hier](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Um den wiederhergestellten Bucket anzugeben, konfigurieren Sie den Abschnitt `S3 Data Source` wie folgt. Die Pfadstruktur ist `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Die Benutzer-ID können Sie im Cognito-Benutzerpool und die Bot-ID in der Adressleiste auf dem Bot-Erstellungsbildschirm überprüfen.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Beachten Sie, dass einige Funktionen in Knowledge Bases nicht verfügbar sind, wie Web Crawling und YouTube-Transkript-Unterstützung (Web Crawler-Unterstützung ist geplant ([Issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Bedenken Sie auch, dass während der Übergangsphase sowohl für Aurora als auch für Knowledge Bases Gebühren anfallen.

4. **Veröffentlichte APIs entfernen**: Alle zuvor veröffentlichten APIs müssen aufgrund der VPC-Löschung vor dem Deployment von v2 neu veröffentlicht werden. Dazu müssen Sie zunächst die bestehenden APIs löschen. Die Verwendung der [Administrator-API-Verwaltungsfunktion](../ADMINISTRATOR_de-DE.md) kann diesen Prozess vereinfachen. Sobald die Löschung aller `APIPublishmentStackXXXX` CloudFormation-Stacks abgeschlossen ist, ist die Umgebung bereit.

5. **v2 deployen**: Nach der Veröffentlichung von v2 laden Sie den getaggten Source-Code herunter und führen das Deployment wie folgt durch (dies wird nach der Veröffentlichung möglich sein):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Nach dem Deployment von v2 **WERDEN ALLE BOTS MIT DEM PREFIX [Unsupported, Read-only] AUSGEBLENDET.** Stellen Sie sicher, dass Sie notwendige Bots neu erstellen, bevor Sie das Upgrade durchführen, um Zugriffsverluste zu vermeiden.

> [!Tip]
> Während Stack-Updates können wiederholt Meldungen wie: "Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." auftreten. Navigieren Sie in solchen Fällen zur Management Console > EC2 > Netzwerkschnittstellen und suchen Sie nach BedrockChatStack. Löschen Sie die angezeigten Schnittstellen, die mit diesem Namen verbunden sind, um einen reibungsloseren Deploymentprozess zu gewährleisten.

### Schritte für Benutzer von v1.3

Wie bereits erwähnt, müssen in v1.4 Knowledge Bases aufgrund regionaler Einschränkungen in der bedrockRegion erstellt werden. Daher müssen Sie die KB neu erstellen. Wenn Sie KB bereits in v1.3 getestet haben, erstellen Sie den Bot in v1.4 mit den gleichen Definitionen neu. Folgen Sie den für v1.2-Benutzer beschriebenen Schritten.