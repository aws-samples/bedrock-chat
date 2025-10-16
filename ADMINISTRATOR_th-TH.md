# คุณสมบัติด้านการจัดการระบบ

## ข้อกำหนดเบื้องต้น

ผู้ใช้งานที่เป็นผู้ดูแลระบบจะต้องเป็นสมาชิกของกลุ่มที่ชื่อว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือผ่าน aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยการเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## ทำเครื่องหมายบอทสาธารณะเป็นบอทจำเป็น

ตอนนี้ผู้ดูแลระบบสามารถทำเครื่องหมายบอทสาธารณะเป็น "บอทจำเป็น" ได้ บอทที่ถูกทำเครื่องหมายว่าจำเป็นจะแสดงในส่วน "บอทจำเป็น" ของร้านค้าบอท ทำให้ผู้ใช้เข้าถึงได้ง่าย วิธีนี้ช่วยให้ผู้ดูแลระบบสามารถปักหมุดบอทสำคัญที่ต้องการให้ผู้ใช้ทุกคนใช้งาน

### ตัวอย่าง

- บอทผู้ช่วย HR: ช่วยพนักงานเกี่ยวกับคำถามและงานด้าน HR
- บอทสนับสนุนด้าน IT: ให้ความช่วยเหลือเกี่ยวกับปัญหาทางเทคนิคภายในและการจัดการบัญชี
- บอทแนะนำนโยบายภายใน: ตอบคำถามที่พบบ่อยเกี่ยวกับกฎการเข้างาน นโยบายความปลอดภัย และระเบียบภายในอื่นๆ
- บอทปฐมนิเทศพนักงานใหม่: แนะนำพนักงานใหม่เกี่ยวกับขั้นตอนและการใช้ระบบในวันแรกของการทำงาน
- บอทข้อมูลสวัสดิการ: อธิบายโปรแกรมสวัสดิการบริษัทและบริการด้านสวัสดิการ

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## การวนรอบย้อนกลับ

ผลลัพธ์จาก LLM อาจไม่ตรงกับความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ เพื่อให้สามารถ "บูรณาการ" LLM เข้ากับการดำเนินธุรกิจและชีวิตประจำวันได้อย่างมีประสิทธิภาพ การนำระบบการวนรอบย้อนกลับมาใช้จึงเป็นสิ่งจำเป็น Bedrock Chat มีฟีเจอร์การให้ข้อมูลย้อนกลับที่ออกแบบมาเพื่อให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พึงพอใจที่เกิดขึ้น จากผลการวิเคราะห์ ผู้ใช้สามารถปรับ prompts แหล่งข้อมูล RAG และพารามิเตอร์ต่างๆ ได้ตามความเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาได้โดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้ [ตัวอย่าง notebook นี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแนวทางอ้างอิงได้

## แดชบอร์ด

ปัจจุบันแสดงภาพรวมพื้นฐานของการใช้งานแชทบอทและผู้ใช้ โดยมุ่งเน้นการรวบรวมข้อมูลสำหรับบอทและผู้ใช้แต่ละรายในช่วงเวลาที่กำหนด และจัดเรียงผลลัพธ์ตามค่าธรรมเนียมการใช้งาน

![](./imgs/admin_bot_analytics.png)

## หมายเหตุ

- ตามที่ระบุไว้ใน [architecture](../README.md#architecture) ฟีเจอร์สำหรับผู้ดูแลระบบจะอ้างอิงถึง S3 bucket ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกจะดำเนินการทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏในทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่มีการใช้งานเลยในช่วงเวลาที่ระบุจะไม่แสดงในรายการ

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่แสดงในรายการ

> [!Important]
> หากคุณใช้หลายสภาพแวดล้อม (dev, prod ฯลฯ) ชื่อฐานข้อมูล Athena จะรวมคำนำหน้าสภาพแวดล้อม แทนที่จะเป็น `bedrockchatstack_usage_analysis` ชื่อฐานข้อมูลจะเป็น:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `bedrockchatstack_usage_analysis`
> - สำหรับสภาพแวดล้อมที่ตั้งชื่อ: `<env-prefix>_bedrockchatstack_usage_analysis` (เช่น `dev_bedrockchatstack_usage_analysis`)
>
> นอกจากนี้ ชื่อตารางจะรวมคำนำหน้าสภาพแวดล้อมด้วย:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `ddb_export`
> - สำหรับสภาพแวดล้อมที่ตั้งชื่อ: `<env-prefix>_ddb_export` (เช่น `dev_ddb_export`)
>
> ตรวจสอบให้แน่ใจว่าได้ปรับแก้คิวรีของคุณตามความเหมาะสมเมื่อทำงานกับหลายสภาพแวดล้อม

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถค้นหาบันทึกการสนทนาได้โดยใช้ Athena ด้วย SQL เพื่อดาวน์โหลดบันทึก ให้เปิด Athena Query Editor จาก management console และรัน SQL ต่อไปนี้เป็นตัวอย่างคำสั่ง query ที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน สามารถดูข้อเสนอแนะได้ในแอตทริบิวต์ `MessageMap`

### ค้นหาตาม Bot ID

แก้ไข `bot-id` และ `datehour` โดยสามารถดู `bot-id` ได้จากหน้าจอ Bot Management ซึ่งเข้าถึงได้จาก Bot Publish APIs ที่แสดงอยู่ในแถบด้านซ้าย สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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

แก้ไข `user-id` และ `datehour` โดยสามารถดู `user-id` ได้จากหน้าจอ Bot Management

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้จะเปิดให้ใช้งานเร็วๆ นี้

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