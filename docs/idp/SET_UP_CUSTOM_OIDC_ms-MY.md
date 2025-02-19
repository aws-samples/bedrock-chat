# Sediakan penyedia identiti luar

## Langkah 1: Buat Klien OIDC

Ikuti prosedur untuk penyedia OIDC yang disasarkan, dan catat nilai untuk ID klien OIDC dan rahsia. Selain itu, URL penerbit diperlukan pada langkah berikutnya. Jika URI pengalihan diperlukan untuk proses penyediaan, masukkan nilai tiruan, yang akan diganti selepas penerapan selesai.

## Langkah 2: Simpan Kredensial dalam AWS Secrets Manager

1. Pergi ke AWS Management Console.
2. Navigasi ke Secrets Manager dan pilih "Simpan rahsia baru".
3. Pilih "Jenis rahsia lain".
4. Masukkan ID pelanggan dan rahsia pelanggan sebagai pasangan kunci-nilai.

   - Kunci: `clientId`, Nilai: <YOUR_GOOGLE_CLIENT_ID>
   - Kunci: `clientSecret`, Nilai: <YOUR_GOOGLE_CLIENT_SECRET>
   - Kunci: `issuerUrl`, Nilai: <ISSUER_URL_OF_THE_PROVIDER>

5. Ikuti petunjuk untuk memberi nama dan menerangkan rahsia. Catat nama rahsia kerana anda akan memerlukannya dalam kod CDK anda (Digunakan dalam nama pembolehubah Langkah 3 <YOUR_SECRET_NAME>).
6. Semak dan simpan rahsia.

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

`userPoolDomainPrefix` mestilah unik secara global merentas semua pengguna Amazon Cognito. Jika anda memilih awalan yang sudah digunakan oleh akaun AWS lain, penciptaan domain kumpulan pengguna akan gagal. Adalah amalan yang baik untuk memasukkan pengecam, nama projek, atau nama persekitaran dalam awalan untuk memastikan keunikan.

## Langkah 4: Deploy Stack CDK Anda

Deploy stack CDK anda ke AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Langkah 5: Kemas Kini Klien OIDC dengan URI Pengalihan Cognito

Selepas menggunakan stack, `AuthApprovedRedirectURI` akan dipaparkan dalam output CloudFormation. Kembali ke konfigurasi OIDC anda dan kemas kini dengan URI pengalihan yang betul.