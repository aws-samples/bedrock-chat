# คุณสมบัติด้านการจัดการระบบ

## ข้อกำหนดเบื้องต้น

ผู้ใช้ที่เป็นผู้ดูแลระบบจะต้องเป็นสมาชิกของกลุ่มที่ชื่อว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือผ่าน aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยการเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## ทำเครื่องหมายบอทสาธารณะเป็นบอทจำเป็น

ตอนนี้ผู้ดูแลระบบสามารถทำเครื่องหมายบอทสาธารณะเป็น "บอทจำเป็น" ได้ บอทที่ถูกทำเครื่องหมายว่าจำเป็นจะแสดงในส่วน "บอทจำเป็น" ของร้านค้าบอท ทำให้ผู้ใช้สามารถเข้าถึงได้ง่าย ช่วยให้ผู้ดูแลระบบสามารถปักหมุดบอทสำคัญที่ต้องการให้ผู้ใช้ทุกคนใช้งาน

### ตัวอย่าง

- บอทผู้ช่วย HR: ช่วยพนักงานเกี่ยวกับคำถามและงานด้าน HR
- บอทสนับสนุนด้าน IT: ให้ความช่วยเหลือเกี่ยวกับปัญหาทางเทคนิคภายในและการจัดการบัญชี
- บอทแนะนำนโยบายภายใน: ตอบคำถามที่พบบ่อยเกี่ยวกับกฎการเข้างาน นโยบายความปลอดภัย และระเบียบภายในอื่นๆ
- บอทปฐมนิเทศพนักงานใหม่: แนะนำพนักงานใหม่เกี่ยวกับขั้นตอนและการใช้ระบบในวันแรกของการทำงาน
- บอทข้อมูลสวัสดิการ: อธิบายเกี่ยวกับโปรแกรมสวัสดิการและบริการต่างๆ ของบริษัท

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## การวนรอบข้อมูลย้อนกลับ

ผลลัพธ์จาก LLM อาจไม่ตรงตามความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ การ "ผสานรวม" LLM เข้ากับการดำเนินธุรกิจและชีวิตประจำวันอย่างมีประสิทธิภาพนั้น จำเป็นต้องมีการนำระบบการวนรอบข้อมูลย้อนกลับมาใช้ Bedrock Chat มีฟีเจอร์การให้ข้อมูลย้อนกลับที่ออกแบบมาเพื่อให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พึงพอใจที่เกิดขึ้น จากผลการวิเคราะห์ ผู้ใช้สามารถปรับ prompts, แหล่งข้อมูล RAG และพารามิเตอร์ต่างๆ ได้ตามความเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาได้โดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้ [ตัวอย่าง notebook นี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแนวทางอ้างอิงได้

## แดชบอร์ด

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอทและผู้ใช้ โดยมุ่งเน้นการรวบรวมข้อมูลสำหรับบอทและผู้ใช้แต่ละรายในช่วงเวลาที่กำหนด และจัดเรียงผลลัพธ์ตามค่าธรรมเนียมการใช้งาน

![](./imgs/admin_bot_analytics.png)

## หมายเหตุ

- ตามที่ระบุไว้ใน [architecture](../README.md#architecture) ฟีเจอร์สำหรับผู้ดูแลระบบจะอ้างอิงถึง S3 bucket ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกจะทำทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏในทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่มีการใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงในรายการ

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงในรายการ

> [!Important]
> หากคุณใช้หลายสภาพแวดล้อม (dev, prod ฯลฯ) ชื่อฐานข้อมูล Athena จะรวมคำนำหน้าของสภาพแวดล้อม แทนที่จะเป็น `bedrockchatstack_usage_analysis` ชื่อฐานข้อมูลจะเป็น:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `bedrockchatstack_usage_analysis`
> - สำหรับสภาพแวดล้อมที่มีการตั้งชื่อ: `<env-prefix>_bedrockchatstack_usage_analysis` (เช่น `dev_bedrockchatstack_usage_analysis`)
>
> นอกจากนี้ ชื่อตารางจะรวมคำนำหน้าของสภาพแวดล้อมด้วย:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `ddb_export`
> - สำหรับสภาพแวดล้อมที่มีการตั้งชื่อ: `<env-prefix>_ddb_export` (เช่น `dev_ddb_export`)
>
> ตรวจสอบให้แน่ใจว่าได้ปรับแก้คิวรีของคุณให้เหมาะสมเมื่อทำงานกับหลายสภาพแวดล้อม

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถค้นหาข้อมูลการสนทนาได้ผ่าน Athena โดยใช้ SQL เพื่อดาวน์โหลดข้อมูล ให้เปิด Athena Query Editor จาก management console และรัน SQL ต่อไปนี้เป็นตัวอย่างคำสั่ง query ที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน สามารถดูข้อมูล Feedback ได้จากแอตทริบิวต์ `MessageMap`

### ค้นหาตาม Bot ID 

แก้ไข `bot-id` และ `datehour` โดย `bot-id` สามารถดูได้จากหน้าจอ Bot Management ซึ่งเข้าถึงได้จาก Bot Publish APIs ที่แสดงอยู่ในแถบด้านซ้าย สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> หากใช้สภาพแวดล้อมที่มีการตั้งชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคำสั่ง query ข้างต้น

### ค้นหาตาม User ID

แก้ไข `user-id` และ `datehour` โดย `user-id` สามารถดูได้จากหน้าจอ Bot Management

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้จะเปิดให้บริการเร็วๆ นี้

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> หากใช้สภาพแวดล้อมที่มีการตั้งชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคำสั่ง query ข้างต้น