# Panduan Penghijrahan Pangkalan Data

> [!Warning]
> Panduan ini adalah untuk v0 ke v1.

Panduan ini menggariskan langkah-langkah untuk menghijrahkan data semasa melakukan pengemaskinian Bedrock Chat yang mengandungi penggantian kluster Aurora. Prosedur berikut memastikan peralihan yang lancar sambil mengurangkan masa henti dan kehilangan data.

## Gambaran Keseluruhan

Proses penghijrahan melibatkan pengimbasan semua bot dan melancarkan tugas ECS pembenaman untuk setiap satu daripadanya. Pendekatan ini memerlukan pengiraan semula pembenaman, yang boleh mengambil masa yang lama dan menimbulkan kos tambahan disebabkan oleh pelaksanaan tugas ECS dan yuran penggunaan Bedrock Cohere. Jika anda lebih suka mengelakkan kos dan keperluan masa ini, sila rujuk [pilihan penghijrahan alternatif](#alternative-migration-options) yang disediakan kemudian dalam panduan ini.

## Langkah-langkah Penghijrahan

- Selepas [npx cdk deploy](../README.md#deploy-using-cdk) dengan penggantian Aurora, buka skrip [migrate_v0_v1.py](./migrate_v0_v1.py) dan kemaskini pembolehubah berikut dengan nilai yang sesuai. Nilai-nilai tersebut boleh dirujuk pada tab `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Open the CloudFormation stack in the AWS Management Console and copy the values from the Outputs tab.
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # No need to change
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Jalankan skrip `migrate_v0_v1.py` untuk memulakan proses penghijrahan. Skrip ini akan mengimbas semua bot, melancarkan tugas pembenaman ECS, dan mencipta data ke kluster Aurora yang baharu. Sila ambil perhatian bahawa:
  - Skrip ini memerlukan `boto3`.
  - Persekitaran memerlukan kebenaran IAM untuk mengakses jadual dynamodb dan untuk memanggil tugas ECS.

## Pilihan Penghijrahan Alternatif

Jika anda tidak mahu menggunakan kaedah di atas kerana implikasi masa dan kos yang berkaitan, pertimbangkan pendekatan alternatif berikut:

### Pemulihan Snapshot dan Penghijrahan DMS

Pertama, ambil perhatian kata laluan untuk mengakses kluster Aurora semasa. Kemudian jalankan `npx cdk deploy`, yang akan mencetuskan penggantian kluster. Selepas itu, cipta pangkalan data sementara dengan memulihkan dari snapshot pangkalan data asal.
Gunakan [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) untuk menghijrahkan data dari pangkalan data sementara ke kluster Aurora yang baharu.

Nota: Sehingga 29 Mei 2024, DMS tidak menyokong sambungan pgvector secara natif. Walau bagaimanapun, anda boleh meneroka pilihan berikut untuk mengatasi batasan ini:

Gunakan [penghijrahan homogen DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), yang memanfaatkan replikasi logikal natif. Dalam kes ini, kedua-dua pangkalan data sumber dan sasaran mestilah PostgreSQL. DMS boleh memanfaatkan replikasi logikal natif untuk tujuan ini.

Pertimbangkan keperluan khusus dan kekangan projek anda semasa memilih pendekatan penghijrahan yang paling sesuai.