# คุณสมบัติการดูแลระบบ

## ข้อกำหนดเบื้องต้น

ผู้ใช้ระดับผู้ดูแลระบบต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## ทำเครื่องหมายบอทสาธารณะเป็นแบบ Essential

ตอนนี้ผู้ดูแลระบบสามารถทำเครื่องหมายบอทสาธารณะเป็น "Essential" ได้ บอทที่ทำเครื่องหมายเป็น Essential จะถูกแสดงในส่วน "Essential" ของร้านบอท ทำให้ผู้ใช้สามารถเข้าถึงได้อย่างง่ายดาย ซึ่งช่วยให้ผู้ดูแลระบบสามารถปักหมุดบอทที่สำคัญที่ต้องการให้ผู้ใช้ทุกคนใช้งาน

### ตัวอย่าง

- บอทช่วยเหลือฝ่ายทรัพยากรบุคคล: ช่วยเหลือพนักงานเกี่ยวกับคำถามและงานที่เกี่ยวข้องกับ HR
- บอทสนับสนุนไอที: ให้ความช่วยเหลือปัญหาทางเทคนิคภายในและการจัดการบัญชี
- บอทคู่มือนโยบายภายใน: ตอบคำถามทั่วไปเกี่ยวกับกฎการลงเวลา นโยบายความปลอดภัย และระเบียบภายในอื่นๆ
- บอทปฐมนิเทศพนักงานใหม่: แนะนำพนักงานใหม่เกี่ยวกับขั้นตอนและการใช้งานระบบในวันแรก
- บอทข้อมูลสวัสดิการ: อธิบายโครงการสวัสดิการและบริการสวัสดิการของบริษัท

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## วงรอบผลตอบรับ

เอาต์พุตจาก LLM อาจไม่ตรงกับความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ เพื่อให้สามารถ "บูรณาการ" LLM เข้ากับการดำเนินงานทางธุรกิจและชีวิตประจำวันได้อย่างมีประสิทธิภาพ การใช้วงรอบผลตอบรับถือเป็นสิ่งสำคัญ Bedrock Chat มีคุณสมบัติการให้ผลตอบรับที่ออกแบบมาเพื่อช่วยให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พึงพอใจ ขึ้นอยู่กับผลการวิเคราะห์ ผู้ใช้สามารถปรับแต่งพรอมต์ แหล่งข้อมูล RAG และพารามิเตอร์ต่าง ๆ ได้ตามความเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาโดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้[ตัวอย่างสมุดบันทึกนี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแนวอ้างอิงได้

## แดชบอร์ด

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอทและผู้ใช้ โดยมุ่งเน้นการรวบรวมข้อมูลสำหรับแต่ละบอทและผู้ใช้ในช่วงเวลาที่กำหนด และจัดเรียงผลลัพธ์ตามค่าใช้จ่ายในการใช้งาน

![](./imgs/admin_bot_analytics.png)

## หมายเหตุ

- ตามที่ระบุใน[สถาปัตยกรรม](../README.md#architecture) คุณสมบัติของผู้ดูแลระบบจะอ้างอิงถึงบัคเก็ต S3 ที่ส่งออกจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกทำการทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่ได้ใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

> [!สำคัญ]
> หากคุณใช้สภาพแวดล้อมหลายแบบ (dev, prod เป็นต้น) ชื่อฐานข้อมูล Athena จะรวมคำนำหน้าสภาพแวดล้อม แทนที่จะเป็น `bedrockchatstack_usage_analysis` ชื่อฐานข้อมูลจะเป็น:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `bedrockchatstack_usage_analysis`
> - สำหรับสภาพแวดล้อมที่มีชื่อ: `<คำนำหน้าสภาพแวดล้อม>_bedrockchatstack_usage_analysis` (เช่น `dev_bedrockchatstack_usage_analysis`)
>
> นอกจากนี้ ชื่อตารางจะรวมคำนำหน้าสภาพแวดล้อม:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `ddb_export`
> - สำหรับสภาพแวดล้อมที่มีชื่อ: `<คำนำหน้าสภาพแวดล้อม>_ddb_export` (เช่น `dev_ddb_export`)
>
> ตรวจสอบให้แน่ใจว่าคุณปรับแต่งการสอบถามให้เหมาะสมเมื่อทำงานกับสภาพแวดล้อมหลายแบบ

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถสืบค้นบันทึกการสนทนาด้วย Athena โดยใช้ SQL เพื่อดาวน์โหลดบันทึก ให้เปิด Athena Query Editor จากคอนโซลการจัดการและรันคำสั่ง SQL ต่อไปนี้เป็นตัวอย่างคิวรีที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน ข้อเสนอแนะสามารถอ้างอิงได้จากแอตทริบิวต์ `MessageMap`

### คิวรีตาม Bot ID

แก้ไข `bot-id` และ `datehour` `bot-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot ซึ่งสามารถเข้าถึงได้จาก Bot Publish APIs แสดงอยู่ที่แถบด้านซ้าย สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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

> [!หมายเหตุ]
> หากใช้สภาพแวดล้อมที่มีชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคิวรีด้านบน

### คิวรีตาม User ID

แก้ไข `user-id` และ `datehour` `user-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot

> [!หมายเหตุ]
> การวิเคราะห์การใช้งานของผู้ใช้กำลังจะมี

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

> [!หมายเหตุ]
> หากใช้สภาพแวดล้อมที่มีชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคิวรีด้านบน