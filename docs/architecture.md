# Architecture Overview

## Coordinator
- `NovaByOpenLaunchCoordinator` maintains the WebSocket connection to the NOVA device, retries on disconnects, and broadcasts shot/status messages to entities.
- It enriches payloads with derived metrics so entities can expose both raw and computed values without extra dependencies.

## Entities
- Binary sensor reports connectivity status.
- Sensor entities cover raw metrics (speed, angles, spin, distances) plus derived statistics (carry/total distance, shot type, rank, color, etc.).

## Data Flow
1. Config flow (manual or SSDP discovery) stores connection info.
2. Coordinator connects to the device and parses incoming JSON.
3. Derived helpers augment shot data; coordinator updates Home Assistant data.
4. Entities subscribed to the coordinator publish state updates to Home Assistant.

Additional diagrams and deeper protocol details can be added here as the integration matures.
