# คุณสมบัติของผู้ดูแลระบบ

คุณสมบัติของผู้ดูแลระบบเป็นเครื่องมือที่สำคัญยิ่ง เนื่องจากให้ข้อมูลเชิงลึกที่จำเป็นเกี่ยวกับการใช้งานบอทที่กำหนดเองและพฤติกรรมของผู้ใช้ หากขาดฟังก์ชันนี้ ผู้ดูแลระบบจะประสบความยากลำบากในการทำความเข้าใจว่าบอทที่กำหนดเองใดเป็นที่นิยม เหตุใดจึงเป็นที่นิยม และใครเป็นผู้ใช้งาน ข้อมูลเหล่านี้มีความสำคัญอย่างยิ่งสำหรับการปรับปรุงคำแนะนำ การปรับแต่งแหล่งข้อมูล RAG และการระบุผู้ใช้งานหนัก ซึ่งอาจกลายเป็นผู้มีอิทธิพลในอนาคต

## วงจรป้อนกลับ

เอาต์พุตจาก LLM อาจไม่เป็นไปตามความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ เพื่อการ "บูรณาการ" LLM เข้ากับการดำเนินงานทางธุรกิจและชีวิตประจำวันอย่างมีประสิทธิภาพ การใช้วงจรป้อนกลับถือเป็นสิ่งสำคัญ Bedrock Claude Chat มีคุณสมบัติการให้ข้อเสนอแนะที่ออกแบบมาเพื่อช่วยให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พึงพอใจได้ ขึ้นอยู่กับผลการวิเคราะห์ ผู้ใช้สามารถปรับแต่งพรอมต์ แหล่งข้อมูล RAG และพารามิเตอร์ต่าง ๆ ได้อย่างเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาโดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้[ตัวอย่างสมุดบันทึกนี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแนวอ้างอิงได้

## แดชบอร์ดผู้ดูแลระบบ

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอทและผู้ใช้ โดยมุ่งเน้นการรวบรวมข้อมูลสำหรับแต่ละบอทและผู้ใช้ในช่วงเวลาที่ระบุ และเรียงลำดับผลลัพธ์ตามค่าใช้จ่ายการใช้งาน

![](./imgs/admin_bot_analytics.png)

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้จะมาถึงเร็วๆ นี้

### ข้อกำหนดเบื้องต้น

ผู้ใช้ที่เป็นผู้ดูแลระบบต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## หมายเหตุ

- ตามที่ระบุไว้ใน[สถาปัตยกรรม](../README.md#architecture) คุณลักษณะผู้ดูแลระบบจะอ้างอิงไปยังบัคเก็ต S3 ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกดำเนินการทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏขึ้นทันที

- ในการใช้งานบอร์ตสาธารณะ บอตที่ไม่ได้ถูกใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

## ดาวน์โหลดข้อมูลการสนทนา

คุณสามารถสอบถามบันทึกการสนทนาโดยใช้ Athena ด้วย SQL เพื่อดาวน์โหลดบันทึก ให้เปิด Athena Query Editor จากคอนโซลการจัดการและรันคำสั่ง SQL ต่อไปนี้เป็นตัวอย่างการสอบถามที่มีประโยชน์ในการวิเคราะห์กรณีการใช้งาน สามารถอ้างอิงข้อเสนอแนะได้ในแอตทริบิวต์ `MessageMap`

### คิวรีตาม Bot ID

แก้ไข `bot-id` และ `datehour` `bot-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot ซึ่งสามารถเข้าถึงได้จาก Bot Publish APIs ที่แสดงบนแถบด้านซ้าย สังเกตส่วนท้ายของ URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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

### คิวรีตาม User ID

แก้ไข `user-id` และ `datehour` `user-id` สามารถอ้างอิงได้จากหน้าจัดการ Bot

> [!Note]
> การวิเคราะห์การใช้งานของผู้ใช้กำลังจะมีเร็วๆ นี้

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