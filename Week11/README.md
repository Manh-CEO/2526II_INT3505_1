# Week 11 - API Design Patterns

## 1. Mục tiêu kiến thức
Tuần này tập trung vào các mô hình thiết kế API phổ biến, giúp hệ thống API trở nên linh hoạt, dễ mở rộng và chuẩn hóa theo quy trình phát triển phần mềm chuyên nghiệp.

### Các Design Patterns chính:
1. **CRUD Pattern**: Mô hình cơ bản nhất (Create, Read, Update, Delete) dựa trên việc ánh xạ trực tiếp với các HTTP Verbs (`POST`, `GET`, `PUT`, `DELETE`).
2. **Query Pattern**: Cơ chế cho phép lọc (filtering), tìm kiếm (searching), và phân trang (pagination) các tập dữ liệu phức tạp thông qua Query Parameters (Ví dụ: `?status=paid&item=laptop`).
3. **HATEOAS (Hypermedia as the Engine of Application State)**: API tự mô tả (self-describing) bằng cách trả về các liên kết định hướng (`links`) trong response, giúp Client biết được các hành động hợp lệ tiếp theo (Tiêu biểu là Stripe API).
4. **Event-driven & Webhook**:
    * **Event-driven**: Kiến trúc hệ thống phản ứng bất đồng bộ (async) dựa trên sự kiện (Ví dụ: Đơn hàng chuyển sang trạng thái `paid` sẽ kích hoạt sự kiện gửi email).
    * **Webhook (Inversion of Control)**: Cơ chế API chủ động "đẩy" (HTTP POST) dữ liệu sang hệ thống bên thứ ba khi có sự kiện xảy ra, giải quyết triệt để bài toán lãng phí tài nguyên của Polling Pattern.

---

## 2. Phân tích API Patterns trong thực tế

### Stripe API (Master of HATEOAS & Webhooks)
* **Resource-based**: Stripe tổ chức cấu trúc tài nguyên cực kỳ chặt chẽ và nhất quán.
* **HATEOAS**: Khi khởi tạo một `PaymentIntent`, Stripe sẽ trả về các URL trong object `next_action` để Client biết chính xác cần điều hướng (redirect) người dùng đi đâu để xác thực 3D-Secure.
* **Webhooks**: Thay vì bắt Client phải Polling liên tục để check trạng thái, Stripe dùng Webhook nhằm thông báo ngay khi sự kiện thanh toán thành công diễn ra.

### GitHub API (REST vs GraphQL)
* **REST API**: Cung cấp các endpoint tường minh tới từng tài nguyên độc lập (`/users`, `/repos`, `/issues`).
* **GraphQL API**: GitHub cung cấp thêm cổng GraphQL song song để giải quyết triệt để bài toán hiệu năng: **Over-fetching** (lấy thừa dữ liệu không dùng) và **Under-fetching** (lấy thiếu dữ liệu dẫn đến n+1 requests).
* **Pattern**: Sử dụng "Preview Headers" (VD: `application/vnd.github.v3+json`) để thử nghiệm các tính năng mới (Beta) mà không làm ảnh hưởng (breaking changes) đến các Client đang chạy phiên bản cũ.

---

## 3. Demo thực hành (FastAPI)

### Cài đặt môi trường
```bash
cd Week11
pip install -r requirements.txt
