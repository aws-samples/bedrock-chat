# Ejen Berkuasa LLM (ReAct)

## Apakah Agent (ReAct)?

Agent adalah sistem AI termaju yang menggunakan model bahasa besar (LLM) sebagai enjin pengkomputeran utamanya. Ia menggabungkan keupayaan penaakulan LLM dengan fungsi tambahan seperti perancangan dan penggunaan alat untuk melaksanakan tugas kompleks secara automatik. Agent boleh memecahkan pertanyaan rumit, menjana penyelesaian langkah demi langkah, dan berinteraksi dengan alat luaran atau API untuk mengumpul maklumat atau melaksanakan subtugas.

Sampel ini mengimplementasikan Agent menggunakan pendekatan [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct membolehkan agent menyelesaikan tugas kompleks dengan menggabungkan penaakulan dan tindakan dalam gelung maklum balas berulang. Agent berulang kali melalui tiga langkah utama: Pemikiran, Tindakan, dan Pemerhatian. Ia menganalisis situasi semasa menggunakan LLM, membuat keputusan tentang tindakan seterusnya yang perlu diambil, melaksanakan tindakan menggunakan alat atau API yang tersedia, dan belajar daripada hasil yang diperhatikan. Proses berterusan ini membolehkan agent menyesuaikan diri dengan persekitaran dinamik, meningkatkan ketepatan penyelesaian tugas, dan menyediakan penyelesaian yang peka konteks.

Implementasi ini dikuasakan oleh [Strands Agents](https://strandsagents.com/), SDK sumber terbuka yang mengambil pendekatan berasaskan model untuk membina agent AI. Strands menyediakan rangka kerja yang ringan dan fleksibel untuk mencipta alat tersuai menggunakan penghias Python dan menyokong pelbagai pembekal model termasuk Amazon Bedrock.

## Contoh Kes Penggunaan

Ejen yang menggunakan ReAct boleh digunakan dalam pelbagai senario, memberikan penyelesaian yang tepat dan cekap.

### Teks-ke-SQL

Seorang pengguna bertanya tentang "jumlah jualan untuk suku tahun lepas." Ejen mentafsir permintaan ini, menukarkannya kepada pertanyaan SQL, melaksanakannya terhadap pangkalan data, dan menyampaikan hasilnya.

### Ramalan Kewangan

Seorang penganalisis kewangan perlu meramalkan hasil suku tahun akan datang. Ejen mengumpulkan data yang berkaitan, melakukan pengiraan yang diperlukan menggunakan model kewangan, dan menghasilkan laporan ramalan terperinci, memastikan ketepatan unjuran tersebut.

## Untuk menggunakan ciri Agent

Untuk mengaktifkan fungsi Agent bagi chatbot tersuai anda, ikuti langkah-langkah berikut:

Terdapat dua cara untuk menggunakan ciri Agent:

### Menggunakan Tool Use

Untuk mengaktifkan fungsi Agent dengan Tool Use bagi chatbot tersuai anda, ikuti langkah-langkah berikut:

1. Navigasi ke bahagian Agent dalam skrin bot tersuai.

2. Di bahagian Agent, anda akan menjumpai senarai alat yang tersedia untuk digunakan oleh Agent. Secara lalai, semua alat dinyahaktifkan.

3. Untuk mengaktifkan alat, hanya togol suis di sebelah alat yang dikehendaki. Setelah alat diaktifkan, Agent akan mempunyai akses kepadanya dan boleh menggunakannya semasa memproses pertanyaan pengguna.

![](./imgs/agent_tools.png)

4. Sebagai contoh, alat "Internet Search" membolehkan Agent mendapatkan maklumat dari internet untuk menjawab soalan pengguna.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Anda boleh membangun dan menambah alat tersuai anda sendiri untuk meluaskan keupayaan Agent. Rujuk bahagian [How to develop your own tools](#how-to-develop-your-own-tools) untuk maklumat lanjut tentang mencipta dan mengintegrasikan alat tersuai.

### Menggunakan Bedrock Agent

Anda boleh menggunakan [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) yang dicipta dalam Amazon Bedrock.

Pertama, cipta Agent dalam Bedrock (contohnya, melalui Management Console). Kemudian, tentukan ID Agent dalam skrin tetapan bot tersuai. Setelah ditetapkan, chatbot anda akan memanfaatkan Bedrock Agent untuk memproses pertanyaan pengguna.

![](./imgs/bedrock_agent_tool.png)

## Cara membangunkan alat sendiri

Untuk membangunkan alat tersuai sendiri untuk Agen menggunakan Strands SDK, ikuti garis panduan berikut:

### Mengenai Alat Strands

Strands menyediakan penghias `@tool` yang mudah yang menukar fungsi Python biasa kepada alat agen AI. Penghias ini secara automatik mengekstrak maklumat dari docstring fungsi anda dan petunjuk jenis untuk mencipta spesifikasi alat yang boleh difahami dan digunakan oleh LLM. Pendekatan ini memanfaatkan ciri-ciri natif Python untuk pengalaman pembangunan alat yang bersih dan berfungsi.

Untuk maklumat terperinci mengenai alat Strands, lihat [dokumentasi Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Penciptaan Alat Asas

Cipta fungsi baru yang dihias dengan penghias `@tool` dari Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Perform mathematical calculations safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Result in Strands format with toolUseId, status, and content
    """
    try:
        # Your calculation logic here
        result = eval(expression)  # Note: Use safe evaluation in production
        return {
            "toolUseId": "placeholder",
            "status": "success",
            "content": [{"text": str(result)}]
        }
    except Exception as e:
        return {
            "toolUseId": "placeholder",
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }
```

### Alat dengan Konteks Bot (Corak Penutupan)

Untuk mengakses maklumat bot (BotModel), gunakan corak penutupan yang menangkap konteks bot:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Create calculator tool with bot context closure."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Perform mathematical calculations safely.

        Args:
            expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Result in Strands format with toolUseId, status, and content
        """
        # Access bot context within the tool
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Use safe evaluation in production
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"text": str(result)}]
            }
        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Error: {str(e)}"}]
            }

    return calculator
```

### Keperluan Format Pulangan

Semua alat Strands mesti memulangkan kamus dengan struktur berikut:

```python
{
    "toolUseId": "placeholder",  # Will be replaced by Strands
    "status": "success" | "error",
    "content": [
        {"text": "Simple text response"} |
        {"json": {"key": "Complex data object"}}
    ]
}
```

- Gunakan `{"text": "message"}` untuk respons teks mudah
- Gunakan `{"json": data}` untuk data kompleks yang perlu dikekalkan sebagai maklumat berstruktur
- Sentiasa tetapkan `status` kepada sama ada `"success"` atau `"error"`

### Garis Panduan Implementasi

- Nama fungsi dan docstring digunakan apabila LLM mempertimbangkan alat mana yang hendak digunakan. Docstring dibenamkan dalam prompt, jadi terangkan tujuan dan parameter alat dengan tepat.

- Rujuk implementasi contoh [alat pengiraan BMI](../examples/agents/tools/bmi/bmi_strands.py). Contoh ini menunjukkan cara mencipta alat yang mengira Indeks Jisim Badan (BMI) menggunakan penghias `@tool` Strands dan corak penutupan.

- Selepas selesai pembangunan, letakkan fail implementasi anda dalam direktori [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Kemudian buka [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) dan edit `get_strands_registered_tools` untuk memasukkan alat baru anda.

- [Pilihan] Tambah nama dan penerangan yang jelas untuk frontend. Langkah ini adalah pilihan, tetapi jika anda tidak melakukan langkah ini, nama alat dan penerangan dari fungsi anda akan digunakan. Memandangkan ini adalah untuk penggunaan LLM, adalah disyorkan untuk menambah penerangan mesra pengguna untuk UX yang lebih baik.

  - Edit fail i18n. Buka [en/index.ts](../frontend/src/i18n/en/index.ts) dan tambah `name` dan `description` anda sendiri pada `agent.tools`.
  - Edit `xx/index.ts` juga. Di mana `xx` mewakili kod negara yang anda inginkan.

- Jalankan `npx cdk deploy` untuk mengatur perubahan anda. Ini akan menjadikan alat tersuai anda tersedia dalam skrin bot tersuai.