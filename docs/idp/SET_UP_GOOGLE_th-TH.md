# การตั้งค่าผู้ให้บริการตัวตนภายนอกสำหรับ Google

## ขั้นตอนที่ 1: สร้างไคลเอ็นต์ Google OAuth 2.0

1. ไปที่คอนโซลนักพัฒนาของ Google
2. สร้างโปรเจ็กต์ใหม่หรือเลือกโปรเจ็กต์ที่มีอยู่
3. ไปที่ "ข้อมูลประจำตัว" แล้วคลิก "สร้างข้อมูลประจำตัว" และเลือก "ไอดีไคลเอ็นต์ OAuth"
4. กำหนดค่าหน้าจอความยินยอมหากมีการแจ้งเตือน
5. สำหรับประเภทแอปพลิเคชัน ให้เลือก "เว็บแอปพลิเคชัน"
6. ปล่อยให้ URI การเปลี่ยนเส้นทางว่างไว้ก่อนเพื่อตั้งค่าในภายหลัง [ดูขั้นตอนที่ 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. เมื่อสร้างเสร็จ ให้จดบันทึก Client ID และ Client Secret

สำหรับรายละเอียด โปรดเยี่ยมชม [เอกสารอย่างเป็นทางการของ Google](https://support.google.com/cloud/answer/6158849?hl=en)

## ขั้นตอนที่ 2: จัดเก็บข้อมูลประจำตัว Google OAuth ใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. นำทางไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อน Google OAuth clientId และ clientSecret เป็นคู่คีย์และค่า

   1. คีย์: clientId, ค่า: <YOUR_GOOGLE_CLIENT_ID>
   2. คีย์: clientSecret, ค่า: <YOUR_GOOGLE_CLIENT_SECRET>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและอธิบายข้อมูลลับ สังเกตชื่อข้อมูลลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK ของคุณ ตัวอย่างเช่น googleOAuthCredentials (ใช้ในชื่อตัวแปร <YOUR_SECRET_NAME> ของขั้นตอนที่ 3)
6. ตรวจสอบและจัดเก็บข้อมูลลับ

### ข้อควรระวัง

ชื่อคีย์ต้องตรงกับสตริง 'clientId' และ 'clientSecret' โดยเคร่งครัด

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

คำนำหน้าโดเมนของ User Pool ต้องมีความเป็นเอกลักษณ์ทั่วโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่ถูกใช้งานแล้วโดยบัญชี AWS อื่น การสร้างโดเมน User Pool จะล้มเหลว เป็นวิธีปฏิบัติที่ดีในการรวมตัวระบุ ชื่อโครงการ หรือชื่อสภาพแวดล้อมลงในคำนำหน้าเพื่อรับประกันความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ปรับใช้สแต็ก CDK

ปรับใช้สแต็ก CDK ไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดตไคลเอนต์ Google OAuth ด้วย URI การเปลี่ยนเส้นทางของ Cognito

หลังจากการปรับใช้สแต็ก ค่า AuthApprovedRedirectURI จะปรากฏในผลลัพธ์ของ CloudFormation ให้กลับไปที่คอนโซลนักพัฒนา Google และอัปเดตไคลเอนต์ OAuth ด้วย URI การเปลี่ยนเส้นทางที่ถูกต้อง