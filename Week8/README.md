# Week 8 - Postman Test Suite & Newman Automation

## Mục tiêu

Tạo Postman test suite cho 5 API endpoints và chạy tự động bằng Newman.

## Cấu trúc thư mục

```
Week8/
├── package.json              # npm scripts + Newman devDependencies
├── collection/
│   └── INT3505-Week8.postman_collection.json   # 5 requests + test scripts
├── environment/
│   └── INT3505-Week8.postman_environment.json # biến môi trường
├── scripts/
│   └── run-tests.sh          # orchestration: start servers → run Newman → cleanup
└── reports/
    └── .gitkeep              # JSON reports được tạo tại đây khi chạy
```

## Các endpoints được test

### Book API (port 5000 — `Week4/swagger.py`)

| # | Method | Endpoint | Mô tả |
|---|--------|----------|--------|
| 1 | POST | `/books` | Tạo sách mới, lưu `bookId` để dùng ở step tiếp theo |
| 2 | GET | `/books/:id` | Lấy sách theo ID (dùng `bookId` từ step 1) |

### JWT Auth API (port 5001 — `Week6/jwt-flask/app.py`)

| # | Method | Endpoint | Mô tả |
|---|--------|----------|--------|
| 3 | POST | `/api/login` | Login với admin/password, lưu `accessToken` + `refreshToken` |
| 4 | GET | `/api/protected` | Truy cập protected route với Bearer token (prerequest tự động gắn header) |
| 5 | GET | `/api/admin` | RBAC check — yêu cầu role admin |

## Cách chạy

### Bước 1: Cài đặt dependencies

```bash
cd Week8
npm install
```

### Bước 2: Chạy test đầy đủ (recommend)

```bash
npm run test:full
```

Script này sẽ:
1. Khởi động Book API trên port 5000 (background)
2. Khởi động JWT API trên port 5001 (background)
3. Chờ cả 2 server sẵn sàng (health check, tối đa 30s)
4. Chạy Newman với 5 requests
5. Xuất JSON report tại `reports/newman-results.json`
6. Dọn dẹp (kill Flask processes)

### Chạy test trên Windows PowerShell

```powershell
cd Week8
.\scripts\run-tests.ps1
```

Script PowerShell dùng `Invoke-WebRequest` cho health check và `Stop-Process` cho cleanup.

```bash
npm test
```

### Chạy với HTML report

```bash
npm run test:html
```

Xuất thêm file `reports/newman-report.html` với giao diện chi tiết.

## Import vào Postman GUI

1. Mở Postman → **Import** → chọn file `Week8/collection/INT3505-Week8.postman_collection.json`
2. Chọn environment **INT3505-Week8-Local** (Import → environment)
3. Chạy collection bằng **Collection Runner** hoặc click **Send** từng request

## Sửa lỗi thường gặp

### Lỗi `ModuleNotFoundError: No module named 'flask'`

Flask chưa được cài. Cài với uv:

```bash
uv pip install flask flask-swagger-ui pyjwt python-dotenv --system
```

### Lỗi `fuser not found`

Script `run-tests.sh` dùng `fuser` để cleanup (Unix). Trên Windows nếu gặp lỗi, cleanup tự động dùng PID-based kill — không ảnh hưởng kết quả test.

### Port 5000 hoặc 5001 đã bị chiếm

Kiểm tra và kill process:

```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID <PID>
```

### Access token bị trống trong requests 4 và 5

Đảm bảo request 3 (login) chạy thành công trước. Kiểm tra biến `accessToken` trong Postman → **Environment** → tab **Variables**.

## Test assertions tổng quan

| Request | Assertions | Chi tiết |
|---------|-----------|----------|
| 1. Create Book | 5 tests | 201, id là number, title/author match, Content-Type |
| 2. Get Book by ID | 5 tests | 200, id match, title/author match, Content-Type |
| 3. Login | 6 tests | 200, accessToken/refreshToken tồn tại, JWT format (3 phần) |
| 4. Protected Route | 4 tests | 200, message chứa username, user object với role |
| 5. Admin Route | 3 tests | 200, message chứa "Admin" |
| **Tổng** | **23 assertions** | |

## Tài liệu tham khảo

- [Postman Collection Schema v2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Newman Documentation](https://github.com/postmanlabs/newman)
- [Newman HTML Extra Reporter](https://github.com/DannyDainty/newman-reporter-htmlextra)