# Sediakan pembekal identiti luaran

## Langkah 1: Cipta Pelanggan OIDC

Ikuti prosedur untuk penyedia OIDC sasaran, dan catatkan nilai-nilai ID pelanggan OIDC dan rahsia. URL pengeluar juga diperlukan pada langkah-langkah berikutnya. Jika URI lencongan diperlukan untuk proses persediaan, masukkan nilai dummy, yang akan digantikan selepas penempatan selesai.

## Langkah 2: Simpan Kelayakan dalam AWS Secrets Manager

1. Pergi ke Konsol Pengurusan AWS.
2. Navigasi ke Secrets Manager dan pilih "Store a new secret".
3. Pilih "Other type of secrets".
4. Masukkan ID klien dan rahsia klien sebagai pasangan kunci-nilai.

   - Kunci: `clientId`, Nilai: <YOUR_GOOGLE_CLIENT_ID>
   - Kunci: `clientSecret`, Nilai: <YOUR_GOOGLE_CLIENT_SECRET>
   - Kunci: `issuerUrl`, Nilai: <ISSUER_URL_OF_THE_PROVIDER>

5. Ikuti arahan untuk menamakan dan menerangkan rahsia tersebut. Catat nama rahsia kerana anda akan memerlukannya dalam kod CDK anda (Digunakan dalam nama pembolehubah Langkah 3 <YOUR_SECRET_NAME>).
6. Semak dan simpan rahsia tersebut.

### Perhatian

Nama kunci mesti sepadan tepat dengan rentetan `clientId`, `clientSecret` dan `issuerUrl`.

## Langkah 3: Kemas kini cdk.json

Dalam fail cdk.json anda, tambahkan ID Provider dan SecretName ke dalam fail cdk.json.

seperti berikut:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Jangan ubah
        "serviceName": "<YOUR_SERVICE_NAME>", // Tetapkan nilai yang anda suka
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Perhatian

#### Keunikan

`userPoolDomainPrefix` mestilah unik secara global merentasi semua pengguna Amazon Cognito. Jika anda memilih awalan yang telah digunakan oleh akaun AWS yang lain, pembuatan domain kumpulan pengguna akan gagal. Adalah amalan yang baik untuk memasukkan pengecam, nama projek, atau nama persekitaran dalam awalan untuk memastikan keunikan.

## Langkah 4: Gunakan Stack CDK Anda

Gunakan stack CDK anda ke AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Langkah 5: Kemas kini Pelanggan OIDC dengan URI Pengalihan Cognito

Selepas menggunakan tindanan, `AuthApprovedRedirectURI` akan dipaparkan pada output CloudFormation. Kembali ke konfigurasi OIDC anda dan kemas kini dengan URI pengalihan yang betul.