# Agen Berkuasa LLM (ReAct)

## Apakah Agen (ReAct)?

Agen adalah sistem AI canggih yang menggunakan model bahasa besar (LLM) sebagai mesin komputasi utamanya. Ia menggabungkan kemampuan penalaran LLM dengan fungsionalitas tambahan seperti perancangan dan penggunaan alat untuk melakukan tugas kompleks secara autonomi. Agen dapat memecah pertanyaan yang rumit, menghasilkan penyelesaian langkah demi langkah, dan berinteraksi dengan alat atau API eksternal untuk mengumpulkan informasi atau melaksanakan sub-tugas.

Contoh ini mengimplementasikan Agen menggunakan pendekatan [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct memungkinkan agen menyelesaikan tugas kompleks dengan menggabungkan penalaran dan tindakan dalam gelung maklum balas berulang. Agen berulang kali melalui tiga langkah utama: Pemikiran, Tindakan, dan Pemerhatian. Ia menganalisis situasi semasa menggunakan LLM, memutuskan tindakan selanjutnya yang akan diambil, melaksanakan tindakan menggunakan alat atau API yang tersedia, dan belajar dari keputusan yang diamati. Proses berterusan ini membolehkan agen menyesuaikan diri dengan persekitaran dinamik, meningkatkan ketepatan penyelesaian tugas, dan menyediakan penyelesaian yang peka konteks.

## Contoh Kes Penggunaan

Ejen yang menggunakan ReAct dapat diaplikasikan dalam pelbagai senario, menyediakan penyelesaian yang tepat dan cekap.

### Teks-ke-SQL

Pengguna meminta "jumlah jualan untuk suku tahun terakhir." Ejen mentafsirkan permintaan ini, menukar ia ke dalam pertanyaan SQL, melaksanakannya terhadap pangkalan data, dan membentangkan hasilnya.

### Ramalan Kewangan

Penganalisis kewangan perlu meramalkan pendapatan suku tahun hadapan. Ejen mengumpul data yang berkaitan, melakukan pengiraan yang diperlukan menggunakan model kewangan, dan menjana laporan ramalan terperinci, memastikan ketepatan unjuran.

## Untuk Menggunakan Fitur Ejen

Untuk mengaktifkan fungsionaliti Ejen untuk chatbot yang disesuaikan, ikuti langkah-langkah berikut:

Terdapat dua cara untuk menggunakan fitur Ejen:

### Menggunakan Penggunaan Alat

Untuk mengaktifkan fungsionaliti Ejen dengan Penggunaan Alat untuk chatbot yang disesuaikan, ikuti langkah-langkah berikut:

1. Navigasi ke bahagian Ejen dalam skrin bot tersuai.

2. Dalam bahagian Ejen, anda akan menemui senarai alat yang tersedia yang boleh digunakan oleh Ejen. Secara lalai, semua alat adalah tidak aktif.

3. Untuk mengaktifkan alat, hanya togol suis di sebelah alat yang diinginkan. Sebaik sahaja alat diaktifkan, Ejen akan mempunyai akses kepadanya dan dapat menggunakannya semasa memproses pertanyaan pengguna.

![](./imgs/agent_tools.png)

4. Contohnya, alat "Carian Internet" membolehkan Ejen mengambil maklumat dari internet untuk menjawab soalan pengguna.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Anda boleh membangun dan menambah alat tersuai anda sendiri untuk mengembangkan keupayaan Ejen. Rujuk bahagian [Cara Membangun Alat Anda Sendiri](#how-to-develop-your-own-tools) untuk maklumat lanjut tentang membuat dan mengintegrasikan alat tersuai.

### Menggunakan Ejen Bedrock

Anda boleh menggunakan [Ejen Bedrock](https://aws.amazon.com/bedrock/agents/) yang dibuat di Amazon Bedrock.

Pertama, buat Ejen di Bedrock (contohnya, melalui Konsol Pengurusan). Kemudian, nyatakan ID Ejen dalam skrin tetapan bot tersuai. Sebaik sahaja ditetapkan, chatbot anda akan memanfaatkan Ejen Bedrock untuk memproses pertanyaan pengguna.

![](./imgs/bedrock_agent_tool.png)

## Cara Membangun Alat Anda Sendiri

Untuk membangun alat khusus anda sendiri untuk Agen, ikuti panduan berikut:

- Buat kelas baru yang mewarisi daripada kelas `AgentTool`. Walaupun antara muka adalah serasi dengan LangChain, implementasi contoh ini menyediakan kelas `AgentTool` sendiri, yang mana anda perlu mewarisinya ([sumber](../backend/app/agents/tools/agent_tool.py)).

- Merujuk kepada implementasi contoh alat [pengiraan BMI](../examples/agents/tools/bmi/bmi.py). Contoh ini menunjukkan cara membuat alat yang mengira Indeks Jisim Tubuh (BMI) berdasarkan input pengguna.

  - Nama dan keterangan yang diisytiharkan pada alat digunakan apabila LLM mempertimbangkan alat mana yang perlu digunakan untuk menjawab soalan pengguna. Dalam erti kata lain, ia disematkan pada arahan apabila memanggil LLM. Oleh itu, disyorkan untuk menjelaskan secara tepat sebanyak mungkin.

- [Pilihan] Sebaik sahaja anda telah melaksanakan alat khusus anda, disyorkan untuk mengesahkan fungsinya menggunakan skrip ujian ([contoh](../examples/agents/tools/bmi/test_bmi.py)). Skrip ini akan membantu anda memastikan alat anda berfungsi seperti yang dijangkakan.

- Selepas menyelesaikan pembangunan dan pengujian alat khusus anda, pindahkan fail pelaksanaan ke direktori [backend/app/agents/tools/](../backend/app/agents/tools/). Kemudian buka [backend/app/agents/utils.py](../backend/app/agents/utils.py) dan edit `get_available_tools` supaya pengguna dapat memilih alat yang dibangunkan.

- [Pilihan] Tambahkan nama dan keterangan yang jelas untuk antara muka hadapan. Langkah ini adalah pilihan, tetapi jika anda tidak melakukan langkah ini, nama alat dan keterangan yang diisytiharkan dalam alat anda akan digunakan. Ia adalah untuk LLM tetapi bukan untuk pengguna, oleh itu disyorkan untuk menambahkan penjelasan khusus untuk UX yang lebih baik.

  - Edit fail i18n. Buka [en/index.ts](../frontend/src/i18n/en/index.ts) dan tambahkan `name` dan `description` anda sendiri pada `agent.tools`.
  - Edit `xx/index.ts` juga. Di mana `xx` mewakili kod negara yang anda inginkan.

- Jalankan `npx cdk deploy` untuk menggunakan perubahan anda. Ini akan menjadikan alat khusus anda tersedia dalam skrin bot khusus.

## Sumbangan

**Sumbangan kepada repositori alat ini adalah dialu-alukan!** Jika anda membangunkan alat yang berguna dan diimplementasikan dengan baik, pertimbangkan untuk menyumbangkannya kepada projek dengan menghantar isu atau permintaan tarik.