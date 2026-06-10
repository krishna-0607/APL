#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../PythonVision"
PYTHONPATH=. python -m app.server --config config/default.yaml
