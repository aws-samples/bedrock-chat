# Panduan Migrasi (v0 ke v1)

Jika anda telah menggunakan Bedrock Chat dengan versi sebelumnya (~`0.4.x`), anda perlu mengikuti langkah-langkah di bawah untuk melakukan migrasi.

## Mengapa saya perlu melakukannya?

Kemas kini utama ini merangkumi pengemaskinian keselamatan yang penting.

- Pangkalan data vektor (iaitu, pgvector pada Aurora PostgreSQL) kini disulitkan, yang akan mencetuskan penggantian apabila dilancarkan. Ini bermakna item vektor sedia ada akan dipadamkan.
- Kami memperkenalkan kumpulan pengguna Cognito `CreatingBotAllowed` untuk menghadkan pengguna yang boleh mencipta bot. Pengguna sedia ada tidak berada dalam kumpulan ini, jadi anda perlu melampirkan kebenaran secara manual jika anda mahu mereka mempunyai keupayaan untuk mencipta bot. Lihat: [Personalisasi Bot](../../README.md#bot-personalization)

## Prasyarat

Baca [Panduan Penghijrahan Pangkalan Data](./DATABASE_MIGRATION_ms-MY.md) dan tentukan kaedah untuk memulihkan item.

## Langkah-langkah

### Penghijrahan stor vektor

- Buka terminal anda dan navigasi ke direktori projek
- Tarik cabang yang anda ingin deploy. Berikut adalah untuk cabang yang dikehendaki (dalam kes ini, `v1`) dan tarik perubahan terkini:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Jika anda ingin memulihkan item dengan DMS, JANGAN LUPA untuk menyahaktifkan putaran kata laluan dan catat kata laluan untuk mengakses pangkalan data. Jika memulihkan dengan skrip penghijrahan ([migrate_v0_v1.py](./migrate_v0_v1.py)), anda tidak perlu mencatat kata laluan.
- Buang semua [API yang diterbitkan](../PUBLISH_API_ms-MY.md) supaya CloudFormation boleh membuang kluster Aurora yang sedia ada.
- Jalankan [npx cdk deploy](../README.md#deploy-using-cdk) mencetuskan penggantian kluster Aurora dan MEMADAM SEMUA ITEM VEKTOR.
- Ikut [Panduan Penghijrahan Pangkalan Data](./DATABASE_MIGRATION_ms-MY.md) untuk memulihkan item vektor.
- Sahkan bahawa pengguna boleh menggunakan bot sedia ada yang mempunyai pengetahuan iaitu bot RAG.

### Tambah kebenaran CreatingBotAllowed

- Selepas penempatan, semua pengguna tidak akan dapat membuat bot baharu.
- Jika anda mahu pengguna tertentu dapat membuat bot, tambah pengguna tersebut ke dalam kumpulan `CreatingBotAllowed` menggunakan konsol pengurusan atau CLI.
- Sahkan sama ada pengguna boleh membuat bot. Perhatikan bahawa pengguna perlu log masuk semula.