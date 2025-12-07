# Changelog

## 0.2.15
- Maintenance release: docs and metadata only; no behavior changes compared to 0.2.14.

## 0.2.14
- Hardened installer: if Lovelace storage dashboards are unavailable, `golf_dashboard.install_dashboards` now logs a warning and exits safely instead of raising an error.
- Storage-mode behavior remains unchanged; no configuration.yaml access.
- Documentation updated for the safer installer behavior.
## 0.2.13
- Clarified README to emphasize storage-mode dashboard creation via the `golf_dashboard.install_dashboards` action and optional sample YAML templates.
- Added upgrade notes for removing legacy YAML `lovelace.dashboards.golf_dashboard` entries when migrating from older versions.
- No code changes; behavior remains the same as 0.2.11/0.2.12.

## 0.2.12
- Clarified README instructions for installing the Golf Dashboard via `golf_dashboard.install_dashboards`.
- Documented storage-mode Lovelace dashboard behavior and example YAML templates.

## 0.2.11
- Switched dashboard installer to use Home Assistant's Lovelace Storage Mode API.
- Automatically creates a "Golf Dashboard" under `/lovelace/golf_dashboard` (UI-controlled, not YAML).
- Adds a starter view with sample Nova sensor cards when empty.
- Copies template YAML files only to `/config/golf_dashboard/dashboards/` without touching existing dashboards.
- No edits occur to configuration.yaml.
- Fully idempotent installation. Re-running the service does not change user dashboards.
- Updated service description.
- Updated manifest to version 0.2.11.

## 0.2.9
- Hardened the Golf Dashboard installer service (`golf_dashboard.install_dashboards`).
- Automatically creates `/config/golf_dashboard.yaml` and registers the `golf_dashboard` Lovelace dashboard.
- Ensures template dashboards are copied without overwriting user files.
- Improved error handling using `HomeAssistantError` so failures show clear messages in the UI.

## 0.2.8
- Hardened the Golf Dashboard installer service (`golf_dashboard.install_dashboards`):
  - Safely creates `golf_dashboard.yaml` and `golf_coach.yaml` from bundled templates.
  - Updates or creates Lovelace dashboard entries in `configuration.yaml` without overwriting existing customizations.
  - Uses clear `HomeAssistantError` messages and logging instead of generic "Unknown error".
- Ready for production use via HACS.

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
