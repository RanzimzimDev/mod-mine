import os
import json

recipe_dir = r"D:\Mine\src\main\resources\data\wingsofthewild\recipe"
crafting_types = {"minecraft:crafting_shaped", "minecraft:crafting_shapeless"}

fixed = []
for fname in os.listdir(recipe_dir):
    if not fname.endswith(".json"):
        continue
    fpath = os.path.join(recipe_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rtype = data.get("type")
    cat = data.get("category")
    
    # Se for crafting e tiver category "food" ou "misc", remova (ou ajuste) pois em 26.3 CraftingBookCategory nao tem "food"
    if rtype in crafting_types and cat not in {"building", "redstone", "equipment"}:
        data.pop("category", None)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        fixed.append((fname, cat))

print(f"Total corrigidos: {len(fixed)}")
for f, c in fixed:
    print(f"  {f}: removido category '{c}'")
