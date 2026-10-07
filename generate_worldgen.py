import os
import json

base_data = r"D:\Mine\src\main\resources\data\wingsofthewild"
feat_dir = os.path.join(base_data, "worldgen", "feature")
placed_dir = os.path.join(base_data, "worldgen", "placed_feature")
biome_mod_dir = os.path.join(base_data, "neoforge", "biome_modifier")

os.makedirs(feat_dir, exist_ok=True)
os.makedirs(placed_dir, exist_ok=True)
os.makedirs(biome_mod_dir, exist_ok=True)

# Minérios do mod
ores = [
    ("ore_ember", "ember_ore", "deepslate_ember_ore", 8, 12, -32, 80),
    ("ore_terraslate", "terraslate_ore", "terraslate_ore", 7, 8, -16, 64),
    ("ore_abyssal_tide", "abyssal_tide_ore", "abyssal_tide_ore", 6, 6, -48, 48),
    ("ore_tempest", "tempest_ore", "tempest_ore", 6, 6, 0, 128),
    ("ore_frostbite", "frostbite_ore", "frostbite_ore", 6, 6, -32, 96),
    ("ore_miasma", "miasma_ore", "miasma_ore", 5, 5, -60, 20),
    ("ore_fulgurite", "fulgurite_ore", "fulgurite_ore", 5, 5, -16, 112),
    ("ore_solarium", "solarium_ore", "solarium_ore", 4, 4, 32, 160),
    ("ore_void_shadow", "void_shadow_ore", "void_shadow_ore", 4, 4, -64, -16),
    ("ore_astralite", "astralite_ore", "astralite_ore", 3, 3, -64, 256),
    ("ore_chronium", "chronium_ore", "chronium_ore", 3, 3, -64, 32)
]

placed_features_list = []

for feat_name, stone_block, deep_block, size, count, min_y, max_y in ores:
    # 1. Feature
    feature_json = {
        "type": "minecraft:ore",
        "discard_chance_on_air_exposure": 0.0,
        "size": size,
        "targets": [
            {
                "state": {
                    "name": f"wingsofthewild:{stone_block}"
                },
                "target": {
                    "predicate_type": "minecraft:tag_match",
                    "tag": "minecraft:stone_ore_replaceables"
                }
            },
            {
                "state": {
                    "name": f"wingsofthewild:{deep_block}"
                },
                "target": {
                    "predicate_type": "minecraft:tag_match",
                    "tag": "minecraft:deepslate_ore_replaceables"
                }
            }
        ]
    }
    with open(os.path.join(feat_dir, f"{feat_name}.json"), "w", encoding="utf-8") as f:
        json.dump(feature_json, f, indent=2)

    # 2. Placed Feature
    placed_json = {
        "feature": f"wingsofthewild:{feat_name}",
        "placement": [
            {
                "type": "minecraft:count",
                "count": count
            },
            {
                "type": "minecraft:in_square"
            },
            {
                "type": "minecraft:height_range",
                "height": {
                    "type": "minecraft:uniform",
                    "max_inclusive": {
                        "absolute": max_y
                    },
                    "min_inclusive": {
                        "absolute": min_y
                    }
                }
            },
            {
                "type": "minecraft:biome"
            }
        ]
    }
    with open(os.path.join(placed_dir, f"{feat_name}.json"), "w", encoding="utf-8") as f:
        json.dump(placed_json, f, indent=2)

    placed_features_list.append(f"wingsofthewild:{feat_name}")
    print(f"Gerado worldgen: {feat_name}")

# 3. Geração Natural do Ninho Dracônico (dragon_nest na superfície)
nest_feature_json = {
    "type": "minecraft:simple_block",
    "to_place": {
        "type": "minecraft:simple_state_provider",
        "state": {
            "name": "wingsofthewild:dragon_nest"
        }
    }
}
with open(os.path.join(feat_dir, "dragon_nest.json"), "w", encoding="utf-8") as f:
    json.dump(nest_feature_json, f, indent=2)

nest_placed_json = {
    "feature": "wingsofthewild:dragon_nest",
    "placement": [
        {
            "type": "minecraft:rarity_filter",
            "chance": 32  # Raro, 1 a cada 32 chunks
        },
        {
            "type": "minecraft:in_square"
        },
        {
            "type": "minecraft:heightmap",
            "heightmap": "WORLD_SURFACE_WG"
        },
        {
            "type": "minecraft:biome"
        }
    ]
}
with open(os.path.join(placed_dir, "dragon_nest.json"), "w", encoding="utf-8") as f:
    json.dump(nest_placed_json, f, indent=2)

placed_features_list.append("wingsofthewild:dragon_nest")
print("Gerado worldgen: dragon_nest")

# 4. Biome Modifiers para Overworld
biome_modifier_ores = {
    "type": "neoforge:add_features",
    "biomes": "#minecraft:is_overworld",
    "features": [f for f in placed_features_list if f != "wingsofthewild:dragon_nest"],
    "step": "underground_ores"
}
with open(os.path.join(biome_mod_dir, "add_draconic_ores.json"), "w", encoding="utf-8") as f:
    json.dump(biome_modifier_ores, f, indent=2)

biome_modifier_nests = {
    "type": "neoforge:add_features",
    "biomes": "#minecraft:is_overworld",
    "features": "wingsofthewild:dragon_nest",
    "step": "surface_structures"
}
with open(os.path.join(biome_mod_dir, "add_dragon_nests.json"), "w", encoding="utf-8") as f:
    json.dump(biome_modifier_nests, f, indent=2)

print("Todos os Biome Modifiers gerados com sucesso!")
