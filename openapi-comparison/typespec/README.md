# TypeSpec Demo

Thư mục này chứa file định nghĩa API chuẩn TypeSpec hiện đại của Microsoft.

## 1. File định nghĩa
- `main.tsp`: Viết API theo phong cách TypeScript code, cực kỳ ngắn gọn và có tính kế thừa cao.

## 2. Demo Compile ra OpenAPI
TypeSpec không sinh code trực tiếp mà thường được dùng để thiết kế, sau đó "compile" ra OpenAPI để tận dụng hệ sinh thái của OpenAPI.

**Lệnh cài đặt compiler:**
```bash
npm install
```

**Lệnh biên dịch:**
```bash
npx tsp compile . --emit @typespec/openapi3
```

Sau khi chạy lệnh trên, Tool sẽ tạo ra thư mục `tsp-output` chứa file `openapi.yaml` (hoặc tạo file `openapi.yaml` tùy cấu hình). 

## 3. Demo Sinh Server Code (Flask)
Dù TypeSpec không sinh code ứng dụng trực tiếp, bạn có thể biến file OpenAPI vừa tạo thành Server Code dễ dàng:

```bash
npx @openapitools/openapi-generator-cli generate -i tsp-output/@typespec/openapi3/openapi.yaml -g python-flask -o ./generated-flask-server
```
*(Nếu openapi.yaml của bạn ở đường dẫn khác, hãy đổi tham số `-i`)*
