# แชทบอตเบดร็อก Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!คำเตือน]
>
> **เวอร์ชัน 2 ได้ถูกปล่อยแล้ว กรุณาตรวจสอบคู่มือการย้ายข้อมูลอย่างระมัดระวัง [migration guide](./migration/V1_TO_V2_th-TH.md)** หากไม่ระมัดระวัง **บอตจากเวอร์ชัน 1 จะใช้งานไม่ได้**

แชทบอตหลายภาษาที่ใช้โมเดล LLM จาก [Amazon Bedrock](https://aws.amazon.com/bedrock/) สำหรับปัญญาประดิษฐ์เชิงสร้างสรรค์

### ชมภาพรวมและวิธีติดตั้งบน YouTube

[![ภาพรวม](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### การสนทนาพื้นฐาน

![](./imgs/demo.gif)

### การปรับแต่งบอต

เพิ่มคำสั่งของคุณเองและให้ความรู้ภายนอกด้วย URL หรือไฟล์ (หรือที่เรียกว่า [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) บอตสามารถแชร์กันระหว่างผู้ใช้แอปพลิเคชัน บอตที่กำหนดเองยังสามารถเผยแพร่เป็น API แบบสแตนด์อโลนได้ (ดูรายละเอียด[ที่นี่](./PUBLISH_API_th-TH.md))

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!สำคัญ]
> ด้วยเหตุผลด้านการกำกับดูแล เฉพาะผู้ใช้ที่ได้รับอนุญาตเท่านั้นที่สามารถสร้างบอตที่กำหนดเองได้ เพื่ออนุญาตให้สร้างบอตที่กำหนดเอง ผู้ใช้ต้องเป็นสมาชิกของกลุ่ม `CreatingBotAllowed` ซึ่งสามารถตั้งค่าได้ผ่านคอนโซลการจัดการ > Amazon Cognito User pools หรือ aws cli โปรดทราบว่าไอดีพูลผู้ใช้สามารถอ้างอิงได้โดยเข้าถึง CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`

### แดชบอร์ดผู้ดูแลระบบ

<details>
<summary>แดชบอร์ดผู้ดูแลระบบ</summary>

วิเคราะห์การใช้งานสำหรับแต่ละผู้ใช้ / บอตบนแดชบอร์ดผู้ดูแลระบบ [รายละเอียด](./ADMINISTRATOR_th-TH.md)

![](./imgs/admin_bot_analytics.png)

</details>

### เอเจนต์ขับเคลื่อนด้วย LLM

<details>
<summary>เอเจนต์ขับเคลื่อนด้วย LLM</summary>

โดยใช้ [ฟังก์ชันเอเจนต์](./AGENT_th-TH.md) แชทบอตของคุณสามารถจัดการงานที่ซับซ้อนได้โดยอัตโนมัติ ตัวอย่างเช่น เพื่อตอบคำถามของผู้ใช้ เอเจนต์สามารถดึงข้อมูลที่จำเป็นจากเครื่องมือภายนอกหรือแบ่งงานออกเป็นหลายขั้นตอนเพื่อประมวลผล

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 การปรับใช้งานง่ายมาก

- ในภูมิภาค us-east-1 เปิด [การเข้าถึงโมเดล Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `จัดการการเข้าถึงโมเดล` > เลือกทั้งหมดของ `Anthropic / Claude 3`, ทั้งหมดของ `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` และ `Cohere / Embed Multilingual` แล้วคลิก `บันทึกการเปลี่ยนแปลง`

<details>
<summary>ภาพหน้าจอ</summary>

![](./imgs/model_screenshot.png)

</details>

- เปิด [CloudShell](https://console.aws.amazon.com/cloudshell/home) ในภูมิภาคที่คุณต้องการปรับใช้งาน
- เรียกใช้การปรับใช้งานด้วยคำสั่งต่อไปนี้ หากคุณต้องการระบุเวอร์ชันที่จะปรับใช้งานหรือต้องการใช้นโยบายความปลอดภัย โปรดระบุพารามิเตอร์ที่เหมาะสมจาก [พารามิเตอร์เสริม](#พารามิเตอร์เสริม)

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- คุณจะถูกถามว่าเป็นผู้ใช้ใหม่หรือใช้ v2 หากคุณไม่ใช่ผู้ใช้ต่อเนื่องจาก v0 โปรดป้อน `y`

### พารามิเตอร์เสริม

คุณสามารถระบุพารามิเตอร์ต่อไปนี้ระหว่างการปรับใช้งานเพื่อเพิ่มความปลอดภัยและการปรับแต่ง:

- **--disable-self-register**: ปิดการลงทะเบียนด้วยตนเอง (ค่าเริ่มต้น: เปิดใช้งาน) หากตั้งค่าฟล็ก คุณจะต้องสร้างผู้ใช้ทั้งหมดบน Cognito และจะไม่อนุญาตให้ผู้ใช้ลงทะเบียนบัญชีด้วยตนเอง
- **--enable-lambda-snapstart**: เปิดใช้งาน [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (ค่าเริ่มต้น: ปิดใช้งาน) หากตั้งค่าฟล็ก จะปรับปรุงเวลาเริ่มต้นแบบเย็นสำหรับฟังก์ชัน Lambda โดยให้เวลาตอบสนองที่เร็วขึ้นเพื่อประสบการณ์ผู้ใช้ที่ดีขึ้น
- **--ipv4-ranges**: รายการช่วง IPv4 ที่อนุญาตคั่นด้วยเครื่องหมายจุลภาค (ค่าเริ่มต้น: อนุญาต IPv4 ทั้งหมด)
- **--ipv6-ranges**: รายการช่วง IPv6 ที่อนุญาตคั่นด้วยเครื่องหมายจุลภาค (ค่าเริ่มต้น: อนุญาต IPv6 ทั้งหมด)
- **--disable-ipv6**: ปิดการเชื่อมต่อผ่าน IPv6 (ค่าเริ่มต้น: เปิดใช้งาน)
- **--allowed-signup-email-domains**: รายการโดเมนอีเมลที่อนุญาตให้ลงทะเบียนคั่นด้วยเครื่องหมายจุลภาค (ค่าเริ่มต้น: ไม่มีข้อจำกัดโดเมน)
- **--bedrock-region**: กำหนดภูมิภาคที่ Bedrock พร้อมใช้งาน (ค่าเริ่มต้น: us-east-1)
- **--repo-url**: ที่เก็บ Bedrock Claude Chat แบบกำหนดเองที่จะปรับใช้งาน หากมีการแยกส่วนหรือการควบคุมแหล่งที่มาแบบกำหนดเอง (ค่าเริ่มต้น: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: เวอร์ชันของ Bedrock Claude Chat ที่จะปรับใช้งาน (ค่าเริ่มต้น: เวอร์ชันล่าสุดในการพัฒนา)
- **--cdk-json-override**: คุณสามารถแทนที่ค่าคอนเท็กซ์ CDK ใดๆ ระหว่างการปรับใช้งานโดยใช้บล็อก JSON แทนที่ ซึ่งช่วยให้คุณสามารถแก้ไขการกำหนดค่าโดยไม่ต้องแก้ไขไฟล์ cdk.json โดยตรง

ตัวอย่างการใช้งาน:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

JSON แทนที่ต้องมีโครงสร้างเดียวกับ cdk.json คุณสามารถแทนที่ค่าคอนเท็กซ์ใดๆ รวมถึง:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- และค่าคอนเท็กซ์อื่นๆ ที่กำหนดใน cdk.json

> [!หมายเหตุ]
> ค่าแทนที่จะถูกผสานกับการกำหนดค่า cdk.json ที่มีอยู่ระหว่างการปรับใช้งานใน AWS code build ค่าที่ระบุในส่วนแทนที่จะมีความสำคัญสูงกว่าค่าใน cdk.json

#### ตัวอย่างคำสั่งพร้อมพารามิเตอร์:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- หลังจากประมาณ 35 นาที คุณจะได้รับผลลัพธ์ต่อไปนี้ ซึ่งคุณสามารถเข้าถึงได้จากเบราว์เซอร์ของคุณ

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

หน้าจอลงทะเบียนจะปรากฏขึ้นดังที่แสดงข้างต้น ซึ่งคุณสามารถลงทะเบียนอีเมลและเข้าสู่ระบบได้

> [!สำคัญ]
> หากไม่ตั้งค่าพารามิเตอร์เสริม วิธีการปรับใช้งานนี้จะอนุญาตให้ทุกคนที่รู้ URL สามารถลงทะเบียนได้ สำหรับการใช้งานในระบบผลิต ขอแนะนำอย่างยิ่งให้เพิ่มข้อจำกัด IP และปิดการลงทะเบียนด้วยตนเองเพื่อลดความเสี่ยงด้านความปลอดภัย (คุณสามารถกำหนด allowed-signup-email-domains เพื่อจำกัดผู้ใช้ให้เป็นเพียงที่อยู่อีเมลจากโดเมนบริษัทของคุณเท่านั้น) ใช้ทั้ง ipv4-ranges และ ipv6-ranges สำหรับข้อจำกัด IP และปิดการลงทะเบียนด้วยตนเองโดยใช้ disable-self-register เมื่อเรียกใช้ ./bin

> [!เคล็ดลับ]
> หาก `Frontend URL` ไม่ปรากฏหรือ Bedrock Claude Chat ไม่ทำงานอย่างถูกต้อง อาจเป็นปัญหากับเวอร์ชันล่าสุด ในกรณีนี้ โปรดเพิ่ม `--version "v1.2.6"` ลงในพารามิเตอร์และลองปรับใช้งานอีกครั้ง

## สถาปัตยกรรม

เป็นสถาปัตยกรรมที่สร้างบน AWS managed services โดยไม่ต้องจัดการโครงสร้างพื้นฐาน การใช้ Amazon Bedrock ช่วยให้ไม่ต้องสื่อสารกับ API ภายนอก AWS ซึ่งช่วยให้สามารถปรับใช้แอปพลิเคชันที่มีความสามารถในการขยายขนาด เชื่อถือได้ และปลอดภัย

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): ฐานข้อมูล NoSQL สำหรับจัดเก็บประวัติการสนทนา
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): จุดเชื่อมต่อ API แบ็กเอนด์ ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): การส่งมอบแอปพลิเคชันฟรอนต์เอนด์ ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): การจำกัดที่อยู่ IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): การรับรองตัวตนผู้ใช้
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): บริการที่จัดการเพื่อใช้โมเดลพื้นฐานผ่าน API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): ให้อินเทอร์เฟซการจัดการสำหรับการสร้างข้อมูลเพิ่มเติม ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)) โดยให้บริการสำหรับการฝังและวิเคราะห์เอกสาร
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): รับเหตุการณ์จาก DynamoDB stream และเรียกใช้ Step Functions เพื่อฝังความรู้ภายนอก
- [AWS Step Functions](https://aws.amazon.com/step-functions/): การประสานงานไปป์ไลน์การนำเข้าเพื่อฝังความรู้ภายนอกลงใน Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): ทำหน้าที่เป็นฐานข้อมูลแบ็กเอนด์สำหรับ Bedrock Knowledge Bases โดยให้ความสามารถในการค้นหาแบบเต็มข้อความและการค้นหาแบบเวกเตอร์ ช่วยให้สามารถดึงข้อมูลที่เกี่ยวข้องได้อย่างแม่นยำ
- [Amazon Athena](https://aws.amazon.com/athena/): บริการสอบถามเพื่อวิเคราะห์ S3 bucket

![](./imgs/arch.png)

## การปรับใช้งานด้วย CDK

การปรับใช้งานแบบง่ายใช้ [AWS CodeBuild](https://aws.amazon.com/codebuild/) เพื่อดำเนินการปรับใช้งานด้วย CDK ภายใน ส่วนนี้อธิบายขั้นตอนการปรับใช้งานโดยตรงด้วย CDK

- กรุณามี UNIX, Docker และสภาพแวดล้อมการทำงานของ Node.js หากไม่มี คุณสามารถใช้ [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!สำคัญ]
> หากพื้นที่จัดเก็บข้อมูลในสภาพแวดล้อมเฉพาะที่ไม่เพียงพอระหว่างการปรับใช้งาน การเตรียมความพร้อม CDK อาจเกิดข้อผิดพลาด หากคุณกำลังทำงานใน Cloud9 เป็นต้น เราแนะนำให้ขยายขนาดโวลุ่มของอินสแตนซ์ก่อนการปรับใช้งาน

- โคลนที่เก็บโค้ดนี้

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- ติดตั้งแพ็คเกจ npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- หากจำเป็น ให้แก้ไขรายการต่อไปนี้ใน [cdk.json](./cdk/cdk.json) หากจำเป็น

  - `bedrockRegion`: ภูมิภาคที่ Bedrock พร้อมใช้งาน **หมายเหตุ: Bedrock ไม่รองรับทุกภูมิภาคในขณะนี้**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: ช่วงที่อยู่ IP ที่อนุญาต
  - `enableLambdaSnapStart`: ค่าเริ่มต้นคือ true ตั้งค่าเป็น false หากปรับใช้งานในภูมิภาคที่ไม่รองรับ Lambda SnapStart สำหรับฟังก์ชัน Python

- ก่อนการปรับใช้งาน CDK คุณจะต้องทำการเตรียมความพร้อมสำหรับภูมิภาคที่คุณกำลังปรับใช้งาน

```
npx cdk bootstrap
```

- ปรับใช้งานโครงการตัวอย่างนี้

```
npx cdk deploy --require-approval never --all
```

- คุณจะได้รับผลลัพธ์คล้ายกับต่อไปนี้ URL ของเว็บแอปพลิเคชันจะแสดงใน `BedrockChatStack.FrontendURL` กรุณาเข้าถึงจากเบราว์เซอร์ของคุณ

```sh
 ✅  BedrockChatStack

✨  เวลาการปรับใช้งาน: 78.57s

ผลลัพธ์:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### กำหนดพารามิเตอร์

คุณสามารถกำหนดพารามิเตอร์สำหรับการปรับใช้งานได้สองวิธี: โดยใช้ `cdk.json` หรือใช้ไฟล์ `parameter.ts` ที่มีความปลอดภัยทางชนิด

#### การใช้ cdk.json (วิธีดั้งเดิม)

วิธีดั้งเดิมในการกำหนดค่าพารามิเตอร์คือการแก้ไขไฟล์ `cdk.json` วิธีนี้ง่ายแต่ขาดการตรวจสอบชนิด:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "enableMistral": false,
    "selfSignUpEnabled": true
  }
}
```

#### การใช้ parameter.ts (วิธีที่แนะนำสำหรับความปลอดภัยทางชนิด)

สำหรับความปลอดภัยทางชนิดและประสบการณ์การพัฒนาที่ดีขึ้น คุณสามารถใช้ไฟล์ `parameter.ts` เพื่อกำหนดพารามิเตอร์ของคุณ:

```typescript
// กำหนดพารามิเตอร์สำหรับสภาพแวดล้อมเริ่มต้น
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  enableMistral: false,
  selfSignUpEnabled: true,
});

// กำหนดพารามิเตอร์สำหรับสภาพแวดล้อมเพิ่มเติม
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // ประหยัดต้นทุนสำหรับสภาพแวดล้อมการพัฒนา
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // เพิ่มความพร้อมใช้งานสำหรับการผลิต
});
```

> [!หมายเหตุ]
> ผู้ใช้ปัจจุบันสามารถยังคงใช้ `cdk.json` โดยไม่มีการเปลี่ยนแปลง วิธีการของ `parameter.ts` แนะนำสำหรับการปรับใช้งานใหม่หรือเมื่อคุณต้องจัดการหลายสภาพแวดล้อม

(ส่วนที่เหลือของเอกสารจะถูกแปลในรูปแบบเดียวกัน)

## อื่นๆ

### กำหนดค่าการสนับสนุนโมเดล Mistral

อัปเดต `enableMistral` เป็น `true` ใน [cdk.json](./cdk/cdk.json) และรัน `npx cdk deploy`

```json
...
  "enableMistral": true,
```

> [!สำคัญ]
> โครงการนี้มุ่งเน้นที่โมเดล Anthropic Claude โมเดล Mistral ได้รับการสนับสนุนอย่างจำกัด ตัวอย่างเช่น ตัวอย่างคำสั่งขึ้นอยู่กับโมเดล Claude นี่เป็นตัวเลือกสำหรับ Mistral เท่านั้น เมื่อคุณเปิดใช้งานโมเดล Mistral คุณสามารถใช้เพียงโมเดล Mistral สำหรับคุณสมบัติแชททั้งหมด ไม่ใช่ทั้ง Claude และ Mistral

### กำหนดค่าการสร้างข้อความเริ่มต้น

ผู้ใช้สามารถปรับ[พารามิเตอร์การสร้างข้อความ](https://docs.anthropic.com/claude/reference/complete_post)จากหน้าจอการสร้างบอทแบบกำหนดเอง หากไม่ได้ใช้บอท จะใช้พารามิเตอร์เริ่มต้นที่ตั้งใน [config.py](./backend/app/config.py)

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### ลบทรัพยากร

หากใช้ CLI และ CDK ให้ใช้ `npx cdk destroy` หากไม่ใช่ ให้เข้าถึง [CloudFormation](https://console.aws.amazon.com/cloudformation/home) แล้วลบ `BedrockChatStack` และ `FrontendWafStack` ด้วยตนเอง โปรดทราบว่า `FrontendWafStack` อยู่ในภูมิภาค `us-east-1`

### การตั้งค่าภาษา

สินทรัพย์นี้ตรวจจับภาษาอัตโนมัติโดยใช้ [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector) คุณสามารถเปลี่ยนภาษาจากเมนูแอปพลิเคชัน หรือสามารถใช้ Query String เพื่อตั้งภาษาได้ดังนี้

> `https://example.com?lng=ja`

### ปิดการลงทะเบียนด้วยตนเอง

ตัวอย่างนี้เปิดใช้การลงทะเบียนด้วยตนเองตามค่าเริ่มต้น หากต้องการปิดการลงทะเบียนด้วยตนเอง ให้เปิด [cdk.json](./cdk/cdk.json) และเปลี่ยน `selfSignUpEnabled` เป็น `false` หากคุณกำหนดค่า[ผู้ให้บริการยืนยันตัวตนภายนอก](#external-identity-provider) ค่าจะถูกละเว้นและปิดใช้งานโดยอัตโนมัติ

### จำกัดโดเมนสำหรับที่อยู่อีเมลลงทะเบียน

ตามค่าเริ่มต้น ตัวอย่างนี้ไม่จำกัดโดเมนสำหรับที่อยู่อีเมลลงทะเบียน หากต้องการอนุญาตให้ลงทะเบียนเฉพาะโดเมนที่ระบุ ให้เปิด `cdk.json` และระบุโดเมนเป็นรายการใน `allowedSignUpEmailDomains`

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### ผู้ให้บริการยืนยันตัวตนภายนอก

ตัวอย่างนี้สนับสนุนผู้ให้บริการยืนยันตัวตนภายนอก ปัจจุบันเรารองรับ [Google](./idp/SET_UP_GOOGLE_th-TH.md) และ [ผู้ให้บริการ OIDC แบบกำหนดเอง](./idp/SET_UP_CUSTOM_OIDC_th-TH.md)

### เพิ่มผู้ใช้ใหม่ให้กับกลุ่มโดยอัตโนมัติ

ตัวอย่างนี้มีกลุ่มต่อไปนี้เพื่อให้สิทธิ์กับผู้ใช้:

- [`Admin`](./ADMINISTRATOR_th-TH.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_th-TH.md)

หากคุณต้องการให้ผู้ใช้ที่สร้างใหม่เข้าร่วมกลุ่มโดยอัตโนมัติ คุณสามารถระบุได้ใน [cdk.json](./cdk/cdk.json)

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

ตามค่าเริ่มต้น ผู้ใช้ที่สร้างใหม่จะเข้าร่วมกลุ่ม `CreatingBotAllowed`

(การแปลต่อไปจะเหมือนเดิม)

## ผู้ติดต่อ

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 ผู้มีส่วนร่วมสำคัญ

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## ผู้มีส่วนร่วม

[![ผู้มีส่วนร่วมของ bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## สัญญาอนุญาต

ไลบรารีนี้ได้รับอนุญาตภายใต้สัญญาอนุญาต MIT-0 ดูที่[ไฟล์สัญญาอนุญาต](./LICENSE)