# Penerbitan API

## Gambaran Keseluruhan

Contoh ini termasuk fitur untuk menerbitkan API. Walaupun antara muka sembang boleh menjadi mudah untuk pengesahan awal, pelaksanaan sebenar bergantung kepada kes penggunaan khusus dan pengalaman pengguna (UX) yang dikehendaki untuk pengguna akhir. Dalam beberapa senario, antara muka sembang mungkin menjadi pilihan yang lebih disukai, manakala dalam senario lain, API kendiri mungkin lebih sesuai. Selepas pengesahan awal, contoh ini menyediakan kemampuan untuk menerbitkan bot yang disesuaikan mengikut keperluan projek. Dengan memasukkan tetapan untuk kuota, pengawal aliran, asal, dan sebagainya, titik akhir dapat diterbitkan bersama kunci API, menawarkan fleksibiliti untuk pelbagai pilihan integrasi.

## Keselamatan

Penggunaan hanya kunci API tidak disarankan seperti yang diterangkan dalam: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Oleh itu, contoh ini melaksanakan sekatan alamat IP yang mudah melalui AWS WAF. Peraturan WAF digunakan secara umum merentasi aplikasi kerana pertimbangan kos, dengan andaian bahawa sumber yang ingin disekat berkemungkinan sama merentasi semua API yang dikeluarkan. **Sila patuhi polisi keselamatan organisasi anda untuk pelaksanaan sebenar.** Lihat juga bahagian [Seni Bina](#architecture).

## Cara Menerbitkan Bot API Tersuai

### Prasyarat

Atas sebab-sebab tadbir urus, hanya pengguna terhad yang boleh menerbitkan bot. Sebelum menerbitkan, pengguna mesti menjadi ahli kumpulan yang dipanggil `PublishAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Perhatikan bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Tetapan Penerbitan API

Selepas log masuk sebagai pengguna `PublishedAllowed` dan membuat bot, pilih `API PublishSettings`. Perhatikan bahawa hanya bot yang dikongsi boleh diterbitkan.
![](./imgs/bot_api_publish_screenshot.png)

Pada skrin berikut, kita boleh mengkonfigurasi beberapa parameter berkaitan pengawal trafik. Untuk maklumat lanjut, sila lihat: [Pengawal trafik permintaan API untuk keluaran yang lebih baik](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Selepas penghantaran, skrin berikut akan muncul di mana anda boleh mendapatkan URL endpoint dan kunci API. Kita juga boleh menambah dan memadamkan kunci API.

![](./imgs/bot_api_publish_screenshot3.png)

## Senibina

API diterbitkan seperti diagram berikut:

![](./imgs/published_arch.png)

WAF digunakan untuk pembatasan alamat IP. Alamat dapat dikonfigurasi dengan menetapkan parameter `publishedApiAllowedIpV4AddressRanges` dan `publishedApiAllowedIpV6AddressRanges` dalam `cdk.json`.

Sebaik sahaja pengguna mengklik untuk menerbitkan bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) melancarkan tugas deployment CDK untuk memperuntukkan stack API (Lihat juga: [Definisi CDK](../cdk/lib/api-publishment-stack.ts)) yang mengandungi API Gateway, Lambda dan SQS. SQS digunakan untuk memisahkan permintaan pengguna dan operasi LLM kerana menjana output mungkin melebihi 30 saat, yang merupakan had kuota API Gateway. Untuk mengambil output, perlu mengakses API secara tidak serentak. Untuk maklumat lanjut, lihat [Spesifikasi API](#api-specification).

Klien perlu menetapkan `x-api-key` pada pengepala permintaan.

## Spesifikasi API

Lihat [di sini](https://aws-samples.github.io/bedrock-claude-chat).