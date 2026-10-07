import os
import re
import json
import zipfile
from PIL import Image

PROJECT_ROOT = r"D:\Mine"
JAR_PATH = os.path.join(PROJECT_ROOT, "build", "libs", "wingsofthewild-1.0.0.jar")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "src", "main", "resources", "assets", "wingsofthewild")
JAVA_DIR = os.path.join(PROJECT_ROOT, "src", "main", "java", "com", "wingsofthewild")

def parse_itens_md():
    itens_md_path = os.path.join(PROJECT_ROOT, "ITENS.md")
    with open(itens_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    items = []
    current_category = ""
    pattern = re.compile(r"^\|\s*\*\*(\d+)\*\*\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*`?\[([ X~])\]`?\s*\|")
    cat_pattern = re.compile(r"^##\s*(.+)")

    for line in lines:
        cat_match = cat_pattern.match(line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue
        
        m = pattern.match(line)
        if m:
            num = int(m.group(1))
            item_id = m.group(2).strip()
            name_pt = m.group(3).strip()
            desc = m.group(4).strip()
            status_char = m.group(5).strip()
            # Blocks are items 01-08, 51-58, and 81-91 (Foundry & Elemental Ores)
            is_block = (num in [1,2,3,4,5,6,7,8, 51,52,53,54,55,56,57,58] or (81 <= num <= 91))
            items.append({
                "num": num,
                "id": item_id,
                "name_pt": name_pt,
                "desc": desc,
                "status_md": status_char,
                "is_block": is_block,
                "category": current_category
            })
    return items

def read_java_code():
    blocks_file = os.path.join(JAVA_DIR, "init", "ModBlocks.java")
    items_file = os.path.join(JAVA_DIR, "init", "ModItems.java")
    tabs_file = os.path.join(JAVA_DIR, "init", "ModCreativeTabs.java")

    with open(blocks_file, "r", encoding="utf-8") as f:
        blocks_code = f.read()
    with open(items_file, "r", encoding="utf-8") as f:
        items_code = f.read()
    with open(tabs_file, "r", encoding="utf-8") as f:
        tabs_code = f.read()

    # Blocks: registerBlock("...", ...)
    block_reg = set(re.findall(r'registerBlock\(\s*"([^"]+)"', blocks_code))
    
    # Items: registerSimpleItem("...") or registerItem("...", ...)
    item_reg = set(re.findall(r'register(?:Simple)?Item\(\s*"([^"]+)"', items_code))

    # Tabs acceptance
    tab_blocks = set(re.findall(r'ModBlocks\.([A-Z0-9_]+)\.get\(\)', tabs_code))
    tab_items = set(re.findall(r'ModItems\.([A-Z0-9_]+)\.get\(\)', tabs_code))

    field_to_block_id = dict(re.findall(r'public\s+static\s+final\s+DeferredBlock<[^>]+>\s+([A-Z0-9_]+)\s*=\s*registerBlock\(\s*"([^"]+)"', blocks_code))
    field_to_item_id = dict(re.findall(r'public\s+static\s+final\s+DeferredItem<[^>]+>\s+([A-Z0-9_]+)\s*=\s*ITEMS\.register(?:Simple)?Item\(\s*"([^"]+)"', items_code))

    tab_block_ids = {field_to_block_id[k] for k in tab_blocks if k in field_to_block_id}
    tab_item_ids = {field_to_item_id[k] for k in tab_items if k in field_to_item_id}

    return block_reg, item_reg, tab_block_ids, tab_item_ids

def run_deep_audit():
    items = parse_itens_md()
    block_reg, item_reg, tab_block_ids, tab_item_ids = read_java_code()

    with open(os.path.join(ASSETS_DIR, "lang", "en_us.json"), "r", encoding="utf-8") as f:
        en_us = json.load(f)
    with open(os.path.join(ASSETS_DIR, "lang", "pt_br.json"), "r", encoding="utf-8") as f:
        pt_br = json.load(f)

    jar_entries = set()
    if os.path.exists(JAR_PATH):
        with zipfile.ZipFile(JAR_PATH, "r") as z:
            jar_entries = set(z.namelist())

    report = []

    for it in items:
        num = it["num"]
        iid = it["id"]
        is_block = it["is_block"]
        status_md = it["status_md"]

        item_audit = {
            "num": num,
            "id": iid,
            "name_pt": it["name_pt"],
            "desc": it["desc"],
            "category": it["category"],
            "status_md": status_md,
            "type": "Bloco" if is_block else "Item",
            "criteria": {
                "java_registered": False,
                "json_models_valid": False,
                "textures_valid": False,
                "translations_present": False,
                "creative_tab_present": False,
                "jar_packaged": False
            },
            "textures_inspected": [],
            "models_inspected": [],
            "errors": []
        }

        # 1. Java Registration
        if is_block:
            item_audit["criteria"]["java_registered"] = (iid in block_reg)
            if not item_audit["criteria"]["java_registered"]:
                item_audit["errors"].append(f"Bloco '{iid}' não registrado em ModBlocks.java")
        else:
            item_audit["criteria"]["java_registered"] = (iid in item_reg)
            if not item_audit["criteria"]["java_registered"]:
                item_audit["errors"].append(f"Item '{iid}' não registrado em ModItems.java")

        # 2. JSON Models & Blockstates
        json_ok = True
        referenced_textures = []

        if is_block:
            # Blockstate
            bs_file = os.path.join(ASSETS_DIR, "blockstates", f"{iid}.json")
            if not os.path.exists(bs_file):
                json_ok = False
                item_audit["errors"].append(f"Blockstate ausente: blockstates/{iid}.json")
            else:
                try:
                    with open(bs_file, "r", encoding="utf-8") as f:
                        bs_data = json.load(f)
                    item_audit["models_inspected"].append(f"blockstates/{iid}.json")
                except Exception as e:
                    json_ok = False
                    item_audit["errors"].append(f"Erro de sintaxe em blockstates/{iid}.json: {e}")

            # Block model
            bm_file = os.path.join(ASSETS_DIR, "models", "block", f"{iid}.json")
            if not os.path.exists(bm_file):
                json_ok = False
                item_audit["errors"].append(f"Modelo de bloco ausente: models/block/{iid}.json")
            else:
                try:
                    with open(bm_file, "r", encoding="utf-8") as f:
                        bm_data = json.load(f)
                    item_audit["models_inspected"].append(f"models/block/{iid}.json")
                    if "textures" in bm_data:
                        for k, v in bm_data["textures"].items():
                            if v.startswith("wingsofthewild:block/"):
                                tex_name = v.replace("wingsofthewild:block/", "")
                                referenced_textures.append(("block", tex_name))
                except Exception as e:
                    json_ok = False
                    item_audit["errors"].append(f"Erro de sintaxe em models/block/{iid}.json: {e}")

            # Block Item Model
            bim_file = os.path.join(ASSETS_DIR, "models", "item", f"{iid}.json")
            if not os.path.exists(bim_file):
                json_ok = False
                item_audit["errors"].append(f"Modelo de item de bloco ausente: models/item/{iid}.json")
            else:
                try:
                    with open(bim_file, "r", encoding="utf-8") as f:
                        bim_data = json.load(f)
                    item_audit["models_inspected"].append(f"models/item/{iid}.json")
                except Exception as e:
                    json_ok = False
                    item_audit["errors"].append(f"Erro de sintaxe em models/item/{iid}.json: {e}")

        else: # Standard Item Model
            im_file = os.path.join(ASSETS_DIR, "models", "item", f"{iid}.json")
            if not os.path.exists(im_file):
                json_ok = False
                item_audit["errors"].append(f"Modelo de item ausente: models/item/{iid}.json")
            else:
                try:
                    with open(im_file, "r", encoding="utf-8") as f:
                        im_data = json.load(f)
                    item_audit["models_inspected"].append(f"models/item/{iid}.json")
                    if "textures" in im_data:
                        for k, v in im_data["textures"].items():
                            if v.startswith("wingsofthewild:item/"):
                                tex_name = v.replace("wingsofthewild:item/", "")
                                referenced_textures.append(("item", tex_name))
                except Exception as e:
                    json_ok = False
                    item_audit["errors"].append(f"Erro de sintaxe em models/item/{iid}.json: {e}")

        item_audit["criteria"]["json_models_valid"] = json_ok

        # 3. Texturas PNG
        tex_ok = True
        if not referenced_textures:
            referenced_textures.append(("block" if is_block else "item", iid))

        for t_type, t_name in referenced_textures:
            t_path = os.path.join(ASSETS_DIR, "textures", t_type, f"{t_name}.png")
            if not os.path.exists(t_path):
                tex_ok = False
                item_audit["errors"].append(f"Textura ausente: textures/{t_type}/{t_name}.png")
            else:
                try:
                    with Image.open(t_path) as img:
                        w, h = img.size
                        mode = img.mode
                        fmt = img.format
                        item_audit["textures_inspected"].append(f"{t_name}.png ({w}x{h}, {mode}, {fmt})")
                        if w <= 0 or h <= 0 or fmt != "PNG":
                            tex_ok = False
                            item_audit["errors"].append(f"Textura corrompida ou inválida: {t_name}.png")
                except Exception as e:
                    tex_ok = False
                    item_audit["errors"].append(f"Erro ao abrir imagem textures/{t_type}/{t_name}.png: {e}")

        item_audit["criteria"]["textures_valid"] = tex_ok

        # 4. Traduções (en_us e pt_br)
        lang_key = f"{'block' if is_block else 'item'}.wingsofthewild.{iid}"
        has_en = (lang_key in en_us) and len(en_us[lang_key].strip()) > 0
        has_pt = (lang_key in pt_br) and len(pt_br[lang_key].strip()) > 0
        item_audit["criteria"]["translations_present"] = (has_en and has_pt)
        item_audit["en_name"] = en_us.get(lang_key, "")
        item_audit["pt_name_lang"] = pt_br.get(lang_key, "")
        if not has_en:
            item_audit["errors"].append(f"Chave '{lang_key}' ausente em lang/en_us.json")
        if not has_pt:
            item_audit["errors"].append(f"Chave '{lang_key}' ausente em lang/pt_br.json")

        # 5. Nova Definição de Item NeoForge/MC 26.3 (items/<id>.json)
        item_def_file = os.path.join(ASSETS_DIR, "items", f"{iid}.json")
        item_def_ok = True
        if not os.path.exists(item_def_file):
            item_def_ok = False
            item_audit["errors"].append(f"Definição de item ausente: items/{iid}.json")
        else:
            try:
                with open(item_def_file, "r", encoding="utf-8") as f:
                    idef_data = json.load(f)
                if idef_data.get("model", {}).get("type") != "minecraft:model":
                    item_def_ok = False
                    item_audit["errors"].append(f"items/{iid}.json: 'type' inválido (esperado 'minecraft:model')")
                expected_target = f"wingsofthewild:item/{iid}"
                if idef_data.get("model", {}).get("model") != expected_target:
                    item_def_ok = False
                    item_audit["errors"].append(f"items/{iid}.json: 'model' esperado '{expected_target}'")
            except Exception as e:
                item_def_ok = False
                item_audit["errors"].append(f"Erro em items/{iid}.json: {e}")

        item_audit["criteria"]["item_definition_valid"] = item_def_ok

        # 6. Aba Criativa
        in_tab = (iid in tab_block_ids) if is_block else (iid in tab_item_ids)
        item_audit["criteria"]["creative_tab_present"] = in_tab
        if not in_tab:
            item_audit["errors"].append(f"Não incluído na aba criativa em ModCreativeTabs.java")

        # 7. Presença no JAR Compilado
        jar_ok = True
        if not jar_entries:
            jar_ok = False
            item_audit["errors"].append("Arquivo JAR não encontrado ou vazio")
        else:
            # Check models & blockstates in JAR
            for m in item_audit["models_inspected"]:
                jar_path = f"assets/wingsofthewild/{m}"
                if jar_path not in jar_entries:
                    jar_ok = False
                    item_audit["errors"].append(f"Arquivo ausente no JAR: {jar_path}")
            # Check item definition in JAR
            jar_idef_path = f"assets/wingsofthewild/items/{iid}.json"
            if jar_idef_path not in jar_entries:
                jar_ok = False
                item_audit["errors"].append(f"Definição de item ausente no JAR: {jar_idef_path}")
            # Check textures in JAR
            for t_type, t_name in referenced_textures:
                jar_path = f"assets/wingsofthewild/textures/{t_type}/{t_name}.png"
                if jar_path not in jar_entries:
                    jar_ok = False
                    item_audit["errors"].append(f"Textura ausente no JAR: {jar_path}")

        item_audit["criteria"]["jar_packaged"] = jar_ok

        # Overall Status
        all_passed = all(item_audit["criteria"].values())
        item_audit["passed_all"] = all_passed
        item_audit["status_auditoria"] = "APROVADO (100%)" if all_passed else "REPROVADO"

        report.append(item_audit)

    return report

if __name__ == "__main__":
    report = run_deep_audit()
    
    total = len(report)
    passed = [r for r in report if r["passed_all"]]
    failed = [r for r in report if not r["passed_all"]]
    
    x_items = [r for r in report if r["status_md"] == "X"]
    x_passed = [r for r in x_items if r["passed_all"]]
    x_failed = [r for r in x_items if not r["passed_all"]]

    print(f"============================================================")
    print(f"RESULTADO DETALHADO DA AUDITORIA TÉCNICA (WINGS OF THE WILD)")
    print(f"============================================================")
    print(f"Total de Itens Auditados: {total}")
    print(f"Itens Marcados com [X] em ITENS.md: {len(x_items)}")
    print(f"Itens [X] Aprovados em 100% dos Critérios: {len(x_passed)} / {len(x_items)}")
    print(f"Itens [X] com Falhas: {len(x_failed)}")
    print(f"------------------------------------------------------------")
    print(f"Total de Itens do Mod (1 a {total}) Aprovados em 100%: {len(passed)} / {total}")
    print(f"============================================================")

    if failed:
        print("\nITENS COM REPROVACAO:")
        for f in failed:
            print(f"- [#{f['num']:02d}] {f['id']}: {', '.join(f['errors'])}")
    else:
        print(f"\n>>> TODOS OS {total} ITENS E BLOCOS ESTAO 100% CONFORMES E CERTIFICADOS! <<<")

    # Salva relatório JSON completo
    with open(r"D:\Mine\audit_full_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("\n[OK] Relatorio JSON salvo com sucesso em D:\\Mine\\audit_full_report.json.")
