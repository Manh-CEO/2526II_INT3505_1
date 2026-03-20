# 📚 API Documentation Standards Comparison & Demo

Dự án này là một bài tập thực hành chuyên sâu về các chuẩn định dạng API hiện đại, bao gồm **OpenAPI**, **API Blueprint**, **RAML**, và **TypeSpec**. Mục tiêu là giúp hiểu rõ cấu trúc, ưu nhược điểm và khả năng tự động hóa (sinh code/test) của từng loại.

---

## 📊 Bảng so sánh chi tiết 4 chuẩn API

| Tiêu chí | OpenAPI (Swagger) | API Blueprint | RAML | TypeSpec |
| :--- | :--- | :--- | :--- | :--- |
| **Định dạng** | YAML / JSON | Markdown (MSON) | YAML | Code (giống TypeScript) |
| **Đặc trưng** | Dựa trên JSON Schema | Hướng tới con người đọc | Hướng đối tượng (Traits) | Code-first, cực kỳ gọn |
| **Tooling** | Hệ sinh thái lớn nhất | Mạnh về Render HTML & Test | Tốt cho thiết kế Top-down | Hỗ trợ tốt từ Microsoft |
| **Tái sử dụng** | `$ref` | MSON | Traits, Resource Types | Decorators, Mixins |
| **Ứng dụng** | Standard cho REST API | Document & Test (Dredd) | Enterprise API Design | Modern Design & SDK Gen |

---

## 📂 Cấu trúc dự án & Nội dung Demo

Dự án được chia thành 4 khu vực tương ứng với 4 chuẩn, mỗi khu vực đều bao gồm file định nghĩa và hướng dẫn sử dụng công cụ đi kèm.

### 1. [OpenAPI (Swagger)](file:///d:/Work/project%20UET/2526II_INT3505_1/openapi)
- **File:** `openapi.yaml`
- **Demo:** Hướng dẫn sinh toàn bộ server Flask tự động chỉ với 1 dòng lệnh.

### 2. [API Blueprint](file:///d:/Work/project%20UET/2526II_INT3505_1/api-blueprint)
- **File:** `api.apib`
- **Demo:** Sử dụng **Aglio** để xem docs đẹp mắt và **Dredd** để tự động kiểm thử (contract testing).

### 3. [RAML](file:///d:/Work/project%20UET/2526II_INT3505_1/raml)
- **File:** `api.raml`
- **Demo:** Dựng Mock Server nhanh chóng bằng **Osprey** để frontend có thể tích hợp ngay.

### 4. [TypeSpec](file:///d:/Work/project%20UET/2526II_INT3505_1/typespec)
- **File:** `main.tsp`
- **Demo:** Cách tối giản hóa việc viết API và biên dịch (compile) sang OpenAPI chuẩn.

---

## 🚀 Cách chạy Demo sinh code/test

1. **Sinh code Flask từ OpenAPI:**
   ```bash
   cd openapi
   npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./generated-flask-server
   ```

2. **Chạy Mock Server từ RAML:**
   ```bash
   cd raml
   npx osprey-mock-service -r api.raml -p 3000
   ```

3. **Chạy Test tự động cho Blueprint:**
   ```bash
   cd api-blueprint
   npx dredd api.apib http://localhost:5000
   ```

---
*Lưu ý: Bạn cần cài đặt Node.js để chạy các lệnh `npx` trên.*
