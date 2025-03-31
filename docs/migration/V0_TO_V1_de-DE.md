# Migrationsleitfaden (v0 zu v1)

Wenn Sie Bedrock Claude Chat bereits mit einer früheren Version (~`0.4.x`) verwenden, müssen Sie die folgenden Schritte zur Migration befolgen.

## Warum muss ich das machen?

Dieses große Update enthält wichtige Sicherheitsupdates.

- Der Vektordatenbankspeicher (d.h. pgvector auf Aurora PostgreSQL) ist jetzt verschlüsselt, was bei der Bereitstellung einen Austausch auslöst. Das bedeutet, dass vorhandene Vektorelemente gelöscht werden.
- Wir haben die Cognito-Benutzergruppe `CreatingBotAllowed` eingeführt, um die Benutzer zu begrenzen, die Bots erstellen können. Bestehende Benutzer sind nicht in dieser Gruppe, daher müssen Sie die Berechtigung manuell hinzufügen, wenn Sie ihnen die Fähigkeit zur Bot-Erstellung geben möchten. Siehe: [Bot-Personalisierung](../../README.md#bot-personalization)

## Voraussetzungen

Lesen Sie den [Leitfaden zur Datenbankmigration](./DATABASE_MIGRATION_de-DE.md) und bestimmen Sie die Methode zum Wiederherstellen von Elementen.

## Schritte

### Migration des Vektorspeichers

- Öffnen Sie Ihr Terminal und navigieren Sie zum Projektverzeichnis
- Ziehen Sie den Branch, den Sie bereitstellen möchten. Wechseln Sie zum gewünschten Branch (in diesem Fall `v1`) und ziehen Sie die neuesten Änderungen:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Wenn Sie Elemente mit DMS wiederherstellen möchten, VERGESSEN SIE NICHT, die Passwortrotation zu deaktivieren und notieren Sie sich das Passwort für den Datenbankzugriff. Bei Wiederherstellung mit dem Migrationsskript ([migrate.py](./migrate.py)) müssen Sie sich das Passwort nicht notieren.
- Entfernen Sie alle [veröffentlichten APIs](../PUBLISH_API_de-DE.md), damit CloudFormation den bestehenden Aurora-Cluster entfernen kann.
- Führen Sie [npx cdk deploy](../README.md#deploy-using-cdk) aus, um den Aurora-Cluster zu ersetzen und ALLE VEKTORELEMENTE ZU LÖSCHEN.
- Folgen Sie dem [Datenbankmigrationsleitfaden](./DATABASE_MIGRATION_de-DE.md), um Vektorelemente wiederherzustellen.
- Überprüfen Sie, ob der Benutzer vorhandene Bots nutzen kann, die Wissen haben, d.h. RAG-Bots.

### Berechtigung "CreatingBotAllowed" hinzufügen

- Nach der Bereitstellung können alle Benutzer keine neuen Bots erstellen.
- Wenn Sie bestimmten Benutzern das Erstellen von Bots ermöglichen möchten, fügen Sie diese Benutzer über die Verwaltungskonsole oder die Befehlszeilenschnittstelle zur Gruppe `CreatingBotAllowed` hinzu.
- Überprüfen Sie, ob der Benutzer einen Bot erstellen kann. Beachten Sie, dass die Benutzer sich erneut anmelden müssen.