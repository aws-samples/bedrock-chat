# ตัวแทนที่ขับเคลื่อนด้วย LLM (ReAct)

## Agent (ReAct) คืออะไร?

Agent คือระบบ AI ขั้นสูงที่ใช้โมเดลภาษาขนาดใหญ่ (LLMs) เป็นกลไกการประมวลผลหลัก มันรวมความสามารถในการให้เหตุผลของ LLMs เข้ากับฟังก์ชันการทำงานเพิ่มเติม เช่น การวางแผนและการใช้เครื่องมือ เพื่อทำงานที่ซับซ้อนได้โดยอัตโนมัติ Agents สามารถแยกแยะคำถามที่ซับซ้อน สร้างวิธีแก้ปัญหาทีละขั้นตอน และโต้ตอบกับเครื่องมือภายนอกหรือ APIs เพื่อรวบรวมข้อมูลหรือดำเนินการงานย่อยต่างๆ

ตัวอย่างนี้ใช้ Agent ที่ใช้แนวทาง [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) ReAct ช่วยให้ agent สามารถแก้ปัญหาที่ซับซ้อนได้โดยการผสมผสานการให้เหตุผลและการกระทำในวงจรการตอบสนองแบบต่อเนื่อง agent จะดำเนินการผ่านขั้นตอนสำคัญสามขั้นตอนซ้ำๆ: การคิด การกระทำ และการสังเกต มันวิเคราะห์สถานการณ์ปัจจุบันโดยใช้ LLM ตัดสินใจเลือกการกระทำถัดไป ดำเนินการโดยใช้เครื่องมือหรือ APIs ที่มีอยู่ และเรียนรู้จากผลลัพธ์ที่สังเกตได้ กระบวนการต่อเนื่องนี้ช่วยให้ agent สามารถปรับตัวเข้ากับสภาพแวดล้อมที่เปลี่ยนแปลง ปรับปรุงความแม่นยำในการแก้ปัญหา และให้คำตอบที่เหมาะสมกับบริบท

การใช้งานนี้ขับเคลื่อนด้วย [Strands Agents](https://strandsagents.com/) ซึ่งเป็น SDK โอเพนซอร์สที่ใช้แนวทางที่ขับเคลื่อนด้วยโมเดลในการสร้าง AI agents Strands ให้เฟรมเวิร์กที่มีน้ำหนักเบาและยืดหยุ่นสำหรับการสร้างเครื่องมือที่กำหนดเองโดยใช้ Python decorators และรองรับผู้ให้บริการโมเดลหลายราย รวมถึง Amazon Bedrock

## ตัวอย่างการใช้งาน

Agent ที่ใช้ ReAct สามารถนำไปประยุกต์ใช้ในสถานการณ์ต่างๆ เพื่อให้คำตอบที่แม่นยำและมีประสิทธิภาพ

### การแปลงข้อความเป็น SQL

เมื่อผู้ใช้ถามหา "ยอดขายรวมในไตรมาสที่แล้ว" Agent จะตีความคำขอนี้ แปลงเป็นคำสั่ง SQL รันคำสั่งกับฐานข้อมูล และแสดงผลลัพธ์

### การพยากรณ์ทางการเงิน

นักวิเคราะห์การเงินต้องการพยากรณ์รายได้ในไตรมาสหน้า Agent จะรวบรวมข้อมูลที่เกี่ยวข้อง ทำการคำนวณที่จำเป็นโดยใช้โมเดลทางการเงิน และสร้างรายงานการพยากรณ์อย่างละเอียด พร้อมทั้งตรวจสอบความถูกต้องของการคาดการณ์

## วิธีใช้งานฟีเจอร์ Agent

เพื่อเปิดใช้งานฟังก์ชัน Agent สำหรับแชทบอทที่คุณปรับแต่ง ให้ทำตามขั้นตอนต่อไปนี้:

มีสองวิธีในการใช้งานฟีเจอร์ Agent:

### การใช้ Tool Use

เพื่อเปิดใช้งานฟังก์ชัน Agent ด้วย Tool Use สำหรับแชทบอทที่คุณปรับแต่ง ให้ทำตามขั้นตอนต่อไปนี้:

1. ไปที่ส่วน Agent ในหน้าจอการปรับแต่งบอท

2. ในส่วน Agent คุณจะพบรายการเครื่องมือที่ Agent สามารถใช้งานได้ โดยค่าเริ่มต้น เครื่องมือทั้งหมดจะถูกปิดใช้งาน

3. หากต้องการเปิดใช้งานเครื่องมือ เพียงกดสวิตช์ที่อยู่ถัดจากเครื่องมือที่ต้องการ เมื่อเปิดใช้งานเครื่องมือแล้ว Agent จะสามารถเข้าถึงและใช้งานเครื่องมือนั้นในการประมวลผลคำถามของผู้ใช้ได้

![](./imgs/agent_tools.png)

4. ตัวอย่างเช่น เครื่องมือ "Internet Search" ช่วยให้ Agent สามารถค้นหาข้อมูลจากอินเทอร์เน็ตเพื่อตอบคำถามของผู้ใช้

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. คุณสามารถพัฒนาและเพิ่มเครื่องมือที่กำหนดเองเพื่อขยายความสามารถของ Agent ดูข้อมูลเพิ่มเติมเกี่ยวกับการสร้างและผสานรวมเครื่องมือที่กำหนดเองได้ในส่วน [วิธีพัฒนาเครื่องมือของคุณเอง](#how-to-develop-your-own-tools)

### การใช้ Bedrock Agent

คุณสามารถใช้ [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) ที่สร้างขึ้นใน Amazon Bedrock

ขั้นแรก ให้สร้าง Agent ใน Bedrock (เช่น ผ่าน Management Console) จากนั้นระบุ Agent ID ในหน้าจอการตั้งค่าแชทบอทที่กำหนดเอง เมื่อตั้งค่าแล้ว แชทบอทของคุณจะใช้ Bedrock Agent ในการประมวลผลคำถามของผู้ใช้

![](./imgs/bedrock_agent_tool.png)

## วิธีพัฒนาเครื่องมือของคุณเอง

การพัฒนาเครื่องมือที่กำหนดเองสำหรับ Agent โดยใช้ Strands SDK มีแนวทางดังนี้:

### เกี่ยวกับเครื่องมือ Strands

Strands มี decorator `@tool` อย่างง่ายที่แปลงฟังก์ชัน Python ปกติให้เป็นเครื่องมือของ AI agent decorator จะดึงข้อมูลจาก docstring และ type hints ของฟังก์ชันโดยอัตโนมัติเพื่อสร้างข้อกำหนดเครื่องมือที่ LLM สามารถเข้าใจและใช้งานได้ วิธีนี้ใช้ประโยชน์จากคุณสมบัติดั้งเดิมของ Python เพื่อประสบการณ์การพัฒนาเครื่องมือที่สะอาดและใช้งานได้จริง

สำหรับข้อมูลเพิ่มเติมเกี่ยวกับเครื่องมือ Strands โปรดดูที่ [เอกสารประกอบ Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)

### การสร้างเครื่องมือพื้นฐาน 

สร้างฟังก์ชันใหม่ที่ตกแต่งด้วย decorator `@tool` จาก Strands:

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

### เครื่องมือที่มี Bot Context (รูปแบบ Closure)

การเข้าถึงข้อมูลบอท (BotModel) ให้ใช้รูปแบบ closure ที่จับข้อมูล bot context:

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

### ข้อกำหนดรูปแบบการส่งคืน

เครื่องมือ Strands ทั้งหมดต้องส่งคืนพจนานุกรมที่มีโครงสร้างดังนี้:

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

- ใช้ `{"text": "message"}` สำหรับการตอบกลับข้อความธรรมดา
- ใช้ `{"json": data}` สำหรับข้อมูลที่ซับซ้อนที่ควรเก็บรักษาเป็นข้อมูลแบบมีโครงสร้าง  
- ตั้งค่า `status` เป็น `"success"` หรือ `"error"` เสมอ

### แนวทางการใช้งาน

- ชื่อฟังก์ชันและ docstring จะถูกใช้เมื่อ LLM พิจารณาว่าจะใช้เครื่องมือใด docstring จะถูกฝังอยู่ในพรอมต์ ดังนั้นควรอธิบายจุดประสงค์และพารามิเตอร์ของเครื่องมืออย่างแม่นยำ

- อ้างอิงตัวอย่างการใช้งานของ [เครื่องมือคำนวณ BMI](../examples/agents/tools/bmi/bmi_strands.py) ตัวอย่างนี้แสดงวิธีการสร้างเครื่องมือที่คำนวณดัชนีมวลกาย (BMI) โดยใช้ decorator `@tool` ของ Strands และรูปแบบ closure

- หลังจากพัฒนาเสร็จแล้ว ให้วางไฟล์การใช้งานของคุณไว้ในไดเร็กทอรี [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) จากนั้นเปิด [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) และแก้ไข `get_strands_registered_tools` เพื่อรวมเครื่องมือใหม่ของคุณ

- [ตัวเลือก] เพิ่มชื่อและคำอธิบายที่ชัดเจนสำหรับ frontend ขั้นตอนนี้เป็นตัวเลือก แต่ถ้าคุณไม่ทำขั้นตอนนี้ ระบบจะใช้ชื่อเครื่องมือและคำอธิบายจากฟังก์ชันของคุณ เนื่องจากสิ่งเหล่านี้ใช้สำหรับ LLM จึงแนะนำให้เพิ่มคำอธิบายที่เป็นมิตรกับผู้ใช้เพื่อ UX ที่ดีขึ้น

  - แก้ไขไฟล์ i18n เปิด [en/index.ts](../frontend/src/i18n/en/index.ts) และเพิ่ม `name` และ `description` ของคุณเองใน `agent.tools`
  - แก้ไข `xx/index.ts` ด้วย โดย `xx` แทนรหัสประเทศที่คุณต้องการ

- รัน `npx cdk deploy` เพื่อ deploy การเปลี่ยนแปลงของคุณ ซึ่งจะทำให้เครื่องมือที่กำหนดเองของคุณพร้อมใช้งานในหน้าจอบอทที่กำหนดเอง