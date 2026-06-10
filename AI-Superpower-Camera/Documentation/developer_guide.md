# Developer Guide

## Key Modules

- `PythonVision/app/vision.py`: camera and landmark extraction
- `PythonVision/app/gesture_rules.py`: rule-based classifier
- `PythonVision/app/gesture_ml.py`: optional TFLite/ONNX classifier
- `PythonVision/app/power_engine.py`: cooldown and state machine
- `PythonVision/app/server.py`: WebSocket server runtime
- `UnityClient/Assets/Scripts`: Unity gameplay/runtime systems

## Extending Gestures

1. Add new rule in `gesture_rules.py`.
2. Add cooldown in `config/default.yaml` and `power_engine.py`.
3. Add matching Unity `PowerDefinition` asset and VFX.

## Retraining ML Classifier

- Export a TFLite or ONNX classifier with compatible input features.
- Replace paths in `config/default.yaml`.
- Keep label ordering aligned with `GestureMLClassifier.labels`.

## Testing

```bash
cd PythonVision
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py'
```
