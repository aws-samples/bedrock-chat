# คุณสมบัติของผู้ดูแลระบบ

คุณสมบัติของผู้ดูแลระบบถือเป็นเครื่องมือที่สำคัญยิ่ง เนื่องจากให้ข้อมูลเชิงลึกที่จำเป็นเกี่ยวกับการใช้งานบอทที่กำหนดเองและพฤติกรรมของผู้ใช้ หากขาดฟังก์ชันนี้ ผู้ดูแลระบบจะประสบความยากลำบากในการทำความเข้าใจว่าบอทที่กำหนดเองใดเป็นที่นิยม เหตุใดจึงเป็นที่นิยม และใครคือผู้ใช้งาน ข้อมูลนี้มีความสำคัญอย่างยิ่งสำหรับการปรับปรุงคำแนะนำ การปรับแต่งแหล่งข้อมูล RAG และการระบุผู้ใช้หนักที่อาจกลายเป็นผู้มีอิทธิพล

## วงรอบผลตอบรับ

เอาต์พุตจาก LLM อาจไม่เป็นไปตามความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจล้มเหลวในการตอบสนองความต้องการของผู้ใช้ เพื่อ "บูรณาการ" LLMs เข้ากับการดำเนินงานทางธุรกิจและชีวิตประจำวันอย่างมีประสิทธิภาพ การใช้วงรอบผลตอบรับเป็นสิ่งสำคัญ Bedrock Claude Chat มีคุณสมบัติการให้ผลตอบรับที่ออกแบบมาเพื่อช่วยให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พอใจได้ ขึ้นอยู่กับผลการวิเคราะห์ ผู้ใช้สามารถปรับแต่งพรอมต์ แหล่งข้อมูล RAG และพารามิเตอร์ต่าง ๆ ได้อย่างเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาโดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้[ตัวอย่างสมุดบันทึกนี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแหล่งอ้างอิงได้

## แดชบอร์ดผู้ดูแลระบบ

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอตและผู้ใช้ โดยมุ่งเน้นการรวบรวมข้อมูลสำหรับแต่ละบอตและผู้ใช้ในช่วงเวลาที่กำหนด และเรียงลำดับผลลัพธ์ตามค่าใช้จ่ายการใช้งาน

![](./imgs/admin_bot_analytics.png)

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้จะมาถึงเร็วๆ นี้

### ข้อกำหนดเบื้องต้น

ผู้ใช้งานแอดมินต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าไอดีกลุ่มผู้ใช้สามารถอ้างอิงได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## บันทึกย่อ

- ตามที่ระบุไว้ใน [สถาปัตยกรรม](../README.md#architecture) คุณสมบัติผู้ดูแลระบบจะอ้างอิงไปยัง S3 bucket ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกทำการทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่ได้ใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดง

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดง

> [!สำคัญ] > **ชื่อฐานข้อมูลหลายสภาพแวดล้อม**
>
> หากคุณใช้หลายสภาพแวดล้อม (dev, prod เป็นต้น) ชื่อฐานข้อมูล Athena จะรวมคำนำหน้าสภาพแวดล้อม แทนที่จะเป็น `bedrockchatstack_usage_analysis` ชื่อฐานข้อมูลจะเป็น:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `bedrockchatstack_usage_analysis`
> - สำหรับสภาพแวดล้อมที่มีชื่อ: `<คำนำหน้าสภาพแวดล้อม>_bedrockchatstack_usage_analysis` (เช่น `dev_bedrockchatstack_usage_analysis`)
>
> นอกจากนี้ ชื่อตารางจะรวมคำนำหน้าสภาพแวดล้อม:
>
> - สำหรับสภาพแวดล้อมเริ่มต้น: `ddb_export`
> - สำหรับสภาพแวดล้อมที่มีชื่อ: `<คำนำหน้าสภาพแวดล้อม>_ddb_export` (เช่น `dev_ddb_export`)
>
> ตรวจสอบให้แน่ใจว่าคุณปรับแก้การสอบถามให้เหมาะสมเมื่อทำงานกับหลายสภาพแวดล้อม

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถค้นหาบันทึกการสนทนาด้วย Athena โดยใช้ SQL เพื่อดาวน์โหลดบันทึก ให้เปิด Athena Query Editor จากคอนโซลการจัดการและรันคำสั่ง SQL ต่อไปนี้เป็นตัวอย่างคิวรีที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน สามารถอ้างอิงข้อเสนอแนะได้ในแอตทริบิวต์ `MessageMap`

### คิวรีตาม Bot ID

แก้ไข `bot-id` และ `datehour` `bot-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot ซึ่งสามารถเข้าถึงได้จาก Bot Publish APIs ที่แสดงบนแถบด้านข้าง สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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
> หากใช้สภาพแวดล้อมที่มีชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคิวรีด้านบน

### คิวรีตาม User ID

แก้ไข `user-id` และ `datehour` `user-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้จะมีให้เร็วๆ นี้

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
> หากใช้สภาพแวดล้อมที่มีชื่อ (เช่น "dev") ให้แทนที่ `bedrockchatstack_usage_analysis.ddb_export` ด้วย `dev_bedrockchatstack_usage_analysis.dev_ddb_export` ในคิวรีด้านบน