# คู่มือการย้ายฐานข้อมูล

คู่มือนี้อธิบายขั้นตอนในการย้ายข้อมูลเมื่อทำการอัปเดต Bedrock Claude Chat ซึ่งประกอบด้วยการแทนที่คลัสเตอร์ Aurora วิธีการนี้จะช่วยให้มั่นใจว่าการเปลี่ยนแปลงจะราบรื่นโดยลดเวลาหยุดทำงานและการสูญเสียข้อมูลให้เหลือน้อยที่สุด

## ภาพรวม

กระบวนการย้ายข้อมูลประกอบด้วยการสแกนบอททั้งหมดและเริ่มใช้งานงาน ECS สำหรับการฝังข้อมูลของแต่ละบอท วิธีนี้ต้องคำนวณการฝังข้อมูลใหม่ ซึ่งอาจใช้เวลานานและทำให้เกิดค่าใช้จ่ายเพิ่มเติมจากการดำเนินงาน ECS task และค่าบริการ Bedrock Cohere หากคุณต้องการหลีกเลี่ยงค่าใช้จ่ายและข้อจำกัดด้านเวลาเหล่านี้ โปรดดูตัวเลือกการย้ายข้อมูลทางเลือกที่ระบุไว้ในส่วนถัดไปของคู่มือนี้

## ขั้นตอนการย้ายข้อมูล

- หลังจากการรันคำสั่ง [npx cdk deploy](../README.md#deploy-using-cdk) พร้อมการแทนที่ Aurora เปิดสคริปต์ [migrate.py](./migrate.py) และอัปเดตตัวแปรต่อไปนี้ด้วยค่าที่เหมาะสม ค่าเหล่านี้สามารถอ้างอิงได้จากแท็บ `CloudFormation` > `BedrockChatStack` > `Outputs`

```py
# เปิดสแต็ก CloudFormation ในคอนโซล AWS Management Console และคัดลอกค่าจากแท็บ Outputs
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

- รันสคริปต์ `migrate.py` เพื่อเริ่มกระบวนการย้ายข้อมูล สคริปต์นี้จะสแกนบอตทั้งหมด เรียกใช้งาน embedding ECS tasks และสร้างข้อมูลไปยัง Aurora cluster ใหม่ โปรดทราบว่า:
  - สคริปต์ต้องการ `boto3`
  - สภาพแวดล้อมต้องมีสิทธิ์ IAM เพื่อเข้าถึงตาราง dynamodb และเรียกใช้งาน ECS tasks

## วิธีการย้ายข้อมูลทางเลือก

หากคุณไม่ต้องการใช้วิธีข้างต้นเนื่องจากข้อจำกัดด้านเวลาและค่าใช้จ่าย ให้พิจารณาแนวทางทางเลือกต่อไปนี้:

### การกู้คืนสแนปช็อตและการย้ายข้อมูลด้วย DMS

ขั้นแรก บันทึกรหัสผ่านเพื่อเข้าถึงคลัสเตอร์ Aurora ปัจจุบัน จากนั้นรันคำสั่ง `npx cdk deploy` ซึ่งจะทำการแทนที่คลัสเตอร์ หลังจากนั้น สร้างฐานข้อมูลชั่วคราวโดยการกู้คืนจากสแนปช็อตของฐานข้อมูลเดิม
ใช้ [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) เพื่อย้ายข้อมูลจากฐานข้อมูลชั่วคราวไปยังคลัสเตอร์ Aurora ใหม่

หมายเหตุ: ณ วันที่ 29 พฤษภาคม 2024 DMS ไม่รองรับส่วนขยาย pgvector โดยตรง อย่างไรก็ตาม คุณสามารถสำรวจตัวเลือกต่อไปนี้เพื่อหลีกเลี่ยงข้อจำกัดนี้:

ใช้ [การย้ายข้อมูลแบบเดียวกัน DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html) ซึ่งใช้การทำซ้ำทางตรรกะดั้งเดิม ในกรณีนี้ ทั้งฐานข้อมูลต้นทางและปลายทางต้องเป็น PostgreSQL DMS สามารถใช้การทำซ้ำทางตรรกะดั้งเดิมเพื่อวัตถุประสงค์นี้

พิจารณาข้อกำหนดและข้อจำกัดเฉพาะของโครงการของคุณเมื่อเลือกวิธีการย้ายข้อมูลที่เหมาะสมที่สุด