# Migration Plan: Payment API v1 → v2

## 1. Executive Summary

Hệ thống Payment API hiện đang chạy phiên bản `v1` với response đơn giản, cơ chế lỗi chưa chuẩn hóa và pagination kiểu offset. Để đáp ứng nhu cầu mở rộng tích hợp, giảm ambiguity cho client, và cải thiện khả năng quan sát lỗi, nhóm backend đề xuất triển khai `v2` với response có cấu trúc rõ ràng hơn, mã lỗi HTTP chuẩn hơn, và hỗ trợ cursor pagination.

Mục tiêu của kế hoạch nâng cấp là cho phép client chuyển từ `v1` sang `v2` an toàn, có lộ trình, có thông báo trước, và không gây gián đoạn đột ngột cho hệ sinh thái tích hợp.

## 2. Breaking Changes Between v1 and v2

| Hạng mục | v1 | v2 | Tác động |
|---|---|---|---|
| Response body | Flat JSON | Nested JSON với `data` và `metadata` | Client parser phải cập nhật |
| Error handling | Luôn trả `200` rồi nhét lỗi vào body | Trả `4xx/5xx` đúng ngữ nghĩa | Client cần sửa logic xử lý lỗi |
| Authentication | API key | API key + JWT/Bearer token | Cập nhật flow xác thực |
| Pagination | `page` + `limit` | `cursor` + `limit` | UI/integration cần đổi cơ chế phân trang |
| Deprecation signaling | Không có | Có `Deprecation`, `Sunset`, `Link` header | Client có thể detect deprecation sớm |

## 3. Recommended Versioning Strategy

### Primary strategy: URL versioning

Sử dụng URL versioning làm chiến lược chính cho public API:
- `GET /api/v1/payments`
- `GET /api/v2/payments`

**Lý do:**
- Dễ hiểu với developers
- Thuận tiện cho documentation, gateway, caching, monitoring
- Giảm ambiguity khi debug production traffic

### Secondary strategies for demonstration and internal compatibility

- **Header versioning**: `Accept: application/vnd.api.v2+json`
- **Query param versioning**: `?version=2`

Hai chiến lược này phù hợp để học thuật, A/B thử nghiệm, hoặc phục vụ tầng compatibility tạm thời, nhưng không nên là public contract chính trong bài toán payment production.

## 4. Deprecation Timeline

| Giai đoạn | Thời điểm | Hành động |
|---|---|---|
| Announcement | T0 | Gửi thông báo deprecation tới developers |
| Parallel support | T0 → T0 + 90 ngày | Chạy song song v1 và v2 |
| Warning period | T0 + 30 ngày | Bật `Deprecation` và `Sunset` header trên v1 |
| Freeze changes | T0 + 60 ngày | Không thêm feature mới cho v1 |
| Sunset | T0 + 90 ngày | Dừng hỗ trợ chính thức, trả `410 Gone` cho endpoint đã sunset |

## 5. Migration Guide for API Consumers

1. **Inventory** toàn bộ nơi đang gọi `v1`
2. **So sánh response schema** giữa `v1` và `v2`
3. **Cập nhật error handling** để xử lý `404`, `400`, `401` đúng chuẩn
4. **Đổi pagination** từ offset sang cursor nếu client có danh sách thanh toán
5. **Cập nhật auth flow** nếu `v2` yêu cầu token nâng cao hơn
6. **Chạy integration test** trên staging
7. **Triển khai canary** cho một phần traffic
8. **Theo dõi metrics**: error rate, latency, contract mismatch, failed parsing

## 6. Internal Checklist for Backend Team

- [ ] Publish OpenAPI spec cho `v2`
- [ ] Thêm deprecation headers cho `v1`
- [ ] Viết migration guide công khai
- [ ] Bổ sung observability theo version (`api_version=v1|v2`)
- [ ] Tách dashboard lỗi theo version
- [ ] Thiết lập alert nếu client cũ vẫn gọi `v1` gần sunset date
- [ ] Chuẩn bị rollback plan cho `v2`

## 7. Rollout Recommendation

Đề xuất rollout theo 3 bước:
1. **Soft launch**: phát hành `v2` nhưng chưa quảng bá rộng
2. **Guided migration**: mời các client quan trọng nâng cấp trước
3. **Sunset enforcement**: khóa dần endpoint `v1` sau khi đủ lead time

## 8. Success Criteria

Việc migration được coi là thành công khi:
- 95% traffic chuyển sang `v2` trước sunset date
- Không có incident P1/P2 do schema mismatch
- Error rate của `v2` không vượt quá `v1`
- Toàn bộ documentation và SDK nội bộ đã cập nhật theo `v2`