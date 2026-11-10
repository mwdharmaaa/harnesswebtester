# Windows PowerShell Desktop Launcher
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Ensure Node.js is accessible in PATH
$nodeDir = "C:\Users\someo\AppData\Local\Programs\nodejs"
if (Test-Path $nodeDir) {
    $env:Path = "$nodeDir;" + $env:Path
}

Write-Host "=========================================================="
Write-Host "[*] Launching AI Web Test Harness Desktop Application..."
Write-Host "=========================================================="

npx electron . @args
