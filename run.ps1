# Windows PowerShell runner
$ErrorActionPreference = "Stop"

$pythonBin = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
$env:PYTHONPATH = "."

if ($args.Count -eq 0) {
    Write-Host "[*] No arguments supplied. Running default search scenario..."
    & $pythonBin -m src.cli run scenarios/sample_search.json
} else {
    & $pythonBin -m src.cli @args
}
