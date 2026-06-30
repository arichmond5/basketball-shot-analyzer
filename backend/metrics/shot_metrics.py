PHASE_ANGLE_MAP = {
    "LOADING":        {"knee": "min", "trunk_lean": "max"},
    "SET_POINT":   {"elbow": "min", "trunk_lean": "max"},
    "FOLLOW_THROUGH": {"wrist": "min", "trunk_lean": "max"},
}

def compute_shot_metrics(frame_data: list[dict], phases: dict[str, tuple[int, int]]) -> dict[str, dict]:
    metrics = {}
    print(phases)

    for phase, angle_map in PHASE_ANGLE_MAP.items():
        if phase not in phases:
            continue

        start, end = phases[phase]

        phase_frames = [
            frame for frame in frame_data
            if start <= frame["frame_index"] <= end
        ]

        phase_metrics = {}
        for angle_key, pick in angle_map.items():
            vals = [
                frame["angles"][angle_key]
                for frame in phase_frames
                if "angles" in frame and angle_key in frame["angles"]
            ]

            if not vals:
                continue

            phase_metrics[angle_key] = min(vals) if pick == "min" else max(vals)

        metrics[phase] = phase_metrics

    return metrics