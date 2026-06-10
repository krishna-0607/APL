# User Guide

## Controls

- Stand in front of webcam.
- Perform gestures:
- `Fireball`: right fist + forward movement
- `Lightning`: index finger extended
- `Shield`: open palm
- `EnergyBlast`: both palms together
- `Teleport`: crossed arms
- `Shockwave`: jump-like acceleration spike

## Recording

- Use UI recording controls connected to `RecordingController`.
- Output files are written to `Videos/`.

## Custom Powers

- Use UI form to submit custom power profile.
- Data is persisted in SQLite (`Database/powers.db`).

## Multiplayer

- Start relay server (`app.multiplayer_relay`).
- Configure both clients to same relay URL.
- Power hit messages are synchronized.
