# Panduan Migrasi (v1 ke v2)

## TL;DR

- **Untuk pengguna v1.2 atau sebelumnya**: Naik taraf ke v1.4 dan cipta semula bot anda menggunakan Knowledge Base (KB). Selepas tempoh peralihan, setelah anda mengesahkan semuanya berfungsi seperti yang diharapkan dengan KB, teruskan dengan naik taraf ke v2.
- **Untuk pengguna v1.3**: Walaupun anda sudah menggunakan KB, adalah **sangat disyorkan** untuk naik taraf ke v1.4 dan cipta semula bot anda. Jika anda masih menggunakan pgvector, lakukan migrasi dengan mencipta semula bot anda menggunakan KB dalam v1.4.
- **Untuk pengguna yang ingin terus menggunakan pgvector**: Naik taraf ke v2 tidak disyorkan jika anda merancang untuk terus menggunakan pgvector. Naik taraf ke v2 akan mengalih keluar semua sumber berkaitan pgvector, dan sokongan pada masa hadapan tidak akan disediakan lagi. Teruskan menggunakan v1 dalam kes ini.
- Sila ambil perhatian bahawa **naik taraf ke v2 akan mengakibatkan penghapusan semua sumber berkaitan Aurora.** Kemas kini pada masa hadapan akan fokus secara eksklusif pada v2, dengan v1 akan dihentikan.

## Pengenalan

### Apa yang akan berlaku

Kemas kini v2 memperkenalkan perubahan besar dengan menggantikan pgvector pada Aurora Serverless dan pembenaman berasaskan ECS dengan [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Perubahan ini tidak serasi ke belakang.

### Mengapa repositori ini telah menggunakan Knowledge Bases dan menghentikan pgvector

Terdapat beberapa sebab untuk perubahan ini:

#### Ketepatan RAG yang Lebih Baik

- Knowledge Bases menggunakan OpenSearch Serverless sebagai backend, membolehkan carian hibrid dengan kedua-dua carian teks penuh dan vektor. Ini membawa kepada ketepatan yang lebih baik dalam menjawab soalan yang mengandungi kata nama khas, yang mana pgvector menghadapi kesukaran.
- Ia juga menyokong lebih banyak pilihan untuk meningkatkan ketepatan RAG, seperti pengelompokan dan penghuraian lanjutan.
- Knowledge Bases telah tersedia secara umum selama hampir setahun sejak Oktober 2024, dengan ciri-ciri seperti pelayaran web yang telah ditambah. Kemas kini masa hadapan dijangka, menjadikannya lebih mudah untuk menggunakan fungsi lanjutan dalam jangka panjang. Sebagai contoh, walaupun repositori ini belum melaksanakan ciri-ciri seperti pengimportan dari bucket S3 sedia ada (ciri yang kerap diminta) dalam pgvector, ia sudah disokong dalam KB (KnowledgeBases).

#### Penyelenggaraan

- Persediaan ECS + Aurora semasa bergantung kepada pelbagai perpustakaan, termasuk yang untuk penghuraian PDF, pelayaran web, dan pengekstrakan transkrip YouTube. Sebaliknya, penyelesaian terurus seperti Knowledge Bases mengurangkan beban penyelenggaraan untuk kedua-dua pengguna dan pasukan pembangunan repositori.

## Proses Penghijrahan (Ringkasan)

Kami amat mengesyorkan untuk menaik taraf ke v1.4 sebelum beralih ke v2. Dalam v1.4, anda boleh menggunakan kedua-dua bot pgvector dan Knowledge Base, membolehkan tempoh peralihan untuk mencipta semula bot pgvector sedia ada anda dalam Knowledge Base dan mengesahkan ia berfungsi seperti yang diharapkan. Walaupun dokumen RAG kekal sama, perlu diambil perhatian bahawa perubahan backend kepada OpenSearch mungkin menghasilkan keputusan yang sedikit berbeza, walaupun secara umumnya serupa, disebabkan perbezaan seperti algoritma k-NN.

Dengan menetapkan `useBedrockKnowledgeBasesForRag` kepada true dalam `cdk.json`, anda boleh mencipta bot menggunakan Knowledge Bases. Walau bagaimanapun, bot pgvector akan menjadi baca-sahaja, menghalang penciptaan atau pengeditan bot pgvector baharu.

![](../imgs/v1_to_v2_readonly_bot.png)

Dalam v1.4, [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) juga diperkenalkan. Disebabkan sekatan serantau Knowledge Bases, bucket S3 untuk memuat naik dokumen mesti berada di rantau yang sama dengan `bedrockRegion`. Kami mengesyorkan untuk membuat sandaran bucket dokumen sedia ada sebelum mengemas kini, untuk mengelakkan keperluan memuat naik semula dokumen dalam jumlah yang besar secara manual kemudian (kerana fungsi import bucket S3 tersedia).

## Proses Penghijrahan (Terperinci)

Langkah-langkah berbeza bergantung sama ada anda menggunakan v1.2 atau sebelumnya, atau v1.3.

![](../imgs/v1_to_v2_arch.png)

### Langkah-langkah untuk pengguna v1.2 atau sebelumnya

1. **Sandar bucket dokumen sedia ada anda (pilihan tetapi disyorkan).** Jika sistem anda sudah beroperasi, kami sangat mengesyorkan langkah ini. Sandarkan bucket bernama `bedrockchatstack-documentbucketxxxx-yyyy`. Sebagai contoh, kita boleh menggunakan [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Kemas kini ke v1.4**: Dapatkan tag v1.4 terkini, ubah suai `cdk.json`, dan deploy. Ikuti langkah-langkah berikut:

   1. Dapatkan tag terkini:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Ubah suai `cdk.json` seperti berikut:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Deploy perubahan:
      ```bash
      npx cdk deploy
      ```

3. **Cipta semula bot anda**: Cipta semula bot anda pada Knowledge Base dengan definisi yang sama (dokumen, saiz chunk, dll.) seperti bot pgvector. Jika anda mempunyai jumlah dokumen yang besar, memulihkan dari sandaran dalam langkah 1 akan memudahkan proses ini. Untuk memulihkan, kita boleh menggunakan pemulihan salinan merentas rantau. Untuk maklumat lanjut, lawati [di sini](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Untuk menentukan bucket yang dipulihkan, tetapkan bahagian `S3 Data Source` seperti berikut. Struktur laluan ialah `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Anda boleh menyemak ID pengguna pada kumpulan pengguna Cognito dan ID bot pada bar alamat pada skrin penciptaan bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Perhatikan bahawa beberapa ciri tidak tersedia pada Knowledge Bases, seperti sokongan perayapan web dan transkrip YouTube (Merancang untuk menyokong perayap web ([isu](https://github.com/aws-samples/bedrock-chat/issues/557))).** Juga, ingat bahawa penggunaan Knowledge Bases akan mengenakan caj untuk kedua-dua Aurora dan Knowledge Bases semasa peralihan.

4. **Buang API yang diterbitkan**: Semua API yang telah diterbitkan sebelumnya perlu diterbitkan semula sebelum menggunakan v2 kerana penghapusan VPC. Untuk melakukan ini, anda perlu memadamkan API sedia ada terlebih dahulu. Menggunakan [ciri Pengurusan API pentadbir](../ADMINISTRATOR_ms-MY.md) boleh memudahkan proses ini. Setelah penghapusan semua tindanan CloudFormation `APIPublishmentStackXXXX` selesai, persekitaran akan sedia.

5. **Deploy v2**: Selepas pelepasan v2, dapatkan sumber yang ditag dan deploy seperti berikut (ini akan mungkin setelah dikeluarkan):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Selepas menggunakan v2, **SEMUA BOT DENGAN AWALAN [Unsupported, Read-only] AKAN DISEMBUNYIKAN.** Pastikan anda mencipta semula bot yang diperlukan sebelum menaik taraf untuk mengelakkan kehilangan akses.

> [!Tip]
> Semasa pengemaskinian tindanan, anda mungkin menghadapi mesej berulang seperti: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." Dalam kes sedemikian, navigasi ke Management Console > EC2 > Network Interfaces dan cari BedrockChatStack. Padamkan antara muka yang dipaparkan yang berkaitan dengan nama ini untuk membantu memastikan proses penempatan yang lebih lancar.

### Langkah-langkah untuk pengguna v1.3

Seperti yang dinyatakan sebelum ini, dalam v1.4, Knowledge Bases mesti dicipta dalam bedrockRegion kerana sekatan serantau. Oleh itu, anda perlu mencipta semula KB. Jika anda telah menguji KB dalam v1.3, cipta semula bot dalam v1.4 dengan definisi yang sama. Ikuti langkah-langkah yang digariskan untuk pengguna v1.2.