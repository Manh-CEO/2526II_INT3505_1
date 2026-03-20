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
npx tsp compile .
```

Sau khi chạy lệnh trên, Tool sẽ tạo ra thư mục `tsp-output` chứa file `openapi.yaml`. Bạn có thể dùng file đó để sinh code/test như thư mục `/openapi`.
