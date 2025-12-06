# Golf Dashboard Assets

This directory is reserved for NOVA golf dashboard assets (cards, images, or additional Lovelace views). Add your dashboard files here if available.

## NOVA Premium Analytics (`dashboards/nova_premium_analytics.yaml`)
- A TrackMan-style, three-column analytics view for simulator sessions.
- Columns:
  - Session overview: shot count, last shot time, ball speed, carry/total distance, club speed.
  - Launch & spin: launch angles, offline, spin components, trajectory/delivery metrics.
  - Shot quality & dispersion: shot type/rank/color, quality score, recommendations, carry vs offline trends.
- To import/use:
  - In Home Assistant, open the Raw Configuration Editor for a dashboard/view and paste the YAML, or place the file under `/config/dashboards/` and reference it as a YAML-mode dashboard (see `config/example_lovelace.yaml`).
