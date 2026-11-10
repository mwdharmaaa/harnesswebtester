#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "[*] Initializing AI E2E Web Testing Harness Environment..."
echo "=========================================================="

if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment in .venv..."
    python3 -m venv .venv || python -m venv .venv
fi

# Activate venv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

echo "[*] Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Installing Playwright browser binaries..."
playwright install chromium

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "[*] Generating default .env from .env.example..."
    cp .env.example .env
fi

echo "=========================================================="
echo "[OK] Installation completed successfully."
echo "=========================================================="
