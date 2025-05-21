# Hướng Dẫn Di Chuyển Cơ Sở Dữ Liệu

> [!Warning]
> Hướng dẫn này dành cho việc nâng cấp từ phiên bản v0 lên v1.

Hướng dẫn này trình bày các bước để di chuyển dữ liệu khi thực hiện cập nhật Bedrock Chat với việc thay thế cụm Aurora. Quy trình sau đây đảm bảo quá trình chuyển đổi diễn ra trơn tru, giảm thiểu thời gian ngừng hoạt động và mất mát dữ liệu.

## Tổng quan

Quá trình di chuyển bao gồm quét tất cả các bot và khởi chạy các tác vụ ECS nhúng cho từng bot. Phương pháp này yêu cầu tính toán lại các embedding, có thể mất nhiều thời gian và phát sinh chi phí bổ sung do thực thi tác vụ ECS và phí sử dụng Bedrock Cohere. Nếu bạn muốn tránh những chi phí và yêu cầu thời gian này, vui lòng tham khảo [các tùy chọn di chuyển thay thế](#alternative-migration-options) được cung cấp sau trong hướng dẫn này.

## Các Bước Di Chuyển

- Sau khi [npx cdk deploy](../README.md#deploy-using-cdk) với việc thay thế Aurora, mở tập lệnh [migrate_v0_v1.py](./migrate_v0_v1.py) và cập nhật các biến sau với các giá trị phù hợp. Các giá trị có thể được tham khảo trong tab `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Mở ngăn xếp CloudFormation trong Bảng điều khiển Quản lý AWS và sao chép các giá trị từ tab Outputs.
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

- Chạy tập lệnh `migrate_v0_v1.py` để bắt đầu quá trình di chuyển. Tập lệnh này sẽ quét tất cả các bot, khởi chạy các tác vụ nhúng ECS và tạo dữ liệu vào cụm Aurora mới. Lưu ý rằng:
  - Tập lệnh yêu cầu `boto3`.
  - Môi trường yêu cầu quyền IAM để truy cập bảng dynamodb và khởi chạy các tác vụ ECS.

## Các Phương Án Di Chuyển Thay Thế

Nếu bạn không muốn sử dụng phương pháp trên do các hàm ý về thời gian và chi phí, hãy xem xét các cách tiếp cận thay thế sau:

### Phục Hồi Ảnh Chụp và Di Chuyển DMS

Trước tiên, lưu ý mật khẩu để truy cập cụm Aurora hiện tại. Sau đó chạy `npx cdk deploy`, điều này sẽ kích hoạt việc thay thế cụm. Tiếp theo, tạo một cơ sở dữ liệu tạm thời bằng cách khôi phục từ ảnh chụp của cơ sở dữ liệu gốc.
Sử dụng [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) để di chuyển dữ liệu từ cơ sở dữ liệu tạm thời sang cụm Aurora mới.

Lưu ý: Tính đến ngày 29 tháng 5 năm 2024, DMS không hỗ trợ nguyên sinh tiện ích mở rộng pgvector. Tuy nhiên, bạn có thể khám phá các tùy chọn sau để giải quyết hạn chế này:

Sử dụng [Di chuyển đồng nhất DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), tận dụng sao chép logic gốc. Trong trường hợp này, cả nguồn và đích cơ sở dữ liệu đều phải là PostgreSQL. DMS có thể tận dụng sao chép logic gốc cho mục đích này.

Xem xét các yêu cầu và ràng buộc cụ thể của dự án của bạn khi chọn phương pháp di chuyển phù hợp nhất.