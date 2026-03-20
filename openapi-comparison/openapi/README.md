# OpenAPI (Swagger) Demo

Thư mục này chứa file định nghĩa API chuẩn OpenAPI 3.0 và hướng dẫn sinh code tự động.

## 1. File định nghĩa
- `openapi.yaml`: Chứa toàn bộ cấu trúc API của hệ thống Library Management.

## 2. Cách xem (Swagger UI)
Bạn có thể copy nội dung file `openapi.yaml` và dán vào [Swagger Editor](https://editor.swagger.io/) để xem giao diện trực quan.

## 3. Demo Sinh Code Flask (Python)
Để sinh code server Flask từ file này, hãy chạy lệnh sau:

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-flask-server
```

**Kết quả:** Tool sẽ tự động tạo ra một thư mục `generated-flask-server` chứa đầy đủ boilerplate code, models, và routes cho API của bạn.
