# Panduan Migrasi (v0 ke v1)

Jika anda sudah menggunakan Bedrock Claude Chat dengan versi sebelumnya (~`0.4.x`), anda perlu mengikuti langkah-langkah di bawah untuk bermigrasi.

## Mengapa saya perlu melakukannya?

Kemas kini utama ini termasuk kemas kini keselamatan yang penting.

- Penyimpanan pangkalan data vektor (iaitu, pgvector pada Aurora PostgreSQL) kini disulitkan, yang mencetuskan penggantian semasa digunakan. Ini bermakna item vektor sedia ada akan dipadam.
- Kami memperkenalkan kumpulan pengguna Cognito `CreatingBotAllowed` untuk membataskan pengguna yang boleh membuat bot. Pengguna sedia ada tidak berada dalam kumpulan ini, jadi anda perlu melampirkan izin secara manual jika anda mahu mereka mempunyai keupayaan membuat bot. Lihat: [Personalisasi Bot](../../README.md#bot-personalization)

## Prasyarat

Baca [Panduan Migrasi Pangkalan Data](./DATABASE_MIGRATION_ms-MY.md) dan tentukan kaedah untuk memulihkan item.

## Langkah-langkah

### Migrasi stor vektor

- Buka terminal anda dan navigasi ke direktori projek
- Tarik cabang yang ingin anda deploy. Berikut adalah untuk cabang yang diinginkan (dalam kes ini, `v1`) dan tarik perubahan terkini:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Jika anda ingin memulihkan item dengan DMS, JANGAN LUPA untuk melumpuhkan putaran kata laluan dan catat kata laluan untuk mengakses pangkalan data. Jika memulihkan dengan skrip migrasi([migrate.py](./migrate.py)), anda tidak perlu mencatat kata laluan.
- Keluarkan semua [API yang diterbitkan](../PUBLISH_API_ms-MY.md) supaya CloudFormation dapat mengeluarkan kluster Aurora sedia ada.
- Jalankan [npx cdk deploy](../README.md#deploy-using-cdk) mencetuskan penggantian kluster Aurora dan MEMADAMKAN SEMUA ITEM VEKTOR.
- Ikuti [Panduan Migrasi Pangkalan Data](./DATABASE_MIGRATION_ms-MY.md) untuk memulihkan item vektor.
- Sahkan bahawa pengguna dapat menggunakan bot sedia ada yang mempunyai pengetahuan iaitu bot RAG.

### Lampirkan Izin CreatingBotAllowed

- Selepas deployment, semua pengguna tidak dapat membuat bot baharu.
- Jika anda ingin pengguna tertentu dapat membuat bot, tambahkan pengguna tersebut ke kumpulan `CreatingBotAllowed` menggunakan konsol pengurusan atau CLI.
- Sahkan sama ada pengguna dapat membuat bot. Perhatikan bahawa pengguna perlu log masuk semula.