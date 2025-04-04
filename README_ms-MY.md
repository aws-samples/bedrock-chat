# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Warning]
>
> **V2 telah dikeluarkan. Untuk mengemas kini, sila semak semula [panduan migrasi](./migration/V1_TO_V2_ms-MY.md) dengan teliti.** Tanpa sebarang perhatian, **BOT DARI V1 AKAN MENJADI TIDAK BOLEH DIGUNAKAN.**

Chatbot pelbagai bahasa yang menggunakan model LLM yang disediakan oleh [Amazon Bedrock](https://aws.amazon.com/bedrock/) untuk AI generatif.

### Tonton Gambaran Keseluruhan dan Pemasangan di YouTube

[![Overview](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Perbualan Asas

![](./imgs/demo.gif)

### Personalisasi Bot

Tambahkan arahan anda sendiri dan berikan pengetahuan luar melalui URL atau fail (a.k.a [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Bot boleh dikongsi di kalangan pengguna aplikasi. Bot yang disesuaikan juga boleh diterbitkan sebagai API berasingan (Lihat [butiran](./PUBLISH_API_ms-MY.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Atas sebab tadbir urus, hanya pengguna yang dibenarkan dapat membuat bot yang disesuaikan. Untuk membenarkan penciptaan bot yang disesuaikan, pengguna mestilah ahli kumpulan yang dipanggil `CreatingBotAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Ambil perhatian bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Papan pemuka pentadbir

<details>
<summary>Papan pemuka pentadbir</summary>

Analisis penggunaan untuk setiap pengguna / bot pada papan pemuka pentadbir. [butiran](./ADMINISTRATOR_ms-MY.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Ejen yang didayakan oleh LLM

<details>
<summary>Ejen yang didayakan oleh LLM</summary>

Dengan menggunakan [fungsi Ejen](./AGENT_ms-MY.md), chatbot anda boleh secara automatik mengendalikan tugas yang lebih kompleks. Contohnya, untuk menjawab soalan pengguna, Ejen boleh mendapatkan maklumat yang diperlukan daripada alat luar atau memecahkan tugas kepada beberapa langkah untuk diproses.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Penggunaan Mudah

- Di kawasan us-east-1, buka [Akses Model Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Urus akses model` > Tandakan semua `Anthropic / Claude 3`, semua `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` dan `Cohere / Embed Multilingual` kemudian `Simpan perubahan`.

<details>
<summary>Tangkapan Layar</summary>

![](./imgs/model_screenshot.png)

</details>

- Buka [CloudShell](https://console.aws.amazon.com/cloudshell/home) di kawasan tempat anda ingin menggunakan
- Jalankan penggunaan melalui arahan berikut. Jika anda ingin menetapkan versi untuk digunakan atau perlu menggunakan polisi keselamatan, sila tentukan parameter yang sesuai dari [Parameter Pilihan](#parameter-pilihan).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Anda akan ditanya sama ada pengguna baru atau menggunakan v2. Jika anda bukan pengguna yang berterusan dari v0, sila masukkan `y`.

### Parameter Pilihan

Anda boleh menetapkan parameter berikut semasa penggunaan untuk meningkatkan keselamatan dan penyesuaian:

- **--disable-self-register**: Matikan pendaftaran sendiri (lalai: didayakan). Jika bendera ini ditetapkan, anda perlu membuat semua pengguna pada cognito dan ia tidak akan membenarkan pengguna mendaftar akaun mereka sendiri.
- **--enable-lambda-snapstart**: Dayakan [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (lalai: dilumpuhkan). Jika bendera ini ditetapkan, ia meningkatkan masa permulaan sejuk untuk fungsi Lambda, memberikan masa respons yang lebih cepat untuk pengalaman pengguna yang lebih baik.
- **--ipv4-ranges**: Senarai yang dipisahkan koma bagi julat IPv4 yang dibenarkan. (lalai: membenarkan semua alamat ipv4)
- **--ipv6-ranges**: Senarai yang dipisahkan koma bagi julat IPv6 yang dibenarkan. (lalai: membenarkan semua alamat ipv6)
- **--disable-ipv6**: Matikan sambungan melalui IPv6. (lalai: didayakan)
- **--allowed-signup-email-domains**: Senarai yang dipisahkan koma bagi domain e-mel yang dibenarkan untuk pendaftaran. (lalai: tiada sekatan domain)
- **--bedrock-region**: Tentukan kawasan di mana bedrock tersedia. (lalai: us-east-1)
- **--repo-url**: Repo Bedrock Claude Chat khusus untuk digunakan, jika diforked atau kawalan sumber khusus. (lalai: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Versi Bedrock Claude Chat untuk digunakan. (lalai: versi terkini dalam pembangunan)
- **--cdk-json-override**: Anda boleh mengatasi mana-mana nilai konteks CDK semasa penggunaan menggunakan blok JSON override. Ini membolehkan anda mengubah konfigurasi tanpa mengedit fail cdk.json secara langsung.

Contoh penggunaan:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

JSON override mesti mengikuti struktur yang sama seperti cdk.json. Anda boleh mengatasi mana-mana nilai konteks termasuk:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Dan nilai konteks lain yang ditakrifkan dalam cdk.json

> [!Nota]
> Nilai override akan digabungkan dengan konfigurasi cdk.json yang sedia ada semasa masa penggunaan dalam AWS code build. Nilai yang ditentukan dalam override akan mengambil keutamaan berbanding nilai dalam cdk.json.

#### Contoh arahan dengan parameter:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Selepas kira-kira 35 minit, anda akan mendapat output berikut, yang boleh anda akses dari pelayar anda

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Skrin pendaftaran akan muncul seperti yang ditunjukkan di atas, di mana anda boleh mendaftar e-mel anda dan log masuk.

> [!Penting]
> Tanpa menetapkan parameter pilihan, kaedah penggunaan ini membenarkan sesiapa yang mengetahui URL untuk mendaftar. Untuk kegunaan pengeluaran, sangat disyorkan untuk menambahkan sekatan alamat IP dan melumpuhkan pendaftaran sendiri untuk mengurangkan risiko keselamatan (anda boleh mentakrifkan allowed-signup-email-domains untuk menyekat pengguna supaya hanya alamat e-mel dari domain syarikat anda yang boleh mendaftar). Gunakan kedua-dua ipv4-ranges dan ipv6-ranges untuk sekatan alamat IP, dan lumpuhkan pendaftaran sendiri dengan menggunakan disable-self-register semasa melaksanakan ./bin.

> [!PETUA]
> Jika `Frontend URL` tidak muncul atau Bedrock Claude Chat tidak berfungsi dengan baik, ia mungkin masalah dengan versi terkini. Dalam kes ini, sila tambahkan `--version "v1.2.6"` ke parameter dan cuba penggunaan semula.

## Seni Bina

Ia adalah seni bina yang dibina di atas perkhidmatan terurus AWS, menghapuskan keperluan pengurusan infrastruktur. Dengan menggunakan Amazon Bedrock, tiada keperluan untuk berkomunikasi dengan API di luar AWS. Ini membolehkan pengplotan aplikasi yang boleh diukur, boleh dipercayai, dan selamat.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Pangkalan data NoSQL untuk menyimpan sejarah perbualan
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Titik akhir API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Penghantaran aplikasi frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Pembatasan alamat IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Pengesahan pengguna
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Perkhidmatan terurus untuk menggunakan model asas melalui API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Menyediakan antara muka terurus untuk Generasi Perolehan Semula ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), menawarkan perkhidmatan untuk menyematkan dan mengurai dokumen
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Menerima acara dari aliran DynamoDB dan melancarkan Step Functions untuk menyematkan pengetahuan luar
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Mengatur saluran pemasukan untuk menyematkan pengetahuan luar ke dalam Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Berkhidmat sebagai pangkalan data backend untuk Bedrock Knowledge Bases, menyediakan ciri carian teks penuh dan carian vektor, membolehkan perolehan semula maklumat yang tepat
- [Amazon Athena](https://aws.amazon.com/athena/): Perkhidmatan pertanyaan untuk menganalisis baldi S3

![](./imgs/arch.png)

## Deploy menggunakan CDK

Deployment Super-mudah menggunakan [AWS CodeBuild](https://aws.amazon.com/codebuild/) untuk melakukan deployment melalui CDK secara dalaman. Bahagian ini menerangkan prosedur untuk deployment terus dengan CDK.

- Sila pastikan mempunyai persekitaran UNIX, Docker dan runtime Node.js. Jika tidak, anda boleh menggunakan [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Penting]
> Jika ruang storan tidak mencukupi dalam persekitaran tempatan semasa deployment, CDK bootstrapping mungkin menghasilkan ralat. Jika anda berjalan di Cloud9 dll., kami mencadangkan mengembangkan saiz volum contoh sebelum deployment.

- Klon repositori ini

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Pasang pakej npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Jika perlu, edit entri berikut dalam [cdk.json](./cdk/cdk.json) jika perlu.

  - `bedrockRegion`: Wilayah di mana Bedrock tersedia. **NOTA: Bedrock TIDAK menyokong semua wilayah untuk sekarang.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Julat Alamat IP yang dibenarkan.
  - `enableLambdaSnapStart`: Secara lalai adalah true. Tetapkan ke false jika deployment ke [wilayah yang tidak menyokong Lambda SnapStart untuk fungsi Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Sebelum deployment CDK, anda perlu bekerja dengan Bootstrap sekali untuk wilayah yang anda deploy.

```
npx cdk bootstrap
```

- Deploy projek sampel ini

```
npx cdk deploy --require-approval never --all
```

- Anda akan mendapatkan output yang serupa dengan berikut. URL aplikasi web akan dikeluarkan dalam `BedrockChatStack.FrontendURL`, jadi sila akses dari pelayar anda.

```sh
 ✅  BedrockChatStack

✨  Masa Deployment: 78.57s

Output:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Mentakrifkan Parameter

Anda boleh mentakrifkan parameter untuk deployment anda dalam dua cara: menggunakan `cdk.json` atau menggunakan fail `parameter.ts` yang selamat dari segi jenis.

#### Menggunakan cdk.json (Kaedah Tradisional)

Cara tradisional untuk mengkonfigurasi parameter adalah dengan mengedit fail `cdk.json`. Pendekatan ini mudah tetapi tidak mempunyai semakan jenis:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Menggunakan parameter.ts (Kaedah Selamat Jenis yang Disyorkan)

Untuk keselamatan jenis dan pengalaman pembangun yang lebih baik, anda boleh menggunakan fail `parameter.ts` untuk mentakrifkan parameter anda:

```typescript
// Takrifkan parameter untuk persekitaran lalai
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Takrifkan parameter untuk persekitaran tambahan
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Jimat kos untuk persekitaran dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Ketersediaan yang dipertingkatkan untuk pengeluaran
});
```

> [!Nota]
> Pengguna sedia ada boleh terus menggunakan `cdk.json` tanpa sebarang perubahan. Pendekatan `parameter.ts` disyorkan untuk deployment baru atau apabila anda perlu mengurus berbagai persekitaran.

### Deployment Berbilang Persekitaran

Anda boleh deploy berbilang persekitaran dari satu pangkalan kod menggunakan fail `parameter.ts` dan pilihan `-c envName`.

#### Prasyarat

1. Takrifkan persekitaran anda dalam `parameter.ts` seperti yang ditunjukkan di atas
2. Setiap persekitaran akan mempunyai set sumbernya sendiri dengan awalan khusus persekitaran

#### Perintah Deployment

Untuk deploy persekitaran tertentu:

```bash
# Deploy persekitaran dev
npx cdk deploy --all -c envName=dev

# Deploy persekitaran prod
npx cdk deploy --all -c envName=prod
```

Jika tiada persekitaran dinyatakan, persekitaran "default" digunakan:

```bash
# Deploy persekitaran default
npx cdk deploy --all
```

#### Nota Penting

1. **Penamaan Tindihan**:

   - Tindihan utama untuk setiap persekitaran akan mempunyai awalan nama persekitaran (contoh: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Walau bagaimanapun, tindihan bot tersuai (`BrChatKbStack*`) dan tindihan penerbitan API (`ApiPublishmentStack*`) tidak menerima awalan persekitaran kerana ia dibuat secara dinamik pada masa larian

2. **Penamaan Sumber**:

   - Hanya beberapa sumber menerima awalan persekitaran dalam nama mereka (contoh: jadual `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Kebanyakan sumber mengekalkan nama asal mereka tetapi diasingkan dengan berada dalam tindihan yang berbeza

3. **Pengenalan Persekitaran**:

   - Semua sumber ditandai dengan tag `CDKEnvironment` yang mengandungi nama persekitaran
   - Anda boleh menggunakan tag ini untuk mengenal pasti persekitaran yang sumber itu milik
   - Contoh: `CDKEnvironment: dev` atau `CDKEnvironment: prod`

4. **Ganti Persekitaran Default**: Jika anda mentakrifkan persekitaran "default" dalam `parameter.ts`, ia akan menggantikan tetapan dalam `cdk.json`. Untuk terus menggunakan `cdk.json`, jangan mentakrifkan persekitaran "default" dalam `parameter.ts`.

5. **Keperluan Persekitaran**: Untuk membuat persekitaran selain "default", anda mesti menggunakan `parameter.ts`. Pilihan `-c envName` sendiri tidak mencukupi tanpa definisi persekitaran yang sepadan.

6. **Pengasingan Sumber**: Setiap persekitaran mencipta set sumbernya sendiri, membolehkan anda mempunyai persekitaran pembangunan, ujian, dan pengeluaran dalam akaun AWS yang sama tanpa konflik.

## Lain-lain

### Konfigurasi Generasi Teks Lalai

Pengguna boleh melaraskan [parameter generasi teks](https://docs.anthropic.com/claude/reference/complete_post) dari skrin penciptaan bot tersuai. Jika bot tidak digunakan, parameter lalai yang ditetapkan dalam [config.py](./backend/app/config.py) akan digunakan.

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Hapus Sumber Daya

Jika menggunakan cli dan CDK, sila `npx cdk destroy`. Jika tidak, akses [CloudFormation](https://console.aws.amazon.com/cloudformation/home) dan kemudian hapus `BedrockChatStack` dan `FrontendWafStack` secara manual. Sila ambil perhatian bahawa `FrontendWafStack` berada di kawasan `us-east-1`.

### Tetapan Bahasa

Aset ini secara automatik mengesan bahasa menggunakan [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Anda boleh menukar bahasa dari menu aplikasi. Sebagai alternatif, anda boleh menggunakan Query String untuk menetapkan bahasa seperti yang ditunjukkan di bawah.

> `https://example.com?lng=ja`

### Nyahdayakan Pendaftaran Sendiri

Sampel ini mempunyai pendaftaran sendiri diaktifkan secara lalai. Untuk menyahdayakan pendaftaran sendiri, buka [cdk.json](./cdk/cdk.json) dan tukar `selfSignUpEnabled` kepada `false`. Jika anda mengkonfigurasi [penyedia identiti luar](#external-identity-provider), nilainya akan diabaikan dan secara automatik dimatikan.

### Hadkan Domain untuk Alamat E-mel Pendaftaran

Secara lalai, sampel ini tidak menyekat domain untuk alamat e-mel pendaftaran. Untuk membenarkan pendaftaran hanya dari domain tertentu, buka `cdk.json` dan nyatakan domain sebagai senarai dalam `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Penyedia Identiti Luar

Sampel ini menyokong penyedia identiti luar. Kini kami menyokong [Google](./idp/SET_UP_GOOGLE_ms-MY.md) dan [penyedia OIDC tersuai](./idp/SET_UP_CUSTOM_OIDC_ms-MY.md).

### Tambah pengguna baru ke kumpulan secara automatik

Sampel ini mempunyai kumpulan berikut untuk memberi izin kepada pengguna:

- [`Admin`](./ADMINISTRATOR_ms-MY.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ms-MY.md)

Jika anda ingin pengguna yang baru dicipta secara automatik menyertai kumpulan, anda boleh menyatakannya dalam [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Secara lalai, pengguna yang baru dicipta akan disertakan ke kumpulan `CreatingBotAllowed`.

### Konfigurasi Replika RAG

`enableRagReplicas` adalah pilihan dalam [cdk.json](./cdk/cdk.json) yang mengawal tetapan replika untuk pangkalan data RAG, khususnya Pangkalan Pengetahuan menggunakan Amazon OpenSearch Serverless.

- **Lalai**: true
- **true**: Meningkatkan ketersediaan dengan mengaktifkan replika tambahan, sesuai untuk persekitaran pengeluaran tetapi meningkatkan kos.
- **false**: Mengurangkan kos dengan menggunakan replika yang lebih sedikit, sesuai untuk pembangunan dan pengujian.

Ini adalah tetapan peringkat akaun/kawasan, mempengaruhi keseluruhan aplikasi dan bukannya bot individu.

> [!Nota]
> Sehingga Jun 2024, Amazon OpenSearch Serverless menyokong 0.5 OCU, menurunkan kos kemasukan untuk beban kerja berskala kecil. Penerapan pengeluaran boleh bermula dengan 2 OCU, manakala beban kerja pembangunan/ujian boleh menggunakan 1 OCU. OpenSearch Serverless secara automatik menskalakan berdasarkan permintaan beban kerja. Untuk maklumat lanjut, lawati [pengumuman](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Inferens rentas wilayah

[Inferens rentas wilayah](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) membolehkan Amazon Bedrock untuk menghantar permintaan inferens model secara dinamik merentasi pelbagai wilayah AWS, meningkatkan kelulusan dan ketahanan semasa tempoh permintaan puncak. Untuk mengkonfigurasi, edit `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) meningkatkan masa permulaan sejuk untuk fungsi Lambda, memberikan masa tindak balas yang lebih cepat untuk pengalaman pengguna yang lebih baik. Sebaliknya, untuk fungsi Python, terdapat [caj bergantung pada saiz cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) dan [tidak tersedia di beberapa kawasan](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) pada masa ini. Untuk menyahdayakan SnapStart, edit `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Konfigurasi Domain Tersuai

Anda boleh mengkonfigurasi domain tersuai untuk pengagihan CloudFront dengan menetapkan parameter berikut dalam [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Nama domain tersuai untuk aplikasi sembang anda (contohnya chat.example.com)
- `hostedZoneId`: ID zona yang di-host Route 53 di mana rekod DNS akan dicipta

Apabila parameter ini disediakan, pengplotan akan secara automatik:

- Mencipta sijil ACM dengan pengesahan DNS di kawasan us-east-1
- Mencipta rekod DNS yang diperlukan dalam zona yang di-host Route 53 anda
- Mengkonfigurasi CloudFront untuk menggunakan domain tersuai anda

> [!Nota]
> Domain mesti diuruskan oleh Route 53 dalam akaun AWS anda. ID zona yang di-host boleh didapati dalam konsol Route 53.

### Pembangunan Tempatan

Lihat [PEMBANGUNAN TEMPATAN](./LOCAL_DEVELOPMENT_ms-MY.md).

### Sumbangan

Terima kasih kerana mempertimbangkan untuk menyumbang kepada repositori ini! Kami mengalu-alukan pembetulan pepijat, terjemahan bahasa (i18n), penambahbaikan ciri, [alat ejen](./docs/AGENT.md#how-to-develop-your-own-tools), dan penambahbaikan lain.

Untuk penambahbaikan ciri dan penambahbaikan lain, **sebelum membuat Permintaan Tarik, kami sangat menghargai jika anda boleh membuat Isu Permintaan Ciri untuk membincangkan pendekatan dan butiran pelaksanaan. Untuk pembetulan pepijat dan terjemahan bahasa (i18n), teruskan dengan membuat Permintaan Tarik secara terus.**

Sila lihat garis panduan berikut sebelum menyumbang:

- [Pembangunan Tempatan](./LOCAL_DEVELOPMENT_ms-MY.md)
- [MENYUMBANG](./CONTRIBUTING_ms-MY.md)

## Kenalan

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Penyumbang Utama

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Penyumbang

[![penyumbang bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Lesen

Pustaka ini dibenarkan di bawah Lesen MIT-0. Lihat [fail LESEN](./LICENSE).