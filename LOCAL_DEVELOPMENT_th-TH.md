# การพัฒนาแบบโลคอล

## การพัฒนาส่วนหลัง

ดูที่ [backend/README](../backend/README_th-TH.md)

## การพัฒนาส่วนหน้า (Frontend)

ในตัวอย่างนี้ คุณสามารถแก้ไขและเรียกใช้ส่วนหน้าในเครื่องโดยใช้ทรัพยากร AWS (`API Gateway`, `Cognito` เป็นต้น) ที่ได้ถูกปรับใช้ด้วย `npx cdk deploy`

1. อ้างอิง [การปรับใช้ด้วย CDK](../README.md#deploy-using-cdk) สำหรับการปรับใช้บนสภาพแวดล้อม AWS
2. คัดลอก `frontend/.env.template` และบันทึกเป็น `frontend/.env.local`
3. กรอกเนื้อหาใน `.env.local` ตามผลลัพธ์เอาต์พุตของ `npx cdk deploy` (เช่น `BedrockChatStack.AuthUserPoolClientIdXXXXX`)
4. เรียกใช้คำสั่งต่อไปนี้:

```zsh
cd frontend && npm ci && npm run dev
```

## (ไม่บังคับ แต่แนะนำ) ตั้งค่าฮุกก่อนการคอมมิต

เราได้เพิ่ม GitHub workflows สำหรับตรวจสอบประเภทและตรวจสอบโค้ด ซึ่งจะทำงานเมื่อมีการสร้าง Pull Request แต่การรอให้การตรวจสอบโค้ดเสร็จสิ้นก่อนดำเนินการต่อไม่ใช่ประสบการณ์การพัฒนาที่ดี ดังนั้นงานตรวจสอบโค้ดเหล่านี้ควรดำเนินการโดยอัตโนมัติในขั้นตอนการคอมมิต เราได้นำ [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) มาใช้เป็นกลไกเพื่อบรรลุเป้าหมายนี้ ไม่บังคับ แต่เราแนะนำให้นำมาใช้เพื่อประสบการณ์การพัฒนาที่มีประสิทธิภาพ นอกจากนี้ แม้ว่าเราจะไม่บังคับใช้การจัดรูปแบบ TypeScript ด้วย [Prettier](https://prettier.io/) แต่เราหวังว่าคุณจะนำมาใช้เมื่อมีส่วนร่วม เนื่องจากช่วยป้องกันความแตกต่างที่ไม่จำเป็นระหว่างการตรวจสอบโค้ด

### ติดตั้ง lefthook

ดูรายละเอียด[ที่นี่](https://github.com/evilmartians/lefthook#install) หากคุณใช้ Mac และ Homebrew เพียงแค่รัน `brew install lefthook`

### ติดตั้ง poetry

จำเป็นต้องใช้เนื่องจากการตรวจสอบโค้ด Python ขึ้นอยู่กับ `mypy` และ `black`

```sh
cd backend
python3 -m venv .venv  # ไม่บังคับ (หากคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
source .venv/bin/activate  # ไม่บังคับ (หากคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
pip install poetry
poetry install
```

สำหรับรายละเอียดเพิ่มเติม กรุณาตรวจสอบ [backend README](../backend/README_th-TH.md)

### สร้างฮุกก่อนการคอมมิต

เพียงรัน `lefthook install` ในไดเรกทอรีรากของโครงการนี้