# การเผยแพร่ API

## ภาพรวม

ตัวอย่างนี้มีฟีเจอร์สำหรับการเผยแพร่ API ในขณะที่อินเทอร์เฟซแชทอาจสะดวกสำหรับการตรวจสอบความถูกต้องเบื้องต้น การนำไปใช้งานจริงขึ้นอยู่กับกรณีการใช้งานเฉพาะและประสบการณ์ผู้ใช้ (UX) ที่ต้องการสำหรับผู้ใช้ปลายทาง ในบางสถานการณ์ ส่วนติดต่อผู้ใช้แบบแชทอาจเป็นตัวเลือกที่เหมาะสม ในขณะที่บางกรณี API แบบสแตนด์อโลนอาจเหมาะสมกว่า หลังจากการตรวจสอบความถูกต้องเบื้องต้น ตัวอย่างนี้มีความสามารถในการเผยแพร่บอทที่ปรับแต่งได้ตามความต้องการของโครงการ โดยการป้อนการตั้งค่าสำหรับโควต้า การควบคุมการเรียกใช้งาน แหล่งที่มา ฯลฯ สามารถเผยแพร่ endpoint พร้อมกับ API key ซึ่งมอบความยืดหยุ่นสำหรับตัวเลือกการผสานรวมที่หลากหลาย

## ความปลอดภัย

การใช้เพียง API key อย่างเดียวนั้นไม่แนะนำตามที่อธิบายไว้ใน: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html) ด้วยเหตุนี้ ตัวอย่างนี้จึงใช้การจำกัด IP address อย่างง่ายผ่าน AWS WAF การกำหนดกฎ WAF นี้ถูกนำไปใช้ร่วมกันทั่วทั้งแอปพลิเคชันเนื่องจากข้อพิจารณาด้านต้นทุน โดยตั้งสมมติฐานว่าแหล่งที่มาที่คุณต้องการจำกัดนั้นมักจะเหมือนกันในทุก API ที่เปิดให้บริการ **กรุณาปฏิบัติตามนโยบายความปลอดภัยขององค์กรของคุณสำหรับการนำไปใช้งานจริง** และดูเพิ่มเติมที่ส่วน [Architecture](#architecture)

## วิธีเผยแพร่ API บอทที่ปรับแต่ง

### ข้อกำหนดเบื้องต้น

เพื่อเหตุผลด้านการกำกับดูแล มีเพียงผู้ใช้จำกัดเท่านั้นที่สามารถเผยแพร่บอทได้ ก่อนการเผยแพร่ ผู้ใช้ต้องเป็นสมาชิกของกลุ่มที่เรียกว่า `PublishAllowed` ซึ่งสามารถตั้งค่าได้ผ่าน management console > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าสามารถอ้างอิง user pool id ได้โดยการเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

![](./imgs/group_membership_publish_allowed.png)

### การตั้งค่าการเผยแพร่ API

หลังจากเข้าสู่ระบบในฐานะผู้ใช้ `PublishedAllowed` และสร้างบอทแล้ว ให้เลือก `API PublishSettings` โปรดทราบว่าเฉพาะบอทที่แชร์เท่านั้นที่สามารถเผยแพร่ได้
![](./imgs/bot_api_publish_screenshot.png)

ในหน้าจอต่อไปนี้ เราสามารถกำหนดค่าพารามิเตอร์หลายตัวเกี่ยวกับการควบคุมการส่งคำขอ สำหรับรายละเอียดเพิ่มเติม โปรดดูที่: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
![](./imgs/bot_api_publish_screenshot2.png)

หลังจากการเผยแพร่ จะปรากฏหน้าจอต่อไปนี้ซึ่งคุณสามารถรับ URL ปลายทางและคีย์ API นอกจากนี้เรายังสามารถเพิ่มและลบคีย์ API ได้

![](./imgs/bot_api_publish_screenshot3.png)

## สถาปัตยกรรม

API ถูกเผยแพร่ตามแผนผังต่อไปนี้:

![](./imgs/published_arch.png)

WAF ถูกใช้สำหรับการจำกัด IP address โดยสามารถกำหนดค่า address ได้โดยการตั้งค่าพารามิเตอร์ `publishedApiAllowedIpV4AddressRanges` และ `publishedApiAllowedIpV6AddressRanges` ใน `cdk.json`

เมื่อผู้ใช้คลิกเพื่อเผยแพร่บอท [AWS CodeBuild](https://aws.amazon.com/codebuild/) จะเริ่มงาน CDK deployment เพื่อจัดเตรียม API stack (ดูเพิ่มเติมที่: [CDK definition](../cdk/lib/api-publishment-stack.ts)) ซึ่งประกอบด้วย API Gateway, Lambda และ SQS โดย SQS ถูกใช้เพื่อแยกคำขอของผู้ใช้และการทำงานของ LLM เนื่องจากการสร้างผลลัพธ์อาจใช้เวลาเกิน 30 วินาที ซึ่งเป็นข้อจำกัดของโควต้า API Gateway ในการดึงผลลัพธ์ จำเป็นต้องเข้าถึง API แบบอะซิงโครนัส สำหรับรายละเอียดเพิ่มเติม ดูที่ [API Specification](#api-specification)

ไคลเอนต์จำเป็นต้องตั้งค่า `x-api-key` ในส่วนหัวของคำขอ

## ข้อกำหนดของ API

ดูได้[ที่นี่](https://aws-samples.github.io/bedrock-chat)