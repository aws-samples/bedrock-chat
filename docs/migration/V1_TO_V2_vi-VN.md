# Hướng Dẫn Di Chuyển (từ phiên bản 1 sang phiên bản 2)

## Tóm tắt

- **Dành cho người dùng phiên bản v1.2 trở về trước**: Nâng cấp lên v1.4 và tạo lại bot của bạn bằng Cơ sở Kiến thức (KB). Sau một giai đoạn chuyển đổi, một khi bạn đã xác nhận mọi thứ hoạt động như mong đợi với KB, hãy tiến hành nâng cấp lên v2.
- **Dành cho người dùng v1.3**: Ngay cả khi bạn đang sử dụng KB, vẫn được **khuyến nghị mạnh mẽ** nâng cấp lên v1.4 và tạo lại bot của bạn. Nếu bạn vẫn đang sử dụng pgvector, hãy di chuyển bằng cách tạo lại bot của bạn bằng KB trong v1.4.
- **Dành cho người dùng muốn tiếp tục sử dụng pgvector**: Không khuyến nghị nâng cấp lên v2 nếu bạn dự định tiếp tục sử dụng pgvector. Nâng cấp lên v2 sẽ xóa tất cả các tài nguyên liên quan đến pgvector, và hỗ trợ trong tương lai sẽ không còn khả dụng. Trong trường hợp này, hãy tiếp tục sử dụng v1.
- Lưu ý rằng **nâng cấp lên v2 sẽ dẫn đến việc xóa tất cả các tài nguyên liên quan đến Aurora.** Các bản cập nhật trong tương lai sẽ tập trung riêng vào v2, với v1 sẽ bị loại bỏ.

## Giới thiệu

### Điều gì sẽ xảy ra

Bản cập nhật v2 giới thiệu một thay đổi lớn bằng cách thay thế pgvector trên Aurora Serverless và embedding dựa trên ECS bằng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Thay đổi này không tương thích ngược.

### Tại sao kho lưu trữ này đã áp dụng Knowledge Bases và ngừng sử dụng pgvector

Có một số lý do cho sự thay đổi này:

#### Cải thiện độ chính xác của RAG

- Knowledge Bases sử dụng OpenSearch Serverless làm hệ thống backend, cho phép tìm kiếm lai với cả văn bản đầy đủ và tìm kiếm vector. Điều này dẫn đến độ chính xác tốt hơn trong việc trả lời các câu hỏi có chứa danh từ riêng, mà pgvector gặp khó khăn.
- Nó cũng hỗ trợ nhiều tùy chọn để cải thiện độ chính xác của RAG, như phân đoạn và phân tích nâng cao.
- Knowledge Bases đã được cung cấp rộng rãi gần một năm tính đến tháng 10/2024, với các tính năng như thu thập web đã được thêm vào. Các bản cập nhật trong tương lai được kỳ vọng sẽ giúp dễ dàng áp dụng các chức năng nâng cao theo thời gian dài. Ví dụ, mặc dù kho lưu trữ này chưa triển khai các tính năng như nhập từ các bucket S3 hiện có (một tính năng được yêu cầu thường xuyên) trong pgvector, nhưng nó đã được hỗ trợ trong KB (KnowledgeBases).

#### Bảo trì

- Cài đặt ECS + Aurora hiện tại phụ thuộc vào nhiều thư viện, bao gồm cả các thư viện để phân tích PDF, thu thập web và trích xuất phụ đề YouTube. So với đó, các giải pháp được quản lý như Knowledge Bases giảm gánh nặng bảo trì cho cả người dùng và nhóm phát triển kho lưu trữ.

## Quy Trình Di Chuyển (Tóm Tắt)

Chúng tôi mạnh mẽ khuyến nghị nâng cấp lên v1.4 trước khi chuyển sang v2. Ở v1.4, bạn có thể sử dụng cả bot pgvector và Knowledge Base, cho phép một giai đoạn chuyển đổi để tạo lại các bot pgvector hiện tại trong Knowledge Base và xác minh chúng hoạt động như mong đợi. Ngay cả khi các tài liệu RAG vẫn giống nhau, hãy lưu ý rằng các thay đổi backend sang OpenSearch có thể tạo ra kết quả hơi khác nhau, mặc dù về cơ bản là tương tự, do sự khác biệt như các thuật toán k-NN.

Bằng cách đặt `useBedrockKnowledgeBasesForRag` thành true trong `cdk.json`, bạn có thể tạo bot bằng Knowledge Bases. Tuy nhiên, các bot pgvector sẽ chuyển sang chế độ chỉ đọc, ngăn việc tạo hoặc chỉnh sửa các bot pgvector mới.

![](../imgs/v1_to_v2_readonly_bot.png)

Ở v1.4, [Guardrails cho Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) cũng được giới thiệu. Do các hạn chế khu vực của Knowledge Bases, bucket S3 để tải lên tài liệu phải ở cùng khu vực với `bedrockRegion`. Chúng tôi khuyến nghị sao lưu các bucket tài liệu hiện tại trước khi cập nhật, để tránh phải tải lên thủ công một số lượng lớn tài liệu sau này (vì chức năng nhập bucket S3 là có sẵn).

## Quy Trình Di Chuyển (Chi Tiết)

Các bước khác nhau tùy thuộc vào việc bạn đang sử dụng v1.2 hoặc các phiên bản cũ hơn, hay v1.3.

![](../imgs/v1_to_v2_arch.png)

### Các Bước cho Người Dùng v1.2 hoặc Các Phiên Bản Cũ Hơn

1. **Sao lưu bucket tài liệu hiện có (tùy chọn nhưng được khuyến nghị).** Nếu hệ thống của bạn đã hoạt động, chúng tôi rất khuyến nghị bước này. Sao lưu bucket có tên `bedrockchatstack-documentbucketxxxx-yyyy`. Ví dụ, chúng ta có thể sử dụng [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Cập nhật lên v1.4**: Tìm nạp thẻ v1.4 mới nhất, sửa đổi `cdk.json`, và triển khai. Thực hiện theo các bước sau:

   1. Tìm nạp thẻ mới nhất:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Sửa đổi `cdk.json` như sau:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Triển khai các thay đổi:
      ```bash
      npx cdk deploy
      ```

3. **Tạo lại bot của bạn**: Tạo lại bot của bạn trên Knowledge Base với các định nghĩa giống như các bot pgvector (tài liệu, kích thước khối, v.v.). Nếu bạn có số lượng lớn tài liệu, việc khôi phục từ bản sao lưu ở bước 1 sẽ giúp quá trình này dễ dàng hơn. Để khôi phục, chúng ta có thể sử dụng khôi phục bản sao chéo vùng. Để biết thêm chi tiết, truy cập [tại đây](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Để chỉ định bucket đã khôi phục, đặt phần `S3 Data Source` như sau. Cấu trúc đường dẫn là `s3://<tên-bucket>/<id-người-dùng>/<id-bot>/documents/`. Bạn có thể kiểm tra ID người dùng trên nhóm người dùng Cognito và ID bot trên thanh địa chỉ trên màn hình tạo bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Lưu ý rằng một số tính năng không khả dụng trên Knowledge Bases, như thu thập web và hỗ trợ bản ghi YouTube (Dự định hỗ trợ trình thu thập web ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Đồng thời, hãy lưu ý rằng việc sử dụng Knowledge Bases sẽ phát sinh phí cho cả Aurora và Knowledge Bases trong quá trình chuyển đổi.

4. **Xóa các API đã xuất bản**: Tất cả các API đã xuất bản trước đây sẽ cần được xuất bản lại trước khi triển khai v2 do việc xóa VPC. Để làm điều này, bạn sẽ cần xóa các API hiện có trước. Sử dụng [tính năng Quản lý API của quản trị viên](../ADMINISTRATOR_vi-VN.md) có thể đơn giản hóa quá trình này. Một khi việc xóa tất cả các ngăn xếp CloudFormation `APIPublishmentStackXXXX` hoàn tất, môi trường sẽ sẵn sàng.

5. **Triển khai v2**: Sau khi phát hành v2, tìm nạp mã nguồn được gắn thẻ và triển khai như sau (điều này sẽ khả thi sau khi được phát hành):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Cảnh Báo]
> Sau khi triển khai v2, **TẤT CẢ CÁC BOT CÓ TIỀN TỐ [Không Được Hỗ Trợ, Chỉ Đọc] SẼ BỊ ẨN.** Đảm bảo bạn tạo lại các bot cần thiết trước khi nâng cấp để tránh mất quyền truy cập.

> [!Mẹo]
> Trong quá trình cập nhật ngăn xếp, bạn có thể gặp các thông báo lặp đi lặp lại như: "Trình xử lý tài nguyên trả về thông báo: 'Subnet 'subnet-xxx' có các phụ thuộc và không thể bị xóa.'" Trong những trường hợp như vậy, điều hướng đến Bảng Điều Khiển Quản Lý > EC2 > Giao Diện Mạng và tìm kiếm BedrockChatStack. Xóa các giao diện được hiển thị liên quan đến tên này để giúp quá trình triển khai diễn ra mượt mà hơn.

### Các Bước cho Người Dùng v1.3

Như đã đề cập trước đó, trong v1.4, Knowledge Bases phải được tạo trong bedrockRegion do các hạn chế khu vực. Do đó, bạn sẽ cần tạo lại KB. Nếu bạn đã thử nghiệm KB trong v1.3, hãy tạo lại bot trong v1.4 với các định nghĩa giống nhau. Thực hiện theo các bước được nêu ra cho người dùng v1.2.