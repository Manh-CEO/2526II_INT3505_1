# INT3505 Week 8 - Newman Test Orchestration (PowerShell)
# Khoi dong ca 2 Flask server, chay Newman, roi cleanup.

$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$BOOK_API_SCRIPT = "$PROJECT_ROOT\Week4\swagger.py"
$JWT_API_SCRIPT = "$PROJECT_ROOT\Week6\jwt-flask\app.py"
$BOOK_API_URL = "http://localhost:5000"
$JWT_API_URL = "http://localhost:5001"
$COLLECTION = "$PROJECT_ROOT\Week8\collection\INT3505-Week8.postman_collection.json"
$ENVIRONMENT = "$PROJECT_ROOT\Week8\environment\INT3505-Week8.postman_environment.json"
$REPORT_DIR = "$PROJECT_ROOT\Week8\reports"

# Tao reports dir
New-Item -ItemType Directory -Force -Path $REPORT_DIR | Out-Null

# Cleanup function
function Stop-Servers {
    Write-Host "[INFO] Stopping Flask servers..."
    if ($BOOK_PID) { Stop-Process -Id $BOOK_PID -Force -ErrorAction SilentlyContinue }
    if ($JWT_PID) { Stop-Process -Id $JWT_PID -Force -ErrorAction SilentlyContinue }
    # Fallback: kill by port
    Get-NetTCPConnection -LocalPort 5000, 5001 -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Write-Host "[INFO] Cleanup complete."
}
$ORIGINAL_LOCATION = $PWD
trap {
    Set-Location $ORIGINAL_LOCATION
    Stop-Servers
} Exit

# Khoi dong Flask servers
Write-Host "[INFO] Starting Book API on port 5000..."
python $BOOK_API_SCRIPT 2>&1 | Out-Null &
$BOOK_PID = $PID

Write-Host "[INFO] Starting JWT API on port 5001..."
python $JWT_API_SCRIPT 2>&1 | Out-Null &
$JWT_PID = $PID

# Cho server san sang
$MAX_WAIT = 30
$WAITED = 0
Write-Host "[INFO] Waiting for servers to be ready..."

while ($WAITED -lt $MAX_WAIT) {
    $BOOK_READY = $false
    $JWT_READY = $false

    try {
        $r = Invoke-WebRequest -Uri "$BOOK_API_URL/books" -Method GET -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($r.StatusCode -eq 200) { $BOOK_READY = $true }
    } catch {}

    try {
        $r = Invoke-WebRequest -Uri "$JWT_API_URL/api/login" -Method POST `
            -Body '{"username":"admin","password":"password"}' `
            -ContentType "application/json" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($r.StatusCode -eq 200) { $JWT_READY = $true }
    } catch {}

    if ($BOOK_READY -and $JWT_READY) {
        Write-Host "[INFO] Both servers are ready."
        break
    }

    Start-Sleep -Seconds 1
    $WAITED++
    Write-Host "  ...waiting ($WAITED/$MAX_WAIT)"
}

if ($WAITED -ge $MAX_WAIT) {
    Write-Host "[ERROR] Servers did not start within $MAX_WAIT seconds. Aborting."
    exit 1
}

# Chay Newman
Write-Host ""
Write-Host "========================================"
Write-Host "[INFO] Running Newman tests..."
Write-Host "========================================"

$env:NODE_OPTIONS = "--max-old-space-size=512"
npx newman run $COLLECTION `
    --environment $ENVIRONMENT `
    --reporters cli,json `
    --reporter-json-export "$REPORT_DIR\newman-results.json" `
    --timeout 10000 `
    --delay-request 500

Write-Host ""
Write-Host "========================================"
Write-Host "[INFO] JSON report: $REPORT_DIR\newman-results.json"
Write-Host "========================================"