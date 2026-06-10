# AI Superpower Camera

AI Superpower Camera is a real-time computer-vision + AR desktop project with:
- Python vision backend (OpenCV + MediaPipe + optional TFLite/ONNX classifier)
- Unity 6 client runtime (C# systems for powers, VFX hooks, audio, UI, recording)
- WebSocket bridge between backend and Unity
- SQLite custom power storage
- FFmpeg-based recording hooks
- Multiplayer relay service for power sync and damage events

## Folder Structure

```text
AI-Superpower-Camera/
├── UnityClient/
├── PythonVision/
├── Assets/
├── Models/
├── Sounds/
├── Documentation/
├── Tests/
├── Scripts/
├── Database/
├── Deployment/
└── Videos/
```

## Quick Start

1. Install dependencies:
```bash
cd PythonVision
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run backend vision server:
```bash
cd PythonVision
python -m app.server --config config/default.yaml
```

3. Run multiplayer relay server:
```bash
cd PythonVision
python -m app.multiplayer_relay --host 0.0.0.0 --port 9000
```

4. Open `UnityClient` in Unity 6 and configure scene objects:
- Attach `VisionWebSocketClient`, `PowerEngineController`, `PowerVFXController`, `PowerAudioController`, `HUDController`, `RecordingController`.
- Point WebSocket URL to `ws://127.0.0.1:8765`.

5. Run tests:
```bash
cd PythonVision
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py'
```

## Features Implemented

- Webcam pipeline via OpenCV + MediaPipe Holistic
- Pose, face, and hand landmarks extraction
- Motion metrics (velocity, acceleration, direction)
- Gesture recognition (rule-based + optional ML)
- Power event engine with cooldown/state
- WebSocket event streaming to Unity
- Custom power creation and storage in SQLite
- Recording hooks using FFmpeg
- Multiplayer relay for synchronized damage events
- Documentation, architecture diagrams, deployment scripts, and tests

## Targets

- Designed for 30-60 FPS (camera and hardware dependent)
- Backend message latency target: < 100 ms in local network

## License

MIT
