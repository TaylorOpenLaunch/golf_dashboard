# NOVA by OpenLaunch – Home Assistant Integration

NOVA by OpenLaunch brings launch monitor telemetry into Home Assistant via a native config flow, SSDP discovery, and a WebSocket-driven coordinator that feeds entities and dashboards.

## Quick Start
1. Install: Copy `custom_components/nova_by_openlaunch` into `custom_components` or add this repository as a custom repo in HACS and install from there.
2. Restart Home Assistant.
3. Configure: Settings → Devices & Services → Add Integration → search for "NOVA by Open Launch"; provide host/port if not auto-discovered.
4. Dashboards: Add the Lovelace view from `dashboards/nova_open_golfcoach.yaml` (see `config/example_lovelace.yaml`).

## Documentation
- [Architecture](architecture.md)
- [Open Golf Coach Dashboard](open_golf_coach.md)
