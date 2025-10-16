# ตั้งค่าผู้ให้บริการยืนยันตัวตนภายนอกสำหรับ Google

## ขั้นตอนที่ 1: สร้าง Google OAuth 2.0 Client

1. ไปที่ Google Developer Console
2. สร้างโปรเจกต์ใหม่หรือเลือกโปรเจกต์ที่มีอยู่
3. นำทางไปที่ "Credentials" จากนั้นคลิกที่ "Create Credentials" และเลือก "OAuth client ID"
4. ตั้งค่าหน้าจอการยินยอมหากมีการแจ้งเตือน
5. สำหรับประเภทแอปพลิเคชัน ให้เลือก "Web application"
6. เว้น redirect URI ว่างไว้ก่อนเพื่อตั้งค่าภายหลัง [ดูขั้นตอนที่ 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. เมื่อสร้างเสร็จแล้ว จดบันทึก Client ID และ Client Secret

สำหรับรายละเอียดเพิ่มเติม เยี่ยมชม [เอกสารอย่างเป็นทางการของ Google](https://support.google.com/cloud/answer/6158849?hl=en)

## ขั้นตอนที่ 2: จัดเก็บข้อมูลรับรอง Google OAuth ใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. นำทางไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อนค่า clientId และ clientSecret ของ Google OAuth เป็นคู่ key-value

   1. Key: clientId, Value: <YOUR_GOOGLE_CLIENT_ID>
   2. Key: clientSecret, Value: <YOUR_GOOGLE_CLIENT_SECRET>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและอธิบายข้อมูลลับ จดจำชื่อข้อมูลลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK ของคุณ ตัวอย่างเช่น googleOAuthCredentials (ใช้ในขั้นตอนที่ 3 ชื่อตัวแปร <YOUR_SECRET_NAME>)
6. ตรวจสอบและจัดเก็บข้อมูลลับ

### ข้อควรระวัง

ชื่อ key ต้องตรงกับข้อความ 'clientId' และ 'clientSecret' อย่างแน่นอน

## ขั้นตอนที่ 3: อัปเดตไฟล์ cdk.json

ในไฟล์ cdk.json ของคุณ ให้เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

ดังนี้:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### ข้อควรระวัง

#### ความเป็นเอกลักษณ์

userPoolDomainPrefix จะต้องมีความเป็นเอกลักษณ์ในระดับโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่มีการใช้งานแล้วโดยบัญชี AWS อื่น การสร้างโดเมนของ user pool จะล้มเหลว แนวปฏิบัติที่ดีคือการรวมตัวระบุ ชื่อโครงการ หรือชื่อสภาพแวดล้อมไว้ในคำนำหน้าเพื่อให้แน่ใจว่ามีความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ติดตั้ง CDK Stack ของคุณ

ติดตั้ง CDK stack ของคุณไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดต Google OAuth Client ด้วย URI การเปลี่ยนเส้นทางของ Cognito

หลังจากที่ได้ทำการ deploy stack แล้ว AuthApprovedRedirectURI จะแสดงอยู่ในส่วนของผลลัพธ์ของ CloudFormation ให้กลับไปที่ Google Developer Console และอัปเดต OAuth client ด้วย URI การเปลี่ยนเส้นทางที่ถูกต้อง