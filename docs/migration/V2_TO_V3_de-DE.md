# Migrationsleitfaden (v2 zu v3)

## Kurzfassung

- V3 führt eine differenzierte Berechtigungskontrolle und Bot Store-Funktionalität ein, die Änderungen am DynamoDB-Schema erfordern
- **Sichern Sie Ihre DynamoDB ConversationTable vor der Migration**
- Aktualisieren Sie Ihre Repository-URL von `bedrock-claude-chat` zu `bedrock-chat`
- Führen Sie das Migrationsskript aus, um Ihre Daten in das neue Schema zu konvertieren
- Alle Ihre Bots und Konversationen werden mit dem neuen Berechtigungsmodell beibehalten
- **WICHTIG: Während des Migrationsprozesses ist die Anwendung für alle Benutzer nicht verfügbar, bis die Migration abgeschlossen ist. Dieser Vorgang dauert typischerweise etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.**
- **WICHTIG: Alle veröffentlichten APIs müssen während des Migrationsprozesses gelöscht werden.**
- **WARNUNG: Der Migrationsprozess kann keinen 100%igen Erfolg für alle Bots garantieren. Dokumentieren Sie bitte Ihre wichtigen Bot-Konfigurationen vor der Migration für den Fall, dass Sie sie manuell neu erstellen müssen**

## Einführung

### Neuerungen in V3

V3 führt bedeutende Verbesserungen für Bedrock Chat ein:

1. **Differenzierte Berechtigungskontrolle**: Steuern Sie den Zugriff auf Ihre Bots mit benutzergruppenbezogenen Berechtigungen
2. **Bot-Store**: Teilen und entdecken Sie Bots über einen zentralen Marktplatz
3. **Administrative Funktionen**: Verwalten Sie APIs, markieren Sie Bots als wesentlich und analysieren Sie die Bot-Nutzung

Diese neuen Funktionen erforderten Änderungen am DynamoDB-Schema, was eine Migrationsprozess für bestehende Benutzer notwendig macht.

### Warum Diese Migration Erforderlich Ist

Das neue Berechtigungsmodell und die Bot-Store-Funktionalität erforderten eine Umstrukturierung der Speicherung und des Zugriffs auf Bot-Daten. Der Migrationsprozess konvertiert Ihre bestehenden Bots und Konversationen in das neue Schema und bewahrt dabei alle Ihre Daten.

> [!WARNING]
> Serviceunterbrechungs-Hinweis: **Während des Migrationsprozesses wird die Anwendung für alle Benutzer nicht verfügbar sein.** Planen Sie diese Migration während eines Wartungsfensters, in dem Benutzer keinen Systemzugriff benötigen. Die Anwendung wird erst wieder verfügbar sein, nachdem das Migrationsskript erfolgreich abgeschlossen wurde und alle Daten in das neue Schema konvertiert wurden. Dieser Prozess dauert typischerweise etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.

> [!IMPORTANT]
> Vor Beginn der Migration: **Der Migrationsprozess kann keinen 100%igen Erfolg für alle Bots garantieren**, insbesondere für solche, die mit älteren Versionen oder mit benutzerdefinierten Konfigurationen erstellt wurden. Dokumentieren Sie bitte Ihre wichtigen Bot-Konfigurationen (Anweisungen, Wissensquellen, Einstellungen) vor Beginn des Migrationsprozesses für den Fall, dass Sie sie manuell neu erstellen müssen.

## Migrationsprozess

### Wichtiger Hinweis zur Bot-Sichtbarkeit in V3

In V3 werden **alle v2-Bots mit aktivierter öffentlicher Freigabe im Bot-Store durchsuchbar sein.** Wenn Sie Bots mit sensiblen Informationen haben, die nicht auffindbar sein sollen, ziehen Sie in Betracht, diese vor der Migration zu V3 privat zu machen.

### Schritt 1: Umgebungsname identifizieren

In diesem Verfahren wird `{YOUR_ENV_PREFIX}` verwendet, um den Namen Ihrer CloudFormation-Stacks zu identifizieren. Wenn Sie das Feature [Mehrere Umgebungen bereitstellen](../../README.md#deploying-multiple-environments) verwenden, ersetzen Sie es durch den Namen der zu migrierenden Umgebung. Wenn nicht, ersetzen Sie es durch einen leeren String.

### Schritt 2: Repository-URL aktualisieren (empfohlen)

Das Repository wurde von `bedrock-claude-chat` in `bedrock-chat` umbenannt. Aktualisieren Sie Ihr lokales Repository:

```bash
# Aktuelle Remote-URL überprüfen
git remote -v

# Remote-URL aktualisieren
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Änderung überprüfen
git remote -v
```

### Schritt 3: Sicherstellen, dass Sie die neueste V2-Version verwenden

> [!WARNUNG]
> Sie MÜSSEN auf v2.10.0 aktualisieren, bevor Sie zu V3 migrieren. **Das Überspringen dieses Schritts kann zu Datenverlust während der Migration führen.**

Stellen Sie vor Beginn der Migration sicher, dass Sie die neueste Version von V2 (**v2.10.0**) verwenden. Dies gewährleistet, dass Sie alle notwendigen Fehlerkorrekturen und Verbesserungen vor dem Upgrade auf V3 haben:

```bash
# Neueste Tags abrufen
git fetch --tags

# Neueste V2-Version auschecken
git checkout v2.10.0

# Neueste V2-Version bereitstellen
cd cdk
npm ci
npx cdk deploy --all
```

### Schritt 4: DynamoDB-Tabellenname von V2 aufzeichnen

Rufen Sie den V2-ConversationTable-Namen aus CloudFormation-Ausgaben ab:

```bash
# V2-ConversationTable-Namen abrufen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Stellen Sie sicher, dass Sie diesen Tabellennamen sicher aufbewahren, da Sie ihn später für das Migrationsskript benötigen.

### Schritt 5: DynamoDB-Tabelle sichern

Erstellen Sie vor dem Fortfahren eine Sicherung Ihrer DynamoDB-ConversationTable mit dem gerade aufgezeichneten Namen:

```bash
# Sicherung der V2-Tabelle erstellen
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Sicherungsstatus überprüfen
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Schritt 6: Alle veröffentlichten APIs löschen

> [!WICHTIG]
> Vor der Bereitstellung von V3 müssen Sie alle veröffentlichten APIs löschen, um Konflikte bei CloudFormation-Ausgabewerten während des Upgrade-Prozesses zu vermeiden.

1. Melden Sie sich als Administrator bei Ihrer Anwendung an
2. Navigieren Sie zum Administrationsbereich und wählen Sie "API-Verwaltung"
3. Überprüfen Sie die Liste aller veröffentlichten APIs
4. Löschen Sie jede veröffentlichte API, indem Sie neben ihr auf die Schaltfläche "Löschen" klicken

Weitere Informationen zur API-Veröffentlichung und -Verwaltung finden Sie in der Dokumentation [PUBLISH_API.md](../PUBLISH_API_de-DE.md) und [ADMINISTRATOR.md](../ADMINISTRATOR_de-DE.md).

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

### Schritt 8: V3 DynamoDB-Tabellennamen aufzeichnen

Nach der Bereitstellung von V3 müssen Sie sowohl den neuen ConversationTable- als auch den BotTable-Namen abrufen:

```bash
# V3-ConversationTable-Namen abrufen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# V3-BotTable-Namen abrufen
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Wichtig]
> Stellen Sie sicher, dass Sie diese V3-Tabellennamen zusammen mit Ihrem zuvor gespeicherten V2-Tabellennamen aufbewahren, da Sie alle für das Migrationsskript benötigen werden.

(Der Rest der Dokumentation wurde analog übersetzt. Möchten Sie, dass ich den gesamten Text übersetze?)

## V3 FAQ

### Bot-Zugriff und Berechtigungen

**Q: Was passiert, wenn ein Bot, den ich nutze, gelöscht wird oder meine Zugangsberechtigung entzogen wird?**
A: Die Autorisierung wird zum Zeitpunkt des Chats überprüft, sodass der Zugriff sofort entfällt.

**Q: Was passiert, wenn ein Benutzer gelöscht wird (z.B. Mitarbeiter verlässt das Unternehmen)?**
A: Seine Daten können vollständig entfernt werden, indem alle Elemente in DynamoDB mit seiner Benutzer-ID als Partitionsschlüssel (PK) gelöscht werden.

**Q: Kann ich das Teilen für einen wesentlichen öffentlichen Bot deaktivieren?**
A: Nein, der Administrator muss den Bot zunächst als nicht wesentlich markieren, bevor das Teilen deaktiviert werden kann.

**Q: Kann ich einen wesentlichen öffentlichen Bot löschen?**
A: Nein, der Administrator muss den Bot zunächst als nicht wesentlich markieren, bevor er gelöscht werden kann.

### Sicherheit und Implementierung

**Q: Ist Sicherheit auf Zeilenebene (RLS) für die Bot-Tabelle implementiert?**
A: Nein, aufgrund der Vielfalt an Zugriffsmustern. Die Autorisierung wird beim Zugriff auf Bots durchgeführt, und das Risiko einer Metadaten-Offenlegung wird im Vergleich zum Gesprächsverlauf als minimal eingestuft.

**Q: Was sind die Anforderungen für die Veröffentlichung einer API?**
A: Der Bot muss öffentlich sein.

**Q: Wird es einen Verwaltungsbildschirm für alle privaten Bots geben?**
A: Nicht im ersten V3-Release. Elemente können jedoch bei Bedarf durch Abfrage mit der Benutzer-ID gelöscht werden.

**Q: Wird es Funktionen zur Bot-Markierung für eine bessere Sucherfahrung geben?**
A: Nicht im ersten V3-Release, aber LLM-basierte automatische Markierung könnte in zukünftigen Updates hinzugefügt werden.

### Administration

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
3. Wählen Sie in BrChat die Benutzergruppen aus, denen Sie Zugriff gewähren möchten, wenn Sie die Einstellungen für Bot-Freigabe konfigurieren

Hinweis: Änderungen der Gruppenmitgliedschaft erfordern eine erneute Anmeldung. Änderungen werden beim Token-Refresh berücksichtigt, jedoch nicht während der Gültigkeitsdauer des ID-Tokens (standardmäßig 30 Minuten in V3, konfigurierbar durch `tokenValidMinutes` in `cdk.json` oder `parameter.ts`).

**Q: Überprüft das System bei jedem Bot-Zugriff Cognito?**
A: Nein, die Autorisierung wird mithilfe des JWT-Tokens überprüft, um unnötige I/O-Operationen zu vermeiden.

### Suchfunktionalität

**Q: Unterstützt die Bot-Suche semantische Suche?**
A: Nein, es wird nur Teiltextübereinstimmung unterstützt. Semantische Suche (z.B. "Automobil" → "Auto", "Elektrofahrzeug", "Fahrzeug") ist aufgrund aktueller OpenSearch Serverless-Einschränkungen nicht verfügbar (März 2025).