# Week 10 - Deploy Production API, Observability, Rate Limiting

## 1. Mục tiêu kiến thức

Demo này giúp hiểu cách chuẩn bị một API khi đưa lên môi trường production.

Các nội dung chính:

- Deploy API lên môi trường production.
- Thiết lập observability gồm:
  - Logging: ghi lại request, lỗi, thời gian xử lý.
  - Metrics: xuất số liệu cho Prometheus.
  - Tracing cơ bản: theo dõi request đi qua hệ thống bằng log thời gian xử lý.
- Thiết lập bảo mật production:
  - HTTP security headers bằng Helmet.
  - Rate limiting để chống spam request.
  - Audit logs để biết ai gọi API, gọi lúc nào, kết quả ra sao.

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| API server | Express.js | Xây dựng REST API |
| Logging | Winston | Ghi log request và lỗi |
| Metrics | prom-client | Xuất metrics theo chuẩn Prometheus |
| Rate limit | express-rate-limit | Giới hạn số request của mỗi IP |
| Security headers | Helmet | Tăng bảo mật HTTP headers |

## 3. Cấu trúc thư mục

```text
Week10/
├── package.json
├── README.md
├── .gitignore
├── logs/
│   ├── combined.log
│   └── error.log
└── src/
    └── app.js
```

## 4. Cài đặt và chạy demo

Di chuyển vào thư mục Week10:

```bash
cd Week10
```

Cài thư viện:

```bash
npm install
```

Chạy server:

```bash
npm start
```

Server chạy tại:

```text
http://localhost:3000
```

## 5. Các endpoint demo

### 5.1 Trang giới thiệu

```http
GET /
```

Dùng để kiểm tra server đã chạy.

### 5.2 API chính có rate limiting

```http
GET /api/data
```

Kết quả mẫu:

```json
{
  "message": "Đây là dữ liệu từ API đã được bảo mật và giám sát!",
  "timestamp": "2026-05-14T08:00:00.000Z"
}
```

Endpoint này được áp dụng rate limit.

Mặc định:

```text
100 request / 15 phút / 1 IP
```

Nếu gọi quá nhiều lần, API trả về:

```json
{
  "status": 429,
  "message": "Quá nhiều request từ IP này, vui lòng thử lại sau 15 phút."
}
```

### 5.3 Endpoint metrics cho Prometheus

```http
GET /metrics
```

Endpoint này xuất metrics như:

```text
http_request_duration_seconds_bucket
http_request_duration_seconds_count
process_cpu_user_seconds_total
nodejs_heap_size_used_bytes
```

Prometheus có thể scrape endpoint này để theo dõi hiệu năng API.

### 5.4 Endpoint tạo lỗi để xem log

```http
GET /api/error
```

Endpoint này cố tình trả về lỗi `500` để kiểm tra logging.

## 6. Demo cho người khác dễ hiểu

Khi thuyết trình, có thể demo theo thứ tự sau:

### Bước 1: Chạy server

```bash
npm start
```

Giải thích:

> Đây là API Express mô phỏng một service chạy trong production.

### Bước 2: Gọi API bình thường

Mở trình duyệt hoặc Postman:

```text
http://localhost:3000/api/data
```

Giải thích:

> Endpoint này đại diện cho API thật của hệ thống. Mỗi request đều được ghi log và đo thời gian xử lý.

### Bước 3: Xem log

Sau khi gọi API, mở file:

```text
logs/combined.log
```

Trong log có các thông tin:

- Method: `GET`
- URL: `/api/data`
- Status code: `200`
- Duration: thời gian xử lý request

Ý nghĩa:

> Audit log giúp đội vận hành biết request nào đã xảy ra, thành công hay lỗi, và mất bao lâu.

### Bước 4: Tạo lỗi để xem error log

Gọi:

```text
http://localhost:3000/api/error
```

Sau đó mở file:

```text
logs/error.log
```

Ý nghĩa:

> Trong production, lỗi cần được ghi lại để debug và cảnh báo kịp thời.

### Bước 5: Xem metrics Prometheus

Mở:

```text
http://localhost:3000/metrics
```

Giải thích:

> Metrics là dữ liệu dạng số, dùng để tạo dashboard và cảnh báo. Ví dụ: số request, thời gian xử lý, CPU, RAM.

### Bước 6: Test rate limiting

Có thể dùng PowerShell:

```powershell
1..105 | ForEach-Object { Invoke-WebRequest http://localhost:3000/api/data }
```

Sau khi vượt quá giới hạn, API sẽ trả về status `429 Too Many Requests`.

Giải thích:

> Rate limiting giúp bảo vệ API khỏi spam, brute force hoặc client lỗi gọi quá nhiều request.

## 7. Mapping với yêu cầu bài học

| Yêu cầu | Đã demo ở đâu |
|---|---|
| Deploy API production | `Express server`, dùng `PORT` từ env |
| Logging | Winston trong `src/app.js` |
| Monitoring | `/metrics` Prometheus |
| Tracing cơ bản | Log duration mỗi request |
| Rate limiting | `express-rate-limit` cho `/api/*` |
| Bảo mật production | `helmet()` |
| Audit logs | File `logs/combined.log` |

## 8. Gợi ý triển khai production thật

Khi deploy thật, nên bổ sung:

- Dockerfile và docker-compose.
- Reverse proxy như Nginx.
- HTTPS/TLS.
- WAF như Cloudflare hoặc AWS WAF.
- Centralized logging như ELK, Loki hoặc CloudWatch.
- Dashboard Grafana đọc dữ liệu từ Prometheus.
- Distributed tracing bằng OpenTelemetry.

## 9. Kết luận

Demo này cho thấy một API production không chỉ cần chạy được, mà còn cần:

- Quan sát được hệ thống đang hoạt động thế nào.
- Biết khi nào API lỗi hoặc chậm.
- Có cơ chế chống spam request.
- Có log phục vụ kiểm tra và điều tra sự cố.
