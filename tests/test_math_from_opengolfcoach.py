"""Cross-check NOVA derived math against open-golf-coach reference logic."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import NamedTuple

import pytest

ROOT = Path(__file__).resolve().parents[1]
DERIVED_PATH = ROOT / "custom_components" / "golf_dashboard" / "derived.py"

spec = importlib.util.spec_from_file_location("golf_dashboard_derived", DERIVED_PATH)
derived = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = derived
spec.loader.exec_module(derived)  # type: ignore[attr-defined]


class ImpactBand(NamedTuple):
    max_ball_speed_mps: float
    base_cor: float
    optimal_launch_deg: float
    launch_tolerance_deg: float
    optimal_spin_rpm: float
    spin_tolerance_rpm: float
    face_influence_ratio: float
    spin_axis_gain: float


IMPACT_BANDS: tuple[ImpactBand, ...] = (
    ImpactBand(40.0, 0.55, 28.0, 15.0, 9000.0, 4000.0, 0.65, 1.7),
    ImpactBand(50.0, 0.66, 20.0, 12.0, 7000.0, 2500.0, 0.72, 2.1),
    ImpactBand(60.0, 0.72, 16.0, 10.0, 5000.0, 2000.0, 0.78, 2.4),
    ImpactBand(float("inf"), 0.83, 12.0, 8.0, 2500.0, 1500.0, 0.85, 2.8),
)

BALL_MASS_KG = 0.04593
CLUBHEAD_MASS_KG = 0.200
DRIVER_COR_LIMIT = 0.83
MIN_EFFECTIVE_COR = 0.52
METERS_TO_YARDS = derived.METERS_TO_YARDS
THEORETICAL_CARRY_PER_MPS = derived.THEORETICAL_CARRY_PER_MPS


def _select_impact_band(ball_speed_mps: float) -> ImpactBand:
    for band in IMPACT_BANDS:
        if ball_speed_mps <= band.max_ball_speed_mps:
            return band
    return IMPACT_BANDS[-1]


def _estimate_club_speed_ref(ball_speed_mps: float, vertical_launch_angle_deg: float, total_spin_rpm: float) -> float:
    band = _select_impact_band(max(ball_speed_mps, 5.0))
    launch_angle = max(-5.0, min(vertical_launch_angle_deg, 70.0))
    spin_rpm = max(total_spin_rpm, 0.0)

    launch_deviation = abs(launch_angle - band.optimal_launch_deg)
    normalized_launch = min(launch_deviation / band.launch_tolerance_deg, 3.0)
    launch_penalty = normalized_launch**1.25 * 0.06

    spin_tolerance = max(band.spin_tolerance_rpm, 1.0)
    if spin_rpm >= band.optimal_spin_rpm:
        normalized_spin = min((spin_rpm - band.optimal_spin_rpm) / spin_tolerance, 3.0)
    else:
        normalized_spin = min((band.optimal_spin_rpm - spin_rpm) / (spin_tolerance * 1.5), 3.0)
    spin_penalty = normalized_spin**1.15 * 0.08

    knuckle_penalty = ((1200.0 - spin_rpm) / 1200.0) ** 1.3 * 0.05 if spin_rpm < 1200.0 else 0.0

    effective_cor = band.base_cor - launch_penalty - spin_penalty - knuckle_penalty
    effective_cor = max(MIN_EFFECTIVE_COR, min(effective_cor, DRIVER_COR_LIMIT))

    mass_ratio = BALL_MASS_KG / CLUBHEAD_MASS_KG
    smash_from_cor = (1.0 + effective_cor) / (1.0 + mass_ratio)
    return ball_speed_mps / smash_from_cor


def _estimate_face_path_ref(ball_speed_mps: float, hla_deg: float, spin_axis_deg: float) -> dict[str, float]:
    band = _select_impact_band(max(ball_speed_mps, 5.0))
    face_to_path_deg = spin_axis_deg / band.spin_axis_gain
    club_path_deg = hla_deg - band.face_influence_ratio * face_to_path_deg
    club_face_deg = club_path_deg + face_to_path_deg
    return {
        "club_path_degrees": club_path_deg,
        "club_face_to_path_degrees": face_to_path_deg,
        "club_face_to_target_degrees": club_face_deg,
    }


def _compute_benchmarks_ref(club_speed_mps: float) -> dict[str, float]:
    tour_carry_yards = club_speed_mps * THEORETICAL_CARRY_PER_MPS * METERS_TO_YARDS
    tour_total_yards = tour_carry_yards * 1.05
    amateur_carry = tour_carry_yards * 0.80
    lpga_carry = tour_carry_yards * 0.90
    return {
        "tour_carry_yards": tour_carry_yards,
        "tour_total_yards": tour_total_yards,
        "amateur_carry_yards": amateur_carry,
        "lpga_carry_yards": lpga_carry,
        "amateur_total_yards": tour_total_yards * 0.80,
        "lpga_total_yards": tour_total_yards * 0.90,
    }


SHOT_CASES = [
    {"ball_speed_mps": 70.0, "vla_deg": 12.5, "hla_deg": -2.0, "total_spin_rpm": 2800.0, "spin_axis_deg": 15.0},
    {"ball_speed_mps": 45.0, "vla_deg": 18.0, "hla_deg": 1.0, "total_spin_rpm": 6200.0, "spin_axis_deg": -5.0},
    {"ball_speed_mps": 55.0, "vla_deg": 14.0, "hla_deg": 0.0, "total_spin_rpm": 4500.0, "spin_axis_deg": -8.0},
    {"ball_speed_mps": 30.0, "vla_deg": 30.0, "hla_deg": -3.0, "total_spin_rpm": 8500.0, "spin_axis_deg": 3.0},
]


@pytest.mark.parametrize("shot", SHOT_CASES)
def test_math_matches_open_golf_coach_reference(shot):
    derived_values = derived.compute_derived_from_shot(
        shot["ball_speed_mps"],
        shot["vla_deg"],
        shot["hla_deg"],
        shot["total_spin_rpm"],
        shot["spin_axis_deg"],
    )

    club_speed_ref = _estimate_club_speed_ref(shot["ball_speed_mps"], shot["vla_deg"], shot["total_spin_rpm"])
    smash_ref = shot["ball_speed_mps"] / club_speed_ref
    assert derived_values["club_speed_meters_per_second"] == pytest.approx(club_speed_ref, abs=0.01)
    assert derived_values["smash_factor"] == pytest.approx(smash_ref, abs=0.01)

    face_path_ref = _estimate_face_path_ref(shot["ball_speed_mps"], shot["hla_deg"], shot["spin_axis_deg"])
    assert derived_values["face_angle_deg"] == pytest.approx(
        face_path_ref["club_face_to_target_degrees"], abs=0.01
    )
    assert derived_values["face_to_path_deg"] == pytest.approx(
        face_path_ref["club_face_to_path_degrees"], abs=0.01
    )
    assert derived_values["club_path_deg"] == pytest.approx(face_path_ref["club_path_degrees"], abs=0.01)

    benchmarks_ref = _compute_benchmarks_ref(club_speed_ref)
    assert derived_values["tour_carry_yards"] == pytest.approx(benchmarks_ref["tour_carry_yards"], abs=0.1)
    assert derived_values["tour_total_yards"] == pytest.approx(benchmarks_ref["tour_total_yards"], abs=0.1)
    assert derived_values["amateur_carry_yards"] == pytest.approx(benchmarks_ref["amateur_carry_yards"], abs=0.1)
    assert derived_values["lpga_carry_yards"] == pytest.approx(benchmarks_ref["lpga_carry_yards"], abs=0.1)
    assert derived_values["amateur_total_yards"] == pytest.approx(benchmarks_ref["amateur_total_yards"], abs=0.1)
    assert derived_values["lpga_total_yards"] == pytest.approx(benchmarks_ref["lpga_total_yards"], abs=0.1)

    carry_yards = derived_values["carry_distance_yards"]
    assert derived_values["carry_delta_to_tour_yards"] == pytest.approx(
        carry_yards - benchmarks_ref["tour_carry_yards"], abs=0.1
    )
    assert derived_values["carry_delta_to_amateur_yards"] == pytest.approx(
        carry_yards - benchmarks_ref["amateur_carry_yards"], abs=0.1
    )
    assert derived_values["carry_delta_to_lpga_yards"] == pytest.approx(
        carry_yards - benchmarks_ref["lpga_carry_yards"], abs=0.1
    )
