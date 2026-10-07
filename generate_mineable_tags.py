import os
import json

base_tags = r"D:\Mine\src\main\resources\data\minecraft\tags\block"
mineable_tags = os.path.join(base_tags, "mineable")
os.makedirs(mineable_tags, exist_ok=True)

# Pickaxe mineable (todos os minerios, blocos de pedra e metal)
pickaxe_blocks = [
    "wingsofthewild:ember_ore",
    "wingsofthewild:deepslate_ember_ore",
    "wingsofthewild:terraslate_ore",
    "wingsofthewild:abyssal_tide_ore",
    "wingsofthewild:tempest_ore",
    "wingsofthewild:frostbite_ore",
    "wingsofthewild:miasma_ore",
    "wingsofthewild:fulgurite_ore",
    "wingsofthewild:solarium_ore",
    "wingsofthewild:void_shadow_ore",
    "wingsofthewild:astralite_ore",
    "wingsofthewild:chronium_ore",
    "wingsofthewild:raw_ember_block",
    "wingsofthewild:draconic_stone",
    "wingsofthewild:draconic_stone_bricks",
    "wingsofthewild:chiseled_draconic_bricks",
    "wingsofthewild:ember_lantern",
    "wingsofthewild:draconic_brazier_standing",
    "wingsofthewild:draconic_hearth",
    "wingsofthewild:draconic_anvil",
    "wingsofthewild:incubation_brazier",
    "wingsofthewild:dragon_perch",
    "wingsofthewild:draconic_foundry"
]

# Axe mineable (madeira)
axe_blocks = [
    "wingsofthewild:tack_workbench"
]

# Hoe / Shovel mineable (palha e ninho)
hoe_blocks = [
    "wingsofthewild:dragon_nest",
    "wingsofthewild:charred_nest_straw"
]

# Tool tiers
needs_stone = [
    "wingsofthewild:ember_ore",
    "wingsofthewild:terraslate_ore",
    "wingsofthewild:draconic_stone",
    "wingsofthewild:draconic_stone_bricks",
    "wingsofthewild:chiseled_draconic_bricks"
]

needs_iron = [
    "wingsofthewild:deepslate_ember_ore",
    "wingsofthewild:abyssal_tide_ore",
    "wingsofthewild:tempest_ore",
    "wingsofthewild:frostbite_ore",
    "wingsofthewild:miasma_ore",
    "wingsofthewild:fulgurite_ore",
    "wingsofthewild:raw_ember_block",
    "wingsofthewild:draconic_hearth",
    "wingsofthewild:incubation_brazier",
    "wingsofthewild:draconic_anvil",
    "wingsofthewild:draconic_foundry"
]

needs_diamond = [
    "wingsofthewild:solarium_ore",
    "wingsofthewild:void_shadow_ore",
    "wingsofthewild:astralite_ore",
    "wingsofthewild:chronium_ore"
]

def write_tag(path, values):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"replace": False, "values": values}, f, indent=2)

write_tag(os.path.join(mineable_tags, "pickaxe.json"), pickaxe_blocks)
write_tag(os.path.join(mineable_tags, "axe.json"), axe_blocks)
write_tag(os.path.join(mineable_tags, "hoe.json"), hoe_blocks)
write_tag(os.path.join(base_tags, "needs_stone_tool.json"), needs_stone)
write_tag(os.path.join(base_tags, "needs_iron_tool.json"), needs_iron)
write_tag(os.path.join(base_tags, "needs_diamond_tool.json"), needs_diamond)

print("Todas as tags de mineração geradas com sucesso!")
