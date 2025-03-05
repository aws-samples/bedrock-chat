# Ciri-ciri Pentadbir

Ciri-ciri pentadbir adalah alat yang penting kerana ia memberikan pandangan mendalam tentang penggunaan bot khusus dan tingkah laku pengguna. Tanpa fungsi ini, pentadbir akan menghadapi kesukaran untuk memahami bot khusus mana yang popular, mengapa ia popular, dan siapa yang menggunakannya. Maklumat ini sangat penting untuk mengoptimumkan arahan prompt, menyesuaikan sumber data RAG, dan mengenal pasti pengguna utama yang mungkin menjadi pengaruh.

## Gelung Maklum Balas

Output daripada LLM mungkin tidak sentiasa memenuhi jangkaan pengguna. Kadang-kadang ia gagal memuaskan keperluan pengguna. Untuk mengintegrasikan LLM ke dalam operasi perniagaan dan kehidupan seharian dengan berkesan, melaksanakan gelung maklum balas adalah penting. Bedrock Claude Chat dilengkapi dengan fitur maklum balas yang direka untuk membolehkan pengguna menganalisis mengapa ketidakpuasan berlaku. Berdasarkan keputusan analisis, pengguna dapat melaraskan arahan, sumber data RAG, dan parameter mengikut keperluan.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Penganalisis data boleh mengakses log perbualan menggunakan [Amazon Athena](https://aws.amazon.com/jp/athena/). Jika mereka ingin menganalisis data dengan [Jupyter Notebook](https://jupyter.org/), [contoh notebook ini](../examples/notebooks/feedback_analysis_example.ipynb) boleh dijadikan rujukan.

## Papan Pemuka Pentadbir

Kini menyediakan gambaran keseluruhan asas penggunaan chatbot dan pengguna, dengan fokus pada pengumpulan data untuk setiap bot dan pengguna dalam tempoh masa yang ditetapkan serta mengisih keputusan mengikut yuran penggunaan.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Analitik penggunaan pengguna akan datang tidak lama lagi.

### Prasyarat

Pengguna admin mesti menjadi ahli kumpulan yang dipanggil `Admin`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Perhatikan bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Nota

- Seperti yang dinyatakan dalam [arsitektur](../README.md#architecture), ciri-ciri pentadbir akan merujuk kepada bucket S3 yang dieksport dari DynamoDB. Sila ambil perhatian bahawa memandangkan eksport dilakukan sekali sejam, perbualan terkini mungkin tidak segera direfleksikan.

- Dalam penggunaan bot awam, bot yang tidak digunakan langsung dalam tempoh yang dinyatakan tidak akan disenaraikan.

- Dalam penggunaan pengguna, pengguna yang tidak menggunakan sistem sama sekali dalam tempoh yang dinyatakan tidak akan disenaraikan.

## Muat Turun Data Perbualan

Anda boleh membuat pertanyaan log perbualan menggunakan Athena, dengan SQL. Untuk memuat turun log, buka Athena Query Editor dari konsol pengurusan dan jalankan SQL. Berikut adalah beberapa contoh pertanyaan yang berguna untuk menganalisis kes penggunaan. Maklum balas boleh dirujuk dalam atribut `MessageMap`.

### Pertanyaan mengikut Bot ID

Edit `bot-id` dan `datehour`. `bot-id` boleh dirujuk pada skrin Pengurusan Bot, yang boleh diakses dari Bot Publish APIs, yang ditunjukkan pada sidebar kiri. Ambil perhatian bahagian akhir URL seperti `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

### Pertanyaan mengikut User ID

Edit `user-id` dan `datehour`. `user-id` boleh dirujuk pada skrin Pengurusan Bot.

> [!Nota]
> Analitik penggunaan pengguna akan datang tidak lama lagi.

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