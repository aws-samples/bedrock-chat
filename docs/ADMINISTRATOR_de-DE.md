# Administratorfunktionen

Die Administratorfunktionen sind ein wichtiges Werkzeug, da sie wesentliche Einblicke in die Nutzung benutzerdefinierter Bots und das Benutzerverhalten liefern. Ohne diese Funktionalität wäre es für Administratoren schwierig zu verstehen, welche benutzerdefinierten Bots beliebt sind, warum sie beliebt sind und wer sie nutzt. Diese Informationen sind entscheidend für die Optimierung von Anweisungsprompts, die Anpassung von RAG-Datenquellen und die Identifizierung von intensiven Nutzern, die möglicherweise Einflussreiche sein könnten.

## Feedback-Schleife

Die Ausgabe von LLM entspricht möglicherweise nicht immer den Erwartungen des Benutzers. Manchmal erfüllt sie die Bedürfnisse des Benutzers nicht. Um LLMs effektiv in Geschäftsprozesse und den Alltag zu "integrieren", ist die Implementierung einer Feedback-Schleife unerlässlich. Bedrock Claude Chat verfügt über eine Feedbackfunktion, die es Benutzern ermöglicht, zu analysieren, warum Unzufriedenheit aufgetreten ist. Basierend auf den Analyseergebnissen können Benutzer die Prompts, RAG-Datenquellen und Parameter entsprechend anpassen.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Datenanalysten können auf Gesprächsprotokolle über [Amazon Athena](https://aws.amazon.com/jp/athena/) zugreifen. Wenn sie die Daten in [Jupyter Notebook](https://jupyter.org/) analysieren möchten, kann [dieses Notebook-Beispiel](../examples/notebooks/feedback_analysis_example.ipynb) als Referenz dienen.

## Administrator-Dashboard

Bietet derzeit einen grundlegenden Überblick über Chatbot- und Benutzernutzung mit Fokus auf der Aggregation von Daten für jeden Bot und Benutzer über bestimmte Zeiträume und Sortierung der Ergebnisse nach Nutzungsgebühren.

![](./imgs/admin_bot_analytics.png)

> [!Hinweis]
> Benutzernutzungsanalysen kommen bald.

### Voraussetzungen

Der Administrator-Benutzer muss Mitglied der Gruppe `Admin` sein, die über die Verwaltungskonsole > Amazon Cognito User Pools oder AWS CLI eingerichtet werden kann. Beachten Sie, dass die Benutzer-Pool-ID durch Zugriff auf CloudFormation > BedrockChatStack > Ausgaben > `AuthUserPoolIdxxxx` referenziert werden kann.

![](./imgs/group_membership_admin.png)

## Notizen

- Wie in der [Architektur](../README.md#architecture) beschrieben, werden die Administratorfeatures auf den S3-Bucket verweisen, der aus DynamoDB exportiert wurde. Bitte beachten Sie, dass aufgrund des stündlichen Exports die neuesten Gespräche möglicherweise nicht sofort angezeigt werden.

- Bei öffentlichen Bot-Nutzungen werden Bots, die während des angegebenen Zeitraums überhaupt nicht genutzt wurden, nicht aufgelistet.

- Bei Benutzernutzungen werden Benutzer, die das System während des angegebenen Zeitraums überhaupt nicht genutzt haben, nicht aufgelistet.

## Herunterladen von Gesprächsdaten

Sie können die Gesprächsprotokolle mithilfe von Athena und SQL abfragen. Um Protokolle herunterzuladen, öffnen Sie den Athena Query Editor über die Verwaltungskonsole und führen Sie SQL aus. Die folgenden Beispielabfragen sind nützlich zur Analyse von Anwendungsfällen. Feedback kann im Attribut `MessageMap` nachgeschlagen werden.

### Abfrage nach Bot-ID

Bearbeiten Sie `bot-id` und `datehour`. Die `bot-id` kann auf dem Bot-Verwaltungsbildschirm nachgeschlagen werden, auf den über die Bot-Veröffentlichungs-APIs zugegriffen werden kann und der in der linken Seitenleiste angezeigt wird. Beachten Sie das Ende der URL wie `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

### Abfrage nach Benutzer-ID

Bearbeiten Sie `user-id` und `datehour`. Die `user-id` kann auf dem Bot-Verwaltungsbildschirm nachgeschlagen werden.

> [!Hinweis]
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