# Agen Berkuasa LLM (ReAct)

## Apakah itu Ejen (ReAct)?

Ejen adalah sistem AI canggih yang menggunakan model bahasa besar (LLM) sebagai enjin pengiraan pusat. Ia menggabungkan kemampuan penaakulan LLM dengan fungsi tambahan seperti perancangan dan penggunaan alat untuk melakukan tugas kompleks secara autonomi. Ejen boleh menguraikan pertanyaan yang rumit, menjana penyelesaian langkah demi langkah, dan berinteraksi dengan alat atau API luaran untuk mengumpul maklumat atau melaksanakan subtugas.

Sampel ini melaksanakan Ejen menggunakan pendekatan [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct membolehkan ejen menyelesaikan tugas kompleks dengan menggabungkan penaakulan dan tindakan dalam gelung maklum balas berulang. Ejen berulang kali melalui tiga langkah utama: Pemikiran, Tindakan, dan Pemerhatian. Ia menganalisis situasi semasa menggunakan LLM, memutuskan tindakan seterusnya yang perlu diambil, melaksanakan tindakan menggunakan alat atau API yang tersedia, dan belajar daripada keputusan yang diamati. Proses berterusan ini membolehkan ejen menyesuaikan diri dengan persekitaran dinamik, meningkatkan ketepatan penyelesaian tugas, dan menyediakan penyelesaian yang sedar konteks.

## Contoh Kes Penggunaan

Ejen yang menggunakan ReAct boleh digunakan dalam pelbagai senario, menyediakan penyelesaian yang tepat dan cekap.

### Teks-ke-SQL

Pengguna meminta "jumlah jualan untuk suku tahun terakhir." Ejen mentafsirkan permintaan ini, menukar ia kepada pertanyaan SQL, melaksanakannya terhadap pangkalan data, dan memaparkan hasilnya.

### Ramalan Kewangan

Penganalisis kewangan perlu meramalkan pendapatan suku tahun hadapan. Ejen mengumpul data yang berkaitan, melakukan pengiraan yang diperlukan menggunakan model kewangan, dan menjana laporan ramalan terperinci, memastikan ketepatan unjuran.

## Untuk Menggunakan Ciri-ciri Ejen

Untuk mengaktifkan fungsi Ejen untuk chatbot tersuai anda, ikuti langkah-langkah berikut:

Terdapat dua cara untuk menggunakan ciri-ciri Ejen:

### Menggunakan Penggunaan Alat

Untuk mengaktifkan fungsi Ejen dengan Penggunaan Alat untuk chatbot tersuai anda, ikuti langkah-langkah berikut:

1. Pergi ke bahagian Ejen dalam skrin bot tersuai.

2. Dalam bahagian Ejen, anda akan menemui senarai alat yang tersedia yang boleh digunakan oleh Ejen. Secara lalai, semua alat adalah tidak aktif.

3. Untuk mengaktifkan alat, hanya togol suis di sebelah alat yang diinginkan. Sebaik sahaja alat diaktifkan, Ejen akan mempunyai akses kepadanya dan dapat menggunakannya semasa memproses pertanyaan pengguna.

![](./imgs/agent_tools.png)

4. Contohnya, alat "Carian Internet" membolehkan Ejen mengambil maklumat dari internet untuk menjawab soalan pengguna.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Anda boleh membangun dan menambah alat tersuai anda sendiri untuk mengembangkan keupayaan Ejen. Rujuk bahagian [Cara Membangun Alat Anda Sendiri](#how-to-develop-your-own-tools) untuk maklumat lanjut tentang membuat dan mengintegrasikan alat tersuai.

### Menggunakan Ejen Bedrock

Anda boleh menggunakan [Ejen Bedrock](https://aws.amazon.com/bedrock/agents/) yang dibuat dalam Amazon Bedrock.

Pertama, buat Ejen di Bedrock (contohnya, melalui Konsol Pengurusan). Kemudian, nyatakan ID Ejen dalam skrin tetapan bot tersuai. Sebaik sahaja ditetapkan, chatbot anda akan memanfaatkan Ejen Bedrock untuk memproses pertanyaan pengguna.

![](./imgs/bedrock_agent_tool.png)

## Cara Membangun Alat Anda Sendiri

Untuk membangun alat khusus anda sendiri untuk Agen, ikuti garis panduan berikut:

- Cipta kelas baru yang mewarisi daripada kelas `AgentTool`. Walaupun antara muka serasi dengan LangChain, implementasi contoh ini menyediakan kelas `AgentTool` sendiri, yang anda patut warisi ([sumber](../backend/app/agents/tools/agent_tool.py)).

- Merujuk kepada implementasi contoh alat [pengiraan BMI](../examples/agents/tools/bmi/bmi.py). Contoh ini menunjukkan cara membuat alat yang mengira Indeks Jisim Badan (BMI) berdasarkan input pengguna.

  - Nama dan penerangan yang diisytiharkan pada alat digunakan apabila LLM mempertimbangkan alat mana yang patut digunakan untuk menjawab soalan pengguna. Dalam erti kata lain, ia disematkan pada prompt apabila memanggil LLM. Jadi disyorkan untuk menerangkan secara tepat sebanyak mungkin.

- [Pilihan] Sebaik sahaja anda telah mengimplementasikan alat khusus anda, disyorkan untuk mengesahkan fungsinya menggunakan skrip ujian ([contoh](../examples/agents/tools/bmi/test_bmi.py)). Skrip ini akan membantu anda memastikan alat anda berfungsi seperti yang dijangkakan.

- Selepas menyelesaikan pembangunan dan pengujian alat khusus anda, pindahkan fail implementasi ke direktori [backend/app/agents/tools/](../backend/app/agents/tools/). Kemudian buka [backend/app/agents/utils.py](../backend/app/agents/utils.py) dan edit `get_available_tools` supaya pengguna dapat memilih alat yang dibangun.

- [Pilihan] Tambahkan nama dan penerangan yang jelas untuk frontend. Langkah ini adalah pilihan, tetapi jika anda tidak melakukan langkah ini, nama alat dan penerangan yang diisytiharkan dalam alat anda akan digunakan. Mereka adalah untuk LLM tetapi bukan untuk pengguna, jadi disyorkan untuk menambahkan penerangan khusus untuk UX yang lebih baik.

  - Edit fail i18n. Buka [en/index.ts](../frontend/src/i18n/en/index.ts) dan tambahkan `name` dan `description` anda sendiri pada `agent.tools`.
  - Edit `xx/index.ts` juga. Di mana `xx` mewakili kod negara yang anda inginkan.

- Jalankan `npx cdk deploy` untuk menggunakan perubahan anda. Ini akan menjadikan alat khusus anda tersedia dalam skrin bot khusus.

## Sumbangan

**Sumbangan kepada repositori alat ini dialu-alukan!** Jika anda membangunkan alat yang berguna dan diimplementasikan dengan baik, pertimbangkan untuk menyumbangkannya kepada projek dengan menghantar isu atau permintaan tarik.