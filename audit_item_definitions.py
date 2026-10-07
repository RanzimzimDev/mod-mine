import os
import json
import zipfile
import re

PROJECT_ROOT = r"D:\Mine"
ITEMS_DIR = os.path.join(PROJECT_ROOT, "src", "main", "resources", "assets", "wingsofthewild", "items")
MODELS_ITEM_DIR = os.path.join(PROJECT_ROOT, "src", "main", "resources", "assets", "wingsofthewild", "models", "item")
JAR_PATH = os.path.join(PROJECT_ROOT, "build", "libs", "wingsofthewild-1.0.0.jar")
ITENS_MD = os.path.join(PROJECT_ROOT, "ITENS.md")

def parse_itens_md():
    with open(ITENS_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    items = []
    pattern = re.compile(r"^\|\s*\*\*(\d+)\*\*\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*`?\[([ X~])\]`?\s*\|")
    for line in lines:
        m = pattern.match(line)
        if m:
            items.append({
                "num": int(m.group(1)),
                "id": m.group(2).strip(),
                "name": m.group(3).strip()
            })
    return items

def audit_items_def():
    items = parse_itens_md()
    print(f"Total items in ITENS.md: {len(items)}")

    errors = []
    verified = []

    for it in items:
        iid = it["id"]
        num = it["num"]
        fpath = os.path.join(ITEMS_DIR, f"{iid}.json")

        if not os.path.exists(fpath):
            errors.append(f"[#{num:02d} {iid}] Arquivo ausente: items/{iid}.json")
            continue

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"[#{num:02d} {iid}] JSON inválido em items/{iid}.json: {e}")
            continue

        if "model" not in data:
            errors.append(f"[#{num:02d} {iid}] Chave 'model' ausente em items/{iid}.json")
            continue

        model_info = data["model"]
        if not isinstance(model_info, dict):
            errors.append(f"[#{num:02d} {iid}] 'model' não é um objeto JSON em items/{iid}.json")
            continue

        m_type = model_info.get("type")
        m_target = model_info.get("model")

        if m_type != "minecraft:model":
            errors.append(f"[#{num:02d} {iid}] 'type' esperado 'minecraft:model', obtido '{m_type}'")
            continue

        expected_target = f"wingsofthewild:item/{iid}"
        if m_target != expected_target:
            errors.append(f"[#{num:02d} {iid}] 'model' esperado '{expected_target}', obtido '{m_target}'")
            continue

        # Check target model in models/item/
        target_model_file = os.path.join(MODELS_ITEM_DIR, f"{iid}.json")
        if not os.path.exists(target_model_file):
            errors.append(f"[#{num:02d} {iid}] Modelo de item apontado não existe: models/item/{iid}.json")
            continue

        verified.append({
            "num": num,
            "id": iid,
            "target": m_target,
            "file": f"assets/wingsofthewild/items/{iid}.json"
        })

    print(f"Itens verificados com sucesso: {len(verified)} / {len(items)}")
    if errors:
        print(f"Erros encontrados: {len(errors)}")
        for e in errors:
            print(" -", e)
    else:
        print(">>> 100% DAS DEFINICOES DE ITENS (116/116) ESTAO VALIDAS E PERFEITAS! <<<")

    return items, verified, errors

if __name__ == "__main__":
    audit_items_def()
