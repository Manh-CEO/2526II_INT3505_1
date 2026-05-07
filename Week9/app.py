from copy import deepcopy
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

PAYMENTS = [
    {"id": "pay_001", "amount": 100000, "currency": "VND", "status": "succeeded", "customer_id": "cus_001", "method": "card", "created_at": "2026-05-01T10:00:00Z"},
    {"id": "pay_002", "amount": 250000, "currency": "VND", "status": "pending", "customer_id": "cus_002", "method": "bank_transfer", "created_at": "2026-05-01T11:00:00Z"},
    {"id": "pay_003", "amount": 500000, "currency": "VND", "status": "failed", "customer_id": "cus_003", "method": "ewallet", "created_at": "2026-05-01T12:00:00Z"},
    {"id": "pay_004", "amount": 320000, "currency": "VND", "status": "succeeded", "customer_id": "cus_004", "method": "card", "created_at": "2026-05-02T08:00:00Z"},
    {"id": "pay_005", "amount": 150000, "currency": "VND", "status": "pending", "customer_id": "cus_005", "method": "card", "created_at": "2026-05-02T09:00:00Z"},
    {"id": "pay_006", "amount": 900000, "currency": "VND", "status": "succeeded", "customer_id": "cus_006", "method": "bank_transfer", "created_at": "2026-05-02T10:00:00Z"},
    {"id": "pay_007", "amount": 770000, "currency": "VND", "status": "failed", "customer_id": "cus_007", "method": "ewallet", "created_at": "2026-05-02T11:00:00Z"},
    {"id": "pay_008", "amount": 450000, "currency": "VND", "status": "succeeded", "customer_id": "cus_008", "method": "card", "created_at": "2026-05-02T12:00:00Z"},
    {"id": "pay_009", "amount": 610000, "currency": "VND", "status": "pending", "customer_id": "cus_009", "method": "ewallet", "created_at": "2026-05-03T08:30:00Z"},
    {"id": "pay_010", "amount": 120000, "currency": "VND", "status": "succeeded", "customer_id": "cus_010", "method": "bank_transfer", "created_at": "2026-05-03T09:30:00Z"},
]

DEPRECATION_DOC_URL = "https://developer.example.com/payments/migrate-v2"
SUNSET_DATE = "Wed, 31 Dec 2026 23:59:59 GMT"


def build_v1_payment(payment):
    return {
        "id": payment["id"],
        "amount": payment["amount"],
        "status": payment["status"],
        "currency": payment["currency"],
    }


def build_v2_payment(payment):
    return {
        "id": payment["id"],
        "amount": {
            "value": payment["amount"],
            "currency": payment["currency"],
        },
        "status": payment["status"],
        "metadata": {
            "customer_id": payment["customer_id"],
            "method": payment["method"],
            "created_at": payment["created_at"],
        },
    }


def find_payment(payment_id):
    return next((deepcopy(payment) for payment in PAYMENTS if payment["id"] == payment_id), None)


def get_requested_version():
    query_version = request.args.get("version")
    if query_version in {"1", "2"}:
        return f"v{query_version}"

    accept_header = request.headers.get("Accept", "")
    if "application/vnd.api.v2+json" in accept_header:
        return "v2"
    if "application/vnd.api.v1+json" in accept_header:
        return "v1"

    return "v1"


def add_deprecation_headers(response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE
    response.headers["Link"] = f'<{DEPRECATION_DOC_URL}>; rel="deprecation"'
    return response


def add_legacy_warning(response):
    response.headers["Warning"] = '299 - "Legacy response format is deprecated and will be removed in v2"'
    return response


def get_v1_page_items():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=len(PAYMENTS), type=int)
    start = max(page - 1, 0) * limit
    end = start + limit
    return [build_v1_payment(payment) for payment in PAYMENTS[start:end]]


def get_v2_page_items():
    limit = request.args.get("limit", default=5, type=int)
    cursor = request.args.get("cursor")
    start_index = 0

    if cursor:
        cursor_index = next((index for index, payment in enumerate(PAYMENTS) if payment["id"] == cursor), None)
        if cursor_index is not None:
            start_index = cursor_index + 1

    sliced = PAYMENTS[start_index:start_index + limit]
    next_cursor = sliced[-1]["id"] if sliced else None

    return {
        "data": [build_v2_payment(payment) for payment in sliced],
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor,
            "has_more": start_index + limit < len(PAYMENTS),
        },
    }


@app.get("/api/v1/health")
def health_v1():
    return jsonify({"status": "ok", "version": "v1"})


@app.get("/api/v2/health")
def health_v2():
    return jsonify({"status": "ok", "version": "v2"})


@app.get("/api/v1/payments")
def list_payments_v1():
    response = make_response(jsonify(get_v1_page_items()))
    if request.args.get("format") == "old":
        add_legacy_warning(response)
    return response


@app.get("/api/v2/payments")
def list_payments_v2():
    return jsonify(get_v2_page_items())


@app.get("/api/v1/payments/<payment_id>")
def get_payment_v1(payment_id):
    payment = find_payment(payment_id)
    if payment is None:
        return jsonify({"error": "Payment not found", "id": None})
    return jsonify(build_v1_payment(payment))


@app.get("/api/v2/payments/<payment_id>")
def get_payment_v2(payment_id):
    payment = find_payment(payment_id)
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"data": build_v2_payment(payment)})


@app.get("/api/payments")
def list_payments_dispatch():
    version = get_requested_version()
    if version == "v2":
        return jsonify(get_v2_page_items())

    response = make_response(jsonify(get_v1_page_items()))
    if request.args.get("format") == "old":
        add_legacy_warning(response)
    return response


@app.get("/api/payments/<payment_id>")
def get_payment_dispatch(payment_id):
    version = get_requested_version()
    payment = find_payment(payment_id)

    if version == "v2":
        if payment is None:
            return jsonify({"error": "Payment not found"}), 404
        return jsonify({"data": build_v2_payment(payment)})

    if payment is None:
        return jsonify({"error": "Payment not found", "id": None})
    return jsonify(build_v1_payment(payment))


@app.get("/api/v1/deprecated-endpoint")
def deprecated_endpoint():
    response = make_response(jsonify({
        "message": "This endpoint is deprecated. Please migrate to /api/v2/payments.",
        "migration_guide": DEPRECATION_DOC_URL,
        "sunset": SUNSET_DATE,
    }))
    return add_deprecation_headers(response)


if __name__ == "__main__":
    app.run(port=5000, debug=False)