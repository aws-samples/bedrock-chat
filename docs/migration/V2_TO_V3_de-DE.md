# Migrationsanleitung (v2 zu v3)

## TL;DR

- V3 führt eine feingranulare Berechtigungssteuerung und Bot Store-Funktionalität ein, die Änderungen am DynamoDB-Schema erfordern
- **Sichern Sie Ihre DynamoDB ConversationTable vor der Migration**
- Aktualisieren Sie Ihre Repository-URL von `bedrock-claude-chat` zu `bedrock-chat`
- Führen Sie das Migrationsskript aus, um Ihre Daten in das neue Schema zu konvertieren
- Alle Ihre Bots und Konversationen bleiben mit dem neuen Berechtigungsmodell erhalten
- **WICHTIG: Während des Migrationsprozesses ist die Anwendung für alle Benutzer nicht verfügbar, bis die Migration abgeschlossen ist. Dieser Prozess dauert typischerweise etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.**
- **WICHTIG: Alle veröffentlichten APIs müssen während des Migrationsprozesses gelöscht werden.**
- **WARNUNG: Der Migrationsprozess kann keine 100%ige Erfolgsgarantie für alle Bots geben. Bitte dokumentieren Sie Ihre wichtigen Bot-Konfigurationen vor der Migration, falls Sie sie manuell neu erstellen müssen**

## Einführung

### Was ist neu in V3

V3 führt wichtige Verbesserungen für Bedrock Chat ein:

1. **Feingranulare Berechtigungssteuerung**: Steuern Sie den Zugriff auf Ihre Bots mit gruppenbasierten Berechtigungen
2. **Bot Store**: Teilen und entdecken Sie Bots über einen zentralen Marktplatz
3. **Administrationsfunktionen**: Verwalten Sie APIs, markieren Sie Bots als essentiell und analysieren Sie die Bot-Nutzung

Diese neuen Funktionen erforderten Änderungen am DynamoDB-Schema, wodurch ein Migrationsprozess für bestehende Nutzer notwendig wurde.

### Warum diese Migration notwendig ist

Das neue Berechtigungsmodell und die Bot Store-Funktionalität erforderten eine Umstrukturierung der Art und Weise, wie Bot-Daten gespeichert und abgerufen werden. Der Migrationsprozess konvertiert Ihre bestehenden Bots und Konversationen in das neue Schema, während alle Ihre Daten erhalten bleiben.

> [!WARNING]
> Hinweis zur Serviceunterbrechung: **Während des Migrationsprozesses wird die Anwendung für alle Benutzer nicht verfügbar sein.** Planen Sie diese Migration während eines Wartungsfensters, wenn Benutzer keinen Zugriff auf das System benötigen. Die Anwendung wird erst wieder verfügbar sein, nachdem das Migrationsskript erfolgreich abgeschlossen wurde und alle Daten ordnungsgemäß in das neue Schema konvertiert wurden. Dieser Prozess dauert typischerweise etwa 60 Minuten, abhängig von der Datenmenge und der Leistung Ihrer Entwicklungsumgebung.

> [!IMPORTANT]
> Vor Beginn der Migration: **Der Migrationsprozess kann keinen 100%igen Erfolg für alle Bots garantieren**, insbesondere für solche, die mit älteren Versionen oder mit benutzerdefinierten Konfigurationen erstellt wurden. Bitte dokumentieren Sie Ihre wichtigen Bot-Konfigurationen (Anweisungen, Wissensquellen, Einstellungen), bevor Sie den Migrationsprozess starten, falls Sie diese manuell neu erstellen müssen.

## Migrationsprozess

### Wichtiger Hinweis zur Bot-Sichtbarkeit in V3

In V3 werden **alle v2-Bots mit aktivierter öffentlicher Freigabe im Bot Store durchsuchbar sein.** Wenn Sie Bots mit sensiblen Informationen haben, die nicht auffindbar sein sollen, sollten Sie diese vor der Migration zu V3 auf privat setzen.

### Schritt 1: Identifizieren Sie Ihren Umgebungsnamen

In diesem Verfahren wird `{YOUR_ENV_PREFIX}` verwendet, um den Namen Ihrer CloudFormation Stacks zu identifizieren. Wenn Sie die Funktion [Deploying Multiple Environments](../../README.md#deploying-multiple-environments) verwenden, ersetzen Sie dies durch den Namen der zu migrierenden Umgebung. Falls nicht, ersetzen Sie es durch einen leeren String.

### Schritt 2: Repository-URL aktualisieren (Empfohlen)

Das Repository wurde von `bedrock-claude-chat` in `bedrock-chat` umbenannt. Aktualisieren Sie Ihr lokales Repository:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Schritt 3: Stellen Sie sicher, dass Sie die neueste V2-Version verwenden

> [!WARNING]
> Sie MÜSSEN auf v2.10.0 aktualisieren, bevor Sie zu V3 migrieren. **Das Überspringen dieses Schritts kann während der Migration zu Datenverlust führen.**

Stellen Sie vor Beginn der Migration sicher, dass Sie die neueste Version von V2 (**v2.10.0**) ausführen. Dies gewährleistet, dass Sie alle notwendigen Fehlerbehebungen und Verbesserungen vor dem Upgrade auf V3 haben:

```bash
# Fetch the latest tags
git fetch --tags

# Checkout the latest V2 version
git checkout v2.10.0

# Deploy the latest V2 version
cd cdk
npm ci
npx cdk deploy --all
```

### Schritt 4: Notieren Sie Ihren V2 DynamoDB-Tabellennamen

Holen Sie sich den V2 ConversationTable-Namen aus den CloudFormation-Outputs:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Speichern Sie diesen Tabellennamen an einem sicheren Ort, da Sie ihn später für das Migrationsskript benötigen werden.

### Schritt 5: Sichern Sie Ihre DynamoDB-Tabelle

Erstellen Sie vor dem Fortfahren eine Sicherung Ihrer DynamoDB ConversationTable mit dem soeben notierten Namen:

```bash
# Create a backup of your V2 table
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Check the backup status is available
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Schritt 6: Löschen Sie alle veröffentlichten APIs

> [!IMPORTANT]
> Vor der Bereitstellung von V3 müssen Sie alle veröffentlichten APIs löschen, um Konflikte bei den Cloudformation-Ausgabewerten während des Upgrade-Prozesses zu vermeiden.

1. Melden Sie sich als Administrator in Ihrer Anwendung an
2. Navigieren Sie zum Admin-Bereich und wählen Sie "API Management"
3. Überprüfen Sie die Liste aller veröffentlichten APIs
4. Löschen Sie jede veröffentlichte API durch Klicken auf die Schaltfläche "Löschen" daneben

Weitere Informationen zum Veröffentlichen und Verwalten von APIs finden Sie in der Dokumentation [PUBLISH_API.md](../PUBLISH_API_de-DE.md) bzw. [ADMINISTRATOR.md](../ADMINISTRATOR_de-DE.md).

### Schritt 7: V3 Pull und Deployment

Laden Sie den neuesten V3-Code herunter und deployen Sie ihn:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Sobald Sie V3 deployen, wird die Anwendung für alle Benutzer nicht verfügbar sein, bis der Migrationsprozess abgeschlossen ist. Das neue Schema ist nicht kompatibel mit dem alten Datenformat, sodass Benutzer nicht auf ihre Bots oder Konversationen zugreifen können, bis Sie das Migrationsskript in den nächsten Schritten abgeschlossen haben.

### Schritt 8: Notieren Sie Ihre V3 DynamoDB-Tabellennamen

Nach dem Deployment von V3 müssen Sie sowohl die neuen ConversationTable- als auch BotTable-Namen erhalten:

```bash
# Get the V3 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Get the V3 BotTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Stellen Sie sicher, dass Sie diese V3-Tabellennamen zusammen mit Ihrem zuvor gespeicherten V2-Tabellennamen speichern, da Sie alle für das Migrationsskript benötigen werden.

### Schritt 9: Führen Sie das Migrationsskript aus

Das Migrationsskript konvertiert Ihre V2-Daten in das V3-Schema. Bearbeiten Sie zunächst das Migrationsskript `docs/migration/migrate_v2_v3.py`, um Ihre Tabellennamen und Region festzulegen:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Führen Sie dann das Skript mit Poetry aus dem Backend-Verzeichnis aus:

> [!NOTE]
> Die Python-Anforderungsversion wurde auf 3.13.0 oder höher geändert (kann sich in zukünftiger Entwicklung ändern. Siehe pyproject.toml). Wenn Sie venv mit einer anderen Python-Version installiert haben, müssen Sie es einmal entfernen.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies if you haven't already
poetry install

# Run a dry run first to see what would be migrated
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# If everything looks good, run the actual migration
poetry run python ../docs/migration/migrate_v2_v3.py

# Verify the migration was successful
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Das Migrationsskript erstellt eine Berichtsdatei in Ihrem aktuellen Verzeichnis mit Details zum Migrationsprozess. Überprüfen Sie diese Datei, um sicherzustellen, dass alle Ihre Daten korrekt migriert wurden.

#### Umgang mit großen Datenmengen

Für Umgebungen mit vielen Benutzern oder großen Datenmengen sollten Sie diese Ansätze in Betracht ziehen:

1. **Migrieren Sie Benutzer einzeln**: Für Benutzer mit großen Datenmengen migrieren Sie diese einzeln:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Speicherüberlegungen**: Der Migrationsprozess lädt Daten in den Speicher. Bei Out-Of-Memory (OOM)-Fehlern versuchen Sie:

   - Einen Benutzer nach dem anderen zu migrieren
   - Die Migration auf einem Rechner mit mehr Speicher durchzuführen
   - Die Migration in kleinere Benutzergruppen aufzuteilen

3. **Überwachen Sie die Migration**: Überprüfen Sie die generierten Berichtsdateien, um sicherzustellen, dass alle Daten korrekt migriert wurden, besonders bei großen Datensätzen.

### Schritt 10: Überprüfen Sie die Anwendung

Nach der Migration öffnen Sie Ihre Anwendung und überprüfen Sie:

- Alle Ihre Bots sind verfügbar
- Konversationen sind erhalten geblieben
- Neue Berechtigungskontrollen funktionieren

### Aufräumen (Optional)

Nachdem Sie bestätigt haben, dass die Migration erfolgreich war und alle Ihre Daten in V3 ordnungsgemäß zugänglich sind, können Sie optional die V2-Konversationstabelle löschen, um Kosten zu sparen:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Löschen Sie die V2-Tabelle erst, nachdem Sie gründlich überprüft haben, dass alle Ihre wichtigen Daten erfolgreich zu V3 migriert wurden. Wir empfehlen, die in Schritt 2 erstellte Sicherung mindestens einige Wochen nach der Migration aufzubewahren, auch wenn Sie die ursprüngliche Tabelle löschen.

## V3 FAQ

### Bot-Zugriff und Berechtigungen

**Q: Was passiert, wenn ein von mir genutzter Bot gelöscht wird oder meine Zugriffsrechte entfernt werden?**
A: Die Autorisierung wird zum Zeitpunkt des Chats überprüft, daher verlieren Sie sofort den Zugriff.

**Q: Was passiert, wenn ein Benutzer gelöscht wird (z.B. wenn ein Mitarbeiter das Unternehmen verlässt)?**
A: Die Daten können vollständig entfernt werden, indem alle Einträge aus DynamoDB mit ihrer Benutzer-ID als Partitionsschlüssel (PK) gelöscht werden.

**Q: Kann ich das Teilen für einen essenziellen öffentlichen Bot deaktivieren?**
A: Nein, ein Administrator muss den Bot zuerst als nicht essenziell markieren, bevor das Teilen deaktiviert werden kann.

**Q: Kann ich einen essenziellen öffentlichen Bot löschen?**
A: Nein, ein Administrator muss den Bot zuerst als nicht essenziell markieren, bevor er gelöscht werden kann.

### Sicherheit und Implementierung

**Q: Ist zeilenbasierte Sicherheit (RLS) für die Bot-Tabelle implementiert?**
A: Nein, aufgrund der Vielfalt der Zugriffsmuster. Die Autorisierung erfolgt beim Zugriff auf Bots, und das Risiko eines Metadaten-Lecks wird im Vergleich zum Gesprächsverlauf als minimal eingestuft.

**Q: Welche Anforderungen gibt es für die Veröffentlichung einer API?**
A: Der Bot muss öffentlich sein.

**Q: Wird es einen Verwaltungsbildschirm für alle privaten Bots geben?**
A: Nicht in der ersten V3-Version. Einträge können jedoch weiterhin bei Bedarf durch Abfragen mit der Benutzer-ID gelöscht werden.

**Q: Wird es eine Bot-Tagging-Funktionalität für eine bessere Such-UX geben?**
A: Nicht in der ersten V3-Version, aber LLM-basiertes automatisches Tagging könnte in zukünftigen Updates hinzugefügt werden.

### Administration

**Q: Was können Administratoren tun?**
A: Administratoren können:

- Öffentliche Bots verwalten (einschließlich der Überprüfung von Bots mit hohen Kosten)
- APIs verwalten
- Öffentliche Bots als essenziell markieren

**Q: Kann ich teilweise geteilte Bots als essenziell markieren?**
A: Nein, dies wird nur für öffentliche Bots unterstützt.

**Q: Kann ich eine Priorität für angeheftete Bots festlegen?**
A: Nicht in der ersten Version.

### Autorisierungskonfiguration

**Q: Wie richte ich die Autorisierung ein?**
A:

1. Öffnen Sie die Amazon Cognito-Konsole und erstellen Sie Benutzergruppen im BrChat-Benutzerpool
2. Fügen Sie nach Bedarf Benutzer zu diesen Gruppen hinzu
3. Wählen Sie in BrChat die Benutzergruppen aus, denen Sie Zugriff gewähren möchten, wenn Sie die Bot-Freigabeeinstellungen konfigurieren

Hinweis: Änderungen der Gruppenmitgliedschaft erfordern eine erneute Anmeldung. Änderungen werden bei der Token-Aktualisierung übernommen, aber nicht während der ID-Token-Gültigkeitsdauer (Standard 30 Minuten in V3, konfigurierbar durch `tokenValidMinutes` in `cdk.json` oder `parameter.ts`).

**Q: Prüft das System bei jedem Bot-Zugriff Cognito?**
A: Nein, die Autorisierung wird mittels JWT-Token überprüft, um unnötige I/O-Operationen zu vermeiden.

### Suchfunktionalität

**Q: Unterstützt die Bot-Suche semantische Suche?**
A: Nein, es wird nur partielle Textübereinstimmung unterstützt. Semantische Suche (z.B. "Automobil" → "Auto", "E-Auto", "Fahrzeug") ist aufgrund aktueller OpenSearch Serverless-Einschränkungen (März 2025) nicht verfügbar.