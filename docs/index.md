# Golf Dashboard for Home Assistant (Unofficial)

This unofficial golf dashboard streams NOVA launch monitor telemetry into Home Assistant through a WebSocket-driven coordinator, SSDP discovery, and a native config flow. It is a side project and not an official OpenLaunch product.

## Quick Start
1. Install the integration (manual copy of `custom_components/golf_dashboard` or add this repo as a custom HACS integration).
2. Restart Home Assistant.
3. Configure via *Settings → Devices & Services → Add Integration* and search for **Golf Dashboard**; supply host/port if not discovered.
4. Import/use the Lovelace view from `dashboards/nova_open_golfcoach.yaml` (see `config/example_lovelace.yaml`).

## More Documentation
- [Architecture](architecture.md)
- [Open Golf Coach Dashboard](open_golf_coach.md)
- Dashboards:
  - `nova_open_golfcoach` (baseline analytics view)
  - `nova_premium_analytics` (advanced multi-column analytics view)
