# ตัวแทนที่ขับเคลื่อนด้วย LLM (ReAct)

## Agent (ReAct) คืออะไร?

Agent คือระบบ AI ขั้นสูงที่ใช้โมเดลภาษาขนาดใหญ่ (LLMs) เป็นเครื่องมือประมวลผลหลัก โดยผสมผสานความสามารถในการให้เหตุผลของ LLMs เข้ากับฟังก์ชันการทำงานเพิ่มเติมอื่นๆ เช่น การวางแผนและการใช้เครื่องมือ เพื่อทำงานที่ซับซ้อนได้โดยอัตโนมัติ Agents สามารถแยกแยะคำถามที่ซับซ้อน สร้างขั้นตอนการแก้ปัญหา และโต้ตอบกับเครื่องมือภายนอกหรือ API เพื่อรวบรวมข้อมูลหรือดำเนินงานย่อยต่างๆ

ตัวอย่างนี้ได้นำ Agent มาใช้โดยใช้แนวทาง [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) ReAct ช่วยให้ agent สามารถแก้ไขงานที่ซับซ้อนได้โดยการผสมผสานการให้เหตุผลและการกระทำในวงจรการตอบสนองแบบต่อเนื่อง agent จะดำเนินการผ่านขั้นตอนสำคัญสามขั้นตอนซ้ำๆ คือ การคิด การกระทำ และการสังเกต โดยจะวิเคราะห์สถานการณ์ปัจจุบันโดยใช้ LLM ตัดสินใจเลือกการกระทำถัดไป ดำเนินการโดยใช้เครื่องมือหรือ API ที่มีอยู่ และเรียนรู้จากผลลัพธ์ที่สังเกตได้ กระบวนการต่อเนื่องนี้ช่วยให้ agent สามารถปรับตัวเข้ากับสภาพแวดล้อมที่เปลี่ยนแปลง ปรับปรุงความแม่นยำในการแก้ปัญหา และให้คำตอบที่เหมาะสมกับบริบท

การนำไปใช้งานนี้ขับเคลื่อนด้วย [Strands Agents](https://strandsagents.com/) ซึ่งเป็น SDK แบบโอเพนซอร์สที่ใช้แนวทางที่ขับเคลื่อนด้วยโมเดลในการสร้าง AI agents Strands มอบเฟรมเวิร์กที่มีน้ำหนักเบาและยืดหยุ่นสำหรับการสร้างเครื่องมือที่กำหนดเองโดยใช้ Python decorators และรองรับผู้ให้บริการโมเดลหลายรายรวมถึง Amazon Bedrock

## ตัวอย่างการใช้งาน

Agent ที่ใช้ ReAct สามารถนำไปประยุกต์ใช้ในสถานการณ์ต่างๆ เพื่อให้ได้ผลลัพธ์ที่แม่นยำและมีประสิทธิภาพ

### การแปลงข้อความเป็น SQL

เมื่อผู้ใช้ต้องการทราบ "ยอดขายรวมในไตรมาสที่แล้ว" Agent จะตีความคำขอนี้ แปลงเป็นคำสั่ง SQL ดำเนินการค้นหาในฐานข้อมูล และแสดงผลลัพธ์

### การพยากรณ์ทางการเงิน

นักวิเคราะห์การเงินต้องการพยากรณ์รายได้ในไตรมาสถัดไป Agent จะรวบรวมข้อมูลที่เกี่ยวข้อง ทำการคำนวณที่จำเป็นโดยใช้โมเดลทางการเงิน และสร้างรายงานการพยากรณ์อย่างละเอียด พร้อมทั้งตรวจสอบความถูกต้องของการคาดการณ์

## วิธีใช้ฟีเจอร์ Agent

การเปิดใช้งานฟังก์ชัน Agent สำหรับแชทบอทที่คุณปรับแต่ง มีขั้นตอนดังนี้:

มีสองวิธีในการใช้ฟีเจอร์ Agent:

### การใช้ Tool Use

การเปิดใช้งานฟังก์ชัน Agent ด้วย Tool Use สำหรับแชทบอทที่คุณปรับแต่ง มีขั้นตอนดังนี้:

1. ไปที่ส่วน Agent ในหน้าจอการปรับแต่งบอท

2. ในส่วน Agent คุณจะพบรายการเครื่องมือที่ Agent สามารถใช้งานได้ โดยค่าเริ่มต้นเครื่องมือทั้งหมดจะถูกปิดใช้งาน

3. การเปิดใช้งานเครื่องมือ เพียงเปิดสวิตช์ที่อยู่ข้างเครื่องมือที่ต้องการ เมื่อเปิดใช้งานแล้ว Agent จะสามารถเข้าถึงและใช้งานเครื่องมือนั้นในการประมวลผลคำถามของผู้ใช้

![](./imgs/agent_tools.png)

4. ตัวอย่างเช่น เครื่องมือ "Internet Search" ช่วยให้ Agent สามารถค้นหาข้อมูลจากอินเทอร์เน็ตเพื่อตอบคำถามผู้ใช้

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. คุณสามารถพัฒนาและเพิ่มเครื่องมือที่กำหนดเองเพื่อขยายความสามารถของ Agent ดูข้อมูลเพิ่มเติมเกี่ยวกับการสร้างและผสานเครื่องมือที่กำหนดเองได้ในส่วน [How to develop your own tools](#how-to-develop-your-own-tools)

### การใช้ Bedrock Agent

คุณสามารถใช้ [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) ที่สร้างใน Amazon Bedrock

ขั้นแรก สร้าง Agent ใน Bedrock (เช่น ผ่าน Management Console) จากนั้นระบุ Agent ID ในหน้าการตั้งค่าแชทบอทที่ปรับแต่ง เมื่อตั้งค่าแล้ว แชทบอทของคุณจะใช้ Bedrock Agent ในการประมวลผลคำถามของผู้ใช้

![](./imgs/bedrock_agent_tool.png)

## วิธีพัฒนาเครื่องมือของคุณเอง

ในการพัฒนาเครื่องมือที่กำหนดเองสำหรับ Agent โดยใช้ Strands SDK ให้ทำตามแนวทางต่อไปนี้:

### เกี่ยวกับเครื่องมือ Strands

Strands มี decorator `@tool` อย่างง่ายที่แปลงฟังก์ชัน Python ปกติให้เป็นเครื่องมือสำหรับ AI agent decorator จะดึงข้อมูลจาก docstring และ type hints ของฟังก์ชันของคุณโดยอัตโนมัติเพื่อสร้างข้อกำหนดเครื่องมือที่ LLM สามารถเข้าใจและใช้งานได้ วิธีการนี้ใช้ประโยชน์จากคุณสมบัติดั้งเดิมของ Python เพื่อประสบการณ์การพัฒนาเครื่องมือที่สะอาดและใช้งานได้จริง

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

### เครื่องมือที่มีบริบทของบอท (รูปแบบ Closure)

ในการเข้าถึงข้อมูลบอท (BotModel) ให้ใช้รูปแบบ closure ที่จับบริบทของบอท:

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

- ใช้ `{"text": "message"}` สำหรับการตอบกลับข้อความอย่างง่าย
- ใช้ `{"json": data}` สำหรับข้อมูลที่ซับซ้อนที่ควรเก็บรักษาไว้เป็นข้อมูลแบบมีโครงสร้าง
- ตั้งค่า `status` เป็น `"success"` หรือ `"error"` เสมอ

### แนวทางการใช้งาน

- ชื่อฟังก์ชันและ docstring จะถูกใช้เมื่อ LLM พิจารณาว่าจะใช้เครื่องมือใด docstring จะถูกฝังอยู่ในพรอมต์ ดังนั้นให้อธิบายจุดประสงค์และพารามิเตอร์ของเครื่องมืออย่างแม่นยำ

- อ้างอิงตัวอย่างการใช้งานของ [เครื่องมือคำนวณ BMI](../examples/agents/tools/bmi/bmi_strands.py) ตัวอย่างนี้แสดงวิธีการสร้างเครื่องมือที่คำนวณดัชนีมวลกาย (BMI) โดยใช้ decorator `@tool` ของ Strands และรูปแบบ closure

- หลังจากพัฒนาเสร็จแล้ว ให้วางไฟล์การใช้งานของคุณไว้ในไดเรกทอรี [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) จากนั้นเปิด [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) และแก้ไข `get_strands_registered_tools` เพื่อรวมเครื่องมือใหม่ของคุณ

- [ตัวเลือก] เพิ่มชื่อและคำอธิบายที่ชัดเจนสำหรับส่วนหน้า ขั้นตอนนี้เป็นตัวเลือก แต่ถ้าคุณไม่ทำขั้นตอนนี้ ระบบจะใช้ชื่อเครื่องมือและคำอธิบายจากฟังก์ชันของคุณ เนื่องจากสิ่งเหล่านี้ใช้สำหรับการบริโภค LLM จึงแนะนำให้เพิ่มคำอธิบายที่เป็นมิตรกับผู้ใช้เพื่อ UX ที่ดีขึ้น

  - แก้ไขไฟล์ i18n เปิด [en/index.ts](../frontend/src/i18n/en/index.ts) และเพิ่ม `name` และ `description` ของคุณเองใน `agent.tools`
  - แก้ไข `xx/index.ts` เช่นกัน โดย `xx` แทนรหัสประเทศที่คุณต้องการ

- รัน `npx cdk deploy` เพื่อ deploy การเปลี่ยนแปลงของคุณ ซึ่งจะทำให้เครื่องมือที่กำหนดเองของคุณพร้อมใช้งานในหน้าจอบอทที่กำหนดเอง