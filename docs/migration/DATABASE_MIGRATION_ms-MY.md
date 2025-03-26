# Panduan Migrasi Pangkalan Data

Panduan ini menggariskan langkah-langkah untuk memindahkan data semasa melakukan kemas kini Bedrock Claude Chat yang mengandungi penggantian kluster Aurora. Prosedur berikut memastikan peralihan yang lancar sambil meminimumkan masa henti dan kehilangan data.

## Gambaran Keseluruhan

Proses migrasi melibatkan pengimbasan semua bot dan melancarkan tugas ECS pembenam untuk setiap satunya. Pendekatan ini memerlukan pengiraan semula pembenam, yang boleh mengambil masa dan menimbulkan kos tambahan disebabkan oleh pelaksanaan tugas ECS dan yuran penggunaan Bedrock Cohere. Jika anda lebih suka mengelakkan kos dan keperluan masa ini, sila merujuk kepada [pilihan migrasi alternatif](#alternative-migration-options) yang disediakan kemudian dalam panduan ini.

## Langkah Migrasi

- Selepas [npx cdk deploy](../README.md#deploy-using-cdk) dengan penggantian Aurora, buka skrip [migrate.py](./migrate.py) dan kemas kini pemboleh ubah berikut dengan nilai yang sesuai. Nilai-nilai tersebut boleh dirujuk pada tab `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Buka stack CloudFormation dalam Konsol Pengurusan AWS dan salin nilai dari tab Outputs.
# Kunci: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Kunci: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Kunci: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Tiada perlu menukar
# Kunci: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Kunci: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Jalankan skrip `migrate.py` untuk memulakan proses migrasi. Skrip ini akan mengimbas semua bot, melancarkan tugas ECS embedding, dan membuat data ke kluster Aurora yang baru. Ambil perhatian bahawa:
  - Skrip memerlukan `boto3`.
  - Persekitaran memerlukan kebenaran IAM untuk mengakses jadual dynamodb dan melancarkan tugas ECS.

## Pilihan Alternatif Migrasi

Jika anda tidak menyukai kaedah di atas kerana implikasi masa dan kos, pertimbangkan pendekatan alternatif berikut:

### Pemulihan Snapshot dan Migrasi DMS

Pertama, catat kata laluan untuk mengakses kluster Aurora semasa. Kemudian jalankan `npx cdk deploy`, yang mencetuskan penggantian kluster. Selepas itu, buat pangkalan data sementara dengan memulihkan dari snapshot pangkalan data asal.
Gunakan [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) untuk memigrasikan data dari pangkalan data sementara ke kluster Aurora baru.

Nota: Sehingga 29 Mei 2024, DMS tidak menyokong sambungan pgvector secara asli. Walau bagaimanapun, anda boleh meneroka pilihan berikut untuk mengatasi had ini:

Gunakan [migrasi homogen DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), yang memanfaatkan replikasi logik asli. Dalam kes ini, kedua-dua pangkalan data sumber dan sasaran mesti PostgreSQL. DMS boleh memanfaatkan replikasi logik asli untuk tujuan ini.

Pertimbangkan keperluan dan kekangan khusus projek anda apabila memilih pendekatan migrasi yang paling sesuai.