# Ciri-ciri pentadbiran

## Prasyarat

Pengguna admin mestilah menjadi ahli kumpulan yang dipanggil `Admin`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Ambil perhatian bahawa id kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Tandakan bot awam sebagai Penting

Bot awam kini boleh ditandakan sebagai "Penting" oleh pentadbir. Bot yang ditandakan sebagai Penting akan dipaparkan dalam bahagian "Penting" di kedai bot, menjadikannya mudah diakses oleh pengguna. Ini membolehkan pentadbir menyematkan bot penting yang mereka mahu semua pengguna gunakan.

### Contoh

- Bot Pembantu HR: Membantu pekerja dengan soalan dan tugas berkaitan HR.
- Bot Sokongan IT: Menyediakan bantuan untuk isu teknikal dalaman dan pengurusan akaun.
- Bot Panduan Polisi Dalaman: Menjawab soalan lazim tentang peraturan kehadiran, polisi keselamatan, dan peraturan dalaman lain.
- Bot Pembiasaan Pekerja Baharu: Membimbing pekerja baharu melalui prosedur dan penggunaan sistem pada hari pertama mereka.
- Bot Maklumat Faedah: Menerangkan program faedah syarikat dan perkhidmatan kebajikan.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Gelung maklum balas

Output daripada LLM mungkin tidak sentiasa memenuhi jangkaan pengguna. Kadangkala ia gagal memenuhi keperluan pengguna. Untuk "mengintegrasikan" LLM secara berkesan dalam operasi perniagaan dan kehidupan harian, pelaksanaan gelung maklum balas adalah penting. Bedrock Chat dilengkapi dengan ciri maklum balas yang direka untuk membolehkan pengguna menganalisis mengapa ketidakpuasan timbul. Berdasarkan hasil analisis, pengguna boleh menyesuaikan prompt, sumber data RAG, dan parameter dengan sewajarnya.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Penganalisis data boleh mengakses log perbualan menggunakan [Amazon Athena](https://aws.amazon.com/jp/athena/). Jika mereka ingin menganalisis data menggunakan [Jupyter Notebook](https://jupyter.org/), [contoh notebook ini](../examples/notebooks/feedback_analysis_example.ipynb) boleh dijadikan rujukan.

## Papan Pemuka

Pada masa ini menyediakan gambaran asas tentang penggunaan bot perbualan dan pengguna, dengan fokus kepada pengumpulan data bagi setiap bot dan pengguna dalam tempoh masa yang ditetapkan dan menyusun hasil mengikut yuran penggunaan.

![](./imgs/admin_bot_analytics.png)

## Nota

- Seperti yang dinyatakan dalam [arkitektur](../README.md#architecture), ciri-ciri pentadbir akan merujuk kepada bucket S3 yang dieksport dari DynamoDB. Sila ambil perhatian bahawa memandangkan eksport dilakukan sekali setiap jam, perbualan terkini mungkin tidak dapat dilihat dengan serta-merta.

- Dalam penggunaan bot awam, bot yang langsung tidak digunakan dalam tempoh yang ditetapkan tidak akan disenaraikan.

- Dalam penggunaan pengguna, pengguna yang langsung tidak menggunakan sistem dalam tempoh yang ditetapkan tidak akan disenaraikan.

> [!Important]
> Jika anda menggunakan pelbagai persekitaran (dev, prod, dsb.), nama pangkalan data Athena akan merangkumi awalan persekitaran. Selain daripada `bedrockchatstack_usage_analysis`, nama pangkalan data akan menjadi:
>
> - Untuk persekitaran lalai: `bedrockchatstack_usage_analysis`
> - Untuk persekitaran bernama: `<env-prefix>_bedrockchatstack_usage_analysis` (contoh: `dev_bedrockchatstack_usage_analysis`)
>
> Tambahan pula, nama jadual akan merangkumi awalan persekitaran:
>
> - Untuk persekitaran lalai: `ddb_export`
> - Untuk persekitaran bernama: `<env-prefix>_ddb_export` (contoh: `dev_ddb_export`)
>
> Pastikan anda menyesuaikan pertanyaan anda dengan sewajarnya apabila bekerja dengan pelbagai persekitaran.

## Muat turun data perbualan

Anda boleh membuat pertanyaan log perbualan menggunakan Athena dengan SQL. Untuk memuat turun log, buka Athena Query Editor dari konsol pengurusan dan jalankan SQL. Berikut adalah beberapa contoh pertanyaan yang berguna untuk menganalisis kes penggunaan. Maklum balas boleh dirujuk dalam atribut `MessageMap`.

### Pertanyaan mengikut ID Bot

Sunting `bot-id` dan `datehour`. `bot-id` boleh dirujuk pada skrin Pengurusan Bot, yang boleh diakses dari API Bot Publish, yang ditunjukkan pada bar sisi kiri. Perhatikan bahagian akhir URL seperti `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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
> Jika menggunakan persekitaran bernama (contohnya, "dev"), gantikan `bedrockchatstack_usage_analysis.ddb_export` dengan `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dalam pertanyaan di atas.

### Pertanyaan mengikut ID Pengguna

Sunting `user-id` dan `datehour`. `user-id` boleh dirujuk pada skrin Pengurusan Bot.

> [!Note]
> Analisis penggunaan pengguna akan datang tidak lama lagi.

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
> Jika menggunakan persekitaran bernama (contohnya, "dev"), gantikan `bedrockchatstack_usage_analysis.ddb_export` dengan `dev_bedrockchatstack_usage_analysis.dev_ddb_export` dalam pertanyaan di atas.