# Built-in derived metrics (OpenGolfCoach style)

The NOVA integration now computes OpenGolfCoach-inspired derived metrics directly in Python—no external packages or extra installs required.

## What gets calculated per shot

- Carry Distance (m)
- Total Distance (m)
- Offline Distance (m)
- Backspin / Sidespin (rpm) from total spin + spin axis
- Club Speed (m/s) and Smash Factor
- Shot Type (classification string)
- Shot Rank (letter grade) with rank color (`0xRRGGBB`)

## How it works

- Raw NOVA fields (`ball_speed_meters_per_second`, `vertical_launch_angle_degrees`, `horizontal_launch_angle_degrees`, `total_spin_rpm`, `spin_axis_degrees`) are fed into lightweight physics and classification helpers in `derived.py`.
- Results are merged into the shot payload so the existing sensors pick them up automatically.
- If a value is missing (e.g., no spin axis), only the computable metrics are emitted; no exceptions are raised.

## Using the sensors

All derived entities are defined alongside the raw ones (see `const.py` / `sensor.py`), so they appear automatically after the first shot:

- `sensor.nova_carry_distance`
- `sensor.nova_total_distance`
- `sensor.nova_offline_distance`
- `sensor.nova_backspin`
- `sensor.nova_sidespin`
- `sensor.nova_club_speed`
- `sensor.nova_smash_factor`
- `sensor.nova_shot_type`
- `sensor.nova_shot_rank`
- `sensor.nova_shot_color`

The Lovelace view in `dashboards/nova_open_golfcoach.yaml` places these sensors in a tablet-friendly dark layout.
