# Week 9 - API Versioning, Breaking Changes và Deprecation

## Mục tiêu

Hoàn thành bài tập chuyên nghiệp về chiến lược versioning cho REST API, bao gồm:
- URL versioning
- Header versioning
- Query parameter versioning
- Xử lý breaking changes
- Lập migration plan từ `v1` sang `v2`
- Viết deprecation notice cho developers

Bài thực hành sử dụng **Flask** để mô phỏng một **Payment API** với 2 phiên bản `v1` và `v2`.

## Cấu trúc thư mục

```text
Week9/
├── app.py
├── requirements.txt
├── README.md
├── docs/
│   ├── migration-plan.md
│   └── deprecation-notice.md
├── tests/
│   └── test_versioning.py
└── scripts/
    └── run-tests.ps1
```

## 1. Các chiến lược versioning phổ biến

### 1.1 URL Versioning
Ví dụ:
```http
GET /api/v1/payments
GET /api/v2/payments
```

**Ưu điểm:**
- Dễ nhìn, dễ debug
- Dễ viết tài liệu
- Dễ cấu hình gateway, cache, logs

**Nhược điểm:**
- URL thay đổi khi đổi version
- Có thể tạo nhiều route song song nếu duy trì nhiều version

### 1.2 Header Versioning
Ví dụ:
```http
GET /api/payments
Accept: application/vnd.api.v2+json
```

**Ưu điểm:**
- URL gọn, không đổi
- Tách contract khỏi resource path

**Nhược điểm:**
- Khó debug hơn
- Developers dễ quên set đúng header
- Documentation và test tooling thường ít trực quan hơn URL versioning

### 1.3 Query Parameter Versioning
Ví dụ:
```http
GET /api/payments?version=2
```

**Ưu điểm:**
- Dễ thử nhanh bằng trình duyệt hoặc curl
- Thân thiện với môi trường học tập/demo

**Nhược điểm:**
- Ít chặt chẽ hơn public API contract
- Dễ bị dùng sai hoặc bỏ sót
- Không phải lựa chọn tốt nhất cho API production lâu dài

## 2. Khuyến nghị cho bài toán Payment API

Trong case study này, **URL versioning** được chọn làm chiến lược chính vì phù hợp nhất cho API thanh toán production:
- Dễ quản trị lifecycle
- Dễ theo dõi traffic theo version
- Phù hợp với deprecation communication
- Tối ưu cho API gateway, observability và tài liệu hóa

Header versioning và query parameter versioning vẫn được triển khai trong demo để minh họa trade-offs thực tế.

## 3. Breaking Changes từ v1 sang v2

| Hạng mục | v1 | v2 |
|---|---|---|
| Response schema | Flat JSON | Nested JSON với `data` và `metadata` |
| Error handling | Luôn trả `200`, lỗi nằm trong body | Trả `4xx` đúng chuẩn |
| Pagination | `page`, `limit` | `cursor`, `limit` |
| Contract clarity | Đơn giản nhưng mơ hồ khi mở rộng | Rõ ràng hơn, extensible hơn |

### Ví dụ response v1

```json
{
  "id": "pay_001",
  "amount": 100000,
  "status": "succeeded",
  "currency": "VND"
}
```

### Ví dụ response v2

```json
{
  "data": {
    "id": "pay_001",
    "amount": {
      "value": 100000,
      "currency": "VND"
    },
    "status": "succeeded",
    "metadata": {
      "customer_id": "cus_001",
      "method": "card",
      "created_at": "2026-05-01T10:00:00Z"
    }
  }
}
```

## 4. Deprecation và xử lý breaking changes

Khi có breaking changes, không nên thay đổi âm thầm trên API đang dùng rộng rãi. Quy trình chuyên nghiệp nên gồm:

1. Phát hành `v2` song song với `v1`
2. Công bố deprecation notice sớm
3. Trả thêm `Deprecation`, `Sunset`, `Link` headers trên `v1`
4. Cung cấp migration guide rõ ràng
5. Theo dõi adoption rate trước khi sunset `v1`

## 5. API endpoints trong bài thực hành

### URL Versioning
- `GET /api/v1/health`
- `GET /api/v2/health`
- `GET /api/v1/payments`
- `GET /api/v2/payments`
- `GET /api/v1/payments/<id>`
- `GET /api/v2/payments/<id>`

### Header / Query Parameter Versioning
- `GET /api/payments`
- `GET /api/payments/<id>`

Ví dụ header versioning:
```bash
curl -H "Accept: application/vnd.api.v2+json" http://localhost:5000/api/payments
```

Ví dụ query versioning:
```bash
curl "http://localhost:5000/api/payments?version=2"
```

### Deprecation demo
- `GET /api/v1/deprecated-endpoint`
- `GET /api/v1/payments?format=old`

## 6. Cách chạy

### Bước 1: Cài dependencies

```bash
cd Week9
pip install -r requirements.txt
```

### Bước 2: Chạy Flask server

```bash
python app.py
```

Server mặc định chạy tại `http://127.0.0.1:5000`.

### Bước 3: Test thủ công

```bash
curl http://127.0.0.1:5000/api/v1/payments
curl http://127.0.0.1:5000/api/v2/payments
curl -H "Accept: application/vnd.api.v2+json" http://127.0.0.1:5000/api/payments
curl "http://127.0.0.1:5000/api/payments?version=2"
curl http://127.0.0.1:5000/api/v1/deprecated-endpoint
```

## 7. Chạy test tự động

```bash
pytest tests/test_versioning.py -v
```

Hoặc trên Windows PowerShell:

```powershell
.\scripts\run-tests.ps1
```

## 8. Case study: nâng cấp từ Payment API v1 sang v2

Bài thực hành mô phỏng một tình huống rất phổ biến trong doanh nghiệp:
- `v1` ra đời sớm để ship nhanh
- Sau thời gian sử dụng, client bắt đầu phụ thuộc mạnh vào contract cũ
- Khi cần mở rộng schema, error handling, auth, pagination thì không thể sửa trực tiếp `v1`
- Giải pháp đúng là phát hành `v2`, công bố deprecation, hỗ trợ migration theo lộ trình

Hai tài liệu đi kèm:
- `docs/migration-plan.md`
- `docs/deprecation-notice.md`

## 9. Kết luận

Versioning không chỉ là đổi tên URL. Đó là một phần của quản trị vòng đời API. Một chiến lược versioning tốt cần kết hợp cả kỹ thuật, truyền thông với developers, lộ trình migration, và cách xử lý breaking changes có trách nhiệm.

Trong bài toán này:
- **URL versioning** là lựa chọn phù hợp nhất cho production payment API
- **Header versioning** phù hợp với một số use case cần contract negotiation
- **Query param versioning** hữu ích cho demo và compatibility tạm thời, nhưng không nên là public strategy chính lâu dài