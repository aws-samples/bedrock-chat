# ตั้งค่าผู้ให้บริการตัวตนภายนอกสำหรับ Google

## ขั้นตอนที่ 1: สร้างไคลเอนต์ OAuth 2.0 ของ Google

1. ไปที่คอนโซลนักพัฒนาของ Google
2. สร้างโปรเจกต์ใหม่หรือเลือกโปรเจกต์ที่มีอยู่
3. ไปที่ "ข้อมูลประจำตัว" แล้วคลิก "สร้างข้อมูลประจำตัว" และเลือก "ID ไคลเอนต์ OAuth"
4. กำหนดค่าหน้าจอความยินยอมหากมีการแจ้ง
5. เลือกประเภทแอปพลิเคชันเป็น "เว็บแอปพลิเคชัน"
6. ปล่อยช่อง URI เปลี่ยนเส้นทางว่างไว้ก่อนเพื่อตั้งค่าภายหลัง และบันทึกชั่วคราว [ดูขั้นตอนที่ 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. เมื่อสร้างเสร็จ ให้จดบันทึก Client ID และ Client Secret

สำหรับรายละเอียด โปรดเยี่ยมชม [เอกสารอย่างเป็นทางการของ Google](https://support.google.com/cloud/answer/6158849?hl=en)

## ขั้นตอนที่ 2: จัดเก็บข้อมูลประจำตัว Google OAuth ใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. ไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อน Google OAuth clientId และ clientSecret เป็นคู่คีย์และค่า

   1. คีย์: clientId, ค่า: <YOUR_GOOGLE_CLIENT_ID>
   2. คีย์: clientSecret, ค่า: <YOUR_GOOGLE_CLIENT_SECRET>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและอธิบายความลับ บันทึกชื่อความลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK ของคุณ ตัวอย่างเช่น googleOAuthCredentials (ใช้ในชื่อตัวแปร <YOUR_SECRET_NAME> ในขั้นตอนที่ 3)
6. ตรวจสอบและจัดเก็บความลับ

### ข้อควรระวัง

ชื่อคีย์ต้องตรงกับสตริง 'clientId' และ 'clientSecret' อย่างเคร่งครัด

## ขั้นตอนที่ 3: อัปเดต cdk.json

ในไฟล์ cdk.json ของคุณ ให้เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

ดังนี้:

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
    "userPoolDomainPrefix": "<คำนำหน้าโดเมนที่ไม่ซ้ำกันสำหรับ User Pool ของคุณ>"
  }
}
```

### ข้อควรระวัง

#### ความเป็นเอกลักษณ์

คำนำหน้าโดเมนของ User Pool ต้องมีความเป็นเอกลักษณ์ทั่วโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่ถูกใช้งานแล้วโดยบัญชี AWS อื่น การสร้างโดเมน User Pool จะล้มเหลว เป็นแนวปฏิบัติที่ดีในการรวมตัวระบุ ชื่อโปรเจ็กต์ หรือชื่อสภาพแวดล้อมลงในคำนำหน้าเพื่อรับประกันความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: กระจายสแต็ก CDK

กระจายสแต็ก CDK ของคุณไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดตไคลเอนต์ Google OAuth ด้วย URI การเปลี่ยนเส้นทางของ Cognito

หลังจากที่คุณได้ทำการปรับใช้สแต็ก AuthApprovedRedirectURI จะปรากฏในผลลัพธ์ของ CloudFormation แล้ว ให้กลับไปที่คอนโซลนักพัฒนาของ Google และอัปเดตไคลเอนต์ OAuth ด้วย URI การเปลี่ยนเส้นทางที่ถูกต้อง