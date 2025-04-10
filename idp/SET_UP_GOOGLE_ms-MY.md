# Sediakan penyedia identiti luar untuk Google

## Langkah 1: Cipta Klien OAuth 2.0 Google

1. Pergi ke Konsol Pembangun Google.
2. Buat projek baru atau pilih projek sedia ada.
3. Navigasi ke "Credentials", kemudian klik "Create Credentials" dan pilih "OAuth client ID".
4. Konfigurasikan skrin persetujuan jika diminta.
5. Untuk jenis aplikasi, pilih "Aplikasi web".
6. Biarkan URI pengalihan kosong buat sementara untuk ditetapkan kemudian, dan simpan sementara.[Lihat Langkah 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Setelah dibuat, catat ID Klien dan Rahsia Klien.

Untuk maklumat lanjut, lawati [dokumen rasmi Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Langkah 2: Simpan Credentials Google OAuth dalam AWS Secrets Manager

1. Pergi ke AWS Management Console.
2. Navigasi ke Secrets Manager dan pilih "Store a new secret".
3. Pilih "Other type of secrets".
4. Masukkan clientId dan clientSecret Google OAuth sebagai pasangan kunci-nilai.

   1. Kunci: clientId, Nilai: <YOUR_GOOGLE_CLIENT_ID>
   2. Kunci: clientSecret, Nilai: <YOUR_GOOGLE_CLIENT_SECRET>

5. Ikuti petunjuk untuk memberi nama dan menjelaskan rahsia. Catat nama rahsia kerana anda akan memerlukannya dalam kod CDK anda. Contohnya, googleOAuthCredentials.(Gunakan dalam nama variabel Langkah 3 <YOUR_SECRET_NAME>)
6. Semak dan simpan rahsia.

### Perhatian

Nama kunci mestilah tepat sama dengan rentetan 'clientId' dan 'clientSecret'.

## Langkah 3: Kemas Kini cdk.json

Dalam fail cdk.json anda, tambahkan ID Provider dan SecretName ke dalam fail cdk.json.

seperti berikut:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<NAMA_RAHSIA_ANDA>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIKS_DOMAIN_UNIK_UNTUK_KUMPULAN_PENGGUNA_ANDA>"
  }
}
```

### Perhatian

#### Keunikan

Prefiks kumpulan pengguna (userPoolDomainPrefix) mestilah unik secara global merentas semua pengguna Amazon Cognito. Jika anda memilih prefiks yang sudah digunakan oleh akaun AWS lain, penghasilan domain kumpulan pengguna akan gagal. Adalah amalan yang baik untuk memasukkan pengecam, nama projek, atau nama persekitaran dalam prefiks untuk memastikan keunikan.

## Langkah 4: Deploy Stack CDK Anda

Deploy stack CDK anda ke AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Langkah 5: Kemas Kini Klien Google OAuth dengan URI Pengalihan Cognito

Selepas menggunakan stack, AuthApprovedRedirectURI akan dipaparkan dalam output CloudFormation. Kembali ke Konsol Pembangun Google dan kemas kini klien OAuth dengan URI pengalihan yang betul.