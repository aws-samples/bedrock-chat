# ตั้งค่าผู้ให้บริการตัวตนภายนอก

## ขั้นตอนที่ 1: สร้างไคลเอ็นต์ OIDC

ทำตามขั้นตอนสำหรับผู้ให้บริการ OIDC เป้าหมาย และจดบันทึกค่าสำหรับ ID และความลับของไคลเอ็นต์ OIDC รวมถึง URL ของผู้ออกใบรับรอง หากต้องการ URI การเปลี่ยนเส้นทาง ให้ป้อนค่าจำลอง ซึ่งจะถูกแทนที่หลังจากการติดตั้งเสร็จสมบูรณ์

## ขั้นตอนที่ 2: จัดเก็บข้อมูลประจำตัวใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. ไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อนรหัสลูกค้า (client ID) และความลับของลูกค้า (client secret) เป็นคู่คีย์-ค่า

   - Key: `clientId`, Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`, Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`, Value: <ISSUER_URL_OF_THE_PROVIDER>

5. ทำตามคำแนะนำเพื่อตั้งชื่อและอธิบายความลับ สังเกตชื่อความลับเนื่องจากคุณจะต้องใช้ในโค้ด CDK (ใช้ในตัวแปร <YOUR_SECRET_NAME> ของขั้นตอนที่ 3)
6. ตรวจสอบและจัดเก็บความลับ

### ข้อควรระวัง

ชื่อคีย์ต้องตรงกับสตริง `clientId`, `clientSecret` และ `issuerUrl` โดยเคร่งครัด

## ขั้นตอนที่ 3: อัปเดต cdk.json

ในไฟล์ cdk.json ของคุณ เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

เช่นนี้:

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

`userPoolDomainPrefix` ต้องมีความเป็นเอกลักษณ์ทั่วโลกในบรรดาผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่ถูกใช้งานโดยบัญชี AWS อื่นแล้ว การสร้างโดเมน user pool จะล้มเหลว เป็นแนวปฏิบัติที่ดีในการรวมตัวระบุ ชื่อโครงการ หรือชื่อสภาพแวดล้อมในคำนำหน้าเพื่อสร้างความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ปรับใช้ CDK Stack ของคุณ

ปรับใช้ CDK stack ของคุณไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดต OIDC Client ด้วย Cognito Redirect URIs

หลังจากการปรับใช้สแต็ก `AuthApprovedRedirectURI` จะปรากฏในผลลัพธ์ของ CloudFormation กลับไปยังการกำหนดค่า OIDC และอัปเดตด้วย redirect URIs ที่ถูกต้อง