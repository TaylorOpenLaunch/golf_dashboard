[![CI](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml)
[![Hassfest](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/TaylorOpenLaunch/golf_dashboard?label=release)](https://github.com/TaylorOpenLaunch/golf_dashboard/releases)

# Golf Dashboard for Home Assistant  
### Golf Dashboard: Unofficial NOVA Launch Monitor Integration & Dashboard Suite

Golf Dashboard provides an unofficial Home Assistant integration for NOVA by OpenLaunch **plus a storage-mode Lovelace dashboard** that can be created automatically via the installer action—no manual YAML dashboard edits required. Sample YAML views are shipped as optional templates under `/config/golf_dashboard/dashboards/`, but day-to-day use is entirely storage/UI based. Running the installer action once is recommended so you start with a ready-to-use dashboard.

This project is not affiliated with or endorsed by OpenLaunch or NOVA. It is maintained independently as a personal side project.

---

## 🚀 Features

### Golf Dashboard Integration (for NOVA)

- Automatic discovery via SSDP  
- Connects directly to NOVA’s local data API  
- Exposes ball-flight metrics as Home Assistant entities, including:
  - Ball speed  
  - Vertical and horizontal launch angles  
  - Spin-related values (where available)  
  - Derived metrics such as shot quality and dispersion indicators  
- Updates in near real-time for responsive dashboards  

### Included Dashboards & Installer

Two polished dashboards are bundled under `custom_components/golf_dashboard/dashboards/` and can be installed automatically via the `golf_dashboard.install_dashboards` service.

#### 1. Open Golf Coach

- Session-focused layout  
- Optimized for coaching workflows and post-shot review  
- Clean, tile-based layout for easy viewing during practice sessions  

#### 2. Premium Analytics

- Structured three-column layout  
- Focused on deeper analysis of launch parameters, spin profile, and consistency  
- Useful for dialing in equipment, practicing indoors, or simulator play  

### Home Assistant Friendly

- Native Lovelace compatibility  
- Customizable tiles and layouts  
- Works with built-in history graphs and the Home Assistant automation engine  
- Can be used to trigger automations based on shot data (for example, speed thresholds or logging)

---

## 📦 Installation

Choose one of the following installation methods.

### Install via HACS (recommended)

1. Open **HACS → Integrations**.  
2. Click the menu (⋮) → **Custom repositories**.  
3. Add `https://github.com/TaylorOpenLaunch/golf_dashboard` as a custom repository, type **Integration**.  
4. In HACS → Integrations, click **+** and search for **“Golf Dashboard”**. Install it.  
5. Restart Home Assistant if prompted.  
6. Configure your NOVA device:  
   - Go to **Settings → Devices & Services → Add integration** (if not auto-discovered) → search for **Golf Dashboard**.  
   - Follow the config flow to pick your NOVA device (SSDP/mDNS) and assign a friendly name.  

### Manual installation (advanced/alternative)

1. Download or clone this repository.  
2. Copy `custom_components/golf_dashboard` into `config/custom_components/`.  
3. Restart Home Assistant.  
4. Add the integration via **Settings → Devices & Services → Add Integration → Golf Dashboard** and complete the config flow.

---

## 📊 Creating the Golf Dashboard (storage mode)

Golf Dashboard ships with an installer action that creates a **storage-mode** Lovelace dashboard and copies example YAML templates for reference. Run the installer once after adding the integration—no `configuration.yaml` edits are required.

### Steps

1. Go to **Developer tools → Actions**.  
2. Search for **Install Golf Dashboards** (service ID: `golf_dashboard.install_dashboards`).  
3. Leave `data` empty and click **Perform action**.  
4. The service will:  
   - Create (or reuse) a storage-mode dashboard named **“Golf Dashboard”** with a URL path like `golf-dashboard`, icon `mdi:golf-tee`, sidebar-visible, and not admin-only.  
   - Add an initial view with sample NOVA entities if the dashboard is empty.  
   - Copy bundled YAML templates into `/config/golf_dashboard/dashboards/` **only if they do not already exist** (never overwrites user files).  
5. Open **Settings → Dashboards** and confirm **Golf Dashboard** appears (type: user created, method: storage/UI).  
6. Click it to open and customize like any storage-mode dashboard.  

The action is idempotent: running it again will not overwrite your dashboard and only fills in missing pieces or missing sample files.

### Bundled example YAML (reference only)

- `custom_components/golf_dashboard/dashboards/nova_open_golfcoach.yaml`  
- `custom_components/golf_dashboard/dashboards/nova_premium_analytics.yaml`  
- `custom_components/golf_dashboard/dashboards/example_lovelace.yaml`  

These are copied to `/config/golf_dashboard/dashboards/` for reference. You can import or adapt them manually in other dashboards if desired.

### Upgrading from older YAML dashboards (<= 0.2.10)

If you previously added a YAML dashboard under `lovelace.dashboards.golf_dashboard` in `configuration.yaml`, remove it to avoid conflicts and URL-path errors:

```yaml
lovelace:
  dashboards:
    golf_dashboard:        # REMOVE this whole block
      mode: yaml
      title: Golf Dashboard
      filename: golf_dashboard.yaml
      icon: mdi:golf-tee
      show_in_sidebar: true
```

- Optionally delete old `golf_dashboard.yaml` / `golf_coach.yaml` files from the root if you no longer use YAML dashboards.  
- Restart Home Assistant.  
- Run the **Install Golf Dashboards** action once to ensure the storage-mode dashboard is created.  
- The storage-mode approach is the recommended, future-proof method. The integration no longer edits `configuration.yaml`.

### Troubleshooting

- If the action fails with a YAML error, verify that `configuration.yaml` is valid (Home Assistant's YAML loader is used).  
- If you do not see **Install Golf Dashboards**: ensure the integration is installed and loaded; restart Home Assistant after installing/updating.  
- If the dashboard does not appear under **Settings → Dashboards**: run the installer again and check Home Assistant logs for `golf_dashboard` messages.

---

## 🧩 Project Structure

A high-level overview of the repository structure:

    custom_components/golf_dashboard/   → Main Home Assistant integration
    custom_components/golf_dashboard/dashboards/ → Bundled Lovelace dashboards
    docs/                                   → Documentation and architecture notes
    tests/                                  → Manifest, YAML, and readme validation tests
    .github/workflows/                      → CI, hassfest, HACS validation, release automation

---

## 🔧 Development & CI

This repository includes validation workflows to help keep the integration healthy and compatible.

### GitHub Actions Workflows

- ci.yml – Syntax checks, compile checks, and pytest  
- hassfest.yaml – Home Assistant integration validation  
- hacs-validation.yaml – HACS metadata checks  
- release.yaml – Automatic release generation triggered by git tags  

### Tests

Tests cover:

- Manifest and HACS JSON correctness  
- Dashboard YAML validity  
- README and documentation content presence  

To run tests locally from the repository root:

    pytest -q

---

## 🔖 Versioning & Releases

Versioning follows a simple semantic-style approach:

- VERSION in the repository root tracks the current version.  
- manifest.json maintains a matching version field.  
- CHANGELOG.md records changes across releases.  
- Git tags such as v0.2.0 automatically create GitHub releases using the release.yaml workflow.

---

## ⚠️ Disclaimer

- This is an unofficial NOVA project, not an OpenLaunch or NOVA product.  
- No warranty, guarantee, or official support is provided.  
- Functionality may change at any time.  
- Use at your own discretion.

---

## ❤️ Acknowledgements

Thanks to the Home Assistant open-source community for architecture patterns, tooling, and documentation that make custom integrations possible.
