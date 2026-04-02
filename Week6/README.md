# Báo cáo Thực hành Tuần 6

## 1. So sánh JWT và OAuth 2.0

*   **JWT (JSON Web Token):**
    *   **Bản chất:** Là một chuẩn mở (RFC 7519) định nghĩa cách truyền thông tin an toàn giữa các bên dưới dạng JSON format. Nó thường được sử dụng như một **token format** (định dạng token).
    *   **Đặc điểm:** Stateless (phi trạng thái) - server không cần lưu trữ session. Thông tin auth (claims) được mã hóa và chèn trực tiếp vào payload.
    *   **Ứng dụng:** Chủ yếu dùng cho Authentication (Xác thực) giữa client và server nội bộ (Single Page Apps, Microservices).

*   **OAuth 2.0:**
    *   **Bản chất:** Là một **framework/protocol** (giao thức) ủy quyền (Authorization). Nó không định nghĩa cụ thể format của token (mặc dù thường sử dụng JWT làm token).
    *   **Đặc điểm:** Cho phép một ứng dụng bên thứ 3 truy cập vào tài nguyên của người dùng mà không cần biết mật khẩu của họ (vd: Đăng nhập bằng Google/Facebook).
    *   **Ứng dụng:** Chủ yếu dùng cho Delegation/Authorization (Ủy quyền phân quyền) giữa các server/hệ thống khác nhau (Third-party integrations).

**Tóm tắt:** JWT là cái *căn cước công dân* của bạn (để chứng minh bạn là ai), trong khi OAuth 2.0 là *quy trình* quản lý cách cấp và kiểm tra giấy phép vào cổng (bạn được phép làm gì).

---

## 2. Các khái niệm cốt lõi

*   **Bearer token:** Là một chuỗi mã xác thực tĩnh được cấp bởi Authorization Server. Trong HTTP Request, token thường được gửi trong header dưới dạng `Authorization: Bearer <token>`. Nếu ai đó đánh cắp được chuỗi này, họ có quyền sử dụng tài nguyên (như người mang vé - "bearer").
*   **Refresh token:** Là một token đặc biệt, thường có tuổi thọ (expiration) dài hơn Access Token. Nó dùng để lấy một Access Token mới khi Access Token cũ đã hết hạn, giúp người dùng không phải đăng nhập lại nhiều lần mà vẫn đảm bảo an toàn vì Access Token bị thay mới liên tục.
*   **Scopes:** Định nghĩa phạm vi quyền hạn (permissions) mà một token có. Ví dụ: `read:users`, `write:articles`. Ứng dụng client chỉ có thể thao tác với tài nguyên nằm trong *scopes* của token đang sở hữu.
*   **Roles:** Vai trò của người dùng trong hệ thống (vd: `Admin`, `User`, `Moderator`). Thường được sử dụng tích hợp trong RBAC (Role-Based Access Control) để quyết định người dùng được làm gì. *Scopes có thể dựa trên Roles để cấp.*

---

## 3. Phân tích rủi ro bảo mật và cách khắc phục

Quá trình thực hành Security Audit API, chúng ta cần phát hiện và xử lý các lỗi sau:

### 3.1. Token Leakage (Rò rỉ token)
*   **Mô tả:** Token bị lộ thông qua URL parameters (vd: `/?token=abc`), lưu ở localStorage/sessionStorage dễ bị XSS tấn công, hoặc không mã hóa HTTPS khi truyền tải.
*   **Khắc phục:**
    *   Luôn gửi token thông qua HTTP Header (`Authorization: Bearer <token>`).
    *   Luôn dùng HTTPS.
    *   Nên lưu trữ bằng **HttpOnly & Secure Cookies** thay vì localStorage để ngăn chặn XSS (hoặc dùng token thời gian rất ngắn trên bộ nhớ).

### 3.2. Replay Attack (Tấn công phát lại)
*   **Mô tả:** Hacker chặn bắt (sniff) Request (bao gồm cả token) và gửi lại y hệt để chiếm quyền thao tác (mặc dù họ không phân tích được Payload của JWT do không có secret key).
*   **Khắc phục:**
    *   Sử dụng JWT với thời gian sống (TTL - Time To Live) cực ngắn cho Access Token (ví dụ 10-15 phút).
    *   Cấu hình Rotate Refresh Token (mỗi khi dùng refresh token đổi lấy access token mới, refresh token cũ bị thu hồi/đổi mới).
    *   Kiểm tra JTI (JWT ID) để chống dùng lại token cũ cho các hành động đòi hỏi 1 lần (one-time logic).

---

## 4. Hướng dẫn chạy Backend Demo

1. Chuyển thư mục: `cd jwt-backend`
2. Cài đặt dependencies: `npm install`
3. Chạy môi trường dev: `node server.js`

**Các API Endpoint:**
*   `POST /api/login`: Đăng nhập, nhận Access và Refresh Token.
*   `POST /api/refresh`: Làm mới Access Token.
*   `GET /api/protected`: Endpoint yêu cầu Bearer token trong Headers.
*   `GET /api/admin`: Endpoint yêu cầu role admin.

---

*(Tài liệu tham khảo tham chiếu thiết kế JWT từ JJ Geewax – Chapter 5 liên quan đến Standard/Custom API behaviors and security practices).*
