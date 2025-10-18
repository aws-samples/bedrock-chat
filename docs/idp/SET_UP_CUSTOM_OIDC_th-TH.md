# ตั้งค่าผู้ให้บริการยืนยันตัวตนภายนอก

## ขั้นตอนที่ 1: สร้าง OIDC Client

ดำเนินการตามขั้นตอนสำหรับผู้ให้บริการ OIDC เป้าหมาย และจดบันทึกค่า client ID และ secret ของ OIDC นอกจากนี้จะต้องใช้ issuer URL ในขั้นตอนถัดไป หากจำเป็นต้องใส่ redirect URI ในขั้นตอนการตั้งค่า ให้ใส่ค่าชั่วคราวไปก่อน ซึ่งจะถูกแทนที่หลังจากการ deploy เสร็จสมบูรณ์

## ขั้นตอนที่ 2: จัดเก็บข้อมูลรับรองใน AWS Secrets Manager

1. ไปที่ AWS Management Console
2. นำทางไปที่ Secrets Manager และเลือก "Store a new secret"
3. เลือก "Other type of secrets"
4. ป้อนค่า client ID และ client secret เป็นคู่ key-value

   - Key: `clientId`, Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`, Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`, Value: <ISSUER_URL_OF_THE_PROVIDER>

5. ทำตามขั้นตอนในการตั้งชื่อและคำอธิบายสำหรับ secret จดชื่อ secret ไว้เนื่องจากคุณจะต้องใช้ในโค้ด CDK (ใช้ในขั้นตอนที่ 3 ตัวแปรชื่อ <YOUR_SECRET_NAME>)
6. ตรวจสอบและบันทึก secret

### ข้อควรระวัง

ชื่อ key ต้องตรงกับข้อความ `clientId`, `clientSecret` และ `issuerUrl` อย่างแม่นยำ

## ขั้นตอนที่ 3: อัปเดตไฟล์ cdk.json

ในไฟล์ cdk.json ของคุณ ให้เพิ่ม ID Provider และ SecretName ลงในไฟล์ cdk.json

ดังนี้:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // ห้ามเปลี่ยน
        "serviceName": "<YOUR_SERVICE_NAME>", // ตั้งค่าเป็นอะไรก็ได้ตามที่คุณต้องการ
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### ข้อควรระวัง

#### ความเป็นเอกลักษณ์

`userPoolDomainPrefix` จะต้องมีความเป็นเอกลักษณ์ในระดับโลกสำหรับผู้ใช้ Amazon Cognito ทั้งหมด หากคุณเลือกคำนำหน้าที่มีการใช้งานอยู่แล้วโดยบัญชี AWS อื่น การสร้างโดเมนของ user pool จะล้มเหลว แนวทางปฏิบัติที่ดีคือการรวมตัวระบุ ชื่อโครงการ หรือชื่อสภาพแวดล้อมไว้ในคำนำหน้าเพื่อให้แน่ใจว่ามีความเป็นเอกลักษณ์

## ขั้นตอนที่ 4: ติดตั้ง CDK Stack ของคุณ

ติดตั้ง CDK stack ของคุณไปยัง AWS:

```sh
npx cdk deploy --require-approval never --all
```

## ขั้นตอนที่ 5: อัปเดตไคลเอนต์ OIDC ด้วย URI การเปลี่ยนเส้นทางของ Cognito

หลังจากที่ทำการ deploy stack แล้ว `AuthApprovedRedirectURI` จะแสดงขึ้นในส่วนของผลลัพธ์ของ CloudFormation กลับไปที่การตั้งค่า OIDC ของคุณและอัปเดตด้วย URI การเปลี่ยนเส้นทางที่ถูกต้อง