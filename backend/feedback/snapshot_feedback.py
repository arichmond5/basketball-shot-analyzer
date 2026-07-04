IDEAL = {
    "LOADING": {
        "knee": (105, 135),
        "trunk_lean": (0, 10)
    },

    "SET_POINT": {
        "elbow": (45, 90),
        "knee": (140, 165),
        "trunk_lean": (0, 5)
    },

    "RELEASE": {
        "elbow": (150, 180),
        "knee": (165, 180),
        "trunk_lean": (0, 5)
    }
}

MESSAGES = {
    "LOADING": {
        "knee": (
            "Good knee bend",
            "Slightly shallow — could be tracking variation or a smaller dip",
            "Slightly deep — could be tracking variation or a deeper load",
            "Don't dip quite as deep",
            "Load into your legs more"
        ),
        "trunk_lean": (
            "Good posture",
            "Slight forward lean — may be normal tracking noise",
            "Slightly upright deviation — may be tracking variation",
            "",
            "Stay more upright during the dip"
        )
    },

    "SET_POINT": {
        "elbow": (
            "Good elbow angle",
            "Slightly open — within normal tracking variance",
            "Slightly tight — within normal tracking variance",
            "Keep your shooting arm more open",
            "Bring your shooting arm in slightly"
        ),
        "knee": (
            "Good leg drive",
            "Slightly under extended — likely normal timing variation",
            "Slightly over extended — likely normal timing variation",
            "Start extending through your legs sooner",
            "Avoid extending your legs too early"
        ),
        "trunk_lean": (
            "Good posture",
            "Slight forward lean — within expected tracking noise",
            "Slight upright variance — within expected tracking noise",
            "",
            "Keep your torso more upright"
        )
    },

    "RELEASE": {
        "elbow": (
            "Good elbow extension",
            "Slightly under extended — may be frame timing variance",
            "Slight over extension — may be frame timing variance",
            "Extend your shooting arm more",
            ""
        ),
        "knee": (
            "Good leg extension",
            "Slightly under extended — likely timing noise",
            "Slight over extension — likely timing noise",
            "Finish driving through your legs",
            ""
        ),
        "trunk_lean": (
            "Good posture",
            "Slight lean detected — may be tracking variance",
            "Slight upright variance — may be tracking variance",
            "",
            "Keep your body more upright through release"
        )
    }
}

TOLERANCE = 10


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

            tol_lo = lo - TOLERANCE
            tol_hi = hi + TOLERANCE

            if lo <= peak <= hi:
                status = "good"
                message = msgs[0]

            elif tol_lo <= peak < lo:
                status = "uncertain"
                message = msgs[1]

            elif hi < peak <= tol_hi:
                status = "uncertain"
                message = msgs[2]

            elif peak < tol_lo:
                status = "too_low"
                message = msgs[3]

            else:
                status = "too_high"
                message = msgs[4]

            feedback[phase][joint] = {
                "angle": peak,
                "status": status,
                "message": message,
                "ideal": [lo, hi],
                "tolerance_band": [tol_lo, tol_hi]
            }

    return feedback