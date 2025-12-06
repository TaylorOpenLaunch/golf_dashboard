# Open Golf Coach Dashboard

Open Golf Coach is part of the Golf Dashboard project for Home Assistant (built for NOVA launch monitors).

The Open Golf Coach dashboard is a Lovelace view tailored for Golf Dashboard data. It highlights raw and derived shot metrics in a tablet-friendly layout.

## Dashboard File
- Path: `dashboards/nova_open_golfcoach.yaml`
- Purpose: Presents NOVA shot data (speed, angles, spin) and derived metrics (carry/total distance, offline, club speed, smash factor, shot type/rank/color).
- Typical layout: shot summary cards, key metrics tiles, and derived KPIs suited for range or simulator tablets.

## How to Use
1. Ensure the Golf Dashboard integration is installed and configured so the entities are available (binary sensor + sensor entities from `const.py`/`sensor.py`).
2. Copy `dashboards/nova_open_golfcoach.yaml` into your Home Assistant `/config/dashboards/` (or adjust the path to your setup).
3. In `configuration.yaml` or `ui-lovelace.yaml`, add a dashboard entry pointing to this file (see `config/example_lovelace.yaml` for a template).
4. Reload Lovelace resources or restart Home Assistant to load the view.

## Expected Entities
- Connectivity binary sensor.
- Sensors for ball speed, launch angles, spin metrics, distances (carry/total/offline), club speed, smash factor, shot type/rank/color, and related status fields.

## Troubleshooting
- Missing entities: confirm the integration is configured and receiving shot data; check Logs for connection errors.
- Empty cards: ensure entity IDs match the defaults created by the integration (re-add the integration if IDs changed).
- Path issues: verify the dashboard file path in your Lovelace configuration matches where you placed `nova_open_golfcoach.yaml`.
- Data not updating: make sure the NOVA device is online and reachable; restart the integration if the WebSocket disconnects.

## Premium analytics view
For a more advanced, TrackMan-style layout, see `dashboards/nova_premium_analytics.yaml`. Import it as a separate Lovelace view to pair with or replace the Open Golf Coach view when you want deeper session analytics.
