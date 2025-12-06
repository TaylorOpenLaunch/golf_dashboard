[![CI](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml)
[![Hassfest](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/TaylorOpenLaunch/golf_dashboard?label=release)](https://github.com/TaylorOpenLaunch/golf_dashboard/releases)

# Golf Dashboard for Home Assistant (Unofficial NOVA project)

This repository contains an unofficial Home Assistant dashboard and integration config for experimenting with golf simulator data from a NOVA launch monitor. It is a personal side project by Taylor Hargrave and is **not an official OpenLaunch or NOVA product**. Use it if you want to tinker, build dashboards, and explore golf analytics in Home Assistant.

## Features
- Real-time NOVA ball-flight data as Home Assistant entities (connectivity binary sensor plus sensors for ball speed, launch angles, spin, distances, and derived metrics).
- Derived metrics (carry/total distance, offline, club speed, smash factor, shot classification) computed locally in Python.
- Built-in Lovelace dashboards, including the `nova_open_golfcoach` analytics view.
- Open, dev-friendly structure with docs, dashboards, and CI workflows.

## Disclaimer
- This project is **unofficial** and maintained as a personal side project.
- It is not affiliated with or endorsed by OpenLaunch or NOVA as an official product.
- Functionality and support are best-effort and may change at any time.

## Installation

**Manual install (custom component)**
1. Copy `custom_components/nova_by_openlaunch` into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Go to *Settings → Devices & services* and add **NOVA by OpenLaunch**.

**Install via HACS (custom repository)**
1. In HACS → Integrations → three-dots menu → *Custom repositories*.
2. Add `https://github.com/TaylorOpenLaunch/golf_dashboard` with category `Integration`.
3. Install **NOVA by OpenLaunch** from HACS.
4. Restart Home Assistant.
5. Configure from *Settings → Devices & services*.

## Configuration
- Provide the NOVA host/IP and port if SSDP discovery does not find it automatically.
- After setup, entities appear under the NOVA device (connectivity + shot/status sensors and derived metrics).
- Re-run the config flow if connection details change.

## Dashboards
- `dashboards/nova_open_golfcoach.yaml`: Standard Open Golf Coach-style view for core analytics.
- `dashboards/nova_premium_analytics.yaml`: Premium analytics layout (TrackMan-style) with three columns for overview, launch/spin, and shot quality/dispersion.
- `dashboards/golf_dashboard/README.md`: Notes/space for additional dashboard assets or future expansions.

## Development
- Integration code lives in `custom_components/nova_by_openlaunch/` (config flow, coordinator, entities, derived metrics).
- See `docs/architecture.md` for an overview; contributions and PRs are welcome.
- CI runs syntax checks; hassfest and HACS validation workflows are included.

## Documentation
- [Docs index](docs/index.md)
- [Architecture](docs/architecture.md)
- [Open Golf Coach dashboard](docs/open_golf_coach.md)

## License
MIT License. See [LICENSE](LICENSE).
