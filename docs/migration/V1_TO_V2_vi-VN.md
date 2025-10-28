# Hướng dẫn Nâng cấp (v1 lên v2)

## TL;DR

- **Đối với người dùng v1.2 hoặc cũ hơn**: Nâng cấp lên v1.4 và tạo lại bot của bạn bằng Knowledge Base (KB). Sau một thời gian chuyển đổi, khi bạn đã xác nhận mọi thứ hoạt động như mong đợi với KB, hãy tiếp tục nâng cấp lên v2.
- **Đối với người dùng v1.3**: Ngay cả khi bạn đã đang sử dụng KB, chúng tôi **khuyến nghị mạnh mẽ** việc nâng cấp lên v1.4 và tạo lại bot của bạn. Nếu bạn vẫn đang sử dụng pgvector, hãy di chuyển bằng cách tạo lại bot của bạn sử dụng KB trong v1.4.
- **Đối với người dùng muốn tiếp tục sử dụng pgvector**: Không nên nâng cấp lên v2 nếu bạn dự định tiếp tục sử dụng pgvector. Việc nâng cấp lên v2 sẽ xóa tất cả các tài nguyên liên quan đến pgvector, và hỗ trợ trong tương lai sẽ không còn được cung cấp. Trong trường hợp này hãy tiếp tục sử dụng v1.
- Lưu ý rằng **việc nâng cấp lên v2 sẽ dẫn đến việc xóa tất cả các tài nguyên liên quan đến Aurora.** Các cập nhật trong tương lai sẽ tập trung độc quyền vào v2, với v1 sẽ bị loại bỏ dần.

## Giới thiệu

### Điều gì sẽ xảy ra

Bản cập nhật v2 giới thiệu một thay đổi lớn bằng cách thay thế pgvector trên Aurora Serverless và embedding dựa trên ECS bằng [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Thay đổi này không tương thích ngược.

### Lý do tại sao repository này đã áp dụng Knowledge Bases và ngừng sử dụng pgvector

Có một số lý do cho sự thay đổi này:

#### Cải thiện độ chính xác RAG

- Knowledge Bases sử dụng OpenSearch Serverless làm backend, cho phép tìm kiếm kết hợp cả tìm kiếm toàn văn và tìm kiếm vector. Điều này dẫn đến độ chính xác tốt hơn trong việc trả lời các câu hỏi có chứa danh từ riêng, vốn là điểm yếu của pgvector.
- Nó cũng hỗ trợ nhiều tùy chọn hơn để cải thiện độ chính xác RAG, như phân đoạn và phân tích nâng cao.
- Knowledge Bases đã được phát hành rộng rãi gần một năm tính đến tháng 10 năm 2024, với các tính năng như thu thập dữ liệu web đã được thêm vào. Dự kiến sẽ có các cập nhật trong tương lai, giúp việc áp dụng các chức năng nâng cao dễ dàng hơn về lâu dài. Ví dụ, mặc dù repository này chưa triển khai các tính năng như nhập từ bucket S3 hiện có (một tính năng thường được yêu cầu) trong pgvector, nhưng nó đã được hỗ trợ trong KB (KnowledgeBases).

#### Bảo trì

- Cấu hình ECS + Aurora hiện tại phụ thuộc vào nhiều thư viện, bao gồm các thư viện để phân tích PDF, thu thập dữ liệu web và trích xuất phụ đề YouTube. Ngược lại, các giải pháp được quản lý như Knowledge Bases giảm gánh nặng bảo trì cho cả người dùng và đội ngũ phát triển của repository.

## Quy Trình Di Chuyển (Tóm Tắt)

Chúng tôi đặc biệt khuyến nghị nâng cấp lên v1.4 trước khi chuyển sang v2. Trong v1.4, bạn có thể sử dụng cả pgvector và bot Knowledge Base, cho phép một giai đoạn chuyển tiếp để tạo lại các bot pgvector hiện có của bạn trong Knowledge Base và xác minh chúng hoạt động như mong đợi. Ngay cả khi các tài liệu RAG vẫn giống nhau, lưu ý rằng những thay đổi backend sang OpenSearch có thể tạo ra kết quả hơi khác nhau, mặc dù nhìn chung vẫn tương tự, do sự khác biệt như thuật toán k-NN.

Bằng cách đặt `useBedrockKnowledgeBasesForRag` thành true trong `cdk.json`, bạn có thể tạo bot sử dụng Knowledge Bases. Tuy nhiên, các bot pgvector sẽ chuyển sang chế độ chỉ đọc, ngăn việc tạo mới hoặc chỉnh sửa bot pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Trong v1.4, [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) cũng được giới thiệu. Do hạn chế về khu vực của Knowledge Bases, bucket S3 để tải lên tài liệu phải nằm trong cùng khu vực với `bedrockRegion`. Chúng tôi khuyến nghị sao lưu các bucket tài liệu hiện có trước khi cập nhật, để tránh phải tải lên thủ công số lượng lớn tài liệu sau này (vì chức năng nhập bucket S3 đã có sẵn).

## Quy trình Di chuyển (Chi tiết)

Các bước khác nhau tùy thuộc vào việc bạn đang sử dụng v1.2 trở xuống hay v1.3.

![](../imgs/v1_to_v2_arch.png)

### Các bước cho người dùng v1.2 trở xuống

1. **Sao lưu bucket tài liệu hiện có (tùy chọn nhưng được khuyến nghị).** Nếu hệ thống của bạn đang hoạt động, chúng tôi khuyến nghị thực hiện bước này. Sao lưu bucket có tên `bedrockchatstack-documentbucketxxxx-yyyy`. Ví dụ, chúng ta có thể sử dụng [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Cập nhật lên v1.4**: Lấy tag v1.4 mới nhất, sửa đổi `cdk.json`, và triển khai. Thực hiện theo các bước sau:

   1. Lấy tag mới nhất:
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

3. **Tạo lại các bot**: Tạo lại các bot trên Knowledge Base với các định nghĩa giống như các bot pgvector (tài liệu, kích thước chunk, v.v.). Nếu bạn có số lượng lớn tài liệu, việc khôi phục từ bản sao lưu ở bước 1 sẽ giúp quá trình này dễ dàng hơn. Để khôi phục, chúng ta có thể sử dụng tính năng khôi phục bản sao xuyên vùng. Để biết thêm chi tiết, truy cập [tại đây](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Để chỉ định bucket được khôi phục, thiết lập phần `S3 Data Source` như sau. Cấu trúc đường dẫn là `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Bạn có thể kiểm tra user id trên Cognito user pool và bot id trên thanh địa chỉ trong màn hình tạo bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Lưu ý rằng một số tính năng không có sẵn trên Knowledge Bases, như crawling web và hỗ trợ phụ đề YouTube (Đang lên kế hoạch hỗ trợ web crawler ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Ngoài ra, hãy nhớ rằng việc sử dụng Knowledge Bases sẽ phát sinh chi phí cho cả Aurora và Knowledge Bases trong quá trình chuyển đổi.

4. **Xóa các API đã xuất bản**: Tất cả các API đã xuất bản trước đó sẽ cần được xuất bản lại trước khi triển khai v2 do việc xóa VPC. Để làm điều này, bạn cần xóa các API hiện có trước. Sử dụng [tính năng Quản lý API của quản trị viên](../ADMINISTRATOR_vi-VN.md) có thể đơn giản hóa quy trình này. Khi việc xóa tất cả các stack CloudFormation `APIPublishmentStackXXXX` hoàn tất, môi trường sẽ sẵn sàng.

5. **Triển khai v2**: Sau khi phát hành v2, lấy mã nguồn được gắn tag và triển khai như sau (điều này sẽ khả thi sau khi phát hành):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Sau khi triển khai v2, **TẤT CẢ CÁC BOT CÓ TIỀN TỐ [Unsupported, Read-only] SẼ BỊ ẨN.** Đảm bảo bạn tạo lại các bot cần thiết trước khi nâng cấp để tránh mất quyền truy cập.

> [!Tip]
> Trong quá trình cập nhật stack, bạn có thể gặp phải các thông báo lặp lại như: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." Trong những trường hợp như vậy, hãy điều hướng đến Management Console > EC2 > Network Interfaces và tìm kiếm BedrockChatStack. Xóa các giao diện được hiển thị liên quan đến tên này để giúp đảm bảo quá trình triển khai suôn sẻ hơn.

### Các bước cho người dùng v1.3

Như đã đề cập trước đó, trong v1.4, Knowledge Bases phải được tạo trong bedrockRegion do các hạn chế về khu vực. Do đó, bạn sẽ cần tạo lại KB. Nếu bạn đã thử nghiệm KB trong v1.3, hãy tạo lại bot trong v1.4 với các định nghĩa giống nhau. Thực hiện theo các bước đã nêu cho người dùng v1.2.