import json
import math
import os
import uuid
import base64
from PIL import Image, ImageDraw

# Directories
GEO_DIR = r"D:\Mine\src\main\resources\assets\wingsofthewild\geo"
ANIM_DIR = r"D:\Mine\src\main\resources\assets\wingsofthewild\animations"
TEX_DIR = r"D:\Mine\src\main\resources\assets\wingsofthewild\textures\entity"
BBMODEL_PATH = r"D:\Mine\flamefang.bbmodel"

os.makedirs(GEO_DIR, exist_ok=True)
os.makedirs(ANIM_DIR, exist_ok=True)
os.makedirs(TEX_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. MODEL STRUCTURE DEFINITION
# -------------------------------------------------------------
# Bones required: root, body, neck, head, horns, wing_left, wing_right, leg_left, leg_right, tail_base, tail_tip, tail_flame

bones_def = [
    {
        "name": "root",
        "pivot": [0, 0, 0],
        "cubes": []
    },
    {
        "name": "body",
        "parent": "root",
        "pivot": [0, 16, 0],
        "cubes": [
            {
                "name": "torso",
                "origin": [-7, 10, -6],
                "size": [14, 14, 16],
                "uv": [0, 0],
                "category": "torso"
            },
            {
                "name": "chest_plate",
                "origin": [-6, 12, -8],
                "size": [12, 10, 2],
                "uv": [62, 0],
                "category": "chest"
            },
            {
                "name": "arm_left",
                "origin": [6.5, 11, -5],
                "size": [3, 8, 3],
                "uv": [92, 0],
                "category": "arm"
            },
            {
                "name": "arm_right",
                "origin": [-9.5, 11, -5],
                "size": [3, 8, 3],
                "uv": [106, 0],
                "category": "arm"
            },
            {
                "name": "dorsal_spikes",
                "origin": [-1, 24, -4],
                "size": [2, 3, 12],
                "uv": [92, 12],
                "category": "spikes"
            }
        ]
    },
    {
        "name": "neck",
        "parent": "body",
        "pivot": [0, 20, -5],
        "cubes": [
            {
                "name": "neck_main",
                "origin": [-4, 19, -8],
                "size": [8, 10, 7],
                "uv": [62, 14],
                "category": "neck"
            },
            {
                "name": "neck_spines",
                "origin": [-0.5, 23, -1],
                "size": [1, 5, 2],
                "uv": [120, 0],
                "category": "spikes"
            }
        ]
    },
    {
        "name": "head",
        "parent": "neck",
        "pivot": [0, 27, -6],
        "cubes": [
            {
                "name": "cranium",
                "origin": [-5, 26, -13],
                "size": [10, 7, 8],
                "uv": [0, 32],
                "category": "head"
            },
            {
                "name": "snout",
                "origin": [-4, 26, -19],
                "size": [8, 4, 6],
                "uv": [38, 32],
                "category": "snout"
            },
            {
                "name": "lower_jaw",
                "origin": [-3.5, 24, -18],
                "size": [7, 2, 6],
                "uv": [38, 43],
                "category": "jaw"
            }
        ]
    },
    {
        "name": "horns",
        "parent": "head",
        "pivot": [0, 32, -6],
        "cubes": [
            {
                "name": "horn_left_base",
                "origin": [3, 31, -7],
                "size": [2, 3, 6],
                "uv": [68, 32],
                "category": "horn"
            },
            {
                "name": "horn_left_tip",
                "origin": [3.5, 33, -2],
                "size": [2, 2, 5],
                "uv": [68, 42],
                "category": "horn"
            },
            {
                "name": "horn_right_base",
                "origin": [-5, 31, -7],
                "size": [2, 3, 6],
                "uv": [86, 32],
                "category": "horn"
            },
            {
                "name": "horn_right_tip",
                "origin": [-5.5, 33, -2],
                "size": [2, 2, 5],
                "uv": [86, 42],
                "category": "horn"
            }
        ]
    },
    {
        "name": "leg_left",
        "parent": "body",
        "pivot": [6, 14, 4],
        "cubes": [
            {
                "name": "thigh_left",
                "origin": [5, 6, 2],
                "size": [5, 10, 6],
                "uv": [0, 50],
                "category": "leg"
            },
            {
                "name": "shin_left",
                "origin": [5.5, 0, 1],
                "size": [4, 6, 5],
                "uv": [24, 50],
                "category": "leg"
            },
            {
                "name": "foot_left",
                "origin": [5, 0, -3],
                "size": [5, 2, 6],
                "uv": [24, 62],
                "category": "foot"
            }
        ]
    },
    {
        "name": "leg_right",
        "parent": "body",
        "pivot": [-6, 14, 4],
        "cubes": [
            {
                "name": "thigh_right",
                "origin": [-10, 6, 2],
                "size": [5, 10, 6],
                "uv": [48, 52],
                "category": "leg"
            },
            {
                "name": "shin_right",
                "origin": [-9.5, 0, 1],
                "size": [4, 6, 5],
                "uv": [72, 52],
                "category": "leg"
            },
            {
                "name": "foot_right",
                "origin": [-10, 0, -3],
                "size": [5, 2, 6],
                "uv": [72, 64],
                "category": "foot"
            }
        ]
    },
    {
        "name": "tail_base",
        "parent": "body",
        "pivot": [0, 14, 9],
        "cubes": [
            {
                "name": "tail_base_cube",
                "origin": [-4, 10, 9],
                "size": [8, 8, 14],
                "uv": [0, 72],
                "category": "tail"
            }
        ]
    },
    {
        "name": "tail_tip",
        "parent": "tail_base",
        "pivot": [0, 14, 23],
        "cubes": [
            {
                "name": "tail_tip_cube",
                "origin": [-2.5, 11, 23],
                "size": [5, 5, 14],
                "uv": [46, 72],
                "category": "tail"
            }
        ]
    },
    {
        "name": "tail_flame",
        "parent": "tail_tip",
        "pivot": [0, 13.5, 37],
        "cubes": [
            {
                "name": "flame_core",
                "origin": [-2, 11.5, 36],
                "size": [4, 5, 6],
                "uv": [86, 72],
                "category": "flame_core"
            },
            {
                "name": "flame_outer",
                "origin": [-3, 11, 38],
                "size": [6, 6, 6],
                "uv": [86, 84],
                "category": "flame_outer"
            }
        ]
    },
    {
        "name": "wing_left",
        "parent": "body",
        "pivot": [6, 20, -1],
        "cubes": [
            {
                "name": "wing_left_arm",
                "origin": [6, 19, -2],
                "size": [16, 3, 3],
                "uv": [0, 96],
                "category": "wing_arm"
            },
            {
                "name": "wing_left_strut",
                "origin": [20, 10, -2],
                "size": [3, 10, 2],
                "uv": [40, 96],
                "category": "wing_strut"
            },
            {
                "name": "wing_left_membrane",
                "origin": [7, 8, -0.5],
                "size": [15, 11, 1],
                "uv": [52, 96],
                "category": "wing_membrane"
            }
        ]
    },
    {
        "name": "wing_right",
        "parent": "body",
        "pivot": [-6, 20, -1],
        "cubes": [
            {
                "name": "wing_right_arm",
                "origin": [-22, 19, -2],
                "size": [16, 3, 3],
                "uv": [0, 110],
                "category": "wing_arm"
            },
            {
                "name": "wing_right_strut",
                "origin": [-23, 10, -2],
                "size": [3, 10, 2],
                "uv": [40, 110],
                "category": "wing_strut"
            },
            {
                "name": "wing_right_membrane",
                "origin": [-22, 8, -0.5],
                "size": [15, 11, 1],
                "uv": [52, 110],
                "category": "wing_membrane"
            }
        ]
    }
]

# -------------------------------------------------------------
# 2. GENERATE GECKOLIB / BEDROCK GEO JSON
# -------------------------------------------------------------
geo_data = {
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {
            "description": {
                "identifier": "geometry.flamefang",
                "texture_width": 128,
                "texture_height": 128,
                "visible_bounds_width": 5,
                "visible_bounds_height": 4,
                "visible_bounds_offset": [0, 1.5, 0]
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
    if b["cubes"]:
        bone_entry["cubes"] = []
        for c in b["cubes"]:
            cube_obj = {
                "origin": c["origin"],
                "size": c["size"],
                "uv": c["uv"]
            }
            bone_entry["cubes"].append(cube_obj)
    geo_data["minecraft:geometry"][0]["bones"].append(bone_entry)

geo_file_path = os.path.join(GEO_DIR, "flamefang.geo.json")
with open(geo_file_path, "w", encoding="utf-8") as f:
    json.dump(geo_data, f, indent=2)
print(f"Generated {geo_file_path}")

# -------------------------------------------------------------
# 3. GENERATE TEXTURE WITH PIL
# -------------------------------------------------------------
tex = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw = ImageDraw.Draw(tex)

# Helper for painting box UV faces
def fill_rect(u, v, w, h, color):
    for y in range(int(v), int(v + h)):
        for x in range(int(u), int(u + w)):
            if 0 <= x < 128 and 0 <= y < 128:
                tex.putpixel((x, y), color)

def noise(x, y, factor=12):
    val = int(math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % factor
    return val - factor // 2

def shade_color(c, delta):
    r = max(0, min(255, c[0] + delta))
    g = max(0, min(255, c[1] + delta))
    b = max(0, min(255, c[2] + delta))
    a = c[3] if len(c) > 3 else 255
    return (r, g, b, a)

# Color palettes
SCALE_DARK = (28, 26, 34, 255)       # Charcoal obsidian base
SCALE_MID = (38, 35, 46, 255)        # Obsidian slate
SCALE_LIGHT = (52, 48, 62, 255)      # Highlight sheen
BELLY_DARK = (130, 28, 24, 255)      # Rustic carmine underbelly
BELLY_MID = (168, 42, 32, 255)       # Deep ember red
BELLY_LIGHT = (195, 62, 45, 255)     # Warm scale highlight
HORN_DARK = (45, 38, 32, 255)        # Charred ivory
HORN_MID = (85, 72, 60, 255)         # Weathered horn
HORN_LIGHT = (125, 108, 92, 255)     # Tip bone
FIRE_YELLOW = (255, 235, 90, 255)    # Core incandescence
FIRE_ORANGE = (255, 130, 15, 255)    # Raging fire
FIRE_RED = (220, 45, 15, 255)        # Dark flame
MEMBRANE_DARK = (65, 22, 18, 255)    # Burnt dragon leather
MEMBRANE_MID = (92, 32, 26, 255)     # Ember undertone
MEMBRANE_LIGHT = (115, 42, 34, 255)  # Leather highlight
CLAW_COLOR = (24, 22, 20, 255)
FANG_COLOR = (225, 218, 195, 255)
EYE_GOLD = (255, 198, 10, 255)
EYE_PUPIL = (15, 10, 10, 255)

for b in bones_def:
    for c in b["cubes"]:
        u0, v0 = c["uv"]
        w, h, d = c["size"]
        cat = c["category"]

        # Faces breakdown:
        # up: (u0 + d, v0) size w x d
        # down: (u0 + d + w, v0) size w x d
        # west: (u0, v0 + d) size d x h
        # north: (u0 + d, v0 + d) size w x h
        # east: (u0 + d + w, v0 + d) size d x h
        # south: (u0 + 2*d + w, v0 + d) size w x h

        faces = [
            ("up", u0 + d, v0, w, d),
            ("down", u0 + d + w, v0, w, d),
            ("west", u0, v0 + d, d, h),
            ("north", u0 + d, v0 + d, w, h),
            ("east", u0 + d + w, v0 + d, d, h),
            ("south", u0 + 2*d + w, v0 + d, w, h)
        ]

        for fname, fu, fv, fw, fh in faces:
            for py in range(int(fv), int(fv + fh)):
                for px in range(int(fu), int(fu + fw)):
                    n = noise(px, py, 14)
                    
                    if cat == "torso":
                        # North face (facing neck) is covered/dark
                        # Down face (belly) is red carmine!
                        # South face (back) is dark obsidian
                        # West/East (flanks): gradient from carmine belly to obsidian back
                        if fname == "down":
                            base_c = BELLY_MID
                        elif fname in ("west", "east"):
                            rel_y = (py - fv) / max(1, fh)
                            base_c = BELLY_MID if rel_y > 0.6 else SCALE_MID
                        elif fname == "north":
                            base_c = BELLY_MID
                        else:
                            base_c = SCALE_MID
                    elif cat == "chest":
                        # Chest plate is vivid carmine underbelly armor
                        base_c = BELLY_MID if (px + py) % 4 != 0 else BELLY_LIGHT
                    elif cat == "head":
                        # Cranium: obsidian scales, with golden predatory eyes on east/west faces!
                        base_c = SCALE_MID
                    elif cat == "snout":
                        base_c = SCALE_DARK
                    elif cat == "jaw":
                        base_c = BELLY_DARK if fname == "down" else SCALE_DARK
                    elif cat == "neck":
                        # Throat (north) is reddish, back (south) is obsidian
                        base_c = BELLY_MID if fname == "north" or fname == "down" else SCALE_MID
                    elif cat == "horn":
                        # Horn gradient from base (dark) to tip (light)
                        base_c = HORN_MID
                    elif cat == "spikes":
                        base_c = HORN_DARK
                    elif cat == "leg":
                        base_c = SCALE_MID
                    elif cat == "foot":
                        base_c = SCALE_DARK
                    elif cat == "arm":
                        base_c = SCALE_MID
                    elif cat == "tail":
                        # Bottom is carmine, top is obsidian
                        base_c = BELLY_DARK if fname == "down" else SCALE_MID
                    elif cat == "flame_core":
                        # Blazing hot core
                        base_c = FIRE_YELLOW if (px + py) % 2 == 0 else FIRE_ORANGE
                    elif cat == "flame_outer":
                        # Outer roaring fire
                        rel_dist = math.sqrt((px - fu - fw/2)**2 + (py - fv - fh/2)**2)
                        base_c = FIRE_ORANGE if rel_dist < 2.5 else FIRE_RED
                    elif cat == "wing_arm" or cat == "wing_strut":
                        base_c = SCALE_DARK
                    elif cat == "wing_membrane":
                        base_c = MEMBRANE_MID if (px + py) % 3 != 0 else MEMBRANE_LIGHT
                    else:
                        base_c = SCALE_MID

                    col = shade_color(base_c, n)
                    tex.putpixel((px, py), col)

# Special detail touches:
# 1. Dragon Eyes on head sides (cranium west and east faces)
# Cranium: uv=[0, 32], size=[10, 7, 8].
# west face: fu = 0, fv = 32+8=40, fw = 8, fh = 7.
# east face: fu = 0 + 8 + 10 = 18, fv = 40, fw = 8, fh = 7.
# Eye on west face: x=fu+2..fu+4, y=fv+2..fv+3
for ex in range(2, 5):
    for ey in range(2, 4):
        tex.putpixel((0 + ex, 40 + ey), EYE_GOLD)
        tex.putpixel((18 + 7 - ex, 40 + ey), EYE_GOLD)
# Pupil slit:
tex.putpixel((0 + 3, 40 + 2), EYE_PUPIL)
tex.putpixel((0 + 3, 40 + 3), EYE_PUPIL)
tex.putpixel((18 + 7 - 3, 40 + 2), EYE_PUPIL)
tex.putpixel((18 + 7 - 3, 40 + 3), EYE_PUPIL)

# 2. Fangs on snout
# snout: uv=[38, 32], size=[8, 4, 6]
# west/east lower edges:
tex.putpixel((38 + 1, 32 + 6 + 3), FANG_COLOR)
tex.putpixel((38 + 3, 32 + 6 + 3), FANG_COLOR)
tex.putpixel((38 + 6 + 8 + 1, 32 + 6 + 3), FANG_COLOR)
tex.putpixel((38 + 6 + 8 + 3, 32 + 6 + 3), FANG_COLOR)

# 3. Talons / Claws on feet
# Foot left: uv=[24, 62], size=[5, 2, 6] -> north face: fu=24+6=30, fv=62+6=68, fw=5, fh=2
for tx in range(30, 35, 2):
    tex.putpixel((tx, 69), CLAW_COLOR)
# Foot right: uv=[72, 64], size=[5, 2, 6] -> north face: fu=72+6=78, fv=64+6=70, fw=5, fh=2
for tx in range(78, 83, 2):
    tex.putpixel((tx, 71), CLAW_COLOR)

tex_file_path = os.path.join(TEX_DIR, "flamefang.png")
tex.save(tex_file_path)
print(f"Generated {tex_file_path}")

# -------------------------------------------------------------
# 4. GENERATE GECKOLIB ANIMATIONS JSON
# -------------------------------------------------------------
anim_data = {
    "format_version": "1.8.0",
    "animations": {
        "animation.flamefang.idle": {
            "loop": True,
            "animation_length": 4.0,
            "bones": {
                "body": {
                    "rotation": {
                        "0.0": [0, 0, 0],
                        "2.0": [-2.0, 0, 0],
                        "4.0": [0, 0, 0]
                    },
                    "position": {
                        "0.0": [0, 0, 0],
                        "2.0": [0, -0.4, 0],
                        "4.0": [0, 0, 0]
                    }
                },
                "neck": {
                    "rotation": {
                        "0.0": [0, 0, 0],
                        "2.0": [3.0, 0, 0],
                        "4.0": [0, 0, 0]
                    }
                },
                "head": {
                    "rotation": {
                        "0.0": [0, 0, 0],
                        "2.0": [-2.5, 0, 0],
                        "4.0": [0, 0, 0]
                    }
                },
                "wing_left": {
                    "rotation": {
                        "0.0": [0, 0, -6.0],
                        "2.0": [0, 0, -2.0],
                        "4.0": [0, 0, -6.0]
                    }
                },
                "wing_right": {
                    "rotation": {
                        "0.0": [0, 0, 6.0],
                        "2.0": [0, 0, 2.0],
                        "4.0": [0, 0, 6.0]
                    }
                },
                "tail_base": {
                    "rotation": {
                        "0.0": [0, -4.0, 0],
                        "2.0": [0, 4.0, 0],
                        "4.0": [-0, -4.0, 0]
                    }
                },
                "tail_tip": {
                    "rotation": {
                        "0.0": [0, -8.0, 0],
                        "2.0": [0, 8.0, 0],
                        "4.0": [0, -8.0, 0]
                    }
                },
                "tail_flame": {
                    "rotation": {
                        "0.0": [0, 0, -8.0],
                        "1.0": [5.0, 8.0, 0],
                        "2.0": [0, 0, 8.0],
                        "3.0": [-5.0, -8.0, 0],
                        "4.0": [0, 0, -8.0]
                    },
                    "scale": {
                        "0.0": [1.0, 1.0, 1.0],
                        "1.0": [1.1, 1.2, 1.1],
                        "2.0": [0.95, 0.9, 0.95],
                        "3.0": [1.15, 1.25, 1.15],
                        "4.0": [1.0, 1.0, 1.0]
                    }
                }
            }
        },
        "animation.flamefang.walk": {
            "loop": True,
            "animation_length": 1.6,
            "bones": {
                "root": {
                    "position": {
                        "0.0": [0, 0, 0],
                        "0.4": [0, 0.6, 0],
                        "0.8": [0, 0, 0],
                        "1.2": [0, 0.6, 0],
                        "1.6": [0, 0, 0]
                    }
                },
                "body": {
                    "rotation": {
                        "0.0": [2.0, 0, -2.0],
                        "0.4": [0.5, 1.5, 0],
                        "0.8": [2.0, 0, 2.0],
                        "1.2": [0.5, -1.5, 0],
                        "1.6": [2.0, 0, -2.0]
                    }
                },
                "neck": {
                    "rotation": {
                        "0.0": [0, 0, 2.0],
                        "0.8": [0, 0, -2.0],
                        "1.6": [0, 0, 2.0]
                    }
                },
                "head": {
                    "rotation": {
                        "0.0": [-2.0, -2.0, 0],
                        "0.8": [-2.0, 2.0, 0],
                        "1.6": [-2.0, -2.0, 0]
                    }
                },
                "leg_left": {
                    "rotation": {
                        "0.0": [-22.0, 0, 0],
                        "0.4": [0, 0, 0],
                        "0.8": [22.0, 0, 0],
                        "1.2": [0, 0, 0],
                        "1.6": [-22.0, 0, 0]
                    }
                },
                "leg_right": {
                    "rotation": {
                        "0.0": [22.0, 0, 0],
                        "0.4": [0, 0, 0],
                        "0.8": [-22.0, 0, 0],
                        "1.2": [0, 0, 0],
                        "1.6": [22.0, 0, 0]
                    }
                },
                "wing_left": {
                    "rotation": {
                        "0.0": [0, 0, -7.0],
                        "0.8": [0, 0, -3.0],
                        "1.6": [0, 0, -7.0]
                    }
                },
                "wing_right": {
                    "rotation": {
                        "0.0": [0, 0, 7.0],
                        "0.8": [0, 0, 3.0],
                        "1.6": [0, 0, 7.0]
                    }
                },
                "tail_base": {
                    "rotation": {
                        "0.0": [0, 10.0, 0],
                        "0.8": [0, -10.0, 0],
                        "1.6": [0, 10.0, 0]
                    }
                },
                "tail_tip": {
                    "rotation": {
                        "0.0": [0, 16.0, 0],
                        "0.8": [0, -16.0, 0],
                        "1.6": [0, 16.0, 0]
                    }
                },
                "tail_flame": {
                    "rotation": {
                        "0.0": [0, 12.0, -12.0],
                        "0.8": [0, -12.0, 12.0],
                        "1.6": [0, 12.0, -12.0]
                    },
                    "scale": {
                        "0.0": [1.0, 1.1, 1.0],
                        "0.8": [1.2, 1.3, 1.1],
                        "1.6": [1.0, 1.1, 1.0]
                    }
                }
            }
        },
        "animation.flamefang.fly_flap": {
            "loop": True,
            "animation_length": 1.0,
            "bones": {
                "body": {
                    "rotation": {
                        "0.0": [12.0, 0, 0],
                        "0.3": [8.0, 0, 0],
                        "0.6": [16.0, 0, 0],
                        "1.0": [12.0, 0, 0]
                    },
                    "position": {
                        "0.0": [0, 0, 0],
                        "0.3": [0, 1.5, 0],
                        "0.6": [0, -1.2, 0],
                        "1.0": [0, 0, 0]
                    }
                },
                "neck": {
                    "rotation": {
                        "0.0": [-8.0, 0, 0],
                        "0.5": [-4.0, 0, 0],
                        "1.0": [-8.0, 0, 0]
                    }
                },
                "head": {
                    "rotation": {
                        "0.0": [-4.0, 0, 0],
                        "0.5": [-8.0, 0, 0],
                        "1.0": [-4.0, 0, 0]
                    }
                },
                "wing_left": {
                    "rotation": {
                        "0.0": [0, 0, 20.0],
                        "0.3": [0, 0, -42.0],
                        "0.6": [0, 0, 36.0],
                        "1.0": [0, 0, 20.0]
                    }
                },
                "wing_right": {
                    "rotation": {
                        "0.0": [0, 0, -20.0],
                        "0.3": [0, 0, 42.0],
                        "0.6": [0, 0, -36.0],
                        "1.0": [0, 0, -20.0]
                    }
                },
                "leg_left": {
                    "rotation": {
                        "0.0": [30.0, 0, 4.0],
                        "0.5": [40.0, 0, 4.0],
                        "1.0": [30.0, 0, 4.0]
                    }
                },
                "leg_right": {
                    "rotation": {
                        "0.0": [30.0, 0, -4.0],
                        "0.5": [40.0, 0, -4.0],
                        "1.0": [30.0, 0, -4.0]
                    }
                },
                "tail_base": {
                    "rotation": {
                        "0.0": [-4.0, 0, 0],
                        "0.5": [4.0, 0, 0],
                        "1.0": [-4.0, 0, 0]
                    }
                },
                "tail_tip": {
                    "rotation": {
                        "0.0": [-8.0, 0, 0],
                        "0.5": [8.0, 0, 0],
                        "1.0": [-8.0, 0, 0]
                    }
                },
                "tail_flame": {
                    "rotation": {
                        "0.0": [-12.0, 0, 0],
                        "0.5": [16.0, 0, 0],
                        "1.0": [-12.0, 0, 0]
                    },
                    "scale": {
                        "0.0": [1.1, 1.25, 1.1],
                        "0.5": [1.3, 1.45, 1.2],
                        "1.0": [1.1, 1.25, 1.1]
                    }
                }
            }
        }
    }
}

anim_file_path = os.path.join(ANIM_DIR, "flamefang.animation.json")
with open(anim_file_path, "w", encoding="utf-8") as f:
    json.dump(anim_data, f, indent=2)
print(f"Generated {anim_file_path}")

# -------------------------------------------------------------
# 5. GENERATE NATIVE BLOCKBENCH .BBMODEL PROJECT FILE
# -------------------------------------------------------------
# Encode PNG texture to base64
with open(tex_file_path, "rb") as img_f:
    tex_base64 = "data:image/png;base64," + base64.b64encode(img_f.read()).decode("utf-8")

tex_uuid = str(uuid.uuid4())

# Build Blockbench elements and outliner
elements = []
bone_uuid_map = {}
element_uuid_map = {}

for b in bones_def:
    b_uuid = str(uuid.uuid4())
    bone_uuid_map[b["name"]] = b_uuid

for b in bones_def:
    for c in b["cubes"]:
        c_uuid = str(uuid.uuid4())
        element_uuid_map[c["name"]] = c_uuid
        
        ox, oy, oz = c["origin"]
        sx, sy, sz = c["size"]
        u0, v0 = c["uv"]

        from_pos = [ox, oy, oz]
        to_pos = [ox + sx, oy + sy, oz + sz]

        elem = {
            "name": c["name"],
            "box_uv": True,
            "rescale": False,
            "locked": False,
            "render_order": "default",
            "allow_mirror_modeling": True,
            "from": from_pos,
            "to": to_pos,
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
            "uuid": c_uuid
        }
        elements.append(elem)

# Build hierarchical outliner
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
        "children": [c["name"] for c in b["cubes"]],
        "_raw_children": []
    }

# Link parent-children
root_bones = []
for b in bones_def:
    b_name = b["name"]
    node = bone_dict[b_name]
    
    # replace cube names with cube uuids in _raw_children
    cube_uuids = [element_uuid_map[cname] for cname in node["children"]]
    node["_raw_children"].extend(cube_uuids)

for b in bones_def:
    b_name = b["name"]
    node = bone_dict[b_name]
    if "parent" in b:
        parent_name = b["parent"]
        bone_dict[parent_name]["_raw_children"].append(node)
    else:
        root_bones.append(node)

# Cleanup recursive helper to produce clean outliner
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

# Build Blockbench animations structure
bb_animations = []
for anim_key, anim_val in anim_data["animations"].items():
    anim_name = anim_key.replace("animation.flamefang.", "")
    anim_uuid = str(uuid.uuid4())
    animators = {}

    for bname, channels in anim_val["bones"].items():
        if bname not in bone_uuid_map:
            continue
        buuid = bone_uuid_map[bname]
        keyframes = []

        if "rotation" in channels:
            for time_str, rot_vec in channels["rotation"].items():
                t = float(time_str)
                keyframes.append({
                    "channel": "rotation",
                    "time": t,
                    "data_points": [{"x": rot_vec[0], "y": rot_vec[1], "z": rot_vec[2]}],
                    "interpolation": "linear",
                    "uuid": str(uuid.uuid4())
                })
        if "position" in channels:
            for time_str, pos_vec in channels["position"].items():
                t = float(time_str)
                keyframes.append({
                    "channel": "position",
                    "time": t,
                    "data_points": [{"x": pos_vec[0], "y": pos_vec[1], "z": pos_vec[2]}],
                    "interpolation": "linear",
                    "uuid": str(uuid.uuid4())
                })
        if "scale" in channels:
            for time_str, sc_vec in channels["scale"].items():
                t = float(time_str)
                keyframes.append({
                    "channel": "scale",
                    "time": t,
                    "data_points": [{"x": sc_vec[0], "y": sc_vec[1], "z": sc_vec[2]}],
                    "interpolation": "linear",
                    "uuid": str(uuid.uuid4())
                })

        animators[buuid] = {
            "name": bname,
            "type": "bone",
            "keyframes": keyframes
        }

    bb_animations.append({
        "name": anim_name,
        "uuid": anim_uuid,
        "loop": "loop",
        "length": anim_val["animation_length"],
        "animators": animators
    })

bbmodel_data = {
    "meta": {
        "format_version": "4.10",
        "creation_time": 1728210000,
        "model_format": "geckolib",
        "box_uv": True
    },
    "name": "flamefang",
    "model_identifier": "flamefang",
    "visible_box": [3, 3, 0],
    "resolution": {
        "width": 128,
        "height": 128
    },
    "elements": elements,
    "outliner": outliner,
    "textures": [
        {
            "type": "entity",
            "name": "flamefang.png",
            "id": "0",
            "uuid": tex_uuid,
            "source": tex_base64
        }
    ],
    "animations": bb_animations
}

with open(BBMODEL_PATH, "w", encoding="utf-8") as f:
    json.dump(bbmodel_data, f, indent=2)
print(f"Generated {BBMODEL_PATH}")
