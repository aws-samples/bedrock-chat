# Agen Berkuasa LLM (ReAct)

## Apakah itu Ejen (ReAct)?

Ejen adalah sistem AI canggih yang menggunakan model bahasa besar (LLM) sebagai enjin pengiraan pusat. Ia menggabungkan keupayaan penaakulan LLM dengan fungsi tambahan seperti perancangan dan penggunaan alat untuk melakukan tugas kompleks secara autonomi. Ejen dapat memecahkan pertanyaan yang rumit, menjana penyelesaian langkah demi langkah, dan berinteraksi dengan alat atau API luar untuk mengumpul maklumat atau melaksanakan subtugas.

Contoh ini melaksanakan Ejen menggunakan pendekatan [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct membolehkan ejen menyelesaikan tugas kompleks dengan menggabungkan penaakulan dan tindakan dalam gelung maklum balas berulang. Ejen berulang kali melalui tiga langkah utama: Pemikiran, Tindakan, dan Pemerhatian. Ia menganalisis situasi semasa menggunakan LLM, memutuskan tindakan seterusnya yang perlu diambil, melaksanakan tindakan menggunakan alat atau API yang tersedia, dan belajar daripada keputusan yang diperhatikan. Proses berterusan ini membolehkan ejen menyesuaikan diri dengan persekitaran dinamik, meningkatkan ketepatan penyelesaian tugas, dan memberikan penyelesaian yang peka konteks.

## Contoh Kes Penggunaan

Ejen yang menggunakan ReAct boleh digunakan dalam pelbagai senario, menyediakan penyelesaian yang tepat dan cekap.

### Teks-ke-SQL

Pengguna meminta "jumlah jualan untuk suku tahun terakhir." Ejen menterjemahkan permintaan ini, menukar kepada pertanyaan SQL, melaksanakannya terhadap pangkalan data, dan memaparkan hasilnya.

### Ramalan Kewangan

Penganalisis kewangan perlu meramalkan pendapatan suku tahun hadapan. Ejen mengumpul data yang berkaitan, melakukan pengiraan yang diperlukan menggunakan model kewangan, dan menjana laporan ramalan terperinci, memastikan ketepatan unjuran.

## Cara Menggunakan Fitur Ejen

Untuk mengaktifkan fungsi Ejen untuk chatbot tersuai anda, ikuti langkah-langkah berikut:

1. Pergi ke bahagian Ejen dalam skrin bot tersuai.

2. Dalam bahagian Ejen, anda akan menemui senarai alat yang tersedia yang boleh digunakan oleh Ejen. Secara lalai, semua alat adalah tidak aktif.

3. Untuk mengaktifkan alat, hanya togol suis di sebelah alat yang dikehendaki. Sebaik sahaja alat diaktifkan, Ejen akan mempunyai akses kepadanya dan dapat menggunakannya semasa memproses pertanyaan pengguna.

![](./imgs/agent_tools.png)

> [!Penting]
> Adalah penting untuk diambil perhatian bahawa mengaktifkan mana-mana alat dalam bahagian Ejen akan secara automatik menganggap fungsi "Pengetahuan" sebagai alat juga. Ini bermakna LLM akan secara autonomi menentukan sama ada untuk menggunakan "Pengetahuan" untuk menjawab pertanyaan pengguna, mempertimbangkannya sebagai salah satu alat yang tersedia.

4. Secara lalai, alat "Carian Internet" disediakan. Alat ini membolehkan Ejen mengambil maklumat dari internet untuk menjawab soalan pengguna.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

Alat ini bergantung kepada [DuckDuckGo](https://duckduckgo.com/) yang mempunyai had kadar. Ia sesuai untuk PoC atau tujuan demo, tetapi jika anda ingin menggunakannya untuk persekitaran pengeluaran, kami mencadangkan untuk menggunakan API carian lain.

5. Anda boleh membangun dan menambah alat tersuai anda sendiri untuk mengembangkan keupayaan Ejen. Rujuk bahagian [Cara Membangun Alat Anda Sendiri](#how-to-develop-your-own-tools) untuk maklumat lanjut tentang membuat dan mengintegrasikan alat tersuai.

## Cara Membangun Alat Anda Sendiri

Untuk membangun alat khusus anda sendiri untuk Agent, ikuti panduan berikut:

- Buat kelas baru yang mewarisi dari kelas `AgentTool`. Walaupun antara muka serasi dengan LangChain, implementasi contoh ini menyediakan kelas `AgentTool` sendiri, yang perlu anda warisi ([sumber](../backend/app/agents/tools/agent_tool.py)).

- Merujuk kepada implementasi contoh alat [pengiraan BMI](../examples/agents/tools/bmi/bmi.py). Contoh ini menunjukkan cara membuat alat yang mengira Indeks Jisim Badan (BMI) berdasarkan input pengguna.

  - Nama dan penerangan yang diisytiharkan pada alat digunakan apabila LLM mempertimbangkan alat mana yang perlu digunakan untuk menjawab soalan pengguna. Dalam erti kata lain, ia disematkan pada arahan apabila memanggil LLM. Jadi disyorkan untuk menghuraikan secara tepat sebanyak mungkin.

- [Pilihan] Setelah anda mengimplementasikan alat khusus anda, disyorkan untuk mengesahkan fungsinya menggunakan skrip ujian ([contoh](../examples/agents/tools/bmi/test_bmi.py)). Skrip ini akan membantu anda memastikan alat anda berfungsi seperti yang dijangkakan.

- Selepas menyelesaikan pembangunan dan pengujian alat khusus anda, pindahkan fail implementasi ke direktori [backend/app/agents/tools/](../backend/app/agents/tools/). Kemudian buka [backend/app/agents/utils.py](../backend/app/agents/utils.py) dan edit `get_available_tools` supaya pengguna dapat memilih alat yang dibangun.

- [Pilihan] Tambahkan nama dan penerangan yang jelas untuk antara muka pengguna. Langkah ini adalah pilihan, tetapi jika anda tidak melakukan langkah ini, nama alat dan penerangan yang diisytiharkan dalam alat anda akan digunakan. Mereka adalah untuk LLM tetapi bukan untuk pengguna, jadi disyorkan untuk menambahkan penerangan khusus untuk UX yang lebih baik.

  - Edit fail i18n. Buka [en/index.ts](../frontend/src/i18n/en/index.ts) dan tambahkan `name` dan `description` anda sendiri pada `agent.tools`.
  - Edit `xx/index.ts` juga. Di mana `xx` mewakili kod negara yang anda inginkan.

- Jalankan `npx cdk deploy` untuk menggunakan perubahan anda. Ini akan menjadikan alat khusus anda tersedia dalam skrin bot khusus.

## Sumbangan

**Sumbangan kepada repositori alat ini dialu-alukan!** Jika anda membangunkan alat yang berguna dan dilaksanakan dengan baik, pertimbangkan untuk menyumbangkannya kepada projek dengan menghantar isu atau permintaan tarik.