"""
Finds each phase of a basketball shot (loading, set point, and release) in sequential order.
"""

def shot_segmenter(frame_data: list[dict]) -> dict[str, tuple[int, int]]:
    IDLE           = "IDLE"
    LOADING        = "LOADING"
    SET_POINT      = "SET_POINT"
    RELEASE        = "RELEASE"

    state        = IDLE
    min_knee     = 180.0
    prev_wrist_y = None
    frames_in    = 0

    #Thresholds used to signify start of phase
    LOAD_THRESHOLD          = 140
    MIN_DIP_THRESHOLD       = 158
    RELEASE_THRESHOLD       = 100

    phase_frames = {
        LOADING:        [],
        SET_POINT:      [],
        RELEASE:        [],
    }

    for frame in frame_data:
        landmarks = frame["landmarks"]
        angles    = frame.get("angles", {})

        knee  = angles.get("knee")
        elbow = angles.get("elbow")

        wrist    = landmarks.get("right_wrist") or landmarks.get("left_wrist")
        shoulder = landmarks.get("right_shoulder") or landmarks.get("left_shoulder")

        if wrist is None or shoulder is None:
            continue

        wrist_y    = wrist["y"]
        shoulder_y = shoulder["y"]

        wrist_above    = wrist_y < shoulder_y
        wrist_moving_up = prev_wrist_y is not None and wrist_y < prev_wrist_y
        prev_wrist_y   = wrist_y

        frame_idx = frame["frame_index"]
        frames_in += 1

        if state == IDLE:
            if knee is not None and knee < LOAD_THRESHOLD:
                state     = LOADING
                min_knee  = knee
                frames_in = 0

        elif state == LOADING:
            phase_frames[LOADING].append(frame_idx)
            if knee is not None:
                min_knee = min(min_knee, knee)
            if wrist_above and wrist_moving_up and min_knee < MIN_DIP_THRESHOLD:
                state     = SET_POINT
                frames_in = 0

        elif state == SET_POINT:
            phase_frames[SET_POINT].append(frame_idx)
            if elbow is not None and elbow > RELEASE_THRESHOLD:
                state     = RELEASE
                frames_in = 0

        elif state == RELEASE:
            phase_frames[RELEASE].append(frame_idx)

    phases = {}
    for phase, frames in phase_frames.items():
        if frames:
            phases[phase] = (frames[0], frames[-1])

    return phases