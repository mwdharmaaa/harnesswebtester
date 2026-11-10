#!/usr/bin/env bash
set -euo pipefail

# Activate virtualenv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

export PYTHONPATH="."

if [ $# -eq 0 ]; then
    echo "[*] No arguments supplied. Running default search scenario..."
    python -m src.cli run scenarios/sample_search.json
else
    python -m src.cli "$@"
fi
