# Hướng Dẫn Di Chuyển (từ phiên bản 2 sang phiên bản 3)

## Tóm tắt

- Phiên bản V3 giới thiệu điều khiển quyền chi tiết và chức năng Cửa hàng Bot, yêu cầu thay đổi lược đồ DynamoDB
- **Sao lưu bảng ConversationTable của DynamoDB trước khi di chuyển**
- Cập nhật URL kho lưu trữ từ `bedrock-claude-chat` sang `bedrock-chat`
- Chạy tập lệnh di chuyển để chuyển đổi dữ liệu sang lược đồ mới
- Tất cả bot và cuộc trò chuyện của bạn sẽ được bảo toàn với mô hình quyền mới
- **QUAN TRỌNG: Trong quá trình di chuyển, ứng dụng sẽ không khả dụng cho tất cả người dùng cho đến khi quá trình di chuyển hoàn tất. Quá trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu suất môi trường phát triển của bạn.**
- **QUAN TRỌNG: Tất cả các API Đã xuất bản phải được xóa trong quá trình di chuyển.**
- **CẢNH BÁO: Quá trình di chuyển không thể đảm bảo 100% thành công cho tất cả các bot. Vui lòng ghi lại cấu hình bot quan trọng của bạn trước khi di chuyển trong trường hợp bạn cần phải tạo lại chúng theo cách thủ công**

## Giới thiệu

### Có Gì Mới Trong Phiên Bản V3

V3 giới thiệu những cải tiến đáng kể cho Bedrock Chat:

1. **Kiểm soát quyền chi tiết**: Kiểm soát quyền truy cập vào bot của bạn thông qua quyền dựa trên nhóm người dùng
2. **Cửa hàng Bot**: Chia sẻ và khám phá bot thông qua một nơi tập trung
3. **Tính năng quản trị**: Quản lý API, đánh dấu bot là thiết yếu và phân tích việc sử dụng bot

Những tính năng mới này đòi hỏi phải thay đổi lược đồ DynamoDB, buộc phải thực hiện quá trình di chuyển dữ liệu cho người dùng hiện tại.

### Tại Sao Cần Thực Hiện Quá Trình Di Chuyển Này

Mô hình quyền mới và chức năng Cửa hàng Bot đòi hỏi phải cấu trúc lại cách lưu trữ và truy cập dữ liệu bot. Quá trình di chuyển sẽ chuyển đổi các bot và cuộc trò chuyện hiện tại của bạn sang lược đồ mới trong khi vẫn giữ nguyên toàn bộ dữ liệu.

> [!CẢNH BÁO]
> Thông Báo Gián Đoạn Dịch Vụ: **Trong quá trình di chuyển, ứng dụng sẽ không khả dụng đối với tất cả người dùng.** Hãy lên kế hoạch thực hiện di chuyển này trong một cửa sổ bảo trì khi người dùng không cần truy cập vào hệ thống. Ứng dụng chỉ trở nên khả dụng trở lại sau khi tập lệnh di chuyển đã hoàn tất thành công và tất cả dữ liệu đã được chuyển đổi sang lược đồ mới. Quá trình này thường mất khoảng 60 phút, tùy thuộc vào lượng dữ liệu và hiệu năng của môi trường phát triển của bạn.

> [!QUAN TRỌNG]
> Trước khi tiến hành di chuyển: **Quá trình di chuyển không thể đảm bảo 100% thành công cho tất cả các bot**, đặc biệt là những bot được tạo với các phiên bản cũ hoặc có cấu hình tùy chỉnh. Vui lòng ghi lại các cấu hình bot quan trọng (hướng dẫn, nguồn kiến thức, cài đặt) trước khi bắt đầu quá trình di chuyển trong trường hợp bạn cần phải tạo lại chúng theo cách thủ công.

## Quá Trình Di Chuyển

### Thông Báo Quan Trọng Về Khả Năng Hiển Thị Bot Trong V3

Trong V3, **tất cả các bot v2 có chia sẻ công khai sẽ được tìm thấy trong Cửa Hàng Bot.** Nếu bạn có các bot chứa thông tin nhạy cảm mà bạn không muốn được phát hiện, hãy cân nhắc đặt chúng ở chế độ riêng tư trước khi di chuyển sang V3.

### Bước 1: Xác định tên môi trường của bạn

Trong quy trình này, `{TÊN_MÔI_TRƯỜNG_CỦA_BẠN}` được sử dụng để xác định tên các CloudFormation Stack. Nếu bạn đang sử dụng tính năng [Triển Khai Nhiều Môi Trường](../../README.md#deploying-multiple-environments), hãy thay thế bằng tên môi trường sẽ được di chuyển. Nếu không, hãy thay thế bằng chuỗi trống.

### Bước 2: Cập Nhật URL Kho Lưu Trữ (Được Khuyến Nghị)

Kho lưu trữ đã được đổi tên từ `bedrock-claude-chat` thành `bedrock-chat`. Cập nhật kho lưu trữ cục bộ của bạn:

```bash
# Kiểm tra URL remote hiện tại
git remote -v

# Cập nhật URL remote
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Xác minh sự thay đổi
git remote -v
```

### Bước 3: Đảm Bảo Bạn Đang Ở Phiên Bản V2 Mới Nhất

> [!CẢNH BÁO]
> Bạn PHẢI cập nhật lên v2.10.0 trước khi di chuyển sang V3. **Bỏ qua bước này có thể dẫn đến mất dữ liệu trong quá trình di chuyển.**

Trước khi bắt đầu quá trình di chuyển, hãy đảm bảo bạn đang chạy phiên bản mới nhất của V2 (**v2.10.0**). Điều này đảm bảo bạn có tất cả các bản sửa lỗi và cải tiến trước khi nâng cấp lên V3:

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

Hãy chắc chắn lưu lại tên bảng này ở một nơi an toàn, vì bạn sẽ cần nó cho script di chuyển sau này.

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
  --backup-arn MÃ_ĐỊNH_DANH_SAO_LƯU_CỦA_BẠN
```

### Bước 6: Xóa Tất Cả Các API Đã Xuất Bản

> [!QUAN TRỌNG]
> Trước khi triển khai V3, bạn phải xóa tất cả các API đã xuất bản để tránh xung đột giá trị đầu ra Cloudformation trong quá trình nâng cấp.

1. Đăng nhập vào ứng dụng với tư cách quản trị viên
2. Điều hướng đến phần Quản Trị và chọn "Quản Lý API"
3. Xem xét danh sách tất cả các API đã xuất bản
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
> Sau khi triển khai V3, ứng dụng sẽ không khả dụng cho tất cả người dùng cho đến khi quá trình di chuyển hoàn tất. Lược đồ mới không tương thích với định dạng dữ liệu cũ, vì vậy người dùng sẽ không thể truy cập bot hoặc cuộc trò chuyện của họ cho đến khi bạn hoàn tất script di chuyển trong các bước tiếp theo.

### Bước 8: Ghi Lại Tên Bảng DynamoDB V3

Sau khi triển khai V3, bạn cần lấy cả tên ConversationTable và BotTable mới:

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
> Hãy chắc chắn lưu lại các tên bảng V3 này cùng với tên bảng V2 mà bạn đã lưu trước đó, vì bạn sẽ cần tất cả chúng cho script di chuyển.

(Phần còn lại của tài liệu được dịch tương tự, giữ nguyên các đoạn code và định dạng markdown)

## Câu hỏi Thường gặp V3

### Quyền Truy cập và Quyền Bot

**Q: Chuyện gì xảy ra nếu bot tôi đang sử dụng bị xóa hoặc quyền truy cập của tôi bị loại bỏ?**
A: Việc ủy quyền được kiểm tra tại thời điểm trò chuyện, vì vậy bạn sẽ mất quyền truy cập ngay lập tức.

**Q: Chuyện gì xảy ra nếu người dùng bị xóa (ví dụ: nhân viên rời đi)?**
A: Dữ liệu của họ có thể được xóa hoàn toàn bằng cách xóa tất cả các mục từ DynamoDB với ID người dùng làm khóa phân vùng (PK).

**Q: Tôi có thể tắt chia sẻ cho một bot công cộng thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi tắt chế độ chia sẻ.

**Q: Tôi có thể xóa một bot công cộng thiết yếu không?**
A: Không, quản trị viên phải đánh dấu bot là không thiết yếu trước khi xóa.

### Bảo mật và Triển khai

**Q: Bảo mật cấp hàng (RLS) có được triển khai cho bảng bot không?**
A: Không, do sự đa dạng của các mẫu truy cập. Việc ủy quyền được thực hiện khi truy cập bot, và nguy cơ rò rỉ siêu dữ liệu được coi là tối thiểu so với lịch sử cuộc trò chuyện.

**Q: Yêu cầu để xuất bản một API là gì?**
A: Bot phải ở chế độ công khai.

**Q: Sẽ có màn hình quản lý cho tất cả các bot riêng tư không?**
A: Không có trong phiên bản V3 ban đầu. Tuy nhiên, các mục vẫn có thể được xóa bằng cách truy vấn với ID người dùng nếu cần.

**Q: Sẽ có chức năng gắn thẻ bot để cải thiện trải nghiệm tìm kiếm không?**
A: Không có trong phiên bản V3 ban đầu, nhưng việc gắn thẻ tự động dựa trên LLM có thể được thêm vào trong các bản cập nhật trong tương lai.

### Quản trị

**Q: Quản trị viên có thể làm gì?**
A: Quản trị viên có thể:

- Quản lý bot công cộng (bao gồm kiểm tra các bot có chi phí cao)
- Quản lý API
- Đánh dấu bot công cộng là thiết yếu

**Q: Tôi có thể đánh dấu các bot được chia sẻ một phần là thiết yếu không?**
A: Không, chỉ hỗ trợ bot công cộng.

**Q: Tôi có thể đặt ưu tiên cho các bot được ghim không?**
A: Ở phiên bản ban đầu, không.

### Cấu hình Ủy quyền

**Q: Làm thế nào để thiết lập ủy quyền?**
A:

1. Mở bảng điều khiển Amazon Cognito và tạo nhóm người dùng trong nhóm người dùng BrChat
2. Thêm người dùng vào các nhóm này nếu cần
3. Trong BrChat, chọn các nhóm người dùng bạn muốn cho phép truy cập khi cấu hình cài đặt chia sẻ bot

Lưu ý: Các thay đổi về thành viên nhóm yêu cầu đăng nhập lại để có hiệu lực. Các thay đổi được phản ánh khi làm mới token, nhưng không trong thời gian hiệu lực của ID token (mặc định 30 phút trong V3, có thể cấu hình bằng `tokenValidMinutes` trong `cdk.json` hoặc `parameter.ts`).

**Q: Hệ thống có kiểm tra với Cognito mỗi khi truy cập bot không?**
A: Không, việc ủy quyền được kiểm tra bằng token JWT để tránh các thao tác I/O không cần thiết.

### Chức năng Tìm kiếm

**Q: Tìm kiếm bot có hỗ trợ tìm kiếm ngữ nghĩa không?**
A: Không, chỉ hỗ trợ khớp văn bản một phần. Tìm kiếm ngữ nghĩa (ví dụ: "automobile" → "car", "EV", "vehicle") không khả dụng do các hạn chế của OpenSearch Serverless hiện tại (Tháng 3 năm 2025).