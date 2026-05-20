# Week 11 - API Design Patterns

## 1. Má»¥c tiÃªu kiáº¿n thá»©c
Tuáº§n nÃ y táº­p trung vÃ o cÃ¡c mÃ´ hÃ¬nh thiáº¿t káº¿ API phá»• biáº¿n, giÃºp API linh hoáº¡t, dá»… má»Ÿ rá»™ng vÃ  chuyÃªn nghiá»‡p hÃ³a.

### CÃ¡c Design Patterns chÃ­nh:
1.  **CRUD Pattern**: MÃ´ hÃ¬nh cÆ¡ báº£n (Create, Read, Update, Delete) dÃ¹ng cÃ¡c HTTP Verbs tÆ°Æ¡ng á»©ng.
2.  **Query Pattern**: Cho phÃ©p lá»c, tÃ¬m kiáº¿m dá»¯ liá»‡u phá»©c táº¡p (vÃ­ dá»¥: `?status=paid&item=laptop`).
3.  **HATEOAS (Hypermedia as the Engine of Application State)**: Cung cáº¥p cÃ¡c link trong response Ä‘á»ƒ client biáº¿t cÃ¡c hÃ nh Ä‘á»™ng tiáº¿p theo (nhÆ° Stripe API).
4.  **Event-driven & Webhook**:
    *   **Event-driven**: Há»‡ thá»‘ng pháº£n á»©ng vá»›i cÃ¡c sá»± kiá»‡n (ví dụ: Thanh toÃ¡n xong thÃ¬ gá»­i email).
    *   **Webhook**: CÃ¡ch API chá»§ Ä‘á»™ng "Ä‘áº©y" dá»¯ liá»‡u sang há»‡ thá»‘ng khÃ¡c khi cÃ³ sá»± kiá»‡n (Inversion of Control).

---

## 2. PhÃ¢n tÃ­ch API Patterns thá»±c táº¿

### Stripe API (Master of HATEOAS & Webhooks)
*   **Pattern**: Stripe dÃ¹ng cáº¥u trÃºc Resource-based ráº¥t cháº·t cháº½.
*   **HATEOAS**: Khi báº¡n táº¡o má»™t `PaymentIntent`, Stripe tráº£ vá» cÃ¡c URL trong `next_action` Ä‘á»ƒ client biáº¿t cáº§n redirect ngÆ°á»i dÃ¹ng Ä‘i Ä‘Ã¢u.
*   **Webhooks**: Stripe dÃ¹ng Webhook ráº¥t máº¡nh Ä‘á»ƒ thÃ´ng bÃ¡o khi thanh toÃ¡n thÃ nh cÃ´ng (async), trÃ¡nh viá»‡c client pháº£i polling.

### GitHub API (REST vs GraphQL)
*   **REST**: Cung cáº¥p cÃ¡c endpoint tÆ°á»›i tá»«ng resource (User, Repo, Issue).
*   **GraphQL**: GitHub cung cáº¥p thÃªm GraphQL API Ä‘á»ƒ giáº£i quyáº¿t bÃ i toÃ¡n **Over-fetching** (láº¥y thá»«a dá»¯ liá»‡u) vÃ  **Under-fetching** (láº¥y thiáº¿u pháº£i gá»i nhiá»u API).
*   **Pattern**: GitHub dÃ¹ng "Preview Headers" Ä‘á»ƒ thá»­ nghiá»‡m cÃ¡c tÃ­nh nÄƒng má»›i mÃ  khÃ´ng lÃ m break API cũ.

---

## 3. Demo thá»±c hÃ nh (FastAPI)

### CÃ i Ä‘áº·t
```bash
cd Week11
pip install -r requirements.txt
```

### Cháº¡y Demo
```bash
uvicorn app.main:app --reload
```
Truy cáº­p: `http://localhost:8000/docs`

---

## 4. Ká»‹ch báº£n thuyáº¿t trÃ¬nh "Dá»… hiá»ƒu"

### BÆ°á»›c 1: CRUD & Query
- **Thao tÃ¡c**: Gá»i `GET /orders` vÃ  `GET /orders?item=Laptop`.
- **Giải thÃ­ch**: "ÄÃ¢y lÃ  cÃ¡ch truy váº¥n dá»¯ liá»‡u cÆ¡ báº£n. Pattern nÃ y giÃºp client láº¥y Ä‘Ãºng thá»© há» cáº§n mÃ  khÃ´ng cáº§n táº¡o endpoint riÃªng biá»‡t cho tá»™i tÃ¬m kiáº¿m."

### BÆ°á»›c 2: HATEOAS
- **Thao tÃ¡c**: Gá»i `GET /orders/ord_001`.
- **Quan sÃ¡t**: Trong JSON cÃ³ trÆ°á»ng `"links": [...]`.
- **Giáº£i thÃ­ch**: "Thay vÃ¬ client pháº£i 'đoÃ¡n' URL Ä‘á»ƒ pay hay cancel, API tráº£ vá» luÃ´n cÃ¡c link Ä‘Ã³. Client chá»» viá»‡c theo link. Äiá»u nÃ y lÃ m API trá»Ÿ nÃªn self-describing."

### BÆ°á»›c 3: Webhook (Quan trá»重 nhất)
- **Chuáº©n bá»‹**: Má»Ÿ 2 tab terminal.
- **Tab 1**: Cháº¡y server.
- **Tab 2**: Gá»i API subscribe webhook:
  ```bash
  curl -X POST "http://localhost:8000/webhooks/subscribe" -H "Content-Type: application/json" -d "{\"target_url\": \"http://localhost:8000/demo-receiver\"}"
  ```
- **Thá»±c thi**: Gá»i API thanh toÃ¡n:
  ```bash
  curl -X POST "http://localhost:8000/orders/ord_001/pay"
  ```
- **Quan sÃ¡t**: Server log saráº½ hiá»‡n: `[Webhook] Sending order.paid to ...` vÃ  `[Receiver] Received payload: ...`.
- **Giáº£i thÃ­ch**: "Khi cÃ³ sá»± kiá»‡n thanh toÃ¡n, server tÆ°Æ¡ng tÃ¡c vá»›i cÃ¡c server khÃ¡c thÃ´ng qua Webhook. ÄÃ¢y lÃ  mÃ´ hÃ¬nh 'Äá»«ng gá»i chÃºng tÃ´i, chÃºng tÃ´i sáº½ gá»i báº¡n' (Don't call us, we'll call you)."

---

## 5. So sÃ¡nh nhanh
| Giao thá»©c | Khi nÃ o dÃ¹ng? |
|---|---|
| **REST** | Phá»• biáº¿n, dÃ¹ng cho Web/Mobile App thÃ´ng thÆ°á»ng. |
| **GraphQL** | Khi dá»¯ liá»‡u phá»©c táº¡p, nhiá»u quan hệ, cáº§n tá»‘i Æ°u bang thÃ´ng. |
| **gRPC** | Giao tiáº¿p ná»™i bá»™ giá»¯a cÃ¡c Microservices (hiá»‡u nÄƒng cao, binary). |
| **Webhooks** | Giao tiáº¿p async giÃ»a cÃ¡c há»‡ thá»‘ng bÃªn ngoÃ i (Notified-based). |
