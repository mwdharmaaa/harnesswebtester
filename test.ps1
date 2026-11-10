# Windows PowerShell test runner
$ErrorActionPreference = "Stop"

$pytestBin = if (Test-Path ".venv\Scripts\pytest.exe") { ".venv\Scripts\pytest.exe" } else { "pytest" }
$env:PYTHONPATH = "."

Write-Host "=========================================================="
Write-Host "[*] Executing Automated Test Suite..."
Write-Host "=========================================================="

& $pytestBin tests/ -v @args
