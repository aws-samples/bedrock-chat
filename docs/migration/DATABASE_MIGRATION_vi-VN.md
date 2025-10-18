# Hướng dẫn Di chuyển Cơ sở dữ liệu

> [!Warning]
> Hướng dẫn này dành cho việc nâng cấp từ v0 lên v1.

Hướng dẫn này mô tả các bước để di chuyển dữ liệu khi thực hiện cập nhật Bedrock Chat có bao gồm việc thay thế cụm Aurora. Quy trình sau đây đảm bảo quá trình chuyển đổi diễn ra suôn sẻ trong khi giảm thiểu thời gian ngừng hoạt động và mất dữ liệu.

## Tổng quan

Quá trình di chuyển bao gồm việc quét tất cả các bot và khởi chạy các tác vụ ECS nhúng cho từng bot. Phương pháp này yêu cầu tính toán lại các embedding, điều này có thể tốn thời gian và phát sinh thêm chi phí do việc thực thi tác vụ ECS và phí sử dụng Bedrock Cohere. Nếu bạn muốn tránh các chi phí và yêu cầu thời gian này, vui lòng tham khảo [các lựa chọn di chuyển thay thế](#alternative-migration-options) được cung cấp trong phần sau của hướng dẫn này.

## Các bước di chuyển

- Sau khi thực hiện [npx cdk deploy](../README.md#deploy-using-cdk) với việc thay thế Aurora, mở tệp script [migrate_v0_v1.py](./migrate_v0_v1.py) và cập nhật các biến sau với giá trị thích hợp. Các giá trị có thể được tham chiếu trong tab `Outputs` tại `CloudFormation` > `BedrockChatStack`.

```py
# Mở stack CloudFormation trong AWS Management Console và sao chép các giá trị từ tab Outputs.
# Key: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Key: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Key: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Không cần thay đổi
# Key: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Key: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Chạy script `migrate_v0_v1.py` để bắt đầu quá trình di chuyển. Script này sẽ quét tất cả các bot, khởi chạy các tác vụ embedding ECS và tạo dữ liệu vào cụm Aurora mới. Lưu ý rằng:
  - Script yêu cầu `boto3`.
  - Môi trường yêu cầu các quyền IAM để truy cập bảng dynamodb và để gọi các tác vụ ECS.

## Các Tùy Chọn Di Chuyển Thay Thế

Nếu bạn không muốn sử dụng phương pháp trên do những hạn chế về thời gian và chi phí, hãy xem xét các phương pháp thay thế sau:

### Khôi Phục Snapshot và Di Chuyển DMS

Đầu tiên, hãy ghi nhớ mật khẩu để truy cập cụm Aurora hiện tại. Sau đó chạy lệnh `npx cdk deploy`, điều này sẽ kích hoạt việc thay thế cụm. Tiếp theo, tạo một cơ sở dữ liệu tạm thời bằng cách khôi phục từ snapshot của cơ sở dữ liệu gốc.
Sử dụng [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) để di chuyển dữ liệu từ cơ sở dữ liệu tạm thời sang cụm Aurora mới.

Lưu ý: Tính đến ngày 29 tháng 5 năm 2024, DMS không hỗ trợ sẵn extension pgvector. Tuy nhiên, bạn có thể khám phá các tùy chọn sau để khắc phục giới hạn này:

Sử dụng [DMS homogeneous migration](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), phương pháp này tận dụng logical replication có sẵn. Trong trường hợp này, cả cơ sở dữ liệu nguồn và đích phải là PostgreSQL. DMS có thể tận dụng logical replication có sẵn cho mục đích này.

Hãy cân nhắc các yêu cầu và ràng buộc cụ thể của dự án khi chọn phương pháp di chuyển phù hợp nhất.