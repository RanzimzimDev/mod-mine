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
# Common Texture Palette & Shading Helpers
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

# Shelf UV Packing algorithm
def pack_uvs(cubes_list, tex_w, tex_h, padding=1):
    # cubes_list: list of dicts with 'name', 'size', etc.
    # assigns c['uv'] = [u, v]
    # Unique footprints
    unique_items = []
    seen = set()
    for c in cubes_list:
        uv_group = c.get('uv_group', c['name'])
        if uv_group not in seen:
            seen.add(uv_group)
            sx, sy, sz = c['size']
            pw = 2 * (sx + sz)
            ph = sz + sy
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
                raise ValueError(f"Texture canvas ({tex_w}x{tex_h}) overflow while packing {gid} ({pw}x{ph}) at y={current_y}")

    for c in cubes_list:
        gid = c.get('uv_group', c['name'])
        c['uv'] = uv_map[gid]

    return uv_map

# ---------------------------------------------------------------------------
# Blockbench & GeckoLib Exporters
# ---------------------------------------------------------------------------
def export_stage(stage_id, bones_def, anims_def, tex_w, tex_h, painter_fn):
    print(f"\n==========================================")
    print(f"Generating stage: {stage_id} ({tex_w}x{tex_h})")
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

    tex_path = os.path.join(TEX_DIR, f"{stage_id}.png")
    tex_img.save(tex_path)
    print(f"Saved texture: {tex_path}")

    # 3. Export GeckoLib Geo JSON
    geo_data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": f"geometry.{stage_id}",
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

    geo_path = os.path.join(GEO_DIR, f"{stage_id}.geo.json")
    with open(geo_path, "w", encoding="utf-8") as f:
        json.dump(geo_data, f, indent=2)
    print(f"Saved geo JSON: {geo_path}")

    # 4. Export GeckoLib Animation JSON
    anim_data = {
        "format_version": "1.8.0",
        "animations": anims_def
    }
    anim_path = os.path.join(ANIM_DIR, f"{stage_id}.animation.json")
    with open(anim_path, "w", encoding="utf-8") as f:
        json.dump(anim_data, f, indent=2)
    print(f"Saved animations: {anim_path}")

    # 5. Export Blockbench .bbmodel
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

    # Animations for BBModel
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
            "model_format": "geckolib",
            "box_uv": True
        },
        "name": stage_id,
        "model_identifier": stage_id,
        "visible_box": [6, 6, 0],
        "resolution": {"width": tex_w, "height": tex_h},
        "elements": elements,
        "outliner": outliner,
        "textures": [
            {
                "type": "entity",
                "name": f"{stage_id}.png",
                "id": "0",
                "uuid": tex_uuid,
                "source": tex_base64
            }
        ],
        "animations": bb_animations
    }

    bbmodel_path = os.path.join(MODELS_DIR, f"{stage_id}.bbmodel")
    with open(bbmodel_path, "w", encoding="utf-8") as f:
        json.dump(bbmodel_data, f, indent=2)
    print(f"Saved Blockbench model: {bbmodel_path}")

# ===========================================================================
# 1. FLAMEFANG ADULT (COLOSSAL: 4-6 Blocks Tall, 14-16 Blocks Wingspan)
# ===========================================================================

adult_bones = [
    {
        "name": "root",
        "pivot": [0, 0, 0]
    },
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 36, 0],
        "cubes": [
            {
                "name": "torso_main",
                "origin": [-13, 26, -16],
                "size": [26, 22, 32],
                "category": "torso"
            },
            {
                "name": "chest_pectoral",
                "origin": [-11, 28, -22],
                "size": [22, 16, 6],
                "category": "chest"
            },
            {
                "name": "shoulder_blades",
                "origin": [-14, 40, -10],
                "size": [28, 6, 10],
                "category": "spikes"
            },
            {
                "name": "dorsal_ridge",
                "origin": [-2, 48, -14],
                "size": [4, 6, 26],
                "category": "spikes"
            }
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
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [13, 44, -6],
        "cubes": [
            {"name": "wing_left_bone1", "origin": [13, 41, -9], "size": [32, 6, 6], "category": "wing_arm", "uv_group": "wing_bone1"},
            {"name": "wing_left_membrane1", "origin": [14, 24, -6], "size": [30, 18, 1], "category": "wing_membrane", "uv_group": "wing_mem1"}
        ]
    },
    {
        "name": "wing_left_mid",
        "parent": "wing_left",
        "pivot": [45, 44, -6],
        "cubes": [
            {"name": "wing_left_bone2", "origin": [45, 41, -8.5], "size": [34, 5, 5], "category": "wing_arm", "uv_group": "wing_bone2"},
            {"name": "wing_left_membrane2", "origin": [46, 18, -6], "size": [32, 24, 1], "category": "wing_membrane", "uv_group": "wing_mem2"}
        ]
    },
    {
        "name": "wing_left_outer",
        "parent": "wing_left_mid",
        "pivot": [79, 44, -6],
        "cubes": [
            {"name": "wing_left_bone3", "origin": [79, 42, -8], "size": [36, 4, 4], "category": "wing_arm", "uv_group": "wing_bone3"},
            {"name": "wing_left_membrane3", "origin": [80, 15, -6], "size": [34, 28, 1], "category": "wing_membrane", "uv_group": "wing_mem3"}
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-13, 44, -6],
        "cubes": [
            {"name": "wing_right_bone1", "origin": [-45, 41, -9], "size": [32, 6, 6], "category": "wing_arm", "uv_group": "wing_bone1"},
            {"name": "wing_right_membrane1", "origin": [-44, 24, -6], "size": [30, 18, 1], "category": "wing_membrane", "uv_group": "wing_mem1"}
        ]
    },
    {
        "name": "wing_right_mid",
        "parent": "wing_right",
        "pivot": [-45, 44, -6],
        "cubes": [
            {"name": "wing_right_bone2", "origin": [-79, 41, -8.5], "size": [34, 5, 5], "category": "wing_arm", "uv_group": "wing_bone2"},
            {"name": "wing_right_membrane2", "origin": [-78, 18, -6], "size": [32, 24, 1], "category": "wing_membrane", "uv_group": "wing_mem2"}
        ]
    },
    {
        "name": "wing_right_outer",
        "parent": "wing_right_mid",
        "pivot": [-79, 44, -6],
        "cubes": [
            {"name": "wing_right_bone3", "origin": [-115, 42, -8], "size": [36, 4, 4], "category": "wing_arm", "uv_group": "wing_bone3"},
            {"name": "wing_right_membrane3", "origin": [-114, 15, -6], "size": [34, 28, 1], "category": "wing_membrane", "uv_group": "wing_mem3"}
        ]
    }
]

# Texture Painter for Adult
def paint_adult_texture(tex, bones_def, tex_w, tex_h):
    SCALE_DARK = (24, 22, 28, 255)
    SCALE_MID = (35, 32, 42, 255)
    SCALE_EDGE = (48, 44, 58, 255)
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
                                # Molten magma belly with yellow cracks
                                base_c = MAGMA_CORE if (px * 3 + py * 7) % 11 == 0 else MAGMA_MID
                            elif fname in ("west", "east"):
                                rel_y = (py - fv) / max(1, fh)
                                base_c = MAGMA_MID if rel_y > 0.65 else SCALE_MID
                            else:
                                base_c = SCALE_MID
                        elif cat == "chest":
                            # Heavy pectoral armor: magma veins
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
                            # Leathery veins
                            base_c = MEMBRANE_MID if (px * 2 + py * 3) % 7 != 0 else MEMBRANE_DARK
                        else:
                            base_c = SCALE_MID

                        col = shade(base_c, n)
                        tex.putpixel((px, py), col)

            # Details on specific cubes
            if c["name"] == "cranium":
                # Eye on west and east faces
                # west face: fu = u0, fv = v0 + sz, fw = sz, fh = sy
                fu_w, fv_w = u0, v0 + sz
                fu_e, fv_e = u0 + sz + sx, v0 + sz
                for ex in range(4, 8):
                    for ey in range(3, 7):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_GOLD)
                # Slit pupil
                for ey in range(3, 7):
                    tex.putpixel((fu_w + 6, fv_w + ey), EYE_PUPIL)
                    tex.putpixel((fu_e + sz - 1 - 6, fv_e + ey), EYE_PUPIL)
            elif c["name"] == "jaw":
                # Fangs protruding up
                fu_n, fv_n = u0 + sz, v0 + sz
                for fx in [2, 4, fw - 5, fw - 3]:
                    if 0 <= fx < fw:
                        tex.putpixel((fu_n + fx, fv_n), FANG_COLOR)

# Adult Animations
adult_anims = {
    "animation.flamefang_adult.idle": {
        "loop": True,
        "animation_length": 4.5,
        "bones": {
            "body": {
                "rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "2.25": [0, -0.6, 0], "4.5": [0, 0, 0]}
            },
            "neck": {
                "rotation": {"0.0": [0, 0, 0], "2.25": [2.5, 0, 0], "4.5": [0, 0, 0]}
            },
            "neck_upper": {
                "rotation": {"0.0": [0, 0, 0], "2.25": [-1.5, 0, 0], "4.5": [0, 0, 0]}
            },
            "head": {
                "rotation": {"0.0": [0, 0, 0], "2.25": [-1.0, 0, 0], "4.5": [0, 0, 0]}
            },
            "wing_left": {
                "rotation": {"0.0": [0, 0, -4.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -4.0]}
            },
            "wing_left_mid": {
                "rotation": {"0.0": [0, 0, 3.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 3.0]}
            },
            "wing_right": {
                "rotation": {"0.0": [0, 0, 4.0], "2.25": [0, 0, 1.0], "4.5": [0, 0, 4.0]}
            },
            "wing_right_mid": {
                "rotation": {"0.0": [0, 0, -3.0], "2.25": [0, 0, -1.0], "4.5": [0, 0, -3.0]}
            },
            "tail_base": {
                "rotation": {"0.0": [0, -3.0, 0], "2.25": [0, 3.0, 0], "4.5": [0, -3.0, 0]}
            },
            "tail_mid": {
                "rotation": {"0.0": [0, -6.0, 0], "2.25": [0, 6.0, 0], "4.5": [0, -6.0, 0]}
            },
            "tail_tip": {
                "rotation": {"0.0": [0, -10.0, 0], "2.25": [0, 10.0, 0], "4.5": [0, -10.0, 0]}
            },
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
            "root": {
                "position": {"0.0": [0, 0, 0], "0.5": [0, 0.8, 0], "1.0": [0, 0, 0], "1.5": [0, 0.8, 0], "2.0": [0, 0, 0]}
            },
            "body": {
                "rotation": {"0.0": [2.0, 0, -2.5], "0.5": [0.5, 1.5, 0], "1.0": [2.0, 0, 2.5], "1.5": [0.5, -1.5, 0], "2.0": [2.0, 0, -2.5]}
            },
            "neck": {
                "rotation": {"0.0": [0, 0, 2.0], "1.0": [0, 0, -2.0], "2.0": [0, 0, 2.0]}
            },
            "head": {
                "rotation": {"0.0": [-2.0, -2.0, 0], "1.0": [-2.0, 2.0, 0], "2.0": [-2.0, -2.0, 0]}
            },
            "leg_left": {
                "rotation": {"0.0": [-24.0, 0, 0], "0.5": [0, 0, 0], "1.0": [24.0, 0, 0], "1.5": [0, 0, 0], "2.0": [-24.0, 0, 0]}
            },
            "leg_left_shin": {
                "rotation": {"0.0": [10.0, 0, 0], "0.5": [-15.0, 0, 0], "1.0": [5.0, 0, 0], "1.5": [0, 0, 0], "2.0": [10.0, 0, 0]}
            },
            "leg_right": {
                "rotation": {"0.0": [24.0, 0, 0], "0.5": [0, 0, 0], "1.0": [-24.0, 0, 0], "1.5": [0, 0, 0], "2.0": [24.0, 0, 0]}
            },
            "leg_right_shin": {
                "rotation": {"0.0": [5.0, 0, 0], "0.5": [0, 0, 0], "1.0": [10.0, 0, 0], "1.5": [-15.0, 0, 0], "2.0": [5.0, 0, 0]}
            },
            "tail_base": {
                "rotation": {"0.0": [0, 8.0, 0], "1.0": [0, -8.0, 0], "2.0": [0, 8.0, 0]}
            },
            "tail_mid": {
                "rotation": {"0.0": [0, 14.0, 0], "1.0": [0, -14.0, 0], "2.0": [0, 14.0, 0]}
            },
            "tail_tip": {
                "rotation": {"0.0": [0, 20.0, 0], "1.0": [0, -20.0, 0], "2.0": [0, 20.0, 0]}
            },
            "tail_flame": {
                "rotation": {"0.0": [0, 15.0, -12.0], "1.0": [0, -15.0, 12.0], "2.0": [0, 15.0, -12.0]},
                "scale": {"0.0": [1.0, 1.1, 1.0], "1.0": [1.25, 1.35, 1.15], "2.0": [1.0, 1.1, 1.0]}
            }
        }
    },
    "animation.flamefang_adult.fly_flap": {
        "loop": True,
        "animation_length": 1.2,
        "bones": {
            "body": {
                "rotation": {"0.0": [14.0, 0, 0], "0.35": [8.0, 0, 0], "0.7": [18.0, 0, 0], "1.2": [14.0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "0.35": [0, 2.5, 0], "0.7": [0, -1.8, 0], "1.2": [0, 0, 0]}
            },
            "neck": {
                "rotation": {"0.0": [-8.0, 0, 0], "0.6": [-3.0, 0, 0], "1.2": [-8.0, 0, 0]}
            },
            "head": {
                "rotation": {"0.0": [-4.0, 0, 0], "0.6": [-8.0, 0, 0], "1.2": [-4.0, 0, 0]}
            },
            "wing_left": {
                "rotation": {"0.0": [0, 0, 22.0], "0.35": [0, 0, -45.0], "0.7": [0, 0, 38.0], "1.2": [0, 0, 22.0]}
            },
            "wing_left_mid": {
                "rotation": {"0.0": [0, 0, -10.0], "0.35": [0, 0, 25.0], "0.7": [0, 0, -18.0], "1.2": [0, 0, -10.0]}
            },
            "wing_left_outer": {
                "rotation": {"0.0": [0, 0, -15.0], "0.35": [0, 0, 30.0], "0.7": [0, 0, -25.0], "1.2": [0, 0, -15.0]}
            },
            "wing_right": {
                "rotation": {"0.0": [0, 0, -22.0], "0.35": [0, 0, 45.0], "0.7": [0, 0, -38.0], "1.2": [0, 0, -22.0]}
            },
            "wing_right_mid": {
                "rotation": {"0.0": [0, 0, 10.0], "0.35": [0, 0, -25.0], "0.7": [0, 0, 18.0], "1.2": [0, 0, 10.0]}
            },
            "wing_right_outer": {
                "rotation": {"0.0": [0, 0, 15.0], "0.35": [0, 0, -30.0], "0.7": [0, 0, 25.0], "1.2": [0, 0, 15.0]}
            },
            "leg_left": {
                "rotation": {"0.0": [35.0, 0, 4.0], "0.6": [45.0, 0, 4.0], "1.2": [35.0, 0, 4.0]}
            },
            "leg_right": {
                "rotation": {"0.0": [35.0, 0, -4.0], "0.6": [45.0, 0, -4.0], "1.2": [35.0, 0, -4.0]}
            },
            "tail_base": {
                "rotation": {"0.0": [-4.0, 0, 0], "0.6": [4.0, 0, 0], "1.2": [-4.0, 0, 0]}
            },
            "tail_tip": {
                "rotation": {"0.0": [-8.0, 0, 0], "0.6": [8.0, 0, 0], "1.2": [-8.0, 0, 0]}
            },
            "tail_flame": {
                "rotation": {"0.0": [-12.0, 0, 0], "0.6": [18.0, 0, 0], "1.2": [-12.0, 0, 0]},
                "scale": {"0.0": [1.1, 1.25, 1.1], "0.6": [1.35, 1.5, 1.25], "1.2": [1.1, 1.25, 1.1]}
            }
        }
    }
}

# ===========================================================================
# 2. FLAMEFANG JUVENILE (Athletic, 2 - 2.5 Blocks Tall)
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
        "cubes": [{"name": "arm_left_cube", "origin": [7, 10, -7], "size": [3, 8, 3], "category": "arm", "uv_group": "arm_cubes"}]
    },
    {
        "name": "arm_right",
        "parent": "body",
        "pivot": [-8, 16, -6],
        "cubes": [{"name": "arm_right_cube", "origin": [-10, 10, -7], "size": [3, 8, 3], "category": "arm", "uv_group": "arm_cubes"}]
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
            {"name": "horn_left", "origin": [3, 35, -14], "size": [2, 3, 8], "category": "horn", "uv_group": "horn_cubes"},
            {"name": "horn_right", "origin": [-5, 35, -14], "size": [2, 3, 8], "category": "horn", "uv_group": "horn_cubes"}
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [8, 16, 4],
        "cubes": [
            {"name": "thigh_left", "origin": [6, 8, 2], "size": [5, 10, 6], "category": "leg", "uv_group": "leg_thigh"},
            {"name": "shin_left", "origin": [6.5, 2, 2.5], "size": [4, 6, 5], "category": "leg", "uv_group": "leg_shin"},
            {"name": "foot_left", "origin": [6, 0, -1], "size": [5, 2, 7], "category": "foot", "uv_group": "leg_foot"}
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-8, 16, 4],
        "cubes": [
            {"name": "thigh_right", "origin": [-11, 8, 2], "size": [5, 10, 6], "category": "leg", "uv_group": "leg_thigh"},
            {"name": "shin_right", "origin": [-10.5, 2, 2.5], "size": [4, 6, 5], "category": "leg", "uv_group": "leg_shin"},
            {"name": "foot_right", "origin": [-11, 0, -1], "size": [5, 2, 7], "category": "foot", "uv_group": "leg_foot"}
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
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [8, 22, -2],
        "cubes": [
            {"name": "wing_left_bone", "origin": [8, 20, -4], "size": [22, 4, 4], "category": "wing_arm", "uv_group": "wing_bone"},
            {"name": "wing_left_membrane", "origin": [9, 8, -2.5], "size": [20, 14, 1], "category": "wing_membrane", "uv_group": "wing_mem"}
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-8, 22, -2],
        "cubes": [
            {"name": "wing_right_bone", "origin": [-30, 20, -4], "size": [22, 4, 4], "category": "wing_arm", "uv_group": "wing_bone"},
            {"name": "wing_right_membrane", "origin": [-29, 8, -2.5], "size": [20, 14, 1], "category": "wing_membrane", "uv_group": "wing_mem"}
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
            "body": {
                "rotation": {"0.0": [0, 0, 0], "1.5": [-2.0, 0, 0], "3.0": [0, 0, 0]},
                "position": {"0.0": [0, 0, 0], "1.5": [0, -0.4, 0], "3.0": [0, 0, 0]}
            },
            "neck": {"rotation": {"0.0": [0, 0, 0], "1.5": [2.5, 0, 0], "3.0": [0, 0, 0]}},
            "head": {"rotation": {"0.0": [0, 0, 0], "1.5": [-2.0, 0, 0], "3.0": [0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, -5.0], "1.5": [0, 0, -1.0], "3.0": [0, 0, -5.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, 5.0], "1.5": [0, 0, 1.0], "3.0": [0, 0, 5.0]}},
            "tail_base": {"rotation": {"0.0": [0, -5.0, 0], "1.5": [0, 5.0, 0], "3.0": [0, -5.0, 0]}},
            "tail_tip": {"rotation": {"0.0": [0, -10.0, 0], "1.5": [0, 10.0, 0], "3.0": [0, -10.0, 0]}},
            "tail_flame": {
                "rotation": {"0.0": [0, 0, -10.0], "1.5": [0, 0, 10.0], "3.0": [0, 0, -10.0]},
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.5": [1.2, 1.3, 1.2], "3.0": [1.0, 1.0, 1.0]}
            }
        }
    },
    "animation.flamefang_juvenile.walk": {
        "loop": True,
        "animation_length": 1.4,
        "bones": {
            "root": {"position": {"0.0": [0, 0, 0], "0.35": [0, 0.6, 0], "0.7": [0, 0, 0], "1.05": [0, 0.6, 0], "1.4": [0, 0, 0]}},
            "body": {"rotation": {"0.0": [2.0, 0, -2.0], "0.7": [2.0, 0, 2.0], "1.4": [2.0, 0, -2.0]}},
            "leg_left": {"rotation": {"0.0": [-22.0, 0, 0], "0.7": [22.0, 0, 0], "1.4": [-22.0, 0, 0]}},
            "leg_right": {"rotation": {"0.0": [22.0, 0, 0], "0.7": [-22.0, 0, 0], "1.4": [22.0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, 10.0, 0], "0.7": [0, -10.0, 0], "1.4": [0, 10.0, 0]}}
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
# 3. FLAMEFANG HATCHLING (Chibi Cute Baby: 0.8 - 1.0 Block Tall)
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
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [4, 9, -1],
        "cubes": [{"name": "wing_left_cube", "origin": [4, 6, -1], "size": [8, 6, 0.5], "category": "wing_membrane", "uv_group": "hatch_wing"}]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-4, 9, -1],
        "cubes": [{"name": "wing_right_cube", "origin": [-12, 6, -1], "size": [8, 6, 0.5], "category": "wing_membrane", "uv_group": "hatch_wing"}]
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
                # Big cute shiny puppy dragon eyes!
                fu_w, fv_w = u0, v0 + sz
                fu_e, fv_e = u0 + sz + sx, v0 + sz
                for ex in range(1, 5):
                    for ey in range(1, 5):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_GOLD)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_GOLD)
                # Big round pupil
                for ex in range(2, 4):
                    for ey in range(2, 4):
                        tex.putpixel((fu_w + ex, fv_w + ey), EYE_PUPIL)
                        tex.putpixel((fu_e + sz - 1 - ex, fv_e + ey), EYE_PUPIL)
                # Cute specular highlight shine
                tex.putpixel((fu_w + 2, fv_w + 1), EYE_SHINE)
                tex.putpixel((fu_e + sz - 1 - 2, fv_e + 1), EYE_SHINE)

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
                "rotation": {"0.0": [0, 0, 0], "0.8": [5.0, 10.0, 5.0], "1.6": [2.0, -8.0, -3.0], "2.5": [0, 0, 0]}
            },
            "tail_base": {
                "rotation": {"0.0": [0, -8.0, 0], "1.25": [0, 8.0, 0], "2.5": [0, -8.0, 0]}
            },
            "tail_flame": {
                "scale": {"0.0": [1.0, 1.0, 1.0], "1.25": [1.2, 1.3, 1.2], "2.5": [1.0, 1.0, 1.0]}
            }
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
            "leg_right": {"rotation": {"0.0": [20.0, 0, 0], "0.5": [-20.0, 0, 0], "1.0": [20.0, 0, 0]}},
            "tail_base": {"rotation": {"0.0": [0, 15.0, 0], "0.5": [0, -15.0, 0], "1.0": [0, 15.0, 0]}}
        }
    },
    "animation.flamefang_hatchling.fly_flap": {
        "loop": True,
        "animation_length": 0.5,
        "bones": {
            "body": {"rotation": {"0.0": [10.0, 0, 0], "0.25": [15.0, 0, 0], "0.5": [10.0, 0, 0]}},
            "wing_left": {"rotation": {"0.0": [0, 0, 35.0], "0.25": [0, 0, -50.0], "0.5": [0, 0, 35.0]}},
            "wing_right": {"rotation": {"0.0": [0, 0, -35.0], "0.25": [0, 0, 50.0], "0.5": [0, 0, -35.0]}},
            "tail_flame": {"scale": {"0.0": [1.1, 1.2, 1.1], "0.25": [1.3, 1.5, 1.3], "0.5": [1.1, 1.2, 1.1]}}
        }
    }
}

# ===========================================================================
# MAIN EXECUTION: GENERATE ALL 3 GROWTH STAGES
# ===========================================================================
if __name__ == "__main__":
    # 1. Adult Colossal (256x256)
    export_stage("flamefang_adult", adult_bones, adult_anims, 256, 256, paint_adult_texture)

    # 2. Juvenile Athletic (128x128)
    export_stage("flamefang_juvenile", juv_bones, juv_anims, 128, 128, paint_juv_texture)

    # 3. Hatchling Cute (64x64)
    export_stage("flamefang_hatchling", hatch_bones, hatch_anims, 64, 64, paint_hatch_texture)

    print("\n[SUCCESS] ALL 3 FLAMEFANG GROWTH STAGES GENERATED SUCCESSFULLY!")
