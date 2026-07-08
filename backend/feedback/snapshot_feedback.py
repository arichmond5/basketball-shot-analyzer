"""
Analyzes keyframe data and compares with "IDEAL" data.

Outputs feedback based on accuracy.
"""

"""
Analyzes keyframe data and compares with "IDEAL" data.

Outputs feedback based on accuracy.
"""

IDEAL = {
    "LOADING": {
        "knee": (105, 135),
        "trunk_lean": (-5, 10)
    },

    "SET_POINT": {
        "elbow": (45, 90),
        "knee": (140, 165),
        "trunk_lean": (-5, 5)
    },

    "RELEASE": {
        "elbow": (150, 180),
        "knee": (165, 180),
        "trunk_lean": (-5, 5)
    }
}

MESSAGES = {
    "LOADING": {
        "knee": (
            "Good knee bend",
            "Load into your legs more",
            "Don't dip quite as deep"
        ),
        "trunk_lean": (
            "Good posture",
            "Stay more upright during the dip",
            ""
        )
    },

    "SET_POINT": {
        "elbow": (
            "Good elbow angle",
            "Keep your shooting arm more open",
            "Bring your shooting arm in slightly"
        ),
        "knee": (
            "Good leg drive",
            "Start extending through your legs sooner",
            "Avoid extending your legs too early"
        ),
        "trunk_lean": (
            "Good posture",
            "Keep your torso more upright",
            ""
        )
    },

    "RELEASE": {
        "elbow": (
            "Good elbow extension",
            "Extend your shooting arm more",
            ""
        ),
        "knee": (
            "Good leg extension",
            "Finish driving through your legs",
            ""
        ),
        "trunk_lean": (
            "Good posture",
            "Keep your body more upright through release",
            ""
        )
    }
}


def generate_snapshot_feedback(keyframe_data: dict[str, dict]) -> dict:
    feedback = {}

    for phase, frame_data in keyframe_data.items():
        feedback[phase] = {}
        angles = frame_data["angles"]

        for joint in IDEAL[phase]:
            if joint not in angles:
                continue

            lo, hi = IDEAL[phase][joint]
            msgs = MESSAGES[phase][joint]
            peak = angles[joint]

            if lo <= peak <= hi:
                status = "good"
                message = msgs[0]

            elif peak < lo:
                status = "too_low"
                message = msgs[1]

            else:
                status = "too_high"
                message = msgs[2]

            feedback[phase][joint] = {
                "angle": peak,
                "status": status,
                "message": message,
                "ideal": [lo, hi]
            }

    return feedback
