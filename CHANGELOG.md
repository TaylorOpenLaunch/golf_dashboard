# Changelog

## 0.2.7
- Added mDNS (zeroconf) discovery support using _openapi-nova._tcp.local. and _openlaunch-ws._tcp.local.
- SSDP discovery remains supported.
- Improved discovery confirmation flow and description placeholders.

## 0.2.6
- Patch release to update Golf Dashboard in HACS.

## 0.2.5
- Improved connection validation in config flow.
- Automatic fallback between ports 2920 and 2921 before failing.

## 0.2.4
- Fix discovery flow translation placeholder for device name.
- Auto-install dashboards option still behaves as before.

## 0.2.3
- Automated release version bump.

## 0.2.0
- Add Golf Dashboard premium analytics dashboard.
- Polish README and documentation (index, architecture, Open Golf Coach).
- Add basic unit tests for manifest, HACS metadata, dashboards, and docs.
- Integrate pytest into CI alongside Python syntax checks.

## 0.1.0
- Initial public structure of the Golf Dashboard integration and dashboard files.
