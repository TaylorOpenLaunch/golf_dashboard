# NOVA by OpenLaunch – Home Assistant Docs

NOVA by OpenLaunch streams launch monitor telemetry into Home Assistant through a WebSocket-driven coordinator, SSDP discovery, and a native config flow.

## Quick Start
1. Install the integration (manual copy of `custom_components/nova_by_openlaunch` or add this repo as a custom HACS integration).
2. Restart Home Assistant.
3. Configure via *Settings → Devices & Services → Add Integration* and search for **NOVA by Open Launch**; supply host/port if not discovered.
4. Import/use the Lovelace view from `dashboards/nova_open_golfcoach.yaml` (see `config/example_lovelace.yaml`).

## More Documentation
- [Architecture](architecture.md)
- [Open Golf Coach Dashboard](open_golf_coach.md)
- Dashboards:
  - `nova_open_golfcoach` (baseline analytics view)
  - `nova_premium_analytics` (advanced TrackMan-style analytics view)
