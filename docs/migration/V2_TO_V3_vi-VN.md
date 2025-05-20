# Hướng Dẫn Di Chuyển (từ phiên bản 2 sang phiên bản 3)

## TóM TẮT

- V3 giới thiệu điều khiển quyền chi tiết và chức năng Bot Store, yêu cầu thay đổi lược đồ DynamoDB
- **Sao lưu bảng ConversationTable của DynamoDB trước khi di chuyển**
- Cập nhật URL kho lưu trữ từ `bedrock-claude-chat` sang `bedrock-chat`
- Chạy tập lệnh di chuyển để chuyển đổi dữ liệu sang lược đồ mới
- Tất cả bot và cuộc trò chuyện của bạn sẽ được bảo toàn với mô hình quyền mới
- **QUAN TRỌNG: Trong quá trình di chuyển, ứng dụng sẽ không khả dụng cho tất cả người dùng cho đến khi quá trình di chuyển hoàn tất. Quá trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu năng môi trường phát triển của bạn.**
- **QUAN TRỌNG: Tất cả các API Đã Xuất Bản phải bị xóa trong quá trình di chuyển.**
- **CẢNH BÁO: Quá trình di chuyển không thể đảm bảo 100% thành công cho tất cả các bot. Vui lòng ghi lại cấu hình bot quan trọng của bạn trước khi di chuyển để có thể tạo lại thủ công nếu cần**

## Giới thiệu

### Có Gì Mới Trong Phiên Bản 3

Phiên bản 3 giới thiệu những cải tiến đáng kể cho Bedrock Chat:

1. **Kiểm soát quyền chi tiết**: Kiểm soát quyền truy cập vào bot của bạn thông qua quyền theo nhóm người dùng
2. **Cửa hàng Bot**: Chia sẻ và khám phá bot thông qua một marketplace tập trung
3. **Tính năng quản trị**: Quản lý API, đánh dấu bot là thiết yếu và phân tích việc sử dụng bot

Những tính năng mới này đòi hỏi thay đổi trong lược đồ DynamoDB, buộc phải thực hiện quá trình di chuyển dữ liệu cho người dùng hiện tại.

### Tại Sao Việc Di Chuyển Này Là Cần Thiết

Mô hình quyền mới và chức năng Cửa hàng Bot yêu cầu cấu trúc lại cách lưu trữ và truy cập dữ liệu bot. Quá trình di chuyển sẽ chuyển đổi các bot và cuộc trò chuyện hiện có của bạn sang lược đồ mới trong khi vẫn giữ nguyên toàn bộ dữ liệu.

> [!CẢNH BÁO]
> Thông Báo Gián Đoạn Dịch Vụ: **Trong quá trình di chuyển, ứng dụng sẽ không khả dụng đối với tất cả người dùng.** Hãy lên kế hoạch thực hiện di chuyển này trong một cửa sổ bảo trì khi người dùng không cần truy cập vào hệ thống. Ứng dụng chỉ khả dụng trở lại sau khi script di chuyển đã hoàn tất thành công và tất cả dữ liệu đã được chuyển đổi sang lược đồ mới. Quá trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu suất của môi trường phát triển của bạn.

> [!QUAN TRỌNG]
> Trước khi tiến hành di chuyển: **Quá trình di chuyển không thể đảm bảo 100% thành công cho tất cả các bot**, đặc biệt là những bot được tạo với các phiên bản cũ hoặc có cấu hình tùy chỉnh. Vui lòng ghi lại các cấu hình bot quan trọng (hướng dẫn, nguồn kiến thức, cài đặt) trước khi bắt đầu quá trình di chuyển trong trường hợp bạn cần phải tạo lại chúng theo cách thủ công.

## Quá Trình Di Chuyển

### Thông Báo Quan Trọng Về Khả Năng Hiển Thị Bot Trong V3

Trong V3, **tất cả các bot v2 có chế độ chia sẻ công khai sẽ được tìm thấy trong Cửa Hàng Bot.** Nếu bạn có các bot chứa thông tin nhạy cảm mà bạn không muốn hiển thị, hãy cân nhắc chuyển chúng thành riêng tư trước khi di chuyển sang V3.

### Bước 1: Xác Định Tên Môi Trường Của Bạn

Trong quy trình này, `{TÊN_MÔI_TRƯỜNG_CỦA_BẠN}` được sử dụng để xác định tên CloudFormation Stacks. Nếu bạn đang sử dụng tính năng [Triển Khai Nhiều Môi Trường](../../README.md#deploying-multiple-environments), hãy thay thế bằng tên môi trường sẽ được di chuyển. Nếu không, hãy thay thế bằng chuỗi trống.

### Bước 2: Cập Nhật URL Kho Lưu Trữ (Được Khuyến Nghị)

Kho lưu trữ đã được đổi tên từ `bedrock-claude-chat` thành `bedrock-chat`. Cập nhật kho lưu trữ cục bộ của bạn:

```bash
# Kiểm tra URL remote hiện tại
git remote -v

# Cập nhật URL remote
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Xác minh thay đổi
git remote -v
```

### Bước 3: Đảm Bảo Bạn Đang Ở Phiên Bản V2 Mới Nhất

> [!CẢNH BÁO]
> Bạn PHẢI cập nhật lên v2.10.0 trước khi di chuyển sang V3. **Bỏ qua bước này có thể dẫn đến mất dữ liệu trong quá trình di chuyển.**

Trước khi bắt đầu di chuyển, hãy đảm bảo bạn đang chạy phiên bản V2 mới nhất (**v2.10.0**). Điều này đảm bảo bạn có tất cả các bản sửa lỗi và cải tiến trước khi nâng cấp lên V3:

```bash
# Tìm nạp các thẻ mới nhất
git fetch --tags

# Chuyển sang phiên bản V2 mới nhất
git checkout v2.10.0

# Triển khai phiên bản V2 mới nhất
cd cdk
npm ci
npx cdk deploy --all
```

### Bước 4: Ghi Lại Tên Bảng DynamoDB V2

Lấy tên ConversationTable V2 từ đầu ra CloudFormation:

```bash
# Lấy tên ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {TÊN_MÔI_TRƯỜNG_CỦA_BẠN}BedrockChatStack
```

Hãy chắc chắn lưu lại tên bảng này ở nơi an toàn, vì bạn sẽ cần nó cho script di chuyển sau này.

### Bước 5: Sao Lưu Bảng DynamoDB

Trước khi tiếp tục, hãy tạo một bản sao lưu của ConversationTable DynamoDB bằng tên bạn vừa ghi lại:

```bash
# Tạo bản sao lưu của bảng V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name TÊN_BẢNG_CONVERSATION_V2_CỦA_BẠN

# Kiểm tra trạng thái sao lưu đã sẵn sàng
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn MÃ_XÁC_NHẬN_SAO_LƯU_CỦA_BẠN
```

### Bước 6: Xóa Tất Cả Các API Đã Xuất Bản

> [!QUAN TRỌNG]
> Trước khi triển khai V3, bạn phải xóa tất cả các API đã xuất bản để tránh xung đột giá trị đầu ra Cloudformation trong quá trình nâng cấp.

1. Đăng nhập vào ứng dụng với tư cách quản trị viên
2. Điều hướng đến phần Quản Trị và chọn "Quản Lý API"
3. Xem danh sách tất cả các API đã xuất bản
4. Xóa từng API đã xuất bản bằng cách nhấp vào nút xóa bên cạnh nó

Bạn có thể tìm thêm thông tin về việc xuất bản và quản lý API trong tài liệu [PUBLISH_API.md](../PUBLISH_API_vi-VN.md), [ADMINISTRATOR.md](../ADMINISTRATOR_vi-VN.md).

### Bước 7: Kéo V3 và Triển Khai

Kéo mã V3 mới nhất và triển khai:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!QUAN TRỌNG]
> Một khi bạn triển khai V3, ứng dụng sẽ không khả dụng cho tất cả người dùng cho đến khi hoàn tất quá trình di chuyển. Lược đồ mới không tương thích với định dạng dữ liệu cũ, vì vậy người dùng sẽ không thể truy cập bot hoặc cuộc trò chuyện của họ cho đến khi bạn hoàn tất script di chuyển trong các bước tiếp theo.

### Bước 8: Ghi Lại Tên Bảng DynamoDB V3

Sau khi triển khai V3, bạn cần lấy tên ConversationTable và BotTable mới:

```bash
# Lấy tên ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {TÊN_MÔI_TRƯỜNG_CỦA_BẠN}BedrockChatStack

# Lấy tên BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {TÊN_MÔI_TRƯỜNG_CỦA_BẠN}BedrockChatStack
```

> [!Quan Trọng]
> Hãy chắc chắn lưu lại các tên bảng V3 này cùng với tên bảng V2 bạn đã lưu trước đó, vì bạn sẽ cần tất cả chúng cho script di chuyển.

### Bước 9: Chạy Script Di Chuyển

Script di chuyển sẽ chuyển đổi dữ liệu V2 của bạn sang lược đồ V3. Đầu tiên, chỉnh sửa script di chuyển `docs/migration/migrate_v2_v3.py` để đặt tên bảng và khu vực của bạn:

```python
# Khu vực nơi dynamodb được đặt
REGION = "ap-northeast-1" # Thay thế bằng khu vực của bạn

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Thay thế bằng giá trị đã ghi lại trong Bước 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Thay thế bằng giá trị đã ghi lại trong Bước 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Thay thế bằng giá trị đã ghi lại trong Bước 8
```

Sau đó chạy script bằng Poetry từ thư mục backend:

> [!LƯU Ý]
> Phiên bản yêu cầu Python đã được thay đổi thành 3.13.0 trở lên (Có thể thay đổi trong phát triển tương lai. Xem pyproject.toml). Nếu bạn đã cài đặt venv với phiên bản Python khác, bạn sẽ cần xóa nó một lần.

```bash
# Điều hướng đến thư mục backend
cd backend

# Cài đặt các phụ thuộc nếu bạn chưa làm
poetry install

# Chạy thử trước để xem những gì sẽ được di chuyển
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Nếu mọi thứ trông ổn, chạy di chuyển thực tế
poetry run python ../docs/migration/migrate_v2_v3.py

# Xác minh di chuyển thành công
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Script di chuyển sẽ tạo một tệp báo cáo trong thư mục hiện tại với chi tiết về quá trình di chuyển. Kiểm tra tệp này để đảm bảo tất cả dữ liệu của bạn đã được di chuyển chính xác.

#### Xử Lý Khối Lượng Dữ Liệu Lớn

Đối với các môi trường có người dùng nặng hoặc lượng dữ liệu lớn, hãy xem xét các phương pháp sau:

1. **Di chuyển người dùng từng người**: Đối với người dùng có khối lượng dữ liệu lớn, hãy di chuyển từng người một:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Xem xét bộ nhớ**: Quá trình di chuyển tải dữ liệu vào bộ nhớ. Nếu bạn gặp lỗi Hết Bộ Nhớ (OOM), hãy thử:

   - Di chuyển từng người dùng một
   - Chạy di chuyển trên máy có bộ nhớ nhiều hơn
   - Chia di chuyển thành các lô người dùng nhỏ hơn

3. **Giám sát di chuyển**: Kiểm tra các tệp báo cáo được tạo để đảm bảo tất cả dữ liệu được di chuyển chính xác, đặc biệt là với các tập dữ liệu lớn.

### Bước 10: Xác Minh Ứng Dụng

Sau khi di chuyển, mở ứng dụng của bạn và xác minh:

- Tất cả bot của bạn đều có sẵn
- Các cuộc trò chuyện được bảo toàn
- Các điều khiển quyền mới đang hoạt động

### Dọn Dẹp (Tùy Chọn)

Sau khi xác nhận di chuyển thành công và tất cả dữ liệu của bạn được truy cập chính xác trong V3, bạn có thể tùy ý xóa bảng conversation V2 để tiết kiệm chi phí:

```bash
# Xóa bảng conversation V2 (CHỈ sau khi xác nhận di chuyển thành công)
aws dynamodb delete-table --table-name TÊN_BẢNG_CONVERSATION_V2_CỦA_BẠN
```

> [!QUAN TRỌNG]
> Chỉ xóa bảng V2 sau khi xác minh kỹ lưỡng rằng tất cả dữ liệu quan trọng của bạn đã được di chuyển thành công sang V3. Chúng tôi khuyến nghị giữ bản sao lưu được tạo trong Bước 2 trong ít nhất vài tuần sau khi di chuyển, ngay cả khi bạn xóa bảng gốc.

## Câu hỏi Thường gặp V3

### Truy cập Bot và Quyền

**Q: Chuyện gì xảy ra nếu bot tôi đang sử dụng bị xóa hoặc quyền truy cập của tôi bị thu hồi?**
A: Việc ủy quyền được kiểm tra tại thời điểm trò chuyện, vì vậy bạn sẽ mất quyền truy cập ngay lập tức.

**Q: Chuyện gì xảy ra nếu người dùng bị xóa (ví dụ: nhân viên nghỉ việc)?**
A: Dữ liệu của họ có thể được xóa hoàn toàn bằng cách xóa tất cả các mục từ DynamoDB với ID người dùng làm khóa phân vùng (PK).

**Q: Tôi có thể tắt chia sẻ cho bot công khai thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi tắt chế độ chia sẻ.

**Q: Tôi có thể xóa bot công khai thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi xóa.

### Bảo mật và Triển khai

**Q: Bảo mật cấp hàng (RLS) có được triển khai cho bảng bot không?**
A: Không, do sự đa dạng của các mẫu truy cập. Việc ủy quyền được thực hiện khi truy cập bot, và nguy cơ rò rỉ siêu dữ liệu được coi là tối thiểu so với lịch sử cuộc trò chuyện.

**Q: Các yêu cầu để xuất bản một API là gì?**
A: Bot phải ở chế độ công khai.

**Q: Có màn hình quản lý cho tất cả các bot riêng tư không?**
A: Không có trong phiên bản V3 ban đầu. Tuy nhiên, các mục vẫn có thể được xóa bằng cách truy vấn với ID người dùng nếu cần.

**Q: Có chức năng gắn thẻ bot để cải thiện trải nghiệm tìm kiếm không?**
A: Không có trong phiên bản V3 ban đầu, nhưng gắn thẻ tự động dựa trên LLM có thể được thêm vào trong các bản cập nhật trong tương lai.

### Quản trị

**Q: Quản trị viên có thể làm gì?**
A: Quản trị viên có thể:

- Quản lý bot công khai (bao gồm kiểm tra các bot có chi phí cao)
- Quản lý API
- Đánh dấu bot công khai là thiết yếu

**Q: Tôi có thể đánh dấu bot được chia sẻ một phần là thiết yếu không?**
A: Không, chỉ hỗ trợ bot công khai.

**Q: Tôi có thể đặt ưu tiên cho các bot được ghim không?**
A: Ở phiên bản ban đầu, không.

### Cấu hình Ủy quyền

**Q: Làm thế nào để thiết lập ủy quyền?**
A:

1. Mở bảng điều khiển Amazon Cognito và tạo các nhóm người dùng trong nhóm người dùng BrChat
2. Thêm người dùng vào các nhóm này nếu cần
3. Trong BrChat, chọn các nhóm người dùng mà bạn muốn cho phép truy cập khi cấu hình cài đặt chia sẻ bot

Lưu ý: Các thay đổi về thành viên nhóm yêu cầu đăng nhập lại để có hiệu lực. Các thay đổi được phản ánh khi làm mới token, nhưng không trong thời gian hiệu lực của token ID (mặc định 30 phút trong V3, có thể cấu hình bằng `tokenValidMinutes` trong `cdk.json` hoặc `parameter.ts`).

**Q: Hệ thống có kiểm tra với Cognito mỗi khi truy cập bot không?**
A: Không, việc ủy quyền được kiểm tra bằng token JWT để tránh các thao tác I/O không cần thiết.

### Chức năng Tìm kiếm

**Q: Tìm kiếm bot có hỗ trợ tìm kiếm ngữ nghĩa không?**
A: Không, chỉ hỗ trợ khớp văn bản một phần. Tìm kiếm ngữ nghĩa (ví dụ: "automobile" → "car", "EV", "vehicle") không khả dụng do các hạn chế của OpenSearch Serverless hiện tại (Tháng 3 năm 2025).