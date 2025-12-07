"""Derived golf metrics computed locally for Golf Dashboard.

This module ports the spirit of OpenGolfCoach calculations into pure Python so the
Home Assistant integration can run without external dependencies. The functions
are intentionally lightweight (no third-party imports) and deterministic.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

GRAVITY = 9.81  # m/s^2
MPS_TO_MPH = 2.236936
METERS_TO_YARDS = 1.09361


def _calculate_spin_components(
    total_spin_rpm: float, spin_axis_degrees: float
) -> Tuple[float, float]:
    """Split total spin into backspin and sidespin using spin axis."""
    total_spin = max(total_spin_rpm, 0.0)
    spin_axis_rad = math.radians(spin_axis_degrees)
    backspin = total_spin * math.cos(spin_axis_rad)
    sidespin = total_spin * math.sin(spin_axis_rad)
    return backspin, sidespin


def _estimate_carry_total_offline(
    ball_speed_mps: float,
    vla_deg: float,
    hla_deg: Optional[float],
    total_spin_rpm: Optional[float],
    backspin_rpm: Optional[float],
    sidespin_rpm: Optional[float],
) -> Dict[str, float]:
    """Approximate carry/total/offline distances based on launch conditions.

    This is a light-weight ballistic approximation inspired by the Rust physics in
    open-golf-coach. Drag and roll effects are simplified but produce stable,
    reasonable numbers for dashboard use.
    """
    results: Dict[str, float] = {}

    # Clamp launch angles to keep the math within realistic shot shapes.
    vla_clamped = max(-5.0, min(vla_deg, 35.0))
    hla_clamped = None if hla_deg is None else max(-25.0, min(hla_deg, 25.0))

    theta = math.radians(vla_clamped)
    if theta <= 0 or ball_speed_mps <= 0:
        return results

    # Baseline carry using projectile range with a mild drag reduction.
    base_range = (ball_speed_mps**2 / GRAVITY) * math.sin(2 * theta)
    # Cap to a plausible max carry to avoid absurd outputs for extreme inputs (meters).
    base_range = min(base_range, 350.0)
    drag_factor = 0.92  # More conservative lift/drag tuning for realistic carry.

    spin_total = total_spin_rpm
    if spin_total is None and backspin_rpm is not None and sidespin_rpm is not None:
        spin_total = math.hypot(backspin_rpm, sidespin_rpm)

    spin_penalty = 0.0
    if spin_total is not None:
        # High spin tends to add lift but also adds drag; apply a soft penalty.
        spin_penalty = min(spin_total / 40000.0, 0.2)

    launch_tuning = max(min((vla_clamped - 12.0) / 100.0, 0.1), -0.1)

    carry = base_range * drag_factor * max(0.75, 1 - spin_penalty + launch_tuning)
    if carry < 0:
        carry = 0.0
    # Raw carry in meters for internal use
    # Roll depends on launch and spin; low launch/low spin tends to roll more.
    roll_factor = 0.07 + max(0.0, 12.0 - vla_clamped) * 0.005
    if spin_total is not None:
        roll_factor -= min(spin_total / 25000.0, 0.05)
    roll_factor = max(0.0, min(0.25, roll_factor))
    total_distance = carry * (1 + roll_factor)
    # Convert carry/total to yards for output
    carry_yards = carry * METERS_TO_YARDS
    total_yards = total_distance * METERS_TO_YARDS
    results["carry_distance_yards"] = carry_yards
    results["total_distance_yards"] = total_yards

    # Offline distance combines initial face angle (HLA) with curvature from sidespin.
    offline = 0.0
    offline_computable = False
    if hla_clamped is not None:
        offline += carry_yards * math.tan(math.radians(hla_clamped))
        offline_computable = True

    if backspin_rpm is not None and sidespin_rpm is not None and carry > 0:
        curvature = math.atan2(sidespin_rpm, max(abs(backspin_rpm), 1.0))
        offline += carry_yards * math.sin(curvature) * 0.3
        offline_computable = True

    if offline_computable:
        # Keep offline within a reasonable multiple of carry to avoid explosions.
        offline_limit = carry_yards * 3.0
        offline = max(-offline_limit, min(offline, offline_limit))
        results["offline_distance_yards"] = offline

    return results


def _estimate_club_speed(
    ball_speed_mps: float, total_spin_rpm: Optional[float]
) -> tuple[float, float]:
    """Estimate club speed (in mph) and smash factor from ball speed."""
    if ball_speed_mps <= 0:
        return 0.0, 0.0

    ball_speed_mph = ball_speed_mps * MPS_TO_MPH

    # Very low speeds (putts/duffs) should not yield meaningful club speed.
    if ball_speed_mph < 10.0:
        return 0.0, 0.0

    if ball_speed_mph > 145.40084:
        smash_estimate = 1.48
    elif ball_speed_mph > 122.03148:
        smash_estimate = 1.45
    elif ball_speed_mph > 100.66212:
        smash_estimate = 1.40
    else:
        smash_estimate = 1.30

    if total_spin_rpm is not None:
        smash_estimate -= min(total_spin_rpm / 60000.0, 0.05)

    smash_estimate = max(smash_estimate, 1.1)
    club_speed = ball_speed_mph / smash_estimate

    # Clamp to a realistic upper bound to avoid runaway estimates.
    club_speed = min(club_speed, 145.40084)
    return club_speed, smash_estimate


def _classify_shot(
    ball_speed_mps: float,
    vla_deg: float,
    hla_deg: float,
    spin_axis_deg: float,
) -> Dict[str, str]:
    """Deterministic shot classification mirroring shot_classifier.rs rules."""
    ball_speed_mph = ball_speed_mps * MPS_TO_MPH

    # Special cases
    if abs(vla_deg) < 0.1 and ball_speed_mph < 6.0:
        rank = "P"
        return {"shot_name": "Putt", "shot_rank": rank}

    # Ultra-low speed, low-launch mishits.
    if ball_speed_mph < 25.0 and vla_deg < 10.0:
        rank = "E"
        return {"shot_name": "Chunk", "shot_rank": rank}

    if vla_deg < 5.0 and ball_speed_mph > 44.73872:
        rank = "E"
        return {"shot_name": "Worm Burner", "shot_rank": rank}

    if hla_deg > 12.0 and vla_deg > 12.0:
        rank = "E"
        return {"shot_name": "Right Shank", "shot_rank": rank}

    if hla_deg < -12.0 and vla_deg > 12.0:
        rank = "E"
        return {"shot_name": "Left Shank", "shot_rank": rank}

    if ball_speed_mph > 100.0 and vla_deg < 20.0 and spin_axis_deg < -25.0:
        rank = "E"
        return {"shot_name": "Duck Hook", "shot_rank": rank}

    if ball_speed_mph > 100.0 and vla_deg < 20.0 and spin_axis_deg > 25.0:
        rank = "E"
        return {"shot_name": "Banana Slice", "shot_rank": rank}

    hla_abs = abs(hla_deg)
    spin_abs = abs(spin_axis_deg)
    if hla_abs < 2.0 and spin_abs < 2.0 and ball_speed_mph > 55.9234:
        if hla_deg > 0.0 and spin_axis_deg < 0.0:
            rank = "S+"
            return {"shot_name": "Baby Push Draw", "shot_rank": rank}
        if hla_deg < 0.0 and spin_axis_deg > 0.0:
            rank = "S"
            return {"shot_name": "Baby Pull Fade", "shot_rank": rank}

    # Direction from horizontal launch angle
    if hla_deg < -3.0:
        direction = "Pull"
    elif hla_deg > 3.0:
        direction = "Push"
    else:
        direction = "Straight"

    # Shape from spin axis
    if spin_axis_deg < -12.0:
        shape = "Hook"
    elif spin_axis_deg < -3.0:
        shape = "Draw"
    elif spin_axis_deg > 12.0:
        shape = "Slice"
    elif spin_axis_deg > 3.0:
        shape = "Fade"
    else:
        shape = None

    if shape:
        shot_name = f"{direction} {shape}"
    else:
        shot_name = direction

    # Rank matrix mirroring shot_classifier.rs
    if (direction, shape) in {
        ("Straight", "Draw"),
        ("Straight", "Fade"),
        ("Push", "Draw"),
    }:
        rank = "A"
    elif (direction, shape) in {
        ("Straight", None),
        ("Pull", None),
        ("Push", None),
        ("Pull", "Fade"),
    }:
        rank = "B"
    elif (direction, shape) in {
        ("Pull", "Draw"),
        ("Push", "Fade"),
        ("Push", "Hook"),
        ("Pull", "Slice"),
    }:
        rank = "C"
    else:
        # Hooks/slices and extremes
        rank = "D"

    return {"shot_name": shot_name, "shot_rank": rank}


def _infer_club_class(ball_speed_mph: Optional[float]) -> str:
    """
    Rough classification by ball speed.
    Returns one of: "wedge", "mid_iron", "long_iron_hybrid", "driver".
    """
    if ball_speed_mph is None or ball_speed_mph < 60.0:
        return "wedge"
    if ball_speed_mph < 80.0:
        return "mid_iron"
    if ball_speed_mph < 105.0:
        return "long_iron_hybrid"
    return "driver"


DRIVER_STATIC_LOFT = 10.0
LONG_IRON_STATIC_LOFT = 18.0
MID_IRON_STATIC_LOFT = 30.0
WEDGE_STATIC_LOFT = 44.0


def compute_spin_loft_and_aoa(
    ball_speed_mph: Optional[float],
    total_spin_rpm: Optional[float],
    vla_deg: Optional[float],
) -> Dict[str, float]:
    """Estimate spin loft and attack angle from speed, spin, and launch angle."""
    if ball_speed_mph is None or total_spin_rpm is None or vla_deg is None:
        return {}

    club_class = _infer_club_class(ball_speed_mph)
    if club_class == "driver":
        k = 0.0030
        min_sl, max_sl = 6.0, 18.0
        static_loft = DRIVER_STATIC_LOFT
    elif club_class == "long_iron_hybrid":
        k = 0.0035
        min_sl, max_sl = 10.0, 24.0
        static_loft = LONG_IRON_STATIC_LOFT
    elif club_class == "mid_iron":
        k = 0.0040
        min_sl, max_sl = 12.0, 30.0
        static_loft = MID_IRON_STATIC_LOFT
    else:
        k = 0.0045
        min_sl, max_sl = 18.0, 40.0
        static_loft = WEDGE_STATIC_LOFT

    spin_loft_deg = k * total_spin_rpm / max(ball_speed_mph, 1.0)
    spin_loft_deg = max(min_sl, min(spin_loft_deg, max_sl))

    dynamic_loft_deg = static_loft + 2.0  # simple approximation
    aoa_deg = dynamic_loft_deg - spin_loft_deg

    return {
        "spin_loft_deg": spin_loft_deg,
        "attack_angle_deg": aoa_deg,
    }


def compute_face_and_path(
    hla_deg: Optional[float],
    spin_axis_deg: Optional[float],
) -> Dict[str, float]:
    """Estimate face angle, face-to-path, and club path from HLA and spin axis."""
    if hla_deg is None or spin_axis_deg is None:
        return {}

    face_fraction = 0.80
    spin_axis_to_ftp = 0.60

    face_angle_deg = hla_deg * face_fraction
    face_to_path_deg = spin_axis_deg * spin_axis_to_ftp
    club_path_deg = face_angle_deg - face_to_path_deg

    def clamp(val: float) -> float:
        return max(-20.0, min(val, 20.0))

    return {
        "face_angle_deg": clamp(face_angle_deg),
        "face_to_path_deg": clamp(face_to_path_deg),
        "club_path_deg": clamp(club_path_deg),
    }


def compute_apex_hang_and_descent(
    ball_speed_mps: Optional[float],
    vla_deg: Optional[float],
) -> Dict[str, float]:
    """Estimate apex height (ft), hang time (s), and descent angle (deg) via simple projectile."""
    if ball_speed_mps is None or vla_deg is None:
        return {}

    theta = math.radians(vla_deg)
    v = ball_speed_mps
    v_y = v * math.sin(theta)
    v_x = v * math.cos(theta)

    gravity = 9.80665
    time_up = v_y / gravity
    hang_time = 2.0 * time_up

    apex_m = (v_y * v_y) / (2.0 * gravity)
    apex_yards = (apex_m * 3.28084) / 3.0

    descent_angle = math.degrees(math.atan2(v_y, v_x))

    return {
        "apex_height_yards": apex_yards,
        "hang_time_seconds": hang_time,
        "descent_angle_deg": descent_angle,
    }


def compute_tour_benchmark_from_shot(
    ball_speed_mph: Optional[float],
    vla_deg: Optional[float],
    total_spin_rpm: Optional[float],
) -> Dict[str, float]:
    """Compute simple tour-style benchmark distances (yards) for comparison."""
    if ball_speed_mph is None or ball_speed_mph < 10.0:
        return {}

    # Baseline carry using a linear rule with clamps.
    if ball_speed_mph < 90.0:
        tour_carry = max(ball_speed_mph * 1.1 - 30.0, 40.0)
    else:
        tour_carry = ball_speed_mph * 1.60 - 25.0

    # Clamp to plausible tour bounds.
    tour_carry = min(max(tour_carry, 30.0), 320.0)
    tour_total = min(tour_carry * 1.05, 340.0)

    # Apply small bonuses/penalties for near-optimal launch/spin.
    if vla_deg is not None and total_spin_rpm is not None:
        if 11.0 <= vla_deg <= 15.0 and 2200.0 <= total_spin_rpm <= 3000.0:
            tour_carry *= 1.02
        elif vla_deg < 8.0 or vla_deg > 18.0 or total_spin_rpm < 1500.0 or total_spin_rpm > 4000.0:
            tour_carry *= 0.97
        tour_carry = min(max(tour_carry, 30.0), 320.0)
        tour_total = min(tour_carry * 1.05, 340.0)

    return {
        "tour_carry_yards": tour_carry,
        "tour_total_yards": tour_total,
    }


def compute_optimal_window(
    ball_speed_mph: Optional[float],
    vla_deg: Optional[float],
    hla_deg: Optional[float],
    total_spin_rpm: Optional[float],
) -> Dict[str, object]:
    """Assess whether launch, spin, and start line are within simple optimal windows."""
    launch_ok: Optional[bool] = None
    spin_ok: Optional[bool] = None
    start_ok: Optional[bool] = None

    if vla_deg is not None:
        launch_ok = 11.0 <= vla_deg <= 15.0
    if total_spin_rpm is not None:
        spin_ok = 2200.0 <= total_spin_rpm <= 3200.0
    if hla_deg is not None:
        start_ok = -2.0 <= hla_deg <= 2.0

    def _label_fragment(ok: Optional[bool], good: str, bad: str) -> str:
        if ok is None:
            return ""
        return good if ok else bad

    if launch_ok is True and spin_ok is True and start_ok is True:
        label = "Launch, spin, and start line in optimal window."
    else:
        launch_frag = _label_fragment(launch_ok, "launch good", "launch off")
        spin_frag = _label_fragment(spin_ok, "spin good", "spin off")
        start_frag = _label_fragment(start_ok, "start centered", "start off")
        fragments = [frag for frag in (launch_frag, spin_frag, start_frag) if frag]
        if fragments:
            label = ", ".join(fragments).capitalize() + "."
        else:
            label = "All windows off: adjust launch, spin, and start line."

    return {
        "launch_in_window": launch_ok,
        "spin_in_window": spin_ok,
        "start_in_window": start_ok,
        "optimal_window_label": label,
    }


def compute_shot_quality_score(
    carry_yards: Optional[float],
    offline_yards: Optional[float],
    tour_carry_yards: Optional[float],
    launch_in_window: Optional[bool],
    spin_in_window: Optional[bool],
    start_in_window: Optional[bool],
) -> Optional[float]:
    """Compute a 0–100 shot quality score based on dispersion, distance, and windows."""
    if carry_yards is None or offline_yards is None or tour_carry_yards is None:
        return None

    score = 100.0

    diff = abs(carry_yards - tour_carry_yards)
    penalty_dist = min(diff / 2.0, 30.0)
    score -= penalty_dist

    penalty_off = min(abs(offline_yards) / 5.0, 25.0)
    score -= penalty_off

    for flag in (launch_in_window, spin_in_window, start_in_window):
        if flag is False:
            score -= 10.0

    return max(0.0, min(score, 100.0))


def compute_club_recommendation(
    ball_speed_mph: Optional[float],
    carry_yards: Optional[float],
    tour_carry_yards: Optional[float],
) -> Optional[str]:
    """Provide a short club guidance message based on speed and efficiency."""
    if ball_speed_mph is None or carry_yards is None:
        return None

    if ball_speed_mph < 70.0:
        club_class = "Wedge / short iron"
    elif ball_speed_mph < 90.0:
        club_class = "Mid iron (7–9i)"
    elif ball_speed_mph < 105.0:
        club_class = "Long iron / hybrid"
    else:
        club_class = "Driver / 3-wood"

    guidance = "Solid strike."
    if tour_carry_yards is not None:
        diff = tour_carry_yards - carry_yards
        if diff > 20:
            guidance = "You’re well short of Tour for this speed; focus on solid contact and launch."
        elif 5 < diff <= 20:
            guidance = "Within striking distance of Tour. Small gains in launch and spin will help."
        elif -10 <= diff <= 5:
            guidance = "You’re in the Tour ballpark for this speed. Great strike."
        else:
            guidance = "You’re surpassing a typical Tour carry for this speed. Strong efficiency."

    return f"{club_class}: {guidance}"


def compute_amateur_lpga_benchmarks(
    tour_carry_yards: Optional[float],
    tour_total_yards: Optional[float],
) -> Dict[str, float]:
    """Scale Tour benchmarks to simple amateur and LPGA curves."""
    if tour_carry_yards is None or tour_total_yards is None:
        return {}

    amateur_carry = tour_carry_yards * 0.80
    lpga_carry = tour_carry_yards * 0.90
    amateur_total = tour_total_yards * 0.80
    lpga_total = tour_total_yards * 0.90

    return {
        "amateur_carry_yards": amateur_carry,
        "amateur_total_yards": amateur_total,
        "lpga_carry_yards": lpga_carry,
        "lpga_total_yards": lpga_total,
    }


def compute_derived_from_shot(
    ball_speed_mps: Optional[float],
    vla_deg: Optional[float],
    hla_deg: Optional[float],
    total_spin_rpm: Optional[float],
    spin_axis_deg: Optional[float],
) -> Dict[str, Any]:
    """Compute derived metrics and classification from NOVA shot data.

    Inputs can be None; the function will compute what it can without raising.
    """
    derived: Dict[str, Any] = {}

    backspin_rpm: Optional[float] = None
    sidespin_rpm: Optional[float] = None

    if total_spin_rpm is not None and spin_axis_deg is not None:
        backspin_rpm, sidespin_rpm = _calculate_spin_components(total_spin_rpm, spin_axis_deg)
        derived["backspin_rpm"] = backspin_rpm
        derived["sidespin_rpm"] = sidespin_rpm

    # Distances and offline
    if ball_speed_mps is not None and vla_deg is not None:
        distances = _estimate_carry_total_offline(
            ball_speed_mps,
            vla_deg,
            hla_deg,
            total_spin_rpm,
            backspin_rpm,
            sidespin_rpm,
        )
        derived.update(distances)

    # Club speed and smash factor
    if ball_speed_mps is not None and ball_speed_mps > 0:
        club_speed, smash_estimate = _estimate_club_speed(ball_speed_mps, total_spin_rpm)
        if club_speed > 0:
            derived["club_speed_meters_per_second"] = club_speed
            derived["smash_factor"] = smash_estimate

    # Tour benchmark metrics and comparison
    ball_speed_mph = ball_speed_mps * MPS_TO_MPH if ball_speed_mps is not None else None
    tour_metrics = compute_tour_benchmark_from_shot(ball_speed_mph, vla_deg, total_spin_rpm)
    derived.update(tour_metrics)
    if tour_metrics and "carry_distance_yards" in derived:
        carry_yards = derived["carry_distance_yards"]
        tour_carry = tour_metrics.get("tour_carry_yards")
        if carry_yards is not None and tour_carry is not None:
            derived["carry_delta_to_tour_yards"] = carry_yards - tour_carry

    # Amateur and LPGA benchmarks/deltas
    if tour_metrics:
        derived.update(compute_amateur_lpga_benchmarks(tour_metrics.get("tour_carry_yards"), tour_metrics.get("tour_total_yards")))
        carry_yards = derived.get("carry_distance_yards")
        amateur_carry = derived.get("amateur_carry_yards")
        lpga_carry = derived.get("lpga_carry_yards")
        if carry_yards is not None and amateur_carry is not None:
            derived["carry_delta_to_amateur_yards"] = carry_yards - amateur_carry
        if carry_yards is not None and lpga_carry is not None:
            derived["carry_delta_to_lpga_yards"] = carry_yards - lpga_carry

    # Optimal window assessment
    optimal = compute_optimal_window(ball_speed_mph, vla_deg, hla_deg, total_spin_rpm)
    derived.update(optimal)

    # Shot quality score
    carry_yards = derived.get("carry_distance_yards")
    offline_yards = derived.get("offline_distance_yards")
    tour_carry = derived.get("tour_carry_yards")
    score = compute_shot_quality_score(
        carry_yards,
        offline_yards,
        tour_carry,
        optimal.get("launch_in_window"),
        optimal.get("spin_in_window"),
        optimal.get("start_in_window"),
    )
    if score is not None:
        derived["shot_quality_score"] = score

    # Club recommendation
    recommendation = compute_club_recommendation(ball_speed_mph, carry_yards, tour_carry)
    if recommendation:
        derived["club_recommendation"] = recommendation

    # Spin loft / attack angle
    derived.update(compute_spin_loft_and_aoa(ball_speed_mph, total_spin_rpm, vla_deg))

    # Face / path estimates
    derived.update(compute_face_and_path(hla_deg, spin_axis_deg))

    # Apex / hang / descent estimates
    derived.update(compute_apex_hang_and_descent(ball_speed_mps, vla_deg))

    # Shot classification
    if (
        ball_speed_mps is not None
        and vla_deg is not None
        and hla_deg is not None
        and spin_axis_deg is not None
    ):
        derived.update(_classify_shot(ball_speed_mps, vla_deg, hla_deg, spin_axis_deg))

    return derived
