# Penerbitan API

## Gambaran Keseluruhan

Sampel ini merangkumi ciri untuk menerbitkan API. Walaupun antara muka perbualan boleh menjadi mudah untuk pengesahan awal, pelaksanaan sebenar bergantung pada kes penggunaan tertentu dan pengalaman pengguna (UX) yang dikehendaki untuk pengguna akhir. Dalam sesetengah senario, antara muka perbualan mungkin menjadi pilihan yang diutamakan, manakala dalam kes lain, API kendiri mungkin lebih sesuai. Selepas pengesahan awal, sampel ini menyediakan keupayaan untuk menerbitkan bot yang disesuaikan mengikut keperluan projek. Dengan memasukkan tetapan untuk kuota, pendikit, sumber asal, dan sebagainya, satu titik akhir boleh diterbitkan bersama dengan kunci API, menawarkan fleksibiliti untuk pelbagai pilihan integrasi.

## Keselamatan

Penggunaan kunci API sahaja adalah tidak disyorkan seperti yang diterangkan dalam: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Oleh itu, sampel ini melaksanakan sekatan alamat IP yang ringkas melalui AWS WAF. Peraturan WAF digunakan secara umum merentasi aplikasi disebabkan pertimbangan kos, dengan andaian bahawa sumber-sumber yang ingin disekat berkemungkinan sama merentasi semua API yang dikeluarkan. **Sila patuhi dasar keselamatan organisasi anda untuk pelaksanaan sebenar.** Sila lihat juga bahagian [Seni Bina](#architecture).

## Cara menerbitkan API bot yang disesuaikan

### Prasyarat

Atas sebab tadbir urus, hanya pengguna terhad boleh menerbitkan bot. Sebelum penerbitan, pengguna mesti menjadi ahli kumpulan yang dipanggil `PublishAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Ambil perhatian bahawa id kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Tetapan Penerbitan API

Selepas log masuk sebagai pengguna `PublishedAllowed` dan mencipta bot, pilih `API PublishSettings`. Ambil perhatian bahawa hanya bot yang dikongsi boleh diterbitkan.
![](./imgs/bot_api_publish_screenshot.png)

Pada skrin berikutnya, kita boleh mengkonfigurasi beberapa parameter berkaitan pendikit. Untuk perincian, sila lihat juga: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Selepas penempatan, skrin berikut akan muncul di mana anda boleh mendapatkan URL titik akhir dan kunci api. Kita juga boleh menambah dan memadamkan kunci api.

![](./imgs/bot_api_publish_screenshot3.png)

## Seni Bina

API ini diterbitkan seperti gambar rajah berikut:

![](./imgs/published_arch.png)

WAF digunakan untuk pembatasan alamat IP. Alamat boleh dikonfigurasi dengan menetapkan parameter `publishedApiAllowedIpV4AddressRanges` dan `publishedApiAllowedIpV6AddressRanges` dalam `cdk.json`.

Apabila pengguna mengklik untuk menerbitkan bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) akan melancarkan tugas penempatan CDK untuk menyediakan tindanan API (Lihat juga: [Definisi CDK](../cdk/lib/api-publishment-stack.ts)) yang mengandungi API Gateway, Lambda dan SQS. SQS digunakan untuk memisahkan permintaan pengguna dan operasi LLM kerana penjanaan output mungkin melebihi 30 saat, iaitu had kuota API Gateway. Untuk mendapatkan output, anda perlu mengakses API secara tak segerak. Untuk maklumat lebih lanjut, sila lihat [Spesifikasi API](#api-specification).

Pelanggan perlu menetapkan `x-api-key` pada pengepala permintaan.

## Spesifikasi API

Lihat [di sini](https://aws-samples.github.io/bedrock-chat).