# Migrationsanleitung (v0 zu v1)

Wenn Sie Bedrock Chat bereits mit einer früheren Version (~`0.4.x`) verwenden, müssen Sie die folgenden Schritte zur Migration durchführen.

## Warum muss ich das tun?

Dieses große Update enthält wichtige Sicherheitsaktualisierungen.

- Der Speicher der Vektordatenbank (d.h. pgvector auf Aurora PostgreSQL) ist jetzt verschlüsselt, was bei der Bereitstellung einen Austausch auslöst. Das bedeutet, dass bestehende Vektorelemente gelöscht werden.
- Wir haben die Cognito-Benutzergruppe `CreatingBotAllowed` eingeführt, um die Benutzer einzuschränken, die Bots erstellen können. Bestehende Benutzer sind nicht in dieser Gruppe, daher müssen Sie die Berechtigung manuell hinzufügen, wenn Sie möchten, dass sie Bots erstellen können. Siehe: [Bot-Personalisierung](../../README.md#bot-personalization)

## Voraussetzungen

Lesen Sie den [Database Migration Guide](./DATABASE_MIGRATION_de-DE.md) und bestimmen Sie die Methode zur Wiederherstellung von Elementen.

## Schritte

### Vector-Store-Migration

- Öffnen Sie Ihr Terminal und navigieren Sie zum Projektverzeichnis
- Pullen Sie den Branch, den Sie deployen möchten. Im Folgenden zum gewünschten Branch (in diesem Fall `v1`) und pullen Sie die neuesten Änderungen:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Wenn Sie Elemente mit DMS wiederherstellen möchten, VERGESSEN SIE NICHT die Passwortrotation zu deaktivieren und notieren Sie sich das Passwort für den Datenbankzugriff. Bei der Wiederherstellung mit dem Migrationsskript ([migrate_v0_v1.py](./migrate_v0_v1.py)) müssen Sie sich das Passwort nicht notieren.
- Entfernen Sie alle [veröffentlichten APIs](../PUBLISH_API_de-DE.md), damit CloudFormation den bestehenden Aurora-Cluster entfernen kann.
- Die Ausführung von [npx cdk deploy](../README.md#deploy-using-cdk) löst den Austausch des Aurora-Clusters aus und LÖSCHT ALLE VECTOR-ELEMENTE.
- Folgen Sie der [Datenbank-Migrationsanleitung](./DATABASE_MIGRATION_de-DE.md), um Vector-Elemente wiederherzustellen.
- Überprüfen Sie, ob Benutzer existierende Bots mit Wissen (z.B. RAG-Bots) verwenden können.

### CreatingBotAllowed-Berechtigung hinzufügen

- Nach dem Deployment können alle Benutzer keine neuen Bots mehr erstellen.
- Wenn Sie möchten, dass bestimmte Benutzer Bots erstellen können, fügen Sie diese Benutzer über die Management-Konsole oder CLI der Gruppe `CreatingBotAllowed` hinzu.
- Überprüfen Sie, ob der Benutzer einen Bot erstellen kann. Beachten Sie, dass sich die Benutzer neu anmelden müssen.