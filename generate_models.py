import json
import os

base = r"D:\Mine\src\main\resources\assets\wingsofthewild"

item_models = os.path.join(base, "models", "item")
block_models = os.path.join(base, "models", "block")
blockstates = os.path.join(base, "blockstates")

os.makedirs(item_models, exist_ok=True)
os.makedirs(block_models, exist_ok=True)
os.makedirs(blockstates, exist_ok=True)

# 1. Standard generated items
items = [
    "flamefang_scale",
    "raw_ember",
    "ember_ingot",
    "flamefang_egg",
    "spicy_magma_berries"
]

for item in items:
    data = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"wingsofthewild:item/{item}"
        }
    }
    with open(os.path.join(item_models, f"{item}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# 2. Blocks and their BlockItems
blocks = ["dragon_nest", "ember_ore"]

for block in blocks:
    # Blockstate
    bs_data = {
        "variants": {
            "": {"model": f"wingsofthewild:block/{block}"}
        }
    }
    with open(os.path.join(blockstates, f"{block}.json"), "w", encoding="utf-8") as f:
        json.dump(bs_data, f, indent=2)

    # Block Model
    bm_data = {
        "parent": "minecraft:block/cube_all",
        "textures": {
            "all": f"wingsofthewild:block/{block}"
        }
    }
    with open(os.path.join(block_models, f"{block}.json"), "w", encoding="utf-8") as f:
        json.dump(bm_data, f, indent=2)

    # Block Item Model
    bi_data = {
        "parent": f"wingsofthewild:block/{block}"
    }
    with open(os.path.join(item_models, f"{block}.json"), "w", encoding="utf-8") as f:
        json.dump(bi_data, f, indent=2)

print("Todos os modelos e blockstates JSON foram criados com sucesso!")
