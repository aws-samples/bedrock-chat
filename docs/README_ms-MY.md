<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md)

Platform AI generatif pelbagai bahasa yang dikuasakan oleh [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Menyokong sembang, bot tersuai dengan pengetahuan (RAG), perkongsian bot melalui kedai bot, dan pengautomatan tugas menggunakan ejen.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 telah dikeluarkan. Untuk mengemas kini, sila semak semula panduan migrasi [migration guide](./migration/V2_TO_V3_ms-MY.md) dengan teliti.** Tanpa pengawasan, **BOT DARI V2 AKAN MENJADI TIDAK BOLEH DIGUNAKAN.**

### Personalisasi Bot / Kedai Bot

Tambahkan arahan dan pengetahuan anda sendiri (a.k.a [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Bot boleh dikongsi antara pengguna aplikasi melalui kedai bot. Bot tersuai juga boleh diterbitkan sebagai API berasingan (Lihat [butiran](./PUBLISH_API_ms-MY.md)).

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Anda juga boleh mengimport [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/) yang sedia ada.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Atas sebab tadbir urus, hanya pengguna yang dibenarkan sahaja yang boleh membuat bot tersuai. Untuk membenarkan penciptaan bot tersuai, pengguna mesti menjadi ahli kumpulan yang dipanggil `CreatingBotAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Ambil perhatian bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Ciri-ciri Pentadbiran

Pengurusan API, Tandai bot sebagai penting, Analisis penggunaan bot. [butiran](./ADMINISTRATOR_ms-MY.md)

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Ejen

Dengan menggunakan [fungsi Ejen](./AGENT_ms-MY.md), chatbot anda boleh mengendalikan tugas yang lebih kompleks secara automatik. Contohnya, untuk menjawab soalan pengguna, Ejen boleh mengambil maklumat yang diperlukan daripada alat luar atau membahagikan tugas kepada beberapa langkah untuk diproses.

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Penggunaan Mudah

- Di kawasan us-east-1, buka [Akses Model Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Urus akses model` > Tandakan semua model yang anda ingin gunakan kemudian `Simpan perubahan`.

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/model_screenshot.png)

</details>

- Buka [CloudShell](https://console.aws.amazon.com/cloudshell/home) di kawasan yang anda ingin deploy
- Jalankan deployment melalui arahan berikut. Jika anda ingin menetapkan versi untuk deploy atau perlu menggunakan dasar keselamatan, sila nyatakan parameter yang sesuai daripada [Parameter Pilihan](#parameter-pilihan).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Anda akan ditanya sama ada pengguna baru atau menggunakan v3. Jika anda bukan pengguna yang berterusan dari v0, sila masukkan `y`.

### Parameter Pilihan

Anda boleh menetapkan parameter berikut semasa deployment untuk meningkatkan keselamatan dan penyesuaian:

- **--disable-self-register**: Nyahdayakan pendaftaran sendiri (lalai: didayakan). Jika flag ini ditetapkan, anda perlu membuat semua pengguna di cognito dan tidak akan membenarkan pengguna mendaftar akaun sendiri.
- **--enable-lambda-snapstart**: Dayakan [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (lalai: nyahdayakan). Jika flag ini ditetapkan, ia menambah baik masa permulaan sejuk untuk fungsi Lambda, memberikan masa tindak balas yang lebih cepat untuk pengalaman pengguna yang lebih baik.
- **--ipv4-ranges**: Senarai rentang IPv4 yang dibenarkan yang dipisahkan dengan koma. (lalai: benarkan semua alamat ipv4)
- **--ipv6-ranges**: Senarai rentang IPv6 yang dibenarkan yang dipisahkan dengan koma. (lalai: benarkan semua alamat ipv6)
- **--disable-ipv6**: Nyahdayakan sambungan melalui IPv6. (lalai: didayakan)
- **--allowed-signup-email-domains**: Senarai domain e-mel yang dibenarkan untuk pendaftaran yang dipisahkan dengan koma. (lalai: tiada sekatan domain)
- **--bedrock-region**: Tentukan kawasan di mana bedrock tersedia. (lalai: us-east-1)
- **--repo-url**: Repo Bedrock Chat yang disesuaikan untuk deploy, jika diforked atau kawalan sumber yang disesuaikan. (lalai: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Versi Bedrock Chat untuk deploy. (lalai: versi terkini dalam pembangunan)
- **--cdk-json-override**: Anda boleh mengatasi mana-mana nilai konteks CDK semasa deployment menggunakan blok JSON override. Ini membolehkan anda mengubah konfigurasi tanpa mengedit fail cdk.json secara langsung.

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
> Nilai override akan digabungkan dengan konfigurasi cdk.json yang sedia ada semasa masa deployment dalam AWS code build. Nilai yang dinyatakan dalam override akan mempunyai keutamaan berbanding nilai dalam cdk.json.

#### Contoh arahan dengan parameter:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Selepas kira-kira 35 minit, anda akan mendapatkan output berikut, yang boleh anda akses dari pelayar anda

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Skrin pendaftaran akan muncul seperti yang ditunjukkan di atas, di mana anda boleh mendaftar e-mel anda dan log masuk.

> [!Penting]
> Tanpa menetapkan parameter pilihan, kaedah deployment ini membenarkan sesiapa yang mengetahui URL untuk mendaftar. Untuk penggunaan produksi, sangat disyorkan untuk menambah sekatan alamat IP dan nyahdayakan pendaftaran sendiri untuk mengurangkan risiko keselamatan (anda boleh mentakrifkan allowed-signup-email-domains untuk menyekat pengguna supaya hanya alamat e-mel dari domain syarikat anda yang boleh mendaftar). Gunakan kedua-dua ipv4-ranges dan ipv6-ranges untuk sekatan alamat IP, dan nyahdayakan pendaftaran sendiri dengan menggunakan disable-self-register semasa melakukan ./bin.

> [!PETUA]
> Jika `Frontend URL` tidak muncul atau Bedrock Chat tidak berfungsi dengan baik, ia mungkin masalah dengan versi terkini. Dalam kes ini, sila tambah `--version "v3.0.0"` ke parameter dan cuba deployment semula.

## Senibina

Ia adalah senibina yang dibina di atas perkhidmatan AWS yang diurus, menghapuskan keperluan pengurusan infrastruktur. Dengan menggunakan Amazon Bedrock, tiada keperluan untuk berkomunikasi dengan API di luar AWS. Ini membolehkan penggunaan aplikasi yang boleh diubah skala, boleh dipercayai, dan selamat.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Pangkalan data NoSQL untuk menyimpan sejarah perbualan
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Titik akhir API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Penghantaran aplikasi frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Pembatasan alamat IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Pengesahan pengguna
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Perkhidmatan terurus untuk menggunakan model asas melalui API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Menyediakan antara muka terurus untuk Generasi Penemuan Semula ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), menawarkan perkhidmatan untuk pembenam dan penghuraian dokumen
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Menerima peristiwa dari aliran DynamoDB dan melancarkan Step Functions untuk menyematkan pengetahuan luar
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Mengatur saluran penyerapan untuk menyematkan pengetahuan luar ke dalam Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Berkhidmat sebagai pangkalan data backend untuk Bedrock Knowledge Bases, menyediakan carian teks penuh dan carian vektor, membolehkan pengambilan maklumat yang tepat
- [Amazon Athena](https://aws.amazon.com/athena/): Perkhidmatan pertanyaan untuk menganalisis baldi S3

![](./imgs/arch.png)

## Menggunakan CDK untuk Deployment

Deployment Super-mudah menggunakan [AWS CodeBuild](https://aws.amazon.com/codebuild/) untuk melakukan deployment melalui CDK secara dalaman. Bahagian ini menjelaskan prosedur untuk deployment terus dengan CDK.

- Sila pastikan mempunyai persekitaran UNIX, Docker dan runtime Node.js. Jika tidak, anda boleh menggunakan [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Penting]
> Jika ruang storan tidak mencukupi dalam persekitaran setempat semasa deployment, CDK bootstrapping mungkin menghasilkan ralat. Jika anda berjalan di Cloud9 dll., kami mengesyorkan mengembangkan saiz volum contoh sebelum deployment.

- Klon repositori ini

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Pasang pakej npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Jika perlu, edit entri berikut dalam [cdk.json](./cdk/cdk.json) jika perlu.

  - `bedrockRegion`: Wilayah di mana Bedrock tersedia. **NOTA: Bedrock TIDAK menyokong semua wilayah untuk sekarang.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Julat Alamat IP yang dibenarkan.
  - `enableLambdaSnapStart`: Secara lalai adalah true. Tetapkan ke false jika deployment ke [wilayah yang tidak menyokong Lambda SnapStart untuk fungsi Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Sebelum deployment CDK, anda perlu melakukan Bootstrap sekali untuk wilayah yang anda deployment.

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

### Menentukan Parameter

Anda boleh menentukan parameter untuk deployment anda dalam dua cara: menggunakan `cdk.json` atau menggunakan fail `parameter.ts` yang selamat dari segi jenis.

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

Untuk keselamatan jenis dan pengalaman pembangun yang lebih baik, anda boleh menggunakan fail `parameter.ts` untuk menentukan parameter anda:

```typescript
// Tentukan parameter untuk persekitaran lalai
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Tentukan parameter untuk persekitaran tambahan
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Jimat kos untuk persekitaran pembangunan
  enableBotStoreReplicas: false, // Jimat kos untuk persekitaran pembangunan
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Ketersediaan yang ditingkatkan untuk pengeluaran
  enableBotStoreReplicas: true, // Ketersediaan yang ditingkatkan untuk pengeluaran
});
```

> [!Nota]
> Pengguna sedia ada boleh terus menggunakan `cdk.json` tanpa sebarang perubahan. Pendekatan `parameter.ts` disyorkan untuk deployment baru atau apabila anda perlu mengurus berbilang persekitaran.

### Deployment Berbilang Persekitaran

Anda boleh melakukan deployment berbilang persekitaran dari satu kod sumber menggunakan fail `parameter.ts` dan pilihan `-c envName`.

#### Prasyarat

1. Tentukan persekitaran anda dalam `parameter.ts` seperti yang ditunjukkan di atas
2. Setiap persekitaran akan mempunyai set sumber daya tersendiri dengan awalan persekitaran yang spesifik

#### Perintah Deployment

Untuk deployment persekitaran tertentu:

```bash
# Deploy persekitaran pembangunan
npx cdk deploy --all -c envName=dev

# Deploy persekitaran pengeluaran
npx cdk deploy --all -c envName=prod
```

Jika tiada persekitaran yang ditentukan, persekitaran "lalai" digunakan:

```bash
# Deploy persekitaran lalai
npx cdk deploy --all
```

#### Nota Penting

1. **Penamaan Tumpukan**:

   - Tumpukan utama untuk setiap persekitaran akan mempunyai awalan nama persekitaran (contoh: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Walau bagaimanapun, tumpukan bot tersuai (`BrChatKbStack*`) dan tumpukan penerbitan API (`ApiPublishmentStack*`) tidak menerima awalan persekitaran kerana ia dibuat secara dinamik semasa runtime

2. **Penamaan Sumber Daya**:

   - Hanya beberapa sumber daya menerima awalan persekitaran dalam nama mereka (contoh: jadual `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Kebanyakan sumber daya mengekalkan nama asal mereka tetapi diasingkan dengan berada dalam tumpukan yang berbeza

3. **Pengenalan Persekitaran**:

   - Semua sumber daya ditandai dengan tag `CDKEnvironment` yang mengandungi nama persekitaran
   - Anda boleh menggunakan tag ini untuk mengenal pasti persekitaran yang sumber daya itu miliknya
   - Contoh: `CDKEnvironment: dev` atau `CDKEnvironment: prod`

4. **Ganti Persekitaran Lalai**: Jika anda mentakrifkan persekitaran "lalai" dalam `parameter.ts`, ia akan menggantikan tetapan dalam `cdk.json`. Untuk terus menggunakan `cdk.json`, jangan mentakrifkan persekitaran "lalai" dalam `parameter.ts`.

5. **Keperluan Persekitaran**: Untuk membuat persekitaran selain "lalai", anda mesti menggunakan `parameter.ts`. Pilihan `-c envName` sahaja tidak mencukupi tanpa definisi persekitaran yang sepadan.

6. **Pengasingan Sumber Daya**: Setiap persekitaran mencipta set sumber daya tersendiri, membolehkan anda mempunyai persekitaran pembangunan, pengujian, dan pengeluaran dalam akaun AWS yang sama tanpa konflik.

## Yang Lain

Anda boleh menentukan parameter untuk pengploian anda dengan dua cara: menggunakan `cdk.json` atau menggunakan fail `parameter.ts` yang mempunyai keselamatan jenis.

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

#### Menggunakan parameter.ts (Kaedah Bertipe Selamat yang Disyorkan)

Untuk keselamatan jenis dan pengalaman pembangun yang lebih baik, anda boleh menggunakan fail `parameter.ts` untuk menentukan parameter anda:

```typescript
// Tentukan parameter untuk persekitaran lalai
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Tentukan parameter untuk persekitaran tambahan
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Jimat kos untuk persekitaran pembangunan
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Ketersediaan yang dipertingkatkan untuk pengeluaran
});
```

> [!Nota]
> Pengguna sedia ada boleh terus menggunakan `cdk.json` tanpa sebarang perubahan. Pendekatan `parameter.ts` disyorkan untuk pengploian baru atau apabila anda perlu menguruskan berbilang persekitaran.

### Mengeplo Berbilang Persekitaran

Anda boleh mengeplo berbilang persekitaran daripada satu pangkalan kod menggunakan fail `parameter.ts` dan pilihan `-c envName`.

#### Prasyarat

1. Tentukan persekitaran anda dalam `parameter.ts` seperti yang ditunjukkan di atas
2. Setiap persekitaran akan mempunyai set sumbernya sendiri dengan awalan khusus persekitaran

#### Arahan Pengploian

Untuk mengeplo persekitaran tertentu:

```bash
# Eplo persekitaran pembangunan
npx cdk deploy --all -c envName=dev

# Eplo persekitaran pengeluaran
npx cdk deploy --all -c envName=prod
```

Jika tiada persekitaran ditentukan, persekitaran "lalai" digunakan:

```bash
# Eplo persekitaran lalai
npx cdk deploy --all
```

#### Nota Penting

1. **Penamaan Tindanan**:

   - Tindanan utama untuk setiap persekitaran akan mempunyai awalan nama persekitaran (contohnya, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Walau bagaimanapun, tindanan bot khusus (`BrChatKbStack*`) dan tindanan penerbitan API (`ApiPublishmentStack*`) tidak menerima awalan persekitaran kerana ia dibuat secara dinamik semasa runtime

2. **Penamaan Sumber**:

   - Hanya beberapa sumber menerima awalan persekitaran dalam nama mereka (contohnya, jadual `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Kebanyakan sumber mengekalkan nama asal mereka tetapi diasingkan dengan berada dalam tindanan yang berbeza

3. **Pengenalan Persekitaran**:

   - Semua sumber ditandai dengan tag `CDKEnvironment` yang mengandungi nama persekitaran
   - Anda boleh menggunakan tag ini untuk mengenal pasti sumber yang tergolong dalam persekitaran
   - Contoh: `CDKEnvironment: dev` atau `CDKEnvironment: prod`

4. **Ganti Persekitaran Lalai**: Jika anda mentakrifkan persekitaran "lalai" dalam `parameter.ts`, ia akan menggantikan tetapan dalam `cdk.json`. Untuk terus menggunakan `cdk.json`, jangan mentakrifkan persekitaran "lalai" dalam `parameter.ts`.

5. **Keperluan Persekitaran**: Untuk membuat persekitaran selain daripada "lalai", anda mesti menggunakan `parameter.ts`. Pilihan `-c envName` sahaja tidak mencukupi tanpa definisi persekitaran yang sepadan.

6. **Pengasingan Sumber**: Setiap persekitaran mencipta set sumbernya sendiri, membolehkan anda mempunyai persekitaran pembangunan, ujian, dan pengeluaran dalam akaun AWS yang sama tanpa konflik.

## Yang Lain

### Membuang Sumber Daya

Jika menggunakan CLI dan CDK, sila gunakan `npx cdk destroy`. Jika tidak, akses [CloudFormation](https://console.aws.amazon.com/cloudformation/home) dan kemudian hapus `BedrockChatStack` dan `FrontendWafStack` secara manual. Sila ambil perhatian bahawa `FrontendWafStack` berada di kawasan `us-east-1`.

### Tetapan Bahasa

Aset ini secara automatik mengesan bahasa menggunakan [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Anda boleh menukar bahasa dari menu aplikasi. Sebagai alternatif, anda boleh menggunakan Query String untuk menetapkan bahasa seperti yang ditunjukkan di bawah.

> `https://example.com?lng=ja`

### Nyahaktifkan Pendaftaran Sendiri

Sampel ini mempunyai pendaftaran sendiri yang diaktifkan secara lalai. Untuk menyahdayakan pendaftaran sendiri, buka [cdk.json](./cdk/cdk.json) dan tukar `selfSignUpEnabled` kepada `false`. Jika anda mengkonfigurasi [penyedia identiti luar](#external-identity-provider), nilai tersebut akan diabaikan dan secara automatik dimatikan.

### Hadkan Domain untuk Alamat E-mel Pendaftaran

Secara lalai, sampel ini tidak menghadkan domain untuk alamat e-mel pendaftaran. Untuk membenarkan pendaftaran hanya dari domain tertentu, buka `cdk.json` dan tentukan domain sebagai senarai dalam `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Penyedia Identiti Luar

Sampel ini menyokong penyedia identiti luar. Kini kami menyokong [Google](./idp/SET_UP_GOOGLE_ms-MY.md) dan [penyedia OIDC tersuai](./idp/SET_UP_CUSTOM_OIDC_ms-MY.md).

### Tambahkan pengguna baru ke kumpulan secara automatik

Sampel ini mempunyai kumpulan berikut untuk memberikan izin kepada pengguna:

- [`Admin`](./ADMINISTRATOR_ms-MY.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ms-MY.md)

Jika anda ingin pengguna yang baru dicipta secara automatik menyertai kumpulan, anda boleh menentukan mereka dalam [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Secara lalai, pengguna yang baru dicipta akan disertakan ke kumpulan `CreatingBotAllowed`.

### Konfigurasi Replika RAG

`enableRagReplicas` adalah pilihan dalam [cdk.json](./cdk/cdk.json) yang mengawal tetapan replika untuk pangkalan data RAG, khususnya Pangkalan Pengetahuan yang menggunakan Amazon OpenSearch Serverless.

- **Lalai**: true
- **true**: Meningkatkan ketersediaan dengan mengaktifkan replika tambahan, sesuai untuk persekitaran pengeluaran tetapi meningkatkan kos.
- **false**: Mengurangkan kos dengan menggunakan replika yang lebih sedikit, sesuai untuk pembangunan dan pengujian.

Ini adalah tetapan peringkat akaun/kawasan yang memberi kesan kepada keseluruhan aplikasi dan bukannya bot individu.

> [!Nota]
> Sehingga Jun 2024, Amazon OpenSearch Serverless menyokong 0.5 OCU, menurunkan kos kemasukan untuk beban kerja berskala kecil. Penerapan pengeluaran boleh bermula dengan 2 OCU, manakala beban kerja pembangunan/ujian boleh menggunakan 1 OCU. OpenSearch Serverless secara automatik menskalakan berdasarkan permintaan beban kerja. Untuk maklumat lanjut, lawati [pengumuman](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Konfigurasi Kedai Bot

Ciri kedai bot membolehkan pengguna berkongsi dan mencari bot tersuai. Anda boleh mengkonfigurasi kedai bot melalui tetapan berikut dalam [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Mengawal sama ada ciri kedai bot diaktifkan (lalai: `true`)
- **botStoreLanguage**: Menetapkan bahasa utama untuk carian dan penemuan bot (lalai: `"en"`). Ini memberi kesan kepada cara bot diindeks dan dicari dalam kedai bot, mengoptimumkan analisis teks untuk bahasa yang ditentukan.
- **enableBotStoreReplicas**: Mengawal sama ada replika siaga diaktifkan untuk koleksi OpenSearch Serverless yang digunakan oleh kedai bot (lalai: `false`). Menetapkannya kepada `true` meningkatkan ketersediaan tetapi meningkatkan kos, manakala `false` mengurangkan kos tetapi boleh memberi kesan kepada ketersediaan.
  > **Penting**: Anda tidak boleh mengemas kini sifat ini selepas koleksi sudah dibuat. Jika anda cuba mengubah sifat ini, koleksi akan terus menggunakan nilai asal.

### Inferens rentas kawasan

[Inferens rentas kawasan](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) membolehkan Amazon Bedrock menghantar dinamik permintaan inferens model merentasi pelbagai kawasan AWS, meningkatkan keluaran dan ketahanan semasa tempoh permintaan puncak. Untuk mengkonfigurasi, edit `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) meningkatkan masa permulaan sejuk untuk fungsi Lambda, memberikan masa tindak balas yang lebih cepat untuk pengalaman pengguna yang lebih baik. Sebaliknya, untuk fungsi Python, terdapat [caj bergantung kepada saiz cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) dan [tidak tersedia di beberapa kawasan](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) pada masa ini. Untuk mematikan SnapStart, edit `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Konfigurasi Domain Tersuai

Anda boleh mengkonfigurasi domain tersuai untuk agihan CloudFront dengan menetapkan parameter berikut dalam [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Nama domain tersuai untuk aplikasi chat anda (contoh: chat.example.com)
- `hostedZoneId`: ID zon yang di-host Route 53 di mana rekod DNS akan dibuat

Apabila parameter ini disediakan, penerapan akan secara automatik:

- Membuat sijil ACM dengan pengesahan DNS di kawasan us-east-1
- Membuat rekod DNS yang diperlukan dalam zon Route 53 yang di-host
- Mengkonfigurasi CloudFront untuk menggunakan domain tersuai anda

> [!Nota]
> Domain mesti diuruskan oleh Route 53 dalam akaun AWS anda. ID zon yang di-host boleh didapati dalam konsol Route 53.

### Pembangunan Tempatan

Lihat [PEMBANGUNAN TEMPATAN](./LOCAL_DEVELOPMENT_ms-MY.md).

### Sumbangan

Terima kasih kerana mempertimbangkan untuk menyumbang ke repositori ini! Kami mengalu-alukan pembaikan pepijat, terjemahan bahasa (i18n), penambahbaikan ciri, [alat ejen](./docs/AGENT.md#how-to-develop-your-own-tools), dan penambahbaikan lain.

Untuk penambahbaikan ciri dan penambahbaikan lain, **sebelum membuat Permintaan Tarik, kami sangat menghargai jika anda boleh membuat Isu Permintaan Ciri untuk membincangkan pendekatan pelaksanaan dan butiran. Untuk pembaikan pepijat dan terjemahan bahasa (i18n), teruskan dengan membuat Permintaan Tarik secara langsung.**

Sila juga lihat garis panduan berikut sebelum menyumbang:

- [Pembangunan Tempatan](./LOCAL_DEVELOPMENT_ms-MY.md)
- [MENYUMBANG](./CONTRIBUTING_ms-MY.md)

## Kenalan

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Penyumbang Utama

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Penyumbang

[![penyumbang bedrock chat](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Lesen

Pustaka ini dibenarkan di bawah Lesen MIT-0. Lihat [fail LESEN](./LICENSE).