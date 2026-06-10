# WebSocket API

## Vision Server (`ws://host:8765`)

### Server to Client

- `{"type":"connected","ts":<unix_ts>}`
- `{"type":"power_trigger","power":"Fireball","confidence":0.86,"timestamp":..., "state":"active"}`
- `{"type":"cooldown","power":"Fireball","remaining":1.21,"timestamp":...}`
- `{"type":"custom_powers","powers":[...]}`
- `{"type":"custom_power_saved","power":{...}}`
- `{"type":"custom_power_generated","power":{...}}`

### Client to Server

- Create custom power:
```json
{
  "type": "create_custom_power",
  "name": "Dragon Flame",
  "primary_color": "#FF5500",
  "secondary_color": "#FFD000",
  "particle_profile": "fire_trail",
  "sound_profile": "dragon_roar"
}
```

- List custom powers:
```json
{
  "type": "list_custom_powers"
}
```

- Generate and save custom power from name:
```json
{
  "type": "generate_custom_power",
  "name": "Dragon Flame"
}
```

## Multiplayer Relay (`ws://host:9000`)

### Client to Relay

```json
{"type":"power_hit","power":"EnergyBlast","damage":28.5}
```

### Relay Broadcast

```json
{"type":"damage_event","power":"EnergyBlast","damage":28.5}
```
