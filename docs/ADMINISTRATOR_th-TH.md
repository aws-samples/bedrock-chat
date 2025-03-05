# คุณลักษณะของผู้ดูแลระบบ

คุณลักษณะของผู้ดูแลระบบเป็นเครื่องมือที่สำคัญยิ่ง เนื่องจากให้ข้อมูลเชิงลึกที่จำเป็นเกี่ยวกับการใช้งานบอทที่กำหนดเองและพฤติกรรมของผู้ใช้ หากไม่มีฟังก์ชันนี้ ผู้ดูแลระบบจะประสบความยากลำบากในการทำความเข้าใจว่าบอทที่กำหนดเองตัวใดเป็นที่นิยม เหตุใดจึงเป็นที่นิยม และใครเป็นผู้ใช้งาน ข้อมูลนี้มีความสำคัญอย่างยิ่งสำหรับการปรับปรุงคำแนะนำ การปรับแต่งแหล่งข้อมูล RAG และการระบุผู้ใช้หนักที่อาจจะกลายเป็นผู้มีอิทธิพล

## วงจรป้อนกลับ

เอาต์พุตจาก LLM อาจไม่ตรงตามความคาดหวังของผู้ใช้เสมอไป บางครั้งอาจไม่สามารถตอบสนองความต้องการของผู้ใช้ได้ เพื่อให้สามารถ "บูรณาการ" LLMs เข้ากับการดำเนินงานทางธุรกิจและชีวิตประจำวันอย่างมีประสิทธิภาพ การใช้วงจรป้อนกลับถือเป็นสิ่งสำคัญ Bedrock Claude Chat มีคุณสมบัติการให้ข้อเสนอแนะที่ออกแบบมาเพื่อช่วยให้ผู้ใช้สามารถวิเคราะห์สาเหตุของความไม่พอใจได้ ขึ้นอยู่กับผลการวิเคราะห์ ผู้ใช้สามารถปรับแต่งพรอมต์ แหล่งข้อมูล RAG และพารามิเตอร์ต่าง ๆ ได้ตามความเหมาะสม

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

นักวิเคราะห์ข้อมูลสามารถเข้าถึงบันทึกการสนทนาได้โดยใช้ [Amazon Athena](https://aws.amazon.com/jp/athena/) หากต้องการวิเคราะห์ข้อมูลด้วย [Jupyter Notebook](https://jupyter.org/) สามารถใช้[ตัวอย่างสมุดบันทึกนี้](../examples/notebooks/feedback_analysis_example.ipynb) เป็นแนวทางอ้างอิงได้

## แดชบอร์ดผู้ดูแลระบบ

ปัจจุบันให้ภาพรวมพื้นฐานของการใช้งานแชทบอทและผู้ใช้ โดยมุ่งเน้นไปที่การรวบรวมข้อมูลสำหรับแต่ละบอทและผู้ใช้ในช่วงเวลาที่กำหนด และเรียงลำดับผลลัพธ์ตามค่าใช้จ่ายการใช้งาน

![](./imgs/admin_bot_analytics.png)

> [!หมายเหตุ]
> การวิเคราะห์การใช้งานของผู้ใช้กำลังจะมาถึงเร็วๆ นี้

### ข้อกำหนดเบื้องต้น

ผู้ใช้ที่เป็นผู้ดูแลระบบต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `Admin` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าสามารถอ้างอิง ID ของกลุ่มผู้ใช้ได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_admin.png)

## บันทึกหมายเหตุ

- ตามที่ระบุไว้ใน[สถาปัตยกรรม](../README.md#architecture) คุณสมบัติของผู้ดูแลระบบจะอ้างอิงถึงบัคเก็ต S3 ที่ส่งออกมาจาก DynamoDB โปรดทราบว่าเนื่องจากการส่งออกทำการทุกๆ หนึ่งชั่วโมง การสนทนาล่าสุดอาจไม่ปรากฏทันที

- ในการใช้งานบอทสาธารณะ บอทที่ไม่ได้ถูกใช้งานเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

- ในการใช้งานของผู้ใช้ ผู้ใช้ที่ไม่ได้ใช้ระบบเลยในช่วงเวลาที่ระบุจะไม่ถูกแสดงรายการ

## ดาวน์โหลดข้อมูลการสนทนา

คcanุาร้นquery บันทึกการสนทนาผ่าน Athena โดยใช้ากต้องดาว์น์โหลดบันทึก ใหอเปิดตัวแก้ไข Athena Query จากคอนโซลการจัดการและรันี่่ป่อไเป็นตัวอยอยา่งเชมีประโนชยชการวคราะห์กรณีใใใน ###ข้อมูลfeedbackสามารถ้มารถได จากแอตทริบิวต์ `Message`Map

มรหัสBotท



แไ`` และลา `datehour eh` `bot-id botสามารถอรดูไดบ้จหน้าจอการจ้Bot Management screen ซึข้าสามถได้จาก Bot Publish APIs แสดงบ้อยู่ด้้ านซ้าย สสังเกตส่วน้วนท้ายของของู URL เช่น `https://xxxx.cloudfront.net/admin/bot/<bot-id>`

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

### QueryตามมUser ID

แ้ไ`userขผูช้ ้ใช้` และ`datehourhour ่ โดย `user-ู-id` สามารถอดูได้จอหน้าManagement้อการBot

> [!Note]
> การวิเคราะห์การใานช้งานของผู้ใช้จะมาถึงเร็วๆ นี้

sql
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