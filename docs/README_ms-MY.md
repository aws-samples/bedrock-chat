# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_no.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi.md)

> [!Warning]  
> **V2 telah dikeluarkan. Untuk mengemas kini, sila semak semula panduan migrasi [migration guide](./migration/V1_TO_V2_ms-MY.md) dengan teliti.** Tanpa kehati-hatian, **BOT DARI V1 AKAN MENJADI TIDAK BOLEH DIGUNAKAN.**

Chatbot pelbagai bahasa yang menggunakan model LLM yang disediakan oleh [Amazon Bedrock](https://aws.amazon.com/bedrock/) untuk generatif AI.

### Tonton Gambaran Keseluruhan dan Pemasangan di YouTube

[![Overview](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Perbualan Asas

![](./imgs/demo.gif)

### Personalisasi Bot

Tambahkan arahan anda sendiri dan berikan pengetahuan luar seperti URL atau fail (yang dikenali sebagai [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/). Bot boleh dikongsi antara pengguna aplikasi. Bot yang disesuaikan juga boleh diterbitkan sebagai API berasingan (Lihat [butiran](./PUBLISH_API_ms-MY.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Atas sebab tadbir urus, hanya pengguna yang dibenarkan sahaja yang boleh membuat bot yang disesuaikan. Untuk membenarkan penciptaan bot yang disesuaikan, pengguna mesti menjadi ahli kumpulan yang dipanggil `CreatingBotAllowed`, yang boleh disediakan melalui konsol pengurusan > Amazon Cognito User pools atau aws cli. Ambil perhatian bahawa ID kumpulan pengguna boleh dirujuk dengan mengakses CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Papan pemuka pentadbir

<details>
<summary>Papan pemuka pentadbir</summary>

Analisis penggunaan untuk setiap pengguna / bot pada papan pemuka pentadbir. [butiran](./ADMINISTRATOR_ms-MY.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Ejen Berkuasa LLM

<details>
<summary>Ejen Berkuasa LLM</summary>

Dengan menggunakan [fungsi Ejen](./AGENT_ms-MY.md), chatbot anda boleh mengendalikan tugas yang lebih kompleks secara automatik. Contohnya, untuk menjawab soalan pengguna, Ejen boleh mengambil maklumat yang diperlukan daripada alat luar atau membahagikan tugas kepada beberapa langkah untuk diproses.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Pengploian Super-Mudah

- Di kawasan us-east-1, buka [Akses Model Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Urus akses model` > Tandakan semua `Anthropic / Claude 3`, semua `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` dan `Cohere / Embed Multilingual` kemudian `Simpan perubahan`.

<details>
<summary>Tangkapan Skrin</summary>

![](./imgs/model_screenshot.png)

</details>

- Buka [CloudShell](https://console.aws.amazon.com/cloudshell/home) di kawasan yang anda ingin deploikan
- Jalankan pengploian melalui arahan berikut. Jika anda ingin menetapkan versi untuk diploikan atau perlu menggunakan polisi keselamatan, sila tentukan parameter yang sesuai dari [Parameter Pilihan](#parameter-pilihan).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Anda akan ditanya sama ada pengguna baru atau menggunakan v2. Jika anda bukan pengguna berterusan dari v0, sila masukkan `y`.

### Parameter Pilihan

Anda boleh menetapkan parameter berikut semasa pengploian untuk meningkatkan keselamatan dan pengubahsuaian:

- **--disable-self-register**: Matikan pendaftaran sendiri (lalai: didayakan). Jika flag ini ditetapkan, anda perlu membuat semua pengguna di cognito dan tidak akan membenarkan pengguna mendaftar akaun mereka sendiri.
- **--enable-lambda-snapstart**: Dayakan [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (lalai: dilumpuhkan). Jika flag ini ditetapkan, ia meningkatkan masa permulaan sejuk untuk fungsi Lambda, memberikan masa respons yang lebih cepat untuk pengalaman pengguna yang lebih baik.
- **--ipv4-ranges**: Senarai yang dipisahkan koma bagi julat IPv4 yang dibenarkan. (lalai: benarkan semua alamat ipv4)
- **--ipv6-ranges**: Senarai yang dipisahkan koma bagi julat IPv6 yang dibenarkan. (lalai: benarkan semua alamat ipv6)
- **--disable-ipv6**: Matikan sambungan melalui IPv6. (lalai: didayakan)
- **--allowed-signup-email-domains**: Senarai yang dipisahkan koma bagi domain e-mel yang dibenarkan untuk pendaftaran. (lalai: tiada sekatan domain)
- **--bedrock-region**: Tentukan kawasan di mana bedrock tersedia. (lalai: us-east-1)
- **--repo-url**: Repo Bedrock Claude Chat yang disesuaikan untuk diploikan, jika fork atau kawalan sumber yang disesuaikan. (lalai: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Versi Bedrock Claude Chat untuk diploikan. (lalai: versi terkini dalam pembangunan)
- **--cdk-json-override**: Anda boleh mengatasi mana-mana nilai konteks CDK semasa pengploian menggunakan blok JSON override. Ini membolehkan anda mengubah konfigurasi tanpa mengedit fail cdk.json secara langsung.

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
> Nilai override akan digabungkan dengan konfigurasi cdk.json sedia ada semasa masa pengploian dalam AWS code build. Nilai yang ditentukan dalam override akan mengambil keutamaan berbanding nilai dalam cdk.json.

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
> Tanpa menetapkan parameter pilihan, kaedah pengploian ini membenarkan sesiapa yang mengetahui URL untuk mendaftar. Untuk kegunaan pengeluaran, sangat disyorkan untuk menambah sekatan alamat IP dan melumpuhkan pendaftaran sendiri untuk mengurangkan risiko keselamatan (anda boleh mentakrifkan allowed-signup-email-domains untuk menyekat pengguna supaya hanya alamat e-mel dari domain syarikat anda yang boleh mendaftar). Gunakan kedua-dua ipv4-ranges dan ipv6-ranges untuk sekatan alamat IP, dan lumpuhkan pendaftaran sendiri dengan menggunakan disable-self-register semasa melaksanakan ./bin.

> [!PETUA]
> Jika `Frontend URL` tidak muncul atau Bedrock Claude Chat tidak berfungsi dengan baik, ia mungkin masalah dengan versi terkini. Dalam kes ini, sila tambah `--version "v1.2.6"` ke parameter dan cuba pengploian semula.

## Senibina

Ia adalah senibina yang dibina di atas perkhidmatan yang diuruskan AWS, menghapuskan keperluan pengurusan infrastruktur. Dengan menggunakan Amazon Bedrock, tiada keperluan untuk berkomunikasi dengan API di luar AWS. Ini membolehkan penggunaan aplikasi yang boleh diukur, boleh dipercayai, dan selamat.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Pangkalan data NoSQL untuk menyimpan sejarah perbualan
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Titik akhir API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Penghantaran aplikasi frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Pembatasan alamat IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Pengesahan pengguna
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Perkhidmatan yang diuruskan untuk menggunakan model asas melalui API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Menyediakan antara muka yang diuruskan untuk Generasi Perolehan Semula Tambahan ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), menawarkan perkhidmatan untuk menyematkan dan mengurai dokumen
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Menerima acara dari aliran DynamoDB dan melancarkan Step Functions untuk menyematkan pengetahuan luar
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Mengatur saluran penyerapan untuk menyematkan pengetahuan luar ke dalam Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Berkhidmat sebagai pangkalan data backend untuk Bedrock Knowledge Bases, menyediakan ciri-ciri carian teks penuh dan carian vektor, membolehkan perolehan maklumat yang berkaitan dengan tepat
- [Amazon Athena](https://aws.amazon.com/athena/): Perkhidmatan pertanyaan untuk menganalisis baldi S3

![](./imgs/arch.png)

## Deploy menggunakan CDK

Deployment Super-mudah menggunakan [AWS CodeBuild](https://aws.amazon.com/codebuild/) untuk melakukan deployment melalui CDK secara dalaman. Bahagian ini menjelaskan prosedur untuk melakukan deployment terus dengan CDK.

- Sila pastikan mempunyai persekitaran UNIX, Docker dan runtime Node.js. Jika tidak, anda boleh menggunakan [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Penting]
> Jika ruang storan tidak mencukupi dalam persekitaran tempatan semasa deployment, CDK bootstrapping mungkin menghasilkan ralat. Jika anda sedang menjalankan di Cloud9 dll., kami mengesyorkan mengembangkan saiz volum contoh sebelum deployment.

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

  - `bedrockRegion`: Wilayah di mana Bedrock tersedia. **NOTA: Bedrock TIDAK menyokong semua wilayah buat masa ini.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Julat Alamat IP yang dibenarkan.
  - `enableLambdaSnapStart`: Secara lalai adalah true. Tetapkan ke false jika melakukan deployment ke [wilayah yang tidak menyokong Lambda SnapStart untuk fungsi Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Sebelum melakukan deployment CDK, anda perlu bekerja dengan Bootstrap sekali untuk wilayah yang anda sedang deploy.

```
npx cdk bootstrap
```

- Deploy projek sampel ini

```
npx cdk deploy --require-approval never --all
```

- Anda akan mendapatkan output yang serupa dengan berikut. URL aplikasi web akan dikeluarkan dalam `BedrockChatStack.FrontendURL`, sila akses dari pelayar anda.

```sh
 ✅  BedrockChatStack

✨  Masa Deployment: 78.57s

Output:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Lain-lain

### Konfigurasi Sokongan Model Mistral

Kemas kini `enableMistral` kepada `true` dalam [cdk.json](./cdk/cdk.json), dan jalankan `npx cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Penting]
> Projek ini fokus kepada model Anthropic Claude, model Mistral mempunyai sokongan terhad. Contohnya, contoh prompt adalah berdasarkan model Claude. Ini adalah pilihan Mistral sahaja, sebaik sahaja anda menghidupkan model Mistral, anda hanya boleh menggunakan model Mistral untuk semua ciri sembang, BUKAN kedua-dua model Claude dan Mistral.

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

### Nyahaktifkan Pendaftaran Sendiri

Sampel ini mempunyai pendaftaran sendiri yang diaktifkan secara lalai. Untuk menyahdayakan pendaftaran sendiri, buka [cdk.json](./cdk/cdk.json) dan tukar `selfSignUpEnabled` kepada `false`. Jika anda mengkonfigurasi [pembekal identiti luar](#external-identity-provider), nilainya akan diabaikan dan secara automatik dimatikan.

### Hadkan Domain untuk Alamat E-mel Pendaftaran

Secara lalai, sampel ini tidak menyekat domain untuk alamat e-mel pendaftaran. Untuk membenarkan pendaftaran hanya dari domain tertentu, buka `cdk.json` dan nyatakan domain sebagai senarai dalam `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Pembekal Identiti Luar

Sampel ini menyokong pembekal identiti luar. Kini kami menyokong [Google](./idp/SET_UP_GOOGLE_ms-MY.md) dan [pembekal OIDC tersuai](./idp/SET_UP_CUSTOM_OIDC_ms-MY.md).

### Tambahkan pengguna baru ke kumpulan secara automatik

Sampel ini mempunyai kumpulan berikut untuk memberikan izin kepada pengguna:

- [`Admin`](./ADMINISTRATOR_ms-MY.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_ms-MY.md)

Jika anda ingin pengguna yang baru dicipta secara automatik menyertai kumpulan, anda boleh menyatakannya dalam [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Secara lalai, pengguna yang baru dicipta akan disertakan ke kumpulan `CreatingBotAllowed`.

(Terjemahan diteruskan untuk bahagian yang selebihnya dengan cara yang sama)

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