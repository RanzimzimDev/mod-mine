import json
import os
from PIL import Image

def validate():
    print("=== VALIDATING 2.5X WIDER ASSETS ===")
    
    # 1. Texture Check
    tex_path = r'D:\Mine\src\main\resources\assets\wingsofthewild\textures\entity\flamefang_adult.png'
    im = Image.open(tex_path)
    print(f"Texture: {im.format}, {im.size}, {im.mode}")
    assert im.size == (512, 512), f"Expected 512x512, got {im.size}"

    # 2. Geo JSON Check
    geo_path = r'D:\Mine\src\main\resources\assets\wingsofthewild\geo\flamefang_adult.geo.json'
    with open(geo_path, 'r', encoding='utf-8') as f:
        geo = json.load(f)
    geom = geo['minecraft:geometry'][0]
    print(f"Texture width in geo: {geom['description']['texture_width']}x{geom['description']['texture_height']}")
    bones = geom['bones']
    print(f"Geo bones count: {len(bones)}")
    bone_names = [b['name'] for b in bones]
    tail_bones = [b for b in bone_names if 'tail' in b]
    print(f"Tail bones ({len(tail_bones)}): {tail_bones}")
    assert len(tail_bones) == 9, f"Expected 9 tail bones, found {len(tail_bones)}"

    # 3. Animation JSON Check
    anim_path = r'D:\Mine\src\main\resources\assets\wingsofthewild\animations\flamefang_adult.animation.json'
    with open(anim_path, 'r', encoding='utf-8') as f:
        anim = json.load(f)
    anims = anim['animations']
    print(f"Animations found: {len(anims)}")
    for k in anims:
        an_bones = anims[k]['bones']
        tail_in_an = [b for b in an_bones if 'tail' in b]
        print(f"  {k}: {len(tail_in_an)} tail bones animated")
    assert len(anims) >= 5, f"Expected at least 5 animations, got {len(anims)}"

    # 4. BBModel Check
    bb_path = r'D:\Mine\models\flamefang\flamefang_adult_geckolib.bbmodel'
    with open(bb_path, 'r', encoding='utf-8') as f:
        bb = json.load(f)
    fmt = bb['meta']['model_format']
    elem_count = len(bb['elements'])
    anim_count = len(bb['animations'])
    print(f"BBModel format: {fmt}")
    print(f"BBModel elements: {elem_count}")
    print(f"BBModel animations: {anim_count}")
    print(f"BBModel resolution: {bb['resolution']}")
    assert fmt == 'geckolib_model', f"Expected geckolib_model, got {fmt}"
    assert elem_count > 100, f"Expected > 100 elements, got {elem_count}"
    assert anim_count >= 5, f"Expected at least 5 bb animations, got {anim_count}"
    assert bb['resolution'] == {'width': 512, 'height': 512}

    print("\n[ALL 4 ASSETS 100% VALIDATED - HARMONIC DRAGON SUCCESS!]")

if __name__ == "__main__":
    validate()
