# Sediakan pembekal identiti luaran untuk Google

## Langkah 1: Cipta Klien Google OAuth 2.0

1. Pergi ke Konsol Pembangun Google.
2. Cipta projek baharu atau pilih yang sedia ada.
3. Navigasi ke "Credentials", kemudian klik pada "Create Credentials" dan pilih "OAuth client ID".
4. Konfigurasikan skrin persetujuan jika diminta.
5. Untuk jenis aplikasi, pilih "Web application".
6. Biarkan URI pengalihan kosong buat masa ini untuk ditetapkan kemudian.[Lihat Langkah5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Setelah dicipta, catat ID Klien dan Rahsia Klien.

Untuk maklumat lanjut, layari [dokumen rasmi Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Langkah 2: Simpan Kelayakan Google OAuth dalam AWS Secrets Manager

1. Pergi ke Konsol Pengurusan AWS.
2. Navigasi ke Secrets Manager dan pilih "Store a new secret".
3. Pilih "Other type of secrets".
4. Masukkan clientId dan clientSecret Google OAuth sebagai pasangan kunci-nilai.

   1. Kunci: clientId, Nilai: <YOUR_GOOGLE_CLIENT_ID>
   2. Kunci: clientSecret, Nilai: <YOUR_GOOGLE_CLIENT_SECRET>

5. Ikuti arahan untuk menamakan dan menerangkan rahsia tersebut. Ambil perhatian nama rahsia kerana anda akan memerlukannya dalam kod CDK anda. Contohnya, googleOAuthCredentials.(Gunakan dalam Langkah 3 nama pembolehubah <YOUR_SECRET_NAME>)
6. Semak dan simpan rahsia tersebut.

### Perhatian

Nama kunci mesti sepadan tepat dengan rentetan 'clientId' dan 'clientSecret'.

## Langkah 3: Kemas kini cdk.json

Dalam fail cdk.json anda, tambah ID Provider dan SecretName ke dalam fail cdk.json.

seperti berikut:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Perhatian

#### Keunikan

Prefix userPoolDomain mestilah unik secara global merentasi semua pengguna Amazon Cognito. Jika anda memilih prefix yang telah digunakan oleh akaun AWS yang lain, penciptaan domain kumpulan pengguna akan gagal. Adalah amalan yang baik untuk memasukkan pengecam, nama projek, atau nama persekitaran dalam prefix untuk memastikan keunikan.

## Langkah 4: Melancarkan Tindanan CDK Anda

Lancarkan tindanan CDK anda ke AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Langkah 5: Kemas Kini Klien OAuth Google dengan URI Pengalihan Cognito

Selepas menggunakan tindanan, AuthApprovedRedirectURI akan dipaparkan pada output CloudFormation. Kembali ke Konsol Pembangun Google dan kemas kini klien OAuth dengan URI pengalihan yang betul.