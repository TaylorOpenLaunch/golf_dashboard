# Changelog

## 0.2.9
- Made the dashboard installer service (golf_dashboard.install_dashboards) robust and idempotent.
- Automatically creates /config/golf_dashboard.yaml including the bundled Golf Coach and Premium Analytics views.
- Automatically registers the golf_dashboard YAML Lovelace dashboard in configuration.yaml without overwriting user customizations.
- Improves error handling using HomeAssistantError so failures report clearly in the UI instead of “Unknown error”.

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
