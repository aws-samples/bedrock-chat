# Xuất Bản API

## Tổng quan

Mẫu này bao gồm một tính năng để xuất bản các API. Mặc dù giao diện chat có thể thuận tiện cho việc xác thực sơ bộ, nhưng việc triển khai thực tế phụ thuộc vào trường hợp sử dụng cụ thể và trải nghiệm người dùng (UX) mong muốn cho người dùng cuối. Trong một số trường hợp, giao diện chat có thể là lựa chọn ưu tiên, trong khi ở những trường hợp khác, API độc lập có thể phù hợp hơn. Sau khi xác thực ban đầu, mẫu này cung cấp khả năng xuất bản các bot được tùy chỉnh theo nhu cầu của dự án. Bằng cách nhập các cài đặt cho hạn ngạch, giới hạn tốc độ, nguồn gốc, v.v., một điểm cuối có thể được xuất bản cùng với một khóa API, mang lại tính linh hoạt cho các tùy chọn tích hợp đa dạng.

## Bảo mật

Việc sử dụng chỉ một khóa API không được khuyến nghị như được mô tả trong: [Hướng dẫn Nhà phát triển AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Do đó, mẫu này triển khai một hạn chế địa chỉ IP đơn giản thông qua AWS WAF. Quy tắc WAF được áp dụng chung trên ứng dụng do các cân nhắc về chi phí, với giả định rằng các nguồn mà người ta muốn hạn chế có khả năng giống nhau trên tất cả các API được phát hành. **Vui lòng tuân thủ chính sách bảo mật của tổ chức bạn cho việc triển khai thực tế.** Cũng xem phần [Kiến trúc](#architecture).

## Cách xuất bản API bot tùy chỉnh

### Điều kiện tiên quyết

Vì lý do quản trị, chỉ một số người dùng hạn chế mới có thể xuất bản bot. Trước khi xuất bản, người dùng phải là thành viên của nhóm được gọi là `PublishAllowed`, có thể được thiết lập thông qua bảng điều khiển quản lý > Amazon Cognito User pools hoặc aws cli. Lưu ý rằng ID nhóm người dùng có thể được tham chiếu bằng cách truy cập CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Cài đặt Xuất bản API

Sau khi đăng nhập với tư cách người dùng `PublishedAllowed` và tạo bot, hãy chọn `API PublishSettings`. Lưu ý rằng chỉ có bot được chia sẻ mới có thể được xuất bản.
![](./imgs/bot_api_publish_screenshot.png)

Trên màn hình tiếp theo, chúng ta có thể cấu hình một số tham số liên quan đến giới hạn tốc độ. Để biết chi tiết, vui lòng xem thêm: [Giới hạn yêu cầu API để cải thiện thông lượng](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Sau khi triển khai, màn hình sau sẽ xuất hiện nơi bạn có thể lấy URL điểm cuối và khóa API. Chúng ta cũng có thể thêm và xóa khóa API.

![](./imgs/bot_api_publish_screenshot3.png)

## Kiến trúc

API được xuất bản theo sơ đồ sau:

![](./imgs/published_arch.png)

WAF được sử dụng để hạn chế địa chỉ IP. Địa chỉ có thể được cấu hình bằng cách đặt các tham số `publishedApiAllowedIpV4AddressRanges` và `publishedApiAllowedIpV6AddressRanges` trong `cdk.json`.

Khi người dùng nhấp vào xuất bản bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) sẽ khởi chạy tác vụ triển khai CDK để cung cấp ngăn xếp API (Xem thêm: [Định nghĩa CDK](../cdk/lib/api-publishment-stack.ts)) bao gồm API Gateway, Lambda và SQS. SQS được sử dụng để tách rời yêu cầu người dùng và hoạt động LLM vì việc tạo đầu ra có thể vượt quá 30 giây, là giới hạn của hạn ngạch API Gateway. Để tìm nạp đầu ra, cần truy cập API một cách không đồng bộ. Để biết thêm chi tiết, xem [Đặc tả API](#api-specification).

Máy khách cần đặt `x-api-key` trong tiêu đề yêu cầu.

## Thông số kỹ thuật API

Xem [tại đây](https://aws-samples.github.io/bedrock-chat).