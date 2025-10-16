# การพัฒนาในเครื่องท้องถิ่น

## การพัฒนาแบ็กเอนด์

ดูที่ [backend/README](../backend/README_th-TH.md)

## การพัฒนาฟรอนต์เอนด์

ในตัวอย่างนี้ คุณสามารถแก้ไขและเรียกใช้ฟรอนต์เอนด์ในเครื่องของคุณโดยใช้ทรัพยากร AWS (`API Gateway`, `Cognito` ฯลฯ) ที่ได้ถูกติดตั้งด้วยคำสั่ง `npx cdk deploy`

1. อ้างอิงจาก [Deploy using CDK](../README.md#deploy-using-cdk) สำหรับการติดตั้งบนสภาพแวดล้อม AWS
2. คัดลอกไฟล์ `frontend/.env.template` และบันทึกเป็น `frontend/.env.local`
3. กรอกข้อมูลใน `.env.local` โดยอ้างอิงจากผลลัพธ์ของคำสั่ง `npx cdk deploy` (เช่น `BedrockChatStack.AuthUserPoolClientIdXXXXX`)
4. รันคำสั่งต่อไปนี้:

```zsh
cd frontend && npm ci && npm run dev
```

## (ไม่จำเป็น แต่แนะนำ) การตั้งค่า pre-commit hook

เราได้เพิ่ม GitHub workflows สำหรับการตรวจสอบประเภทและการตรวจสอบโค้ด (linting) เข้ามา สิ่งเหล่านี้จะทำงานเมื่อมีการสร้าง Pull Request แต่การรอให้การตรวจสอบโค้ดเสร็จสิ้นก่อนที่จะดำเนินการต่อไม่ใช่ประสบการณ์การพัฒนาที่ดี ดังนั้นงานตรวจสอบโค้ดเหล่านี้ควรดำเนินการโดยอัตโนมัติในขั้นตอนการ commit เราได้นำ [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) มาใช้เป็นกลไกในการทำสิ่งนี้ ไม่ได้เป็นสิ่งที่บังคับ แต่เราแนะนำให้นำมาใช้เพื่อประสบการณ์การพัฒนาที่มีประสิทธิภาพ นอกจากนี้ แม้ว่าเราจะไม่บังคับการจัดรูปแบบ TypeScript ด้วย [Prettier](https://prettier.io/) แต่เราจะขอบคุณหากคุณสามารถนำมาใช้เมื่อมีส่วนร่วมในการพัฒนา เนื่องจากช่วยป้องกันความแตกต่างที่ไม่จำเป็นระหว่างการตรวจสอบโค้ด

### ติดตั้ง lefthook

ดูรายละเอียดได้[ที่นี่](https://github.com/evilmartians/lefthook#install) หากคุณใช้ mac และ homebrew เพียงแค่รัน `brew install lefthook`

### ติดตั้ง poetry

สิ่งนี้จำเป็นเนื่องจากการตรวจสอบโค้ด python ขึ้นอยู่กับ `mypy` และ `black`

```sh
cd backend
python3 -m venv .venv  # ไม่จำเป็น (ถ้าคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
source .venv/bin/activate  # ไม่จำเป็น (ถ้าคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
pip install poetry
poetry install
```

สำหรับรายละเอียดเพิ่มเติม โปรดตรวจสอบ [backend README](../backend/README_th-TH.md)

### สร้าง pre-commit hook

เพียงแค่รัน `lefthook install` ในไดเรกทอรีหลักของโปรเจคนี้