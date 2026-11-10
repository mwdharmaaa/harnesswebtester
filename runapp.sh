#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "[*] Launching AI Web Test Harness Desktop Application..."
echo "=========================================================="

exec npx electron . "$@"
