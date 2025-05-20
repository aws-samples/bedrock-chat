# Panduan Migrasi (v2 ke v3)

Would you like me to continue translating the rest of the document? I'll ensure that I follow the critical requirements you specified:
- Personal names will remain unchanged
- URLs, links, code blocks, and technical terms in backticks will stay in their original form
- Markdown formatting will be preserved
- The structure and layout will remain the same
- The translation will be natural and technically accurate for Malaysian Malay (ms-MY)

## Ringkasan Singkat

- V3 memperkenalkan kawalan izin yang terperinci dan fungsi Bot Store, memerlukan perubahan skema DynamoDB
- **Backup Jadual Perbualan DynamoDB anda sebelum migrasi**
- Kemas kini URL repositori anda dari `bedrock-claude-chat` ke `bedrock-chat`
- Jalankan skrip migrasi untuk menukar data anda ke skema baru
- Semua bot dan perbualan anda akan dikekalkan dengan model izin baru
- **PENTING: Semasa proses migrasi, aplikasi akan tidak tersedia untuk semua pengguna sehingga migrasi selesai. Proses ini biasanya mengambil masa sekitar 60 minit, bergantung kepada jumlah data dan prestasi persekitaran pembangunan anda.**
- **PENTING: Semua API Yang Diterbitkan mesti dipadam semasa proses migrasi.**
- **AMARAN: Proses migrasi tidak dapat menjamin kejayaan 100% untuk semua bot. Sila dokumentasikan konfigurasi bot penting anda sebelum migrasi sekiranya anda perlu membuat semula secara manual**

## Pengenalan

### Apa yang Baru dalam V3

V3 memperkenalkan peningkatan yang ketara dalam Bedrock Chat:

1. **Kawalan izin terperinci**: Mengawal akses kepada bot anda dengan izin berdasarkan kumpulan pengguna
2. **Kedai Bot**: Kongsi dan temui bot melalui pusat pasaran
3. **Ciri-ciri pentadbiran**: Urus API, tandai bot sebagai penting, dan analisis penggunaan bot

Ciri-ciri baru ini memerlukan perubahan dalam skema DynamoDB, yang memerlukan proses migrasi untuk pengguna sedia ada.

### Mengapa Migrasi Ini Diperlukan

Model izin baru dan fungsi Kedai Bot memerlukan penyusunan semula cara data bot disimpan dan diakses. Proses migrasi ini menukar bot dan perbualan anda yang sedia ada kepada skema baru sambil mengekalkan semua data anda.

> [!AMARAN]
> Notis Gangguan Perkhidmatan: **Semasa proses migrasi, aplikasi akan tidak tersedia untuk semua pengguna.** Rancang untuk melakukan migrasi ini dalam tetingkap penyelenggaraan apabila pengguna tidak memerlukan akses kepada sistem. Aplikasi hanya akan tersedia semula selepas skrip migrasi berjaya diselesaikan dan semua data telah ditukar dengan betul ke skema baru. Proses ini biasanya mengambil masa kira-kira 60 minit, bergantung kepada jumlah data dan prestasi persekitaran pembangunan anda.

> [!PENTING]
> Sebelum meneruskan migrasi: **Proses migrasi tidak dapat menjamin kejayaan 100% untuk semua bot**, terutamanya yang dibuat dengan versi lama atau dengan konfigurasi khusus. Sila dokumentasikan konfigurasi bot penting anda (arahan, sumber pengetahuan, tetapan) sebelum memulakan proses migrasi sekiranya anda perlu membuat semula secara manual.

## Proses Migrasi

### Notis Penting Tentang Keterlihatan Bot dalam V3

Dalam V3, **semua bot v2 dengan perkongsian awam diaktifkan akan dapat dicari dalam Bot Store.** Jika anda mempunyai bot yang mengandungi maklumat sensitif yang anda tidak mahu didapati, pertimbangkan untuk menjadikannya peribadi sebelum bermigrasi ke V3.

### Langkah 1: Kenal pasti nama persekitaran anda

Dalam prosedur ini, `{YOUR_ENV_PREFIX}` ditentukan untuk mengenal pasti nama Tindanan CloudFormation anda. Jika anda menggunakan fitur [Menggunakan Berbagai Persekitaran](../../README.md#deploying-multiple-environments), gantikan dengan nama persekitaran yang akan dimigrasikan. Jika tidak, gantikan dengan rentetan kosong.

### Langkah 2: Kemas Kini URL Repositori (Disyorkan)

Repositori telah dinamakan semula dari `bedrock-claude-chat` kepada `bedrock-chat`. Kemas kini repositori tempatan anda:

```bash
# Semak URL remote semasa anda
git remote -v

# Kemas kini URL remote
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Sahkan perubahan
git remote -v
```

### Langkah 3: Pastikan Anda Berada pada Versi V2 Terkini

> [!WARNING]
> Anda MESTI mengemas kini ke v2.10.0 sebelum bermigrasi ke V3. **Melangkau langkah ini mungkin mengakibatkan kehilangan data semasa migrasi.**

Sebelum memulakan migrasi, pastikan anda menjalankan versi terkini V2 (**v2.10.0**). Ini memastikan anda mempunyai semua pembetulan dan penambahbaikan yang diperlukan sebelum naik taraf ke V3:

```bash
# Dapatkan tag terkini
git fetch --tags

# Tukar ke versi V2 terkini
git checkout v2.10.0

# Gunakan versi V2 terkini
cd cdk
npm ci
npx cdk deploy --all
```

### Langkah 4: Rekod Nama Jadual DynamoDB V2 Anda

Dapatkan nama ConversationTable V2 dari output CloudFormation:

```bash
# Dapatkan nama ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Pastikan menyimpan nama jadual ini di lokasi yang selamat, kerana anda akan memerlukannya untuk skrip migrasi kemudian.

### Langkah 5: Sandaran Jadual DynamoDB Anda

Sebelum meneruskan, cipta sandaran ConversationTable DynamoDB menggunakan nama yang baru anda rekod:

```bash
# Cipta sandaran jadual V2 anda
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Semak status sandaran tersedia
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Langkah 6: Padam Semua API yang Diterbitkan

> [!IMPORTANT]
> Sebelum menggunakan V3, anda mesti memadam semua API yang diterbitkan untuk mengelakkan konflik nilai output Cloudformation semasa proses naik taraf.

1. Log masuk ke aplikasi anda sebagai pentadbir
2. Navigasi ke bahagian Admin dan pilih "Pengurusan API"
3. Semak senarai semua API yang diterbitkan
4. Padam setiap API yang diterbitkan dengan mengklik butang padam di sebelahnya

Anda boleh mencari maklumat lanjut tentang penerbitan dan pengurusan API dalam dokumentasi [PUBLISH_API.md](../PUBLISH_API_ms-MY.md), [ADMINISTRATOR.md](../ADMINISTRATOR_ms-MY.md) masing-masing.

### Langkah 7: Tarik V3 dan Gunakan

Tarik kod V3 terkini dan gunakan:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Sebaik sahaja anda menggunakan V3, aplikasi akan tidak tersedia untuk semua pengguna sehingga proses migrasi selesai. Skema baru tidak serasi dengan format data lama, jadi pengguna tidak dapat mengakses bot atau perbualan mereka sehingga anda menyelesaikan skrip migrasi pada langkah seterusnya.

### Langkah 8: Rekod Nama Jadual DynamoDB V3 Anda

Selepas menggunakan V3, anda perlu mendapatkan nama ConversationTable dan BotTable yang baru:

```bash
# Dapatkan nama ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Dapatkan nama BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Pastikan menyimpan nama jadual V3 ini bersama nama jadual V2 yang disimpan sebelum ini, kerana anda akan memerlukannya untuk skrip migrasi.

### Langkah 9: Jalankan Skrip Migrasi

Skrip migrasi akan menukar data V2 anda ke skema V3. Pertama, edit skrip migrasi `docs/migration/migrate_v2_v3.py` untuk menetapkan nama jadual dan wilayah anda:

```python
# Wilayah di mana dynamodb terletak
REGION = "ap-northeast-1" # Ganti dengan wilayah anda

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Ganti dengan nilai yang anda rekod dalam Langkah 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Ganti dengan nilai yang anda rekod dalam Langkah 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Ganti dengan nilai yang anda rekod dalam Langkah 8
```

Kemudian jalankan skrip menggunakan Poetry dari direktori backend:

> [!NOTE]
> Versi keperluan Python telah diubah kepada 3.13.0 atau lebih baru (Mungkin berubah dalam pembangunan masa hadapan. Lihat pyproject.toml). Jika anda mempunyai venv yang dipasang dengan versi Python yang berbeza, anda perlu membuangnya sekali.

```bash
# Navigasi ke direktori backend
cd backend

# Pasang dependensi jika anda belum melakukannya
poetry install

# Jalankan percubaan kering terlebih dahulu untuk melihat apa yang akan dimigrasikan
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Jika semuanya kelihatan baik, jalankan migrasi sebenar
poetry run python ../docs/migration/migrate_v2_v3.py

# Sahkan migrasi berjaya
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Skrip migrasi akan menjana fail laporan dalam direktori semasa anda dengan butiran tentang proses migrasi. Semak fail ini untuk memastikan semua data anda telah dimigrasikan dengan betul.

#### Mengendalikan Volum Data Besar

Untuk persekitaran dengan pengguna yang berat atau jumlah data yang besar, pertimbangkan pendekatan ini:

1. **Migrasikan pengguna secara individu**: Untuk pengguna dengan volum data besar, migrasikan mereka satu per satu:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Pertimbangan memori**: Proses migrasi memuatkan data ke dalam memori. Jika anda menghadapi ralat Keluar Dari Memori (OOM), cuba:

   - Migrasikan seorang pengguna pada satu masa
   - Jalankan migrasi pada mesin dengan memori yang lebih
   - Memecahkan migrasi kepada kelompok pengguna yang lebih kecil

3. **Pantau migrasi**: Semak fail laporan yang dijana untuk memastikan semua data dimigrasikan dengan betul, terutamanya untuk set data yang besar.

### Langkah 10: Sahkan Aplikasi

Selepas migrasi, buka aplikasi anda dan sahkan:

- Semua bot anda tersedia
- Perbualan dikekalkan
- Kawalan izin baru berfungsi

### Pembersihan (Pilihan)

Selepas mengesahkan migrasi berjaya dan semua data anda dapat diakses dengan betul dalam V3, anda boleh secara pilihan memadam jadual perbualan V2 untuk menjimatkan kos:

```bash
# Padam jadual perbualan V2 (HANYA selepas mengesahkan migrasi berjaya)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Hanya padamkan jadual V2 selepas menyemak dengan teliti bahawa semua data penting anda telah berjaya dimigrasikan ke V3. Kami mencadangkan menyimpan sandaran yang dibuat dalam Langkah 2 selama beberapa minggu selepas migrasi, walaupun anda memadam jadual asal.

## V3 Soalan Lazim

### Akses Bot dan Kebenaran

**S: Apa yang berlaku jika bot yang saya gunakan dipadamkan atau kebenaran akses saya dialih keluar?**
A: Pengesahan disemak semasa sembang, jadi anda akan kehilangan akses serta-merta.

**S: Apa yang berlaku jika pengguna dipadamkan (contohnya, pekerja meninggalkan syarikat)?**
A: Data mereka boleh dipadamkan sepenuhnya dengan memadamkan semua item dari DynamoDB dengan ID pengguna mereka sebagai kunci partition (PK).

**S: Bolehkah saya mematikan perkongsian untuk bot awam yang penting?**
A: Tidak, pentadbir mesti menandakan bot sebagai tidak penting terlebih dahulu sebelum mematikan perkongsian.

**S: Bolehkah saya memadamkan bot awam yang penting?**
A: Tidak, pentadbir mesti menandakan bot sebagai tidak penting terlebih dahulu sebelum memadam.

### Keselamatan dan Pelaksanaan

**S: Adakah keselamatan peringkat baris (RLS) dilaksanakan untuk jadual bot?**
A: Tidak, memandangkan kepelbagaian corak akses. Pengesahan dilakukan semasa mengakses bot, dan risiko bocoran metadata dianggap minimum berbanding sejarah perbualan.

**S: Apakah keperluan untuk menerbitkan API?**
A: Bot mesti awam.

**S: Adakah akan ada skrin pengurusan untuk semua bot peribadi?**
A: Tidak dalam keluaran V3 awal. Walau bagaimanapun, item masih boleh dipadamkan dengan pertanyaan menggunakan ID pengguna mengikut keperluan.

**S: Adakah akan ada fungsi penandaan bot untuk pengalaman carian yang lebih baik?**
A: Tidak dalam keluaran V3 awal, tetapi penandaan automatik berasaskan LLM mungkin ditambah dalam kemas kini masa hadapan.

### Pentadbiran

**S: Apa yang boleh dilakukan oleh pentadbir?**
A: Pentadbir boleh:

- Menguruskan bot awam (termasuk menyemak bot berkos tinggi)
- Menguruskan API
- Menandakan bot awam sebagai penting

**S: Bolehkah saya menjadikan bot separa kongsi sebagai penting?**
A: Tidak, hanya menyokong bot awam.

**S: Bolehkah saya menetapkan keutamaan untuk bot yang dipinkan?**
A: Pada keluaran awal, tidak.

### Konfigurasi Pengesahan

**S: Bagaimana saya menyediakan pengesahan?**
A:

1. Buka konsol Amazon Cognito dan buat kumpulan pengguna dalam kumpulan pengguna BrChat
2. Tambahkan pengguna ke kumpulan ini mengikut keperluan
3. Dalam BrChat, pilih kumpulan pengguna yang anda ingin membenarkan akses semasa mengkonfigurasi tetapan perkongsian bot

Nota: Perubahan keahlian kumpulan memerlukan log masuk semula. Perubahan direfleksikan semasa refresh token, tetapi tidak semasa tempoh kesahihan token ID (lalai 30 minit dalam V3, boleh dikonfigurasi oleh `tokenValidMinutes` dalam `cdk.json` atau `parameter.ts`).

**S: Adakah sistem menyemak dengan Cognito setiap kali bot diakses?**
A: Tidak, pengesahan disemak menggunakan token JWT untuk mengelakkan operasi I/O yang tidak perlu.

### Fungsi Carian

**S: Adakah carian bot menyokong carian semantik?**
A: Tidak, hanya separa pemadanan teks disokong. Carian semantik (contohnya, "automobil" → "kereta", "EV", "kenderaan") tidak tersedia disebabkan kekangan OpenSearch Serverless semasa (Mac 2025).