import os
import json

base_loot = r"D:\Mine\src\main\resources\data\wingsofthewild\loot_table\blocks"
os.makedirs(base_loot, exist_ok=True)

# Mapeamento dos minérios e o item bruto que dropam com fortuna / silk touch
ore_drops = {
    "ember_ore": "raw_ember",
    "deepslate_ember_ore": "raw_ember",
    "terraslate_ore": "raw_terraslate",
    "abyssal_tide_ore": "raw_abyssal_tide",
    "tempest_ore": "raw_tempest",
    "frostbite_ore": "raw_frostbite",
    "miasma_ore": "raw_miasma",
    "fulgurite_ore": "raw_fulgurite",
    "solarium_ore": "raw_solarium",
    "void_shadow_ore": "raw_void_shadow",
    "astralite_ore": "raw_astralite",
    "chronium_ore": "raw_chronium"
}

# Todos os outros blocos que dropam a si mesmos
self_drop_blocks = [
    "dragon_nest",
    "draconic_hearth",
    "tack_workbench",
    "incubation_brazier",
    "draconic_anvil",
    "raw_ember_block",
    "draconic_stone",
    "draconic_stone_bricks",
    "chiseled_draconic_bricks",
    "ember_lantern",
    "draconic_brazier_standing",
    "flamefang_trophy_skull",
    "charred_nest_straw",
    "dragon_perch",
    "draconic_foundry"
]

def make_ore_loot(block_name, drop_item):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "rolls": 1.0,
                "entries": [
                    {
                        "type": "minecraft:alternatives",
                        "children": [
                            {
                                "type": "minecraft:item",
                                "name": f"wingsofthewild:{block_name}",
                                "conditions": [
                                    {
                                        "condition": "minecraft:match_tool",
                                        "predicate": {
                                            "predicates": {
                                                "minecraft:enchantments": [
                                                    {
                                                        "enchantments": "minecraft:silk_touch",
                                                        "levels": {
                                                            "min": 1
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "minecraft:item",
                                "name": f"wingsofthewild:{drop_item}",
                                "functions": [
                                    {
                                        "function": "minecraft:apply_bonus",
                                        "enchantment": "minecraft:fortune",
                                        "formula": "minecraft:ore_drops"
                                    },
                                    {
                                        "function": "minecraft:explosion_decay"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "random_sequence": f"wingsofthewild:blocks/{block_name}"
    }

def make_self_drop_loot(block_name):
    return {
        "type": "minecraft:block",
        "pools": [
            {
                "rolls": 1.0,
                "conditions": [
                    {
                        "condition": "minecraft:survives_explosion"
                    }
                ],
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": f"wingsofthewild:{block_name}"
                    }
                ]
            }
        ],
        "random_sequence": f"wingsofthewild:blocks/{block_name}"
    }

# Gerar para minérios
for block_name, drop_item in ore_drops.items():
    fpath = os.path.join(base_loot, f"{block_name}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(make_ore_loot(block_name, drop_item), f, indent=2)
    print("Gerado loot table ore:", block_name)

# Gerar para blocos normais
for block_name in self_drop_blocks:
    fpath = os.path.join(base_loot, f"{block_name}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(make_self_drop_loot(block_name), f, indent=2)
    print("Gerado loot table self:", block_name)

print("Todas as 27 tabelas de loot de blocos foram geradas com sucesso!")
