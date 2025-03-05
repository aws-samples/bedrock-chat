# Pembangunan Tempatan

## Pembangunan Backend

Lihat [backend/README](../backend/README_ms-MY.md).

## Pembangunan Frontend

Dalam contoh ini, anda boleh mengubah dan melancarkan frontend secara tempatan menggunakan sumber AWS (`API Gateway`, `Cognito`, dll.) yang telah digunakan dengan `npx cdk deploy`.

1. Merujuk kepada [Deployment menggunakan CDK](../README.md#deploy-using-cdk) untuk deployment di persekitaran AWS.
2. Salin `frontend/.env.template` dan simpan sebagai `frontend/.env.local`.
3. Isi kandungan `.env.local` berdasarkan keputusan output `npx cdk deploy` (seperti `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Jalankan perintah berikut:

```zsh
cd frontend && npm ci && npm run dev
```

## (Pilihan, disyorkan) Persediaan kait pra-commit

Kami telah memperkenalkan alur kerja GitHub untuk pemeriksaan jenis dan penyiapan. Ini dilaksanakan apabila Permintaan Tarik dibuat, tetapi menunggu penyiapan selesai sebelum meneruskan bukanlah pengalaman pembangunan yang baik. Oleh itu, tugas penyiapan ini perlu dilakukan secara automatik pada peringkat commit. Kami telah memperkenalkan [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) sebagai mekanisme untuk mencapai ini. Ia tidak wajib, tetapi kami mengesyorkan penggunaannya untuk pengalaman pembangunan yang cekap. Tambahan pula, walaupun kami tidak memaksa format TypeScript dengan [Prettier](https://prettier.io/), kami akan menghargai jika anda dapat menggunakannya semasa menyumbang, kerana ia membantu mencegah perbezaan yang tidak perlu semasa semakan kod.

### Pasang lefthook

Merujuk [di sini](https://github.com/evilmartians/lefthook#install). Jika anda pengguna mac dan homebrew, hanya jalankan `brew install lefthook`.

### Pasang poetry

Ini diperlukan kerana penyiapan kod python bergantung kepada `mypy` dan `black`.

```sh
cd backend
python3 -m venv .venv  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
source .venv/bin/activate  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
pip install poetry
poetry install
```

Untuk maklumat lanjut, sila semak [README backend](../backend/README_ms-MY.md).

### Cipta kait pra-commit

Hanya jalankan `lefthook install` pada direktori root projek ini.