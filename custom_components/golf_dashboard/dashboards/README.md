# Golf Dashboard Assets

This directory is reserved for Golf Dashboard assets (cards, images, or additional Lovelace views). Add your dashboard files here if available.

## Golf Dashboard Premium Analytics (`custom_components/golf_dashboard/dashboards/nova_premium_analytics.yaml`)
- A TrackMan-style, three-column analytics view for simulator sessions.
- Columns:
  - Session overview: shot count, last shot time, ball speed, carry/total distance, club speed.
  - Launch & spin: launch angles, offline, spin components, trajectory/delivery metrics.
  - Shot quality & dispersion: shot type/rank/color, quality score, recommendations, carry vs offline trends.
- To import/use:
  - Run the `golf_dashboard.install_dashboards` service to copy templates into `/config/` and register dashboards automatically, **or**
  - open the Raw Configuration Editor for a dashboard/view and paste the YAML, or copy the file into `/config/` and reference it as a YAML-mode dashboard (see `custom_components/golf_dashboard/dashboards/example_lovelace.yaml`).
