import json
import uuid
import base64
import os
from PIL import Image, ImageDraw

def uid():
    return str(uuid.uuid4())

# 1. Create a 64x64 Texture
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Dark charcoal/obsidian base for body
c_obsidian = (36, 32, 38, 255)
c_scales_dark = (48, 42, 52, 255)
c_belly = (160, 48, 38, 255)
c_belly_light = (200, 70, 50, 255)
c_wing = (110, 28, 28, 255)
c_wing_bone = (50, 40, 45, 255)
c_horn = (180, 160, 130, 255)
c_eye = (255, 215, 0, 255)
c_eye_pupil = (0, 0, 0, 255)
c_flame_orange = (255, 120, 20, 255)
c_flame_yellow = (255, 230, 80, 255)

# Fill general palette regions
draw.rectangle([0, 0, 63, 63], fill=c_obsidian)

# Belly texture area
draw.rectangle([16, 16, 32, 48], fill=c_belly)
draw.rectangle([18, 18, 30, 46], fill=c_belly_light)

# Wings texture area
draw.rectangle([32, 0, 63, 32], fill=c_wing)
draw.line([32, 0, 63, 0], fill=c_wing_bone, width=2)

# Horn texture
draw.rectangle([0, 0, 16, 8], fill=c_horn)

# Eyes
draw.rectangle([2, 10, 5, 12], fill=c_eye)
draw.point((4, 11), fill=c_eye_pupil)

# Flame
for y in range(48, 64):
    for x in range(48, 64):
        dist = ((x-56)**2 + (y-56)**2)**0.5
        if dist < 4:
            draw.point((x, y), fill=c_flame_yellow)
        elif dist < 7:
            draw.point((x, y), fill=c_flame_orange)

tex_path = r"D:\Mine\src\main\resources\assets\wingsofthewild\textures\entity\flamefang.png"
os.makedirs(os.path.dirname(tex_path), exist_ok=True)
img.save(tex_path)

import io
buf = io.BytesIO()
img.save(buf, format="PNG")
tex_base64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

# 2. Build Cubes and Outliner
elements = []

def add_cube(name, from_p, to_p, origin, uv=(0, 0)):
    c_uuid = uid()
    dx = to_p[0] - from_p[0]
    dy = to_p[1] - from_p[1]
    dz = to_p[2] - from_p[2]
    u, v = uv
    cube = {
        "name": name,
        "box_uv": True,
        "rescale": False,
        "locked": False,
        "from": from_p,
        "to": to_p,
        "autouv": 0,
        "color": 0,
        "origin": origin,
        "uv_offset": [u, v],
        "faces": {
            "north": {"uv": [u + dz, v + dz, u + dz + dx, v + dz + dy], "texture": 0},
            "east": {"uv": [u, v + dz, u + dz, v + dz + dy], "texture": 0},
            "south": {"uv": [u + dz + dx + dz, v + dz, u + dz + dx + dz + dx, v + dz + dy], "texture": 0},
            "west": {"uv": [u + dz + dx, v + dz, u + dz + dx + dz, v + dz + dy], "texture": 0},
            "up": {"uv": [u + dz + dx, v + dz, u + dz, v], "texture": 0},
            "down": {"uv": [u + dz + dx + dx, v, u + dz + dx, v + dz], "texture": 0}
        },
        "type": "cube",
        "uuid": c_uuid
    }
    elements.append(cube)
    return c_uuid

# Cubes
c_body = add_cube("body", [-5, 6, -6], [5, 17, 7], [0, 11, 0], (0, 0))
c_chest = add_cube("chest", [-4, 7, -8], [4, 15, -6], [0, 11, -7], (16, 20))
c_neck = add_cube("neck", [-3, 14, -10], [3, 22, -6], [0, 18, -8], (0, 24))
c_head = add_cube("head", [-4, 20, -16], [4, 27, -10], [0, 23, -13], (0, 36))
c_snout = add_cube("snout", [-3, 20, -21], [3, 24, -16], [0, 22, -18], (24, 36))

# Horns
c_horn_l = add_cube("horn_l", [2, 26, -12], [4, 31, -8], [3, 26, -10], (36, 0))
c_horn_r = add_cube("horn_r", [-4, 26, -12], [-2, 31, -8], [-3, 26, -10], (36, 0))

# Wings
c_w_arm_l = add_cube("wing_arm_l", [5, 14, -2], [17, 16, 0], [5, 15, -1], (0, 48))
c_w_mem_l = add_cube("wing_membrane_l", [5, 4, -1], [19, 14, 0], [5, 15, -1], (24, 0))

c_w_arm_r = add_cube("wing_arm_r", [-17, 14, -2], [-5, 16, 0], [-5, 15, -1], (0, 48))
c_w_mem_r = add_cube("wing_membrane_r", [-19, 4, -1], [-5, 14, 0], [-5, 15, -1], (24, 0))

# Legs
c_leg_l = add_cube("leg_l", [3, 0, 0], [7, 8, 4], [5, 8, 2], (40, 20))
c_foot_l = add_cube("foot_l", [3, 0, -3], [7, 3, 1], [5, 1, 0], (40, 32))

c_leg_r = add_cube("leg_r", [-7, 0, 0], [-3, 8, 4], [-5, 8, 2], (40, 20))
c_foot_r = add_cube("foot_r", [-7, 0, -3], [-3, 3, 1], [-5, 1, 0], (40, 32))

# Tail
c_tail_1 = add_cube("tail_1", [-3, 9, 7], [3, 14, 14], [0, 11, 7], (0, 16))
c_tail_2 = add_cube("tail_2", [-2, 10, 14], [2, 13, 22], [0, 11, 14], (16, 16))
c_tail_3 = add_cube("tail_3", [-1.5, 11, 22], [1.5, 13, 30], [0, 12, 22], (32, 16))
c_tail_flame = add_cube("tail_flame", [-2.5, 10.5, 30], [2.5, 15.5, 35], [0, 13, 32], (48, 48))

# Build Outliner Hierarchy
bone_head = {"name": "head", "origin": [0, 23, -13], "uuid": uid(), "children": [c_head, c_snout, c_horn_l, c_horn_r]}
bone_neck = {"name": "neck", "origin": [0, 18, -8], "uuid": uid(), "children": [c_neck, bone_head]}

bone_wing_l = {"name": "wing_left", "origin": [5, 15, -1], "uuid": uid(), "children": [c_w_arm_l, c_w_mem_l]}
bone_wing_r = {"name": "wing_right", "origin": [-5, 15, -1], "uuid": uid(), "children": [c_w_arm_r, c_w_mem_r]}

bone_leg_l = {"name": "leg_left", "origin": [5, 8, 2], "uuid": uid(), "children": [c_leg_l, c_foot_l]}
bone_leg_r = {"name": "leg_right", "origin": [-5, 8, 2], "uuid": uid(), "children": [c_leg_r, c_foot_r]}

bone_tail_flame = {"name": "tail_flame", "origin": [0, 13, 32], "uuid": uid(), "children": [c_tail_flame]}
bone_tail_3 = {"name": "tail_3", "origin": [0, 12, 22], "uuid": uid(), "children": [c_tail_3, bone_tail_flame]}
bone_tail_2 = {"name": "tail_2", "origin": [0, 11, 14], "uuid": uid(), "children": [c_tail_2, bone_tail_3]}
bone_tail_1 = {"name": "tail_1", "origin": [0, 11, 7], "uuid": uid(), "children": [c_tail_1, bone_tail_2]}

bone_body = {
    "name": "body",
    "origin": [0, 11, 0],
    "uuid": uid(),
    "children": [c_body, c_chest, bone_neck, bone_wing_l, bone_wing_r, bone_leg_l, bone_leg_r, bone_tail_1]
}

bone_root = {
    "name": "root",
    "origin": [0, 0, 0],
    "uuid": uid(),
    "children": [bone_body]
}

outliner = [bone_root]

# Animations
animations = [
    {
        "uuid": uid(),
        "name": "idle",
        "loop": "loop",
        "length": 2.0,
        "snapping": 24,
        "animators": {
            bone_body["uuid"]: {
                "name": "body",
                "type": "bone",
                "position": {
                    "0": [0, 0, 0],
                    "1.0": [0, 0.5, 0],
                    "2.0": [0, 0, 0]
                }
            },
            bone_wing_l["uuid"]: {
                "name": "wing_left",
                "type": "bone",
                "rotation": {
                    "0": [0, 0, 0],
                    "1.0": [0, 10, -5],
                    "2.0": [0, 0, 0]
                }
            },
            bone_wing_r["uuid"]: {
                "name": "wing_right",
                "type": "bone",
                "rotation": {
                    "0": [0, 0, 0],
                    "1.0": [0, -10, 5],
                    "2.0": [0, 0, 0]
                }
            },
            bone_tail_1["uuid"]: {
                "name": "tail_1",
                "type": "bone",
                "rotation": {
                    "0": [0, -5, 0],
                    "1.0": [0, 5, 0],
                    "2.0": [0, -5, 0]
                }
            }
        }
    },
    {
        "uuid": uid(),
        "name": "fly_flap",
        "loop": "loop",
        "length": 1.0,
        "snapping": 24,
        "animators": {
            bone_wing_l["uuid"]: {
                "name": "wing_left",
                "type": "bone",
                "rotation": {
                    "0": [0, 0, -45],
                    "0.5": [0, 0, 35],
                    "1.0": [0, 0, -45]
                }
            },
            bone_wing_r["uuid"]: {
                "name": "wing_right",
                "type": "bone",
                "rotation": {
                    "0": [0, 0, 45],
                    "0.5": [0, 0, -35],
                    "1.0": [0, 0, 45]
                }
            },
            bone_body["uuid"]: {
                "name": "body",
                "type": "bone",
                "rotation": {
                    "0": [25, 0, 0],
                    "0.5": [15, 0, 0],
                    "1.0": [25, 0, 0]
                }
            }
        }
    }
]

bbmodel_data = {
    "meta": {
        "format_version": "4.10",
        "model_format": "modded_entity",
        "box_uv": True
    },
    "name": "flamefang",
    "model_identifier": "flamefang",
    "visible_box": [3, 3, 3],
    "variable_placeholders": "",
    "resolution": {"width": 64, "height": 64},
    "elements": elements,
    "outliner": outliner,
    "textures": [
        {
            "path": tex_path,
            "name": "flamefang",
            "folder": "entity",
            "namespace": "wingsofthewild",
            "id": "0",
            "particle": False,
            "render_mode": "default",
            "visible": True,
            "mode": "bitmap",
            "saved": True,
            "uuid": uid(),
            "source": tex_base64
        }
    ],
    "animations": animations
}

target_file = r"D:\Mine\flamefang.bbmodel"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(bbmodel_data, f, indent=2)

print(f"Sucesso! Arquivo gerado em: {target_file}")
