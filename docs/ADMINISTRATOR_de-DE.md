# Verwaltungsfunktionen

## Voraussetzungen

Der Admin-Benutzer muss Mitglied einer Gruppe namens `Admin` sein, die über die Management-Konsole > Amazon Cognito User pools oder aws cli eingerichtet werden kann. Beachten Sie, dass die User Pool ID über CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx` abgerufen werden kann.

![](./imgs/group_membership_admin.png)

## Öffentliche Bots als "Essentiell" markieren

Öffentliche Bots können jetzt von Administratoren als "Essentiell" markiert werden. Als essentiell markierte Bots werden im Bereich "Essentiell" des Bot-Stores angezeigt, wodurch sie für Benutzer leicht zugänglich sind. Dies ermöglicht es Administratoren, wichtige Bots hervorzuheben, die von allen Benutzern verwendet werden sollen.

### Beispiele

- HR Assistant Bot: Unterstützt Mitarbeiter bei HR-bezogenen Fragen und Aufgaben.
- IT Support Bot: Bietet Unterstützung bei internen technischen Problemen und Kontoverwaltung.
- Internal Policy Guide Bot: Beantwortet häufig gestellte Fragen zu Anwesenheitsregeln, Sicherheitsrichtlinien und anderen internen Vorschriften.
- New Employee Onboarding Bot: Führt neue Mitarbeiter durch Prozesse und Systemnutzung an ihrem ersten Tag.
- Benefits Information Bot: Erklärt betriebliche Vorsorgeprogramme und Sozialleistungen.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Feedback-Schleife

Die Ausgabe von LLM entspricht möglicherweise nicht immer den Erwartungen des Benutzers. Manchmal werden die Bedürfnisse des Benutzers nicht erfüllt. Um LLMs effektiv in Geschäftsprozesse und den Alltag zu "integrieren", ist die Implementierung einer Feedback-Schleife unerlässlich. Bedrock Chat ist mit einer Feedback-Funktion ausgestattet, die es Benutzern ermöglicht zu analysieren, warum Unzufriedenheit entstanden ist. Basierend auf den Analyseergebnissen können Benutzer die Prompts, RAG-Datenquellen und Parameter entsprechend anpassen.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Datenanalysten können über [Amazon Athena](https://aws.amazon.com/jp/athena/) auf Gesprächsprotokolle zugreifen. Wenn sie die Daten mit [Jupyter Notebook](https://jupyter.org/) analysieren möchten, kann [dieses Notebook-Beispiel](../examples/notebooks/feedback_analysis_example.ipynb) als Referenz dienen.

## Dashboard

Bietet derzeit einen grundlegenden Überblick über die Nutzung von Chatbots und Benutzern, wobei der Fokus auf der Aggregation von Daten für jeden Bot und Benutzer über bestimmte Zeiträume liegt und die Ergebnisse nach Nutzungsgebühren sortiert werden.

![](./imgs/admin_bot_analytics.png)

## Hinweise

- Wie in der [Architektur](../README.md#architecture) beschrieben, greifen die Admin-Funktionen auf den aus DynamoDB exportierten S3-Bucket zu. Bitte beachten Sie, dass der Export nur einmal pro Stunde durchgeführt wird, weshalb die neuesten Konversationen möglicherweise nicht sofort sichtbar sind.

- Bei der öffentlichen Bot-Nutzung werden Bots, die während des angegebenen Zeitraums überhaupt nicht verwendet wurden, nicht aufgelistet.

- Bei der Benutzernutzung werden Benutzer, die das System während des angegebenen Zeitraums überhaupt nicht genutzt haben, nicht aufgelistet.

> [!Important]
> Wenn Sie mehrere Umgebungen verwenden (dev, prod, etc.), wird der Athena-Datenbankname das Umgebungspräfix enthalten. Statt `bedrockchatstack_usage_analysis` lautet der Datenbankname:
>
> - Für Standardumgebung: `bedrockchatstack_usage_analysis`
> - Für benannte Umgebungen: `<env-prefix>_bedrockchatstack_usage_analysis` (z.B. `dev_bedrockchatstack_usage_analysis`)
>
> Zusätzlich wird der Tabellenname das Umgebungspräfix enthalten:
>
> - Für Standardumgebung: `ddb_export`
> - Für benannte Umgebungen: `<env-prefix>_ddb_export` (z.B. `dev_ddb_export`)
>
> Stellen Sie sicher, dass Sie Ihre Abfragen entsprechend anpassen, wenn Sie mit mehreren Umgebungen arbeiten.

## Gesprächsdaten herunterladen

Sie können die Gesprächsprotokolle mit Athena über SQL abfragen. Um Protokolle herunterzuladen, öffnen Sie den Athena Query Editor in der Management Console und führen Sie SQL aus. Im Folgenden finden Sie einige Beispielabfragen, die für die Analyse von Anwendungsfällen nützlich sind. Feedback kann im Attribut `MessageMap` eingesehen werden.

### Abfrage nach Bot-ID

Bearbeiten Sie `bot-id` und `datehour`. Die `bot-id` kann im Bot Management Bildschirm eingesehen werden, der über die Bot Publish APIs in der linken Seitenleiste zugänglich ist. Beachten Sie den letzten Teil der URL wie `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

> [!Note]
> Bei Verwendung einer benannten Umgebung (z.B. "dev"), ersetzen Sie `bedrockchatstack_usage_analysis.ddb_export` durch `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in der obigen Abfrage.

### Abfrage nach Benutzer-ID

Bearbeiten Sie `user-id` und `datehour`. Die `user-id` kann im Bot Management Bildschirm eingesehen werden.

> [!Note]
> Benutzernutzungsanalysen werden in Kürze verfügbar sein.

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

> [!Note]
> Bei Verwendung einer benannten Umgebung (z.B. "dev"), ersetzen Sie `bedrockchatstack_usage_analysis.ddb_export` durch `dev_bedrockchatstack_usage_analysis.dev_ddb_export` in der obigen Abfrage.