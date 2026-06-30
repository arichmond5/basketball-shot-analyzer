IDEAL = {
    "elbow":       (45,  90),
    "knee":        (100, 135),
    "wrist":       (0, 45),
    "trunk_lean":  (0,   20),
}

MESSAGES = {
    "elbow":      ("Good elbow angle",        "Open your elbow more — aim for 90°",       "Elbow too open — bend to ~90°"),
    "knee":       ("Good knee bend",          "Bend your knees more",                      "Too deep — straighten slightly"),
    "wrist":      ("Good wrist snap",         "Snap your wrist more on release",           ""),
    "trunk_lean": ("Good posture",            "Stay upright — you leaned forward",         ""),
}

def generate_feedback(metrics: dict) -> dict:
    feedback = {}

    for phase, joints in metrics.items():
        feedback[phase] = {}
        print(phase)

        for joint, peak in joints.items():
            if joint not in IDEAL:
                continue

            lo, hi                   = IDEAL[joint]
            good, low_msg, high_msg  = MESSAGES[joint]

            if lo <= peak <= hi:
                feedback[phase][joint] = {"angle": peak, "status": "good",     "message": good}
            elif peak > lo:
                feedback[phase][joint] = {"angle": peak, "status": "too_low",  "message": low_msg}
            else:
                feedback[phase][joint] = {"angle": peak, "status": "too_high", "message": high_msg}

    return feedback