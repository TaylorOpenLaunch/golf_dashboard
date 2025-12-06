# Home Assistant Nova – OpenLaunch NOVA Integration

Home Assistant Nova brings OpenLaunch NOVA launch monitor data into Home Assistant. It includes a config flow for discovery/setup, real-time sensors derived from shot data, and Lovelace dashboards tailored for golf sessions.

## Installation

1. Copy the `custom_components/nova_by_openlaunch` directory into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Configure the integration via the UI (Settings → Devices & Services → Add Integration → search for "NOVA by Open Launch").

## Dashboards

- `dashboards/nova_open_golfcoach.yaml`: Lovelace view showcasing the NOVA metrics in an OpenGolfCoach-inspired layout.
- `dashboards/golf_dashboard/`: Supporting assets or additional dashboards for the NOVA experience (add your own files here).

## Development

- The coordinator manages WebSocket connectivity and pushes updates to sensors/binary sensors.
- Derived metrics are calculated in Python so no extra dependencies are needed.
- A basic CI workflow runs lint checks with Ruff/Flake8 on pushes/PRs.

## License

MIT License. See `LICENSE` for details.
