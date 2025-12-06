# Architecture Overview

## Data Flow
- NOVA hardware exposes a WebSocket endpoint (default port 2920). The integration connects to the device to receive JSON shot and status messages.
- `config_flow.py` handles UI setup and SSDP discovery, creating config entries with host/port/device info.
- `__init__.py` boots the coordinator and forwards platforms for sensors/binary sensors.
- `NovaByOpenLaunchCoordinator` (`custom_components/nova_by_openlaunch/coordinator.py`) maintains the WebSocket connection, reconnects on drop, and parses incoming payloads.
- `derived.py` augments shot payloads with calculated metrics (carry/total distance, shot type/rank/color, backspin/sidespin, etc.) so entities can expose both raw and computed values.
- Coordinator stores latest status and shot data in shared state, which entities consume via the update coordinator.

## Entities
- Binary sensor: connectivity status of the NOVA device.
- Sensors: raw and derived metrics including ball speed, vertical/horizontal launch angles, spin, carry/total/offset distances, club speed, smash factor, shot classification, and more. See `const.py`/`sensor.py` for the catalog.

## Components
- `config_flow.py`: user setup, SSDP discovery, validation of device connectivity.
- `__init__.py`: entry setup/unload and platform forwarding.
- `coordinator.py`: connection lifecycle, parsing, and state distribution to entities.
- `sensor.py` and `binary_sensor.py`: entity definitions tied to coordinator data.
- `derived.py`: helper functions that compute secondary metrics.

## Extending Metrics
- Add new sensor descriptors in `const.py` and map incoming payload fields.
- Extend `derived.py` if new calculated metrics are needed; ensure coordinator merges them into shot data.
- Wire new descriptors into `sensor.py` so entities are created automatically.

Additional diagrams and deeper protocol details can be added as the integration evolves.
