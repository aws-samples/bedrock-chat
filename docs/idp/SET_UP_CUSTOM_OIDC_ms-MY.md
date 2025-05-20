# Sediakan pembekal identiti luar

## Langkah 1: Buat Pelanggan OIDC

Ikuti prosedur untuk penyedia OIDC yang disasarkan, dan catat nilai untuk ID pelanggan OIDC dan rahsia. URL penerbit juga diperlukan pada langkah berikutnya. Jika URI pengalihan diperlukan untuk proses penyediaan, masukkan nilai tiruan, yang akan diganti selepas penyebaran selesai.

## Langkah 2: Simpan Credentials dalam AWS Secrets Manager

1. Pergi ke AWS Management Console.
2. Navigasi ke Secrets Manager dan pilih "Store a new secret".
3. Pilih "Other type of secrets".
4. Masukkan client ID dan client secret sebagai pasangan kunci-nilai.

   - Kunci: `clientId`, Nilai: <YOUR_GOOGLE_CLIENT_ID>
   - Kunci: `clientSecret`, Nilai: <YOUR_GOOGLE_CLIENT_SECRET>
   - Kunci: `issuerUrl`, Nilai: <ISSUER_URL_OF_THE_PROVIDER>

5. Ikuti petunjuk untuk memberi nama dan menjelaskan secret. Catat nama secret kerana anda akan memerlukannya dalam kod CDK anda (Digunakan dalam nama variabel Langkah 3 <YOUR_SECRET_NAME>).
6. Semak dan simpan secret.

### Perhatian

Nama kunci mestilah sepadan tepat dengan rentetan `clientId`, `clientSecret` dan `issuerUrl`.

## Langkah 3: Kemas Kini cdk.json

Dalam fail cdk.json anda, tambahkan ID Provider dan SecretName ke dalam fail cdk.json.

seperti berikut:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Jangan tukar
        "serviceName": "<NAMA_PERKHIDMATAN_ANDA>", // Tetapkan sebarang nilai yang anda suka
        "secretName": "<NAMA_RAHSIA_ANDA>"
      }
    ],
    "userPoolDomainPrefix": "<AWALAN_DOMAIN_UNIK_UNTUK_KUMPULAN_PENGGUNA_ANDA>"
  }
}
```

### Perhatian

#### Keunikan

`userPoolDomainPrefix` mestilah unik secara global merentasi semua pengguna Amazon Cognito. Jika anda memilih awalan yang sudah digunakan oleh akaun AWS lain, pengwujudan domain kumpulan pengguna akan gagal. Adalah amalan yang baik untuk memasukkan pengecam, nama projek, atau nama persekitaran dalam awalan untuk memastikan keunikan.

## Langkah 4: Deploy Stack CDK Anda

Deploy stack CDK anda ke AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Langkah 5: Kemas Kini Klien OIDC dengan URI Pengalihan Cognito

Selepas menggunakan stack, `AuthApprovedRedirectURI` akan dipaparkan dalam output CloudFormation. Kembali ke konfigurasi OIDC anda dan kemas kini dengan URI pengalihan yang betul.