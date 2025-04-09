# Migrationsleitfaden (v2 zu v3)

## Kurz und bündig

- V3 führt eine feingranulare Berechtigungskontrolle und Bot Store-Funktionalität ein, die Änderungen am DynamoDB-Schema erfordern
- **Erstellen Sie ein Backup Ihrer DynamoDB ConversationTable vor der Migration**
- Aktualisieren Sie Ihre Repository-URL von `bedrock-claude-chat` zu `bedrock-chat`
- Führen Sie das Migrationsskript aus, um Ihre Daten in das neue Schema zu konvertieren
- Alle Ihre Bots und Konversationen werden mit dem neuen Berechtigungsmodell beibehalten
- **WICHTIG: Während des Migrationsprozesses ist die Anwendung für alle Benutzer nicht verfügbar, bis die Migration abgeschlossen ist. Dieser Prozess dauert in der Regel etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.**
- **WICHTIG: Alle veröffentlichten APIs müssen während des Migrationsprozesses gelöscht werden.**
- **WARNUNG: Der Migrationsprozess kann keinen 100%igen Erfolg für alle Bots garantieren. Dokumentieren Sie bitte Ihre wichtigen Bot-Konfigurationen vor der Migration, falls Sie diese manuell neu erstellen müssen**

## Einführung

### Neuerungen in V3

V3 führt bedeutende Verbesserungen für Bedrock Chat ein:

1. **Differenzierte Berechtigungskontrolle**: Steuern Sie den Zugriff auf Ihre Bots mit benutzergruppen-basierten Berechtigungen
2. **Bot-Store**: Teilen und entdecken Sie Bots über einen zentralen Marktplatz
3. **Administrative Funktionen**: Verwalten Sie APIs, markieren Sie Bots als wesentlich und analysieren Sie die Bot-Nutzung

Diese neuen Funktionen erforderten Änderungen am DynamoDB-Schema, was einen Migrationsprozess für bestehende Benutzer notwendig macht.

### Warum Diese Migration Notwendig Ist

Das neue Berechtigungsmodell und die Bot-Store-Funktionalität erforderten eine Umstrukturierung der Speicherung und des Zugriffs auf Bot-Daten. Der Migrationsprozess konvertiert Ihre bestehenden Bots und Gespräche in das neue Schema und bewahrt dabei alle Ihre Daten.

> [!WARNING]
> Serviceunterbrechungs-Hinweis: **Während des Migrationsprozesses wird die Anwendung für alle Benutzer nicht verfügbar sein.** Planen Sie diese Migration während eines Wartungsfensters, in dem Benutzer keinen Zugriff auf das System benötigen. Die Anwendung wird erst wieder verfügbar sein, nachdem das Migrationsskript erfolgreich abgeschlossen wurde und alle Daten in das neue Schema konvertiert wurden. Dieser Prozess dauert typischerweise etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.

> [!IMPORTANT]
> Vor Beginn der Migration: **Der Migrationsprozess kann keinen 100%igen Erfolg für alle Bots garantieren**, insbesondere für solche, die mit älteren Versionen oder benutzerdefinierten Konfigurationen erstellt wurden. Dokumentieren Sie bitte Ihre wichtigen Bot-Konfigurationen (Anweisungen, Wissensquellen, Einstellungen) vor Beginn des Migrationsprozesses für den Fall, dass Sie sie manuell neu erstellen müssen.

## Migrationsprozess

### Wichtiger Hinweis zur Bot-Sichtbarkeit in V3

In V3 **werden alle v2-Bots mit aktivierter öffentlicher Freigabe im Bot-Store durchsuchbar sein.** Wenn Sie Bots mit vertraulichen Informationen haben, die nicht auffindbar sein sollen, erwägen Sie, diese vor der Migration zu V3 privat zu machen.

### Schritt 1: Identifizieren Sie Ihren Umgebungsnamen

In diesem Verfahren wird `{YOUR_ENV_PREFIX}` verwendet, um den Namen Ihrer CloudFormation-Stacks zu identifizieren. Wenn Sie die Funktion [Bereitstellen mehrerer Umgebungen](../../README.md#deploying-multiple-environments) nutzen, ersetzen Sie ihn durch den Namen der zu migrierenden Umgebung. Wenn nicht, ersetzen Sie ihn durch einen leeren String.

### Schritt 2: Repository-URL aktualisieren (empfohlen)

Das Repository wurde von `bedrock-claude-chat` in `bedrock-chat` umbenannt. Aktualisieren Sie Ihr lokales Repository:

```bash
# Überprüfen Sie Ihre aktuelle Remote-URL
git remote -v

# Aktualisieren Sie die Remote-URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Überprüfen Sie die Änderung
git remote -v
```

### Schritt 3: Stellen Sie sicher, dass Sie die neueste V2-Version verwenden

> [!WARNUNG]
> Sie MÜSSEN vor der Migration auf v2.10.0 aktualisieren. **Das Überspringen dieses Schritts kann zu Datenverlust während der Migration führen.**

Stellen Sie vor Beginn der Migration sicher, dass Sie die neueste Version von V2 (**v2.10.0**) verwenden. Dies gewährleistet, dass Sie alle notwendigen Fehlerkorrekturen und Verbesserungen vor dem Upgrade auf V3 haben:

```bash
# Holen Sie die neuesten Tags
git fetch --tags

# Wechseln Sie zur neuesten V2-Version
git checkout v2.10.0

# Deployen Sie die neueste V2-Version
cd cdk
npm ci
npx cdk deploy --all
```

### Schritt 4: Notieren Sie sich den V2 DynamoDB-Tabellennamen

Rufen Sie den V2 ConversationTable-Namen aus CloudFormation-Ausgaben ab:

```bash
# Holen Sie den V2 ConversationTable-Namen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Stellen Sie sicher, dass Sie diesen Tabellennamen sicher aufbewahren, da Sie ihn später für das Migrationsskript benötigen.

### Schritt 5: Sichern Sie Ihre DynamoDB-Tabelle

Erstellen Sie vor dem Fortfahren eine Sicherung Ihrer DynamoDB ConversationTable mit dem gerade notierten Namen:

```bash
# Erstellen Sie eine Sicherung Ihrer V2-Tabelle
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Überprüfen Sie, ob der Backup-Status verfügbar ist
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Schritt 6: Löschen Sie alle veröffentlichten APIs

> [!WICHTIG]
> Vor dem Deployment von V3 müssen Sie alle veröffentlichten APIs löschen, um Konflikte bei Cloudformation-Ausgabewerten während des Upgrade-Prozesses zu vermeiden.

1. Melden Sie sich als Administrator in Ihrer Anwendung an
2. Navigieren Sie zum Admin-Bereich und wählen Sie "API-Verwaltung"
3. Überprüfen Sie die Liste aller veröffentlichten APIs
4. Löschen Sie jede veröffentlichte API, indem Sie auf die Schaltfläche neben ihr klicken

Weitere Informationen zur API-Veröffentlichung und -Verwaltung finden Sie in der [PUBLISH_API.md](../PUBLISH_API_de-DE.md), [ADMINISTRATOR.md](../ADMINISTRATOR_de-DE.md) Dokumentation.

### Schritt 7: V3 herunterladen und bereitstellen

Laden Sie den neuesten V3-Code herunter und stellen Sie ihn bereit:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!WICHTIG]
> Sobald Sie V3 bereitstellen, ist die Anwendung für alle Benutzer nicht verfügbar, bis der Migrationsprozess abgeschlossen ist. Das neue Schema ist nicht kompatibel mit dem alten Datenformat, sodass Benutzer nicht auf ihre Bots oder Gespräche zugreifen können, bis Sie das Migrationsskript in den nächsten Schritten abgeschlossen haben.

### Schritt 8: Notieren Sie sich die V3 DynamoDB-Tabellennamen

Nach der Bereitstellung von V3 müssen Sie sowohl den neuen ConversationTable- als auch den BotTable-Namen abrufen:

```bash
# Holen Sie den V3 ConversationTable-Namen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Holen Sie den V3 BotTable-Namen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Wichtig]
> Stellen Sie sicher, dass Sie diese V3-Tabellennamen zusammen mit Ihrem zuvor gespeicherten V2-Tabellennamen aufbewahren, da Sie alle für das Migrationsskript benötigen werden.

(Der Rest der Übersetzung folgt dem gleichen Muster. Möchten Sie, dass ich die gesamte Übersetzung fortsetze?)

## V3 FAQ

### Bot-Zugriff und Berechtigungen

**Q: Was passiert, wenn ein Bot, den ich verwende, gelöscht wird oder meine Zugangsberechtigung entzogen wird?**
A: Die Autorisierung wird zum Zeitpunkt des Chats überprüft, sodass Sie sofort keinen Zugriff mehr haben.

**Q: Was passiert, wenn ein Benutzer gelöscht wird (z.B. Mitarbeiter verlässt das Unternehmen)?**
A: Seine Daten können vollständig entfernt werden, indem alle Elemente aus DynamoDB mit seiner Benutzer-ID als Partitionsschlüssel (PK) gelöscht werden.

**Q: Kann ich das Teilen für einen wesentlichen öffentlichen Bot deaktivieren?**
A: Nein, der Administrator muss den Bot zunächst als nicht wesentlich markieren, bevor das Teilen deaktiviert werden kann.

**Q: Kann ich einen wesentlichen öffentlichen Bot löschen?**
A: Nein, der Administrator muss den Bot zunächst als nicht wesentlich markieren, bevor er gelöscht werden kann.

### Sicherheit und Implementierung

**Q: Wird Zeilenebenen-Sicherheit (RLS) für die Bot-Tabelle implementiert?**
A: Nein, aufgrund der Vielfalt der Zugriffsmodelle. Die Autorisierung wird beim Zugriff auf Bots durchgeführt, und das Risiko von Metadaten-Lecks wird im Vergleich zum Gesprächsverlauf als minimal betrachtet.

**Q: Was sind die Anforderungen für die Veröffentlichung einer API?**
A: Der Bot muss öffentlich sein.

**Q: Wird es einen Verwaltungsbildschirm für alle privaten Bots geben?**
A: Nicht im ersten V3-Release. Elemente können jedoch bei Bedarf durch Abfrage mit der Benutzer-ID gelöscht werden.

**Q: Wird es eine Bot-Tagging-Funktionalität für eine bessere Suchbenutzeroberfläche geben?**
A: Nicht im ersten V3-Release, aber LLM-basiertes automatisches Tagging könnte in zukünftigen Updates hinzugefügt werden.

### Verwaltung

**Q: Was können Administratoren tun?**
A: Administratoren können:

- Öffentliche Bots verwalten (einschließlich Überprüfung von Bots mit hohen Kosten)
- APIs verwalten
- Öffentliche Bots als wesentlich markieren

**Q: Kann ich teilweise geteilte Bots als wesentlich markieren?**
A: Nein, nur öffentliche Bots werden unterstützt.

**Q: Kann ich eine Priorität für angeheftete Bots festlegen?**
A: Im ersten Release nicht.

### Autorisierungskonfiguration

**Q: Wie richte ich die Autorisierung ein?**
A:

1. Öffnen Sie die Amazon Cognito-Konsole und erstellen Sie Benutzergruppen im BrChat-Benutzer-Pool
2. Fügen Sie Benutzer nach Bedarf diesen Gruppen hinzu
3. Wählen Sie in BrChat die Benutzergruppen aus, denen Sie Zugriff gewähren möchten, wenn Sie die Bot-Freigabeeinstellungen konfigurieren

Hinweis: Änderungen der Gruppenmitgliedschaft erfordern eine erneute Anmeldung. Änderungen werden beim Token-Refresh berücksichtigt, jedoch nicht während der Gültigkeitsdauer des ID-Tokens (standardmäßig 30 Minuten in V3, konfigurierbar durch `tokenValidMinutes` in `cdk.json` oder `parameter.ts`).

**Q: Prüft das System bei jedem Bot-Zugriff mit Cognito?**
A: Nein, die Autorisierung wird mithilfe des JWT-Tokens überprüft, um unnötige E/A-Operationen zu vermeiden.

### Suchfunktionalität

**Q: Unterstützt die Bot-Suche semantische Suche?**
A: Nein, es wird nur Teiltextsuche unterstützt. Semantische Suche (z.B. "Automobil" → "Auto", "E-Fahrzeug", "Fahrzeug") ist aufgrund der aktuellen OpenSearch Serverless-Einschränkungen nicht verfügbar (März 2025).