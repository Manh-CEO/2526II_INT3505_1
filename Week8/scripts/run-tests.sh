#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# INT3505 Week 8 - Newman Test Orchestration Script
# Starts both Flask servers, runs Newman tests, then cleans up.
# ============================================================

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BOOK_API_SCRIPT="$PROJECT_ROOT/Week4/swagger.py"
JWT_API_SCRIPT="$PROJECT_ROOT/Week6/jwt-flask/app.py"
BOOK_API_URL="http://localhost:5000"
JWT_API_URL="http://localhost:5001"
COLLECTION="$PROJECT_ROOT/Week8/collection/INT3505-Week8.postman_collection.json"
ENVIRONMENT="$PROJECT_ROOT/Week8/environment/INT3505-Week8.postman_environment.json"
REPORT_DIR="$PROJECT_ROOT/Week8/reports"

# --- Cleanup function (runs on EXIT) ---
cleanup() {
  echo "[INFO] Stopping Flask servers..."
  if [ -n "${BOOK_PID:-}" ]; then
    kill "$BOOK_PID" 2>/dev/null || true
  fi
  if [ -n "${JWT_PID:-}" ]; then
    kill "$JWT_PID" 2>/dev/null || true
  fi
  # Fallback: kill by PID (reliable when debug=False)
  # On Windows, try netstat + taskkill as fallback
  if command -v fuser >/dev/null 2>&1; then
    fuser -k 5000/tcp 2>/dev/null || true
    fuser -k 5001/tcp 2>/dev/null || true
  fi
  echo "[INFO] Cleanup complete."
}
trap cleanup EXIT

# --- Create report directory ---
mkdir -p "$REPORT_DIR"

# --- Start Flask servers ---
echo "[INFO] Starting Book API on port 5000..."
python "$BOOK_API_SCRIPT" &
BOOK_PID=$!

echo "[INFO] Starting JWT API on port 5001..."
python "$JWT_API_SCRIPT" &
JWT_PID=$!

# --- Wait for servers to be ready ---
MAX_WAIT=30
WAITED=0
echo "[INFO] Waiting for servers to be ready..."

while [ $WAITED -lt $MAX_WAIT ]; do
  BOOK_READY=$(curl -sf "$BOOK_API_URL/books" >/dev/null 2>&1 && echo "1" || echo "0")
  JWT_READY=$(curl -sf "$JWT_API_URL/api/login" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"password"}' >/dev/null 2>&1 && echo "1" || echo "0")

  if [ "$BOOK_READY" = "1" ] && [ "$JWT_READY" = "1" ]; then
    echo "[INFO] Both servers are ready."
    break
  fi

  sleep 1
  WAITED=$((WAITED + 1))
  echo "  ...waiting ($WAITED/$MAX_WAIT)"
done

if [ $WAITED -ge $MAX_WAIT ]; then
  echo "[ERROR] Servers did not start within $MAX_WAIT seconds. Aborting."
  exit 1
fi

# --- Run Newman ---
echo ""
echo "========================================"
echo "[INFO] Running Newman tests..."
echo "========================================"

NEWMAN_EXIT=0
npx newman run "$COLLECTION" \
  --environment "$ENVIRONMENT" \
  --reporters cli,json \
  --reporter-json-export "$REPORT_DIR/newman-results.json" \
  --timeout 10000 \
  --delay-request 500 \
  || NEWMAN_EXIT=$?

echo ""
echo "========================================"
if [ "$NEWMAN_EXIT" -eq 0 ]; then
  echo "[PASS] All Newman tests passed!"
else
  echo "[FAIL] Some Newman tests failed (exit code: $NEWMAN_EXIT)"
fi
echo "[INFO] JSON report: $REPORT_DIR/newman-results.json"
echo "========================================"

exit "$NEWMAN_EXIT"
