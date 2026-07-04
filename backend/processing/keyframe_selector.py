def get_keyframe_data(
    frame_data: list[dict],
    phases: dict[str, tuple[int, int]],
    shooting_side: str
) -> dict[str, dict]:

    keyframe_data = {}

    for phase, (start, end) in phases.items():

        phase_frames = [
            frame for frame in frame_data
            if start <= frame["frame_index"] <= end
            and "angles" in frame
        ]

        if not phase_frames:
            continue

        # --------------------
        # LOADING: max hip y
        # --------------------
        if phase == "LOADING":
            best_frame = max(
                phase_frames,
                key=lambda f: f["landmarks"][f"{shooting_side}_hip"]["y"]
            )

        # --------------------
        # SET_POINT: min elbow angle
        # --------------------
        elif phase == "SET_POINT":
            best_frame = min(
                phase_frames,
                key=lambda f: f["angles"].get("elbow", 180)
            )

        # --------------------
        # RELEASE: SAME LOGIC AS SNAPSHOT (peak wrist THEN +4 frames)
        # --------------------
        elif phase == "RELEASE":
            peak_frame = min(
                phase_frames,
                key=lambda f: f["landmarks"][f"{shooting_side}_wrist"]["y"]
            )

            peak_idx = phase_frames.index(peak_frame)
            target_idx = peak_idx + 4

            if target_idx < len(phase_frames):
                best_frame = phase_frames[target_idx]
            else:
                best_frame = peak_frame

        else:
            continue

        keyframe_data[phase] = best_frame

    return keyframe_data