# Agen Berkuasa LLM (ReAct)

## Apakah Agent (ReAct)?

Agent adalah sistem AI termaju yang menggunakan model bahasa besar (LLM) sebagai enjin pengiraan pusat. Ia menggabungkan kemampuan penaakulan LLM dengan fungsi tambahan seperti perancangan dan penggunaan alat untuk melakukan tugas kompleks secara autonomi. Agent dapat memecahkan pertanyaan yang rumit, menjana penyelesaian langkah demi langkah, dan berinteraksi dengan alat atau API luar untuk mengumpul maklumat atau melaksanakan sub-tugas.

Contoh ini melaksanakan Agent menggunakan pendekatan [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct membolehkan agent menyelesaikan tugas kompleks dengan menggabungkan penaakulan dan tindakan dalam gelung maklum balas berulang. Agent berulang kali melalui tiga langkah utama: Pemikiran, Tindakan, dan Pemerhatian. Ia menganalisis situasi semasa menggunakan LLM, memutuskan tindakan seterusnya yang perlu diambil, melaksanakan tindakan menggunakan alat atau API yang tersedia, dan belajar daripada keputusan yang diperhatikan. Proses berterusan ini membolehkan agent menyesuaikan diri dengan persekitaran dinamik, meningkatkan ketepatan penyelesaian tugas, dan menyediakan penyelesaian yang peka konteks.

## Contoh Kes Penggunaan

Ejen yang menggunakan ReAct boleh diaplikasikan dalam pelbagai senario, menyediakan penyelesaian yang tepat dan cekap.

### Teks-ke-SQL

Pengguna meminta "jumlah jualan untuk suku tahun lepas." Ejen mentafsirkan permintaan ini, menukar ia ke dalam pertanyaan SQL, melaksanakannya terhadap pangkalan data, dan mempersembahkan hasilnya.

### Ramalan Kewangan

Penganalisis kewangan perlu meramalkan pendapatan suku tahun hadapan. Ejen mengumpul data yang berkaitan, melakukan pengiraan yang diperlukan menggunakan model kewangan, dan menjana laporan ramalan terperinci, memastikan ketepatan unjuran.

## Untuk Menggunakan Fitur Ejen

Untuk mengaktifkan fungsionaliti Ejen untuk chatbot tersuai anda, ikuti langkah-langkah berikut:

1. Pergi ke bahagian Ejen dalam skrin bot tersuai.

2. Dalam bahagian Ejen, anda akan menemui senarai alat yang tersedia yang boleh digunakan oleh Ejen. Secara lalai, semua alat adalah tidak aktif.

3. Untuk mengaktifkan alat, hanya togol suis di sebelah alat yang dikehendaki. Sebaik sahaja alat diaktifkan, Ejen akan mempunyai akses kepadanya dan dapat menggunakannya semasa memproses pertanyaan pengguna.

![](./imgs/agent_tools.png)

> [!Penting]
> Adalah penting untuk diambil perhatian bahawa mengaktifkan mana-mana alat dalam bahagian Ejen akan secara automatik menganggap fungsi ["Pengetahuan"](https://aws.amazon.com/what-is/retrieval-augmented-generation/) sebagai alat juga. Ini bermakna LLM akan secara autonomi menentukan sama ada untuk menggunakan "Pengetahuan" untuk menjawab pertanyaan pengguna, dengan mempertimbangkannya sebagai salah satu alat yang tersedia.

4. Secara lalai, alat "Carian Internet" disediakan. Alat ini membolehkan Ejen mencari maklumat dari internet untuk menjawab soalan pengguna.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

Alat ini bergantung kepada [DuckDuckGo](https://duckduckgo.com/) yang mempunyai had kadar. Ia sesuai untuk PoC atau tujuan demo, tetapi jika anda ingin menggunakannya untuk persekitaran pengeluaran, kami mencadangkan untuk menggunakan API carian lain.

5. Anda boleh membangun dan menambah alat tersuai anda sendiri untuk mengembangkan keupayaan Ejen. Rujuk bahagian [Cara Membangun Alat Anda Sendiri](#how-to-develop-your-own-tools) untuk maklumat lanjut tentang membuat dan mengintegrasikan alat tersuai.

## Cara Membangun Alat Anda Sendiri

Untuk membangun alat khusus anda sendiri untuk Agent, ikuti panduan berikut:

- Buat kelas baru yang mewarisi dari kelas `AgentTool`. Walaupun antara muka adalah serasi dengan LangChain, implementasi contoh ini menyediakan kelas `AgentTool` sendiri, yang perlu anda warisi ([sumber](../backend/app/agents/tools/agent_tool.py)).

- Rujuk implementasi contoh alat [pengiraan BMI](../examples/agents/tools/bmi/bmi.py). Contoh ini menunjukkan cara membuat alat yang mengira Indeks Jisim Tubuh (BMI) berdasarkan input pengguna.

  - Nama dan keterangan yang diisytiharkan pada alat digunakan apabila LLM mempertimbangkan alat mana yang perlu digunakan untuk menjawab soalan pengguna. Dalam erti kata lain, ia disematkan pada prompt apabila memanggil LLM. Oleh itu, disyorkan untuk menjelaskan secara tepat sebanyak mungkin.

- [Pilihan] Setelah anda mengimplementasikan alat khusus anda, disyorkan untuk mengesahkan fungsinya menggunakan skrip ujian ([contoh](../examples/agents/tools/bmi/test_bmi.py)). Skrip ini akan membantu anda memastikan alat anda berfungsi seperti yang dijangkakan.

- Selepas menyelesaikan pembangunan dan pengujian alat khusus anda, pindahkan fail implementasi ke direktori [backend/app/agents/tools/](../backend/app/agents/tools/). Kemudian buka [backend/app/agents/utils.py](../backend/app/agents/utils.py) dan edit `get_available_tools` supaya pengguna dapat memilih alat yang dibangun.

- [Pilihan] Tambahkan nama dan keterangan yang jelas untuk antara muka pengguna. Langkah ini adalah pilihan, tetapi jika anda tidak melakukan langkah ini, nama alat dan keterangan yang diisytiharkan dalam alat anda akan digunakan. Mereka adalah untuk LLM tetapi bukan untuk pengguna, jadi disyorkan untuk menambahkan penjelasan khusus untuk UX yang lebih baik.

  - Edit fail i18n. Buka [en/index.ts](../frontend/src/i18n/en/index.ts) dan tambahkan `name` dan `description` anda sendiri pada `agent.tools`.
  - Edit `xx/index.ts` juga. Di mana `xx` mewakili kod negara yang anda inginkan.

- Jalankan `npx cdk deploy` untuk menggunakan perubahan anda. Ini akan menjadikan alat khusus anda tersedia dalam skrin bot khusus.

## Sumbangan

**Sumbangan ke repositori alat ini dialu-alukan!** Jika anda membangunkan alat yang berguna dan dilaksanakan dengan baik, pertimbangkan untuk menyumbangkannya kepada projek dengan menghantar isu atau permintaan tarik.