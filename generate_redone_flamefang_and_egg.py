import json
import math
import os
import uuid
import base64
from PIL import Image, ImageDraw

# Directories
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

def pack_uvs(cubes_list, tex_w, tex_h, padding=1):
    unique_items = []
    seen = set()
    for c in cubes_list:
        uv_group = c.get('uv_group', c['name'])
        if uv_group not in seen:
            seen.add(uv_group)
            sx, sy, sz = c['size']
            pw = int(2 * (sx + sz))
            ph = int(sz + sy)
            unique_items.append((uv_group, pw, ph))

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

def export_model(model_name, bbmodel_filename, bones_def, anims_def, tex_w, tex_h, painter_fn, extra_geo_names=None):
    print(f"\n==========================================")
    print(f"Exporting: {model_name} -> {bbmodel_filename} ({tex_w}x{tex_h})")
    print(f"==========================================")

    # 1. Gather all cubes and pack UVs
    all_cubes = []
    for b in bones_def:
        for c in b.get("cubes", []):
            all_cubes.append(c)

    pack_uvs(all_cubes, tex_w, tex_h, padding=1)

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
                    "visible_bounds_width": 10,
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

    geo_targets = [f"{model_name}.geo.json"]
    if extra_geo_names:
        geo_targets.extend(extra_geo_names)

    for g_target in geo_targets:
        geo_path = os.path.join(GEO_DIR, g_target)
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

    # 5. Export Blockbench .bbmodel with '_geckolib.bbmodel' format
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
                "to": [ox + sx, oy + sy, oz + sz],
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

    root_bones = []
    for b in bones_def:
        b_name = b["name"]
        node = bone_dict[b_name]
        cube_uuids = [element_uuid_map[cname] for cname in node["children"]]
        node["_raw_children"].extend(cube_uuids)

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
            "loop": "loop",
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
        "visible_box": [6, 6, 0],
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

# ===========================================================================
# 1. FLAMEFANG ADULT COLOSSAL (AERODYNAMIC HORIZONTAL ISLE OF BERK WINGS)
# ===========================================================================

adult_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 36, 0],
        "cubes": [
            {"name": "torso_main", "origin": [-13, 26, -16], "size": [26, 22, 32], "category": "torso"},
            {"name": "chest_pectoral", "origin": [-11, 28, -22], "size": [22, 16, 6], "category": "chest"},
            {"name": "shoulder_blades", "origin": [-14, 40, -10], "size": [28, 6, 10], "category": "spikes"},
            {"name": "dorsal_ridge", "origin": [-2, 48, -14], "size": [4, 6, 26], "category": "spikes"}
        ]
    },
    {
        "name": "arm_left",
        "parent": "body",
        "pivot": [14, 34, -10],
        "cubes": [
            {"name": "bicep_left", "origin": [13, 26, -12], "size": [5, 10, 5], "category": "arm", "uv_group": "arm_bicep"},
            {"name": "forearm_left", "origin": [13.5, 18, -11.5], "size": [4, 8, 4], "category": "arm", "uv_group": "arm_forearm"},
            {"name": "claw_left", "origin": [13, 15, -14], "size": [5, 3, 6], "category": "claw", "uv_group": "arm_claw"}
        ]
    },
    {
        "name": "arm_right",
        "parent": "body",
        "pivot": [-14, 34, -10],
        "cubes": [
            {"name": "bicep_right", "origin": [-18, 26, -12], "size": [5, 10, 5], "category": "arm", "uv_group": "arm_bicep"},
            {"name": "forearm_right", "origin": [-17.5, 18, -11.5], "size": [4, 8, 4], "category": "arm", "uv_group": "arm_forearm"},
            {"name": "claw_right", "origin": [-18, 15, -14], "size": [5, 3, 6], "category": "claw", "uv_group": "arm_claw"}
        ]
    },
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 42, -14],
        "cubes": [
            {"name": "neck_lower", "origin": [-7, 36, -26], "size": [14, 16, 16], "category": "neck"},
            {"name": "neck_spines_lower", "origin": [-1, 48, -24], "size": [2, 6, 12], "category": "spikes"}
        ]
    },
    {
        "name": "neck_upper",
        "parent": "neck",
        "pivot": [0, 50, -26],
        "cubes": [
            {"name": "neck_upper_main", "origin": [-6, 46, -38], "size": [12, 14, 14], "category": "neck"},
            {"name": "neck_spines_upper", "origin": [-1, 58, -36], "size": [2, 6, 10], "category": "spikes"}
        ]
    },
    {
        "name": "head",
        "parent": "neck_upper",
        "pivot": [0, 58, -38],
        "cubes": [
            {"name": "cranium", "origin": [-8, 54, -52], "size": [16, 12, 16], "category": "head"},
            {"name": "brow_ridges", "origin": [-7, 64, -50], "size": [14, 4, 10], "category": "spikes"},
            {"name": "snout_upper", "origin": [-6, 54, -64], "size": [12, 8, 14], "category": "snout"}
        ]
    },
    {
        "name": "jaw_lower",
        "parent": "head",
        "pivot": [0, 54, -48],
        "cubes": [
            {"name": "jaw", "origin": [-5.5, 49, -62], "size": [11, 5, 14], "category": "jaw"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 64, -46],
        "cubes": [
            {"name": "horn_left_main", "origin": [5, 62, -44], "size": [4, 5, 14], "category": "horn", "uv_group": "horn_main"},
            {"name": "horn_left_tip", "origin": [6, 65, -32], "size": [3, 3, 10], "category": "horn", "uv_group": "horn_tip"},
            {"name": "horn_right_main", "origin": [-9, 62, -44], "size": [4, 5, 14], "category": "horn", "uv_group": "horn_main"},
            {"name": "horn_right_tip", "origin": [-9, 65, -32], "size": [3, 3, 10], "category": "horn", "uv_group": "horn_tip"},
            {"name": "cheek_spikes", "origin": [-9, 53, -48], "size": [18, 4, 4], "category": "spikes"}
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [13, 34, 10],
        "cubes": [
            {"name": "thigh_left", "origin": [11, 20, 6], "size": [9, 18, 12], "category": "leg", "uv_group": "leg_thigh"}
        ]
    },
    {
        "name": "leg_left_shin",
        "parent": "leg_left",
        "pivot": [15, 20, 16],
        "cubes": [
            {"name": "shin_left", "origin": [13, 6, 12], "size": [7, 16, 9], "category": "leg", "uv_group": "leg_shin"}
        ]
    },
    {
        "name": "leg_left_foot",
        "parent": "leg_left_shin",
        "pivot": [15, 6, 14],
        "cubes": [
            {"name": "foot_left", "origin": [12, 0, 6], "size": [8, 4, 12], "category": "foot", "uv_group": "leg_foot"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-13, 34, 10],
        "cubes": [
            {"name": "thigh_right", "origin": [-20, 20, 6], "size": [9, 18, 12], "category": "leg", "uv_group": "leg_thigh"}
        ]
    },
    {
        "name": "leg_right_shin",
        "parent": "leg_right",
        "pivot": [-15, 20, 16],
        "cubes": [
            {"name": "shin_right", "origin": [-20, 6, 12], "size": [7, 16, 9], "category": "leg", "uv_group": "leg_shin"}
        ]
    },
    {
        "name": "leg_right_foot",
        "parent": "leg_right_shin",
        "pivot": [-15, 6, 14],
        "cubes": [
            {"name": "foot_right", "origin": [-20, 0, 6], "size": [8, 4, 12], "category": "foot", "uv_group": "leg_foot"}
        ]
    },
    {
        "name": "tail_base",
        "parent": "body",
        "pivot": [0, 34, 16],
        "cubes": [
            {"name": "tail_base_seg", "origin": [-7, 26, 16], "size": [14, 14, 28], "category": "tail"},
            {"name": "tail_base_spines", "origin": [-1, 40, 18], "size": [2, 5, 24], "category": "spikes"}
        ]
    },
    {
        "name": "tail_mid",
        "parent": "tail_base",
        "pivot": [0, 32, 44],
        "cubes": [
            {"name": "tail_mid_seg", "origin": [-5, 26, 44], "size": [10, 10, 28], "category": "tail"},
            {"name": "tail_mid_spines", "origin": [-1, 36, 46], "size": [2, 4, 22], "category": "spikes"}
        ]
    },
    {
        "name": "tail_tip",
        "parent": "tail_mid",
        "pivot": [0, 30, 72],
        "cubes": [
            {"name": "tail_tip_seg", "origin": [-3, 26, 72], "size": [6, 6, 28], "category": "tail"}
        ]
    },
    {
        "name": "tail_flame",
        "parent": "tail_tip",
        "pivot": [0, 29, 100],
        "cubes": [
            {"name": "flame_core", "origin": [-4, 24, 98], "size": [8, 10, 14], "category": "flame_core"},
            {"name": "flame_plume_1", "origin": [-6, 22, 102], "size": [12, 14, 16], "category": "flame_outer"},
            {"name": "flame_plume_2", "origin": [-7, 21, 106], "size": [14, 16, 12], "category": "flame_outer"}
        ]
    },
    # -------------------------------------------------------------
    # AERODYNAMIC HORIZONTAL ISLE OF BERK WINGS (LEFT & RIGHT)
    # Thickness Y = 1, broad chord Z = 16 to 26 extending backward!
    # -------------------------------------------------------------
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [12, 42, -8],
        "cubes": [
            # Inner arm leading edge
            {"name": "wing_left_arm", "origin": [12, 40, -10], "size": [28, 4, 6], "category": "wing_arm", "uv_group": "wing_bone1"},
            # Horizontal aerodynamic inner membrane (extends backwards towards flank)
            {"name": "wing_left_membrane_inner", "origin": [12, 41, -4], "size": [26, 1, 16], "category": "wing_membrane", "uv_group": "wing_mem_inner"}
        ]
    },
    {
        "name": "wing_left_mid",
        "parent": "wing_left",
        "pivot": [40, 42, -6],
        "cubes": [
            # Forearm / wrist bone
            {"name": "wing_left_forearm", "origin": [40, 40, -8], "size": [32, 4, 5], "category": "wing_arm", "uv_group": "wing_bone2"},
            # Thumb hook claw
            {"name": "wing_left_thumb", "origin": [39, 41, -12], "size": [3, 4, 5], "category": "claw", "uv_group": "wing_thumb"},
            # Horizontal aerodynamic mid membrane
            {"name": "wing_left_membrane_mid", "origin": [38, 41, -3], "size": [32, 1, 24], "category": "wing_membrane", "uv_group": "wing_mem_mid"}
        ]
    },
    {
        "name": "wing_left_outer",
        "parent": "wing_left_mid",
        "pivot": [72, 42, -5],
        "cubes": [
            # Leading edge finger strut
            {"name": "wing_left_finger1", "origin": [72, 41, -7], "size": [38, 3, 4], "category": "wing_arm", "uv_group": "wing_finger1"},
            # Secondary support finger
            {"name": "wing_left_finger2", "origin": [72, 41, 4], "size": [30, 2, 3], "category": "wing_arm", "uv_group": "wing_finger2"},
            # Horizontal outer wing membrane sweeping back in scythe fan
            {"name": "wing_left_membrane_outer", "origin": [70, 41, -3], "size": [38, 1, 26], "category": "wing_membrane", "uv_group": "wing_mem_outer"},
            # Trailing wing tip scallop
            {"name": "wing_left_membrane_tip", "origin": [96, 41, 10], "size": [16, 1, 18], "category": "wing_membrane", "uv_group": "wing_mem_tip"}
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-12, 42, -8],
        "cubes": [
            {"name": "wing_right_arm", "origin": [-40, 40, -10], "size": [28, 4, 6], "category": "wing_arm", "uv_group": "wing_bone1"},
            {"name": "wing_right_membrane_inner", "origin": [-38, 41, -4], "size": [26, 1, 16], "category": "wing_membrane", "uv_group": "wing_mem_inner"}
        ]
    },
    {
        "name": "wing_right_mid",
        "parent": "wing_right",
        "pivot": [-40, 42, -6],
        "cubes": [
            {"name": "wing_right_forearm", "origin": [-72, 40, -8], "size": [32, 4, 5], "category": "wing_arm", "uv_group": "wing_bone2"},
            {"name": "wing_right_thumb", "origin": [-42, 41, -12], "size": [3, 4, 5], "category": "claw", "uv_group": "wing_thumb"},
            {"name": "wing_right_membrane_mid", "origin": [-70, 41, -3], "size": [32, 1, 24], "category": "wing_membrane", "uv_group": "wing_mem_mid"}
        ]
    },
    {
        "name": "wing_right_outer",
        "parent": "wing_right_mid",
        "pivot": [-72, 42, -5],
        "cubes": [
            {"name": "wing_right_finger1", "origin": [-110, 41, -7], "size": [38, 3, 4], "category": "wing_arm", "uv_group": "wing_finger1"},
            {"name": "wing_right_finger2", "origin": [-102, 41, 4], "size": [30, 2, 3], "category": "wing_arm", "uv_group": "wing_finger2"},
            {"name": "wing_right_membrane_outer", "origin": [-108, 41, -3], "size": [38, 1, 26], "category": "wing_membrane", "uv_group": "wing_mem_outer"},
            {"name": "wing_right_membrane_tip", "origin": [-112, 41, 10], "size": [16, 1, 18], "category": "wing_membrane", "uv_group": "wing_mem_tip"}
        ]
    }
]

def paint_adult_texture(tex, bones_def, tex_w, tex_h):
    SCALE_DARK = (24, 22, 28, 255)
    SCALE_MID = (35, 32, 42, 255)
    MAGMA_DARK = (140, 28, 22, 255)
    MAGMA_MID = (185, 48, 30, 255)
    MAGMA_GLOW = (225, 80, 35, 255)
    MAGMA_CORE = (255, 160, 40, 255)
    HORN_DARK = (42, 36, 30, 255)
    HORN_MID = (78, 66, 54, 255)
    HORN_LIGHT = (118, 102, 86, 255)
    FIRE_YELLOW = (255, 245, 120, 255)
    FIRE_ORANGE = (255, 125, 20, 255)
    FIRE_RED = (210, 40, 15, 255)
    MEMBRANE_DARK = (60, 20, 16, 255)
    MEMBRANE_MID = (88, 30, 24, 255)
    EYE_GOLD = (255, 200, 15, 255)
    EYE_PUPIL = (12, 8, 8, 255)
    FANG_COLOR = (228, 220, 198, 255)

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
                for py in range(int(fv), int(fv + fh)):
                    for px in range(int(fu), int(fu + fw)):
                        n = noise(px, py, 14)
                        if cat == "torso":
                            if fname == "down":
                                base_c = MAGMA_CORE if (px * 3 + py * 7) % 11 == 0 else MAGMA_MID
                            elif fname in ("west", "east"):
                                rel_y = (py - fv) / max(1, fh)
                                base_c = MAGMA_MID if rel_y > 0.65 else SCALE_MID
                            else:
                                base_c = SCALE_MID
                        elif cat == "chest":
                            base_c = MAGMA_GLOW if (px + py) % 6 == 0 else MAGMA_DARK
                        elif cat == "neck":
                            base_c = MAGMA_MID if fname in ("north", "down") else SCALE_MID
                        elif cat == "head":
                            base_c = SCALE_MID
                        elif cat == "snout":
                            base_c = SCALE_DARK
                        elif cat == "jaw":
                            base_c = MAGMA_DARK if fname == "down" else SCALE_DARK
                        elif cat == "horn":
                            rel = (px - fu) / max(1, fw)
                            base_c = HORN_LIGHT if rel > 0.6 else HORN_MID
                        elif cat == "spikes":
                            base_c = HORN_DARK
                        elif cat in ("leg", "foot", "arm", "claw"):
                            base_c = SCALE_DARK if fname == "down" else SCALE_MID
                        elif cat == "tail":
                            base_c = MAGMA_DARK if fname == "down" else SCALE_MID
                        elif cat == "flame_core":
                            base_c = FIRE_YELLOW if (px + py) % 2 == 0 else FIRE_ORANGE
                        elif cat == "flame_outer":
                            dist = math.sqrt((px - fu - fw/2)**2 + (py - fv - fh/2)**2)
                            base_c = FIRE_ORANGE if dist < fw * 0.3 else FIRE_RED
                        elif cat == "wing_arm":
                            base_c = SCALE_DARK
                        elif cat == "wing_membrane":
                            # Top (up) is dark dragon leather, bottom (down) is warm ember leather!
                            if fname == "down":
                                base_c = MAGMA_DARK if (px + py) % 5 == 0 else MEMBRANE_MID
                            else:
                                base_c = MEMBRANE_MID if (px * 2 + py * 3) % 7 != 0 else MEMBRANE_DARK
                        else:
                            base_c = SCALE_MID

                        col = shade(base_c, n)
                        tex.putpixel((px, py), col)

            if c["name"] == "cranium":
                fu_w, fv_w = u0, v0 + sz
                fu_e, fv_e = u0 + sz + sx, v0 + sz
                for ex in range(4, 8):
                    for ey in range(3, 7):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_GOLD)
                for ey in range(3, 7):
                    tex.putpixel((fu_w + 6, fv_w + ey), EYE_PUPIL)
                    tex.putpixel((fu_e + sz - 1 - 6, fv_e + ey), EYE_PUPIL)
            elif c["name"] == "jaw":
                fu_n, fv_n = u0 + sz, v0 + sz
                for fx in [2, 4, fw - 5, fw - 3]:
                    if 0 <= fx < fw:
                        tex.putpixel((fu_n + fx, fv_n), FANG_COLOR)

adult_anims = {
    "animation.flamefang_adult.idle": {
        "loop": True,
        "animation_length": 4.5,
        "bones": {
            "body": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]}, "position": {"0.0": [0, 0, 0], "2.25": [0, -0.6, 0], "4.5": [0, 0, 0]}},
            "neck": {"rotation": {"0.0": [0, 0, 0], "2.25": [2.5, 0, 0], "4.5": [0, 0, 0]}},
            "neck_upper": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "2.25": [-1.0, 0, 0], "4.5": [0, 0, 0]}},
            # Aerodynamic wings gently flex and breathe horizontally
            "wing_left": {"rotation": {"0.0": [0, 0, -4.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -4.0]}},
            "wing_left_mid": {"rotation": {"0.0": [0, 0, 3.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 3.0]}},
            "wing_left_outer": {"rotation": {"0.0": [0, 0, -2.0], "2.25": [0, 0, 0], "4.5": [0, 0, -2.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, 4.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 4.0]}},
            "wing_right_mid": {"rotation": {"0.0": [0, 0, -3.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -3.0]}},
            "wing_right_outer": {"rotation": {"0.0": [0, 0, 2.0], "2.25": [0, 0, 0], "4.5": [0, 0, 2.0]}},
            "tail_base": {"rotation": {"0.0": [0, -3.0, 0], "2.25": [0, 3.0, 0], "4.5": [0, -3.0, 0]}},
            "tail_mid": {"rotation": {"0.0": [0, -6.0, 0], "2.25": [0, 6.0, 0], "4.5": [0, -6.0, 0]}},
            "tail_tip": {"rotation": {"0.0": [0, -10.0, 0], "2.25": [0, 10.0, 0], "4.5": [0, -10.0, 0]}},
            "tail_flame": {
                "rotation": {"0.0": [0, 0, -10.0], "1.1": [5.0, 8.0, 0], "2.25": [0, 0, 10.0], "3.4": [-5.0, -8.0, 0], "4.5": [0, 0, -10.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.1": [1.15, 1.25, 1.15], "2.25": [0.95, 0.9, 0.95], "3.4": [1.2, 1.3, 1.2], "4.5": [1.0, 1.0, 1.0]}
            }
        }
    },
    "animation.flamefang_adult.walk": {
        "loop": True,
        "animation_length": 2.0,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.5": [0, 0.8, 0], "1.0": [0, 0, 0], "1.5": [0, 0.8, 0], "2.0": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [2.0, 0, -2.5], "0.5": [0.5, 1.5, 0], "1.0": [2.0, 0, 2.5], "1.5": [0.5, -1.5, 0], "2.0": [2.0, 0, -2.5]}},
            "leg_left": {"rotation": {"0.0": [-24.0, 0, 0], "0.5": [0, 0, 0], "1.0": [24.0, 0, 0], "1.5": [0, 0, 0], "2.0": [-24.0, 0, 0]}},
            "leg_left_shin": {"rotation": {"0.0": [10.0, 0, 0], "0.5": [-15.0, 0, 0], "1.0": [5.0, 0, 0], "1.5": [0, 0, 0], "2.0": [10.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [24.0, 0, 0], "0.5": [0, 0, 0], "1.0": [-24.0, 0, 0], "1.5": [0, 0, 0], "2.0": [24.0, 0, 0]}},
            "leg_right_shin": {"rotation": {"0.0": [5.0, 0, 0], "0.5": [0, 0, 0], "1.0": [10.0, 0, 0], "1.5": [-15.0, 0, 0], "2.0": [5.0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, 8.0, 0], "1.0": [0, -8.0, 0], "2.0": [0, 8.0, 0]}},
            "tail_mid": {"rotation": {"0.0": [0, 14.0, 0], "1.0": [0, -14.0, 0], "2.0": [0, 14.0, 0]}},
            "tail_tip": {"rotation": {"0.0": [0, 20.0, 0], "1.0": [0, -20.0, 0], "2.0": [0, 20.0, 0]}}
        }
    },
    "animation.flamefang_adult.fly_flap": {
        "loop": True,
        "animation_length": 1.2,
        "bones": {
            "body": {"rotation": {"0.0": [14.0, 0, 0], "0.35": [8.0, 0, 0], "0.7": [18.0, 0, 0], "1.2": [14.0, 0, 0]}, "position": {"0.0": [0, 0, 0], "0.35": [0, 2.5, 0], "0.7": [0, -1.8, 0], "1.2": [0, 0, 0]}},
            # Powerful downstrokes and upstrokes across the 3 articulated wing joints
            "wing_left": {"rotation": {"0.0": [0, 0, 22.0], "0.35": [0, 0, -45.0], "0.7": [0, 0, 38.0], "1.2": [0, 0, 22.0]}},
            "wing_left_mid": {"rotation": {"0.0": [0, 0, -10.0], "0.35": [0, 0, 25.0], "0.7": [0, 0, -18.0], "1.2": [0, 0, -10.0]}},
            "wing_left_outer": {"rotation": {"0.0": [0, 0, -15.0], "0.35": [0, 0, 30.0], "0.7": [0, 0, -25.0], "1.2": [0, 0, -15.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, -22.0], "0.35": [0, 0, 45.0], "0.7": [0, 0, -38.0], "1.2": [0, 0, -22.0]}},
            "wing_right_mid": {"rotation": {"0.0": [0, 0, 10.0], "0.35": [0, 0, -25.0], "0.7": [0, 0, 18.0], "1.2": [0, 0, 10.0]}},
            "wing_right_outer": {"rotation": {"0.0": [0, 0, 15.0], "0.35": [0, 0, -30.0], "0.7": [0, 0, 25.0], "1.2": [0, 0, 15.0]}},
            "leg_left": {"rotation": {"0.0": [35.0, 0, 4.0], "0.6": [45.0, 0, 4.0], "1.2": [35.0, 0, 4.0]}},
            "leg_right": {"rotation": {"0.0": [35.0, 0, -4.0], "0.6": [45.0, 0, -4.0], "1.2": [35.0, 0, -4.0]}},
            "tail_flame": {"scale": {"0.0": [1.1, 1.25, 1.1], "0.6": [1.35, 1.5, 1.25], "1.2": [1.1, 1.25, 1.1]}}
        }
    }
}

# ===========================================================================
# 2. FLAMEFANG JUVENIL (Athletic, Aerodynamic Horizontal Wings)
# ===========================================================================

juv_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 18, 0],
        "cubes": [
            {"name": "torso_main", "origin": [-8, 12, -8], "size": [16, 14, 18], "category": "torso"},
            {"name": "chest_plate", "origin": [-7, 14, -11], "size": [14, 10, 3], "category": "chest"},
            {"name": "dorsal_spikes", "origin": [-1, 26, -7], "size": [2, 3, 16], "category": "spikes"}
        ]
    },
    {
        "name": "arm_left",
        "parent": "body",
        "pivot": [8, 16, -6],
        "cubes": [{"name": "arm_left_cube", "origin": [7, 10, -7], "size": [3, 8, 3], "category": "arm", "uv_group": "juv_arm"}]
    },
    {
        "name": "arm_right",
        "parent": "body",
        "pivot": [-8, 16, -6],
        "cubes": [{"name": "arm_right_cube", "origin": [-10, 10, -7], "size": [3, 8, 3], "category": "arm", "uv_group": "juv_arm"}]
    },
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 22, -6],
        "cubes": [{"name": "neck_main", "origin": [-4, 20, -12], "size": [8, 12, 8], "category": "neck"}]
    },
    {
        "name": "head",
        "parent": "neck",
        "pivot": [0, 30, -10],
        "cubes": [
            {"name": "cranium", "origin": [-5, 28, -18], "size": [10, 8, 10], "category": "head"},
            {"name": "snout", "origin": [-4, 28, -26], "size": [8, 5, 8], "category": "snout"},
            {"name": "jaw", "origin": [-3.5, 25, -25], "size": [7, 3, 8], "category": "jaw"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 36, -12],
        "cubes": [
            {"name": "horn_left", "origin": [3, 35, -14], "size": [2, 3, 8], "category": "horn", "uv_group": "juv_horns"},
            {"name": "horn_right", "origin": [-5, 35, -14], "size": [2, 3, 8], "category": "horn", "uv_group": "juv_horns"}
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [8, 16, 4],
        "cubes": [
            {"name": "thigh_left", "origin": [6, 8, 2], "size": [5, 10, 6], "category": "leg", "uv_group": "juv_thigh"},
            {"name": "shin_left", "origin": [6.5, 2, 2.5], "size": [4, 6, 5], "category": "leg", "uv_group": "juv_shin"},
            {"name": "foot_left", "origin": [6, 0, -1], "size": [5, 2, 7], "category": "foot", "uv_group": "juv_foot"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-8, 16, 4],
        "cubes": [
            {"name": "thigh_right", "origin": [-11, 8, 2], "size": [5, 10, 6], "category": "leg", "uv_group": "juv_thigh"},
            {"name": "shin_right", "origin": [-10.5, 2, 2.5], "size": [4, 6, 5], "category": "leg", "uv_group": "juv_shin"},
            {"name": "foot_right", "origin": [-11, 0, -1], "size": [5, 2, 7], "category": "foot", "uv_group": "juv_foot"}
        ]
    },
    {
        "name": "tail_base",
        "parent": "body",
        "pivot": [0, 16, 10],
        "cubes": [{"name": "tail_base_cube", "origin": [-4, 12, 10], "size": [8, 8, 16], "category": "tail"}]
    },
    {
        "name": "tail_mid",
        "parent": "tail_base",
        "pivot": [0, 16, 26],
        "cubes": [{"name": "tail_mid_cube", "origin": [-3, 13, 26], "size": [6, 6, 16], "category": "tail"}]
    },
    {
        "name": "tail_tip",
        "parent": "tail_mid",
        "pivot": [0, 16, 42],
        "cubes": [{"name": "tail_tip_cube", "origin": [-2, 14, 42], "size": [4, 4, 14], "category": "tail"}]
    },
    {
        "name": "tail_flame",
        "parent": "tail_tip",
        "pivot": [0, 16, 56],
        "cubes": [
            {"name": "flame_core", "origin": [-2.5, 13, 55], "size": [5, 6, 8], "category": "flame_core"},
            {"name": "flame_outer", "origin": [-4, 12, 57], "size": [8, 8, 8], "category": "flame_outer"}
        ]
    },
    # Horizontal Aerodynamic Juvenile Wings
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [8, 22, -2],
        "cubes": [
            {"name": "wing_left_bone", "origin": [8, 20, -4], "size": [20, 3, 4], "category": "wing_arm", "uv_group": "juv_wbone1"},
            {"name": "wing_left_membrane_inner", "origin": [8, 21, 0], "size": [18, 1, 12], "category": "wing_membrane", "uv_group": "juv_wmem1"}
        ]
    },
    {
        "name": "wing_left_mid",
        "parent": "wing_left",
        "pivot": [28, 22, 0],
        "cubes": [
            {"name": "wing_left_forearm", "origin": [28, 20, -2], "size": [24, 3, 4], "category": "wing_arm", "uv_group": "juv_wbone2"},
            {"name": "wing_left_membrane_outer", "origin": [26, 21, 2], "size": [24, 1, 16], "category": "wing_membrane", "uv_group": "juv_wmem2"}
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-8, 22, -2],
        "cubes": [
            {"name": "wing_right_bone", "origin": [-28, 20, -4], "size": [20, 3, 4], "category": "wing_arm", "uv_group": "juv_wbone1"},
            {"name": "wing_right_membrane_inner", "origin": [-26, 21, 0], "size": [18, 1, 12], "category": "wing_membrane", "uv_group": "juv_wmem1"}
        ]
    },
    {
        "name": "wing_right_mid",
        "parent": "wing_right",
        "pivot": [-28, 22, 0],
        "cubes": [
            {"name": "wing_right_forearm", "origin": [-52, 20, -2], "size": [24, 3, 4], "category": "wing_arm", "uv_group": "juv_wbone2"},
            {"name": "wing_right_membrane_outer", "origin": [-50, 21, 2], "size": [24, 1, 16], "category": "wing_membrane", "uv_group": "juv_wmem2"}
        ]
    }
]

def paint_juv_texture(tex, bones_def, tex_w, tex_h):
    SCALE_DARK = (28, 26, 32, 255)
    SCALE_MID = (38, 35, 46, 255)
    BELLY_MID = (165, 40, 32, 255)
    BELLY_LIGHT = (195, 60, 42, 255)
    HORN_MID = (85, 72, 60, 255)
    FIRE_YELLOW = (255, 230, 80, 255)
    FIRE_ORANGE = (255, 125, 18, 255)
    FIRE_RED = (215, 42, 16, 255)
    MEMBRANE_MID = (90, 30, 24, 255)
    EYE_GOLD = (255, 195, 12, 255)
    EYE_PUPIL = (14, 10, 10, 255)

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
                for py in range(int(fv), int(fv + fh)):
                    for px in range(int(fu), int(fu + fw)):
                        n = noise(px, py, 14)
                        if cat == "torso":
                            base_c = BELLY_MID if fname == "down" else SCALE_MID
                        elif cat == "chest":
                            base_c = BELLY_LIGHT if (px + py) % 4 == 0 else BELLY_MID
                        elif cat == "head":
                            base_c = SCALE_MID
                        elif cat in ("snout", "jaw"):
                            base_c = SCALE_DARK
                        elif cat == "horn":
                            base_c = HORN_MID
                        elif cat == "tail":
                            base_c = BELLY_MID if fname == "down" else SCALE_MID
                        elif cat == "flame_core":
                            base_c = FIRE_YELLOW
                        elif cat == "flame_outer":
                            base_c = FIRE_ORANGE if (px + py) % 2 == 0 else FIRE_RED
                        elif cat == "wing_membrane":
                            base_c = MEMBRANE_MID
                        else:
                            base_c = SCALE_MID

                        col = shade(base_c, n)
                        tex.putpixel((px, py), col)

            if c["name"] == "cranium":
                fu_w, fv_w = u0, v0 + sz
                fu_e, fv_e = u0 + sz + sx, v0 + sz
                for ex in range(2, 5):
                    for ey in range(2, 5):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_GOLD)
                tex.putpixel((fu_w + 3, fv_w + 3), EYE_PUPIL)
                tex.putpixel((fu_e + sz - 1 - 3, fv_e + 3), EYE_PUPIL)

juv_anims = {
    "animation.flamefang_juvenile.idle": {
        "loop": True,
        "animation_length": 3.0,
        "bones": {
            "body": {"rotation": {"0.0": [0, 0, 0], "1.5": [-2.0, 0, 0], "3.0": [0, 0, 0]}, "position": {"0.0": [0, 0, 0], "1.5": [0, -0.4, 0], "3.0": [0, 0, 0]}},
            "neck": {"rotation": {"0.0": [0, 0, 0], "1.5": [2.5, 0, 0], "3.0": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [-2.0, 0, 0], "3.0": [0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, -5.0], "1.5": [0, 0, -1.0], "3.0": [0, 0, -5.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, 5.0], "1.5": [0, 0, 1.0], "3.0": [0, 0, 5.0]}},
            "tail_base": {"rotation": {"0.0": [0, -5.0, 0], "1.5": [0, 5.0, 0], "3.0": [0, -5.0, 0]}},
            "tail_flame": {"scale": {"0.0": [1.0, 1.0, 1.0], "1.5": [1.2, 1.3, 1.2], "3.0": [1.0, 1.0, 1.0]}}
        }
    },
    "animation.flamefang_juvenile.walk": {
        "loop": True,
        "animation_length": 1.4,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.35": [0, 0.6, 0], "0.7": [0, 0, 0], "1.05": [0, 0.6, 0], "1.4": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [2.0, 0, -2.0], "0.7": [2.0, 0, 2.0], "1.4": [2.0, 0, -2.0]}},
            "leg_left": {"rotation": {"0.0": [-22.0, 0, 0], "0.7": [22.0, 0, 0], "1.4": [-22.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [22.0, 0, 0], "0.7": [-22.0, 0, 0], "1.4": [22.0, 0, 0]}}
        }
    },
    "animation.flamefang_juvenile.fly_flap": {
        "loop": True,
        "animation_length": 0.8,
        "bones": {
            "body": {"rotation": {"0.0": [12.0, 0, 0], "0.4": [16.0, 0, 0], "0.8": [12.0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, 25.0], "0.25": [0, 0, -45.0], "0.5": [0, 0, 35.0], "0.8": [0, 0, 25.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, -25.0], "0.25": [0, 0, 45.0], "0.5": [0, 0, -35.0], "0.8": [0, 0, -25.0]}}
        }
    }
}

# ===========================================================================
# 3. FLAMEFANG HATCHLING (Chibi Baby with Cute Horizontal Wings)
# ===========================================================================

hatch_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 7, 0],
        "cubes": [
            {"name": "torso", "origin": [-4, 4, -4], "size": [8, 7, 9], "category": "torso"},
            {"name": "belly", "origin": [-3.5, 4.5, -5.5], "size": [7, 5, 2], "category": "chest"}
        ]
    },
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 8, -3],
        "cubes": [{"name": "neck_main", "origin": [-2.5, 7, -6], "size": [5, 4, 4], "category": "neck"}]
    },
    {
        "name": "head",
        "parent": "neck",
        "pivot": [0, 9, -5],
        "cubes": [
            {"name": "cranium", "origin": [-4, 8, -10], "size": [8, 7, 7], "category": "head"},
            {"name": "snout", "origin": [-3, 8, -13], "size": [6, 3, 3], "category": "snout"}
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 15, -7],
        "cubes": [
            {"name": "horn_left", "origin": [2, 14, -8], "size": [1.5, 2, 2], "category": "horn", "uv_group": "horn_nubs"},
            {"name": "horn_right", "origin": [-3.5, 14, -8], "size": [1.5, 2, 2], "category": "horn", "uv_group": "horn_nubs"}
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [4, 5, 2],
        "cubes": [
            {"name": "thigh_left", "origin": [3, 2, 1], "size": [3, 4, 4], "category": "leg", "uv_group": "hatch_leg"},
            {"name": "foot_left", "origin": [3, 0, 0], "size": [3, 2, 4], "category": "foot", "uv_group": "hatch_foot"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-4, 5, 2],
        "cubes": [
            {"name": "thigh_right", "origin": [-6, 2, 1], "size": [3, 4, 4], "category": "leg", "uv_group": "hatch_leg"},
            {"name": "foot_right", "origin": [-6, 0, 0], "size": [3, 2, 4], "category": "foot", "uv_group": "hatch_foot"}
        ]
    },
    {
        "name": "tail_base",
        "parent": "body",
        "pivot": [0, 6, 5],
        "cubes": [{"name": "tail", "origin": [-2, 5, 5], "size": [4, 4, 7], "category": "tail"}]
    },
    {
        "name": "tail_flame",
        "parent": "tail_base",
        "pivot": [0, 6, 12],
        "cubes": [{"name": "flame", "origin": [-1.5, 5, 12], "size": [3, 4, 4], "category": "flame_core"}]
    },
    # Horizontal cute little baby wings (Y thickness = 1, Z depth = 6 extending back)
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [4, 8, -2],
        "cubes": [{"name": "wing_left_cube", "origin": [4, 7.5, -2], "size": [8, 1, 6], "category": "wing_membrane", "uv_group": "hatch_wing"}]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-4, 8, -2],
        "cubes": [{"name": "wing_right_cube", "origin": [-12, 7.5, -2], "size": [8, 1, 6], "category": "wing_membrane", "uv_group": "hatch_wing"}]
    }
]

def paint_hatch_texture(tex, bones_def, tex_w, tex_h):
    SCALE_MID = (48, 44, 56, 255)
    SCALE_LIGHT = (65, 60, 75, 255)
    BELLY_WARM = (210, 75, 55, 255)
    BELLY_SOFT = (235, 105, 80, 255)
    HORN_CUTE = (120, 105, 90, 255)
    FIRE_YELLOW = (255, 240, 110, 255)
    FIRE_ORANGE = (255, 140, 30, 255)
    EYE_GOLD = (255, 210, 20, 255)
    EYE_SHINE = (255, 255, 240, 255)
    EYE_PUPIL = (25, 18, 15, 255)

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
                for py in range(int(fv), int(fv + fh)):
                    for px in range(int(fu), int(fu + fw)):
                        n = noise(px, py, 10)
                        if cat == "torso":
                            base_c = BELLY_WARM if fname == "down" else SCALE_MID
                        elif cat == "chest":
                            base_c = BELLY_SOFT
                        elif cat == "head":
                            base_c = SCALE_MID
                        elif cat == "snout":
                            base_c = SCALE_LIGHT
                        elif cat == "horn":
                            base_c = HORN_CUTE
                        elif cat == "tail":
                            base_c = BELLY_WARM if fname == "down" else SCALE_MID
                        elif cat == "flame_core":
                            base_c = FIRE_YELLOW if (px + py) % 2 == 0 else FIRE_ORANGE
                        elif cat == "wing_membrane":
                            base_c = BELLY_WARM
                        else:
                            base_c = SCALE_MID

                        col = shade(base_c, n)
                        tex.putpixel((px, py), col)

            if c["name"] == "cranium":
                fu_w, fv_w = u0, v0 + sz
                fu_e, fv_e = u0 + sz + sx, v0 + sz
                for ex in range(1, 5):
                    for ey in range(1, 5):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_GOLD)
                for ex in range(2, 4):
                    for ey in range(2, 4):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_PUPIL)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_PUPIL)
                tex.putpixel((fu_w + 2, fv_w + 1), EYE_SHINE)
                tex.putpixel((fu_e + sz - 1 - 2, fv_e + 1), EYE_SHINE)

hatch_anims = {
    "animation.flamefang_hatchling.idle": {
        "loop": True,
        "animation_length": 2.5,
        "bones": {
            "body": {"rotation": {"0.0": [0, 0, 0], "1.25": [-2.0, 0, 0], "2.5": [0, 0, 0]}, "position": {"0.0": [0, 0, 0], "1.25": [0, -0.3, 0], "2.5": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "0.8": [5.0, 10.0, 5.0], "1.6": [2.0, -8.0, -3.0], "2.5": [0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, -8.0, 0], "1.25": [0, 8.0, 0], "2.5": [0, -8.0, 0]}},
            "tail_flame": {"scale": {"0.0": [1.0, 1.0, 1.0], "1.25": [1.2, 1.3, 1.2], "2.5": [1.0, 1.0, 1.0]}}
        }
    },
    "animation.flamefang_hatchling.walk": {
        "loop": True,
        "animation_length": 1.0,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.25": [0, 0.4, 0], "0.5": [0, 0, 0], "0.75": [0, 0.4, 0], "1.0": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [0, 0, -3.0], "0.5": [0, 0, 3.0], "1.0": [0, 0, -3.0]}},
            "head": {"rotation": {"0.0": [0, 0, 3.0], "0.5": [0, 0, -3.0], "1.0": [0, 0, 3.0]}},
            "leg_left": {"rotation": {"0.0": [-20.0, 0, 0], "0.5": [20.0, 0, 0], "1.0": [-20.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [20.0, 0, 0], "0.5": [-20.0, 0, 0], "1.0": [20.0, 0, 0]}}
        }
    },
    "animation.flamefang_hatchling.fly_flap": {
        "loop": True,
        "animation_length": 0.5,
        "bones": {
            "body": {"rotation": {"0.0": [10.0, 0, 0], "0.25": [15.0, 0, 0], "0.5": [10.0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, 35.0], "0.25": [0, 0, -50.0], "0.5": [0, 0, 35.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, -35.0], "0.25": [0, 0, 50.0], "0.5": [0, 0, -35.0]}}
        }
    }
}

# ===========================================================================
# 4. FLAMEFANG EGG (3D Volumetric Egg matching Concept Art)
# ===========================================================================

egg_bones = [
    {"name": "root", "pivot": [0, 0, 0]},
    {
        "name": "egg",
        "parent": "root",
        "pivot": [0, 10, 0],
        "cubes": [
            # Tier 1 (Bottom base rim)
            {"name": "tier_base", "origin": [-4, 0, -4], "size": [8, 2, 8], "category": "egg_base"},
            # Tier 2 (Lower swell)
            {"name": "tier_lower", "origin": [-6, 2, -6], "size": [12, 3, 12], "category": "egg_core"},
            # Tier 3 (Maximum girth equator)
            {"name": "tier_equator", "origin": [-7.5, 5, -7.5], "size": [15, 5, 15], "category": "egg_core"},
            # Tier 4 (Mid body)
            {"name": "tier_mid", "origin": [-7, 10, -7], "size": [14, 4, 14], "category": "egg_core"},
            # Tier 5 (Upper taper)
            {"name": "tier_upper", "origin": [-6, 14, -6], "size": [12, 4, 12], "category": "egg_core"},
            # Tier 6 (Shoulder)
            {"name": "tier_shoulder", "origin": [-4.5, 18, -4.5], "size": [9, 3, 9], "category": "egg_core"},
            # Tier 7 (Top dome crown)
            {"name": "tier_crown", "origin": [-3, 21, -3], "size": [6, 2, 6], "category": "egg_base"},
            # 3D Raised Obsidian Rock Plates (Volumetric Cobblestone tiles from concept art)
            {"name": "plate_front_waist", "origin": [-5, 6, -8], "size": [10, 4, 1], "category": "obsidian_plate", "uv_group": "plate_waist"},
            {"name": "plate_back_waist", "origin": [-5, 6, 7], "size": [10, 4, 1], "category": "obsidian_plate", "uv_group": "plate_waist"},
            {"name": "plate_left_waist", "origin": [7, 6, -5], "size": [1, 4, 10], "category": "obsidian_plate", "uv_group": "plate_waist_side"},
            {"name": "plate_right_waist", "origin": [-8, 6, -5], "size": [1, 4, 10], "category": "obsidian_plate", "uv_group": "plate_waist_side"},
            {"name": "plate_mid_fl", "origin": [2.5, 11, -7.5], "size": [4, 3, 1], "category": "obsidian_plate", "uv_group": "plate_mid"},
            {"name": "plate_mid_fr", "origin": [-6.5, 11, -7.5], "size": [4, 3, 1], "category": "obsidian_plate", "uv_group": "plate_mid"},
            {"name": "plate_mid_bl", "origin": [2.5, 11, 6.5], "size": [4, 3, 1], "category": "obsidian_plate", "uv_group": "plate_mid"},
            {"name": "plate_mid_br", "origin": [-6.5, 11, 6.5], "size": [4, 3, 1], "category": "obsidian_plate", "uv_group": "plate_mid"},
            {"name": "plate_top_front", "origin": [-3.5, 15, -6.5], "size": [7, 3, 1], "category": "obsidian_plate", "uv_group": "plate_top"},
            {"name": "plate_top_back", "origin": [-3.5, 15, 5.5], "size": [7, 3, 1], "category": "obsidian_plate", "uv_group": "plate_top"}
        ]
    }
]

def paint_egg_texture(tex, bones_def, tex_w, tex_h):
    # Palette matching flamefang_egg_concept.jpg
    OBSIDIAN_DEEP = (22, 23, 28, 255)
    OBSIDIAN_MID = (38, 41, 50, 255)
    OBSIDIAN_LIGHT = (55, 60, 72, 255)
    OBSIDIAN_SHINE = (75, 82, 98, 255)
    MAGMA_FISSURE_HOT = (255, 235, 75, 255)
    MAGMA_FISSURE_MID = (255, 125, 20, 255)
    MAGMA_FISSURE_EDGE = (210, 42, 14, 255)
    MAGMA_GLOW = (120, 20, 10, 255)

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
                for py in range(int(fv), int(fv + fh)):
                    for px in range(int(fu), int(fu + fw)):
                        n = noise(px, py, 12)
                        if cat in ("egg_core", "egg_base"):
                            # Core egg body: dark obsidian basalt tiles with glowing magma veins between them!
                            is_fissure_center = ((px * 3 + py * 7) % 13 == 0) or ((px * 5 - py * 2) % 17 == 0)
                            is_fissure_rim = ((px * 3 + py * 7) % 13 in (1, 12)) or ((px * 5 - py * 2) % 17 in (1, 16))

                            if is_fissure_center:
                                base_c = MAGMA_FISSURE_HOT if (px + py) % 3 == 0 else MAGMA_FISSURE_MID
                            elif is_fissure_rim:
                                base_c = MAGMA_FISSURE_EDGE
                            else:
                                # Obsidian plate face
                                base_c = OBSIDIAN_MID if (px + py) % 4 != 0 else OBSIDIAN_LIGHT
                        elif cat == "obsidian_plate":
                            # Protruding 3D rock plates: dark basalt with highlight edges
                            rel_x = (px - fu)
                            rel_y = (py - fv)
                            is_edge = (rel_x == 0 or rel_x == fw - 1 or rel_y == 0 or rel_y == fh - 1)
                            if is_edge:
                                base_c = OBSIDIAN_SHINE if rel_y == 0 else OBSIDIAN_DEEP
                            else:
                                base_c = OBSIDIAN_MID if (px * 3 + py) % 5 != 0 else OBSIDIAN_LIGHT
                        else:
                            base_c = OBSIDIAN_MID

                        col = shade(base_c, n)
                        tex.putpixel((px, py), col)

egg_anims = {
    "animation.flamefang_egg.idle": {
        "loop": True,
        "animation_length": 3.0,
        "bones": {
            "egg": {
                # Gentle thermal pulsation / breathing of magical embryo
                "scale": {
                    "0.0": [1.0, 1.0, 1.0],
                    "1.5": [1.025, 1.035, 1.025],
                    "3.0": [1.0, 1.0, 1.0]
                }
            }
        }
    },
    "animation.flamefang_egg.wobble": {
        "loop": True,
        "animation_length": 1.2,
        "bones": {
            "egg": {
                # Pre-hatch wobble / shake
                "rotation": {
                    "0.0": [0, 0, 0],
                    "0.2": [0, 0, -5.0],
                    "0.4": [0, 0, 6.0],
                    "0.6": [0, 0, -4.0],
                    "0.8": [0, 0, 3.0],
                    "1.2": [0, 0, 0]
                },
                "position": {
                    "0.0": [0, 0, 0],
                    "0.3": [0, 0.4, 0],
                    "0.6": [0, 0.2, 0],
                    "1.2": [0, 0, 0]
                }
            }
        }
    }
}

# ===========================================================================
# MAIN RUNNER
# ===========================================================================
if __name__ == "__main__":
    print("STARTING COMPLETE FLAMEFANG REBUILD & EGG CREATION...")

    # 1. Adult Colossal (256x256) -> flamefang_adult_geckolib.bbmodel
    export_model("flamefang_adult", "flamefang_adult_geckolib.bbmodel", adult_bones, adult_anims, 256, 256, paint_adult_texture)

    # 2. Juvenil Athletic (256x256) -> flamefang_Juvenil_geckolib.bbmodel (exact required casing!)
    export_model("flamefang_juvenile", "flamefang_Juvenil_geckolib.bbmodel", juv_bones, juv_anims, 256, 256, paint_juv_texture, extra_geo_names=["flamefang.geo.json"])

    # 3. Hatchling Chibi (64x64) -> flamefang_hatchling_geckolib.bbmodel
    export_model("flamefang_hatchling", "flamefang_hatchling_geckolib.bbmodel", hatch_bones, hatch_anims, 64, 64, paint_hatch_texture)

    # 4. Dragon Egg 3D (128x128) -> flamefang_egg_geckolib.bbmodel
    export_model("flamefang_egg", "flamefang_egg_geckolib.bbmodel", egg_bones, egg_anims, 128, 128, paint_egg_texture)

    print("\n[ALL MODELS REBUILT AND EXPORTED WITH GECKOLIB FORMAT SUCCESSFULLY!]")
