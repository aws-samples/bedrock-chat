# Pembangunan Tempatan

## Pembangunan Backend

Lihat [backend/README](../backend/README_ms-MY.md).

## Pembangunan Frontend

Dalam contoh ini, anda boleh mengubah dan melancarkan frontend secara tempatan menggunakan sumber AWS (`API Gateway`, `Cognito`, dll.) yang telah digunakan dengan `npx cdk deploy`.

1. Merujuk kepada [Deploy menggunakan CDK](../README.md#deploy-using-cdk) untuk deployment di persekitaran AWS.
2. Salin `frontend/.env.template` dan simpan sebagai `frontend/.env.local`.
3. Isi kandungan `.env.local` berdasarkan keputusan output `npx cdk deploy` (seperti `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Jalankan perintah berikut:

```zsh
cd frontend && npm ci && npm run dev
```

## (Pilihan, disyorkan) Sediakan kait pra-commit

Kami telah memperkenalkan aliran kerja GitHub untuk menyemak jenis dan memeriksa kod. Ini dilakukan apabila Permintaan Tarik (Pull Request) dibuat, tetapi menunggu pemeriksaan kod selesai sebelum meneruskan bukan pengalaman pembangunan yang baik. Oleh itu, tugas pemeriksaan kod ini perlu dilakukan secara automatik pada peringkat commit. Kami telah memperkenalkan [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) sebagai mekanisme untuk mencapai ini. Ia tidak wajib, tetapi kami mengesyorkan untuk menggunakannya bagi pengalaman pembangunan yang cekap. Tambahan pula, walaupun kami tidak mewajibkan pemformatan TypeScript dengan [Prettier](https://prettier.io/), kami akan menghargai jika anda dapat menggunakannya semasa menyumbang, kerana ia membantu mencegah perbezaan yang tidak perlu semasa semakan kod.

### Pasang lefthook

Rujuk [di sini](https://github.com/evilmartians/lefthook#install). Jika anda pengguna mac dan homebrew, hanya jalankan `brew install lefthook`.

### Pasang poetry

Ini diperlukan kerana pemeriksaan kod python bergantung kepada `mypy` dan `black`.

```sh
cd backend
python3 -m venv .venv  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
source .venv/bin/activate  # Pilihan (Jika anda tidak mahu memasang poetry pada env anda)
pip install poetry
poetry install
```

Untuk maklumat lanjut, sila semak [README backend](../backend/README_ms-MY.md).

### Buat kait pra-commit

Hanya jalankan `lefthook install` pada direktori akar projek ini.