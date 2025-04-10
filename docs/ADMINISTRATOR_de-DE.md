# Administratives Features

## Voraussetzungen

Der Administrator-Benutzer muss Mitglied der Gruppe `Admin` sein, die über die Verwaltungskonsole > Amazon Cognito-Benutzer-Pools oder die AWS-CLI eingerichtet werden kann. Beachten Sie, dass die Benutzer-Pool-ID durch den Zugriff auf CloudFormation > BedrockChatStack > Ausgaben > `AuthUserPoolIdxxxx` referenziert werden kann.

![](./imgs/group_membership_admin.png)

## Öffentliche Bots als Wesentlich markieren

Öffentliche Bots können jetzt von Administratoren als "Wesentlich" markiert werden. Bots, die als Wesentlich gekennzeichnet sind, werden im Abschnitt "Wesentlich" des Bot-Stores hervorgehoben, wodurch sie für Benutzer leicht zugänglich sind. Dies ermöglicht es Administratoren, wichtige Bots zu markieren, die alle Benutzer nutzen sollen.

### Beispiele

- HR-Assistenz-Bot: Hilft Mitarbeitern bei HR-bezogenen Fragen und Aufgaben.
- IT-Support-Bot: Bietet Unterstützung bei internen technischen Problemen und Kontoverwaltung.
- Interner Richtlinien-Leitfaden-Bot: Beantwortet häufig gestellte Fragen zu Anwesenheitsregeln, Sicherheitsrichtlinien und anderen internen Vorschriften.
- Neuer Mitarbeiter Onboarding-Bot: Führt neue Mitarbeiter an Verfahren und Systemnutzung am ersten Tag heran.
- Leistungsinformations-Bot: Erklärt betriebliche Leistungsprogramme und Sozialleistungen.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Feedback-Schleife

Die Ausgabe von LLMs entspricht möglicherweise nicht immer den Erwartungen des Benutzers. Manchmal erfüllt sie die Bedürfnisse des Benutzers nicht. Um LLMs effektiv in Geschäftsprozesse und den Alltag zu "integrieren", ist die Implementierung einer Feedback-Schleife unerlässlich. Bedrock Chat verfügt über eine Feedbackfunktion, die es Benutzern ermöglicht, zu analysieren, warum Unzufriedenheit aufgetreten ist. Basierend auf den Analyseergebnissen können Benutzer die Prompts, RAG-Datenquellen und Parameter entsprechend anpassen.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Datenanalysten können auf Gesprächsprotokolle mit [Amazon Athena](https://aws.amazon.com/jp/athena/) zugreifen. Wenn sie die Daten in [Jupyter Notebook](https://jupyter.org/) analysieren möchten, kann [dieses Notebook-Beispiel](../examples/notebooks/feedback_analysis_example.ipynb) als Referenz dienen.

## Dashboard

Bietet derzeit einen grundlegenden Überblick über Chatbot- und Benutzernutzung und konzentriert sich darauf, Daten für jeden Bot und Benutzer über festgelegte Zeiträume zu aggregieren und die Ergebnisse nach Nutzungsgebühren zu sortieren.

![](./imgs/admin_bot_analytics.png)

## Hinweise

- Wie in der [Architektur](../README.md#architecture) beschrieben, beziehen sich die Admin-Funktionen auf den S3-Bucket, der aus DynamoDB exportiert wurde. Bitte beachten Sie, dass die neuesten Gespräche möglicherweise nicht sofort angezeigt werden, da der Export nur einmal pro Stunde durchgeführt wird.

- Bei öffentlichen Bot-Nutzungen werden Bots, die während des angegebenen Zeitraums überhaupt nicht genutzt wurden, nicht aufgelistet.

- Bei Benutzernutzungen werden Benutzer, die das System während des angegebenen Zeitraums überhaupt nicht genutzt haben, nicht aufgelistet.

> [!Wichtig]
> Bei Verwendung mehrerer Umgebungen (dev, prod, usw.) enthält der Athena-Datenbankname das Umgebungs-Präfix. Anstelle von `bedrockchatstack_usage_analysis` lautet der Datenbankname:
>
> - Für Standardumgebung: `bedrockchatstack_usage_analysis`
> - Für benannte Umgebungen: `<env-prefix>_bedrockchatstack_usage_analysis` (z.B. `dev_bedrockchatstack_usage_analysis`)
>
> Zusätzlich enthält der Tabellenname das Umgebungs-Präfix:
>
> - Für Standardumgebung: `ddb_export`
> - Für benannte Umgebungen: `<env-prefix>_ddb_export` (z.B. `dev_ddb_export`)
>
> Stellen Sie sicher, dass Sie Ihre Abfragen bei der Arbeit mit mehreren Umgebungen entsprechend anpassen.

## Gesprächsdaten herunterladen

Sie können die Gesprächsprotokolle mithilfe von Athena und SQL abfragen. Um Protokolle herunterzuladen, öffnen Sie den Athena Query Editor über die Verwaltungskonsole und führen Sie SQL aus. Die folgenden Beispielabfragen sind nützlich zur Analyse von Anwendungsfällen. Feedback kann im `MessageMap`-Attribut nachgeschlagen werden.

### Abfrage nach Bot-ID

Bearbeiten Sie `bot-id` und `datehour`. Die `bot-id` kann auf dem Bildschirm zur Bot-Verwaltung nachgeschlagen werden, auf den über die Bot-Veröffentlichungs-APIs zugegriffen werden kann und der in der linken Seitenleiste angezeigt wird. Beachten Sie das Ende der URL wie `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Hinweis]
> Wenn Sie eine benannte Umgebung verwenden (z.B. "dev"), ersetzen Sie `bedrockchatstack_usage_analysis.ddb_export` durch `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in der obigen Abfrage.

### Abfrage nach Benutzer-ID

Bearbeiten Sie `user-id` und `datehour`. Die `user-id` kann auf dem Bildschirm zur Bot-Verwaltung nachgeschlagen werden.

> [!Hinweis]
> Benutzernutzungsanalysen sind in Kürze verfügbar.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Hinweis]
> Wenn Sie eine benannte Umgebung verwenden (z.B. "dev"), ersetzen Sie `bedrockchatstack_usage_analysis.ddb_export` durch `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in der obigen Abfrage.