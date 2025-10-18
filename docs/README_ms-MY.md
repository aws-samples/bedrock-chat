<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Platform AI generatif pelbagai bahasa yang dikuasakan oleh [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Menyokong perbualan, bot tersuai dengan pengetahuan (RAG), perkongsian bot melalui kedai bot, dan automasi tugas menggunakan ejen.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 telah dikeluarkan. Untuk mengemaskini, sila semak dengan teliti [panduan penghijrahan](./migration/V2_TO_V3_ms-MY.md).** Tanpa sebarang perhatian, **BOT DARI V2 AKAN MENJADI TIDAK BOLEH DIGUNAKAN.**

### Personalisasi Bot / Kedai Bot

Tambah arahan dan pengetahuan anda sendiri (juga dikenali sebagai [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/). Bot boleh dikongsi antara pengguna aplikasi melalui pasaran kedai bot. Bot yang disesuaikan juga boleh diterbitkan sebagai API kendiri (Lihat [butiran](./PUBLISH_API_ms-MY.md)).

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
> Atas sebab tadbir urus, hanya pengguna yang dibenarkan sahaja boleh mencipta bot tersuai. Untuk membenarkan penciptaan bot tersuai, pengguna mesti menjadi ahli kumpulan yang dipanggil `CreatingBotAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Perhatikan bahawa id kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Ciri-ciri pentadbiran

Pengurusan API, Tandakan bot sebagai penting, Analisis penggunaan untuk bot. [butiran](./ADMINISTRATOR_ms-MY.md)

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Ejen

Dengan menggunakan [fungsi Ejen](./AGENT_ms-MY.md), bot perbualan anda boleh mengendalikan tugas yang lebih kompleks secara automatik. Sebagai contoh, untuk menjawab soalan pengguna, Ejen boleh mendapatkan maklumat yang diperlukan daripada alat luaran atau memecahkan tugas kepada beberapa langkah untuk diproses.

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Penempatan Super Mudah

- Di rantau us-east-1, buka [Akses Model Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Urus akses model` > Tandakan semua model yang anda ingin gunakan dan kemudian `Simpan perubahan`.

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/model_screenshot.png)

</details>

### Rantau yang Disokong

Sila pastikan anda menempatkan Bedrock Chat di rantau [di mana OpenSearch Serverless dan API Ingestion tersedia](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), jika anda ingin menggunakan bot dan mencipta pangkalan pengetahuan (OpenSearch Serverless adalah pilihan lalai). Sehingga Ogos 2025, rantau berikut disokong: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Untuk parameter **bedrock-region** anda perlu memilih rantau [di mana Bedrock tersedia](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Buka [CloudShell](https://console.aws.amazon.com/cloudshell/home) di rantau di mana anda ingin menempatkan
- Jalankan penempatan melalui arahan berikut. Jika anda ingin menentukan versi untuk ditempatkan atau perlu menggunakan dasar keselamatan, sila tentukan parameter yang sesuai dari [Parameter Pilihan](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Anda akan ditanya sama ada pengguna baru atau menggunakan v3. Jika anda bukan pengguna berterusan dari v0, sila masukkan `y`.

### Parameter Pilihan

Anda boleh menentukan parameter berikut semasa penempatan untuk meningkatkan keselamatan dan penyesuaian:

- **--disable-self-register**: Nyahaktifkan pendaftaran sendiri (lalai: diaktifkan). Jika bendera ini ditetapkan, anda perlu mencipta semua pengguna di cognito dan ia tidak akan membenarkan pengguna mendaftar akaun mereka sendiri.
- **--enable-lambda-snapstart**: Aktifkan [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (lalai: dinyahaktifkan). Jika bendera ini ditetapkan, ia meningkatkan masa permulaan sejuk untuk fungsi Lambda, memberikan masa tindak balas yang lebih pantas untuk pengalaman pengguna yang lebih baik.
- **--ipv4-ranges**: Senarai julat IPv4 yang dibenarkan dipisahkan dengan koma. (lalai: benarkan semua alamat ipv4)
- **--ipv6-ranges**: Senarai julat IPv6 yang dibenarkan dipisahkan dengan koma. (lalai: benarkan semua alamat ipv6)
- **--disable-ipv6**: Nyahaktifkan sambungan melalui IPv6. (lalai: diaktifkan)
- **--allowed-signup-email-domains**: Senarai domain e-mel yang dibenarkan untuk pendaftaran dipisahkan dengan koma. (lalai: tiada sekatan domain)
- **--bedrock-region**: Tentukan rantau di mana bedrock tersedia. (lalai: us-east-1)
- **--repo-url**: Repo tersuai Bedrock Chat untuk ditempatkan, jika difork atau kawalan sumber tersuai. (lalai: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: Versi Bedrock Chat untuk ditempatkan. (lalai: versi terkini dalam pembangunan)
- **--cdk-json-override**: Anda boleh mengatasi mana-mana nilai konteks CDK semasa penempatan menggunakan blok JSON override. Ini membolehkan anda mengubah suai konfigurasi tanpa mengedit fail cdk.json secara langsung.

Contoh penggunaan:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

JSON override mesti mengikuti struktur yang sama seperti cdk.json. Anda boleh mengatasi mana-mana nilai konteks termasuk:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: menerima senarai ID model untuk diaktifkan. Nilai lalai adalah senarai kosong, yang mengaktifkan semua model.
- `logoPath`: laluan relatif ke aset logo dalam direktori `public/` frontend yang muncul di bahagian atas laci navigasi.
- Dan nilai konteks lain yang ditentukan dalam cdk.json

> [!Note]
> Nilai override akan digabungkan dengan konfigurasi cdk.json sedia ada semasa masa penempatan dalam AWS code build. Nilai yang ditentukan dalam override akan mengambil keutamaan berbanding nilai dalam cdk.json.

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

> [!Important]
> Tanpa menetapkan parameter pilihan, kaedah penempatan ini membenarkan sesiapa sahaja yang mengetahui URL untuk mendaftar. Untuk penggunaan produksi, adalah sangat disyorkan untuk menambah sekatan alamat IP dan menyahaktifkan pendaftaran sendiri untuk mengurangkan risiko keselamatan (anda boleh menentukan allowed-signup-email-domains untuk menyekat pengguna supaya hanya alamat e-mel dari domain syarikat anda boleh mendaftar). Gunakan kedua-dua ipv4-ranges dan ipv6-ranges untuk sekatan alamat IP, dan nyahaktifkan pendaftaran sendiri dengan menggunakan disable-self-register semasa melaksanakan ./bin.

> [!TIP]
> Jika `Frontend URL` tidak muncul atau Bedrock Chat tidak berfungsi dengan betul, ia mungkin masalah dengan versi terkini. Dalam kes ini, sila tambah `--version "v3.0.0"` kepada parameter dan cuba penempatan sekali lagi.

## Seni Bina

Ia adalah seni bina yang dibina pada perkhidmatan terurus AWS, menghapuskan keperluan untuk pengurusan infrastruktur. Dengan menggunakan Amazon Bedrock, tiada keperluan untuk berkomunikasi dengan API di luar AWS. Ini membolehkan penerapan aplikasi yang berskala, boleh dipercayai, dan selamat.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Pangkalan data NoSQL untuk penyimpanan sejarah perbualan
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Titik akhir API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Penghantaran aplikasi frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Sekatan alamat IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Pengesahan pengguna
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Perkhidmatan terurus untuk menggunakan model asas melalui API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Menyediakan antara muka terurus untuk Penjanaan Dipertingkat Pengambilan Semula ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), menawarkan perkhidmatan untuk pembenaman dan penghuraian dokumen
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Menerima acara dari aliran DynamoDB dan melancarkan Step Functions untuk membenamkan pengetahuan luaran
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Mengorkestrasi saluran pengambilan untuk membenamkan pengetahuan luaran ke dalam Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Berfungsi sebagai pangkalan data backend untuk Bedrock Knowledge Bases, menyediakan carian teks penuh dan carian vektor, membolehkan pengambilan semula maklumat yang tepat
- [Amazon Athena](https://aws.amazon.com/athena/): Perkhidmatan pertanyaan untuk menganalisis baldi S3

![](./imgs/arch.png)

## Penempatan menggunakan CDK

Penempatan Super-mudah menggunakan [AWS CodeBuild](https://aws.amazon.com/codebuild/) untuk melakukan penempatan dengan CDK secara dalaman. Bahagian ini menerangkan prosedur untuk penempatan secara langsung dengan CDK.

- Sila pastikan anda mempunyai persekitaran UNIX, Docker dan Node.js.

> [!Important]
> Jika ruang storan tidak mencukupi dalam persekitaran tempatan semasa penempatan, bootstrap CDK mungkin mengakibatkan ralat. Kami mengesyorkan untuk menambah saiz volum instans sebelum penempatan.

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

- Jika perlu, edit entri berikut dalam [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Rantau di mana Bedrock tersedia. **NOTA: Bedrock TIDAK menyokong semua rantau buat masa ini.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Julat alamat IP yang dibenarkan.
  - `enableLambdaSnapStart`: Lalai kepada true. Tetapkan kepada false jika menempatkan ke [rantau yang tidak menyokong Lambda SnapStart untuk fungsi Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Lalai kepada semua. Jika ditetapkan (senarai ID model), membolehkan kawalan global model yang muncul dalam menu dropdown merentas perbualan untuk semua pengguna dan semasa penciptaan bot dalam aplikasi Bedrock Chat.
  - `logoPath`: Laluan relatif di bawah `frontend/public` yang menunjuk kepada imej yang dipaparkan di bahagian atas laci aplikasi.
ID model berikut disokong (sila pastikan ia juga diaktifkan dalam konsol Bedrock di bawah Model access di rantau penempatan anda):
- **Model Claude:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Model Amazon Nova:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Model Mistral:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **Model DeepSeek:** `deepseek-r1`
- **Model Meta Llama:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

Senarai penuh boleh didapati dalam [index.ts](./frontend/src/constants/index.ts).

- Sebelum menempatkan CDK, anda perlu melakukan Bootstrap sekali untuk rantau yang anda akan tempatkan.

```
npx cdk bootstrap
```

- Tempatkan projek sampel ini

```
npx cdk deploy --require-approval never --all
```

- Anda akan mendapat output seperti berikut. URL aplikasi web akan dikeluarkan dalam `BedrockChatStack.FrontendURL`, sila akses melalui pelayar web anda.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Menentukan Parameter

Anda boleh menentukan parameter untuk penempatan anda dalam dua cara: menggunakan `cdk.json` atau menggunakan fail `parameter.ts` yang selamat jenis.

#### Menggunakan cdk.json (Kaedah Tradisional)

Cara tradisional untuk mengkonfigurasi parameter adalah dengan mengedit fail `cdk.json`. Pendekatan ini mudah tetapi tidak mempunyai pemeriksaan jenis:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Menggunakan parameter.ts (Kaedah Selamat Jenis yang Disyorkan)

Untuk keselamatan jenis dan pengalaman pembangun yang lebih baik, anda boleh menggunakan fail `parameter.ts` untuk menentukan parameter anda:

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
  enableBotStoreReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
  enableBotStoreReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Pengguna sedia ada boleh terus menggunakan `cdk.json` tanpa sebarang perubahan. Pendekatan `parameter.ts` disyorkan untuk penempatan baharu atau apabila anda perlu menguruskan pelbagai persekitaran.

### Menempatkan Pelbagai Persekitaran

Anda boleh menempatkan pelbagai persekitaran dari kod asas yang sama menggunakan fail `parameter.ts` dan pilihan `-c envName`.

#### Prasyarat

1. Tentukan persekitaran anda dalam `parameter.ts` seperti yang ditunjukkan di atas
2. Setiap persekitaran akan mempunyai set sumber sendiri dengan awalan khusus persekitaran

#### Arahan Penempatan

Untuk menempatkan persekitaran tertentu:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Jika tiada persekitaran yang ditetapkan, persekitaran "default" digunakan:

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Nota Penting

1. **Penamaan Stack**:

   - Stack utama untuk setiap persekitaran akan diawali dengan nama persekitaran (cth., `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Walau bagaimanapun, stack bot tersuai (`BrChatKbStack*`) dan stack penerbitan API (`ApiPublishmentStack*`) tidak menerima awalan persekitaran kerana ia dicipta secara dinamik semasa runtime

2. **Penamaan Sumber**:

   - Hanya beberapa sumber menerima awalan persekitaran dalam nama mereka (cth., jadual `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Kebanyakan sumber mengekalkan nama asal mereka tetapi diasingkan dengan berada dalam stack yang berbeza

3. **Pengenalan Persekitaran**:

   - Semua sumber ditag dengan tag `CDKEnvironment` yang mengandungi nama persekitaran
   - Anda boleh menggunakan tag ini untuk mengenal pasti persekitaran mana sumber tersebut
   - Contoh: `CDKEnvironment: dev` atau `CDKEnvironment: prod`

4. **Penggantian Persekitaran Lalai**: Jika anda menentukan persekitaran "default" dalam `parameter.ts`, ia akan menggantikan tetapan dalam `cdk.json`. Untuk terus menggunakan `cdk.json`, jangan tentukan persekitaran "default" dalam `parameter.ts`.

5. **Keperluan Persekitaran**: Untuk mencipta persekitaran selain daripada "default", anda mesti menggunakan `parameter.ts`. Pilihan `-c envName` sahaja tidak mencukupi tanpa definisi persekitaran yang sepadan.

6. **Pengasingan Sumber**: Setiap persekitaran mencipta set sumber sendiri, membolehkan anda mempunyai persekitaran pembangunan, pengujian, dan pengeluaran dalam akaun AWS yang sama tanpa konflik.

## Lain-lain

Anda boleh menentukan parameter untuk penempatan anda dalam dua cara: menggunakan `cdk.json` atau menggunakan fail `parameter.ts` yang selamat jenis.

#### Menggunakan cdk.json (Kaedah Tradisional)

Cara tradisional untuk mengkonfigurasi parameter adalah dengan mengedit fail `cdk.json`. Pendekatan ini mudah tetapi tidak mempunyai pemeriksaan jenis:

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
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Pengguna sedia ada boleh terus menggunakan `cdk.json` tanpa sebarang perubahan. Pendekatan `parameter.ts` disyorkan untuk penempatan baharu atau apabila anda perlu menguruskan pelbagai persekitaran.

### Menempatkan Pelbagai Persekitaran

Anda boleh menempatkan pelbagai persekitaran dari kod asas yang sama menggunakan fail `parameter.ts` dan pilihan `-c envName`.

#### Prasyarat

1. Tentukan persekitaran anda dalam `parameter.ts` seperti yang ditunjukkan di atas
2. Setiap persekitaran akan mempunyai set sumber sendiri dengan awalan khusus persekitaran

#### Arahan Penempatan

Untuk menempatkan persekitaran tertentu:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Jika tiada persekitaran dinyatakan, persekitaran "default" digunakan:

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Nota Penting

1. **Penamaan Tindanan**:

   - Tindanan utama untuk setiap persekitaran akan diawali dengan nama persekitaran (contoh: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Walau bagaimanapun, tindanan bot tersuai (`BrChatKbStack*`) dan tindanan penerbitan API (`ApiPublishmentStack*`) tidak menerima awalan persekitaran kerana ia dicipta secara dinamik semasa masa jalan

2. **Penamaan Sumber**:

   - Hanya beberapa sumber menerima awalan persekitaran dalam nama mereka (contoh: jadual `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Kebanyakan sumber mengekalkan nama asal mereka tetapi diasingkan dengan berada dalam tindanan yang berbeza

3. **Pengenalpastian Persekitaran**:

   - Semua sumber ditag dengan tag `CDKEnvironment` yang mengandungi nama persekitaran
   - Anda boleh menggunakan tag ini untuk mengenal pasti persekitaran mana sumber tersebut
   - Contoh: `CDKEnvironment: dev` atau `CDKEnvironment: prod`

4. **Penggantian Persekitaran Default**: Jika anda menentukan persekitaran "default" dalam `parameter.ts`, ia akan menggantikan tetapan dalam `cdk.json`. Untuk terus menggunakan `cdk.json`, jangan tentukan persekitaran "default" dalam `parameter.ts`.

5. **Keperluan Persekitaran**: Untuk mencipta persekitaran selain daripada "default", anda mesti menggunakan `parameter.ts`. Pilihan `-c envName` sahaja tidak mencukupi tanpa definisi persekitaran yang sepadan.

6. **Pengasingan Sumber**: Setiap persekitaran mencipta set sumber sendiri, membolehkan anda mempunyai persekitaran pembangunan, pengujian, dan pengeluaran dalam akaun AWS yang sama tanpa konflik.

## Lain-lain

### Membuang sumber

Jika menggunakan cli dan CDK, sila gunakan `npx cdk destroy`. Jika tidak, akses [CloudFormation](https://console.aws.amazon.com/cloudformation/home) dan kemudian padam `BedrockChatStack` dan `FrontendWafStack` secara manual. Sila ambil perhatian bahawa `FrontendWafStack` berada di rantau `us-east-1`.

### Tetapan Bahasa

Aset ini mengesan bahasa secara automatik menggunakan [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Anda boleh menukar bahasa dari menu aplikasi. Sebagai alternatif, anda boleh menggunakan Query String untuk menetapkan bahasa seperti yang ditunjukkan di bawah.

> `https://example.com?lng=ja`

### Menyahaktifkan pendaftaran sendiri

Sampel ini mempunyai pendaftaran sendiri diaktifkan secara lalai. Untuk menyahaktifkan pendaftaran sendiri, buka [cdk.json](./cdk/cdk.json) dan tukar `selfSignUpEnabled` kepada `false`. Jika anda mengkonfigurasi [pembekal identiti luaran](#external-identity-provider), nilai ini akan diabaikan dan dinyahaktifkan secara automatik.

### Menyekat Domain untuk Alamat E-mel Pendaftaran

Secara lalai, sampel ini tidak menyekat domain untuk alamat e-mel pendaftaran. Untuk membenarkan pendaftaran hanya dari domain tertentu, buka `cdk.json` dan tentukan domain sebagai senarai dalam `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Pembekal Identiti Luaran

Sampel ini menyokong pembekal identiti luaran. Buat masa ini kami menyokong [Google](./idp/SET_UP_GOOGLE_ms-MY.md) dan [pembekal OIDC tersuai](./idp/SET_UP_CUSTOM_OIDC_ms-MY.md).

### WAF Frontend Pilihan

Untuk pengedaran CloudFront, WebACL AWS WAF mesti dibuat di rantau us-east-1. Di sesetengah organisasi, penciptaan sumber di luar rantau utama dihadkan oleh dasar. Dalam persekitaran sedemikian, penggunaan CDK boleh gagal apabila cuba menyediakan Frontend WAF di us-east-1.

Untuk menampung sekatan ini, tindanan Frontend WAF adalah pilihan. Apabila dinyahaktifkan, pengedaran CloudFront digunakan tanpa WebACL. Ini bermakna anda tidak akan mempunyai kawalan membenarkan/menafikan IP di bahagian hadapan. Pengesahan dan semua kawalan aplikasi lain terus berfungsi seperti biasa. Perhatikan bahawa tetapan ini hanya mempengaruhi Frontend WAF (skop CloudFront); WAF API yang Diterbitkan (serantau) kekal tidak terjejas.

Untuk menyahaktifkan Frontend WAF tetapkan yang berikut dalam `parameter.ts` (Kaedah Selamat Jenis yang Disyorkan):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Atau jika menggunakan `cdk/cdk.json` legasi tetapkan yang berikut:

```json
"enableFrontendWaf": false
``` 

### Tambah pengguna baharu ke kumpulan secara automatik

Sampel ini mempunyai kumpulan berikut untuk memberikan kebenaran kepada pengguna:

- [`Admin`](./ADMINISTRATOR_ms-MY.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ms-MY.md)

Jika anda mahu pengguna yang baru dibuat secara automatik menyertai kumpulan, anda boleh menentukannya dalam [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Secara lalai, pengguna yang baru dibuat akan disertakan ke dalam kumpulan `CreatingBotAllowed`.

### Mengkonfigurasi Replika RAG

`enableRagReplicas` adalah pilihan dalam [cdk.json](./cdk/cdk.json) yang mengawal tetapan replika untuk pangkalan data RAG, khususnya Pangkalan Pengetahuan menggunakan Amazon OpenSearch Serverless.

- **Lalai**: true
- **true**: Meningkatkan ketersediaan dengan mengaktifkan replika tambahan, menjadikannya sesuai untuk persekitaran pengeluaran tetapi meningkatkan kos.
- **false**: Mengurangkan kos dengan menggunakan replika yang lebih sedikit, menjadikannya sesuai untuk pembangunan dan pengujian.

Ini adalah tetapan peringkat akaun/rantau, yang mempengaruhi keseluruhan aplikasi dan bukannya bot individu.

> [!Note]
> Mulai Jun 2024, Amazon OpenSearch Serverless menyokong 0.5 OCU, mengurangkan kos permulaan untuk beban kerja skala kecil. Penempatan pengeluaran boleh bermula dengan 2 OCU, manakala beban kerja dev/ujian boleh menggunakan 1 OCU. OpenSearch Serverless secara automatik mengskala berdasarkan permintaan beban kerja. Untuk maklumat lanjut, lawati [pengumuman](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Mengkonfigurasi Kedai Bot

Ciri kedai bot membolehkan pengguna berkongsi dan menemui bot tersuai. Anda boleh mengkonfigurasi kedai bot melalui tetapan berikut dalam [cdk.json](./cdk/cdk.json):

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
- **botStoreLanguage**: Menetapkan bahasa utama untuk carian dan penemuan bot (lalai: `"en"`). Ini mempengaruhi bagaimana bot diindeks dan dicari dalam kedai bot, mengoptimumkan analisis teks untuk bahasa yang ditentukan.
- **enableBotStoreReplicas**: Mengawal sama ada replika siap sedia diaktifkan untuk koleksi OpenSearch Serverless yang digunakan oleh kedai bot (lalai: `false`). Menetapkannya kepada `true` meningkatkan ketersediaan tetapi meningkatkan kos, manakala `false` mengurangkan kos tetapi mungkin mempengaruhi ketersediaan.
  > **Penting**: Anda tidak boleh mengemaskini sifat ini selepas koleksi sudah dibuat. Jika anda cuba mengubah sifat ini, koleksi akan terus menggunakan nilai asal.

### Inferens Rentas Rantau dan Global

[Inferens Rentas Rantau dan Global](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
membolehkan Amazon Bedrock mengarahkan permintaan inferens model secara dinamik merentasi
pelbagai rantau AWS, meningkatkan daya pemprosesan dan ketahanan semasa tempoh
permintaan tinggi. Inferens global mengarahkan permintaan ke rantau optimum berdasarkan
kependaman dan ketersediaan di mana-mana di dunia, manakala inferens rentas rantau mengarahkan
permintaan dalam rantau AWS yang sama, contohnya, dalam US. Sesetengah
SCP mungkin menyekat satu atau yang lain atau kedua-duanya dan oleh itu anda boleh mengkonfigurasinya
secara berasingan. Secara lalai kedua-duanya diaktifkan.

Untuk mengkonfigurasi ubah tetapan berikut dalam `cdk.json` atau `parameters.ts`:

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) meningkatkan masa mula sejuk untuk fungsi Lambda, memberikan masa tindak balas yang lebih pantas untuk pengalaman pengguna yang lebih baik. Sebaliknya, untuk fungsi Python, terdapat [caj bergantung kepada saiz cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) dan [tidak tersedia di sesetengah rantau](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) buat masa ini. Untuk menyahaktifkan SnapStart, edit `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Mengkonfigurasi Domain Tersuai

Anda boleh mengkonfigurasi domain tersuai untuk pengedaran CloudFront dengan menetapkan parameter berikut dalam [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Nama domain tersuai untuk aplikasi sembang anda (cth., chat.example.com)
- `hostedZoneId`: ID zon hos Route 53 anda di mana rekod domain akan dibuat

Apabila parameter ini disediakan, penempatan akan secara automatik:

- Membuat sijil ACM dengan pengesahan DNS di rantau us-east-1
- Membuat rekod DNS yang diperlukan dalam zon hos Route 53 anda
- Mengkonfigurasi CloudFront untuk menggunakan domain tersuai anda

> [!Note]
> Domain mesti diuruskan oleh Route 53 dalam akaun AWS anda. ID zon hos boleh didapati dalam konsol Route 53.

### Mengkonfigurasi negara yang dibenarkan (sekatan geo)

Anda boleh menyekat akses kepada Bedrock-Chat berdasarkan negara dari mana pelanggan mengaksesnya.
Gunakan parameter `allowedCountries` dalam [cdk.json](./cdk/cdk.json) yang mengambil senarai [Kod Negara ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Sebagai contoh, perniagaan yang berpangkalan di New Zealand mungkin memutuskan bahawa hanya alamat IP dari New Zealand (NZ) dan Australia (AU) boleh mengakses portal dan semua yang lain harus dinafikan akses.
Untuk mengkonfigurasi tingkah laku ini gunakan tetapan berikut dalam [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Atau, menggunakan `parameter.ts` (Kaedah Selamat Jenis yang Disyorkan):

```ts
// Define parameters for the default environment
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Menyahaktifkan sokongan IPv6

Frontend mendapat kedua-dua alamat IP dan IPv6 secara lalai. Dalam beberapa keadaan
yang jarang berlaku, anda mungkin perlu menyahaktifkan sokongan IPv6 secara eksplisit. Untuk melakukan ini, tetapkan
parameter berikut dalam [parameter.ts](./cdk/parameter.ts) atau serupa dalam [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Jika tidak ditetapkan, sokongan IPv6 akan diaktifkan secara lalai.

### Pembangunan Tempatan

Lihat [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_ms-MY.md).

### Sumbangan

Terima kasih kerana mempertimbangkan untuk menyumbang kepada repositori ini! Kami mengalu-alukan pembetulan pepijat, terjemahan bahasa (i18n), peningkatan ciri, [alat ejen](./docs/AGENT.md#how-to-develop-your-own-tools), dan penambahbaikan lain.

Untuk peningkatan ciri dan penambahbaikan lain, **sebelum membuat Permintaan Tarik, kami sangat menghargai jika anda boleh membuat Isu Permintaan Ciri untuk membincangkan pendekatan pelaksanaan dan butiran. Untuk pembetulan pepijat dan terjemahan bahasa (i18n), teruskan dengan membuat Permintaan Tarik secara langsung.**

Sila juga lihat garis panduan berikut sebelum menyumbang:

- [Local Development](./LOCAL_DEVELOPMENT_ms-MY.md)
- [CONTRIBUTING](./CONTRIBUTING_ms-MY.md)

## Kenalan

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Penyumbang Penting

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Penyumbang

[![penyumbang bedrock chat](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Lesen

Perpustakaan ini dilesenkan di bawah Lesen MIT-0. Sila rujuk [fail LESEN](./LICENSE).