# API Blueprint Demo

Thư mục này chứa file định nghĩa API chuẩn Blueprint (Markdown) và hướng dẫn sinh test tự động.

## 1. File định nghĩa
- `api.apib`: Chứa cấu trúc API của hệ thống Library Management viết bằng Markdown.

## 2. Cách xem (Aglio)
Để render file `.apib` ra giao diện HTML đẹp mắt, bạn có thể dùng Aglio:

```bash
npx aglio -i api.apib -o api.html
```

## 3. Demo Sinh Test (Dredd)
Dredd là công cụ mạnh mẽ nhất của hệ sinh thái Blueprint để kiểm tra xem server của bạn có tuân thủ đúng định nghĩa hay không.

**Lệnh chạy test:**
```bash
npx dredd api.apib http://localhost:5000
```

Dredd sẽ tự động đọc các ví dụ (examples) trong file `.apib` và bắn request lên server để so sánh kết quả trả về.

## 4. Demo Sinh Server Code (Flask)
Tuy API Blueprint không hỗ trợ trực tiếp sinh server code, ta có thể convert sang OpenAPI để sinh code nhờ sự hỗ trợ của cộng đồng.

**Bước 1: Chuyển đổi sang `openapi.yaml`:**
```bash
npx apib2swagger -i api.apib -o openapi.yaml
```

**Bước 2: Sinh mã nguồn Flask Server:**
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-flask-server
```
