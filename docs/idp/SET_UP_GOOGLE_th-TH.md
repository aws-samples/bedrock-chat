# ตั้งค่าผู้ให้บริการยืนยันตัวตนภายนอกสำหรับ Google

## ขั้นตอนที่ 1: สร้างไคลเอนต์ Google OAuth 2.0

1. ไปที่คอนโซลนักพัฒนาของ Google
2. สร้างโปรเจกต์ใหม่หรือเลือกโปรเจกต์ที่มีอยู่
3. ไปที่ "ข้อมูลประจำตัว" แล้วคลิก "สร้างข้อมูลประจำตัว" และเลือก "ID ไคลเอนต์ OAuth"
4. กำหนดค่าหน้าจอความยินยอมหากได้รับแจ้ง
5. เลือก "เว็บแอปพลิเคชัน" สำหรับประเภทแอปพลิเคชัน
6. ปล่อยช่อง URI เปลี่ยนเส้นทางว่างไว้ก่อนเพื่อตั้งค่าภายหลัง และบันทึกไว้ชั่วคราว [ดูขั้นตอนที่ 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. เมื่อสร้างเสร็จ ให้จดบันทึก Client ID และ Client Secret

สำหรับรายละเอียดเพิ่มเติม ให้เยี่ยมชม [เอกสารอย่างเป็นทางการของ Google](https://support.google.com/cloud/answer/6158849?hl=en)

## ขั้นตอนที่ 2: จัดเก็บข้อมูลประจำตัว Google OAuth ใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. ไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อนข้อมูลประจำตัว Google OAuth clientId และ clientSecret เป็นคู่คีย์-ค่า

   1. คีย์: clientId, ค่า: <YOUR_GOOGLE_CLIENT_ID>
   2. คีย์: clientSecret, ค่า: <YOUR_GOOGLE_CLIENT_SECRET>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและคำอธิบายข้อมูลลับ บันทึกชื่อข้อมูลลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK ของคุณ ตัวอย่างเช่น googleOAuthCredentials (ใช้ในชื่อตัวแปร <YOUR_SECRET_NAME> ของขั้นตอนที่ 3)
6. ตรวจสอบและจัดเก็บข้อมูลลับ

### ข้อควรระวัง

ชื่อคีย์ต้องตรงกับสตริง 'clientId' และ 'clientSecret' อย่างเคร่งครัด

## ขั้นตอนที่ 3: อัปเดต cdk.json

ในไฟล์ cdk.json ของคุณ ให้เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

เช่นนี้:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<ชื่อความลับของคุณ>"
      }
    ],
    "userPoolDomainPrefix": "<คำนำหน้าโดเมนเฉพาะสำหรับ User Pool ของคุณ>"
  }
}
```

### ข้อควรระวัง

#### ความเป็นเอกลักษณ์

คำนำหน้าโดเมนของ User Pool ต้องมีความเป็นเอกลักษณ์ทั่วโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่ถูกใช้งานโดยบัญชี AWS อื่นแล้ว การสร้างโดเมน User Pool จะล้มเหลว เป็นวิธีปฏิบัติที่ดีในการรวมตัวระบุ ชื่อโปรเจ็ค หรือชื่อสภาพแวดล้อมในคำนำหน้าเพื่อรับประกันความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ปรับใช้ CDK Stack

ปรับใช้ CDK stack บน AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดต Google OAuth Client ด้วย Redirect URIs ของ Cognito

หลังจากที่คุณได้ทำการ deploy stack แล้ว AuthApprovedRedirectURI จะปรากฏอยู่ในส่วน CloudFormation outputs ให้กลับไปที่ Google Developer Console และอัปเดต OAuth client ด้วย redirect URIs ที่ถูกต้อง