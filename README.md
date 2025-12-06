[![CI](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/ci.yml)
[![Hassfest](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml/badge.svg)](https://github.com/TaylorOpenLaunch/golf_dashboard/actions/workflows/hacs-validation.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/tag/TaylorOpenLaunch/golf_dashboard?label=release)](https://github.com/TaylorOpenLaunch/golf_dashboard/releases)

# Golf Dashboard for Home Assistant  
### Golf Dashboard: Unofficial NOVA Launch Monitor Integration & Dashboard Suite

Golf Dashboard provides an unofficial Home Assistant integration and a set of Lovelace dashboards designed to visualize and analyze data from a NOVA launch monitor. It enables golfers, home simulator enthusiasts, coaches, and developers to explore detailed shot analytics within Home Assistant's automation and dashboard ecosystem.

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

### Included Dashboards

Two polished dashboards are included under the dashboards/ directory.

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

### Option 1: Manual Installation (Custom Component)

1. Download or clone this repository.  
2. Copy the folder:

        custom_components/golf_dashboard

   into your Home Assistant configuration:

        config/custom_components/

3. Restart Home Assistant.  
4. Go to Settings → Devices & Services → Add Integration and search for “Golf Dashboard”.

---

### Option 2: Install via HACS (Custom Repository)

If you use HACS:

1. Open HACS → Integrations.  
2. Click the menu (⋮) → Custom repositories.  
3. Add this repository’s GitHub URL.  
4. Select category: Integration.  
5. Install the Golf Dashboard integration.  
6. Restart Home Assistant.  
7. Add the integration via Settings → Devices & Services.

---

## 📊 Dashboards

Two dashboards ship with this project and can be imported into Home Assistant.

### Dashboard files

- dashboards/nova_open_golfcoach.yaml  
- dashboards/nova_premium_analytics.yaml  

You can import them by:

- Opening your Lovelace dashboard in Home Assistant.  
- Using the Raw configuration editor or appropriate UI tools to paste or reference the YAML definitions.  

You may need to adjust entity IDs based on your installation (for example, if your NOVA device has a different entity naming pattern).

---

## 🧩 Project Structure

A high-level overview of the repository structure:

    custom_components/golf_dashboard/   → Main Home Assistant integration
    dashboards/                             → Included Lovelace dashboards
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
