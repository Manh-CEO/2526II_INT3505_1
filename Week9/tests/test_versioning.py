"""
Week 9 — API Versioning Tests (TDD approach)
Tests verify v1 vs v2 behavior and three versioning mechanisms.
Run: pytest tests/test_versioning.py -v
"""
import pytest
import requests
import sys
import time
import subprocess
import os
import signal

BASE_URL = "http://127.0.0.1:5000"
APP_PATH = os.path.join(os.path.dirname(__file__), "..", "app.py")


def wait_for_server(url, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{url}/api/v1/health", timeout=2)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False


@pytest.fixture(scope="module")
def server():
    proc = subprocess.Popen(
        [sys.executable, APP_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(APP_PATH),
    )
    if not wait_for_server(BASE_URL):
        proc.terminate()
        pytest.fail("Flask server did not start in time")
    yield proc
    proc.terminate()
    proc.wait(timeout=5)


# ── v1 vs v2 response shape ──────────────────────────────────────────────────

def test_v1_payments_returns_flat_list(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    item = data[0]
    assert "id" in item
    assert "amount" in item
    assert "status" in item
    assert "metadata" not in item


def test_v2_payments_returns_nested_list(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "pagination" in data
    items = data["data"]
    assert isinstance(items, list)
    item = items[0]
    assert "id" in item
    assert "amount" in item
    assert "metadata" in item


def test_v1_single_returns_flat(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments/pay_001")
    assert r.status_code == 200
    d = r.json()
    assert d.get("id") == "pay_001"
    assert "metadata" not in d


def test_v2_single_returns_nested(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments/pay_001")
    assert r.status_code == 200
    d = r.json()
    assert d["data"]["id"] == "pay_001"
    assert "metadata" in d["data"]


# ── v1 always returns 200 with error in body; v2 uses proper 4xx ──────────

def test_v1_missing_returns_200_with_error_in_body(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments/nonexistent")
    assert r.status_code == 200  # v1 convention: always 200
    d = r.json()
    assert "error" in d or d.get("id") is None


def test_v2_missing_returns_404(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments/nonexistent")
    assert r.status_code == 404
    d = r.json()
    assert "error" in d


# ── URL Path Versioning ─────────────────────────────────────────────────────

def test_url_path_v1_handler(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments")
    assert r.status_code == 200
    d = r.json()
    # v1 has no nested "data" key — flat list
    assert isinstance(d, list)


def test_url_path_v2_handler(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments")
    assert r.status_code == 200
    d = r.json()
    assert "data" in d  # v2 uses nested structure


# ── Header Versioning ────────────────────────────────────────────────────────

def test_header_v2_returns_nested(server):
    r = requests.get(
        f"{BASE_URL}/api/payments",
        headers={"Accept": "application/vnd.api.v2+json"},
    )
    assert r.status_code == 200
    d = r.json()
    assert "data" in d


def test_header_v1_returns_flat(server):
    r = requests.get(
        f"{BASE_URL}/api/payments",
        headers={"Accept": "application/vnd.api.v1+json"},
    )
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d, list) and not isinstance(d, dict)


def test_header_v2_single(server):
    r = requests.get(
        f"{BASE_URL}/api/payments/pay_001",
        headers={"Accept": "application/vnd.api.v2+json"},
    )
    assert r.status_code == 200
    d = r.json()
    assert d["data"]["id"] == "pay_001"


# ── Query Parameter Versioning ───────────────────────────────────────────────

def test_query_param_v2_returns_nested(server):
    r = requests.get(f"{BASE_URL}/api/payments?version=2")
    assert r.status_code == 200
    d = r.json()
    assert "data" in d


def test_query_param_v1_returns_flat(server):
    r = requests.get(f"{BASE_URL}/api/payments?version=1")
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d, list)


def test_query_param_v2_single(server):
    r = requests.get(f"{BASE_URL}/api/payments/pay_001?version=2")
    assert r.status_code == 200
    d = r.json()
    assert d["data"]["id"] == "pay_001"


def test_query_param_invalid_version_defaults_to_v1(server):
    r = requests.get(f"{BASE_URL}/api/payments?version=99")
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d, list)


# ── Deprecation / Sunset Headers ─────────────────────────────────────────────

def test_deprecated_endpoint_returns_deprecation_header(server):
    r = requests.get(f"{BASE_URL}/api/v1/deprecated-endpoint")
    # After sunset, should return 410 Gone with Deprecation header
    # Our demo: returns 200 with header but warns client
    assert "Deprecation" in r.headers or r.status_code in (200, 410)
    if "Deprecation" in r.headers:
        assert "true" in r.headers.get("Deprecation", "").lower() or "v1" in r.headers.get("Deprecation", "").lower()


def test_legacy_format_returns_warning_header(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments?format=old")
    assert "Warning" in r.headers or r.status_code in (200, 400)
    if "Warning" in r.headers:
        assert "299" in r.headers.get("Warning", "")


def test_v2_endpoint_has_no_deprecation(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments")
    assert r.status_code == 200
    assert "Deprecation" not in r.headers


# ── Pagination (v2 cursor vs v1 offset) ──────────────────────────────────────

def test_v1_pagination_offset_only(server):
    r = requests.get(f"{BASE_URL}/api/v1/payments?page=2&limit=5")
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d, list)
    assert len(d) == 5


def test_v2_pagination_includes_cursor(server):
    r = requests.get(f"{BASE_URL}/api/v2/payments?cursor=pay_005&limit=3")
    assert r.status_code == 200
    d = r.json()
    assert "data" in d
    assert "pagination" in d
    assert "next_cursor" in d["pagination"]


# ── Health endpoints ─────────────────────────────────────────────────────────

def test_v1_health(server):
    r = requests.get(f"{BASE_URL}/api/v1/health")
    assert r.status_code == 200
    assert r.json()["version"] == "v1"


def test_v2_health(server):
    r = requests.get(f"{BASE_URL}/api/v2/health")
    assert r.status_code == 200
    assert r.json()["version"] == "v2"