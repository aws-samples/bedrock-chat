# Hướng dẫn Nâng cấp (v2 lên v3)

## TL;DR

- V3 giới thiệu kiểm soát quyền chi tiết và chức năng Bot Store, yêu cầu thay đổi schema DynamoDB
- **Sao lưu ConversationTable DynamoDB của bạn trước khi di chuyển**
- Cập nhật URL repository của bạn từ `bedrock-claude-chat` thành `bedrock-chat`
- Chạy script di chuyển để chuyển đổi dữ liệu của bạn sang schema mới
- Tất cả bot và cuộc hội thoại của bạn sẽ được bảo toàn với mô hình phân quyền mới
- **QUAN TRỌNG: Trong quá trình di chuyển, ứng dụng sẽ không khả dụng cho tất cả người dùng cho đến khi quá trình di chuyển hoàn tất. Quá trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu suất của môi trường phát triển của bạn.**
- **QUAN TRỌNG: Tất cả API đã Xuất bản phải được xóa trong quá trình di chuyển.**
- **CẢNH BÁO: Quá trình di chuyển không thể đảm bảo thành công 100% cho tất cả các bot. Vui lòng ghi lại các cấu hình bot quan trọng của bạn trước khi di chuyển trong trường hợp bạn cần tạo lại chúng thủ công**

## Giới thiệu

### Có gì mới trong V3

V3 giới thiệu những cải tiến đáng kể cho Bedrock Chat:

1. **Kiểm soát quyền chi tiết**: Kiểm soát quyền truy cập vào bot của bạn dựa trên nhóm người dùng
2. **Cửa hàng Bot**: Chia sẻ và khám phá bot thông qua một thị trường tập trung
3. **Tính năng quản trị**: Quản lý API, đánh dấu bot là thiết yếu và phân tích việc sử dụng bot

Những tính năng mới này yêu cầu thay đổi schema DynamoDB, đòi hỏi quy trình di chuyển dữ liệu cho người dùng hiện tại.

### Tại sao cần Di chuyển Dữ liệu

Mô hình phân quyền mới và chức năng Cửa hàng Bot đòi hỏi phải tái cấu trúc cách lưu trữ và truy cập dữ liệu bot. Quy trình di chuyển sẽ chuyển đổi các bot và cuộc hội thoại hiện có của bạn sang schema mới trong khi vẫn bảo toàn toàn bộ dữ liệu.

> [!WARNING]
> Thông báo Gián đoạn Dịch vụ: **Trong quá trình di chuyển, ứng dụng sẽ không khả dụng với tất cả người dùng.** Hãy lên kế hoạch thực hiện việc di chuyển này trong thời gian bảo trì khi người dùng không cần truy cập hệ thống. Ứng dụng sẽ chỉ khả dụng trở lại sau khi script di chuyển hoàn tất thành công và tất cả dữ liệu đã được chuyển đổi đúng sang schema mới. Quy trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu suất của môi trường phát triển của bạn.

> [!IMPORTANT]
> Trước khi tiến hành di chuyển: **Quy trình di chuyển không thể đảm bảo thành công 100% cho tất cả các bot**, đặc biệt là những bot được tạo bằng phiên bản cũ hơn hoặc có cấu hình tùy chỉnh. Vui lòng ghi lại các cấu hình bot quan trọng (hướng dẫn, nguồn kiến thức, cài đặt) trước khi bắt đầu quá trình di chuyển trong trường hợp bạn cần tạo lại chúng theo cách thủ công.

## Quy trình Di chuyển

### Thông báo Quan trọng về Khả năng Hiển thị Bot trong V3

Trong V3, **tất cả các bot v2 có chia sẻ công khai sẽ có thể tìm kiếm được trong Cửa hàng Bot.** Nếu bạn có các bot chứa thông tin nhạy cảm mà bạn không muốn người khác khám phá được, hãy cân nhắc việc đặt chúng ở chế độ riêng tư trước khi di chuyển lên V3.

### Bước 1: Xác định tên môi trường của bạn

Trong quy trình này, `{YOUR_ENV_PREFIX}` được chỉ định để xác định tên của Stack CloudFormation của bạn. Nếu bạn đang sử dụng tính năng [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), hãy thay thế bằng tên của môi trường cần di chuyển. Nếu không, thay thế bằng chuỗi rỗng.

### Bước 2: Cập nhật URL Kho lưu trữ (Khuyến nghị)

Kho lưu trữ đã được đổi tên từ `bedrock-claude-chat` thành `bedrock-chat`. Cập nhật kho lưu trữ cục bộ của bạn:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Bước 3: Đảm bảo Bạn đang ở Phiên bản V2 Mới nhất

> [!WARNING]
> Bạn PHẢI cập nhật lên v2.10.0 trước khi di chuyển lên V3. **Bỏ qua bước này có thể dẫn đến mất dữ liệu trong quá trình di chuyển.**

Trước khi bắt đầu di chuyển, hãy đảm bảo bạn đang chạy phiên bản V2 mới nhất (**v2.10.0**). Điều này đảm bảo bạn có tất cả các bản sửa lỗi và cải tiến cần thiết trước khi nâng cấp lên V3:

```bash
# Fetch the latest tags
git fetch --tags

# Checkout the latest V2 version
git checkout v2.10.0

# Deploy the latest V2 version
cd cdk
npm ci
npx cdk deploy --all
```

### Bước 4: Ghi lại Tên Bảng DynamoDB V2 của Bạn

Lấy tên ConversationTable V2 từ đầu ra CloudFormation:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Hãy đảm bảo lưu tên bảng này ở một vị trí an toàn, vì bạn sẽ cần nó cho tập lệnh di chuyển sau này.

### Bước 5: Sao lưu Bảng DynamoDB của Bạn

Trước khi tiếp tục, hãy tạo bản sao lưu của ConversationTable DynamoDB bằng tên bạn vừa ghi lại:

```bash
# Create a backup of your V2 table
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Check the backup status is available
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Bước 6: Xóa Tất cả API đã Xuất bản

> [!IMPORTANT]
> Trước khi triển khai V3, bạn phải xóa tất cả các API đã xuất bản để tránh xung đột giá trị đầu ra Cloudformation trong quá trình nâng cấp.

1. Đăng nhập vào ứng dụng với tư cách quản trị viên
2. Điều hướng đến phần Admin và chọn "API Management"
3. Xem lại danh sách tất cả các API đã xuất bản
4. Xóa từng API đã xuất bản bằng cách nhấp vào nút xóa bên cạnh nó

Bạn có thể tìm thêm thông tin về xuất bản và quản lý API trong tài liệu [PUBLISH_API.md](../PUBLISH_API_vi-VN.md), [ADMINISTRATOR.md](../ADMINISTRATOR_vi-VN.md) tương ứng.

### Bước 7: Kéo V3 và Triển khai

Kéo mã V3 mới nhất và triển khai:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Khi bạn triển khai V3, ứng dụng sẽ không khả dụng với tất cả người dùng cho đến khi quá trình di chuyển hoàn tất. Lược đồ mới không tương thích với định dạng dữ liệu cũ, vì vậy người dùng sẽ không thể truy cập bot hoặc cuộc hội thoại của họ cho đến khi bạn hoàn thành tập lệnh di chuyển trong các bước tiếp theo.

### Bước 8: Ghi lại Tên Bảng DynamoDB V3 của Bạn

Sau khi triển khai V3, bạn cần lấy cả tên ConversationTable và BotTable mới:

```bash
# Get the V3 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Get the V3 BotTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Hãy đảm bảo lưu các tên bảng V3 này cùng với tên bảng V2 đã lưu trước đó, vì bạn sẽ cần tất cả chúng cho tập lệnh di chuyển.

### Bước 9: Chạy Tập lệnh Di chuyển

Tập lệnh di chuyển sẽ chuyển đổi dữ liệu V2 của bạn sang lược đồ V3. Đầu tiên, chỉnh sửa tập lệnh di chuyển `docs/migration/migrate_v2_v3.py` để đặt tên bảng và vùng của bạn:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Sau đó chạy tập lệnh bằng Poetry từ thư mục backend:

> [!NOTE]
> Phiên bản yêu cầu Python đã được thay đổi thành 3.13.0 hoặc cao hơn (Có thể thay đổi trong phát triển tương lai. Xem pyproject.toml). Nếu bạn đã cài đặt venv với phiên bản Python khác, bạn sẽ cần xóa nó một lần.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies if you haven't already
poetry install

# Run a dry run first to see what would be migrated
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# If everything looks good, run the actual migration
poetry run python ../docs/migration/migrate_v2_v3.py

# Verify the migration was successful
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Tập lệnh di chuyển sẽ tạo một tệp báo cáo trong thư mục hiện tại của bạn với chi tiết về quá trình di chuyển. Kiểm tra tệp này để đảm bảo tất cả dữ liệu của bạn được di chuyển chính xác.

#### Xử lý Khối lượng Dữ liệu Lớn

Đối với môi trường có nhiều người dùng hoặc lượng dữ liệu lớn, hãy cân nhắc các cách tiếp cận sau:

1. **Di chuyển người dùng riêng lẻ**: Đối với người dùng có khối lượng dữ liệu lớn, di chuyển từng người một:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Cân nhắc về bộ nhớ**: Quá trình di chuyển tải dữ liệu vào bộ nhớ. Nếu bạn gặp lỗi Hết Bộ Nhớ (OOM), hãy thử:

   - Di chuyển từng người dùng một
   - Chạy di chuyển trên máy có nhiều bộ nhớ hơn
   - Chia nhỏ việc di chuyển thành các đợt người dùng nhỏ hơn

3. **Giám sát việc di chuyển**: Kiểm tra các tệp báo cáo được tạo để đảm bảo tất cả dữ liệu được di chuyển chính xác, đặc biệt là đối với các tập dữ liệu lớn.

### Bước 10: Xác minh Ứng dụng

Sau khi di chuyển, mở ứng dụng của bạn và xác minh:

- Tất cả bot của bạn đều khả dụng
- Các cuộc hội thoại được bảo toàn
- Các điều khiển quyền mới đang hoạt động

### Dọn dẹp (Tùy chọn)

Sau khi xác nhận rằng việc di chuyển đã thành công và tất cả dữ liệu của bạn có thể truy cập đúng cách trong V3, bạn có thể tùy chọn xóa bảng hội thoại V2 để tiết kiệm chi phí:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Chỉ xóa bảng V2 sau khi xác minh kỹ lưỡng rằng tất cả dữ liệu quan trọng của bạn đã được di chuyển thành công lên V3. Chúng tôi khuyên bạn nên giữ bản sao lưu đã tạo ở Bước 2 trong ít nhất vài tuần sau khi di chuyển, ngay cả khi bạn xóa bảng gốc.

## FAQ V3

### Truy cập Bot và Quyền hạn

**Q: Điều gì xảy ra nếu bot tôi đang sử dụng bị xóa hoặc quyền truy cập của tôi bị thu hồi?**
A: Việc xác thực được kiểm tra tại thời điểm chat, vì vậy bạn sẽ mất quyền truy cập ngay lập tức.

**Q: Điều gì xảy ra nếu một người dùng bị xóa (ví dụ: nhân viên nghỉ việc)?**
A: Dữ liệu của họ có thể được xóa hoàn toàn bằng cách xóa tất cả các mục từ DynamoDB với ID người dùng của họ làm khóa phân vùng (PK).

**Q: Tôi có thể tắt chia sẻ đối với một bot công khai thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi tắt chia sẻ.

**Q: Tôi có thể xóa một bot công khai thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi xóa.

### Bảo mật và Triển khai

**Q: Bảo mật cấp hàng (RLS) có được triển khai cho bảng bot không?**
A: Không, do sự đa dạng của các mẫu truy cập. Việc xác thực được thực hiện khi truy cập bot, và rủi ro rò rỉ metadata được coi là tối thiểu so với lịch sử hội thoại.

**Q: Yêu cầu để xuất bản một API là gì?**
A: Bot phải là công khai.

**Q: Có màn hình quản lý cho tất cả các bot riêng tư không?**
A: Không có trong phiên bản V3 ban đầu. Tuy nhiên, các mục vẫn có thể bị xóa bằng cách truy vấn với ID người dùng khi cần.

**Q: Có chức năng gắn thẻ bot để cải thiện trải nghiệm tìm kiếm không?**
A: Không có trong phiên bản V3 ban đầu, nhưng gắn thẻ tự động dựa trên LLM có thể được thêm vào trong các cập nhật tương lai.

### Quản trị

**Q: Quản trị viên có thể làm gì?**
A: Quản trị viên có thể:

- Quản lý bot công khai (bao gồm kiểm tra bot chi phí cao)
- Quản lý API
- Đánh dấu bot công khai là thiết yếu

**Q: Tôi có thể đánh dấu bot được chia sẻ một phần là thiết yếu không?**
A: Không, chỉ hỗ trợ bot công khai.

**Q: Tôi có thể đặt ưu tiên cho bot được ghim không?**
A: Không có trong phiên bản ban đầu.

### Cấu hình Xác thực

**Q: Làm thế nào để thiết lập xác thực?**
A:

1. Mở bảng điều khiển Amazon Cognito và tạo nhóm người dùng trong user pool BrChat
2. Thêm người dùng vào các nhóm này khi cần
3. Trong BrChat, chọn các nhóm người dùng bạn muốn cho phép truy cập khi cấu hình cài đặt chia sẻ bot

Lưu ý: Thay đổi thành viên nhóm yêu cầu đăng nhập lại để có hiệu lực. Các thay đổi được phản ánh khi làm mới token, nhưng không trong thời gian hiệu lực của ID token (mặc định 30 phút trong V3, có thể cấu hình bằng `tokenValidMinutes` trong `cdk.json` hoặc `parameter.ts`).

**Q: Hệ thống có kiểm tra với Cognito mỗi lần truy cập bot không?**
A: Không, việc xác thực được kiểm tra bằng token JWT để tránh các hoạt động I/O không cần thiết.

### Chức năng Tìm kiếm

**Q: Tìm kiếm bot có hỗ trợ tìm kiếm ngữ nghĩa không?**
A: Không, chỉ hỗ trợ tìm kiếm văn bản một phần. Tìm kiếm ngữ nghĩa (ví dụ: "ô tô" → "xe hơi", "xe điện", "phương tiện") không khả dụng do các hạn chế hiện tại của OpenSearch Serverless (tháng 3/2025).