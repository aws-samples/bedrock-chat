# Ciri-ciri Pentadbir

Ciri-ciri pentadbir adalah alat yang sangat penting kerana ia memberikan pandangan mendalam yang penting tentang penggunaan bot tersuai dan tingkah laku pengguna. Tanpa fungsi ini, akan sukar bagi pentadbir untuk memahami bot tersuai mana yang popular, mengapa mereka popular, dan siapa yang menggunakannya. Maklumat ini amat kritikal untuk mengoptimumkan arahan prompt, menyesuaikan sumber data RAG, dan mengenal pasti pengguna yang kerap yang mungkin akan menjadi pengaruh.

## Gelung Maklum Balas

Output daripada LLM mungkin tidak sentiasa memenuhi jangkaan pengguna. Kadang-kadang ia gagal memuaskan keperluan pengguna. Untuk mengintegrasikan LLM dengan berkesan ke dalam operasi perniagaan dan kehidupan seharian, melaksanakan gelung maklum balas adalah penting. Bedrock Claude Chat dilengkapi dengan fitur maklum balas yang direka untuk membolehkan pengguna menganalisis mengapa ketidakpuasan berlaku. Berdasarkan keputusan analisis, pengguna boleh melaraskan arahan, sumber data RAG, dan parameter yang sesuai.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Penganalisis data boleh mengakses log perbualan menggunakan [Amazon Athena](https://aws.amazon.com/jp/athena/). Jika mereka ingin menganalisis data dengan [Jupyter Notebook](https://jupyter.org/), [contoh notebook ini](../examples/notebooks/feedback_analysis_example.ipynb) boleh menjadi rujukan.

## Papan Pemuka Pentadbir

Pada masa ini menyediakan gambaran keseluruhan asas penggunaan chatbot dan pengguna, dengan fokus pada pengumpulan data untuk setiap bot dan pengguna dalam tempoh masa yang ditetapkan dan menyusun keputusan mengikut yuran penggunaan.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Analitik penggunaan pengguna akan datang tidak lama lagi.

### Prasyarat

Pengguna admin mesti menjadi ahli kumpulan yang dipanggil `Admin`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Perhatikan bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Nota

- Seperti yang dinyatakan dalam [arsitektur](../README.md#architecture), ciri-ciri pentadbir akan merujuk kepada bucket S3 yang dieksport dari DynamoDB. Sila ambil perhatian bahawa memandangkan eksport dilakukan sekali sejam, perbualan terkini mungkin tidak segera direfleksikan.

- Dalam penggunaan bot awam, bot yang tidak digunakan langsung dalam tempoh yang ditetapkan tidak akan disenaraikan.

- Dalam penggunaan pengguna, pengguna yang tidak menggunakan sistem langsung dalam tempoh yang ditetapkan tidak akan disenaraikan.

> [!Penting] > **Nama Pangkalan Data Pelbagai Persekitaran**
>
> Jika anda menggunakan pelbagai persekitaran (dev, prod, dll.), nama pangkalan data Athena akan termasuk awalan persekitaran. Daripada `bedrockchatstack_usage_analysis`, nama pangkalan data akan menjadi:
>
> - Untuk persekitaran lalai: `bedrockchatstack_usage_analysis`
> - Untuk persekitaran bernama: `<awalan-env>_bedrockchatstack_usage_analysis` (contohnya, `dev_bedrockchatstack_usage_analysis`)
>
> Tambahan pula, nama jadual akan termasuk awalan persekitaran:
>
> - Untuk persekitaran lalai: `ddb_export`
> - Untuk persekitaran bernama: `<awalan-env>_ddb_export` (contohnya, `dev_ddb_export`)
>
> Pastikan untuk melaraskan pertanyaan anda dengan sewajarnya apabila bekerja dengan pelbagai persekitaran.

## Muat turun data perbualan

Anda boleh mendapatkan log perbualan menggunakan Athena dengan SQL. Untuk memuat turun log, buka Athena Query Editor dari konsol pengurusan dan jalankan SQL. Berikut adalah beberapa contoh pertanyaan yang berguna untuk menganalisis kes penggunaan. Maklum balas boleh dirujuk dalam atribut `MessageMap`.

### Pertanyaan mengikut ID Bot

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

> [!Nota]
> Jika menggunakan persekitaran bernama (contohnya "dev"), gantikan `bedrockchatstack_usage_analysis.ddb_export` dengan `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dalam pertanyaan di atas.

### Pertanyaan mengikut ID Pengguna

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

> [!Nota]
> Jika menggunakan persekitaran bernama (contohnya "dev"), gantikan `bedrockchatstack_usage_analysis.ddb_export` dengan `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dalam pertanyaan di atas.