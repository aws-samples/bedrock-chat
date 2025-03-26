# ตั้งค่าผู้ให้บริการยืนยันตัวตนภายนอก

## ขั้นตอนที่ 1: สร้างไคลเอ็นต์ OIDC

ทำตามขั้นตอนสำหรับผู้ให้บริการ OIDC เป้าหมาย และจดบันทึกค่าสำหรับ ID ไคลเอ็นต์ OIDC และรหัสลับ นอกจากนี้ URL ผู้ออกใบรับรองจำเป็นต้องใช้ในขั้นตอนถัดไป หากจำเป็นต้องใช้ URI เปลี่ยนเส้นทาง ให้ป้อนค่าจำลอง ซึ่งจะถูกแทนที่หลังจากการปรับใช้เสร็จสมบูรณ์

## ขั้นตอนที่ 2: จัดเก็บข้อมูลประจำตัวใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. ไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อน client ID และ client secret เป็นคู่คีย์และค่า

   - Key: `clientId`, Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`, Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`, Value: <ISSUER_URL_OF_THE_PROVIDER>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและอธิบายความลับ สังเกตชื่อความลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK (ใช้ใน Step 3 ชื่อตัวแปร <YOUR_SECRET_NAME>)
6. ตรวจสอบและจัดเก็บความลับ

### ข้อควรระวัง

ชื่อคีย์ต้องตรงกับสตริง `clientId`, `clientSecret` และ `issuerUrl` โดยเคร่งครัด

## ขั้นตอนที่ 3: อัปเดต cdk.json

ในไฟล์ cdk.json ของคุณ ให้เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

ดังนี้:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // ห้ามเปลี่ยน
        "serviceName": "<ชื่อบริการของคุณ>", // ตั้งค่าเป็นอะไรก็ได้ที่คุณชอบ
        "secretName": "<ชื่อความลับของคุณ>"
      }
    ],
    "userPoolDomainPrefix": "<คำนำหน้าโดเมนที่ไม่ซ้ำกันสำหรับ User Pool ของคุณ>"
  }
}
```

### ข้อควรระวัง

#### ความเป็นเอกลักษณ์

`userPoolDomainPrefix` ต้องมีความเป็นเอกลักษณ์ทั่วโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่ถูกใช้งานโดยบัญชี AWS อื่นแล้ว การสร้างโดเมน user pool จะล้มเหลว เป็นแนวปฏิบัติที่ดีในการรวมตัวระบุ ชื่อโครงการ หรือชื่อสภาพแวดล้อมในคำนำหน้าเพื่อสร้างความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ปรับใช้สแต็ก CDK

ปรับใช้สแต็ก CDK ไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดตไคลเอนต์ OIDC ด้วย URI เปลี่ยนเส้นทางของ Cognito

หลังจากการปรับใช้สแต็ก `AuthApprovedRedirectURI` จะแสดงอยู่ในผลลัพธ์ของ CloudFormation ให้กลับไปที่การกำหนดค่า OIDC ของคุณและอัปเดตด้วย URI เปลี่ยนเส้นทางที่ถูกต้อง