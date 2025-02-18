# คู่มือการย้ายฐานข้อมูล

คู่มือนี้อธิบายขั้นตอนในการย้ายข้อมูลเมื่อทำการอัปเดต Bedrock Claude Chat ซึ่งประกอบด้วยการแทนที่คลัสเตอร์ Aurora กระบวนการต่อไปนี้จะช่วยให้มั่นใจว่าการเปลี่ยนผ่านจะราบรื่นโดยลดเวลาหยุดทำงานและการสูญเสียข้อมูลให้น้อยที่สุด

## ภาพรวม

กระบวนการย้ายข้อมูลประกอบด้วยการสแกนบอตทั้งหมดและเริ่มใช้งานงาน ECS สำหรับการฝังข้อมูลของแต่ละบอต วิธีนี้ต้องคำนวณการฝังข้อมูลใหม่ ซึ่งอาจใช้เวลานานและก่อให้เกิดค่าใช้จ่ายเพิ่มเติมจากการดำเนินงาน ECS และค่าธรรมเนียมการใช้ Bedrock Cohere หากคุณต้องการหลีกเลี่ยงค่าใช้จ่ายและข้อกำหนดด้านเวลาเหล่านี้ โปรดดูที่[ตัวเลือกการย้ายข้อมูลทางเลือก](#alternative-migration-options) ที่ให้มาในคู่มือนี้

## ขั้นตอนการย้ายข้อมูล

- หลังจาก [npx cdk deploy](../README.md#deploy-using-cdk) กับการแทนที่ Aurora ให้เปิดสคริปต์ [migrate.py](./migrate.py) และอัปเดตตัวแปรต่อไปนี้ด้วยค่าที่เหมาะสม ค่าสามารถอ้างอิงได้จากแท็บ `CloudFormation` > `BedrockChatStack` > `Outputs`

```py
# เปิดสแตคของ CloudFormation ในคอนโซลการจัดการ AWS และคัดลอกค่าจากแท็บ Outputs
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # ไม่ต้องเปลี่ยน
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- เรียกใช้สคริปต์ `migrate.py` เพื่อเริ่มกระบวนการย้ายข้อมูล สคริปต์นี้จะสแกนบอตทั้งหมด เรียกใช้งานงาน Embedding ของ ECS และสร้างข้อมูลไปยังคลัสเตอร์ Aurora ใหม่ โปรดทราบว่า:
  - สคริปต์ต้องการ `boto3`
  - สภาพแวดล้อมต้องมีสิทธิ์ IAM เพื่อเข้าถึงตาราง DynamoDB และเรียกใช้งานงาน ECS

## ตัวเลือกการย้ายข้อมูลทางเลือก

หากคุณไม่ต้องการใช้วิธีข้างต้นเนื่องจากข้อจำกัดด้านเวลาและค่าใช้จ่าย ให้พิจารณาแนวทางทางเลือกต่อไปนี้:

### การกู้คืนสแนปช็อตและการย้ายข้อมูลด้วย DMS

ขั้นแรก ให้จดบันทึกรหัสผ่านเพื่อเข้าถึงคลัสเตอร์ Aurora ปัจจุบัน จากนั้นรันคำสั่ง `npx cdk deploy` ซึ่งจะทำการแทนที่คลัสเตอร์ หลังจากนั้นให้สร้างฐานข้อมูลชั่วคราวโดยการกู้คืนจากสแนปช็อตของฐานข้อมูลเดิม
ใช้ [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) เพื่อย้ายข้อมูลจากฐานข้อมูลชั่วคราวไปยังคลัสเตอร์ Aurora ใหม่

หมายเหตุ: ณ วันที่ 29 พฤษภาคม 2024 DMS ยังไม่รองรับส่วนขยาย pgvector โดยตรง อย่างไรก็ตาม คุณสามารถสำรวจตัวเลือกต่อไปนี้เพื่อหลีกเลี่ยงข้อจำกัดนี้:

ใช้ [การย้ายข้อมูลแบบเดียวกัน DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html) ซึ่งใช้การทำซ้ำแบบตรรกะดั้งเดิม ในกรณีนี้ ฐานข้อมูลต้นทางและปลายทางทั้งสองต้องเป็น PostgreSQL DMS สามารถใช้การทำซ้ำแบบตรรกะดั้งเดิมเพื่อวัตถุประสงค์นี้

พิจารณาข้อกำหนดและข้อจำกัดเฉพาะของโครงการของคุณเมื่อเลือกแนวทางการย้ายข้อมูลที่เหมาะสมที่สุด