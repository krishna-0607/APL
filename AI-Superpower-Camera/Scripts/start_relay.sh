#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../PythonVision"
PYTHONPATH=. python -m app.multiplayer_relay --host 0.0.0.0 --port 9000
