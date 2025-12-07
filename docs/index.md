# Golf Dashboard for Home Assistant (Unofficial)

Golf Dashboard streams NOVA launch monitor telemetry into Home Assistant through a WebSocket-driven coordinator, SSDP discovery, and a native config flow. It is a side project and not an official OpenLaunch product.

## Quick Start
1. Install the integration (manual copy of `custom_components/golf_dashboard` or add this repo as a custom HACS integration).
2. Restart Home Assistant.
3. Configure via *Settings → Devices & Services → Add Integration* and search for **Golf Dashboard**; supply host/port if not discovered.
4. (Recommended) Run the service `golf_dashboard.install_dashboards` from **Developer Tools → Services** to copy bundled dashboards into `/config` and register YAML dashboards automatically.
5. Manual option: import/use the Lovelace view from `custom_components/golf_dashboard/dashboards/nova_open_golfcoach.yaml` (see `custom_components/golf_dashboard/dashboards/example_lovelace.yaml`).

## More Documentation
- [Architecture](architecture.md)
- [Open Golf Coach Dashboard](open_golf_coach.md)
- Dashboards:
  - `nova_open_golfcoach` (baseline analytics view)
  - `nova_premium_analytics` (advanced multi-column analytics view)
