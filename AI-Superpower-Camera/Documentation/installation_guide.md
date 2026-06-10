# Installation Guide

## Prerequisites

- Python 3.10+
- Unity 6
- FFmpeg in PATH
- Webcam

## Setup

1. Python backend setup:
```bash
cd PythonVision
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start services:
```bash
cd PythonVision
python -m app.server --config config/default.yaml
python -m app.multiplayer_relay --host 0.0.0.0 --port 9000
```

3. Unity setup:
- Open `UnityClient` in Unity Hub with Unity 6.
- Add scripts from `Assets/Scripts` to scene objects.
- Ensure TextMeshPro package is installed.
- Add VFX Graph package if not already present.

4. Validate:
```bash
cd PythonVision
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py'
```
