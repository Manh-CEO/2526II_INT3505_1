# Deprecation Notice for Developers

## Subject
Deprecation Notice: Payment API v1 will be sunset in 90 days

## Summary
Chúng tôi chính thức thông báo rằng **Payment API v1** đã bước vào giai đoạn deprecation. Phiên bản này sẽ tiếp tục hoạt động trong thời gian chuyển tiếp, nhưng developers cần bắt đầu migration sang **Payment API v2** ngay từ bây giờ để tránh gián đoạn dịch vụ.

## Affected Endpoints
- `GET /api/v1/payments`
- `GET /api/v1/payments/{id}`
- Các endpoint phụ thuộc cùng schema phản hồi của `v1`

## Deprecation Policy
Từ thời điểm công bố, các endpoint `v1` sẽ trả thêm các HTTP headers sau:

```http
Deprecation: true
Sunset: Wed, 31 Dec 2026 23:59:59 GMT
Link: <https://developer.example.com/payments/migrate-v2>; rel="deprecation"
```

## Why this change is happening
Phiên bản `v2` được phát hành để:
- Chuẩn hóa response schema
- Trả mã lỗi HTTP đúng ngữ nghĩa
- Hỗ trợ metadata rõ ràng hơn cho payment objects
- Chuẩn bị nền tảng cho mở rộng authentication và pagination

## What you need to do
1. Kiểm tra toàn bộ integration hiện đang gọi `v1`
2. Cập nhật parser theo schema `v2`
3. Điều chỉnh logic xử lý lỗi theo mã trạng thái HTTP thật
4. Chạy regression test trên staging trước khi cut over production

## Recommended Timeline
- **Ngay lập tức**: bắt đầu review tác động
- **Trong 30 ngày**: hoàn thành cập nhật code và test
- **Trong 60 ngày**: rollout production
- **Trước sunset date**: gỡ hoàn toàn dependency vào `v1`

## Support
Nếu cần hỗ trợ migration, vui lòng liên hệ team platform API hoặc tham khảo migration guide:

- Migration guide: `docs/migration-plan.md`
- Public guide: `https://developer.example.com/payments/migrate-v2`

## Example Announcement Message

> Payment API v1 is now deprecated and will be sunset on Wed, 31 Dec 2026 23:59:59 GMT. Please migrate to Payment API v2 to continue receiving supported behavior, structured error handling, and future-compatible response contracts.