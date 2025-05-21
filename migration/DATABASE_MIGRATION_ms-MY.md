# Panduan Migrasi Pangkalan Data

> [!Warning]
> Panduan ini adalah untuk v0 ke v1.

Panduan ini menggariskan langkah-langkah untuk memindahkan data semasa mengemas kini Bedrock Chat yang mengandungi penggantian kluster Aurora. Prosedur berikut memastikan peralihan yang lancar sambil meminimumkan masa henti dan kehilangan data.

## Gambaran Keseluruhan

Proses migrasi melibatkan pengimbasan semua bot dan melancarkan tugas ECS penyematan untuk setiap bot. Pendekatan ini memerlukan pengiraan semula penyematan, yang boleh mengambil masa dan menimbulkan kos tambahan disebabkan oleh pelaksanaan tugas ECS dan yuran penggunaan Bedrock Cohere. Jika anda lebih suka mengelakkan kos dan keperluan masa ini, sila merujuk kepada [pilihan migrasi alternatif](#alternative-migration-options) yang disediakan kemudian dalam panduan ini.

## Langkah Migrasi

- Selepas [npx cdk deploy](../README.md#deploy-using-cdk) dengan penggantian Aurora, buka skrip [migrate_v0_v1.py](./migrate_v0_v1.py) dan kemas kini pemboleh ubah berikut dengan nilai yang sesuai. Nilai-nilai ini boleh dirujuk pada tab `CloudFormation` > `BedrockChatStack` > `Outputs`.

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

- Jalankan skrip `migrate_v0_v1.py` untuk memulakan proses migrasi. Skrip ini akan mengimbas semua bot, melancarkan tugas penyematan ECS, dan membuat data ke kluster Aurora yang baru. Ambil perhatian bahawa:
  - Skrip memerlukan `boto3`.
  - Persekitaran memerlukan keizinan IAM untuk mengakses jadual dynamodb dan melancarkan tugas ECS.

## Pilihan Alternatif Migrasi

Jika anda tidak menyukai kaedah di atas kerana implikasi masa dan kos, pertimbangkan pendekatan alternatif berikut:

### Pulihan Snapshot dan Migrasi DMS

Pertama, catat kata laluan untuk mengakses kluster Aurora semasa. Kemudian jalankan `npx cdk deploy`, yang mencetuskan penggantian kluster. Selepas itu, buat pangkalan data sementara dengan memulihkan dari snapshot pangkalan data asal.
Gunakan [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) untuk memindahkan data dari pangkalan data sementara ke kluster Aurora baharu.

Nota: Sehingga 29 Mei 2024, DMS tidak menyokong sambungan pgvector secara semula jadi. Walau bagaimanapun, anda boleh meneroka pilihan berikut untuk mengatasi had ini:

Gunakan [migrasi homogen DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), yang memanfaatkan replikasi logik semula jadi. Dalam kes ini, pangkalan data sumber dan sasaran mestilah PostgreSQL. DMS boleh memanfaatkan replikasi logik semula jadi untuk tujuan ini.

Pertimbangkan keperluan dan kekangan khusus projek anda apabila memilih pendekatan migrasi yang paling sesuai.