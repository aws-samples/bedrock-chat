# คู่มือการย้ายฐานข้อมูล

> [!Warning]
> คู่มือนี้สำหรับการอัปเกรดจาก v0 เป็น v1

คู่มือนี้อธิบายขั้นตอนการย้ายข้อมูลเมื่อทำการอัปเดต Bedrock Chat ซึ่งมีการเปลี่ยนคลัสเตอร์ Aurora ใหม่ ขั้นตอนต่อไปนี้ช่วยให้มั่นใจว่าการเปลี่ยนแปลงจะราบรื่นโดยลดเวลาหยุดทำงานและการสูญเสียข้อมูลให้น้อยที่สุด

## ภาพรวม

กระบวนการโยกย้ายข้อมูลเกี่ยวข้องกับการสแกนบอททั้งหมดและเริ่มการทำงานของ embedding ECS tasks สำหรับบอทแต่ละตัว วิธีการนี้จำเป็นต้องมีการคำนวณ embeddings ใหม่ ซึ่งอาจใช้เวลานานและมีค่าใช้จ่ายเพิ่มเติมจากการทำงานของ ECS task และค่าบริการ Bedrock Cohere หากคุณต้องการหลีกเลี่ยงค่าใช้จ่ายและระยะเวลาดังกล่าว โปรดดูที่[ตัวเลือกการโยกย้ายข้อมูลทางเลือก](#alternative-migration-options) ที่ระบุไว้ในส่วนถัดไปของคู่มือนี้

## ขั้นตอนการย้ายข้อมูล

- หลังจาก [npx cdk deploy](../README.md#deploy-using-cdk) พร้อมการเปลี่ยน Aurora แล้ว ให้เปิดสคริปต์ [migrate_v0_v1.py](./migrate_v0_v1.py) และอัปเดตตัวแปรต่อไปนี้ด้วยค่าที่เหมาะสม สามารถดูค่าได้จากแท็บ `Outputs` ใน `CloudFormation` > `BedrockChatStack`

```py
# เปิดสแตค CloudFormation ในคอนโซล AWS Management และคัดลอกค่าจากแท็บ Outputs
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # ไม่จำเป็นต้องเปลี่ยน
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- รันสคริปต์ `migrate_v0_v1.py` เพื่อเริ่มกระบวนการย้ายข้อมูล สคริปต์นี้จะสแกนบอททั้งหมด เรียกใช้งาน embedding ECS tasks และสร้างข้อมูลในคลัสเตอร์ Aurora ใหม่ โปรดทราบว่า:
  - สคริปต์นี้ต้องการ `boto3`
  - สภาพแวดล้อมต้องมีสิทธิ์ IAM ในการเข้าถึงตาราง dynamodb และเรียกใช้ ECS tasks

## ตัวเลือกการย้ายข้อมูลทางเลือก

หากคุณไม่ต้องการใช้วิธีข้างต้นเนื่องจากข้อจำกัดด้านเวลาและค่าใช้จ่าย โปรดพิจารณาแนวทางทางเลือกต่อไปนี้:

### การกู้คืนสแนปช็อตและการย้ายข้อมูลด้วย DMS

อันดับแรก จดบันทึกรหัสผ่านสำหรับเข้าถึงคลัสเตอร์ Aurora ปัจจุบัน จากนั้นรัน `npx cdk deploy` ซึ่งจะทริกเกอร์การแทนที่คลัสเตอร์ หลังจากนั้น สร้างฐานข้อมูลชั่วคราวโดยกู้คืนจากสแนปช็อตของฐานข้อมูลต้นฉบับ
ใช้ [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) เพื่อย้ายข้อมูลจากฐานข้อมูลชั่วคราวไปยังคลัสเตอร์ Aurora ใหม่

หมายเหตุ: ณ วันที่ 29 พฤษภาคม 2024 DMS ไม่รองรับส่วนขยาย pgvector โดยตรง อย่างไรก็ตาม คุณสามารถสำรวจตัวเลือกต่อไปนี้เพื่อแก้ไขข้อจำกัดนี้:

ใช้ [การย้ายข้อมูลแบบเหมือนกันของ DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html) ซึ่งใช้การทำซ้ำเชิงตรรกะแบบเนทีฟ ในกรณีนี้ ทั้งฐานข้อมูลต้นทางและปลายทางต้องเป็น PostgreSQL DMS สามารถใช้ประโยชน์จากการทำซ้ำเชิงตรรกะแบบเนทีฟสำหรับจุดประสงค์นี้

พิจารณาข้อกำหนดเฉพาะและข้อจำกัดของโครงการของคุณเมื่อเลือกวิธีการย้ายข้อมูลที่เหมาะสมที่สุด