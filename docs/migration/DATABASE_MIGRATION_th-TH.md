# คู่มือการย้ายฐานข้อมูล

คู่มือนี้อธิบายขั้นตอนในการย้ายข้อมูลเมื่อทำการอัปเดต Bedrock Claude Chat ซึ่งประกอบด้วยการแทนที่คลัสเตอร์ Aurora โดยขั้นตอนต่อไปนี้จะช่วยให้การเปลี่ยนผ่านเป็นไปอย่างราบรื่นและลดการหยุดทำงานและการสูญเสียข้อมูลให้เหลือน้อยที่สุด

## ภาพรวม

กระบวนการย้ายข้อมูลประกอบด้วยการสแกนบอททั้งหมดและเริ่มงาน ECS สำหรับการฝังข้อมูลสำหรับแต่ละบอท วิธีการนี้ต้องคำนวณการฝังข้อมูลใหม่ ซึ่งอาจใช้เวลานานและเกิดค่าใช้จ่ายเพิ่มเติมจากการดำเนินงาน ECS task และค่าบริการ Bedrock Cohere หากคุณต้องการหลีกเลี่ยงค่าใช้จ่ายและข้อกำหนดด้านเวลาเหล่านี้ โปรดดูที่[ตัวเลือกการย้ายข้อมูลทางเลือก](#alternative-migration-options) ที่จะกล่าวถึงในคู่มือนี้ต่อไป

## ขั้นตอนการย้ายข้อมูล

- หลังจาก [npx cdk deploy](../README.md#deploy-using-cdk) ด้วยการแทนที่ Aurora ให้เปิดสคริปต์ [migrate.py](./migrate.py) และอัปเดตตัวแปรต่อไปนี้ด้วยค่าที่เหมาะสม ค่าเหล่านี้สามารถอ้างอิงได้จากแท็บ `CloudFormation` > `BedrockChatStack` > `Outputs`

```py
# เปิดสแต็ก CloudFormation ในคอนโซลการจัดการ AWS และคัดลอกค่าจากแท็บ Outputs
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # ไม่ต้องเปลี่ยน
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- เรียกใช้สคริปต์ `migrate.py` เพื่อเริ่มกระบวนการย้ายข้อมูล สคริปต์นี้จะสแกนบอตทั้งหมด เรียกใช้งานงาน ECS การฝังข้อมูล และสร้างข้อมูลไปยังคลัสเตอร์ Aurora ใหม่ โปรดทราบว่า:
  - สคริปต์ต้องใช้ `boto3`
  - สภาพแวดล้อมต้องมีสิทธิ์ IAM ในการเข้าถึงตาราง dynamodb และเรียกใช้งานงาน ECS

## วิธีการย้ายข้อมูลทางเลือก

หากคุณไม่ต้องการใช้วิธีการข้างต้นเนื่องจากข้อจำกัดด้านเวลาและค่าใช้จ่าย ให้พิจารณาแนวทางทางเลือกต่อไปนี้:

### การกู้คืนสแนปช็อตและการย้ายข้อมูลด้วย DMS

ขั้นแรก บันทึกรหัสผ่านเพื่อเข้าถึงคลัสเตอร์ Aurora ปัจจุบัน จากนั้นรัน `npx cdk deploy` ซึ่งจะทำการแทนที่คลัสเตอร์ หลังจากนั้น ให้สร้างฐานข้อมูลชั่วคราวโดยการกู้คืนจากสแนปช็อตของฐานข้อมูลเดิม
ใช้ [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) เพื่อย้ายข้อมูลจากฐานข้อมูลชั่วคราวไปยังคลัสเตอร์ Aurora ใหม่

หมายเหตุ: ณ วันที่ 29 พฤษภาคม 2024 DMS ไม่รองรับส่วนขยาย pgvector โดยตรง อย่างไรก็ตาม คุณสามารถสำรวจตัวเลือกต่อไปนี้เพื่อแก้ปัญหาข้อจำกัดนี้:

ใช้ [การย้ายข้อมูลแบบเดียวกัน DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html) ซึ่งใช้การทำซ้ำตามตรรกะดั้งเดิม ในกรณีนี้ ทั้งฐานข้อมูลต้นทางและปลายทางต้องเป็น PostgreSQL DMS สามารถใช้การทำซ้ำตามตรรกะดั้งเดิมเพื่อวัตถุประสงค์นี้

พิจารณาความต้องการและข้อจำกัดเฉพาะของโครงการของคุณเมื่อเลือกวิธีการย้ายข้อมูลที่เหมาะสมที่สุด