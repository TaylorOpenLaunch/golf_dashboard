"""Regression tests for NOVA benchmark math (Amateur / LPGA / Tour)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DERIVED_PATH = ROOT / "custom_components" / "golf_dashboard" / "derived.py"

spec = importlib.util.spec_from_file_location("golf_dashboard_derived_benchmark", DERIVED_PATH)
derived = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = derived
spec.loader.exec_module(derived)  # type: ignore[attr-defined]


def _expected_benchmarks(club_speed_mps: float) -> dict[str, float]:
    tour_carry_yards = club_speed_mps * derived.THEORETICAL_CARRY_PER_MPS * derived.METERS_TO_YARDS
    tour_total_yards = tour_carry_yards * 1.05
    return {
        "tour_carry_yards": tour_carry_yards,
        "tour_total_yards": tour_total_yards,
        "amateur_carry_yards": tour_carry_yards * 0.80,
        "lpga_carry_yards": tour_carry_yards * 0.90,
        "amateur_total_yards": tour_total_yards * 0.80,
        "lpga_total_yards": tour_total_yards * 0.90,
    }


SHOT_CASES = [
    {
        "id": "driver_profile",
        "ball_speed_mps": 70.0,
        "vla_deg": 12.5,
        "hla_deg": 0.0,
        "total_spin_rpm": 2800.0,
        "spin_axis_deg": 5.0,
    },
    {
        "id": "mid_iron_profile",
        "ball_speed_mps": 50.0,
        "vla_deg": 17.0,
        "hla_deg": 1.0,
        "total_spin_rpm": 5500.0,
        "spin_axis_deg": -4.0,
    },
    {
        "id": "wedge_profile",
        "ball_speed_mps": 35.0,
        "vla_deg": 30.0,
        "hla_deg": -1.5,
        "total_spin_rpm": 8500.0,
        "spin_axis_deg": 3.0,
    },
]


@pytest.mark.parametrize("case", SHOT_CASES, ids=[c["id"] for c in SHOT_CASES])
def test_benchmark_profiles_regression(case: dict[str, float]) -> None:
    result = derived.compute_derived_from_shot(
        case["ball_speed_mps"],
        case["vla_deg"],
        case["hla_deg"],
        case["total_spin_rpm"],
        case["spin_axis_deg"],
    )

    club_speed_mps = result["club_speed_meters_per_second"]
    expected = _expected_benchmarks(club_speed_mps)

    # Benchmark carries and totals
    assert result["tour_carry_yards"] == pytest.approx(expected["tour_carry_yards"], abs=1e-6)
    assert result["tour_total_yards"] == pytest.approx(expected["tour_total_yards"], abs=1e-6)
    assert result["amateur_carry_yards"] == pytest.approx(expected["amateur_carry_yards"], abs=1e-6)
    assert result["amateur_total_yards"] == pytest.approx(expected["amateur_total_yards"], abs=1e-6)
    assert result["lpga_carry_yards"] == pytest.approx(expected["lpga_carry_yards"], abs=1e-6)
    assert result["lpga_total_yards"] == pytest.approx(expected["lpga_total_yards"], abs=1e-6)

    # Carry deltas vs benchmarks
    carry_yards = result["carry_distance_yards"]
    assert result["carry_delta_to_tour_yards"] == pytest.approx(
        carry_yards - expected["tour_carry_yards"], abs=1e-6
    )
    assert result["carry_delta_to_amateur_yards"] == pytest.approx(
        carry_yards - expected["amateur_carry_yards"], abs=1e-6
    )
    assert result["carry_delta_to_lpga_yards"] == pytest.approx(
        carry_yards - expected["lpga_carry_yards"], abs=1e-6
    )
