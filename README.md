[![CI](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml)
[![Hassfest](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/TaylorOpenLaunch/golf_dashboard?label=release)](https://github.com/TaylorOpenLaunch/golf_dashboard/releases)

# Home Assistant Nova – OpenLaunch NOVA Integration

## Introduction
NOVA by OpenLaunch brings launch monitor data into Home Assistant with native config flow, SSDP discovery, and real-time entities fed by a WebSocket coordinator. Derived golf metrics are computed in Python so no external services are needed.

## Features
- NOVA launch monitor data exposed as Home Assistant entities (binary sensor for connectivity; sensors for speed, angles, spin, distances, and derived metrics).
- Config flow for UI setup and SSDP discovery.
- Lovelace dashboards tailored for range sessions, including an OpenGolfCoach-style view.

## Installation
- Manual: Copy `custom_components/nova_by_openlaunch` into your Home Assistant `custom_components` folder and restart Home Assistant.
- HACS: Add this repository URL as a custom repository in HACS and install the integration, then restart Home Assistant.

## Configuration
- In Home Assistant, go to Settings → Devices & Services → Add Integration and search for "NOVA by Open Launch".
- Provide host/port for your NOVA device if not auto-discovered via SSDP.
- After setup, entities for connectivity and shot/status metrics will appear.

## Dashboards
- `dashboards/nova_open_golfcoach.yaml`: Lovelace view showcasing NOVA metrics in an OpenGolfCoach-inspired layout.
- `dashboards/golf_dashboard/README.md`: Notes and placeholders for additional dashboard assets you may add.

## Documentation
- See `docs/index.md` for the documentation index, with links to architecture details and dashboard usage.

## License
MIT License. See `LICENSE` for details.
