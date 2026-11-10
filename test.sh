#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

export PYTHONPATH="."
echo "=========================================================="
echo "[*] Executing Automated Test Suite..."
echo "=========================================================="
pytest tests/ -v "$@"
