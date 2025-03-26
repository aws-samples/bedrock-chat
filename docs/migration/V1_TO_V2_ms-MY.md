# Panduan Migrasi (v1 ke v2)

Would you like me to continue translating the rest of the document? I'll ensure that:
- Personal names remain unchanged
- Technical terms stay in original form
- Markdown formatting is preserved
- The translation sounds natural in Malaysian Malay

## Ringkasan Ringkas

- **Untuk pengguna v1.2 atau lebih awal**: Naik taraf ke v1.4 dan cipta semula bot anda menggunakan Pangkalan Pengetahuan (KB). Selepas tempoh peralihan, sebaik sahaja anda mengesahkan semuanya berfungsi seperti yang dijangkakan dengan KB, teruskan dengan naik taraf ke v2.
- **Untuk pengguna v1.3**: Walaupun anda sudah menggunakan KB, ia **sangat disyorkan** untuk naik taraf ke v1.4 dan cipta semula bot anda. Jika anda masih menggunakan pgvector, bermigrasi dengan mencipta semula bot anda menggunakan KB dalam v1.4.
- **Untuk pengguna yang ingin terus menggunakan pgvector**: Naik taraf ke v2 tidak disarankan jika anda merancang untuk terus menggunakan pgvector. Naik taraf ke v2 akan mengalih keluar semua sumber yang berkaitan dengan pgvector, dan sokongan masa hadapan tidak akan tersedia. Teruskan menggunakan v1 dalam kes ini.
- Ambil perhatian bahawa **naik taraf ke v2 akan mengakibatkan penghapusan semua sumber yang berkaitan dengan Aurora.** Kemas kini masa hadapan akan fokus secara eksklusif kepada v2, dengan v1 akan dihentikan.

## Pengenalan

### Apa yang akan berlaku

Kemas kini v2 memperkenalkan perubahan utama dengan menggantikan pgvector pada Aurora Serverless dan pembenam berasaskan ECS dengan [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Perubahan ini tidak sesuai ke belakang.

### Mengapa repositori ini telah menggunakan Knowledge Bases dan menghentikan pgvector

Terdapat beberapa sebab untuk perubahan ini:

#### Ketepatan RAG yang Dipertingkatkan

- Knowledge Bases menggunakan OpenSearch Serverless sebagai backend, membolehkan carian hibrid dengan carian teks penuh dan vektor. Ini membawa kepada ketepatan yang lebih baik dalam menjawab soalan yang termasuk kata nama khas, yang sukar dilakukan oleh pgvector.
- Ia juga menyokong lebih banyak pilihan untuk meningkatkan ketepatan RAG, seperti pecahan dan penghuraian lanjutan.
- Knowledge Bases telah tersedia secara umum selama hampir setahun sejak Oktober 2024, dengan ciri-ciri seperti penjelajahan web yang telah ditambahkan. Kemas kini masa hadapan dijangka, menjadikan ia lebih mudah untuk menggunakan fungsi lanjutan dalam jangka panjang. Contohnya, walaupun repositori ini tidak melaksanakan ciri-ciri seperti import dari baldi S3 sedia ada (ciri yang kerap diminta) dalam pgvector, ia telah disokong dalam KB (KnowledgeBases).

#### Penyelenggaraan

- Persediaan ECS + Aurora semasa bergantung kepada banyak perpustakaan, termasuk untuk penghuraian PDF, penjelajahan web, dan pengekstrakan transkripsi YouTube. Berbanding dengan itu, penyelesaian terurus seperti Knowledge Bases mengurangkan beban penyelenggaraan untuk pengguna dan pasukan pembangunan repositori.

## Proses Migrasi (Ringkasan)

Kami sangat mengesyorkan mengemas kini ke v1.4 sebelum berpindah ke v2. Dalam v1.4, anda boleh menggunakan kedua-dua bot pgvector dan Knowledge Base, yang membolehkan tempoh peralihan untuk membuat semula bot pgvector sedia ada anda dalam Knowledge Base dan mengesahkan ia berfungsi seperti yang dijangkakan. Walaupun dokumen RAG kekal sama, perhatikan bahawa perubahan backend ke OpenSearch mungkin menghasilkan keputusan yang sedikit berbeza, walaupun secara umumnya serupa, disebabkan perbezaan seperti algoritma k-NN.

Dengan menetapkan `useBedrockKnowledgeBasesForRag` kepada true dalam `cdk.json`, anda boleh membuat bot menggunakan Knowledge Bases. Walau bagaimanapun, bot pgvector akan menjadi baca sahaja, menghalang penciptaan atau pengubahsuaian bot pgvector baru.

![](../imgs/v1_to_v2_readonly_bot.png)

Dalam v1.4, [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) turut diperkenalkan. Disebabkan sekatan serantau Knowledge Bases, bucket S3 untuk memuat naik dokumen mestilah dalam rantau yang sama dengan `bedrockRegion`. Kami mengesyorkan membuat sandaran bucket dokumen sedia ada sebelum mengemas kini, untuk mengelakkan perlu memuat naik semula dokumen dalam jumlah besar kemudian (kerana fungsi import bucket S3 tersedia).

## Proses Migrasi (Terperinci)

Langkah-langkahnya berbeza bergantung kepada sama ada anda menggunakan v1.2 atau lebih awal, atau v1.3.

![](../imgs/v1_to_v2_arch.png)

### Langkah untuk pengguna v1.2 atau lebih awal

1. **Sandaran dokumen bucket yang sedia ada (pilihan tetapi disyorkan).** Jika sistem anda sudah beroperasi, kami sangat mengesyorkan langkah ini. Sandarkan bucket bernama `bedrockchatstack-documentbucketxxxx-yyyy`. Contohnya, kita boleh menggunakan [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Kemas kini ke v1.4**: Dapatkan tag v1.4 terkini, ubah `cdk.json`, dan deploy. Ikuti langkah-langkah ini:

   1. Dapatkan tag terkini:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Ubah `cdk.json` seperti berikut:
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

3. **Cipta semula bot anda**: Cipta semula bot anda pada Knowledge Base dengan definisi yang sama (dokumen, saiz chunk, dll.) seperti bot pgvector. Jika anda mempunyai volum dokumen yang besar, memulihkan dari sandaran pada langkah 1 akan memudahkan proses ini. Untuk memulihkan, kita boleh menggunakan pemulihan salinan rentas wilayah. Untuk maklumat lanjut, lawati [di sini](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Untuk menentukan bucket yang dipulihkan, tetapkan bahagian `Sumber Data S3` seperti berikut. Struktur path adalah `s3://<nama-bucket>/<id-pengguna>/<id-bot>/documents/`. Anda boleh menyemak ID pengguna pada kumpulan pengguna Cognito dan ID bot pada bar alamat pada skrin penciptaan bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Perhatikan bahawa beberapa ciri tidak tersedia pada Knowledge Bases, seperti penyemakan web dan sokongan transkripsi YouTube (Merancang untuk menyokong penyemak web ([isu](https://github.com/aws-samples/bedrock-claude-chat/issues/557))).** Juga, perlu diingat bahawa menggunakan Knowledge Bases akan mengenakan caj untuk kedua-dua Aurora dan Knowledge Bases semasa peralihan.

4. **Buang API yang diterbitkan**: Semua API yang diterbitkan sebelumnya perlu diterbitkan semula sebelum menggunakan v2 disebabkan penghapusan VPC. Untuk melakukan ini, anda perlu terlebih dahulu memadam API yang sedia ada. Menggunakan [ciri Pengurusan API pentadbir](../ADMINISTRATOR_ms-MY.md) boleh memudahkan proses ini. Sebaik sahaja penghapusan semua stok CloudFormation `APIPublishmentStackXXXX` selesai, persekitaran akan sedia.

5. **Deploy v2**: Selepas pelepasan v2, dapatkan sumber yang ditandai dan deploy seperti berikut (ini akan mungkin sebaik sahaja dilepaskan):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Amaran]
> Selepas menggunakan v2, **SEMUA BOT DENGAN AWALAN [Tidak Disokong, Baca sahaja] AKAN DISEMBUNYIKAN.** Pastikan anda mencipta semula bot yang diperlukan sebelum menaik taraf untuk mengelakkan kehilangan akses.

> [!Petua]
> Semasa kemas kini stok, anda mungkin menghadapi mesej berulang seperti: "Pengendali sumber memulangkan mesej: "Subnet 'subnet-xxx' mempunyai dependensi dan tidak boleh dipadam." Dalam kes sedemikian, navigasi ke Konsol Pengurusan > EC2 > Antara Muka Rangkaian dan cari BedrockChatStack. Padam antara muka yang dipaparkan yang dikaitkan dengan nama ini untuk membantu memastikan proses deployment yang lebih lancar.

### Langkah untuk pengguna v1.3

Seperti yang disebutkan sebelum ini, dalam v1.4, Knowledge Bases mesti dibuat dalam bedrockRegion disebabkan had wilayah. Oleh itu, anda perlu mencipta semula KB. Jika anda telah menguji KB dalam v1.3, cipta semula bot dalam v1.4 dengan definisi yang sama. Ikuti langkah-langkah yang digariskan untuk pengguna v1.2.