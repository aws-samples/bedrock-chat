# Panduan Penghijrahan (v2 ke v3)

## TL;DR

- V3 memperkenalkan kawalan kebenaran terperinci dan fungsi Bot Store, yang memerlukan perubahan skema DynamoDB
- **Sandarkan ConversationTable DynamoDB anda sebelum penghijrahan**
- Kemas kini URL repositori anda dari `bedrock-claude-chat` kepada `bedrock-chat`
- Jalankan skrip penghijrahan untuk menukar data anda kepada skema baharu
- Semua bot dan perbualan anda akan dikekalkan dengan model kebenaran baharu
- **PENTING: Semasa proses penghijrahan, aplikasi tidak akan tersedia kepada semua pengguna sehingga penghijrahan selesai. Proses ini biasanya mengambil masa sekitar 60 minit, bergantung pada jumlah data dan prestasi persekitaran pembangunan anda.**
- **PENTING: Semua API yang Diterbitkan mesti dipadamkan semasa proses penghijrahan.**
- **AMARAN: Proses penghijrahan tidak dapat menjamin kejayaan 100% untuk semua bot. Sila dokumentasikan konfigurasi bot penting anda sebelum penghijrahan sekiranya anda perlu membuatnya semula secara manual**

## Pengenalan

### Apa yang Baharu dalam V3

V3 memperkenalkan peningkatan penting kepada Bedrock Chat:

1. **Kawalan kebenaran terperinci**: Kawal akses kepada bot anda dengan kebenaran berasaskan kumpulan pengguna
2. **Bot Store**: Kongsi dan temui bot melalui pasaran berpusat
3. **Ciri-ciri pentadbiran**: Urus API, tandakan bot sebagai penting, dan analisis penggunaan bot

Ciri-ciri baharu ini memerlukan perubahan pada skema DynamoDB, menjadikan proses migrasi diperlukan untuk pengguna sedia ada.

### Mengapa Migrasi Ini Diperlukan

Model kebenaran baharu dan fungsi Bot Store memerlukan penstrukturan semula cara data bot disimpan dan diakses. Proses migrasi menukar bot dan perbualan sedia ada anda kepada skema baharu sambil mengekalkan semua data anda.

> [!WARNING]
> Notis Gangguan Perkhidmatan: **Semasa proses migrasi, aplikasi tidak akan tersedia kepada semua pengguna.** Rancang untuk melaksanakan migrasi ini semasa tempoh penyelenggaraan apabila pengguna tidak memerlukan akses kepada sistem. Aplikasi hanya akan tersedia semula selepas skrip migrasi berjaya selesai dan semua data telah ditukar dengan betul kepada skema baharu. Proses ini biasanya mengambil masa sekitar 60 minit, bergantung kepada jumlah data dan prestasi persekitaran pembangunan anda.

> [!IMPORTANT]
> Sebelum meneruskan migrasi: **Proses migrasi tidak dapat menjamin kejayaan 100% untuk semua bot**, terutamanya yang dibuat dengan versi lama atau dengan konfigurasi tersuai. Sila dokumentasikan konfigurasi bot penting anda (arahan, sumber pengetahuan, tetapan) sebelum memulakan proses migrasi sekiranya anda perlu membuatnya semula secara manual.

## Proses Migrasi

### Notis Penting Mengenai Keterlihatan Bot dalam V3

Dalam V3, **semua bot v2 dengan perkongsian awam yang diaktifkan akan boleh dicari dalam Bot Store.** Jika anda mempunyai bot yang mengandungi maklumat sensitif yang tidak mahu ditemui, pertimbangkan untuk menjadikannya peribadi sebelum bermigrasi ke V3.

### Langkah 1: Kenal pasti nama persekitaran anda

Dalam prosedur ini, `{YOUR_ENV_PREFIX}` ditentukan untuk mengenal pasti nama Stack CloudFormation anda. Jika anda menggunakan ciri [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), gantikan dengan nama persekitaran yang akan dimigrasi. Jika tidak, gantikan dengan rentetan kosong.

### Langkah 2: Kemas Kini URL Repositori (Disyorkan)

Repositori telah dinamakan semula daripada `bedrock-claude-chat` kepada `bedrock-chat`. Kemas kini repositori tempatan anda:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Langkah 3: Pastikan Anda Menggunakan Versi V2 Terkini

> [!WARNING]
> Anda MESTI mengemas kini ke v2.10.0 sebelum bermigrasi ke V3. **Melangkau langkah ini boleh menyebabkan kehilangan data semasa migrasi.**

Sebelum memulakan migrasi, pastikan anda menjalankan versi V2 terkini (**v2.10.0**). Ini memastikan anda mempunyai semua pembetulan pepijat dan penambahbaikan yang diperlukan sebelum menaik taraf ke V3:

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

### Langkah 4: Rekod Nama Jadual DynamoDB V2 Anda

Dapatkan nama ConversationTable V2 daripada output CloudFormation:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Pastikan untuk menyimpan nama jadual ini di lokasi yang selamat, kerana anda akan memerlukannya untuk skrip migrasi kemudian.

### Langkah 5: Sandar Jadual DynamoDB Anda

Sebelum meneruskan, buat sandaran ConversationTable DynamoDB anda menggunakan nama yang baru anda rekodkan:

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

### Langkah 6: Padam Semua API yang Diterbitkan

> [!IMPORTANT]
> Sebelum menggunakan V3, anda mesti memadam semua API yang diterbitkan untuk mengelakkan konflik nilai output Cloudformation semasa proses naik taraf.

1. Log masuk ke aplikasi anda sebagai pentadbir
2. Navigasi ke bahagian Admin dan pilih "API Management"
3. Semak senarai semua API yang diterbitkan
4. Padam setiap API yang diterbitkan dengan mengklik butang padam di sebelahnya

Anda boleh mendapatkan maklumat lanjut tentang penerbitan dan pengurusan API dalam dokumentasi [PUBLISH_API.md](../PUBLISH_API_ms-MY.md), [ADMINISTRATOR.md](../ADMINISTRATOR_ms-MY.md).

### Langkah 7: Tarik V3 dan Deploy

Tarik kod V3 terkini dan deploy:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Sebaik sahaja anda menggunakan V3, aplikasi tidak akan tersedia untuk semua pengguna sehingga proses migrasi selesai. Skema baru tidak serasi dengan format data lama, jadi pengguna tidak akan dapat mengakses bot atau perbualan mereka sehingga anda menyelesaikan skrip migrasi dalam langkah seterusnya.

### Langkah 8: Rekod Nama Jadual DynamoDB V3 Anda

Selepas menggunakan V3, anda perlu mendapatkan kedua-dua nama ConversationTable dan BotTable yang baharu:

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
> Pastikan untuk menyimpan nama jadual V3 ini bersama dengan nama jadual V2 anda yang disimpan sebelumnya, kerana anda akan memerlukan semuanya untuk skrip migrasi.

### Langkah 9: Jalankan Skrip Migrasi

Skrip migrasi akan menukar data V2 anda ke skema V3. Pertama, edit skrip migrasi `docs/migration/migrate_v2_v3.py` untuk menetapkan nama jadual dan wilayah anda:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Kemudian jalankan skrip menggunakan Poetry dari direktori backend:

> [!NOTE]
> Versi keperluan Python telah diubah kepada 3.13.0 atau lebih tinggi (Mungkin berubah dalam pembangunan masa hadapan. Lihat pyproject.toml). Jika anda mempunyai venv yang dipasang dengan versi Python yang berbeza, anda perlu membuangnya sekali.

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

Skrip migrasi akan menjana fail laporan dalam direktori semasa anda dengan butiran tentang proses migrasi. Periksa fail ini untuk memastikan semua data anda telah berjaya dimigrasi.

#### Mengendalikan Jumlah Data yang Besar

Untuk persekitaran dengan pengguna berat atau jumlah data yang besar, pertimbangkan pendekatan ini:

1. **Migrasikan pengguna secara individu**: Untuk pengguna dengan jumlah data yang besar, migrasikan mereka satu persatu:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Pertimbangan memori**: Proses migrasi memuatkan data ke dalam memori. Jika anda menghadapi ralat Out-Of-Memory (OOM), cuba:

   - Migrasikan satu pengguna pada satu masa
   - Menjalankan migrasi pada mesin dengan lebih banyak memori
   - Memecahkan migrasi kepada kumpulan pengguna yang lebih kecil

3. **Pantau migrasi**: Periksa fail laporan yang dijana untuk memastikan semua data dimigrasi dengan betul, terutamanya untuk set data yang besar.

### Langkah 10: Sahkan Aplikasi

Selepas migrasi, buka aplikasi anda dan sahkan:

- Semua bot anda tersedia
- Perbualan dikekalkan
- Kawalan kebenaran baharu berfungsi

### Pembersihan (Pilihan)

Selepas mengesahkan bahawa migrasi berjaya dan semua data anda boleh diakses dengan betul dalam V3, anda boleh memilih untuk memadam jadual perbualan V2 untuk menjimatkan kos:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Hanya padam jadual V2 selepas mengesahkan secara menyeluruh bahawa semua data penting anda telah berjaya dimigrasi ke V3. Kami mengesyorkan untuk menyimpan sandaran yang dibuat dalam Langkah 2 untuk sekurang-kurangnya beberapa minggu selepas migrasi, walaupun anda memadam jadual asal.

## Soalan Lazim V3

### Akses dan Kebenaran Bot

**Q: Apa yang berlaku jika bot yang saya gunakan dipadamkan atau kebenaran akses saya ditarik balik?**
A: Pengesahan diperiksa semasa perbualan, jadi anda akan hilang akses serta-merta.

**Q: Apa yang berlaku jika pengguna dipadamkan (contohnya, pekerja berhenti)?**
A: Data mereka boleh dipadamkan sepenuhnya dengan memadamkan semua item dari DynamoDB yang mempunyai ID pengguna mereka sebagai kunci partition (PK).

**Q: Bolehkah saya matikan perkongsian untuk bot awam yang penting?**
A: Tidak, admin perlu menandakan bot sebagai tidak penting terlebih dahulu sebelum mematikan perkongsian.

**Q: Bolehkah saya padamkan bot awam yang penting?**
A: Tidak, admin perlu menandakan bot sebagai tidak penting terlebih dahulu sebelum memadamkannya.

### Keselamatan dan Pelaksanaan

**Q: Adakah keselamatan peringkat baris (RLS) dilaksanakan untuk jadual bot?**
A: Tidak, memandangkan kepelbagaian corak akses. Pengesahan dilakukan semasa mengakses bot, dan risiko kebocoran metadata dianggap minimum berbanding dengan sejarah perbualan.

**Q: Apakah keperluan untuk menerbitkan API?**
A: Bot tersebut mestilah awam.

**Q: Adakah akan ada skrin pengurusan untuk semua bot peribadi?**
A: Tidak dalam keluaran awal V3. Walau bagaimanapun, item masih boleh dipadamkan dengan membuat pertanyaan menggunakan ID pengguna mengikut keperluan.

**Q: Adakah akan ada fungsi penandaan bot untuk pengalaman carian yang lebih baik?**
A: Tidak dalam keluaran awal V3, tetapi penandaan automatik berasaskan LLM mungkin ditambah dalam kemas kini akan datang.

### Pentadbiran

**Q: Apa yang boleh dilakukan oleh pentadbir?**
A: Pentadbir boleh:

- Mengurus bot awam (termasuk memeriksa bot kos tinggi)
- Mengurus API
- Menandakan bot awam sebagai penting

**Q: Bolehkah saya menjadikan bot yang dikongsi sebahagian sebagai penting?**
A: Tidak, hanya menyokong bot awam.

**Q: Bolehkah saya menetapkan keutamaan untuk bot yang disematkan?**
A: Pada keluaran awal, tidak.

### Konfigurasi Pengesahan

**Q: Bagaimana saya menyediakan pengesahan?**
A:

1. Buka konsol Amazon Cognito dan cipta kumpulan pengguna dalam kumpulan pengguna BrChat
2. Tambah pengguna ke kumpulan ini mengikut keperluan
3. Dalam BrChat, pilih kumpulan pengguna yang anda mahu benarkan akses semasa mengkonfigurasi tetapan perkongsian bot

Nota: Perubahan keahlian kumpulan memerlukan log masuk semula untuk berkuat kuasa. Perubahan akan dicerminkan semasa token diperbaharui, tetapi tidak semasa tempoh sah token ID (lalai 30 minit dalam V3, boleh dikonfigurasi melalui `tokenValidMinutes` dalam `cdk.json` atau `parameter.ts`).

**Q: Adakah sistem memeriksa dengan Cognito setiap kali bot diakses?**
A: Tidak, pengesahan diperiksa menggunakan token JWT untuk mengelakkan operasi I/O yang tidak perlu.

### Fungsi Carian

**Q: Adakah carian bot menyokong carian semantik?**
A: Tidak, hanya padanan teks separa disokong. Carian semantik (contohnya, "automobil" → "kereta", "EV", "kenderaan") tidak tersedia disebabkan kekangan semasa OpenSearch Serverless (Mac 2025).