# การพัฒนาในเครื่อง

## การพัฒนาส่วนหลัง

ดูที่ [backend/README](../backend/README_th-TH.md)

## การพัฒนาส่วนหน้า

ในตัวอย่างนี้ คุณสามารถแก้ไขและเปิดใช้งานส่วนหน้าในเครื่องได้โดยใช้ทรัพยากร AWS (`API Gateway`, `Cognito` ฯลฯ) ที่ได้ถูกปรับใช้ด้วย `npx cdk deploy`

1. ดูที่ [ปรับใช้ด้วย CDK](../README.md#deploy-using-cdk) สำหรับการปรับใช้บนสภาพแวดล้อม AWS
2. คัดลอก `frontend/.env.template` และบันทึกเป็น `frontend/.env.local`
3. กรอกเนื้อหาของ `.env.local` ตามผลลัพธ์ที่ได้จาก `npx cdk deploy` (เช่น `BedrockChatStack.AuthUserPoolClientIdXXXXX`)
4. เรียกใช้คำสั่งต่อไปนี้:

```zsh
cd frontend && npm ci && npm run dev
```

## (ไม่บังคับ แต่แนะนำ) ตั้งค่าฮุกก่อนการคอมมิต

เราได้เพิ่มเวิร์กโฟลว์ของ GitHub สำหรับตรวจสอบประเภทและตรวจสอบโค้ด ซึ่งจะทำงานเมื่อมีการสร้าง Pull Request แต่การรอให้การตรวจสอบโค้ดเสร็จสิ้นก่อนดำเนินการต่อไปไม่ใช่ประสบการณ์การพัฒนาที่ดี ดังนั้นงานการตรวจสอบโค้ดเหล่านี้ควรทำการตรวจสอบโดยอัตโนมัติในขั้นตอนการคอมมิต เราได้แนะนำ [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) เป็นกลไกเพื่อให้บรรลุเป้าหมายนี้ ไม่บังคับ แต่เราแนะนำให้นำมาใช้เพื่อประสบการณ์การพัฒนาที่มีประสิทธิภาพ นอกจากนี้ แม้ว่าเราจะไม่บังคับการจัดรูปแบบ TypeScript ด้วย [Prettier](https://prettier.io/) แต่เราหวังว่าคุณจะนำมาใช้เมื่อมีส่วนร่วม เนื่องจากช่วยป้องกันความแตกต่างที่ไม่จำเป็นระหว่างการตรวจสอบโค้ด

### ติดตั้ง lefthook

ดูรายละเอียด[ที่นี่](https://github.com/evilmartians/lefthook#install) หากคุณใช้ mac และ homebrew เพียงรัน `brew install lefthook`

### ติดตั้ง poetry

จำเป็นเนื่องจากการตรวจสอบโค้ด Python ขึ้นอยู่กับ `mypy` และ `black`

```sh
cd backend
python3 -m venv .venv  # ไม่บังคับ (หากคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
source .venv/bin/activate  # ไม่บังคับ (หากคุณไม่ต้องการติดตั้ง poetry บนสภาพแวดล้อมของคุณ)
pip install poetry
poetry install
```

สำหรับรายละเอียดเพิ่มเติม กรุณาตรวจสอบ [backend README](../backend/README_th-TH.md)

### สร้างฮุกก่อนการคอมมิต

เพียงรัน `lefthook install` ที่ไดเรกทอรีรากของโปรเจกต์นี้