import json
from PIL import Image

stages = [
    ('flamefang_adult', 'flamefang_adult_geckolib.bbmodel', (512, 512), 36),
    ('flamefang_juvenile', 'flamefang_Juvenil_geckolib.bbmodel', (256, 256), 25),
    ('flamefang_hatchling', 'flamefang_hatchling_geckolib.bbmodel', (128, 128), 13),
    ('flamefang_egg', 'flamefang_egg_geckolib.bbmodel', (128, 128), 1)
]

for name, bbname, tex_size, min_bones in stages:
    # 1. Texture
    tpath = rf"D:\Mine\src\main\resources\assets\wingsofthewild\textures\entity\{name}.png"
    im = Image.open(tpath)
    assert im.size == tex_size, f"{name} tex size {im.size} != {tex_size}"
    
    # 2. Geo
    gpath = rf"D:\Mine\src\main\resources\assets\wingsofthewild\geo\{name}.geo.json"
    with open(gpath, 'r', encoding='utf-8') as f:
        geo = json.load(f)
    bones = geo['minecraft:geometry'][0]['bones']
    print(f"{name}: {len(bones)} geo bones, tex {im.size}")
    assert len(bones) >= min_bones
    
    # 3. Anim
    apath = rf"D:\Mine\src\main\resources\assets\wingsofthewild\animations\{name}.animation.json"
    with open(apath, 'r', encoding='utf-8') as f:
        anim = json.load(f)
    print(f"{name}: {len(anim['animations'])} animations")
    
    # 4. BBModel
    bbpath = rf"D:\Mine\models\flamefang\{bbname}"
    with open(bbpath, 'r', encoding='utf-8') as f:
        bb = json.load(f)
    assert bb['meta']['model_format'] == 'geckolib_model'
    print(f"{bbname}: {len(bb['elements'])} elements, {len(bb['animations'])} bb animations, format: {bb['meta']['model_format']}")

print("\n[ALL 4 FLAMEFANG LIFECYCLE STAGES 100% VALIDATED!]")
