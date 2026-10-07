import os, glob, json, re

# 1. Carregar IDs válidos registrados no Java
blocks_code = open('src/main/java/com/wingsofthewild/init/ModBlocks.java', encoding='utf-8').read()
items_code = open('src/main/java/com/wingsofthewild/init/ModItems.java', encoding='utf-8').read()

registered_blocks = set(re.findall(r'registerBlock\(["\']([^"\']+)["\']', blocks_code))
registered_items = set(re.findall(r'register(?:Simple)?Item\(["\']([^"\']+)["\']', items_code))
all_registered = registered_blocks | registered_items

print(f"Total registrados no ModBlocks: {len(registered_blocks)}")
print(f"Total registrados no ModItems: {len(registered_items)}")
print(f"Total único registrado: {len(all_registered)}")

# Mapeamento do ITENS.md para ver os nomes reais
itens_md = open('ITENS.md', encoding='utf-8').read()
item_rows = re.findall(r'\|\s*\*\*(\d+)\*\*\s*\|\s*`([^`]+)`', itens_md)
md_map = {row[1]: int(row[0]) for row in item_rows}

# 2. Auditar cada receita em data/wingsofthewild/recipe/
recipe_files = glob.glob('src/main/resources/data/wingsofthewild/recipe/*.json')
print(f"Total de receitas: {len(recipe_files)}")

issues = []

for rpath in recipe_files:
    fname = os.path.basename(rpath)
    with open(rpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Checar result
    result = data.get('result', {})
    res_id = result.get('id', '') if isinstance(result, dict) else (result if isinstance(result, str) else '')
    if res_id.startswith('wingsofthewild:'):
        item_name = res_id.split(':')[1]
        if item_name not in all_registered:
            issues.append((fname, 'RESULT_UNKNOWN', res_id))
            
    # Checar key (crafting_shaped)
    key_dict = data.get('key', {})
    for k, val in key_dict.items():
        val_str = val if isinstance(val, str) else (val.get('item', '') if isinstance(val, dict) else '')
        if val_str.startswith('wingsofthewild:'):
            item_name = val_str.split(':')[1]
            if item_name not in all_registered:
                issues.append((fname, f'KEY_{k}_UNKNOWN', val_str))
                
    # Checar ingredients (crafting_shapeless, smelting, blasting)
    ingredients = list(data.get('ingredients', []))
    if isinstance(data.get('ingredient'), dict):
        ingredients.append(data.get('ingredient'))
    elif isinstance(data.get('ingredient'), str):
        ingredients.append(data.get('ingredient'))
        
    for ing in ingredients:
        ing_str = ing if isinstance(ing, str) else (ing.get('item', '') if isinstance(ing, dict) else '')
        if ing_str.startswith('wingsofthewild:'):
            item_name = ing_str.split(':')[1]
            if item_name not in all_registered:
                issues.append((fname, 'ING_UNKNOWN', ing_str))

print("\n--- PROBLEMAS ENCONTRADOS NAS RECEITAS ---")
unknown_names = set()
for fname, err, val in issues:
    name = val.split(':')[1]
    unknown_names.add(name)
    print(f"[{fname}] {err}: {val}")

print("\n--- NOMES DESCONHECIDOS ---")
for u in sorted(unknown_names):
    # Tenta achar parecido em all_registered
    similar = [r for r in all_registered if any(part in r for part in u.split('_'))]
    print(f"Desconhecido: {u} -> Registrados parecidos: {similar}")
