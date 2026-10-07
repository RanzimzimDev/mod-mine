import json
import math
import os
import uuid
import base64
from PIL import Image

BASE_DIR = r"D:\Mine"
MODELS_DIR = os.path.join(BASE_DIR, "models", "flamefang")
GEO_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "assets", "wingsofthewild", "geo")
TEX_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "assets", "wingsofthewild", "textures", "entity")
ANIM_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "assets", "wingsofthewild", "animations")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(GEO_DIR, exist_ok=True)
os.makedirs(TEX_DIR, exist_ok=True)
os.makedirs(ANIM_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Utility Helpers
# ---------------------------------------------------------------------------
def noise(x, y, factor=12):
    val = int(math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % factor
    return val - factor // 2

def shade(color, delta):
    r = max(0, min(255, color[0] + delta))
    g = max(0, min(255, color[1] + delta))
    b = max(0, min(255, color[2] + delta))
    a = color[3] if len(color) > 3 else 255
    return (r, g, b, a)

def pack_uvs(cubes_list, tex_w, tex_h, padding=2):
    unique_items_map = {}
    for c in cubes_list:
        uv_group = c.get('uv_group', c['name'])
        sx, sy, sz = c['size']
        pw = int(math.ceil(2 * (sx + sz)))
        ph = int(math.ceil(sz + sy))
        if uv_group not in unique_items_map:
            unique_items_map[uv_group] = [pw, ph]
        else:
            unique_items_map[uv_group][0] = max(unique_items_map[uv_group][0], pw)
            unique_items_map[uv_group][1] = max(unique_items_map[uv_group][1], ph)

    unique_items = [(gid, dims[0], dims[1]) for gid, dims in unique_items_map.items()]

    # Sort descending by height, then width
    unique_items.sort(key=lambda item: (item[2], item[1]), reverse=True)

    shelves = []
    current_y = 0
    uv_map = {}

    for gid, pw, ph in unique_items:
        placed = False
        for s in shelves:
            if s['rem_w'] >= pw and s['h'] >= ph:
                uv_map[gid] = [s['x'], s['y']]
                s['x'] += pw + padding
                s['rem_w'] -= (pw + padding)
                placed = True
                break
        if not placed:
            if current_y + ph <= tex_h and pw <= tex_w:
                shelves.append({'y': current_y, 'h': ph, 'x': pw + padding, 'rem_w': tex_w - (pw + padding)})
                uv_map[gid] = [0, current_y]
                current_y += ph + padding
                placed = True
            else:
                raise ValueError(f"Texture canvas ({tex_w}x{tex_h}) overflow packing {gid} ({pw}x{ph}) at y={current_y}")

    for c in cubes_list:
        gid = c.get('uv_group', c['name'])
        c['uv'] = uv_map[gid]

    return uv_map

# ---------------------------------------------------------------------------
# ADULT FLAMEFANG ANATOMY — HARMONIC 3D PROPORTIONS (NON-FLATTENED)
# Imposing, noble, apex predatory dragon (style Monster Hunter / ARK Wyvern)
#
# - Torso Height: 26-28 units (Y: 24 to 52). Deep chest keel & massive pectorals.
# - Torso Width: 36-42 units (X: -21 to +21 at shoulders, -18 to +18 mid-torso).
# - Ratio Width/Height: ~1.4 (Athletic, powerful, eliminates flat pancake look!).
# - Legs: Long, muscular quadrupedal limbs raising belly 24-28 units above ground.
#   All 4 feet planted firmly at Y = 0 with sharp raptorial talons.
# - Neck & Head: Serpentine noble S-curve raising cranium to Y = 78 and horns to Y = 88.
#   Total creature height: 5.5 blocks (88 units).
# - Wings: 4-joint chain with 284-unit colossal wingspan (~17.8 blocks).
# - Tail: 7-stage articulated chain (9 bones) tapering from 20 to 6 width,
#   ending in a 37-unit wide glowing magma fan blade.
# ---------------------------------------------------------------------------

adult_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 42, 0],
        "cubes": [
            # 1. Deep chest keel (prominent flight muscle anchor, 28 width, 22 height)
            {"name": "chest_keel_l", "origin": [0, 24, -26], "size": [14, 22, 16], "category": "torso_chest", "uv_group": "chest_keel_half"},
            {"name": "chest_keel_r", "origin": [-14, 24, -26], "size": [14, 22, 16], "category": "torso_chest", "uv_group": "chest_keel_half"},
            # 2. Heavy pectoral armor plates (32 width, 18 height)
            {"name": "pectoral_armor_l", "origin": [0, 26, -24], "size": [16, 18, 10], "category": "chest_armor", "uv_group": "pectoral_half"},
            {"name": "pectoral_armor_r", "origin": [-16, 26, -24], "size": [16, 18, 10], "category": "chest_armor", "uv_group": "pectoral_half"},
            # 3. Broad muscular shoulder girdle (42 width total: X from -21 to +21)
            {"name": "shoulder_girdle_l", "origin": [0, 38, -18], "size": [21, 12, 12], "category": "torso_back", "uv_group": "shoulder_girdle_half"},
            {"name": "shoulder_girdle_r", "origin": [-21, 38, -18], "size": [21, 12, 12], "category": "torso_back", "uv_group": "shoulder_girdle_half"},
            # 4. Mid torso ribcage (36 width, 22 height: X from -18 to +18, Y from 28 to 50)
            {"name": "torso_mid_l", "origin": [0, 28, -14], "size": [18, 22, 16], "category": "torso_mid", "uv_group": "torso_mid_half"},
            {"name": "torso_mid_r", "origin": [-18, 28, -14], "size": [18, 22, 16], "category": "torso_mid", "uv_group": "torso_mid_half"},
            # 5. Tapered belly (32 width, 18 height: X from -16 to +16, Y from 30 to 48)
            {"name": "belly_mid_l", "origin": [0, 30, 2], "size": [16, 18, 14], "category": "torso_belly", "uv_group": "belly_half"},
            {"name": "belly_mid_r", "origin": [-16, 30, 2], "size": [16, 18, 14], "category": "torso_belly", "uv_group": "belly_half"},
            # 6. Muscular pelvis / hips (34 width, 18 height: X from -17 to +17, Y from 32 to 50)
            {"name": "pelvis_hips_l", "origin": [0, 32, 16], "size": [17, 18, 14], "category": "torso_hips", "uv_group": "pelvis_half"},
            {"name": "pelvis_hips_r", "origin": [-17, 32, 16], "size": [17, 18, 14], "category": "torso_hips", "uv_group": "pelvis_half"},
            # 7. Tiered dorsal spines along the central back
            {"name": "dorsal_spines", "origin": [-2.5, 48, -18], "size": [5, 8, 32], "category": "spikes", "uv_group": "dorsal_spines"}
        ]
    },
    # -------------------------------------------------------------
    # FRONT LEGS (ATHLETIC DIGITIGRADE FORELIMBS, GROUND Y = 0)
    # Stance at X = ±20, raising shoulders high to Y = 42
    # -------------------------------------------------------------
    {
        "name": "leg_front_left",
        "parent": "body",
        "pivot": [20, 42, -14],
        "cubes": [
            {"name": "shoulder_front_left", "origin": [14, 22, -21], "size": [12, 22, 14], "category": "leg", "uv_group": "leg_front_upper"},
            {"name": "shoulder_plate_fl", "origin": [14, 32, -22], "size": [12.5, 10, 15], "category": "spikes", "uv_group": "shoulder_plate"}
        ]
    },
    {
        "name": "leg_front_left_shin",
        "parent": "leg_front_left",
        "pivot": [20, 22, -14],
        "cubes": [
            {"name": "shin_front_left", "origin": [15, 4, -20], "size": [10, 20, 11], "category": "leg", "uv_group": "shin_column"},
            {"name": "elbow_spur_fl", "origin": [17, 18, -9], "size": [6, 6, 6], "category": "spikes", "uv_group": "elbow_spur"},
            {"name": "carpal_fl", "origin": [15.5, 2, -19.5], "size": [9, 5, 10], "category": "leg", "uv_group": "carpal_joint"}
        ]
    },
    {
        "name": "leg_front_left_foot",
        "parent": "leg_front_left_shin",
        "pivot": [20, 4, -15],
        "cubes": [
            {"name": "foot_pad_fl", "origin": [13.5, 0, -22], "size": [13, 5, 14], "category": "foot", "uv_group": "foot_pad"},
            {"name": "toe_fl_outer", "origin": [21.5, 0, -28], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_fl_outer", "origin": [22, 0, -33], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "toe_fl_mid", "origin": [18, 0, -30], "size": [4.5, 4, 10], "category": "claw", "uv_group": "toe_mid"},
            {"name": "claw_fl_mid", "origin": [18.5, 0, -36], "size": [3, 3, 6], "category": "claw", "uv_group": "claw_mid"},
            {"name": "toe_fl_inner", "origin": [14, 0, -28], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_fl_inner", "origin": [14.5, 0, -33], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "claw_fl_rear", "origin": [18.5, 0.5, -9], "size": [3.5, 3, 5], "category": "claw", "uv_group": "claw_rear"}
        ]
    },
    {
        "name": "leg_front_right",
        "parent": "body",
        "pivot": [-20, 42, -14],
        "cubes": [
            {"name": "shoulder_front_right", "origin": [-26, 22, -21], "size": [12, 22, 14], "category": "leg", "uv_group": "leg_front_upper"},
            {"name": "shoulder_plate_fr", "origin": [-26.5, 32, -22], "size": [12.5, 10, 15], "category": "spikes", "uv_group": "shoulder_plate"}
        ]
    },
    {
        "name": "leg_front_right_shin",
        "parent": "leg_front_right",
        "pivot": [-20, 22, -14],
        "cubes": [
            {"name": "shin_front_right", "origin": [-25, 4, -20], "size": [10, 20, 11], "category": "leg", "uv_group": "shin_column"},
            {"name": "elbow_spur_fr", "origin": [-23, 18, -9], "size": [6, 6, 6], "category": "spikes", "uv_group": "elbow_spur"},
            {"name": "carpal_fr", "origin": [-24.5, 2, -19.5], "size": [9, 5, 10], "category": "leg", "uv_group": "carpal_joint"}
        ]
    },
    {
        "name": "leg_front_right_foot",
        "parent": "leg_front_right_shin",
        "pivot": [-20, 4, -15],
        "cubes": [
            {"name": "foot_pad_fr", "origin": [-26.5, 0, -22], "size": [13, 5, 14], "category": "foot", "uv_group": "foot_pad"},
            {"name": "toe_fr_outer", "origin": [-25.5, 0, -28], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_fr_outer", "origin": [-24.5, 0, -33], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "toe_fr_mid", "origin": [-22.5, 0, -30], "size": [4.5, 4, 10], "category": "claw", "uv_group": "toe_mid"},
            {"name": "claw_fr_mid", "origin": [-21.5, 0, -36], "size": [3, 3, 6], "category": "claw", "uv_group": "claw_mid"},
            {"name": "toe_fr_inner", "origin": [-18, 0, -28], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_fr_inner", "origin": [-17, 0, -33], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "claw_fr_rear", "origin": [-22, 0.5, -9], "size": [3.5, 3, 5], "category": "claw", "uv_group": "claw_rear"}
        ]
    },
    # -------------------------------------------------------------
    # NECK, HEAD & HORNS (ERECT MAJESTIC S-CURVE, CROWNING AT Y = 88)
    # -------------------------------------------------------------
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 46, -18],
        "cubes": [
            {"name": "neck_lower", "origin": [-8, 38, -30], "size": [16, 18, 14], "category": "neck", "uv_group": "neck_lower_wide"},
            {"name": "neck_spines_lower", "origin": [-1.5, 54, -28], "size": [3, 7, 10], "category": "spikes", "uv_group": "neck_spines"}
        ]
    },
    {
        "name": "neck_upper",
        "parent": "neck",
        "pivot": [0, 56, -28],
        "cubes": [
            {"name": "neck_upper_main", "origin": [-7, 52, -40], "size": [14, 18, 14], "category": "neck", "uv_group": "neck_upper_wide"},
            {"name": "neck_spines_upper", "origin": [-1.5, 68, -38], "size": [3, 7, 10], "category": "spikes", "uv_group": "neck_spines"}
        ]
    },
    {
        "name": "head",
        "parent": "neck_upper",
        "pivot": [0, 68, -38],
        "cubes": [
            {"name": "cranium", "origin": [-8, 64, -54], "size": [16, 14, 16], "category": "head", "uv_group": "cranium_wide"},
            {"name": "brow_ridges", "origin": [-7.5, 76, -52], "size": [15, 4, 10], "category": "spikes", "uv_group": "brow_ridges"},
            {"name": "snout_upper", "origin": [-6, 64, -66], "size": [12, 10, 14], "category": "snout", "uv_group": "snout_upper_wide"}
        ]
    },
    {
        "name": "jaw_lower",
        "parent": "head",
        "pivot": [0, 64, -50],
        "cubes": [
            {"name": "jaw", "origin": [-5.5, 59, -64], "size": [11, 6, 14], "category": "jaw", "uv_group": "jaw_wide"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 76, -48],
        "cubes": [
            {"name": "horn_left_main", "origin": [5, 74, -46], "size": [4, 6, 14], "category": "horn", "uv_group": "horn_main"},
            {"name": "horn_left_tip", "origin": [7, 78, -34], "size": [3, 3, 10], "category": "horn", "uv_group": "horn_tip"},
            {"name": "horn_right_main", "origin": [-9, 74, -46], "size": [4, 6, 14], "category": "horn", "uv_group": "horn_main"},
            {"name": "horn_right_tip", "origin": [-10, 78, -34], "size": [3, 3, 10], "category": "horn", "uv_group": "horn_tip"},
            {"name": "cheek_spikes", "origin": [-11, 63, -50], "size": [22, 4, 4], "category": "spikes", "uv_group": "cheek_spikes"}
        ]
    },
    # -------------------------------------------------------------
    # COLOSSAL HIND LEGS & RAPTOR FEET (GROUND Y = 0)
    # Stance at X = ±18, raising pelvis high to Y = 42
    # -------------------------------------------------------------
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [18, 42, 18],
        "cubes": [
            {"name": "thigh_left", "origin": [12, 20, 10], "size": [14, 24, 16], "category": "leg", "uv_group": "thigh_muscle"}
        ]
    },
    {
        "name": "leg_left_shin",
        "parent": "leg_left",
        "pivot": [19, 22, 18],
        "cubes": [
            {"name": "shin_left", "origin": [14, 4, 14], "size": [11, 20, 12], "category": "leg", "uv_group": "shin_column"},
            {"name": "hock_left", "origin": [14.5, 2, 12], "size": [10, 8, 9], "category": "leg", "uv_group": "hock_ankle"}
        ]
    },
    {
        "name": "leg_left_foot",
        "parent": "leg_left_shin",
        "pivot": [19, 4, 15],
        "cubes": [
            {"name": "foot_pad_left", "origin": [12.5, 0, 7], "size": [14, 5, 16], "category": "foot", "uv_group": "foot_pad"},
            {"name": "toe_outer_l", "origin": [21, 0, 2], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_outer_l", "origin": [21.5, 0, -3], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "toe_mid_l", "origin": [17, 0, 0], "size": [4.5, 4, 10], "category": "claw", "uv_group": "toe_mid"},
            {"name": "claw_mid_l", "origin": [17.5, 0, -6], "size": [3, 3, 6], "category": "claw", "uv_group": "claw_mid"},
            {"name": "toe_inner_l", "origin": [13, 0, 2], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_inner_l", "origin": [13.5, 0, -3], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "claw_rear_l", "origin": [17.5, 1, 22], "size": [3.5, 3, 5], "category": "claw", "uv_group": "claw_rear"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-18, 42, 18],
        "cubes": [
            {"name": "thigh_right", "origin": [-26, 20, 10], "size": [14, 24, 16], "category": "leg", "uv_group": "thigh_muscle"}
        ]
    },
    {
        "name": "leg_right_shin",
        "parent": "leg_right",
        "pivot": [-19, 22, 18],
        "cubes": [
            {"name": "shin_right", "origin": [-25, 4, 14], "size": [11, 20, 12], "category": "leg", "uv_group": "shin_column"},
            {"name": "hock_right", "origin": [-24.5, 2, 12], "size": [10, 8, 9], "category": "leg", "uv_group": "hock_ankle"}
        ]
    },
    {
        "name": "leg_right_foot",
        "parent": "leg_right_shin",
        "pivot": [-19, 4, 15],
        "cubes": [
            {"name": "foot_pad_right", "origin": [-26.5, 0, 7], "size": [14, 5, 16], "category": "foot", "uv_group": "foot_pad"},
            {"name": "toe_outer_r", "origin": [-25, 0, 2], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_outer_r", "origin": [-24, 0, -3], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "toe_mid_r", "origin": [-21.5, 0, 0], "size": [4.5, 4, 10], "category": "claw", "uv_group": "toe_mid"},
            {"name": "claw_mid_r", "origin": [-20.5, 0, -6], "size": [3, 3, 6], "category": "claw", "uv_group": "claw_mid"},
            {"name": "toe_inner_r", "origin": [-17, 0, 2], "size": [4, 4, 8], "category": "claw", "uv_group": "toe_side"},
            {"name": "claw_inner_r", "origin": [-16, 0, -3], "size": [2.5, 3, 5], "category": "claw", "uv_group": "claw_side"},
            {"name": "claw_rear_r", "origin": [-21, 1, 22], "size": [3.5, 3, 5], "category": "claw", "uv_group": "claw_rear"}
        ]
    },
    # -------------------------------------------------------------
    # 4-JOINT ARTICULATED WINGS (Anchored at muscular shoulders X = ±21)
    # Total wingspan: 284 units (~17.8 blocks)
    # -------------------------------------------------------------
    {
        "name": "wing_shoulder_left",
        "parent": "body",
        "pivot": [21, 48, -12],
        "cubes": [
            {"name": "shoulder_joint_l", "origin": [19, 45, -15], "size": [8, 6, 8], "category": "wing_arm", "uv_group": "wing_shoulder_joint"},
            {"name": "shoulder_guard_l", "origin": [18, 50, -16], "size": [10, 4, 8], "category": "spikes", "uv_group": "wing_shoulder_guard"}
        ]
    },
    {
        "name": "wing_arm_left",
        "parent": "wing_shoulder_left",
        "pivot": [27, 48, -12],
        "cubes": [
            {"name": "wing_arm_l", "origin": [27, 46, -14], "size": [26, 5, 5], "category": "wing_arm", "uv_group": "wing_bone_arm"},
            {"name": "wing_mem_inner_l", "origin": [26, 47, -9], "size": [26, 1, 39], "category": "wing_membrane", "uv_group": "wing_mem_inner"}
        ]
    },
    {
        "name": "wing_forearm_left",
        "parent": "wing_arm_left",
        "pivot": [53, 48, -11],
        "cubes": [
            {"name": "wing_forearm_l", "origin": [53, 46, -13], "size": [32, 5, 5], "category": "wing_arm", "uv_group": "wing_bone_arm"},
            {"name": "elbow_spur_l", "origin": [51, 47, -17], "size": [4, 5, 5], "category": "claw", "uv_group": "wing_elbow_spur"},
            {"name": "wrist_claw_l", "origin": [83, 46, -16], "size": [4, 4, 4], "category": "claw", "uv_group": "wing_wrist_claw"},
            {"name": "wing_mem_mid_l", "origin": [51, 47, -8], "size": [33, 1, 50], "category": "wing_membrane", "uv_group": "wing_mem_mid"}
        ]
    },
    {
        "name": "wing_fingers_left",
        "parent": "wing_forearm_left",
        "pivot": [85, 48, -10],
        "cubes": [
            {"name": "wing_finger1_l", "origin": [85, 47, -12], "size": [48, 3, 4], "category": "wing_arm", "uv_group": "wing_finger_main"},
            {"name": "wing_finger2_l", "origin": [85, 47, 12], "size": [40, 2.5, 3.5], "category": "wing_arm", "uv_group": "wing_finger_sub"},
            {"name": "wing_finger3_l", "origin": [85, 47, 28], "size": [34, 2.5, 3.5], "category": "wing_arm", "uv_group": "wing_finger_sub"},
            {"name": "wing_mem_outer_l", "origin": [83, 47, -8], "size": [48, 1, 52], "category": "wing_membrane", "uv_group": "wing_mem_outer"},
            {"name": "wing_mem_tip_l", "origin": [118, 47, 2], "size": [24, 1, 38], "category": "wing_membrane", "uv_group": "wing_mem_tip"}
        ]
    },
    {
        "name": "wing_shoulder_right",
        "parent": "body",
        "pivot": [-21, 48, -12],
        "cubes": [
            {"name": "shoulder_joint_r", "origin": [-27, 45, -15], "size": [8, 6, 8], "category": "wing_arm", "uv_group": "wing_shoulder_joint"},
            {"name": "shoulder_guard_r", "origin": [-28, 50, -16], "size": [10, 4, 8], "category": "spikes", "uv_group": "wing_shoulder_guard"}
        ]
    },
    {
        "name": "wing_arm_right",
        "parent": "wing_shoulder_right",
        "pivot": [-27, 48, -12],
        "cubes": [
            {"name": "wing_arm_r", "origin": [-53, 46, -14], "size": [26, 5, 5], "category": "wing_arm", "uv_group": "wing_bone_arm"},
            {"name": "wing_mem_inner_r", "origin": [-52, 47, -9], "size": [26, 1, 39], "category": "wing_membrane", "uv_group": "wing_mem_inner"}
        ]
    },
    {
        "name": "wing_forearm_right",
        "parent": "wing_arm_right",
        "pivot": [-53, 48, -11],
        "cubes": [
            {"name": "wing_forearm_r", "origin": [-85, 46, -13], "size": [32, 5, 5], "category": "wing_arm", "uv_group": "wing_bone_arm"},
            {"name": "elbow_spur_r", "origin": [-55, 47, -17], "size": [4, 5, 5], "category": "claw", "uv_group": "wing_elbow_spur"},
            {"name": "wrist_claw_r", "origin": [-87, 46, -16], "size": [4, 4, 4], "category": "claw", "uv_group": "wing_wrist_claw"},
            {"name": "wing_mem_mid_r", "origin": [-84, 47, -8], "size": [33, 1, 50], "category": "wing_membrane", "uv_group": "wing_mem_mid"}
        ]
    },
    {
        "name": "wing_fingers_right",
        "parent": "wing_forearm_right",
        "pivot": [-85, 48, -10],
        "cubes": [
            {"name": "wing_finger1_r", "origin": [-133, 47, -12], "size": [48, 3, 4], "category": "wing_arm", "uv_group": "wing_finger_main"},
            {"name": "wing_finger2_r", "origin": [-125, 47, 12], "size": [40, 2.5, 3.5], "category": "wing_arm", "uv_group": "wing_finger_sub"},
            {"name": "wing_finger3_r", "origin": [-119, 47, 28], "size": [34, 2.5, 3.5], "category": "wing_arm", "uv_group": "wing_finger_sub"},
            {"name": "wing_mem_outer_r", "origin": [-131, 47, -8], "size": [48, 1, 52], "category": "wing_membrane", "uv_group": "wing_mem_outer"},
            {"name": "wing_mem_tip_r", "origin": [-142, 47, 2], "size": [24, 1, 38], "category": "wing_membrane", "uv_group": "wing_mem_tip"}
        ]
    },
    # -------------------------------------------------------------
    # ORGANIC 7-STAGE ARTICULATED TAIL CHAIN (9 BONES TOTAL)
    # Tapers smoothly from pelvis (width 20) down to shaft (width 6),
    # ending in a colossal 37-unit wide glowing magma fan blade
    # -------------------------------------------------------------
    # Segment 1: Base connecting smoothly to pelvis
    {
        "name": "tail_1",
        "parent": "body",
        "pivot": [0, 42, 30],
        "cubes": [
            {"name": "tail_1_core", "origin": [-10, 34, 30], "size": [20, 16, 16], "category": "tail_core", "uv_group": "tail_1_core"},
            {"name": "tail_1_side_l", "origin": [10, 36, 31], "size": [4, 12, 14], "category": "tail_plate", "uv_group": "tail1_side_plate"},
            {"name": "tail_1_side_r", "origin": [-14, 36, 31], "size": [4, 12, 14], "category": "tail_plate", "uv_group": "tail1_side_plate"},
            {"name": "tail_1_spine", "origin": [-1.5, 50, 31], "size": [3, 6, 14], "category": "tail_spine", "uv_group": "tail_spine_upper"},
            {"name": "tail_1_keel", "origin": [-3, 31.5, 31], "size": [6, 2.5, 14], "category": "tail_keel", "uv_group": "tail_keel_base"}
        ]
    },
    # Segment 2: Upper tail with conical lateral spikes
    {
        "name": "tail_2",
        "parent": "tail_1",
        "pivot": [0, 41, 46],
        "cubes": [
            {"name": "tail_2_core", "origin": [-8, 34.5, 46], "size": [16, 14, 16], "category": "tail_core", "uv_group": "tail_2_core"},
            {"name": "tail_2_spike_l", "origin": [8, 38.5, 47], "size": [4, 3.5, 14], "category": "tail_spike", "uv_group": "tail_lateral_spike"},
            {"name": "tail_2_spike_r", "origin": [-12, 38.5, 47], "size": [4, 3.5, 14], "category": "tail_spike", "uv_group": "tail_lateral_spike"},
            {"name": "tail_2_spine", "origin": [-1.25, 48.5, 47], "size": [2.5, 6, 14], "category": "tail_spine", "uv_group": "tail_spine_upper"},
            {"name": "tail_2_keel", "origin": [-2.5, 32.5, 47], "size": [5, 2.5, 14], "category": "tail_keel", "uv_group": "tail_keel_base"}
        ]
    },
    # Segment 3: Mid tail with cutting obsidian lateral blades
    {
        "name": "tail_3",
        "parent": "tail_2",
        "pivot": [0, 40, 62],
        "cubes": [
            {"name": "tail_3_core", "origin": [-6.5, 34.5, 62], "size": [13, 12, 16], "category": "tail_core", "uv_group": "tail_mid_core"},
            {"name": "tail_3_blade_l", "origin": [6.5, 38, 63], "size": [4, 3.5, 14], "category": "tail_blade", "uv_group": "tail_lateral_spike"},
            {"name": "tail_3_blade_r", "origin": [-10.5, 38, 63], "size": [4, 3.5, 14], "category": "tail_blade", "uv_group": "tail_lateral_spike"},
            {"name": "tail_3_spine", "origin": [-1.1, 46.5, 63], "size": [2.2, 5, 14], "category": "tail_spine", "uv_group": "tail_spine_mid"},
            {"name": "tail_3_keel", "origin": [-2, 32.5, 63], "size": [4, 2.5, 14], "category": "tail_keel", "uv_group": "tail_keel_base"}
        ]
    },
    # Segment 4: Tapered mid-rear tail with stabilizing fins
    {
        "name": "tail_4",
        "parent": "tail_3",
        "pivot": [0, 39, 78],
        "cubes": [
            {"name": "tail_4_core", "origin": [-5, 34.5, 78], "size": [10, 10, 16], "category": "tail_core", "uv_group": "tail_mid_core"},
            {"name": "tail_4_fin_l", "origin": [5, 37.5, 79], "size": [4.5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_4_fin_r", "origin": [-9.5, 37.5, 79], "size": [4.5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_4_spine", "origin": [-1.1, 44.5, 79], "size": [2.2, 5, 14], "category": "tail_spine", "uv_group": "tail_spine_mid"}
        ]
    },
    # Segment 5: Pre-fan tapered segment expanding horizontal wings
    {
        "name": "tail_5",
        "parent": "tail_4",
        "pivot": [0, 38, 94],
        "cubes": [
            {"name": "tail_5_core", "origin": [-4, 34.5, 94], "size": [8, 8, 16], "category": "tail_core", "uv_group": "tail_rear_core"},
            {"name": "tail_5_fin_l", "origin": [4, 37, 95], "size": [5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_5_fin_r", "origin": [-9, 37, 95], "size": [5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_5_spine", "origin": [-0.75, 42.5, 95], "size": [1.5, 4, 14], "category": "tail_spine", "uv_group": "tail_spine_lower"}
        ]
    },
    # Segment 6: Base anchor shaft for the caudal fan
    {
        "name": "tail_6",
        "parent": "tail_5",
        "pivot": [0, 37, 110],
        "cubes": [
            {"name": "tail_6_core", "origin": [-3, 34.5, 110], "size": [6, 6.5, 16], "category": "tail_core", "uv_group": "tail_rear_core"},
            {"name": "tail_6_fin_l", "origin": [3, 36.5, 111], "size": [5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_6_fin_r", "origin": [-8, 36.5, 111], "size": [5, 2, 14], "category": "tail_fin", "uv_group": "tail_lateral_fin"},
            {"name": "tail_6_spine", "origin": [-0.75, 41, 111], "size": [1.5, 3.5, 14], "category": "tail_spine", "uv_group": "tail_spine_lower"}
        ]
    },
    # Segment 7: COLOSSAL CAUDAL BLADE & MAGMA FAN (Width: 37 units)
    {
        "name": "tail_flame",
        "parent": "tail_6",
        "pivot": [0, 37, 126],
        "cubes": [
            {"name": "fan_spine_core", "origin": [-2, 35, 126], "size": [4, 4, 26], "category": "flame_core", "uv_group": "fan_spine_core"},
            {"name": "fan_spear_tip", "origin": [-1, 36, 152], "size": [2, 2, 10], "category": "spikes", "uv_group": "fan_spear_tip"},
            {"name": "fan_keel_dorsal", "origin": [-1, 39, 127], "size": [2, 5.5, 24], "category": "flame_keel", "uv_group": "fan_keel"},
            {"name": "fan_keel_ventral", "origin": [-1, 30.5, 128], "size": [2, 5.5, 24], "category": "flame_keel", "uv_group": "fan_keel"}
        ]
    },
    # Articulated Left Flame Wing (X extends to +18.5)
    {
        "name": "tail_flame_left",
        "parent": "tail_flame",
        "pivot": [2, 37, 127],
        "cubes": [
            {"name": "fan_blade_inner_l", "origin": [2, 36.2, 127], "size": [7, 1.6, 24], "category": "flame_blade_inner", "uv_group": "fan_blade_inner"},
            {"name": "fan_blade_mid_l", "origin": [9, 36.3, 129], "size": [4.5, 1.2, 18], "category": "flame_blade_mid", "uv_group": "fan_blade_outer_group"},
            {"name": "fan_blade_outer_l", "origin": [13.5, 36.4, 131], "size": [4.5, 1.2, 18], "category": "flame_blade_outer", "uv_group": "fan_blade_outer_group"},
            {"name": "fan_spike_front_l", "origin": [12.5, 36.8, 127], "size": [3, 2, 8], "category": "flame_spike", "uv_group": "fan_spike_front"},
            {"name": "fan_flare_rear_l", "origin": [1, 36.5, 149], "size": [6, 1.0, 16], "category": "flame_flare", "uv_group": "fan_flare_rear"},
            {"name": "fan_crust_tip_l", "origin": [16, 36, 135], "size": [2.5, 2.5, 6], "category": "basalt_crust", "uv_group": "fan_crust_tip"}
        ]
    },
    # Articulated Right Flame Wing (X extends to -18.5)
    {
        "name": "tail_flame_right",
        "parent": "tail_flame",
        "pivot": [-2, 37, 127],
        "cubes": [
            {"name": "fan_blade_inner_r", "origin": [-9, 36.2, 127], "size": [7, 1.6, 24], "category": "flame_blade_inner", "uv_group": "fan_blade_inner"},
            {"name": "fan_blade_mid_r", "origin": [-13.5, 36.3, 129], "size": [4.5, 1.2, 18], "category": "flame_blade_mid", "uv_group": "fan_blade_outer_group"},
            {"name": "fan_blade_outer_r", "origin": [-18, 36.4, 131], "size": [4.5, 1.2, 18], "category": "flame_blade_outer", "uv_group": "fan_blade_outer_group"},
            {"name": "fan_spike_front_r", "origin": [-15.5, 36.8, 127], "size": [3, 2, 8], "category": "flame_spike", "uv_group": "fan_spike_front"},
            {"name": "fan_flare_rear_r", "origin": [-7, 36.5, 149], "size": [6, 1.0, 16], "category": "flame_flare", "uv_group": "fan_flare_rear"},
            {"name": "fan_crust_tip_r", "origin": [-18.5, 36, 135], "size": [2.5, 2.5, 6], "category": "basalt_crust", "uv_group": "fan_crust_tip"}
        ]
    }
]

# ---------------------------------------------------------------------------
# Texture Painter — ULTRA-HD 512x512 THERMAL VOLCANIC PALETTE
# ---------------------------------------------------------------------------
def paint_adult_texture(tex, bones_def, tex_w, tex_h):
    CORE_WHITE       = (255, 255, 230, 255) # Supercritical white core
    PLASMA_YELLOW    = (255, 238, 51, 255)  # #FFEE33 pure magma
    MAGMA_GOLD       = (255, 170, 0, 255)   # #FFAA00 active radiant magma
    FIRE_ORANGE      = (255, 68, 0, 255)    # #FF4400 surging flame
    CRIMSON_LAVA     = (185, 28, 16, 255)   # Deep volcanic crimson
    CHAR_EMBER       = (98, 20, 16, 255)    # Cooling embers
    BASALT_CRUST     = (46, 36, 40, 255)    # Cooled volcanic crust
    OBSIDIAN_BASE    = (22, 20, 26, 255)    # Deep glossy obsidian
    OBSIDIAN_SCALE   = (34, 31, 40, 255)    # Armor scale body
    OBSIDIAN_BEVEL   = (58, 54, 70, 255)    # Scale bevel highlight
    OBSIDIAN_SHADOW  = (14, 12, 17, 255)    # Scale shadow
    HORN_DARK        = (38, 32, 28, 255)
    HORN_MID         = (75, 62, 50, 255)
    HORN_LIGHT       = (120, 102, 85, 255)
    MEMBRANE_CRIMSON = (178, 26, 22, 255)   # Vibrant dragon crimson
    MEMBRANE_SCARLET = (220, 48, 24, 255)   # Radiant glowing scarlet
    MEMBRANE_EMBER   = (250, 102, 28, 255)  # Fiery warm membrane highlight
    MEMBRANE_SHADOW  = (118, 18, 16, 255)   # Deep red leathery shadow
    MEMBRANE_RIB     = (76, 14, 12, 255)    # Structural fold
    EYE_GOLD         = (255, 205, 15, 255)
    EYE_PUPIL        = (12, 8, 8, 255)
    FANG_COLOR       = (232, 224, 202, 255)

    for b in bones_def:
        for c in b.get("cubes", []):
            u0, v0 = c["uv"]
            sx, sy, sz = c["size"]
            cat = c["category"]

            faces = [
                ("up", u0 + sz, v0, sx, sz),
                ("down", u0 + sz + sx, v0, sx, sz),
                ("west", u0, v0 + sz, sz, sy),
                ("north", u0 + sz, v0 + sz, sx, sy),
                ("east", u0 + sz + sx, v0 + sz, sz, sy),
                ("south", u0 + 2*sz + sx, v0 + sz, sx, sy)
            ]

            for fname, fu, fv, fw, fh in faces:
                fw_int = int(math.ceil(fw))
                fh_int = int(math.ceil(fh))

                for py in range(int(fv), int(fv + fh)):
                    local_y = py - int(fv)
                    t_y = local_y / max(1, fh_int - 1)

                    for px in range(int(fu), int(fu + fw)):
                        local_x = px - int(fu)
                        t_x = local_x / max(1, fw_int - 1)

                        n = noise(px, py, 10)

                        # 1. Torso, Keel, Belly, Hips, Legs & Tail Core
                        if cat in ("torso_chest", "torso_mid", "torso_belly", "torso_hips", "torso_back", "tail_core", "leg", "foot"):
                            sw, sh = 5, 4
                            row = local_y // sh
                            shift = (sw // 2) if (row % 2 == 1) else 0
                            cu = (local_x + shift) % sw
                            cv = local_y % sh

                            if cv == 0 or (cu == 0 and cv <= 1):
                                base_c = OBSIDIAN_BEVEL
                            elif cv == sh - 1 or cu == sw - 1:
                                base_c = OBSIDIAN_SHADOW
                            else:
                                base_c = OBSIDIAN_SCALE

                            # Sinuous radiant magma veins
                            if fname == "down" or (cat in ("torso_chest", "torso_belly") and fname in ("west", "east") and t_y > 0.6):
                                vein_center = fw_int / 2.0 + 1.8 * math.sin(local_y * 0.6)
                                d_vein = abs(local_x - vein_center)
                                if d_vein < 1.2:
                                    base_c = PLASMA_YELLOW
                                elif d_vein < 2.5:
                                    base_c = MAGMA_GOLD
                                elif d_vein < 4.0:
                                    base_c = FIRE_ORANGE
                                elif d_vein < 5.5:
                                    base_c = CRIMSON_LAVA
                            elif fname == "up" and cat in ("tail_core", "torso_mid"):
                                seam_center = fw_int / 2.0
                                d_seam = abs(local_x - seam_center)
                                if d_seam < 1.4:
                                    base_c = MAGMA_GOLD
                                elif d_seam < 2.8:
                                    base_c = FIRE_ORANGE

                        # 2. Chest Armor Plates
                        elif cat == "chest_armor":
                            d_mid = abs(local_x - fw_int / 2.0)
                            if d_mid < 1.8:
                                base_c = PLASMA_YELLOW
                            elif d_mid < 3.5:
                                base_c = MAGMA_GOLD
                            elif d_mid < 5.5:
                                base_c = FIRE_ORANGE
                            else:
                                base_c = OBSIDIAN_BASE

                        # 3. Tail Plates, Spikes, Blades & Fins
                        elif cat in ("tail_plate", "tail_spike", "tail_blade", "tail_fin"):
                            rel_edge = local_x / max(1, fw_int - 1)
                            if local_y == 0 or local_y == fh_int - 1:
                                base_c = OBSIDIAN_SHADOW
                            elif rel_edge > 0.8:
                                base_c = OBSIDIAN_BEVEL
                            elif rel_edge < 0.25:
                                base_c = MAGMA_GOLD if (local_x + local_y) % 3 != 0 else FIRE_ORANGE
                            else:
                                base_c = OBSIDIAN_SCALE

                        # 4. Spines & Keels
                        elif cat in ("tail_spine", "tail_keel", "flame_keel"):
                            if cat in ("tail_keel", "flame_keel"):
                                if t_y < 0.35:
                                    base_c = PLASMA_YELLOW
                                elif t_y < 0.7:
                                    base_c = FIRE_ORANGE
                                else:
                                    base_c = CRIMSON_LAVA
                            else:
                                if fname in ("west", "east") and t_y > 0.65:
                                    base_c = MAGMA_GOLD
                                elif fname == "up":
                                    base_c = OBSIDIAN_BEVEL
                                else:
                                    base_c = OBSIDIAN_SCALE

                        # 5. Caudal Magma Fan & Blades
                        elif cat in ("flame_core", "flame_blade_inner", "flame_blade_mid", "flame_blade_outer", "flame_flare", "flame_spike", "basalt_crust"):
                            if cat == "flame_core":
                                if fname in ("up", "down"):
                                    d_c = abs(local_x - fw_int / 2.0)
                                    base_c = CORE_WHITE if d_c < 1.0 else PLASMA_YELLOW
                                else:
                                    base_c = PLASMA_YELLOW if t_y < 0.5 else MAGMA_GOLD

                            elif cat == "flame_blade_inner":
                                heat = 1.0 - (0.45 * t_y + 0.35 * t_x) + 0.08 * math.sin(local_x * 0.9 + local_y * 0.6)
                                if heat > 0.75:
                                    base_c = PLASMA_YELLOW
                                elif heat > 0.5:
                                    base_c = MAGMA_GOLD
                                else:
                                    base_c = FIRE_ORANGE

                            elif cat in ("flame_blade_mid", "flame_blade_outer"):
                                heat = 0.80 - (0.48 * t_y + 0.38 * t_x) + 0.06 * math.sin(local_x * 0.8 + local_y * 0.5)
                                if heat > 0.55:
                                    base_c = MAGMA_GOLD
                                elif heat > 0.35:
                                    base_c = FIRE_ORANGE
                                elif heat > 0.20:
                                    base_c = CRIMSON_LAVA
                                else:
                                    base_c = CHAR_EMBER

                            elif cat == "flame_flare":
                                stream = 0.5 + 0.4 * math.sin(local_y * 0.8 + local_x * 1.2)
                                heat = (1.0 - t_y * 0.7) * 0.7 + stream * 0.3
                                if heat > 0.65:
                                    base_c = PLASMA_YELLOW
                                elif heat > 0.45:
                                    base_c = FIRE_ORANGE
                                elif heat > 0.25:
                                    base_c = CRIMSON_LAVA
                                else:
                                    base_c = CHAR_EMBER

                            elif cat == "flame_spike":
                                if t_y < 0.3:
                                    base_c = FIRE_ORANGE
                                elif t_y < 0.6:
                                    base_c = CRIMSON_LAVA
                                else:
                                    base_c = OBSIDIAN_BASE

                            elif cat == "basalt_crust":
                                base_c = CHAR_EMBER if (local_x + local_y) % 4 == 0 else BASALT_CRUST

                        # 6. Head, Snout, Jaw, Horns & Wings
                        elif cat == "neck":
                            base_c = MAGMA_GOLD if (fname == "down" and abs(local_x - fw_int/2.0) < 2.5) else OBSIDIAN_SCALE
                        elif cat == "head":
                            base_c = OBSIDIAN_SCALE
                        elif cat == "snout":
                            base_c = OBSIDIAN_BASE
                        elif cat == "jaw":
                            base_c = MAGMA_GOLD if (fname == "down" and local_y < fh_int * 0.4) else OBSIDIAN_BASE
                        elif cat == "horn":
                            rel = (px - fu) / max(1, fw_int)
                            base_c = HORN_LIGHT if rel > 0.6 else (HORN_MID if rel > 0.3 else HORN_DARK)
                        elif cat == "spikes":
                            base_c = HORN_DARK if fname != "up" else OBSIDIAN_BEVEL
                        elif cat == "claw":
                            base_c = HORN_DARK if t_y > 0.5 else HORN_MID
                        elif cat == "wing_arm":
                            base_c = OBSIDIAN_BASE if fname != "up" else OBSIDIAN_SCALE
                        elif cat == "wing_membrane":
                            fold = math.sin(local_x * 0.4 + local_y * 0.25)
                            vein = math.sin(local_x * 0.85 - local_y * 0.5)
                            if fold < -0.6:
                                base_c = MEMBRANE_RIB
                            elif vein > 0.75:
                                base_c = MEMBRANE_EMBER
                            elif fold > 0.3:
                                base_c = MEMBRANE_SCARLET
                            elif fold > -0.2:
                                base_c = MEMBRANE_CRIMSON
                            else:
                                base_c = MEMBRANE_SHADOW
                        else:
                            base_c = OBSIDIAN_SCALE

                        col = shade(base_c, n)
                        if 0 <= px < tex_w and 0 <= py < tex_h:
                            tex.putpixel((px, py), col)

            # Glowing dragon eyes & fangs on cranium and jaw
            if c["name"] == "cranium":
                fu_w, fv_w = int(u0), int(v0 + sz)
                fu_e, fv_e = int(u0 + sz + sx), int(v0 + sz)
                for ex in range(4, 9):
                    for ey in range(3, 8):
                        if 0 <= fu_w + ex < tex_w and 0 <= fv_w + ey < tex_h:
                            tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        if 0 <= fu_e + int(sz) - 1 - ex < tex_w and 0 <= fv_e + ey < tex_h:
                            tex.putpixel((fu_e + int(sz) - 1 - ex, fv_e + ey), EYE_GOLD)
                for ey in range(3, 8):
                    if 0 <= fu_w + 7 < tex_w and 0 <= fv_w + ey < tex_h:
                        tex.putpixel((fu_w + 7, fv_w + ey), EYE_PUPIL)
                    if 0 <= fu_e + int(sz) - 1 - 7 < tex_w and 0 <= fv_e + ey < tex_h:
                        tex.putpixel((fu_e + int(sz) - 1 - 7, fv_e + ey), EYE_PUPIL)
            elif c["name"] == "jaw":
                fu_n, fv_n = int(u0 + sz), int(v0 + sz)
                for fx in [2, 4, int(sx) - 5, int(sx) - 3]:
                    if 0 <= fu_n + fx < tex_w and 0 <= fv_n < tex_h:
                        tex.putpixel((fu_n + fx, fv_n), FANG_COLOR)

# ---------------------------------------------------------------------------
# 5 ADVANCED ANIMATIONS (ADAPTED TO HARMONIC QUADRUPEDAL STANCE)
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

adult_anims = {
    # 1. NOBLE QUADRUPEDAL IDLE (Harmonic stance, deep predatory breathing)
    "animation.flamefang_adult.idle": {
        "loop": True,
        "animation_length": 4.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "2.25": [0, -0.6, 0], "4.5": [0, 0, 0]}
            },
            "neck": {"rotation": {"0.0": [0, 0, 0], "2.25": [2.5, 0, 0], "4.5": [0, 0, 0]}},
            "neck_upper": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.0, 0, 0], "4.5": [0, 0, 0]}},
            "leg_front_left": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.0, 0, 0], "4.5": [0, 0, 0]}},
            "leg_front_right": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.0, 0, 0], "4.5": [0, 0, 0]}},
            "leg_left": {"rotation": {"0.0": [0, 0, 0], "2.25": [1.0, 0, 0], "4.5": [0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [0, 0, 0], "2.25": [1.0, 0, 0], "4.5": [0, 0, 0]}},
            "wing_shoulder_left": {"rotation": {"0.0": [0, 0, -2.0], "2.25": [0, 0, 0], "4.5": [0, 0, -2.0]}},
            "wing_arm_left": {"rotation": {"0.0": [0, 0, -4.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -4.0]}},
            "wing_forearm_left": {"rotation": {"0.0": [0, 0, 3.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 3.0]}},
            "wing_fingers_left": {"rotation": {"0.0": [0, 0, -2.0], "2.25": [0, 0, 0], "4.5": [0, 0, -2.0]}},
            "wing_shoulder_right": {"rotation": {"0.0": [0, 0, 2.0], "2.25": [0, 0, 0], "4.5": [0, 0, 2.0]}},
            "wing_arm_right": {"rotation": {"0.0": [0, 0, 4.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 4.0]}},
            "wing_forearm_right": {"rotation": {"0.0": [0, 0, -3.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -3.0]}},
            "wing_fingers_right": {"rotation": {"0.0": [0, 0, 2.0], "2.25": [0, 0, 0], "4.5": [0, 0, 2.0]}},
            "tail_1": {"rotation": {"0.0": [0, -2.0, 0], "2.25": [0, 2.0, 0], "4.5": [0, -2.0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, -3.5, 0], "2.25": [0, 3.5, 0], "4.5": [0, -3.5, 0]}},
            "tail_3": {"rotation": {"0.0": [0, -5.5, 0], "2.25": [0, 5.5, 0], "4.5": [0, -5.5, 0]}},
            "tail_4": {"rotation": {"0.0": [0, -8.0, 0], "2.25": [0, 8.0, 0], "4.5": [0, -8.0, 0]}},
            "tail_5": {"rotation": {"0.0": [0, -11.0, 0], "2.25": [0, 11.0, 0], "4.5": [0, -11.0, 0]}},
            "tail_6": {"rotation": {"0.0": [0, -14.0, 0], "2.25": [0, 14.0, 0], "4.5": [0, -14.0, 0]}},
            "tail_flame": {
                "rotation": {"0.0": [0, -18.0, -5.0], "1.12": [3.0, 0.0, 0], "2.25": [0, 18.0, 5.0], "3.38": [-3.0, 0.0, 0], "4.5": [0, -18.0, -5.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.12": [1.12, 1.15, 1.12], "2.25": [0.95, 0.92, 0.95], "3.38": [1.14, 1.18, 1.14], "4.5": [1.0, 1.0, 1.0]}
            },
            "tail_flame_left": {
                "rotation": {"0.0": [0, 0, -4.0], "2.25": [0, 0, 4.0], "4.5": [0, 0, -4.0]}
            },
            "tail_flame_right": {
                "rotation": {"0.0": [0, 0, 4.0], "2.25": [0, 0, -4.0], "4.5": [0, 0, 4.0]}
            }
        }
    },
    # 2. REALISTIC QUADRUPEDAL GAIT (Balanced trot/walk)
    "animation.flamefang_adult.walk": {
        "loop": True,
        "animation_length": 2.0,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.5": [0, 0.8, 0], "1.0": [0, 0, 0], "1.5": [0, 0.8, 0], "2.0": [0, 0, 0]}},
            "body": {
                "rotation": {
                    "0.0": [2.0, 1.5, -2.5],
                    "0.5": [0.5, 0.0, 0.0],
                    "1.0": [2.0, -1.5, 2.5],
                    "1.5": [0.5, 0.0, 0.0],
                    "2.0": [2.0, 1.5, -2.5]
                }
            },
            "leg_front_left": {
                "rotation": {
                    "0.0": [20.0, 0, 0],
                    "0.5": [-10.0, 0, 0],
                    "1.0": [-20.0, 0, 0],
                    "1.5": [0.0, 0, 0],
                    "2.0": [20.0, 0, 0]
                }
            },
            "leg_front_left_shin": {
                "rotation": {
                    "0.0": [5.0, 0, 0],
                    "0.5": [-20.0, 0, 0],
                    "1.0": [5.0, 0, 0],
                    "1.5": [0.0, 0, 0],
                    "2.0": [5.0, 0, 0]
                }
            },
            "leg_right": {
                "rotation": {
                    "0.0": [22.0, 0, 0],
                    "0.5": [-10.0, 0, 0],
                    "1.0": [-22.0, 0, 0],
                    "1.5": [0.0, 0, 0],
                    "2.0": [22.0, 0, 0]
                }
            },
            "leg_right_shin": {
                "rotation": {
                    "0.0": [5.0, 0, 0],
                    "0.5": [-18.0, 0, 0],
                    "1.0": [10.0, 0, 0],
                    "1.5": [0.0, 0, 0],
                    "2.0": [5.0, 0, 0]
                }
            },
            "leg_front_right": {
                "rotation": {
                    "0.0": [-20.0, 0, 0],
                    "0.5": [0.0, 0, 0],
                    "1.0": [20.0, 0, 0],
                    "1.5": [-10.0, 0, 0],
                    "2.0": [-20.0, 0, 0]
                }
            },
            "leg_front_right_shin": {
                "rotation": {
                    "0.0": [5.0, 0, 0],
                    "0.5": [0.0, 0, 0],
                    "1.0": [5.0, 0, 0],
                    "1.5": [-20.0, 0, 0],
                    "2.0": [5.0, 0, 0]
                }
            },
            "leg_left": {
                "rotation": {
                    "0.0": [-22.0, 0, 0],
                    "0.5": [0.0, 0, 0],
                    "1.0": [22.0, 0, 0],
                    "1.5": [-10.0, 0, 0],
                    "2.0": [-22.0, 0, 0]
                }
            },
            "leg_left_shin": {
                "rotation": {
                    "0.0": [10.0, 0, 0],
                    "0.5": [0.0, 0, 0],
                    "1.0": [5.0, 0, 0],
                    "1.5": [-18.0, 0, 0],
                    "2.0": [10.0, 0, 0]
                }
            },
            "tail_1": {"rotation": {"0.0": [0, 4.0, 0], "1.0": [0, -4.0, 0], "2.0": [0, 4.0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, 7.0, 0], "1.0": [0, -7.0, 0], "2.0": [0, 7.0, 0]}},
            "tail_3": {"rotation": {"0.0": [0, 11.0, 0], "1.0": [0, -11.0, 0], "2.0": [0, 11.0, 0]}},
            "tail_4": {"rotation": {"0.0": [0, 15.0, 0], "1.0": [0, -15.0, 0], "2.0": [0, 15.0, 0]}},
            "tail_5": {"rotation": {"0.0": [0, 19.0, 0], "1.0": [0, -19.0, 0], "2.0": [0, 19.0, 0]}},
            "tail_6": {"rotation": {"0.0": [0, 23.0, 0], "1.0": [0, -23.0, 0], "2.0": [0, 23.0, 0]}},
            "tail_flame": {"rotation": {"0.0": [0, 27.0, 0], "1.0": [0, -27.0, 0], "2.0": [0, 27.0, 0]}},
            "tail_flame_left": {"rotation": {"0.0": [0, 3.0, -3.0], "1.0": [0, -3.0, 3.0], "2.0": [0, 3.0, -3.0]}},
            "tail_flame_right": {"rotation": {"0.0": [0, 3.0, 3.0], "1.0": [0, -3.0, -3.0], "2.0": [0, 3.0, 3.0]}}
        }
    },
    # 3. ULTRA-FLUID DENSE FLIGHT (APPROVED 37-KEYFRAME SINE PHYSICS)
        # 3. ULTRA-FLUID DENSE FLIGHT (APPROVED 43-KEYFRAME ASYMMETRIC FLIGHT PHYSICS)
    "animation.flamefang_adult.fly_flap": generate_adult_fly_flap(duration=1.4, frames=43),
    # 4. GLIDE (GENTLE THERMAL UPDRAFT HOVERING)
    "animation.flamefang_adult.glide": generate_adult_glide(duration=4.0, frames=41),
    # 5. EATING (RHYTHMIC MASTICATION & SWALLOWING)
    "animation.flamefang_adult.eating": generate_adult_eating(),
    # 6. SLEEP (NESTED DEEP SLUMBER & SLOW BREATHING)
    "animation.flamefang_adult.sleep": generate_adult_sleep(),
    # 7. WAKE UP (YAWN, STRETCH & ALERT POSTURE)
    "animation.flamefang_adult.wake_up": generate_adult_wake_up(),
    # 8. ROAR (INTIMIDATING TITANIC ROAR & 284 WINGSPAN DISPLAY)
    "animation.flamefang_adult.roar": generate_adult_roar(),
    # 4. COMBAT 1: VICIOUS BITE ATTACK
    "animation.flamefang_adult.attack_bite": {
        "loop": False,
        "animation_length": 1.4,
        "bones": {
            "body": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [-3.0, 0, 0], "0.7": [4.0, 0, 0], "1.1": [1.0, 0, 0], "1.4": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "0.3": [0, 0, 2.0], "0.7": [0, 0, -4.0], "1.1": [0, 0, -1.0], "1.4": [0, 0, 0]}
            },
            "neck": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [-18.0, 0, 0], "0.7": [24.0, 0, 0], "1.1": [5.0, 0, 0], "1.4": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "0.3": [0, 1.0, 2.0], "0.7": [0, -2.0, -8.0], "1.1": [0, 0, -2.0], "1.4": [0, 0, 0]}
            },
            "head": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [-10.0, 0, 0], "0.7": [15.0, 0, 0], "1.1": [2.0, 0, 0], "1.4": [0, 0, 0]}
            },
            "jaw_lower": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [20.0, 0, 0], "0.55": [50.0, 0, 0], "0.7": [-5.0, 0, 0], "0.9": [0, 0, 0], "1.4": [0, 0, 0]}
            },
            "leg_front_left": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [-12.0, 0, 2.0], "0.7": [15.0, 0, 3.0], "1.1": [4.0, 0, 1.0], "1.4": [0, 0, 0]}
            },
            "leg_front_right": {
                "rotation": {"0.0": [0, 0, 0], "0.3": [-12.0, 0, -2.0], "0.7": [15.0, 0, -3.0], "1.1": [4.0, 0, -1.0], "1.4": [0, 0, 0]}
            },
            "tail_1": {"rotation": {"0.0": [0, 0, 0], "0.3": [5.0, 0, 0], "0.7": [-8.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, 0, 0], "0.3": [8.0, 0, 0], "0.7": [-12.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_3": {"rotation": {"0.0": [0, 0, 0], "0.3": [10.0, 0, 0], "0.7": [-16.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_4": {"rotation": {"0.0": [0, 0, 0], "0.3": [12.0, 0, 0], "0.7": [-18.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_5": {"rotation": {"0.0": [0, 0, 0], "0.3": [14.0, 0, 0], "0.7": [-20.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_6": {"rotation": {"0.0": [0, 0, 0], "0.3": [16.0, 0, 0], "0.7": [-22.0, 0, 0], "1.4": [0, 0, 0]}},
            "tail_flame": {"rotation": {"0.0": [0, 0, 0], "0.3": [20.0, 0, 0], "0.7": [-25.0, 0, 0], "1.4": [0, 0, 0]}}
        }
    },
    # 5. COMBAT 2: DEEP INHALE & DEVASTATING FIREBALL BLAST
    "animation.flamefang_adult.attack_fireball": {
        "loop": False,
        "animation_length": 1.8,
        "bones": {
            "body": {
                "scale": {"0.0": [1.0, 1.0, 1.0], "0.5": [1.08, 1.12, 1.08], "0.8": [1.10, 1.15, 1.10], "1.0": [1.0, 1.0, 1.0], "1.8": [1.0, 1.0, 1.0]},
                "rotation": {"0.0": [0, 0, 0], "0.6": [-12.0, 0, 0], "1.0": [6.0, 0, 0], "1.3": [-4.0, 0, 0], "1.8": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "0.6": [0, 1.0, 2.0], "1.0": [0, 0, 4.5], "1.4": [0, 0, 1.5], "1.8": [0, 0, 0]}
            },
            "neck": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [-25.0, 0, 0], "1.0": [30.0, 0, 0], "1.4": [5.0, 0, 0], "1.8": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "0.6": [0, 2.0, 2.0], "1.0": [0, -2.0, -10.0], "1.4": [0, 0, -2.0], "1.8": [0, 0, 0]}
            },
            "head": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [-15.0, 0, 0], "1.0": [20.0, 0, 0], "1.4": [5.0, 0, 0], "1.8": [0, 0, 0]}
            },
            "jaw_lower": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [35.0, 0, 0], "0.85": [55.0, 0, 0], "1.1": [25.0, 0, 0], "1.5": [5.0, 0, 0], "1.8": [0, 0, 0]}
            },
            "leg_front_left": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [-18.0, 0, 4.0], "1.0": [16.0, 0, 5.0], "1.4": [-4.0, 0, 1.0], "1.8": [0, 0, 0]}
            },
            "leg_front_right": {
                "rotation": {"0.0": [0, 0, 0], "0.6": [-18.0, 0, -4.0], "1.0": [16.0, 0, -5.0], "1.4": [-4.0, 0, -1.0], "1.8": [0, 0, 0]}
            },
            "wing_shoulder_left": {"rotation": {"0.0": [0, 0, 0], "0.6": [-15.0, 0, -10.0], "1.0": [20.0, 0, 25.0], "1.8": [0, 0, 0]}},
            "wing_shoulder_right": {"rotation": {"0.0": [0, 0, 0], "0.6": [-15.0, 0, 10.0], "1.0": [20.0, 0, -25.0], "1.8": [0, 0, 0]}},
            "tail_1": {"rotation": {"0.0": [0, 0, 0], "0.6": [-8.0, 0, 0], "1.0": [10.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, 0, 0], "0.6": [-12.0, 0, 0], "1.0": [15.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_3": {"rotation": {"0.0": [0, 0, 0], "0.6": [-15.0, 0, 0], "1.0": [18.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_4": {"rotation": {"0.0": [0, 0, 0], "0.6": [-18.0, 0, 0], "1.0": [22.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_5": {"rotation": {"0.0": [0, 0, 0], "0.6": [-20.0, 0, 0], "1.0": [25.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_6": {"rotation": {"0.0": [0, 0, 0], "0.6": [-22.0, 0, 0], "1.0": [28.0, 0, 0], "1.8": [0, 0, 0]}},
            "tail_flame": {
                "scale": {"0.0": [1.0, 1.0, 1.0], "0.6": [1.4, 1.4, 1.4], "0.85": [1.9, 2.1, 1.9], "1.1": [1.3, 1.3, 1.3], "1.8": [1.0, 1.0, 1.0]},
                "rotation": {"0.0": [0, 0, 0], "0.6": [-25.0, 0, 0], "1.0": [32.0, 0, 0], "1.8": [0, 0, 0]}
            },
            "tail_flame_left": {
                "rotation": {"0.0": [0, 0, -12.0], "0.85": [0, 0, -18.0], "1.8": [0, 0, 0]}
            },
            "tail_flame_right": {
                "rotation": {"0.0": [0, 0, 12.0], "0.85": [0, 0, 18.0], "1.8": [0, 0, 0]}
            }
        }
    }
}

# ---------------------------------------------------------------------------
# Blockbench & GeckoLib Exporter
# ---------------------------------------------------------------------------
def export_updated_adult():
    model_name = "flamefang_adult"
    bbmodel_filename = "flamefang_adult_geckolib.bbmodel"
    tex_w, tex_h = 512, 512

    print(f"\n==========================================")
    print(f"Exporting HARMONIC 3D ADULT FLAMEFANG: {model_name} ({tex_w}x{tex_h})")
    print(f"Torso: 36-42 width, 26-28 height (Width/Height ratio ~1.4 - NON-FLATTENED)")
    print(f"Height: 88 units (5.5 blocks). Stance: 4 legs planted at Y=0 (X=±20/±18)")
    print(f"Wings: 4 joints, 284 wingspan. Tail: 7 stages, 37 fan width")
    print(f"==========================================")

    # 1. Gather cubes and pack UVs
    all_cubes = []
    for b in adult_bones:
        for c in b.get("cubes", []):
            all_cubes.append(c)

    pack_uvs(all_cubes, tex_w, tex_h, padding=2)

    # 2. Paint Texture
    tex_img = Image.new("RGBA", (tex_w, tex_h), (0, 0, 0, 0))
    paint_adult_texture(tex_img, adult_bones, tex_w, tex_h)

    tex_path = os.path.join(TEX_DIR, f"{model_name}.png")
    tex_img.save(tex_path)
    print(f"Saved texture: {tex_path}")

    # 3. Export GeckoLib Geo JSON
    geo_data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": f"geometry.{model_name}",
                    "texture_width": tex_w,
                    "texture_height": tex_h,
                    "visible_bounds_width": 20,
                    "visible_bounds_height": 12,
                    "visible_bounds_offset": [0, 4, 0]
                },
                "bones": []
            }
        ]
    }

    for b in adult_bones:
        bone_entry = {
            "name": b["name"],
            "pivot": b["pivot"]
        }
        if "parent" in b:
            bone_entry["parent"] = b["parent"]
        if b.get("cubes"):
            bone_entry["cubes"] = []
            for c in b["cubes"]:
                cube_obj = {
                    "origin": c["origin"],
                    "size": c["size"],
                    "uv": c["uv"]
                }
                bone_entry["cubes"].append(cube_obj)
        geo_data["minecraft:geometry"][0]["bones"].append(bone_entry)

    geo_path = os.path.join(GEO_DIR, f"{model_name}.geo.json")
    with open(geo_path, "w", encoding="utf-8") as f:
        json.dump(geo_data, f, indent=2)
    print(f"Saved geo JSON: {geo_path}")

    # 4. Export GeckoLib Animation JSON
    anim_data = {
        "format_version": "1.8.0",
        "animations": adult_anims
    }
    anim_path = os.path.join(ANIM_DIR, f"{model_name}.animation.json")
    with open(anim_path, "w", encoding="utf-8") as f:
        json.dump(anim_data, f, indent=2)
    print(f"Saved animations: {anim_path}")

    # 5. Export Blockbench .bbmodel with 'flamefang_adult_geckolib.bbmodel'
    with open(tex_path, "rb") as f:
        tex_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    tex_uuid = str(uuid.uuid4())

    elements = []
    bone_uuid_map = {}
    element_uuid_map = {}

    for b in adult_bones:
        bone_uuid_map[b["name"]] = str(uuid.uuid4())

    for b in adult_bones:
        for c in b.get("cubes", []):
            cuuid = str(uuid.uuid4())
            element_uuid_map[c["name"]] = cuuid
            ox, oy, oz = c["origin"]
            sx, sy, sz = c["size"]
            u0, v0 = c["uv"]

            elem = {
                "name": c["name"],
                "box_uv": True,
                "rescale": False,
                "locked": False,
                "render_order": "default",
                "allow_mirror_modeling": True,
                "from": [ox, oy, oz],
                "to": [round(ox + sx, 2), round(oy + sy, 2), round(oz + sz, 2)],
                "autouv": 0,
                "color": 0,
                "origin": b["pivot"],
                "uv_offset": [u0, v0],
                "faces": {
                    "north": {"uv": [u0 + sz, v0 + sz, u0 + sz + sx, v0 + sz + sy], "texture": 0},
                    "south": {"uv": [u0 + 2*sz + sx, v0 + sz, u0 + 2*sz + 2*sx, v0 + sz + sy], "texture": 0},
                    "west":  {"uv": [u0, v0 + sz, u0 + sz, v0 + sz + sy], "texture": 0},
                    "east":  {"uv": [u0 + sz + sx, v0 + sz, u0 + 2*sz + sx, v0 + sz + sy], "texture": 0},
                    "up":    {"uv": [u0 + sz + sx, v0 + sz, u0 + sz, v0], "texture": 0},
                    "down":  {"uv": [u0 + sz + 2*sx, v0, u0 + sz + sx, v0 + sz], "texture": 0}
                },
                "type": "cube",
                "uuid": cuuid
            }
            elements.append(elem)

    # Hierarchical Outliner
    bone_dict = {}
    for b in adult_bones:
        bone_dict[b["name"]] = {
            "name": b["name"],
            "origin": b["pivot"],
            "color": 0,
            "uuid": bone_uuid_map[b["name"]],
            "export": True,
            "isOpen": True,
            "locked": False,
            "visibility": True,
            "autouv": 0,
            "children": [c["name"] for c in b.get("cubes", [])],
            "_raw_children": []
        }

    for b in adult_bones:
        b_name = b["name"]
        node = bone_dict[b_name]
        cube_uuids = [element_uuid_map[cname] for cname in node["children"]]
        node["_raw_children"].extend(cube_uuids)

    root_bones = []
    for b in adult_bones:
        b_name = b["name"]
        node = bone_dict[b_name]
        if "parent" in b:
            p_name = b["parent"]
            bone_dict[p_name]["_raw_children"].append(node)
        else:
            root_bones.append(node)

    def clean_node(n):
        return {
            "name": n["name"],
            "origin": n["origin"],
            "color": 0,
            "uuid": n["uuid"],
            "export": True,
            "isOpen": True,
            "locked": False,
            "visibility": True,
            "autouv": 0,
            "children": [clean_node(c) if isinstance(c, dict) else c for c in n["_raw_children"]]
        }

    outliner = [clean_node(r) for r in root_bones]

    # Blockbench Animations
    bb_animations = []
    for a_key, a_val in adult_anims.items():
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
        bb_animations.append({
            "name": aname,
            "uuid": str(uuid.uuid4()),
            "loop": "loop" if a_val.get("loop", True) else "once",
            "length": a_val.get("animation_length", 1.0),
            "animators": animators
        })

    bbmodel_data = {
        "meta": {
            "format_version": "4.10",
            "creation_time": 1728210000,
            "model_format": "geckolib_model",
            "box_uv": True
        },
        "name": model_name,
        "model_identifier": model_name,
        "visible_box": [20, 12, 0],
        "resolution": {"width": tex_w, "height": tex_h},
        "elements": elements,
        "outliner": outliner,
        "textures": [
            {
                "type": "entity",
                "name": f"{model_name}.png",
                "id": "0",
                "uuid": tex_uuid,
                "source": tex_base64
            }
        ],
        "animations": bb_animations
    }

    bbmodel_path = os.path.join(MODELS_DIR, bbmodel_filename)
    with open(bbmodel_path, "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)
    print(f"Saved Blockbench model: {bbmodel_path}")

if __name__ == "__main__":
    export_updated_adult()
    print("\n[SUCCESS] HARMONIC 3D ADULT FLAMEFANG GENERATED SUCCESSFULLY!")
