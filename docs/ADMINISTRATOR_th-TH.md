# คุณสมบัติการดูแลระบบ

## ข้อกำหนดเบื้องต้น

ผู้ใช้งานผู้ดูแลระบบจะต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## ทำเครื่องหมายบอทสาธารณะเป็นแบบ Essential

ตอนนี้ผู้ดูแลระบบสามารถทำเครื่องหมายบอทสาธารณะเป็น "Essential" ได้ บอทที่ทำเครื่องหมายเป็น Essential จะถูกนำเสนอในส่วน "Essential" ของร้านค้าบอท ทำให้ผู้ใช้สามารถเข้าถึงได้อย่างง่ายดาย ซึ่งช่วยให้ผู้ดูแลระบบสามารถปักหมุดบอทที่สำคัญที่ต้องการให้ผู้ใช้ทุกคนใช้งาน

### ตัวอย่าง

- บอทช่วยเหลือฝ่ายทรัพยากรบุคคล: ช่วยเหลือพนักงานเกี่ยวกับคำถามและงานที่เกี่ยวข้องกับ HR
- บอทสนับสนุนไอที: ให้ความช่วยเหลือปัญหาทางเทคนิคภายในและการจัดการบัญชี
- บอทคู่มือนโยบายภายใน: ตอบคำถามที่พบบ่อยเกี่ยวกับกฎการลงเวลา นโยบายความปลอดภัย และระเบียบภายในอื่นๆ
- บอทปฐมนิเทศพนักงานใหม่: แนะนำพนักงานใหม่ผ่านขั้นตอนและการใช้งานระบบในวันแรก
- บอทข้อมูลสวัสดิการ: อธิบายโปรแกรมสวัสดิการและบริการสวัสดิการของบริษัท

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## วงจรป้อนกลับ

ผลลัพธ์จาก LLM อาจไม่ตรงตามความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ เพื่อ "บูรณาการ" LLMs เข้ากับการดำเนินงานทางธุรกิจและชีวิตประจำวันอย่างมีประสิทธิภาพ การใช้วงจรป้อนกลับถือเป็นสิ่งสำคัญ Bedrock Chat มีคุณสมบัติการให้ข้อเสนอแนะที่ออกแบบมาเพื่อช่วยให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พอใจได้ ขึ้นอยู่กับผลการวิเคราะห์ ผู้ใช้สามารถปรับแต่งพรอมpt แหล่งข้อมูล RAG และพารามิเตอร์ต่างๆ ได้อย่างเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาได้โดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้[ตัวอย่างสมุดบันทึกนี้](../examples/notebooks/feedback_analysis_example.ipynb)เป็นแหล่งอ้างอิงได้

## แดชบอร์ด

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอตและผู้ใช้ โดยมุ่งเน้นไปที่การรวบรวมข้อมูลสำหรับแต่ละบอตและผู้ใช้ในช่วงเวลาที่กำหนด และจัดเรียงผลลัพธ์ตามค่าใช้จ่ายในการใช้งาน

![](./imgs/admin_bot_analytics.png)

## หมายเหตุ

- ตามที่ระบุไว้ใน[สถาปัตยกรรม](../README.md#architecture) คุณสมบัติการดูแลระบบจะอ้างอิงไปยังบัคเก็ต S3 ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกจะดำเนินการทุกๆ 1 ชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่ได้ใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดง

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดง

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
> ตรวจสอบให้แน่ใจว่าคุณปรับแก้คิวรีให้เหมาะสมเมื่อทำงานกับสภาพแวดล้อมหลายแบบ

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถค้นหาบันทึกการสนทนาโดย Athena โดยใช้ SQL เพื่อดาวน์โหลดบันทึก ให้เปิด Athena Query Editor จากคอนโซลการจัดการและเรียกใช้ SQL ต่อไปนี้เป็นตัวอย่างการสอบถามที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน สามารถอ้างอิงข้อเสนอแนะได้ในแอตทริบิวต์ `MessageMap`

### สอบถามตาม Bot ID

แก้ไข `bot-id` และ `datehour` `bot-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot ซึ่งสามารถเข้าถึงได้จาก Bot Publish APIs แสดงที่แถบด้านข้าย สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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

### สอบถามตาม User ID

แก้ไข `user-id` และ `datehour` `user-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot

> [!หมายเหตุ]
> การวิเคราะห์การใช้งานของผู้ใช้กำลังจะมาถึง

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