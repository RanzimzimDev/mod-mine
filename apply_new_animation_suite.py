import os
import json
import math
import uuid
import re

print("=====================================================================")
print("ANIMATION SUITE UPGRADE: FLY_FLAP, GLIDE, EATING, SLEEP, WAKE_UP, ROAR")
print("=====================================================================")

# ---------------------------------------------------------------------------
# ADULT ANIMATION GENERATORS
# ---------------------------------------------------------------------------

def generate_adult_fly_flap(duration=1.4, frames=43):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}, "position": {}},
        "neck_upper": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_shoulder_left": {"rotation": {}},
        "wing_arm_left": {"rotation": {}},
        "wing_forearm_left": {"rotation": {}},
        "wing_fingers_left": {"rotation": {}},
        "wing_shoulder_right": {"rotation": {}},
        "wing_arm_right": {"rotation": {}},
        "wing_forearm_right": {"rotation": {}},
        "wing_fingers_right": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_left_shin": {"rotation": {}},
        "leg_front_left_foot": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_front_right_shin": {"rotation": {}},
        "leg_front_right_foot": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_left_shin": {"rotation": {}},
        "leg_left_foot": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "leg_right_shin": {"rotation": {}},
        "leg_right_foot": {"rotation": {}},
        "tail_1": {"rotation": {}},
        "tail_2": {"rotation": {}},
        "tail_3": {"rotation": {}},
        "tail_4": {"rotation": {}},
        "tail_5": {"rotation": {}},
        "tail_6": {"rotation": {}},
        "tail_flame": {"rotation": {}, "scale": {}},
        "tail_flame_left": {"rotation": {}},
        "tail_flame_right": {"rotation": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        psi = phi - 0.32 * math.sin(phi) # Asymmetric flight mechanics: smooth upstroke, punchy power downstroke

        s = math.sin(psi)
        c = math.cos(psi)

        # 4 wing joints (graceful upstroke arch, powerful 284-unit full span downstroke)
        sh_z = 24.0 * s
        sh_x = -4.0 * c
        sh_y = 6.0 * s

        arm_z = 32.0 * s
        arm_y = 14.0 * max(0.0, s) # folds back in upstroke
        arm_x = -6.0 * c

        s_fore = math.sin(psi - 0.45)
        fore_z = -16.0 * max(0.0, s) + 24.0 * min(0.0, s_fore) # graceful arch upstroke, full stretch downstroke
        fore_y = 10.0 * max(0.0, s_fore)

        s_fing = math.sin(psi - 0.75)
        fing_z = -22.0 * max(0.0, s) + 28.0 * min(0.0, s_fing)

        # Left wing
        bones_data["wing_shoulder_left"]["rotation"][str(t)] = [round(sh_x, 2), round(sh_y, 2), round(sh_z, 2)]
        bones_data["wing_arm_left"]["rotation"][str(t)] = [round(arm_x, 2), round(arm_y, 2), round(arm_z, 2)]
        bones_data["wing_forearm_left"]["rotation"][str(t)] = [0.0, round(fore_y, 2), round(fore_z, 2)]
        bones_data["wing_fingers_left"]["rotation"][str(t)] = [0.0, 0.0, round(fing_z, 2)]

        # Right wing (bilateral mirror)
        bones_data["wing_shoulder_right"]["rotation"][str(t)] = [round(sh_x, 2), round(-sh_y, 2), round(-sh_z, 2)]
        bones_data["wing_arm_right"]["rotation"][str(t)] = [round(arm_x, 2), round(-arm_y, 2), round(-arm_z, 2)]
        bones_data["wing_forearm_right"]["rotation"][str(t)] = [0.0, round(-fore_y, 2), round(-fore_z, 2)]
        bones_data["wing_fingers_right"]["rotation"][str(t)] = [0.0, 0.0, round(-fing_z, 2)]

        # Body thrust dynamics: upward lift and forward surge on downstroke
        lift_y = round(3.8 * (-s) + 1.2, 2)
        surge_z = round(2.2 * c, 2)
        pitch_x = round(7.0 - 5.5 * s, 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, surge_z]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, 0.0]

        # Vestibular neck/head stabilization
        bones_data["neck"]["rotation"][str(t)] = [round(-5.0 + 3.0 * s, 2), 0.0, 0.0]
        bones_data["neck"]["position"][str(t)] = [0.0, round(0.5 * s, 2), round(-0.8 * c, 2)]
        bones_data["neck_upper"]["rotation"][str(t)] = [round(-3.0 + 2.0 * s, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-2.0 - 1.5 * s, 2), 0.0, 0.0]

        # 4 legs aerodynamically tucked under belly
        leg_susp = 2.5 * c
        front_leg_pitch = round(50.0 + leg_susp, 2)
        front_shin_pitch = round(-42.0 - leg_susp, 2)
        front_foot_pitch = round(12.0, 2)
        bones_data["leg_front_left"]["rotation"][str(t)] = [front_leg_pitch, 0.0, 4.0]
        bones_data["leg_front_left_shin"]["rotation"][str(t)] = [front_shin_pitch, 0.0, 0.0]
        bones_data["leg_front_left_foot"]["rotation"][str(t)] = [front_foot_pitch, 0.0, 0.0]

        bones_data["leg_front_right"]["rotation"][str(t)] = [front_leg_pitch, 0.0, -4.0]
        bones_data["leg_front_right_shin"]["rotation"][str(t)] = [front_shin_pitch, 0.0, 0.0]
        bones_data["leg_front_right_foot"]["rotation"][str(t)] = [front_foot_pitch, 0.0, 0.0]

        hind_leg_pitch = round(44.0 + leg_susp, 2)
        hind_shin_pitch = round(-32.0 - leg_susp, 2)
        hind_foot_pitch = round(10.0, 2)
        bones_data["leg_left"]["rotation"][str(t)] = [hind_leg_pitch, 0.0, 5.0]
        bones_data["leg_left_shin"]["rotation"][str(t)] = [hind_shin_pitch, 0.0, 0.0]
        bones_data["leg_left_foot"]["rotation"][str(t)] = [hind_foot_pitch, 0.0, 0.0]

        bones_data["leg_right"]["rotation"][str(t)] = [hind_leg_pitch, 0.0, -5.0]
        bones_data["leg_right_shin"]["rotation"][str(t)] = [hind_shin_pitch, 0.0, 0.0]
        bones_data["leg_right_foot"]["rotation"][str(t)] = [hind_foot_pitch, 0.0, 0.0]

        # Continuous sinusoidal traveling whip wave along all 7 tail segments
        for seg_idx, (bname, amp, lag) in enumerate([
            ("tail_1", 3.0, 0.35),
            ("tail_2", 5.5, 0.70),
            ("tail_3", 8.5, 1.05),
            ("tail_4", 12.0, 1.40),
            ("tail_5", 16.0, 1.75),
            ("tail_6", 20.0, 2.10)
        ]):
            seg_pitch = round(-amp * math.sin(psi - lag), 2)
            seg_yaw = round(2.0 * math.cos(psi - lag), 2)
            bones_data[bname]["rotation"][str(t)] = [seg_pitch, seg_yaw, 0.0]

        flame_pitch = round(-24.0 * math.sin(psi - 2.45), 2)
        flame_scale = round(1.18 + 0.22 * math.sin(psi - 2.45), 2)
        bones_data["tail_flame"]["rotation"][str(t)] = [flame_pitch, 0.0, 0.0]
        bones_data["tail_flame"]["scale"][str(t)] = [flame_scale, flame_scale, flame_scale]

        fan_roll = round(6.5 * math.sin(psi - 2.2), 2)
        bones_data["tail_flame_left"]["rotation"][str(t)] = [0.0, 0.0, -fan_roll]
        bones_data["tail_flame_right"]["rotation"][str(t)] = [0.0, 0.0, fan_roll]

    return {
        "loop": True,
        "animation_length": duration,
        "bones": bones_data
    }

def generate_adult_glide(duration=4.0, frames=41):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}},
        "neck_upper": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_shoulder_left": {"rotation": {}},
        "wing_arm_left": {"rotation": {}},
        "wing_forearm_left": {"rotation": {}},
        "wing_fingers_left": {"rotation": {}},
        "wing_shoulder_right": {"rotation": {}},
        "wing_arm_right": {"rotation": {}},
        "wing_forearm_right": {"rotation": {}},
        "wing_fingers_right": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_left_shin": {"rotation": {}},
        "leg_front_left_foot": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_front_right_shin": {"rotation": {}},
        "leg_front_right_foot": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_left_shin": {"rotation": {}},
        "leg_left_foot": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "leg_right_shin": {"rotation": {}},
        "leg_right_foot": {"rotation": {}},
        "tail_1": {"rotation": {}},
        "tail_2": {"rotation": {}},
        "tail_3": {"rotation": {}},
        "tail_4": {"rotation": {}},
        "tail_5": {"rotation": {}},
        "tail_6": {"rotation": {}},
        "tail_flame": {"rotation": {}, "scale": {}},
        "tail_flame_left": {"rotation": {}},
        "tail_flame_right": {"rotation": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        s = math.sin(phi)
        c = math.cos(phi)

        lift_y = round(1.2 * s, 2)
        pitch_x = round(1.5 * c, 2)
        roll_z = round(0.8 * math.sin(phi * 2.0), 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, 0.0]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, roll_z]

        wind_flutter = round(1.4 * math.sin(phi * 3.0), 2)
        bones_data["wing_shoulder_left"]["rotation"][str(t)] = [0.0, 0.0, round(3.5 + 0.5 * s, 2)]
        bones_data["wing_arm_left"]["rotation"][str(t)] = [0.0, 0.0, 2.0]
        bones_data["wing_forearm_left"]["rotation"][str(t)] = [0.0, 0.0, 0.0]
        bones_data["wing_fingers_left"]["rotation"][str(t)] = [0.0, 0.0, wind_flutter]

        bones_data["wing_shoulder_right"]["rotation"][str(t)] = [0.0, 0.0, round(-3.5 - 0.5 * s, 2)]
        bones_data["wing_arm_right"]["rotation"][str(t)] = [0.0, 0.0, -2.0]
        bones_data["wing_forearm_right"]["rotation"][str(t)] = [0.0, 0.0, 0.0]
        bones_data["wing_fingers_right"]["rotation"][str(t)] = [0.0, 0.0, -wind_flutter]

        bones_data["neck"]["rotation"][str(t)] = [round(-2.0 - 0.8 * c, 2), 0.0, 0.0]
        bones_data["neck_upper"]["rotation"][str(t)] = [round(-1.5 - 0.5 * c, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-1.0 + 0.3 * c, 2), 0.0, 0.0]

        bones_data["leg_front_left"]["rotation"][str(t)] = [52.0, 0.0, 4.0]
        bones_data["leg_front_left_shin"]["rotation"][str(t)] = [-44.0, 0.0, 0.0]
        bones_data["leg_front_left_foot"]["rotation"][str(t)] = [14.0, 0.0, 0.0]

        bones_data["leg_front_right"]["rotation"][str(t)] = [52.0, 0.0, -4.0]
        bones_data["leg_front_right_shin"]["rotation"][str(t)] = [-44.0, 0.0, 0.0]
        bones_data["leg_front_right_foot"]["rotation"][str(t)] = [14.0, 0.0, 0.0]

        bones_data["leg_left"]["rotation"][str(t)] = [46.0, 0.0, 5.0]
        bones_data["leg_left_shin"]["rotation"][str(t)] = [-34.0, 0.0, 0.0]
        bones_data["leg_left_foot"]["rotation"][str(t)] = [12.0, 0.0, 0.0]

        bones_data["leg_right"]["rotation"][str(t)] = [46.0, 0.0, -5.0]
        bones_data["leg_right_shin"]["rotation"][str(t)] = [-34.0, 0.0, 0.0]
        bones_data["leg_right_foot"]["rotation"][str(t)] = [12.0, 0.0, 0.0]

        for seg_idx, (bname, amp) in enumerate([
            ("tail_1", 0.8),
            ("tail_2", 1.4),
            ("tail_3", 2.0),
            ("tail_4", 2.8),
            ("tail_5", 3.6),
            ("tail_6", 4.5)
        ]):
            bones_data[bname]["rotation"][str(t)] = [round(amp * 0.4 * s, 2), round(amp * math.sin(phi - seg_idx * 0.2), 2), 0.0]

        bones_data["tail_flame"]["rotation"][str(t)] = [round(2.0 * s, 2), round(5.0 * math.sin(phi - 1.2), 2), 0.0]
        bones_data["tail_flame"]["scale"][str(t)] = [1.0, 1.0, 1.0]

        aileron = round(3.0 * math.sin(phi * 2.0), 2)
        bones_data["tail_flame_left"]["rotation"][str(t)] = [0.0, 0.0, -aileron]
        bones_data["tail_flame_right"]["rotation"][str(t)] = [0.0, 0.0, aileron]

    return {
        "loop": True,
        "animation_length": duration,
        "bones": bones_data
    }

def generate_adult_eating():
    return {
        "loop": True,
        "animation_length": 3.2,
        "bones": {
            "body": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [6.0, 0.0, 0.0],
                    "1.2": [7.0, 2.0, 0.0],
                    "1.8": [6.0, -2.0, 0.0],
                    "2.4": [2.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [0.0, -1.8, -2.0],
                    "1.2": [0.0, -2.0, -1.0],
                    "2.4": [0.0, -0.6, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "neck": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [28.0, 0.0, 0.0],
                    "1.2": [24.0, 4.0, 2.0],
                    "1.8": [26.0, -4.0, -2.0],
                    "2.4": [10.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [0.0, -2.5, -3.0],
                    "1.2": [0.0, -2.0, -1.0],
                    "2.4": [0.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "neck_upper": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [22.0, 0.0, 0.0],
                    "1.2": [18.0, 3.0, 0.0],
                    "1.8": [20.0, -3.0, 0.0],
                    "2.4": [6.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "head": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [16.0, 0.0, 0.0],
                    "1.2": [12.0, 8.0, 5.0],
                    "1.5": [15.0, -6.0, -4.0],
                    "1.8": [10.0, 4.0, 2.0],
                    "2.4": [-4.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "jaw_lower": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [15.0, 0.0, 0.0],
                    "0.9": [45.0, 0.0, 0.0],
                    "1.15": [-2.0, 0.0, 0.0],
                    "1.4": [38.0, 0.0, 0.0],
                    "1.65": [0.0, 0.0, 0.0],
                    "1.9": [28.0, 0.0, 0.0],
                    "2.15": [0.0, 0.0, 0.0],
                    "2.5": [10.0, 0.0, 0.0],
                    "2.8": [0.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [-6.0, 0.0, 1.0],
                    "2.4": [-2.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.6": [-6.0, 0.0, -1.0],
                    "2.4": [-2.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0]
                }
            },
            "tail_1": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [2.0, 2.0, 0.0], "1.8": [2.0, -2.0, 0.0], "3.2": [0.0, 0.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [3.0, 4.0, 0.0], "1.8": [3.0, -4.0, 0.0], "3.2": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [6.0, 8.0, 0.0], "2.4": [-4.0, -4.0, 0.0], "3.2": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.2": [1.15, 1.15, 1.15], "2.4": [1.25, 1.25, 1.25], "3.2": [1.0, 1.0, 1.0]}
            }
        }
    }

def generate_adult_sleep():
    return {
        "loop": True,
        "animation_length": 6.0,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, -1.5], "3.0": [0.5, 0.0, -1.0], "6.0": [0.0, 0.0, -1.5]},
                "position": {"0.0": [0.0, -22.0, 0.0], "3.0": [0.0, -21.2, 0.0], "6.0": [0.0, -22.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "3.0": [1.03, 1.04, 1.02], "6.0": [1.0, 1.0, 1.0]}
            },
            "leg_front_left": {
                "rotation": {"0.0": [-25.0, 15.0, 20.0], "3.0": [-24.0, 15.0, 20.0], "6.0": [-25.0, 15.0, 20.0]}
            },
            "leg_front_left_shin": {"rotation": {"0.0": [65.0, 0.0, 0.0], "6.0": [65.0, 0.0, 0.0]}},
            "leg_front_left_foot": {"rotation": {"0.0": [-30.0, 0.0, 0.0], "6.0": [-30.0, 0.0, 0.0]}},
            "leg_front_right": {
                "rotation": {"0.0": [-25.0, -15.0, -20.0], "3.0": [-24.0, -15.0, -20.0], "6.0": [-25.0, -15.0, -20.0]}
            },
            "leg_front_right_shin": {"rotation": {"0.0": [65.0, 0.0, 0.0], "6.0": [65.0, 0.0, 0.0]}},
            "leg_front_right_foot": {"rotation": {"0.0": [-30.0, 0.0, 0.0], "6.0": [-30.0, 0.0, 0.0]}},
            "leg_left": {"rotation": {"0.0": [-40.0, 10.0, 25.0], "6.0": [-40.0, 10.0, 25.0]}},
            "leg_left_shin": {"rotation": {"0.0": [60.0, 0.0, 0.0], "6.0": [60.0, 0.0, 0.0]}},
            "leg_left_foot": {"rotation": {"0.0": [-25.0, 0.0, 0.0], "6.0": [-25.0, 0.0, 0.0]}},
            "leg_right": {"rotation": {"0.0": [-40.0, -10.0, -25.0], "6.0": [-40.0, -10.0, -25.0]}},
            "leg_right_shin": {"rotation": {"0.0": [60.0, 0.0, 0.0], "6.0": [60.0, 0.0, 0.0]}},
            "leg_right_foot": {"rotation": {"0.0": [-25.0, 0.0, 0.0], "6.0": [-25.0, 0.0, 0.0]}},
            "wing_shoulder_left": {"rotation": {"0.0": [-15.0, -10.0, -25.0], "3.0": [-14.0, -10.0, -24.0], "6.0": [-15.0, -10.0, -25.0]}},
            "wing_arm_left": {"rotation": {"0.0": [-20.0, -15.0, 15.0], "6.0": [-20.0, -15.0, 15.0]}},
            "wing_forearm_left": {"rotation": {"0.0": [10.0, 30.0, -10.0], "6.0": [10.0, 30.0, -10.0]}},
            "wing_fingers_left": {"rotation": {"0.0": [5.0, 15.0, 5.0], "6.0": [5.0, 15.0, 5.0]}},
            "wing_shoulder_right": {"rotation": {"0.0": [-15.0, 10.0, 25.0], "3.0": [-14.0, 10.0, 24.0], "6.0": [-15.0, 10.0, 25.0]}},
            "wing_arm_right": {"rotation": {"0.0": [-20.0, 15.0, -15.0], "6.0": [-20.0, 15.0, -15.0]}},
            "wing_forearm_right": {"rotation": {"0.0": [10.0, -30.0, 10.0], "6.0": [10.0, -30.0, 10.0]}},
            "wing_fingers_right": {"rotation": {"0.0": [5.0, -15.0, -5.0], "6.0": [5.0, -15.0, -5.0]}},
            "tail_1": {"rotation": {"0.0": [2.0, 12.0, 0.0], "3.0": [1.0, 12.0, 0.0], "6.0": [2.0, 12.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 18.0, 0.0], "6.0": [0.0, 18.0, 0.0]}},
            "tail_3": {"rotation": {"0.0": [-2.0, 22.0, 0.0], "6.0": [-2.0, 22.0, 0.0]}},
            "tail_4": {"rotation": {"0.0": [-4.0, 24.0, 0.0], "6.0": [-4.0, 24.0, 0.0]}},
            "tail_5": {"rotation": {"0.0": [-5.0, 22.0, 0.0], "6.0": [-5.0, 22.0, 0.0]}},
            "tail_6": {"rotation": {"0.0": [-6.0, 18.0, 0.0], "6.0": [-6.0, 18.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [-5.0, 12.0, 0.0], "6.0": [-5.0, 12.0, 0.0]},
                "scale": {"0.0": [0.85, 0.85, 0.85], "3.0": [0.92, 0.95, 0.92], "6.0": [0.85, 0.85, 0.85]}
            },
            "neck": {
                "rotation": {"0.0": [22.0, 26.0, 10.0], "3.0": [20.5, 26.0, 10.0], "6.0": [22.0, 26.0, 10.0]}
            },
            "neck_upper": {
                "rotation": {"0.0": [20.0, 32.0, 12.0], "3.0": [19.0, 32.0, 12.0], "6.0": [20.0, 32.0, 12.0]}
            },
            "head": {
                "rotation": {"0.0": [14.0, 20.0, -8.0], "3.0": [13.0, 20.0, -8.0], "6.0": [14.0, 20.0, -8.0]}
            },
            "jaw_lower": {"rotation": {"0.0": [0.0, 0.0, 0.0], "6.0": [0.0, 0.0, 0.0]}}
        }
    }

def generate_adult_wake_up():
    return {
        "loop": False,
        "animation_length": 4.0,
        "bones": {
            "body": {
                "rotation": {
                    "0.0": [0.0, 0.0, -1.5],
                    "0.8": [2.0, 0.0, 0.0],
                    "1.6": [8.0, 0.0, 0.0],
                    "2.4": [4.0, 0.0, 0.0],
                    "3.2": [0.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, -22.0, 0.0],
                    "0.8": [0.0, -20.0, 0.0],
                    "1.6": [0.0, -16.0, 2.0],
                    "2.4": [0.0, -8.0, 1.0],
                    "3.2": [0.0, -2.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "neck": {
                "rotation": {
                    "0.0": [22.0, 26.0, 10.0],
                    "0.8": [15.0, 12.0, 4.0],
                    "1.6": [-18.0, 0.0, 0.0],
                    "2.4": [-8.0, 0.0, 0.0],
                    "3.2": [4.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, 0.0, 0.0],
                    "1.6": [0.0, 2.0, -2.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "neck_upper": {
                "rotation": {
                    "0.0": [20.0, 32.0, 12.0],
                    "0.8": [12.0, 14.0, 4.0],
                    "1.6": [-14.0, 0.0, 0.0],
                    "2.4": [-4.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "head": {
                "rotation": {
                    "0.0": [14.0, 20.0, -8.0],
                    "0.8": [8.0, 8.0, 0.0],
                    "1.6": [-22.0, 0.0, 0.0],
                    "2.2": [-15.0, 0.0, 0.0],
                    "2.6": [4.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "jaw_lower": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [0.0, 0.0, 0.0],
                    "1.6": [58.0, 0.0, 0.0],
                    "2.0": [62.0, 0.0, 0.0],
                    "2.4": [0.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left": {
                "rotation": {
                    "0.0": [-25.0, 15.0, 20.0],
                    "1.6": [-35.0, 0.0, 2.0],
                    "2.8": [-10.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left_shin": {
                "rotation": {
                    "0.0": [65.0, 0.0, 0.0],
                    "1.6": [20.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_right": {
                "rotation": {
                    "0.0": [-25.0, -15.0, -20.0],
                    "1.6": [-35.0, 0.0, -2.0],
                    "2.8": [-10.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_right_shin": {
                "rotation": {
                    "0.0": [65.0, 0.0, 0.0],
                    "1.6": [20.0, 0.0, 0.0],
                    "4.0": [0.0, 0.0, 0.0]
                }
            },
            "leg_left": {
                "rotation": {"0.0": [-40.0, 10.0, 25.0], "2.4": [-15.0, 0.0, 5.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "leg_left_shin": {"rotation": {"0.0": [60.0, 0.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "leg_right": {
                "rotation": {"0.0": [-40.0, -10.0, -25.0], "2.4": [-15.0, 0.0, -5.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "leg_right_shin": {"rotation": {"0.0": [60.0, 0.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "wing_shoulder_left": {
                "rotation": {"0.0": [-15.0, -10.0, -25.0], "1.6": [0.0, 0.0, 16.0], "3.0": [0.0, 0.0, -2.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "wing_arm_left": {
                "rotation": {"0.0": [-20.0, -15.0, 15.0], "1.6": [0.0, 0.0, -8.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "wing_forearm_left": {
                "rotation": {"0.0": [10.0, 30.0, -10.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "wing_shoulder_right": {
                "rotation": {"0.0": [-15.0, 10.0, 25.0], "1.6": [0.0, 0.0, -16.0], "3.0": [0.0, 0.0, 2.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "wing_arm_right": {
                "rotation": {"0.0": [-20.0, 15.0, -15.0], "1.6": [0.0, 0.0, 8.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "wing_forearm_right": {
                "rotation": {"0.0": [10.0, -30.0, 10.0], "4.0": [0.0, 0.0, 0.0]}
            },
            "tail_1": {"rotation": {"0.0": [2.0, 12.0, 0.0], "2.4": [0.0, 4.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 18.0, 0.0], "2.4": [0.0, 6.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_3": {"rotation": {"0.0": [-2.0, 22.0, 0.0], "2.4": [0.0, 8.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_4": {"rotation": {"0.0": [-4.0, 24.0, 0.0], "2.4": [0.0, 8.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_5": {"rotation": {"0.0": [-5.0, 22.0, 0.0], "2.4": [0.0, 6.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_6": {"rotation": {"0.0": [-6.0, 18.0, 0.0], "2.4": [0.0, 4.0, 0.0], "4.0": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [-5.0, 12.0, 0.0], "2.4": [0.0, 0.0, 0.0], "4.0": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [0.85, 0.85, 0.85], "2.4": [1.15, 1.15, 1.15], "4.0": [1.0, 1.0, 1.0]}
            }
        }
    }

def generate_adult_roar():
    return {
        "loop": False,
        "animation_length": 3.5,
        "bones": {
            "body": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-6.0, 0.0, 0.0],
                    "1.3": [10.0, 0.0, 0.0],
                    "1.7": [11.5, 0.0, 0.0],
                    "2.1": [9.5, 0.0, 0.0],
                    "2.7": [4.0, 0.0, 0.0],
                    "3.5": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [0.0, -1.0, 3.0],
                    "1.3": [0.0, 1.5, -4.0],
                    "2.1": [0.0, 1.0, -3.5],
                    "2.7": [0.0, 0.0, -1.0],
                    "3.5": [0.0, 0.0, 0.0]
                },
                "scale": {
                    "0.0": [1.0, 1.0, 1.0],
                    "0.8": [1.15, 1.18, 1.12],
                    "1.3": [1.18, 1.20, 1.15],
                    "2.1": [1.16, 1.18, 1.14],
                    "2.7": [1.06, 1.06, 1.06],
                    "3.5": [1.0, 1.0, 1.0]
                }
            },
            "neck": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-22.0, 0.0, 0.0],
                    "1.3": [34.0, 0.0, 0.0],
                    "1.7": [36.0, 1.0, 0.0],
                    "2.1": [33.0, -1.0, 0.0],
                    "2.7": [12.0, 0.0, 0.0],
                    "3.5": [0.0, 0.0, 0.0]
                },
                "position": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [0.0, 1.0, 2.0],
                    "1.3": [0.0, 2.0, -8.0],
                    "2.1": [0.0, 1.5, -7.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "neck_upper": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-16.0, 0.0, 0.0],
                    "1.3": [28.0, 0.0, 0.0],
                    "1.7": [30.0, 0.0, 0.0],
                    "2.1": [27.0, 0.0, 0.0],
                    "2.7": [8.0, 0.0, 0.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "head": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-10.0, 0.0, 0.0],
                    "1.3": [22.0, 0.0, 0.0],
                    "1.7": [24.0, 0.0, 0.0],
                    "2.1": [21.0, 0.0, 0.0],
                    "2.7": [6.0, 0.0, 0.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "jaw_lower": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [18.0, 0.0, 0.0],
                    "1.3": [65.0, 0.0, 0.0],
                    "1.7": [67.0, 0.0, 0.0],
                    "2.1": [64.0, 0.0, 0.0],
                    "2.7": [12.0, 0.0, 0.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_shoulder_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-10.0, -15.0, 12.0],
                    "1.3": [15.0, -20.0, -38.0],
                    "1.7": [16.0, -20.0, -39.0],
                    "2.1": [14.0, -18.0, -36.0],
                    "2.7": [5.0, -6.0, -10.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_arm_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-5.0, 0.0, 10.0],
                    "1.3": [-10.0, 0.0, -25.0],
                    "2.1": [-8.0, 0.0, -22.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_forearm_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "1.3": [0.0, 0.0, 15.0],
                    "2.1": [0.0, 0.0, 12.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_fingers_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "1.3": [0.0, 0.0, -10.0],
                    "2.1": [0.0, 0.0, -8.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_shoulder_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-10.0, 15.0, -12.0],
                    "1.3": [15.0, 20.0, 38.0],
                    "1.7": [16.0, 20.0, 39.0],
                    "2.1": [14.0, 18.0, 36.0],
                    "2.7": [5.0, 6.0, 10.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_arm_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-5.0, 0.0, -10.0],
                    "1.3": [-10.0, 0.0, 25.0],
                    "2.1": [-8.0, 0.0, 22.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_forearm_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "1.3": [0.0, 0.0, -15.0],
                    "2.1": [0.0, 0.0, -12.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "wing_fingers_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "1.3": [0.0, 0.0, 10.0],
                    "2.1": [0.0, 0.0, 8.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-10.0, 0.0, 2.0],
                    "1.3": [16.0, 0.0, 4.0],
                    "2.1": [14.0, 0.0, 3.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_right": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.8": [-10.0, 0.0, -2.0],
                    "1.3": [16.0, 0.0, -4.0],
                    "2.1": [14.0, 0.0, -3.0],
                    "3.5": [0.0, 0.0, 0.0]
                }
            },
            "tail_1": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [4.0, 0.0, 0.0], "2.1": [4.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [8.0, 0.0, 0.0], "2.1": [8.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_3": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [12.0, 0.0, 0.0], "2.1": [12.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_4": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [16.0, 0.0, 0.0], "2.1": [16.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_5": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [20.0, 0.0, 0.0], "2.1": [20.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_6": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [24.0, 0.0, 0.0], "2.1": [24.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [28.0, 0.0, 0.0], "2.1": [28.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "0.8": [1.3, 1.3, 1.3], "1.3": [1.7, 1.9, 1.7], "2.1": [1.7, 1.9, 1.7], "3.5": [1.0, 1.0, 1.0]}
            },
            "tail_flame_left": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [0.0, 0.0, -15.0], "2.1": [0.0, 0.0, -15.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "tail_flame_right": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.3": [0.0, 0.0, 15.0], "2.1": [0.0, 0.0, 15.0], "3.5": [0.0, 0.0, 0.0]}
            }
        }
    }

print("Loaded adult animation generators successfully.")

# ---------------------------------------------------------------------------
# JUVENILE ANIMATION GENERATORS
# ---------------------------------------------------------------------------

def generate_juv_fly_flap(duration=1.1, frames=37):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}, "position": {}},
        "neck_upper": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_left": {"rotation": {}},
        "wing_left_mid": {"rotation": {}},
        "wing_left_fingers": {"rotation": {}},
        "wing_right": {"rotation": {}},
        "wing_right_mid": {"rotation": {}},
        "wing_right_fingers": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_left_shin": {"rotation": {}},
        "leg_front_left_foot": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_front_right_shin": {"rotation": {}},
        "leg_front_right_foot": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_left_shin": {"rotation": {}},
        "leg_left_foot": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "leg_right_shin": {"rotation": {}},
        "leg_right_foot": {"rotation": {}},
        "tail_1": {"rotation": {}},
        "tail_2": {"rotation": {}},
        "tail_3": {"rotation": {}},
        "tail_flame": {"rotation": {}, "scale": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        psi = phi - 0.28 * math.sin(phi)
        s = math.sin(psi)
        c = math.cos(psi)

        w_z = 32.0 * s
        w_x = -4.0 * c
        w_y = 10.0 * max(0.0, s)

        s_mid = math.sin(psi - 0.45)
        mid_z = -15.0 * max(0.0, s) + 24.0 * min(0.0, s_mid)
        mid_y = 8.0 * max(0.0, s_mid)

        s_fing = math.sin(psi - 0.75)
        fing_z = -20.0 * max(0.0, s) + 26.0 * min(0.0, s_fing)

        bones_data["wing_left"]["rotation"][str(t)] = [round(w_x, 2), round(w_y, 2), round(w_z, 2)]
        bones_data["wing_left_mid"]["rotation"][str(t)] = [0.0, round(mid_y, 2), round(mid_z, 2)]
        bones_data["wing_left_fingers"]["rotation"][str(t)] = [0.0, 0.0, round(fing_z, 2)]

        bones_data["wing_right"]["rotation"][str(t)] = [round(w_x, 2), round(-w_y, 2), round(-w_z, 2)]
        bones_data["wing_right_mid"]["rotation"][str(t)] = [0.0, round(-mid_y, 2), round(-mid_z, 2)]
        bones_data["wing_right_fingers"]["rotation"][str(t)] = [0.0, 0.0, round(-fing_z, 2)]

        lift_y = round(2.5 * (-s) + 0.8, 2)
        surge_z = round(1.5 * c, 2)
        pitch_x = round(6.0 - 4.5 * s, 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, surge_z]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, 0.0]

        bones_data["neck"]["rotation"][str(t)] = [round(-4.0 + 2.5 * s, 2), 0.0, 0.0]
        bones_data["neck_upper"]["rotation"][str(t)] = [round(-2.5 + 1.5 * s, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-1.5 - 1.0 * s, 2), 0.0, 0.0]

        leg_susp = 2.0 * c
        bones_data["leg_front_left"]["rotation"][str(t)] = [round(46.0 + leg_susp, 2), 0.0, 3.0]
        bones_data["leg_front_left_shin"]["rotation"][str(t)] = [round(-38.0 - leg_susp, 2), 0.0, 0.0]
        bones_data["leg_front_left_foot"]["rotation"][str(t)] = [10.0, 0.0, 0.0]

        bones_data["leg_front_right"]["rotation"][str(t)] = [round(46.0 + leg_susp, 2), 0.0, -3.0]
        bones_data["leg_front_right_shin"]["rotation"][str(t)] = [round(-38.0 - leg_susp, 2), 0.0, 0.0]
        bones_data["leg_front_right_foot"]["rotation"][str(t)] = [10.0, 0.0, 0.0]

        bones_data["leg_left"]["rotation"][str(t)] = [round(40.0 + leg_susp, 2), 0.0, 4.0]
        bones_data["leg_left_shin"]["rotation"][str(t)] = [round(-28.0 - leg_susp, 2), 0.0, 0.0]
        bones_data["leg_left_foot"]["rotation"][str(t)] = [8.0, 0.0, 0.0]

        bones_data["leg_right"]["rotation"][str(t)] = [round(40.0 + leg_susp, 2), 0.0, -4.0]
        bones_data["leg_right_shin"]["rotation"][str(t)] = [round(-28.0 - leg_susp, 2), 0.0, 0.0]
        bones_data["leg_right_foot"]["rotation"][str(t)] = [8.0, 0.0, 0.0]

        for seg_idx, (bname, amp, lag) in enumerate([
            ("tail_1", 3.0, 0.4),
            ("tail_2", 6.0, 0.8),
            ("tail_3", 10.0, 1.2)
        ]):
            bones_data[bname]["rotation"][str(t)] = [round(-amp * math.sin(psi - lag), 2), round(2.0 * math.cos(psi - lag), 2), 0.0]

        flame_pitch = round(-16.0 * math.sin(psi - 1.6), 2)
        flame_scale = round(1.15 + 0.2 * math.sin(psi - 1.6), 2)
        bones_data["tail_flame"]["rotation"][str(t)] = [flame_pitch, 0.0, 0.0]
        bones_data["tail_flame"]["scale"][str(t)] = [flame_scale, flame_scale, flame_scale]

    return {"loop": True, "animation_length": duration, "bones": bones_data}

def generate_juv_glide(duration=3.5, frames=37):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}},
        "neck_upper": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_left": {"rotation": {}},
        "wing_left_mid": {"rotation": {}},
        "wing_left_fingers": {"rotation": {}},
        "wing_right": {"rotation": {}},
        "wing_right_mid": {"rotation": {}},
        "wing_right_fingers": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_left_shin": {"rotation": {}},
        "leg_front_left_foot": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_front_right_shin": {"rotation": {}},
        "leg_front_right_foot": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_left_shin": {"rotation": {}},
        "leg_left_foot": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "leg_right_shin": {"rotation": {}},
        "leg_right_foot": {"rotation": {}},
        "tail_1": {"rotation": {}},
        "tail_2": {"rotation": {}},
        "tail_3": {"rotation": {}},
        "tail_flame": {"rotation": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        s = math.sin(phi)
        c = math.cos(phi)

        lift_y = round(0.9 * s, 2)
        pitch_x = round(1.2 * c, 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, 0.0]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, 0.0]

        flutter = round(1.2 * math.sin(phi * 3.0), 2)
        bones_data["wing_left"]["rotation"][str(t)] = [0.0, 0.0, round(3.0 + 0.4 * s, 2)]
        bones_data["wing_left_mid"]["rotation"][str(t)] = [0.0, 0.0, 1.5]
        bones_data["wing_left_fingers"]["rotation"][str(t)] = [0.0, 0.0, flutter]

        bones_data["wing_right"]["rotation"][str(t)] = [0.0, 0.0, round(-3.0 - 0.4 * s, 2)]
        bones_data["wing_right_mid"]["rotation"][str(t)] = [0.0, 0.0, -1.5]
        bones_data["wing_right_fingers"]["rotation"][str(t)] = [0.0, 0.0, -flutter]

        bones_data["neck"]["rotation"][str(t)] = [round(-1.5 - 0.5 * c, 2), 0.0, 0.0]
        bones_data["neck_upper"]["rotation"][str(t)] = [round(-1.0 - 0.3 * c, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-0.8 + 0.2 * c, 2), 0.0, 0.0]

        bones_data["leg_front_left"]["rotation"][str(t)] = [48.0, 0.0, 3.0]
        bones_data["leg_front_left_shin"]["rotation"][str(t)] = [-40.0, 0.0, 0.0]
        bones_data["leg_front_left_foot"]["rotation"][str(t)] = [12.0, 0.0, 0.0]

        bones_data["leg_front_right"]["rotation"][str(t)] = [48.0, 0.0, -3.0]
        bones_data["leg_front_right_shin"]["rotation"][str(t)] = [-40.0, 0.0, 0.0]
        bones_data["leg_front_right_foot"]["rotation"][str(t)] = [12.0, 0.0, 0.0]

        bones_data["leg_left"]["rotation"][str(t)] = [42.0, 0.0, 4.0]
        bones_data["leg_left_shin"]["rotation"][str(t)] = [-30.0, 0.0, 0.0]
        bones_data["leg_left_foot"]["rotation"][str(t)] = [10.0, 0.0, 0.0]

        bones_data["leg_right"]["rotation"][str(t)] = [42.0, 0.0, -4.0]
        bones_data["leg_right_shin"]["rotation"][str(t)] = [-30.0, 0.0, 0.0]
        bones_data["leg_right_foot"]["rotation"][str(t)] = [10.0, 0.0, 0.0]

        for seg_idx, (bname, amp) in enumerate([("tail_1", 1.0), ("tail_2", 2.0), ("tail_3", 3.2)]):
            bones_data[bname]["rotation"][str(t)] = [round(amp * 0.3 * s, 2), round(amp * math.sin(phi - seg_idx * 0.3), 2), 0.0]

        bones_data["tail_flame"]["rotation"][str(t)] = [round(1.5 * s, 2), round(4.0 * math.sin(phi - 1.0), 2), 0.0]

    return {"loop": True, "animation_length": duration, "bones": bones_data}

def generate_juv_eating():
    return {
        "loop": True,
        "animation_length": 2.8,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [5.0, 0.0, 0.0], "1.8": [5.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, 0.0, 0.0], "0.5": [0.0, -1.2, -1.5], "1.8": [0.0, -1.2, -1.5], "2.8": [0.0, 0.0, 0.0]}
            },
            "neck": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [26.0, 0.0, 0.0], "1.4": [22.0, 3.0, 0.0], "2.2": [8.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]}
            },
            "neck_upper": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [20.0, 0.0, 0.0], "1.4": [16.0, 0.0, 0.0], "2.2": [4.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [16.0, 0.0, 0.0], "1.0": [12.0, 6.0, 0.0], "1.5": [14.0, -5.0, 0.0], "2.2": [-3.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]}
            },
            "jaw_lower": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.5": [12.0, 0.0, 0.0],
                    "0.8": [42.0, 0.0, 0.0],
                    "1.05": [-2.0, 0.0, 0.0],
                    "1.3": [36.0, 0.0, 0.0],
                    "1.55": [0.0, 0.0, 0.0],
                    "1.8": [26.0, 0.0, 0.0],
                    "2.05": [0.0, 0.0, 0.0],
                    "2.8": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [-5.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.5": [-5.0, 0.0, 0.0], "2.8": [0.0, 0.0, 0.0]}},
            "tail_1": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.0": [2.0, 3.0, 0.0], "2.8": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.0": [4.0, 6.0, 0.0], "2.8": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.5": [1.2, 1.2, 1.2], "2.8": [1.0, 1.0, 1.0]}
            }
        }
    }

def generate_juv_sleep():
    return {
        "loop": True,
        "animation_length": 5.0,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, -1.0], "2.5": [0.5, 0.0, -0.5], "5.0": [0.0, 0.0, -1.0]},
                "position": {"0.0": [0.0, -11.0, 0.0], "2.5": [0.0, -10.5, 0.0], "5.0": [0.0, -11.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "2.5": [1.03, 1.04, 1.02], "5.0": [1.0, 1.0, 1.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [-22.0, 12.0, 15.0], "5.0": [-22.0, 12.0, 15.0]}},
            "leg_front_left_shin": {"rotation": {"0.0": [55.0, 0.0, 0.0], "5.0": [55.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [-22.0, -12.0, -15.0], "5.0": [-22.0, -12.0, -15.0]}},
            "leg_front_right_shin": {"rotation": {"0.0": [55.0, 0.0, 0.0], "5.0": [55.0, 0.0, 0.0]}},
            "leg_left": {"rotation": {"0.0": [-35.0, 10.0, 20.0], "5.0": [-35.0, 10.0, 20.0]}},
            "leg_left_shin": {"rotation": {"0.0": [50.0, 0.0, 0.0], "5.0": [50.0, 0.0, 0.0]}},
            "leg_right": {"rotation": {"0.0": [-35.0, -10.0, -20.0], "5.0": [-35.0, -10.0, -20.0]}},
            "leg_right_shin": {"rotation": {"0.0": [50.0, 0.0, 0.0], "5.0": [50.0, 0.0, 0.0]}},
            "wing_left": {"rotation": {"0.0": [-12.0, -10.0, -20.0], "5.0": [-12.0, -10.0, -20.0]}},
            "wing_left_mid": {"rotation": {"0.0": [5.0, 25.0, 10.0], "5.0": [5.0, 25.0, 10.0]}},
            "wing_right": {"rotation": {"0.0": [-12.0, 10.0, 20.0], "5.0": [-12.0, 10.0, 20.0]}},
            "wing_right_mid": {"rotation": {"0.0": [5.0, -25.0, -10.0], "5.0": [5.0, -25.0, -10.0]}},
            "tail_1": {"rotation": {"0.0": [2.0, 14.0, 0.0], "5.0": [2.0, 14.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 22.0, 0.0], "5.0": [0.0, 22.0, 0.0]}},
            "tail_3": {"rotation": {"0.0": [-2.0, 26.0, 0.0], "5.0": [-2.0, 26.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [-4.0, 20.0, 0.0], "5.0": [-4.0, 20.0, 0.0]},
                "scale": {"0.0": [0.9, 0.9, 0.9], "2.5": [0.96, 0.96, 0.96], "5.0": [0.9, 0.9, 0.9]}
            },
            "neck": {"rotation": {"0.0": [20.0, 24.0, 8.0], "2.5": [19.0, 24.0, 8.0], "5.0": [20.0, 24.0, 8.0]}},
            "neck_upper": {"rotation": {"0.0": [18.0, 28.0, 10.0], "5.0": [18.0, 28.0, 10.0]}},
            "head": {"rotation": {"0.0": [12.0, 18.0, -6.0], "5.0": [12.0, 18.0, -6.0]}}
        }
    }

def generate_juv_wake_up():
    return {
        "loop": False,
        "animation_length": 3.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, -1.0], "1.4": [6.0, 0.0, 0.0], "2.5": [2.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, -11.0, 0.0], "1.4": [0.0, -8.0, 1.0], "2.5": [0.0, -2.0, 0.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "neck": {
                "rotation": {"0.0": [20.0, 24.0, 8.0], "1.4": [-15.0, 0.0, 0.0], "2.5": [4.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "neck_upper": {
                "rotation": {"0.0": [18.0, 28.0, 10.0], "1.4": [-12.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {"0.0": [12.0, 18.0, -6.0], "1.4": [-18.0, 0.0, 0.0], "2.2": [4.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "jaw_lower": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.4": [52.0, 0.0, 0.0], "1.8": [56.0, 0.0, 0.0], "2.2": [0.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [-22.0, 12.0, 15.0], "1.4": [-30.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "leg_front_left_shin": {"rotation": {"0.0": [55.0, 0.0, 0.0], "1.4": [15.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [-22.0, -12.0, -15.0], "1.4": [-30.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "leg_front_right_shin": {"rotation": {"0.0": [55.0, 0.0, 0.0], "1.4": [15.0, 0.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "wing_left": {"rotation": {"0.0": [-12.0, -10.0, -20.0], "1.4": [0.0, 0.0, 18.0], "3.5": [0.0, 0.0, 0.0]}},
            "wing_right": {"rotation": {"0.0": [-12.0, 10.0, 20.0], "1.4": [0.0, 0.0, -18.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_1": {"rotation": {"0.0": [2.0, 14.0, 0.0], "2.5": [0.0, 2.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 22.0, 0.0], "3.5": [0.0, 0.0, 0.0]}},
            "tail_flame": {"rotation": {"0.0": [-4.0, 20.0, 0.0], "3.5": [0.0, 0.0, 0.0]}}
        }
    }

def generate_juv_roar():
    return {
        "loop": False,
        "animation_length": 3.0,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-5.0, 0.0, 0.0], "1.2": [8.0, 0.0, 0.0], "2.2": [3.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, 0.0, 0.0], "0.7": [0.0, -0.6, 1.5], "1.2": [0.0, 1.0, -2.5], "3.0": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "0.7": [1.12, 1.15, 1.10], "1.2": [1.14, 1.16, 1.12], "3.0": [1.0, 1.0, 1.0]}
            },
            "neck": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-18.0, 0.0, 0.0], "1.2": [30.0, 0.0, 0.0], "2.2": [8.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "neck_upper": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-12.0, 0.0, 0.0], "1.2": [24.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-8.0, 0.0, 0.0], "1.2": [18.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "jaw_lower": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [14.0, 0.0, 0.0], "1.2": [58.0, 0.0, 0.0], "2.0": [56.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "wing_left": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-8.0, 0.0, 10.0], "1.2": [12.0, 0.0, -32.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "wing_left_mid": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [0.0, 0.0, 14.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "wing_right": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-8.0, 0.0, -10.0], "1.2": [12.0, 0.0, 32.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "wing_right_mid": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [0.0, 0.0, -14.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-8.0, 0.0, 0.0], "1.2": [12.0, 0.0, 2.0], "3.0": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.7": [-8.0, 0.0, 0.0], "1.2": [12.0, 0.0, -2.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_1": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [4.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_2": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [8.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_3": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [12.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.2": [16.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.2": [1.4, 1.5, 1.4], "3.0": [1.0, 1.0, 1.0]}
            }
        }
    }

print("Loaded juvenile animation generators successfully.")

# ---------------------------------------------------------------------------
# HATCHLING (CHIBI) ANIMATION GENERATORS
# ---------------------------------------------------------------------------

def generate_hatch_fly_flap(duration=0.65, frames=25):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_left": {"rotation": {}},
        "wing_right": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "tail_base": {"rotation": {}},
        "tail_mid": {"rotation": {}},
        "tail_flame": {"rotation": {}, "scale": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        s = math.sin(phi)
        c = math.cos(phi)

        w_z = 45.0 * s
        w_x = -6.0 * c

        bones_data["wing_left"]["rotation"][str(t)] = [round(w_x, 2), 0.0, round(w_z, 2)]
        bones_data["wing_right"]["rotation"][str(t)] = [round(w_x, 2), 0.0, round(-w_z, 2)]

        lift_y = round(1.2 * (-s) + 0.3, 2)
        pitch_x = round(5.0 - 4.0 * s, 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, 0.0]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, 0.0]

        bones_data["neck"]["rotation"][str(t)] = [round(-3.0 + 2.0 * s, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-1.0 - 1.0 * s, 2), 0.0, 0.0]

        bones_data["leg_front_left"]["rotation"][str(t)] = [30.0, 0.0, 0.0]
        bones_data["leg_front_right"]["rotation"][str(t)] = [30.0, 0.0, 0.0]
        bones_data["leg_left"]["rotation"][str(t)] = [25.0, 0.0, 0.0]
        bones_data["leg_right"]["rotation"][str(t)] = [25.0, 0.0, 0.0]

        bones_data["tail_base"]["rotation"][str(t)] = [round(-4.0 * s, 2), 0.0, 0.0]
        bones_data["tail_mid"]["rotation"][str(t)] = [round(-8.0 * math.sin(phi - 0.5), 2), 0.0, 0.0]
        bones_data["tail_flame"]["rotation"][str(t)] = [round(-12.0 * math.sin(phi - 1.0), 2), 0.0, 0.0]
        bones_data["tail_flame"]["scale"][str(t)] = [round(1.1 + 0.15 * s, 2), round(1.1 + 0.15 * s, 2), round(1.1 + 0.15 * s, 2)]

    return {"loop": True, "animation_length": duration, "bones": bones_data}

def generate_hatch_glide(duration=2.5, frames=25):
    bones_data = {
        "body": {"rotation": {}, "position": {}},
        "neck": {"rotation": {}},
        "head": {"rotation": {}},
        "wing_left": {"rotation": {}},
        "wing_right": {"rotation": {}},
        "leg_front_left": {"rotation": {}},
        "leg_front_right": {"rotation": {}},
        "leg_left": {"rotation": {}},
        "leg_right": {"rotation": {}},
        "tail_base": {"rotation": {}},
        "tail_mid": {"rotation": {}},
        "tail_flame": {"rotation": {}}
    }

    for i in range(frames):
        t = round(i * (duration / (frames - 1)), 3)
        phi = (t / duration) * 2 * math.pi
        s = math.sin(phi)
        c = math.cos(phi)

        lift_y = round(0.5 * s, 2)
        pitch_x = round(1.0 * c, 2)
        roll_z = round(1.5 * math.sin(phi * 2.0), 2)
        bones_data["body"]["position"][str(t)] = [0.0, lift_y, 0.0]
        bones_data["body"]["rotation"][str(t)] = [pitch_x, 0.0, roll_z]

        flutter = round(2.0 * math.sin(phi * 3.0), 2)
        bones_data["wing_left"]["rotation"][str(t)] = [0.0, 0.0, round(4.0 + flutter, 2)]
        bones_data["wing_right"]["rotation"][str(t)] = [0.0, 0.0, round(-4.0 - flutter, 2)]

        bones_data["neck"]["rotation"][str(t)] = [round(-1.0 - 0.5 * c, 2), 0.0, 0.0]
        bones_data["head"]["rotation"][str(t)] = [round(-0.5 + 0.3 * c, 2), 0.0, 0.0]

        bones_data["leg_front_left"]["rotation"][str(t)] = [32.0, 0.0, 0.0]
        bones_data["leg_front_right"]["rotation"][str(t)] = [32.0, 0.0, 0.0]
        bones_data["leg_left"]["rotation"][str(t)] = [28.0, 0.0, 0.0]
        bones_data["leg_right"]["rotation"][str(t)] = [28.0, 0.0, 0.0]

        bones_data["tail_base"]["rotation"][str(t)] = [round(1.0 * s, 2), round(2.0 * math.sin(phi), 2), 0.0]
        bones_data["tail_mid"]["rotation"][str(t)] = [round(1.5 * s, 2), round(3.5 * math.sin(phi - 0.4), 2), 0.0]
        bones_data["tail_flame"]["rotation"][str(t)] = [round(2.0 * s, 2), round(5.0 * math.sin(phi - 0.8), 2), 0.0]

    return {"loop": True, "animation_length": duration, "bones": bones_data}

def generate_hatch_eating():
    return {
        "loop": True,
        "animation_length": 2.2,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.4": [4.0, 0.0, 0.0], "1.6": [4.0, 0.0, 0.0], "2.2": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, 0.0, 0.0], "0.4": [0.0, -0.6, -0.8], "1.6": [0.0, -0.6, -0.8], "2.2": [0.0, 0.0, 0.0]}
            },
            "neck": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.4": [22.0, 0.0, 0.0], "1.4": [20.0, 0.0, 0.0], "1.8": [4.0, 0.0, 0.0], "2.2": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {
                    "0.0": [0.0, 0.0, 0.0],
                    "0.4": [18.0, 0.0, 0.0],
                    "0.65": [26.0, 5.0, 0.0],
                    "0.9": [14.0, -5.0, 0.0],
                    "1.15": [24.0, 4.0, 0.0],
                    "1.4": [16.0, -3.0, 0.0],
                    "1.8": [-4.0, 0.0, 0.0],
                    "2.2": [0.0, 0.0, 0.0]
                }
            },
            "leg_front_left": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.4": [-4.0, 0.0, 0.0], "2.2": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.4": [-4.0, 0.0, 0.0], "2.2": [0.0, 0.0, 0.0]}},
            "tail_base": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.8": [0.0, 6.0, 0.0], "1.4": [0.0, -6.0, 0.0], "2.2": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.8": [0.0, 10.0, 0.0], "1.4": [0.0, -10.0, 0.0], "2.2": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.2": [1.3, 1.3, 1.3], "2.2": [1.0, 1.0, 1.0]}
            }
        }
    }

def generate_hatch_sleep():
    return {
        "loop": True,
        "animation_length": 4.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, -1.0], "2.25": [0.5, 0.0, -0.5], "4.5": [0.0, 0.0, -1.0]},
                "position": {"0.0": [0.0, -4.0, 0.0], "2.25": [0.0, -3.7, 0.0], "4.5": [0.0, -4.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "2.25": [1.04, 1.05, 1.04], "4.5": [1.0, 1.0, 1.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [-20.0, 10.0, 15.0], "4.5": [-20.0, 10.0, 15.0]}},
            "leg_front_right": {"rotation": {"0.0": [-20.0, -10.0, -15.0], "4.5": [-20.0, -10.0, -15.0]}},
            "leg_left": {"rotation": {"0.0": [-25.0, 8.0, 15.0], "4.5": [-25.0, 8.0, 15.0]}},
            "leg_right": {"rotation": {"0.0": [-25.0, -8.0, -15.0], "4.5": [-25.0, -8.0, -15.0]}},
            "wing_left": {"rotation": {"0.0": [-10.0, -8.0, -15.0], "4.5": [-10.0, -8.0, -15.0]}},
            "wing_right": {"rotation": {"0.0": [-10.0, 8.0, 15.0], "4.5": [-10.0, 8.0, 15.0]}},
            "tail_base": {"rotation": {"0.0": [0.0, 16.0, 0.0], "4.5": [0.0, 16.0, 0.0]}},
            "tail_mid": {"rotation": {"0.0": [0.0, 24.0, 0.0], "4.5": [0.0, 24.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 24.0, 0.0], "4.5": [0.0, 24.0, 0.0]},
                "scale": {"0.0": [0.9, 0.9, 0.9], "2.25": [0.95, 0.98, 0.95], "4.5": [0.9, 0.9, 0.9]}
            },
            "neck": {"rotation": {"0.0": [14.0, 18.0, 6.0], "2.25": [13.0, 18.0, 6.0], "4.5": [14.0, 18.0, 6.0]}},
            "head": {"rotation": {"0.0": [10.0, 14.0, -4.0], "4.5": [10.0, 14.0, -4.0]}}
        }
    }

def generate_hatch_wake_up():
    return {
        "loop": False,
        "animation_length": 3.0,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, -1.0], "1.2": [5.0, 0.0, 0.0], "2.2": [1.5, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, -4.0, 0.0], "1.2": [0.0, -2.5, 0.5], "2.2": [0.0, -0.6, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "neck": {
                "rotation": {"0.0": [14.0, 18.0, 6.0], "1.2": [-12.0, 0.0, 0.0], "2.2": [2.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {"0.0": [10.0, 14.0, -4.0], "1.2": [-16.0, 0.0, 0.0], "1.6": [-18.0, 0.0, 0.0], "2.2": [3.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [-20.0, 10.0, 15.0], "1.2": [-25.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [-20.0, -10.0, -15.0], "1.2": [-25.0, 0.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "wing_left": {"rotation": {"0.0": [-10.0, -8.0, -15.0], "1.2": [0.0, 0.0, 20.0], "3.0": [0.0, 0.0, 0.0]}},
            "wing_right": {"rotation": {"0.0": [-10.0, 8.0, 15.0], "1.2": [0.0, 0.0, -20.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_base": {"rotation": {"0.0": [0.0, 16.0, 0.0], "2.2": [0.0, 4.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_mid": {"rotation": {"0.0": [0.0, 24.0, 0.0], "3.0": [0.0, 0.0, 0.0]}},
            "tail_flame": {"rotation": {"0.0": [0.0, 24.0, 0.0], "3.0": [0.0, 0.0, 0.0]}}
        }
    }

def generate_hatch_roar():
    return {
        "loop": False,
        "animation_length": 2.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-4.0, 0.0, 0.0], "1.0": [6.0, 0.0, 0.0], "1.8": [2.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]},
                "position": {"0.0": [0.0, 0.0, 0.0], "0.6": [0.0, -0.4, 0.8], "1.0": [0.0, 0.6, -1.2], "2.5": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "0.6": [1.14, 1.18, 1.12], "1.0": [1.16, 1.20, 1.14], "2.5": [1.0, 1.0, 1.0]}
            },
            "neck": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-14.0, 0.0, 0.0], "1.0": [25.0, 0.0, 0.0], "1.8": [6.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]}
            },
            "head": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-8.0, 0.0, 0.0], "1.0": [22.0, 0.0, 0.0], "1.6": [20.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]}
            },
            "wing_left": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-6.0, 0.0, 12.0], "1.0": [10.0, 0.0, -38.0], "2.5": [0.0, 0.0, 0.0]}
            },
            "wing_right": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-6.0, 0.0, -12.0], "1.0": [10.0, 0.0, 38.0], "2.5": [0.0, 0.0, 0.0]}
            },
            "leg_front_left": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-6.0, 0.0, 0.0], "1.0": [10.0, 0.0, 2.0], "2.5": [0.0, 0.0, 0.0]}},
            "leg_front_right": {"rotation": {"0.0": [0.0, 0.0, 0.0], "0.6": [-6.0, 0.0, 0.0], "1.0": [10.0, 0.0, -2.0], "2.5": [0.0, 0.0, 0.0]}},
            "tail_base": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.0": [4.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]}},
            "tail_mid": {"rotation": {"0.0": [0.0, 0.0, 0.0], "1.0": [8.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]}},
            "tail_flame": {
                "rotation": {"0.0": [0.0, 0.0, 0.0], "1.0": [14.0, 0.0, 0.0], "2.5": [0.0, 0.0, 0.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.0": [1.5, 1.7, 1.5], "2.5": [1.0, 1.0, 1.0]}
            }
        }
    }

print("Loaded hatchling animation generators successfully.")

# ---------------------------------------------------------------------------
# PIPELINE APPLICATION & SYNCHRONIZATION
# ---------------------------------------------------------------------------

MODELS_DIR = r"D:\Mine\models\flamefang"
ANIM_DIR = r"D:\Mine\src\main\resources\assets\wingsofthewild\animations"

def build_bbmodel_animations(anims_dict, bone_uuid_map):
    bb_animations = []
    for a_key, a_val in anims_dict.items():
        aname = a_key.split(".")[-1]
        animators = {}
        for bname, channels in a_val.get("bones", {}).items():
            if bname not in bone_uuid_map:
                continue
            buuid = bone_uuid_map[bname]
            keyframes = []
            for ch_name in ["rotation", "position", "scale"]:
                if ch_name in channels:
                    for t_str, vec in channels[ch_name].items():
                        keyframes.append({
                            "channel": ch_name,
                            "time": float(t_str),
                            "data_points": [{"x": vec[0], "y": vec[1], "z": vec[2]}],
                            "interpolation": "linear",
                            "uuid": str(uuid.uuid4())
                        })
            animators[buuid] = {
                "name": bname,
                "type": "bone",
                "keyframes": keyframes
            }
        is_loop = a_val.get("loop", True)
        bb_animations.append({
            "name": aname,
            "uuid": str(uuid.uuid4()),
            "loop": "loop" if is_loop else "once",
            "length": a_val.get("animation_length", 1.0),
            "animators": animators
        })
    return bb_animations

def update_stage(model_name, bbmodel_filename, anim_generators_dict):
    print(f"\nUpdating {model_name}...")
    bb_path = os.path.join(MODELS_DIR, bbmodel_filename)
    anim_path = os.path.join(ANIM_DIR, f"{model_name}.animation.json")

    with open(bb_path, "r", encoding="utf-8") as f:
        bb = json.load(f)

    bone_uuid_map = {}
    for g in bb.get("groups", []):
        bone_uuid_map[g["name"]] = g["uuid"]

    # Also check existing animations animators if any missing
    for anim in bb.get("animations", []):
        for buuid, adata in anim.get("animators", {}).items():
            bname = adata.get("name")
            if bname and bname not in bone_uuid_map:
                bone_uuid_map[bname] = buuid

    print(f"  Found {len(bone_uuid_map)} bones in {bbmodel_filename}")

    # Build animations dict
    with open(anim_path, "r", encoding="utf-8") as f:
        existing_anim_data = json.load(f)

    anims_dict = existing_anim_data.get("animations", {})

    # Replace / inject new animations
    for anim_name, anim_content in anim_generators_dict.items():
        full_key = f"animation.{model_name}.{anim_name}"
        anims_dict[full_key] = anim_content
        print(f"  [+] Integrated {anim_name} (length: {anim_content['animation_length']}s, loop: {anim_content['loop']})")

    # Save animation.json
    existing_anim_data["animations"] = anims_dict
    with open(anim_path, "w", encoding="utf-8") as f:
        json.dump(existing_anim_data, f, indent=2)
    print(f"  Saved animation JSON: {anim_path}")

    # Build bbmodel animations
    bb_animations = build_bbmodel_animations(anims_dict, bone_uuid_map)
    bb["animations"] = bb_animations

    with open(bb_path, "w", encoding="utf-8") as f:
        json.dump(bb, f, indent=2)
    print(f"  Saved Blockbench model: {bb_path} ({len(bb_animations)} animations)")

def run():
    # 1. Adult
    adult_new_anims = {
        "fly_flap": generate_adult_fly_flap(duration=1.4, frames=43),
        "glide": generate_adult_glide(duration=4.0, frames=41),
        "eating": generate_adult_eating(),
        "sleep": generate_adult_sleep(),
        "wake_up": generate_adult_wake_up(),
        "roar": generate_adult_roar()
    }
    update_stage("flamefang_adult", "flamefang_adult_geckolib.bbmodel", adult_new_anims)

    # 2. Juvenile
    juv_new_anims = {
        "fly_flap": generate_juv_fly_flap(duration=1.1, frames=37),
        "glide": generate_juv_glide(duration=3.5, frames=37),
        "eating": generate_juv_eating(),
        "sleep": generate_juv_sleep(),
        "wake_up": generate_juv_wake_up(),
        "roar": generate_juv_roar()
    }
    update_stage("flamefang_juvenile", "flamefang_Juvenil_geckolib.bbmodel", juv_new_anims)

    # 3. Hatchling
    hatch_new_anims = {
        "fly_flap": generate_hatch_fly_flap(duration=0.65, frames=25),
        "glide": generate_hatch_glide(duration=2.5, frames=25),
        "eating": generate_hatch_eating(),
        "sleep": generate_hatch_sleep(),
        "wake_up": generate_hatch_wake_up(),
        "roar": generate_hatch_roar()
    }
    update_stage("flamefang_hatchling", "flamefang_hatchling_geckolib.bbmodel", hatch_new_anims)

if __name__ == "__main__":
    run()
    print("\n[ALL ANIMATIONS SUCCESSFULLY INTEGRATED AND SAVED!]")
