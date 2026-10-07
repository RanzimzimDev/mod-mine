import os
import json

stations = ['tack_workbench', 'dragon_nest', 'draconic_foundry', 'draconic_hearth', 'incubation_brazier', 'draconic_anvil', 'dragon_perch']
for s in stations:
    fpath = f"D:/Mine/src/main/resources/assets/wingsofthewild/models/block/{s}.json"
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for el in data.get("elements", []):
        for axis in range(3):
            if el["from"][axis] < 0:
                print(f"{s}: clamping {el.get('name')} from[{axis}] = {el['from'][axis]} -> 0")
                el["from"][axis] = max(0.0, float(el["from"][axis]))
                changed = True
            if el["to"][axis] > 16:
                print(f"{s}: clamping {el.get('name')} to[{axis}] = {el['to'][axis]} -> 16")
                el["to"][axis] = min(16.0, float(el["to"][axis]))
                changed = True
    if changed:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("Clamped:", s)
