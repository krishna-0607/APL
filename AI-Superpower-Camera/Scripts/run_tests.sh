#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../PythonVision"
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py'
