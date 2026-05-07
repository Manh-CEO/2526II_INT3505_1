$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$weekDir = Split-Path -Parent $scriptDir
$appPath = Join-Path $weekDir 'app.py'
$testPath = Join-Path $weekDir 'tests\test_versioning.py'

Write-Host 'Starting Week9 Flask server in directory:'$weekDir'...'
$process = Start-Process python -ArgumentList "`"$appPath`"" -WorkingDirectory $weekDir -PassThru -NoNewWindow

try {
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/api/v1/health' -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                $ready = $true
                break
            }
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }

    if (-not $ready) {
        throw 'Flask server did not become ready in time.'
    }

    Write-Host 'Running pytest...'
    python -m pytest "`"$testPath`"" -v
}
finally {
    if ($null -ne $process -and -not $process.HasExited) {
        Write-Host 'Stopping Flask server...'
        Stop-Process -Id $process.Id -Force
    }
}