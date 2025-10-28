# Pembangunan tempatan

## Pembangunan Backend

Lihat [backend/README](../backend/README_ms-MY.md).

## Pembangunan Frontend

Dalam contoh ini, anda boleh mengubah suai dan melancarkan frontend secara tempatan menggunakan sumber AWS (`API Gateway`, `Cognito`, dll.) yang telah dikerah dengan `npx cdk deploy`.

1. Rujuk [Deploy using CDK](../README.md#deploy-using-cdk) untuk pengerahan pada persekitaran AWS.
2. Salin `frontend/.env.template` dan simpan sebagai `frontend/.env.local`.
3. Isikan kandungan `.env.local` berdasarkan hasil output dari `npx cdk deploy` (seperti `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Laksanakan arahan berikut:

```zsh
cd frontend && npm ci && npm run dev
```

## (Pilihan, disyorkan) Menyediakan cangkuk pra-commit

Kami telah memperkenalkan aliran kerja GitHub untuk pemeriksaan jenis dan pelintingan. Ini dilaksanakan apabila Pull Request dibuat, tetapi menunggu pelintingan selesai sebelum meneruskan bukanlah pengalaman pembangunan yang baik. Oleh itu, tugas-tugas pelintingan ini harus dilakukan secara automatik pada peringkat commit. Kami telah memperkenalkan [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) sebagai mekanisme untuk mencapai ini. Ia tidak wajib, tetapi kami mengesyorkan penggunaannya untuk pengalaman pembangunan yang cekap. Selain itu, walaupun kami tidak menguatkuasakan pemformatan TypeScript dengan [Prettier](https://prettier.io/), kami akan menghargai jika anda boleh menggunakannya semasa menyumbang, kerana ia membantu mengelakkan perbezaan yang tidak perlu semasa semakan kod.

### Memasang lefthook

Rujuk [di sini](https://github.com/evilmartians/lefthook#install). Jika anda pengguna mac dan homebrew, hanya jalankan `brew install lefthook`.

### Memasang poetry

Ini diperlukan kerana pelintingan kod python bergantung kepada `mypy` dan `black`.

```sh
cd backend
python3 -m venv .venv  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
source .venv/bin/activate  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
pip install poetry
poetry install
```

Untuk maklumat lanjut, sila semak [backend README](../backend/README_ms-MY.md).

### Mencipta cangkuk pra-commit

Hanya jalankan `lefthook install` pada direktori akar projek ini.