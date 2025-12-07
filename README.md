[![CI](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml)
[![Hassfest](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/TaylorOpenLaunch/golf_dashboard?label=release)](https://github.com/TaylorOpenLaunch/golf_dashboard/releases)

# Golf Dashboard for Home Assistant  
### Golf Dashboard: Unofficial NOVA Launch Monitor Integration & Dashboard Suite

Golf Dashboard provides an unofficial Home Assistant integration for NOVA by OpenLaunch **plus a storage-mode Lovelace dashboard** created automatically via the installer action—no manual `configuration.yaml` edits required. Sample YAML views are provided as optional templates under `/config/golf_dashboard/dashboards/`, but day-to-day use is entirely storage/UI based. Running the installer action once is recommended so you start with a ready-to-use dashboard.

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

Three polished dashboards are bundled under `custom_components/golf_dashboard/dashboards/` and can be installed automatically via the `golf_dashboard.install_dashboards` service.

#### 1. Open Golf Coach

- Session-focused layout  
- Optimized for coaching workflows and post-shot review  
- Clean, tile-based layout for easy viewing during practice sessions  

#### 2. Premium Analytics

- Structured three-column layout  
- Focused on deeper analysis of launch parameters, spin profile, and consistency  
- Useful for dialing in equipment, practicing indoors, or simulator play  

#### 3. NOVA Premium Shot (Hero Card)

- Shot-focused layout with hero summary  
- Launch, spin, club delivery, trajectory, and quick trends in one view  
- Ideal for at-a-glance review after each shot  

### Home Assistant Friendly

- Native Lovelace compatibility  
- Customizable tiles and layouts  
- Works with built-in history graphs and the Home Assistant automation engine  
- Can be used to trigger automations based on shot data (for example, speed thresholds or logging)

---

## 📦 Installation

Choose one of the following installation methods.

### Installation via HACS (recommended)

1. Open **HACS → Integrations**.  
2. Click the menu (⋮) → **Custom repositories**.  
3. Add the repository URL: `https://github.com/TaylorOpenLaunch/golf_dashboard` and set the type to **Integration**.  
4. In HACS → Integrations, click **+** and search for **“Golf Dashboard”**. Install it.  
5. Restart Home Assistant if prompted.  
6. Configure the NOVA device:  
   - Go to **Settings → Devices & services → Add integration** (if not auto-discovered) → search for **Golf Dashboard**.  
   - Follow the config flow to pick your NOVA device (SSDP/mDNS discovery) and assign a friendly name.

### Manual installation (alternative)

1. Download or clone this repository.  
2. Copy the folder `custom_components/golf_dashboard` into `config/custom_components/`.  
3. Restart Home Assistant.  
4. Add the integration via **Settings → Devices & Services → Add Integration → Golf Dashboard** and complete the config flow.

---

## 📊 Creating the Golf Dashboard (storage mode)

Golf Dashboard ships with an installer action that creates a storage-mode Lovelace dashboard and copies example YAML templates for reference. Run the installer once after adding the integration.

### Steps

1. Open **Developer Tools → Actions** in Home Assistant.  
2. In the action selector, search for **Install Golf Dashboards** (`golf_dashboard.install_dashboards`).  
3. Leave the data empty and click **Perform action**.  
4. The installer will:
   - Create (or reuse) a storage-mode dashboard named **“Golf Dashboard”** (url_path `golf_dashboard`, icon `mdi:golf-tee`, sidebar-visible, not admin-only).  
   - Add an initial view with sample NOVA entities if the dashboard is empty.  
   - Copy example YAML templates into `/config/golf_dashboard/dashboards/` **only if they do not already exist**; it never overwrites user files.  
   - Auto-detect your NOVA device slug (for example `nova` or `nova_123456`) and rewrite `sensor.golf_dashboard_*` placeholders in templates to the detected slug.  
5. To open it: go to **Settings → Dashboards** and look for **Golf Dashboard** (type: user created, method: storage/UI). Optionally enable **Show in sidebar**.
6. If Lovelace storage dashboards are not available yet (for example immediately after a restart), the action logs a warning and exits without changes—restart Home Assistant and try again later.

Running the installer again is safe: it will not overwrite your existing dashboard and only copies missing example files.

### Bundled example YAML (reference only)

- `custom_components/golf_dashboard/dashboards/nova_open_golfcoach.yaml`  
- `custom_components/golf_dashboard/dashboards/nova_premium_analytics.yaml`  
- `custom_components/golf_dashboard/dashboards/nova_premium_shot.yaml`  
- `custom_components/golf_dashboard/dashboards/example_lovelace.yaml`  

These are copied to `/config/golf_dashboard/dashboards/` for reference. The installer auto-detects your NOVA slug and rewrites `sensor.golf_dashboard_*` placeholders when copying, so you should not need to edit entity_ids manually. To use them manually:

- Create a storage-mode dashboard in Home Assistant (e.g., **Nova Premium Analytics** with path `nova-premium-analytics` for the premium template).  
- Open the **Raw configuration editor** for that dashboard and paste the YAML from the template.  
- If you customize by hand, replace `golf_dashboard` in all `entity` references with the NOVA slug Home Assistant generated for your device (for example: `sensor.nova_by_open_launch_ball_speed`).  
- The premium templates include a top-level `views:` array and a path suitable for storage-mode dashboards.  
  
### Recommended NOVA device naming

- The installer auto-detects your NOVA slug from existing sensors (for example `sensor.nova_ball_speed` or `sensor.nova_123456_ball_speed`).  
- For best results, name or select the NOVA device whose entities use the `sensor.nova_*` or `sensor.nova_<serial>_*` pattern; the installer will rewrite placeholders automatically.  
- Manual find/replace of entity_ids is no longer required for normal use.  

### Troubleshooting

- If the action fails, check Home Assistant logs for `golf_dashboard` messages and ensure the integration is installed/loaded; a restart after installing/updating can help.  
- If you do not see **Install Golf Dashboards**: ensure the integration is installed and loaded; restart Home Assistant after installing/updating.  
- If the dashboard does not appear under **Settings → Dashboards**: run the installer again and check the Home Assistant logs for `golf_dashboard` messages. If Lovelace storage is not ready, the installer logs a warning and exits safely—restart and try again.

### Legacy cleanup (older YAML dashboards <= 0.2.10)

Older releases used YAML-mode dashboards. If you still have a `lovelace.dashboards.golf_dashboard` block in `configuration.yaml`, you can remove it to avoid conflicts (current releases do not modify `configuration.yaml`):

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

Optionally delete old `golf_dashboard.yaml` / `golf_coach.yaml` files from the root if you no longer use YAML dashboards. After cleanup, run the installer action once to ensure the storage-mode dashboard exists.

### Open GolfCoach dashboard

The Open GolfCoach dashboard provides a coaching-oriented layout with sections for raw launch data, derived ball-flight metrics, shot classification, distance/spin history, tour benchmarks, shot quality, club delivery estimates, trajectory, and optimal windows. It uses `sensor.golf_dashboard_*` placeholders; during installation these are rewritten to the detected NOVA slug automatically.

### Distances are now reported in yards

All distance-oriented sensors (carry, total, offline, benchmarks, and deltas) are now published in yards. Dashboard labels have been updated to match; no configuration changes are needed.

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

The Golf Dashboard integration follows semantic versioning (MAJOR.MINOR.PATCH) using the `VERSION` file at the repository root and the `version` field in `custom_components/golf_dashboard/manifest.json`.

- **VERSION and manifest** must always match.  
- **MAJOR**: breaking changes to the integration or configuration.  
- **MINOR**: new features that are backwards compatible.  
- **PATCH**: bug fixes or documentation/tooling-only changes.  

Starting with **0.2.16**, a GitHub Actions workflow automatically:

1. Reads the current value of `VERSION` on pushes to `main`.  
2. Creates a Git tag `vX.Y.Z` if it does not already exist.  
3. Creates a GitHub Release for that tag with auto-generated release notes.  

Releases that only touch documentation or tooling (like 0.2.16) should be treated as PATCH releases.

---

## ⚠️ Disclaimer

- This is an unofficial NOVA project, not an OpenLaunch or NOVA product.  
- No warranty, guarantee, or official support is provided.  
- Functionality may change at any time.  
- Use at your own discretion.

---

## ❤️ Acknowledgements

Thanks to the Home Assistant open-source community for architecture patterns, tooling, and documentation that make custom integrations possible.
