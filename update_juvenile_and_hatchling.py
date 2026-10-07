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

# ===========================================================================
# 1. FLAMEFANG JUVENIL (Hexápode Atlético, 4 Patas no Chão, Asas Amplas)
# Escala: 2.2 a 2.5 blocos de altura total
# ===========================================================================

juv_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 22, 0],
        "cubes": [
            # 1. Deep chest keel (quilha peitoral de ancoragem)
            {"name": "chest_keel_l", "origin": [0, 13, -13], "size": [7, 11, 8], "category": "torso_chest", "uv_group": "juv_chest_keel"},
            {"name": "chest_keel_r", "origin": [-7, 13, -13], "size": [7, 11, 8], "category": "torso_chest", "uv_group": "juv_chest_keel"},
            # 2. Pectoral armor plates
            {"name": "pectoral_armor_l", "origin": [0, 14, -12], "size": [8, 9, 5], "category": "chest_armor", "uv_group": "juv_pectoral"},
            {"name": "pectoral_armor_r", "origin": [-8, 14, -12], "size": [8, 9, 5], "category": "chest_armor", "uv_group": "juv_pectoral"},
            # 3. Shoulder girdle
            {"name": "shoulder_girdle", "origin": [-10, 20, -9], "size": [20, 6, 6], "category": "torso_mid", "uv_group": "juv_shoulder_girdle"},
            # 4. Mid torso ribcage
            {"name": "torso_mid_l", "origin": [0, 15, -7], "size": [9, 11, 10], "category": "torso_mid", "uv_group": "juv_torso_mid"},
            {"name": "torso_mid_r", "origin": [-9, 15, -7], "size": [9, 11, 10], "category": "torso_mid", "uv_group": "juv_torso_mid"},
            # 5. Tapered belly
            {"name": "belly_mid", "origin": [-8, 16, 3], "size": [16, 9, 8], "category": "torso_belly", "uv_group": "juv_belly"},
            # 6. Muscular pelvis
            {"name": "pelvis_hips", "origin": [-8.5, 17, 11], "size": [17, 9, 9], "category": "torso_hips", "uv_group": "juv_pelvis"},
            # 7. Dorsal spines
            {"name": "dorsal_spines", "origin": [-1.5, 26, -9], "size": [3, 4, 26], "category": "spikes", "uv_group": "juv_dorsal_spines"}
        ]
    },
    # Patas Dianteiras Quadrúpedes (Ground Y = 0)
    {
        "name": "leg_front_left",
        "parent": "body",
        "pivot": [10, 22, -7],
        "cubes": [
            {"name": "shoulder_fl", "origin": [7, 12, -10], "size": [6, 11, 7], "category": "leg", "uv_group": "juv_leg_front"}
        ]
    },
    {
        "name": "leg_front_left_shin",
        "parent": "leg_front_left",
        "pivot": [10, 12, -7],
        "cubes": [
            {"name": "shin_fl", "origin": [7.5, 2, -9.5], "size": [5, 11, 6], "category": "leg", "uv_group": "juv_shin_front"},
            {"name": "elbow_fl", "origin": [8.5, 9, -4.5], "size": [3, 3, 3], "category": "spikes", "uv_group": "juv_elbow"}
        ]
    },
    {
        "name": "leg_front_left_foot",
        "parent": "leg_front_left_shin",
        "pivot": [10, 2, -7],
        "cubes": [
            {"name": "foot_pad_fl", "origin": [7, 0, -11], "size": [6, 2.5, 7], "category": "foot", "uv_group": "juv_foot"},
            {"name": "claw_fl_1", "origin": [7.5, 0, -13], "size": [1.5, 2, 2.5], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_fl_2", "origin": [9.5, 0, -14], "size": [1.5, 2, 3.5], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_fl_3", "origin": [11.5, 0, -13], "size": [1.5, 2, 2.5], "category": "claw", "uv_group": "juv_claw"}
        ]
    },
    {
        "name": "leg_front_right",
        "parent": "body",
        "pivot": [-10, 22, -7],
        "cubes": [
            {"name": "shoulder_fr", "origin": [-13, 12, -10], "size": [6, 11, 7], "category": "leg", "uv_group": "juv_leg_front"}
        ]
    },
    {
        "name": "leg_front_right_shin",
        "parent": "leg_front_right",
        "pivot": [-10, 12, -7],
        "cubes": [
            {"name": "shin_fr", "origin": [-12.5, 2, -9.5], "size": [5, 11, 6], "category": "leg", "uv_group": "juv_shin_front"},
            {"name": "elbow_fr", "origin": [-11.5, 9, -4.5], "size": [3, 3, 3], "category": "spikes", "uv_group": "juv_elbow"}
        ]
    },
    {
        "name": "leg_front_right_foot",
        "parent": "leg_front_right_shin",
        "pivot": [-10, 2, -7],
        "cubes": [
            {"name": "foot_pad_fr", "origin": [-13, 0, -11], "size": [6, 2.5, 7], "category": "foot", "uv_group": "juv_foot"},
            {"name": "claw_fr_1", "origin": [-13, 0, -13], "size": [1.5, 2, 2.5], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_fr_2", "origin": [-11, 0, -14], "size": [1.5, 2, 3.5], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_fr_3", "origin": [-9, 0, -13], "size": [1.5, 2, 2.5], "category": "claw", "uv_group": "juv_claw"}
        ]
    },
    # Patas Traseiras (Ground Y = 0)
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [9, 22, 12],
        "cubes": [
            {"name": "thigh_left", "origin": [6.5, 11, 8], "size": [7, 12, 8], "category": "leg", "uv_group": "juv_thigh"}
        ]
    },
    {
        "name": "leg_left_shin",
        "parent": "leg_left",
        "pivot": [9.5, 12, 12],
        "cubes": [
            {"name": "shin_left", "origin": [7, 2, 10], "size": [5.5, 11, 6], "category": "leg", "uv_group": "juv_shin_rear"},
            {"name": "hock_left", "origin": [7.5, 1, 9], "size": [4.5, 4, 4.5], "category": "leg", "uv_group": "juv_hock"}
        ]
    },
    {
        "name": "leg_left_foot",
        "parent": "leg_left_shin",
        "pivot": [9.5, 2, 11],
        "cubes": [
            {"name": "foot_pad_left", "origin": [6.5, 0, 7], "size": [6.5, 2.5, 8], "category": "foot", "uv_group": "juv_foot_rear"},
            {"name": "claw_hl_1", "origin": [7, 0, 4.5], "size": [1.5, 2, 3], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_hl_2", "origin": [9, 0, 3.5], "size": [1.5, 2, 4], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_hl_3", "origin": [11, 0, 4.5], "size": [1.5, 2, 3], "category": "claw", "uv_group": "juv_claw"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-9, 22, 12],
        "cubes": [
            {"name": "thigh_right", "origin": [-13.5, 11, 8], "size": [7, 12, 8], "category": "leg", "uv_group": "juv_thigh"}
        ]
    },
    {
        "name": "leg_right_shin",
        "parent": "leg_right",
        "pivot": [-9.5, 12, 12],
        "cubes": [
            {"name": "shin_right", "origin": [-12.5, 2, 10], "size": [5.5, 11, 6], "category": "leg", "uv_group": "juv_shin_rear"},
            {"name": "hock_right", "origin": [-12, 1, 9], "size": [4.5, 4, 4.5], "category": "leg", "uv_group": "juv_hock"}
        ]
    },
    {
        "name": "leg_right_foot",
        "parent": "leg_right_shin",
        "pivot": [-9.5, 2, 11],
        "cubes": [
            {"name": "foot_pad_right", "origin": [-13, 0, 7], "size": [6.5, 2.5, 8], "category": "foot", "uv_group": "juv_foot_rear"},
            {"name": "claw_hr_1", "origin": [-12.5, 0, 4.5], "size": [1.5, 2, 3], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_hr_2", "origin": [-10.5, 0, 3.5], "size": [1.5, 2, 4], "category": "claw", "uv_group": "juv_claw"},
            {"name": "claw_hr_3", "origin": [-8.5, 0, 4.5], "size": [1.5, 2, 3], "category": "claw", "uv_group": "juv_claw"}
        ]
    },
    # Pescoço e Cabeça
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 24, -9],
        "cubes": [
            {"name": "neck_lower", "origin": [-4.5, 20, -16], "size": [9, 10, 8], "category": "neck", "uv_group": "juv_neck_low"},
            {"name": "neck_spines_low", "origin": [-1, 29, -15], "size": [2, 4, 6], "category": "spikes", "uv_group": "juv_spikes"}
        ]
    },
    {
        "name": "neck_upper",
        "parent": "neck",
        "pivot": [0, 29, -15],
        "cubes": [
            {"name": "neck_upper_main", "origin": [-4, 26, -22], "size": [8, 9, 8], "category": "neck", "uv_group": "juv_neck_up"},
            {"name": "neck_spines_up", "origin": [-1, 34, -21], "size": [2, 4, 6], "category": "spikes", "uv_group": "juv_spikes"}
        ]
    },
    {
        "name": "head",
        "parent": "neck_upper",
        "pivot": [0, 34, -20],
        "cubes": [
            {"name": "cranium", "origin": [-5, 32, -30], "size": [10, 8, 10], "category": "head", "uv_group": "juv_head"},
            {"name": "snout", "origin": [-4, 32, -37], "size": [8, 5, 8], "category": "snout", "uv_group": "juv_snout"}
        ]
    },
    {
        "name": "jaw_lower",
        "parent": "head",
        "pivot": [0, 32, -28],
        "cubes": [
            {"name": "jaw", "origin": [-3.5, 29, -36], "size": [7, 3.5, 8], "category": "jaw", "uv_group": "juv_jaw"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 38, -26],
        "cubes": [
            {"name": "horn_left", "origin": [3, 37, -26], "size": [2.5, 3.5, 10], "category": "horn", "uv_group": "juv_horns"},
            {"name": "horn_right", "origin": [-5.5, 37, -26], "size": [2.5, 3.5, 10], "category": "horn", "uv_group": "juv_horns"}
        ]
    },
    # Asas Aerodinâmicas Amplas (Isle of Berk, expandidas para trás em Z)
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [10, 26, -6],
        "cubes": [
            {"name": "wing_arm_l", "origin": [10, 24, -8], "size": [16, 3, 3], "category": "wing_arm", "uv_group": "juv_wing_arm"},
            {"name": "wing_mem_inner_l", "origin": [10, 25, -5], "size": [16, 1, 23], "category": "wing_membrane", "uv_group": "juv_wing_mem_inner"}
        ]
    },
    {
        "name": "wing_left_mid",
        "parent": "wing_left",
        "pivot": [26, 26, -5],
        "cubes": [
            {"name": "wing_forearm_l", "origin": [26, 24, -7], "size": [20, 3, 3], "category": "wing_arm", "uv_group": "juv_wing_forearm"},
            {"name": "wing_mem_mid_l", "origin": [25, 25, -4], "size": [21, 1, 30], "category": "wing_membrane", "uv_group": "juv_wing_mem_mid"}
        ]
    },
    {
        "name": "wing_left_fingers",
        "parent": "wing_left_mid",
        "pivot": [46, 26, -4],
        "cubes": [
            {"name": "wing_finger1_l", "origin": [46, 25, -7], "size": [28, 2, 2.5], "category": "wing_arm", "uv_group": "juv_wing_finger1"},
            {"name": "wing_finger2_l", "origin": [46, 25, 6], "size": [24, 1.8, 2], "category": "wing_arm", "uv_group": "juv_wing_finger2"},
            {"name": "wing_mem_outer_l", "origin": [45, 25, -4], "size": [29, 1, 32], "category": "wing_membrane", "uv_group": "juv_wing_mem_outer"}
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-10, 26, -6],
        "cubes": [
            {"name": "wing_arm_r", "origin": [-26, 24, -8], "size": [16, 3, 3], "category": "wing_arm", "uv_group": "juv_wing_arm"},
            {"name": "wing_mem_inner_r", "origin": [-26, 25, -5], "size": [16, 1, 23], "category": "wing_membrane", "uv_group": "juv_wing_mem_inner"}
        ]
    },
    {
        "name": "wing_right_mid",
        "parent": "wing_right",
        "pivot": [-26, 26, -5],
        "cubes": [
            {"name": "wing_forearm_r", "origin": [-46, 24, -7], "size": [20, 3, 3], "category": "wing_arm", "uv_group": "juv_wing_forearm"},
            {"name": "wing_mem_mid_r", "origin": [-46, 25, -4], "size": [21, 1, 30], "category": "wing_membrane", "uv_group": "juv_wing_mem_mid"}
        ]
    },
    {
        "name": "wing_right_fingers",
        "parent": "wing_right_mid",
        "pivot": [-46, 26, -4],
        "cubes": [
            {"name": "wing_finger1_r", "origin": [-74, 25, -7], "size": [28, 2, 2.5], "category": "wing_arm", "uv_group": "juv_wing_finger1"},
            {"name": "wing_finger2_r", "origin": [-70, 25, 6], "size": [24, 1.8, 2], "category": "wing_arm", "uv_group": "juv_wing_finger2"},
            {"name": "wing_mem_outer_r", "origin": [-74, 25, -4], "size": [29, 1, 32], "category": "wing_membrane", "uv_group": "juv_wing_mem_outer"}
        ]
    },
    # Cauda Orgânica Articulada com Leque de Magma (4 Segmentos)
    {
        "name": "tail_1",
        "parent": "body",
        "pivot": [0, 21, 20],
        "cubes": [
            {"name": "tail_1_core", "origin": [-5, 17, 20], "size": [10, 8, 12], "category": "tail_core", "uv_group": "juv_tail_1"},
            {"name": "tail_1_spine", "origin": [-1, 25, 21], "size": [2, 3, 10], "category": "tail_spine", "uv_group": "juv_tail_spine"}
        ]
    },
    {
        "name": "tail_2",
        "parent": "tail_1",
        "pivot": [0, 20, 32],
        "cubes": [
            {"name": "tail_2_core", "origin": [-4, 16.5, 32], "size": [8, 7, 12], "category": "tail_core", "uv_group": "juv_tail_2"},
            {"name": "tail_2_spike_l", "origin": [4, 18.5, 34], "size": [2.5, 2.5, 8], "category": "tail_spike", "uv_group": "juv_tail_spike"},
            {"name": "tail_2_spike_r", "origin": [-6.5, 18.5, 34], "size": [2.5, 2.5, 8], "category": "tail_spike", "uv_group": "juv_tail_spike"},
            {"name": "tail_2_spine", "origin": [-0.75, 23.5, 33], "size": [1.5, 3, 10], "category": "tail_spine", "uv_group": "juv_tail_spine"}
        ]
    },
    {
        "name": "tail_3",
        "parent": "tail_2",
        "pivot": [0, 19, 44],
        "cubes": [
            {"name": "tail_3_core", "origin": [-3, 16.5, 44], "size": [6, 5.5, 12], "category": "tail_core", "uv_group": "juv_tail_3"},
            {"name": "tail_3_fin_l", "origin": [3, 17.5, 45], "size": [3, 1.5, 9], "category": "tail_fin", "uv_group": "juv_tail_fin"},
            {"name": "tail_3_fin_r", "origin": [-6, 17.5, 45], "size": [3, 1.5, 9], "category": "tail_fin", "uv_group": "juv_tail_fin"}
        ]
    },
    {
        "name": "tail_flame",
        "parent": "tail_3",
        "pivot": [0, 18, 56],
        "cubes": [
            {"name": "fan_spear", "origin": [-1.5, 16.5, 56], "size": [3, 3, 16], "category": "flame_core", "uv_group": "juv_flame_core"},
            {"name": "fan_blade_l", "origin": [1.5, 17.2, 57], "size": [7, 1.2, 14], "category": "flame_blade_inner", "uv_group": "juv_flame_blade"},
            {"name": "fan_blade_r", "origin": [-8.5, 17.2, 57], "size": [7, 1.2, 14], "category": "flame_blade_inner", "uv_group": "juv_flame_blade"},
            {"name": "fan_keel_up", "origin": [-0.75, 19.5, 57], "size": [1.5, 3.5, 13], "category": "flame_keel", "uv_group": "juv_flame_keel"}
        ]
    }
]

# ---------------------------------------------------------------------------
# Textura Juvenil HD 256x256 (Paleta de Obsidiana & Magma do Adulto)
# ---------------------------------------------------------------------------
def paint_juv_texture(tex, bones_def, tex_w, tex_h):
    PLASMA_YELLOW    = (255, 238, 51, 255)
    MAGMA_GOLD       = (255, 170, 0, 255)
    FIRE_ORANGE      = (255, 68, 0, 255)
    CRIMSON_LAVA     = (185, 28, 16, 255)
    OBSIDIAN_BASE    = (24, 22, 28, 255)
    OBSIDIAN_SCALE   = (36, 33, 42, 255)
    OBSIDIAN_BEVEL   = (60, 56, 72, 255)
    OBSIDIAN_SHADOW  = (16, 14, 18, 255)
    MEMBRANE_CRIMSON = (178, 26, 22, 255)
    MEMBRANE_SCARLET = (220, 48, 24, 255)
    MEMBRANE_EMBER   = (250, 102, 28, 255)
    MEMBRANE_SHADOW  = (118, 18, 16, 255)
    HORN_MID         = (85, 70, 56, 255)
    EYE_GOLD         = (255, 205, 15, 255)
    EYE_PUPIL        = (12, 8, 8, 255)

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

                        n = noise(px, py, 8)

                        if cat in ("torso_chest", "torso_mid", "torso_belly", "torso_hips", "tail_core", "leg", "foot"):
                            sw, sh = 4, 3
                            row = local_y // sh
                            shift = (sw // 2) if (row % 2 == 1) else 0
                            cu = (local_x + shift) % sw
                            cv = local_y % sh
                            base_c = OBSIDIAN_BEVEL if cv == 0 else (OBSIDIAN_SHADOW if cv == sh - 1 else OBSIDIAN_SCALE)

                            # Veios de magma ventrais
                            if fname == "down" or (cat == "torso_chest" and fname in ("west", "east") and t_y > 0.5):
                                d_v = abs(local_x - fw_int / 2.0)
                                if d_v < 1.2:
                                    base_c = PLASMA_YELLOW
                                elif d_v < 2.5:
                                    base_c = MAGMA_GOLD
                                elif d_v < 3.8:
                                    base_c = FIRE_ORANGE

                        elif cat in ("chest_armor", "tail_spike", "tail_fin", "flame_keel"):
                            base_c = MAGMA_GOLD if (local_x + local_y) % 3 == 0 else FIRE_ORANGE

                        elif cat in ("flame_core", "flame_blade_inner"):
                            heat = 1.0 - (0.5 * t_y + 0.3 * t_x)
                            base_c = PLASMA_YELLOW if heat > 0.6 else (MAGMA_GOLD if heat > 0.35 else FIRE_ORANGE)

                        elif cat == "wing_membrane":
                            fold = math.sin(local_x * 0.4 + local_y * 0.25)
                            base_c = MEMBRANE_SCARLET if fold > 0.3 else (MEMBRANE_CRIMSON if fold > -0.3 else MEMBRANE_SHADOW)

                        elif cat == "horn":
                            base_c = HORN_MID
                        elif cat == "spikes":
                            base_c = OBSIDIAN_BEVEL
                        elif cat == "claw":
                            base_c = HORN_MID
                        elif cat == "head":
                            base_c = OBSIDIAN_SCALE
                        elif cat in ("snout", "jaw"):
                            base_c = OBSIDIAN_BASE
                        else:
                            base_c = OBSIDIAN_SCALE

                        col = shade(base_c, n)
                        if 0 <= px < tex_w and 0 <= py < tex_h:
                            tex.putpixel((px, py), col)

            if c["name"] == "cranium":
                fu_w, fv_w = int(u0), int(v0 + sz)
                fu_e, fv_e = int(u0 + sz + sx), int(v0 + sz)
                for ex in range(2, 5):
                    for ey in range(2, 5):
                        if 0 <= fu_w + ex < tex_w and 0 <= fv_w + ey < tex_h:
                            tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        if 0 <= fu_e + int(sz) - 1 - ex < tex_w and 0 <= fv_e + ey < tex_h:
                            tex.putpixel((fu_e + int(sz) - 1 - ex, fv_e + ey), EYE_GOLD)
                for ey in range(2, 5):
                    if 0 <= fu_w + 4 < tex_w and 0 <= fv_w + ey < tex_h:
                        tex.putpixel((fu_w + 4, fv_w + ey), EYE_PUPIL)
                    if 0 <= fu_e + int(sz) - 1 - 4 < tex_w and 0 <= fv_e + ey < tex_h:
                        tex.putpixel((fu_e + int(sz) - 1 - 4, fv_e + ey), EYE_PUPIL)

# Animações GeckoLib Juvenil
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

juv_anims = {
    "animation.flamefang_juvenile.idle": {
        "loop": True,
        "animation_length": 3.0,
        "bones": {
            "body": {
                "rotation": {"0.0": [0, 0, 0], "1.5": [-1.5, 0, 0], "3.0": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "1.5": [0, -0.4, 0], "3.0": [0, 0, 0]}
            },
            "neck": {"rotation": {"0.0": [0, 0, 0], "1.5": [2.0, 0, 0], "3.0": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [-1.5, 0, 0], "3.0": [0, 0, 0]}},
            "leg_front_left": {"rotation": {"0.0": [0, 0, 0], "1.5": [-1.0, 0, 0], "3.0": [0, 0, 0]}},
            "leg_front_right": {"rotation": {"0.0": [0, 0, 0], "1.5": [-1.0, 0, 0], "3.0": [0, 0, 0]}},
            "leg_left": {"rotation": {"0.0": [0, 0, 0], "1.5": [1.0, 0, 0], "3.0": [0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [0, 0, 0], "1.5": [1.0, 0, 0], "3.0": [0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, -3.0], "1.5": [0, 0, 0], "3.0": [0, 0, -3.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, 3.0], "1.5": [0, 0, 0], "3.0": [0, 0, 3.0]}},
            "tail_1": {"rotation": {"0.0": [0, -2.0, 0], "1.5": [0, 2.0, 0], "3.0": [0, -2.0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, -4.0, 0], "1.5": [0, 4.0, 0], "3.0": [0, -4.0, 0]}},
            "tail_3": {"rotation": {"0.0": [0, -6.0, 0], "1.5": [0, 6.0, 0], "3.0": [0, -6.0, 0]}},
            "tail_flame": {"rotation": {"0.0": [0, -8.0, 0], "1.5": [0, 8.0, 0], "3.0": [0, -8.0, 0]}}
        }
    },
    "animation.flamefang_juvenile.walk": {
        "loop": True,
        "animation_length": 1.6,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.4": [0, 0.5, 0], "0.8": [0, 0, 0], "1.2": [0, 0.5, 0], "1.6": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [1.5, 1.0, -1.5], "0.8": [1.5, -1.0, 1.5], "1.6": [1.5, 1.0, -1.5]}},
            "leg_front_left": {"rotation": {"0.0": [18.0, 0, 0], "0.4": [-8.0, 0, 0], "0.8": [-18.0, 0, 0], "1.2": [0.0, 0, 0], "1.6": [18.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [18.0, 0, 0], "0.4": [-8.0, 0, 0], "0.8": [-18.0, 0, 0], "1.2": [0.0, 0, 0], "1.6": [18.0, 0, 0]}},
            "leg_front_right": {"rotation": {"0.0": [-18.0, 0, 0], "0.4": [0.0, 0, 0], "0.8": [18.0, 0, 0], "1.2": [-8.0, 0, 0], "1.6": [-18.0, 0, 0]}},
            "leg_left": {"rotation": {"0.0": [-18.0, 0, 0], "0.4": [0.0, 0, 0], "0.8": [18.0, 0, 0], "1.2": [-8.0, 0, 0], "1.6": [-18.0, 0, 0]}},
            "tail_1": {"rotation": {"0.0": [0, 3.0, 0], "0.8": [0, -3.0, 0], "1.6": [0, 3.0, 0]}},
            "tail_2": {"rotation": {"0.0": [0, 6.0, 0], "0.8": [0, -6.0, 0], "1.6": [0, 6.0, 0]}},
            "tail_flame": {"rotation": {"0.0": [0, 10.0, 0], "0.8": [0, -10.0, 0], "1.6": [0, 10.0, 0]}}
        }
    },
    "animation.flamefang_juvenile.fly_flap": generate_juv_fly_flap(duration=1.1, frames=37),
    "animation.flamefang_juvenile.glide": generate_juv_glide(duration=3.5, frames=37),
    "animation.flamefang_juvenile.eating": generate_juv_eating(),
    "animation.flamefang_juvenile.sleep": generate_juv_sleep(),
    "animation.flamefang_juvenile.wake_up": generate_juv_wake_up(),
    "animation.flamefang_juvenile.roar": generate_juv_roar()
}


# ===========================================================================
# 2. FLAMEFANG FILHOTE / CHIBI (4 Patinhas Firmes, Barriga Roliça, Broto Orgânico)
# Escala: 0.9 a 1.0 bloco de altura
# ===========================================================================

hatch_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 7, 0],
        "cubes": [
            {"name": "torso", "origin": [-4.5, 3.5, -4.5], "size": [9, 7.5, 10], "category": "torso", "uv_group": "hatch_torso"},
            {"name": "belly_chubby", "origin": [-4, 4, -5.5], "size": [8, 6, 3], "category": "chest", "uv_group": "hatch_belly"}
        ]
    },
    # 4 Patinhas de Filhote (Ground Y = 0)
    {
        "name": "leg_front_left",
        "parent": "body",
        "pivot": [4.5, 6, -3],
        "cubes": [
            {"name": "leg_fl", "origin": [3, 0, -4.5], "size": [3.5, 6, 3.5], "category": "leg", "uv_group": "hatch_leg_front"}
        ]
    },
    {
        "name": "leg_front_right",
        "parent": "body",
        "pivot": [-4.5, 6, -3],
        "cubes": [
            {"name": "leg_fr", "origin": [-6.5, 0, -4.5], "size": [3.5, 6, 3.5], "category": "leg", "uv_group": "hatch_leg_front"}
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [4.5, 6, 3],
        "cubes": [
            {"name": "thigh_left", "origin": [3, 2, 1.5], "size": [3.5, 4.5, 4], "category": "leg", "uv_group": "hatch_leg_rear"},
            {"name": "foot_left", "origin": [3, 0, 0.5], "size": [3.5, 2, 4.5], "category": "foot", "uv_group": "hatch_foot_rear"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-4.5, 6, 3],
        "cubes": [
            {"name": "thigh_right", "origin": [-6.5, 2, 1.5], "size": [3.5, 4.5, 4], "category": "leg", "uv_group": "hatch_leg_rear"},
            {"name": "foot_right", "origin": [-6.5, 0, 0.5], "size": [3.5, 2, 4.5], "category": "foot", "uv_group": "hatch_foot_rear"}
        ]
    },
    # Cabeça e Brotos de Chifres
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 7.5, -3],
        "cubes": [{"name": "neck_main", "origin": [-2.5, 6.5, -6], "size": [5, 4, 4], "category": "neck", "uv_group": "hatch_neck"}]
    },
    {
        "name": "head",
        "parent": "neck",
        "pivot": [0, 9, -5],
        "cubes": [
            {"name": "cranium", "origin": [-4.5, 8, -11], "size": [9, 8, 8], "category": "head", "uv_group": "hatch_cranium"},
            {"name": "snout", "origin": [-3, 8, -14], "size": [6, 4, 4], "category": "snout", "uv_group": "hatch_snout"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 16, -7],
        "cubes": [
            {"name": "horn_nub_l", "origin": [2.5, 15, -8], "size": [1.5, 2, 2.5], "category": "horn", "uv_group": "hatch_horn"},
            {"name": "horn_nub_r", "origin": [-4, 15, -8], "size": [1.5, 2, 2.5], "category": "horn", "uv_group": "hatch_horn"}
        ]
    },
    # Asinhas Fofas de Bebê
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [4.5, 8.5, -2],
        "cubes": [{"name": "wing_l", "origin": [4.5, 8, -2], "size": [9, 1, 7], "category": "wing_membrane", "uv_group": "hatch_wing"}]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-4.5, 8.5, -2],
        "cubes": [{"name": "wing_r", "origin": [-13.5, 8, -2], "size": [9, 1, 7], "category": "wing_membrane", "uv_group": "hatch_wing"}]
    },
    # Cauda com Broto Orgânico de Fogo (Sem Cubos Toscos!)
    {
        "name": "tail_base",
        "parent": "body",
        "pivot": [0, 6, 5],
        "cubes": [{"name": "tail_b", "origin": [-2, 5, 5], "size": [4, 4, 6], "category": "tail", "uv_group": "hatch_tail"}]
    },
    {
        "name": "tail_mid",
        "parent": "tail_base",
        "pivot": [0, 6, 11],
        "cubes": [{"name": "tail_m", "origin": [-1.5, 5.5, 11], "size": [3, 3, 5], "category": "tail", "uv_group": "hatch_tail_mid"}]
    },
    {
        "name": "tail_flame",
        "parent": "tail_mid",
        "pivot": [0, 6, 16],
        "cubes": [
            {"name": "flame_core", "origin": [-1.25, 5.25, 16], "size": [2.5, 3.5, 5], "category": "flame_core", "uv_group": "hatch_flame_core"},
            {"name": "flame_petal_l", "origin": [1.2, 5.8, 17], "size": [2, 2.5, 4], "category": "flame_petal", "uv_group": "hatch_flame_petal"},
            {"name": "flame_petal_r", "origin": [-3.2, 5.8, 17], "size": [2, 2.5, 4], "category": "flame_petal", "uv_group": "hatch_flame_petal"},
            {"name": "flame_crest", "origin": [-0.75, 7.2, 17], "size": [1.5, 2, 4], "category": "flame_crest", "uv_group": "hatch_flame_crest"}
        ]
    }
]

# ---------------------------------------------------------------------------
# Textura Filhote 128x128 (Expressiva, Macia e Detalhada)
# ---------------------------------------------------------------------------
def paint_hatch_texture(tex, bones_def, tex_w, tex_h):
    SCALE_BABY   = (48, 44, 56, 255)
    SCALE_SOFT   = (65, 60, 75, 255)
    BELLY_WARM   = (215, 75, 50, 255)
    BELLY_SOFT   = (240, 110, 80, 255)
    HORN_CUTE    = (125, 110, 95, 255)
    FIRE_YELLOW  = (255, 240, 100, 255)
    FIRE_ORANGE  = (255, 140, 25, 255)
    FIRE_CRIMSON = (195, 35, 20, 255)
    EYE_GOLD     = (255, 215, 25, 255)
    EYE_SHINE    = (255, 255, 245, 255)
    EYE_PUPIL    = (20, 14, 12, 255)

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

                        n = noise(px, py, 6)

                        if cat == "chest":
                            base_c = BELLY_SOFT if t_y > 0.4 else BELLY_WARM
                        elif cat in ("flame_core", "flame_petal", "flame_crest"):
                            heat = 1.0 - t_y * 0.6
                            base_c = FIRE_YELLOW if heat > 0.7 else (FIRE_ORANGE if heat > 0.4 else FIRE_CRIMSON)
                        elif cat == "wing_membrane":
                            base_c = BELLY_WARM if (local_x + local_y) % 2 == 0 else FIRE_ORANGE
                        elif cat == "horn":
                            base_c = HORN_CUTE
                        elif cat == "snout":
                            base_c = SCALE_BABY
                        else:
                            base_c = SCALE_SOFT if (local_x + local_y) % 3 == 0 else SCALE_BABY

                        col = shade(base_c, n)
                        if 0 <= px < tex_w and 0 <= py < tex_h:
                            tex.putpixel((px, py), col)

            if c["name"] == "cranium":
                fu_w, fv_w = int(u0), int(v0 + sz)
                fu_e, fv_e = int(u0 + sz + sx), int(v0 + sz)
                # Olhos grandes e doces
                for ex in range(2, 6):
                    for ey in range(2, 6):
                        if 0 <= fu_w + ex < tex_w and 0 <= fv_w + ey < tex_h:
                            tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        if 0 <= fu_e + int(sz) - 1 - ex < tex_w and 0 <= fv_e + ey < tex_h:
                            tex.putpixel((fu_e + int(sz) - 1 - ex, fv_e + ey), EYE_GOLD)
                for ey in range(3, 6):
                    if 0 <= fu_w + 4 < tex_w and 0 <= fv_w + ey < tex_h:
                        tex.putpixel((fu_w + 4, fv_w + ey), EYE_PUPIL)
                    if 0 <= fu_e + int(sz) - 1 - 4 < tex_w and 0 <= fv_e + ey < tex_h:
                        tex.putpixel((fu_e + int(sz) - 1 - 4, fv_e + ey), EYE_PUPIL)
                # Brilho do olho
                if 0 <= fu_w + 2 < tex_w and 0 <= fv_w + 2 < tex_h:
                    tex.putpixel((fu_w + 2, fv_w + 2), EYE_SHINE)
                if 0 <= fu_e + int(sz) - 1 - 2 < tex_w and 0 <= fv_e + 2 < tex_h:
                    tex.putpixel((fu_e + int(sz) - 1 - 2, fv_e + 2), EYE_SHINE)

# Animações Filhote Chibi
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

hatch_anims = {
    "animation.flamefang_hatchling.idle": {
        "loop": True,
        "animation_length": 2.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0, 0, 0], "1.25": [-2.0, 0, 0], "2.5": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "1.25": [0, -0.3, 0], "2.5": [0, 0, 0]}
            },
            "head": {
                "rotation": {"0.0": [0, 0, 0], "0.8": [4.0, 8.0, 4.0], "1.6": [2.0, -8.0, -3.0], "2.5": [0, 0, 0]}
            },
            "leg_front_left": {"rotation": {"0.0": [0, 0, 0], "1.25": [-1.0, 0, 0], "2.5": [0, 0, 0]}},
            "leg_front_right": {"rotation": {"0.0": [0, 0, 0], "1.25": [-1.0, 0, 0], "2.5": [0, 0, 0]}},
            "leg_left": {"rotation": {"0.0": [0, 0, 0], "1.25": [1.0, 0, 0], "2.5": [0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [0, 0, 0], "1.25": [1.0, 0, 0], "2.5": [0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, -8.0, 0], "1.25": [0, 8.0, 0], "2.5": [0, -8.0, 0]}},
            "tail_flame": {
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.25": [1.2, 1.3, 1.2], "2.5": [1.0, 1.0, 1.0]},
                "rotation": {"0.0": [0, -12.0, 0], "1.25": [0, 12.0, 0], "2.5": [0, -12.0, 0]}
            }
        }
    },
    "animation.flamefang_hatchling.walk": {
        "loop": True,
        "animation_length": 1.2,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.3": [0, 0.4, 0], "0.6": [0, 0, 0], "0.9": [0, 0.4, 0], "1.2": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [1.5, 0, -1.0], "0.6": [1.5, 0, 1.0], "1.2": [1.5, 0, -1.0]}},
            "leg_front_left": {"rotation": {"0.0": [22.0, 0, 0], "0.6": [-22.0, 0, 0], "1.2": [22.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [22.0, 0, 0], "0.6": [-22.0, 0, 0], "1.2": [22.0, 0, 0]}},
            "leg_front_right": {"rotation": {"0.0": [-22.0, 0, 0], "0.6": [22.0, 0, 0], "1.2": [-22.0, 0, 0]}},
            "leg_left": {"rotation": {"0.0": [-22.0, 0, 0], "0.6": [22.0, 0, 0], "1.2": [-22.0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, 14.0, 0], "0.6": [0, -14.0, 0], "1.2": [0, 14.0, 0]}}
        }
    },
    "animation.flamefang_hatchling.fly_flap": generate_hatch_fly_flap(duration=0.65, frames=25),
    "animation.flamefang_hatchling.glide": generate_hatch_glide(duration=2.5, frames=25),
    "animation.flamefang_hatchling.eating": generate_hatch_eating(),
    "animation.flamefang_hatchling.sleep": generate_hatch_sleep(),
    "animation.flamefang_hatchling.wake_up": generate_hatch_wake_up(),
    "animation.flamefang_hatchling.roar": generate_hatch_roar()
}


# ===========================================================================
# Exporter Geral GeckoLib & Blockbench
# ===========================================================================
def export_stage_model(model_name, bbmodel_filename, bones_def, anims_def, tex_w, tex_h, painter_fn):
    print(f"\n==========================================")
    print(f"Exporting: {model_name} -> {bbmodel_filename} ({tex_w}x{tex_h})")
    print(f"==========================================")

    # 1. Gather all cubes and pack UVs
    all_cubes = []
    for b in bones_def:
        for c in b.get("cubes", []):
            all_cubes.append(c)

    pack_uvs(all_cubes, tex_w, tex_h, padding=2)

    # 2. Paint Texture
    tex_img = Image.new("RGBA", (tex_w, tex_h), (0, 0, 0, 0))
    painter_fn(tex_img, bones_def, tex_w, tex_h)

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
                    "visible_bounds_width": 12,
                    "visible_bounds_height": 8,
                    "visible_bounds_offset": [0, 3, 0]
                },
                "bones": []
            }
        ]
    }

    for b in bones_def:
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
        "animations": anims_def
    }
    anim_path = os.path.join(ANIM_DIR, f"{model_name}.animation.json")
    with open(anim_path, "w", encoding="utf-8") as f:
        json.dump(anim_data, f, indent=2)
    print(f"Saved animations: {anim_path}")

    # 5. Export Blockbench .bbmodel with 'geckolib_model' format
    with open(tex_path, "rb") as f:
        tex_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    tex_uuid = str(uuid.uuid4())

    elements = []
    bone_uuid_map = {}
    element_uuid_map = {}

    for b in bones_def:
        bone_uuid_map[b["name"]] = str(uuid.uuid4())

    for b in bones_def:
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
    for b in bones_def:
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

    for b in bones_def:
        b_name = b["name"]
        node = bone_dict[b_name]
        cube_uuids = [element_uuid_map[cname] for cname in node["children"]]
        node["_raw_children"].extend(cube_uuids)

    root_bones = []
    for b in bones_def:
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
    for a_key, a_val in anims_def.items():
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
        "visible_box": [12, 8, 0],
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

def run_updates():
    # 1. Update Juvenile (256x256)
    export_stage_model(
        model_name="flamefang_juvenile",
        bbmodel_filename="flamefang_Juvenil_geckolib.bbmodel",
        bones_def=juv_bones,
        anims_def=juv_anims,
        tex_w=256,
        tex_h=256,
        painter_fn=paint_juv_texture
    )

    # 2. Update Hatchling (128x128)
    export_stage_model(
        model_name="flamefang_hatchling",
        bbmodel_filename="flamefang_hatchling_geckolib.bbmodel",
        bones_def=hatch_bones,
        anims_def=hatch_anims,
        tex_w=128,
        tex_h=128,
        painter_fn=paint_hatch_texture
    )

    print("\n[SUCCESS] JUVENILE AND HATCHLING MODELS 100% UPGRADED TO HARMONIC STANDARD!")

if __name__ == "__main__":
    run_updates()
