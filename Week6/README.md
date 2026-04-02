# Báo cáo Thực hành Tuần 6

## 1. So sánh JWT và OAuth 2.0

*   **JWT (JSON Web Token):**
    *   **Bản chất:** Là một định dạng token (chuẩn RFC 7519) dùng để mã hóa và truyền tải thông tin định danh một cách an toàn.
    *   **Đặc điểm:** Stateless (phi trạng thái) - server không cần lưu trữ session. Thông tin (claims) nằm sẵn trong payload của token chữ ký.
    *   **Ứng dụng:** Chủ yếu dùng cho Authentication (Xác thực) phân tán, đặc biệt là giữa Single Page Apps (SPA) / Mobile Apps và APIs.

*   **OAuth 2.0:**
    *   **Bản chất:** Là một **framework giao thức ủy quyền (Authorization)**. Định nghĩa luồng để mượn quyền, không quy định cụ thể format token (tuy nhiên thực tế thường dùng JWT làm Access Token).
    *   **Đặc điểm:** Cho phép một ứng dụng bên thứ 3 (Ví dụ App của bạn) truy cập vào tài nguyên của người dùng (Ví dụ thông tin tài khoản Facebook) mà không cần giao mật khẩu cho App.
    *   **Ứng dụng:** Delegation/Authorization (Uỷ quyền), ví dụ: "Login with Google/Facebook", OpenID Connect.

---

## 2. Các khái niệm cốt lõi

*   **Bearer token:** Giao thức xác thực HTTP thiết kế cho OAuth 2.0, token thường được để trong Header với từ khóa `Bearer`. Nếu ai đó đánh cắp được chuỗi token này, họ sẽ có quyền sử dụng API như người nắm giữ vé (bearer) hợp pháp.
*   **Refresh token:** Một token phụ có tuổi thọ (expiration) dài. Nó được dùng để lấy lại/làm mới một Access Token khi thẻ này hết hạn. Cơ chế này giúp giữ nguyên trải nghiệm dài hạn cho người dùng nhưng rất an toàn vì Access Token (hay bị lộ do trao đổi nhiều) bị thay mới liên tục.
*   **Scopes:** Giới hạn phạm vi quyền (ví dụ `read:users`, `write:posts`) trên token. Ứng dụng chỉ có thể truy cập những API map đúng với Scope đã cấp.
*   **Roles:** Phân quyền theo vai trò chức danh của user (ví dụ `admin`, `user`). Dùng để xác định ranh giới tính năng dựa vào từng nhóm chức danh.

---

## 3. Phân tích rủi ro bảo mật & Security Audit

Trong API Audit hiện nay có 2 lỗ hổng kinh điển phải khắc phục:

### 3.1. Token Leakage (Rò rỉ token)
*   **Vấn đề / Phát hiện:** Token nằm trong URL Parameter (`https://api.domain.com/v1/auth?token=abc...`). Thông tin này dễ dàng bị ghi vào Browser History, Proxy Cache, hoặc Server Access Logs.
*   **Cách khắc phục:** 
    *   Luôn yêu cầu truyền/cấp token thông qua HTTP Headers (vd: `Authorization: Bearer <token>`).
    *   Nên ép HTTPS để encrypt request.
    *(Tham khảo: API Demo cố tình có 1 route bị lỗi bảo mật này)*.

### 3.2. Replay Attack (Tấn công phát lại)
*   **Vấn đề / Phát hiện:** Token cấp ra không có hạn sử dụng hoặc hạn sử dụng vĩnh viễn. Kẻ xấu lấy trộm được và phát lại (replay) các gói tin trái phép vĩnh viễn lúc nào cũng được.
*   **Cách khắc phục:**
    *   Luôn gắn thời gian hết hạn (`exp`) cực ngắn (15-30 phút) trên Access Token.
    *   Dùng Refresh Token cho mục đích sử dụng lâu dài và bắt phải đăng nhập lại hoặc revoke Refresh Token nếu phát hiện bất thường.

---

## 4. Hướng dẫn chạy Backend Demo (Python / Flask)

1. Cài đặt môi trường thư viện:
   ```bash
   cd jwt-flask
   python -m venv venv
   # Kích hoạt venv (Với Windows)
   venv\Scripts\activate
   # (Với Mac/Linux): source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Chạy server Flask:
   ```bash
   python app.py
   ```

**Các REST API Endpoints Demo:**
*   `POST /api/login`: Truyền JSON `{"username": "admin", "password": "password"}`. Cấp JWT Access Token và Refresh Token.
*   `POST /api/refresh`: Truyền JSON `{"token": "<refresh_token>"}` để xin cấp token mới.
*   `GET /api/protected`: Gửi header `Authorization: Bearer <access_token>`. Check xác thực.
*   `GET /api/admin`: Kiểm tra phân quyền RBAC Role của `admin`.
*   `GET /api/leak-demo?token="xxx"`: Endpoint mô phỏng lỗ hổng Token Leakage.
