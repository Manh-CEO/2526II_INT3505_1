# INT3505 Week 8 - Newman Test Orchestration (PowerShell)
# Khởi động cả 2 Flask server, chạy Newman, rồi cleanup.

$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$BOOK_API_SCRIPT = "$PROJECT_ROOT\Week4\swagger.py"
$JWT_API_SCRIPT = "$PROJECT_ROOT\Week6\jwt-flask\app.py"
$BOOK_API_URL = "http://127.0.0.1:5000"
$JWT_API_URL = "http://127.0.0.1:5001"
$COLLECTION = "$PROJECT_ROOT\Week8\collection\INT3505-Week8.postman_collection.json"
$ENVIRONMENT = "$PROJECT_ROOT\Week8\environment\INT3505-Week8.postman_environment.json"
$REPORT_DIR = "$PROJECT_ROOT\Week8\reports"

# Tạo thư mục reports nếu chưa có
if (!(Test-Path $REPORT_DIR)) {
    New-Item -ItemType Directory -Force -Path $REPORT_DIR | Out-Null
}

# Hàm dọn dẹp các tiến trình khi kết thúc hoặc lỗi
function Stop-Servers {
    Write-Host ""
    Write-Host "[INFO] Stopping Flask servers..." -ForegroundColor Yellow
    if ($global:BOOK_PROC) { 
        Stop-Process -Id $global:BOOK_PROC.Id -Force -ErrorAction SilentlyContinue 
    }
    if ($global:JWT_PROC) { 
        Stop-Process -Id $global:JWT_PROC.Id -Force -ErrorAction SilentlyContinue 
    }
    
    # Fallback: Quét và đóng các process đang chiếm port 5000, 5001
    Get-NetTCPConnection -LocalPort 5000, 5001 -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    
    Write-Host "[INFO] Cleanup complete." -ForegroundColor Green
}

$ORIGINAL_LOCATION = $PWD
# Trap để đảm bảo khi script dừng đột ngột vẫn dọn dẹp server
trap {
    Set-Location $ORIGINAL_LOCATION
    Stop-Servers
    exit
}

# --- KHOI DONG FLASK SERVERS ---

Write-Host "[INFO] Starting Book API on port 5000..." -ForegroundColor Cyan
# Sử dụng Start-Process để chạy ngầm và lưu đối tượng process
$global:BOOK_PROC = Start-Process python -ArgumentList "`"$BOOK_API_SCRIPT`"" -NoNewWindow -PassThru

Write-Host "[INFO] Starting JWT API on port 5001..." -ForegroundColor Cyan
$global:JWT_PROC = Start-Process python -ArgumentList "`"$JWT_API_SCRIPT`"" -NoNewWindow -PassThru

# Chờ server sẵn sàng (Health Check)
$MAX_WAIT = 30
$WAITED = 0
Write-Host "[INFO] Waiting for servers to be ready..." -ForegroundColor Magenta

while ($WAITED -lt $MAX_WAIT) {
    $BOOK_READY = $false
    $JWT_READY = $false

    try {
        $r = Invoke-WebRequest -Uri "$BOOK_API_URL/books" -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($r.StatusCode -eq 200) { $BOOK_READY = $true }
    } catch {}

    try {
        # Giả lập một request login đơn giản để check server JWT
        $body = @{username="admin"; password="password"} | ConvertTo-Json
        $r = Invoke-WebRequest -Uri "$JWT_API_URL/api/login" -Method POST `
            -Body $body -ContentType "application/json" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($r.StatusCode -eq 200) { $JWT_READY = $true }
    } catch {}

    if ($BOOK_READY -and $JWT_READY) {
        Write-Host "[INFO] Both servers are ready!" -ForegroundColor Green
        break
    }

    Start-Sleep -Seconds 2
    $WAITED += 2
    Write-Host "  ...waiting ($WAITED/$MAX_WAIT)"
}

if ($WAITED -ge $MAX_WAIT) {
    Write-Host "[ERROR] Servers did not start within $MAX_WAIT seconds. Aborting." -ForegroundColor Red
    Stop-Servers
    exit 1
}

# --- CHAY NEWMAN TESTS ---

Write-Host ""
Write-Host "========================================" -ForegroundColor White
Write-Host "[INFO] Running Newman tests..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor White

$env:NODE_OPTIONS = "--max-old-space-size=512"
# Chạy Newman bằng npx
npx newman run "$COLLECTION" `
    --environment "$ENVIRONMENT" `
    --reporters cli,json `
    --reporter-json-export "$REPORT_DIR\newman-results.json" `
    --timeout 10000 `
    --delay-request 500

Write-Host ""
Write-Host "========================================"
Write-Host "[INFO] JSON report generated at: $REPORT_DIR\newman-results.json"
Write-Host "========================================"

# Chạy script phân tích hiệu năng (Operational Monitoring)
if (Test-Path "scripts\analyze-performance.py") {
    python scripts\analyze-performance.py "$REPORT_DIR\newman-results.json"
}

# Kết thúc thì dọn dẹp
Stop-Servers