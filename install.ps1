# Windows PowerShell installation bundle
$ErrorActionPreference = "Stop"

Write-Host "=========================================================="
Write-Host "[*] Initializing AI E2E Web Testing Harness Environment..."
Write-Host "=========================================================="

if (-not (Test-Path ".venv")) {
    Write-Host "[*] Creating Python virtual environment in .venv..."
    python -m venv .venv
}

$venvPython = ".venv\Scripts\python.exe"

Write-Host "[*] Upgrading pip and installing dependencies..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "[*] Installing Playwright browser binaries..."
& ".venv\Scripts\playwright.exe" install chromium

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host "[*] Generating default .env from .env.example..."
    Copy-Item ".env.example" ".env"
}

Write-Host "=========================================================="
Write-Host "[OK] Installation completed successfully."
Write-Host "=========================================================="
