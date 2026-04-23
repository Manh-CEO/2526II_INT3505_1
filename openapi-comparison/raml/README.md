# RAML Demo

Thư mục này chứa file định nghĩa API chuẩn RAML 1.0 và hướng dẫn dựng Mock Server.

## 1. File định nghĩa
- `api.raml`: Chứa cấu trúc API hệ thống Library Management. RAML cực kỳ mạnh trong việc thiết kế API từ trên xuống (top-down).

## 2. Demo Mock Server (Osprey)
Bạn có thể nhanh chóng dựng một server giả lập (Mock) từ file RAML để frontend có thể code ngay lập tức:

```bash
npx osprey-mock-service -f api.raml -p 3000
```

Lệnh này sẽ tạo ra một server chạy tại port 3000, tự động trả về dữ liệu mẫu dựa trên các `types` bạn đã định nghĩa.

## 3. Demo Sinh Server Code (Flask)
Tương tự Blueprint, ta có thể sử dụng sức mạnh của OpenAPI để sinh code từ RAML thông qua việc chuyển đổi (convert).

**Bước 1: Chuyển đổi sang `openapi.yaml`:**
```bash
npx oas-raml-converter --from RAML --to OAS30 api.raml > openapi.yaml
```

**Bước 2: Sinh mã nguồn Flask Server:**
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-flask-server
```
