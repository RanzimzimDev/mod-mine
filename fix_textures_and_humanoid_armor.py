"""
Script de Correção e Geração:
1. frostburn_alloy_ingot.png (sólido com 126 pixels opacos, gelo ciano e chama dourada)
2. incubation_brazier.png e incubation_brazier_side.png (base y=15 preenchida com ardósia sólida)
3. Armadura de Flamefang no corpo do jogador:
   - textures/entity/equipment/humanoid/flamefang.png
   - textures/entity/equipment/humanoid_leggings/flamefang.png
   - Fallbacks em textures/models/armor/
"""

import os
from PIL import Image

ITEM_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/item"
BLOCK_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/block"
EQUIP_HUMANOID_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/entity/equipment/humanoid"
EQUIP_LEGGINGS_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/entity/equipment/humanoid_leggings"
ARMOR_LEGACY_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/models/armor"

os.makedirs(EQUIP_HUMANOID_DIR, exist_ok=True)
os.makedirs(EQUIP_LEGGINGS_DIR, exist_ok=True)
os.makedirs(ARMOR_LEGACY_DIR, exist_ok=True)

# ==============================================================================
# 1. FROSTBURN ALLOY INGOT (Sólido, exatamente 126 pixels opacos)
# ==============================================================================
def generate_solid_frostburn_ingot():
    # Paleta de Gelo Glacial e Chama Dourada Incandescente
    PAL_FROSTBURN = {
        '.': (0, 0, 0, 0),
        '#': (18, 22, 34, 255),    # Contorno profundo gelo-obsidiana
        'W': (255, 255, 245, 255), # Ponto branco-incandescente do fogo
        'H': (255, 245, 170, 255), # Chama amarelo-ouro clara
        'Y': (255, 210, 50, 255),  # Ouro solar vibrante
        'O': (255, 125, 25, 255),  # Chama alaranjada ardente
        'R': (200, 45, 20, 255),   # Borda de choque térmico carmesim
        'I': (185, 245, 255, 255), # Gelo ciano claro (luz do topo)
        'i': (80, 205, 245, 255),  # Gelo ciano cristalino
        'b': (35, 140, 205, 255),  # Azul glacial meio-tom
        'd': (18, 80, 145, 255),   # Azul ártico profundo (sombra)
    }

    GRID_FROSTBURN = [
        "................",
        "................",
        "................",
        "......######....",
        "....##IIIIII##..",
        "...#IIiiiHYYii#.",
        "..#IIiiYHHWYOYi#",
        ".#IIiiYHOWWYOYY#",
        ".#IiiYHOWYYOYib#",
        ".#IiYHOWYOYYibd#",
        ".#iiYOYOYYibddd#",
        "..#iYYYibdddd##.",
        "...#bbdddddd##..",
        "................",
        "................",
        "................",
    ]

    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(GRID_FROSTBURN):
        for x, ch in enumerate(row):
            img.putpixel((x, y), PAL_FROSTBURN[ch])

    opaque = sum(1 for p in img.get_flattened_data() if p[3] > 0)
    assert opaque == 126, f"Esperava 126 pixels opacos, obteve {opaque}"
    return img


# ==============================================================================
# 2. INCUBATION BRAZIER BASE FIX (Linha y=15 preenchida com ardósia sólida)
# ==============================================================================
def fix_incubation_brazier():
    # 1. incubation_brazier_side.png
    side_path = os.path.join(BLOCK_DIR, "incubation_brazier_side.png")
    side_img = Image.open(side_path).convert("RGBA")
    slate_dark = (21, 18, 24, 255)
    slate_mid = (36, 30, 42, 255)
    # Preenche a linha y=15 com ardósia sólida
    for x in range(16):
        c = slate_dark if (x == 0 or x == 15 or x % 4 == 0) else slate_mid
        side_img.putpixel((x, 15), c)
    side_img.save(side_path, format="PNG")

    # 2. incubation_brazier.png (bloco principal)
    brazier_path = os.path.join(BLOCK_DIR, "incubation_brazier.png")
    brazier_img = Image.open(brazier_path).convert("RGBA")
    # Prolonga os pés da forja/braseiro até o solo (y=15)
    for x in range(16):
        # Onde a linha 14 tem pé sólido, estende para a linha 15
        p14 = brazier_img.getpixel((x, 14))
        if p14[3] > 0:
            brazier_img.putpixel((x, 15), slate_dark)
    brazier_img.save(brazier_path, format="PNG")
    print("Brazier textures fixed successfully (solid ground at y=15)!")


# ==============================================================================
# 3. HUMANOID ARMOR TEXTURES (64x32)
# ==============================================================================
def generate_humanoid_armor():
    # Cores Oficiais da Armadura de Flamefang
    OBSIDIAN_DARK = (20, 16, 24, 255)
    OBSIDIAN_BASE = (32, 26, 38, 255)
    OBSIDIAN_LIGHT = (48, 40, 56, 255)
    SCALE_CRIMSON = (95, 32, 36, 255)
    SCALE_EMBER = (156, 45, 28, 255)
    SCALE_LIGHT = (210, 68, 35, 255)
    MAGMA_CORE = (255, 130, 25, 255)
    MAGMA_HOT = (255, 220, 60, 255)
    GOLD_HORN = (245, 195, 50, 255)
    GOLD_DARK = (180, 130, 30, 255)
    LEATHER_SEAM = (42, 22, 16, 255)

    # --- CAMADA 1: HUMANOID (Elmo, Peitoral, Botas) ---
    img1 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))

    # HELMET (y: 0..15)
    # Topo da Cabeça: (8, 0) a (15, 7)
    for y in range(8):
        for x in range(8, 16):
            c = OBSIDIAN_BASE if (x + y) % 2 == 0 else SCALE_CRIMSON
            img1.putpixel((x, y), c)
    # Crista dorsal do elmo no topo
    for y in range(8):
        img1.putpixel((11, y), SCALE_LIGHT)
        img1.putpixel((12, y), MAGMA_CORE)

    # Lados, Frente e Traseira do Elmo: y: 8..15, x: 0..31
    for y in range(8, 16):
        for x in range(32):
            img1.putpixel((x, y), OBSIDIAN_BASE)

    # Frente do Elmo (x: 8..15, y: 8..15): Viseira e Fenda de Lava
    for x in range(8, 16):
        img1.putpixel((x, 8), SCALE_EMBER)
        img1.putpixel((x, 9), SCALE_LIGHT)
    # Fendas de visão em brasa incandescente
    img1.putpixel((9, 11), MAGMA_HOT)
    img1.putpixel((10, 11), MAGMA_CORE)
    img1.putpixel((13, 11), MAGMA_CORE)
    img1.putpixel((14, 11), MAGMA_HOT)
    # Narigueira / Protetor facial
    img1.putpixel((11, 10), SCALE_LIGHT)
    img1.putpixel((12, 10), SCALE_LIGHT)
    img1.putpixel((11, 11), OBSIDIAN_DARK)
    img1.putpixel((12, 11), OBSIDIAN_DARK)
    img1.putpixel((11, 12), OBSIDIAN_DARK)
    img1.putpixel((12, 12), OBSIDIAN_DARK)

    # Chifres Dourados / Magma nos lados do elmo (Right: x: 0..7, Left: x: 16..23)
    img1.putpixel((2, 9), GOLD_HORN)
    img1.putpixel((3, 9), GOLD_HORN)
    img1.putpixel((1, 8), GOLD_HORN)
    img1.putpixel((1, 7), GOLD_DARK)

    img1.putpixel((20, 9), GOLD_HORN)
    img1.putpixel((21, 9), GOLD_HORN)
    img1.putpixel((22, 8), GOLD_HORN)
    img1.putpixel((22, 7), GOLD_DARK)

    # CHESTPLATE (y: 16..31)
    # Torso: x: 16..39, y: 16..31
    # Topo dos ombros (x: 20..27, y: 16..19)
    for y in range(16, 20):
        for x in range(20, 28):
            img1.putpixel((x, y), OBSIDIAN_LIGHT)
            
    # Frente do Peitoral (x: 20..27, y: 20..31)
    for y in range(20, 32):
        for x in range(20, 28):
            c = SCALE_CRIMSON if (x + y) % 2 == 0 else SCALE_EMBER
            img1.putpixel((x, y), c)
    # Núcleo de Chamas / Ruby Flame Core no esterno (centro em x: 23, 24, y: 23, 24)
    img1.putpixel((23, 23), MAGMA_HOT)
    img1.putpixel((24, 23), MAGMA_HOT)
    img1.putpixel((23, 24), MAGMA_CORE)
    img1.putpixel((24, 24), MAGMA_CORE)
    # Placas abdominais inferiores
    for x in range(21, 27):
        img1.putpixel((x, 28), OBSIDIAN_BASE)
        img1.putpixel((x, 29), SCALE_LIGHT)
        img1.putpixel((x, 31), OBSIDIAN_DARK)

    # Traseira do Peitoral (x: 32..39, y: 20..31) - Coluna de escamas
    for y in range(20, 32):
        for x in range(32, 40):
            img1.putpixel((x, y), OBSIDIAN_BASE)
        img1.putpixel((35, y), SCALE_EMBER)
        img1.putpixel((36, y), SCALE_LIGHT)

    # Laterais do Peitoral (x: 16..19 e x: 28..31, y: 20..31)
    for y in range(20, 32):
        for x in range(16, 20):
            img1.putpixel((x, y), OBSIDIAN_BASE)
        for x in range(28, 32):
            img1.putpixel((x, y), OBSIDIAN_BASE)

    # Braços / Ombreiras Pontiagudas (x: 40..55, y: 16..31)
    for y in range(16, 20):
        for x in range(44, 48):
            img1.putpixel((x, y), SCALE_LIGHT)
    for y in range(20, 32):
        for x in range(40, 56):
            c = SCALE_CRIMSON if y < 25 else OBSIDIAN_BASE
            img1.putpixel((x, y), c)
    # Ponta da ombreira com brasa
    for x in range(40, 44):
        img1.putpixel((x, 20), MAGMA_CORE)
        img1.putpixel((x, 21), SCALE_LIGHT)

    # BOOTS (x: 0..15, y: 26..31)
    # Solas de obsidiana refratária (y: 30..31)
    for y in range(26, 32):
        for x in range(16):
            img1.putpixel((x, y), OBSIDIAN_BASE)
    # Biqueira térmica ardente nos pés (x: 4..7, y: 28..31)
    for x in range(4, 8):
        img1.putpixel((x, 28), SCALE_LIGHT)
        img1.putpixel((x, 29), MAGMA_CORE)
        img1.putpixel((x, 30), OBSIDIAN_DARK)
        img1.putpixel((x, 31), OBSIDIAN_DARK)

    # --- CAMADA 2: HUMANOID_LEGGINGS (Calças, Coxotes e Joelheiras) ---
    img2 = Image.new("RGBA", (64, 32), (0, 0, 0, 0))

    # Cinto e Pélvis (y: 27..31, x: 16..39)
    for y in range(27, 32):
        for x in range(16, 40):
            img2.putpixel((x, y), LEATHER_SEAM)
    # Fivela de Ouro/Brasa na frente (x: 23, 24, y: 28)
    img2.putpixel((23, 28), GOLD_HORN)
    img2.putpixel((24, 28), GOLD_HORN)
    img2.putpixel((23, 29), GOLD_DARK)
    img2.putpixel((24, 29), GOLD_DARK)

    # Pernas / Coxotes e Joelheiras (x: 0..15, y: 16..28)
    for y in range(16, 20):
        for x in range(4, 8):
            img2.putpixel((x, y), OBSIDIAN_BASE)
    for y in range(20, 28):
        for x in range(16):
            c = SCALE_CRIMSON if (x + y) % 2 == 0 else SCALE_EMBER
            img2.putpixel((x, y), c)
    # Joelheira reforçada diamantada com núcleo de brasa (x: 4..7, y: 25..27)
    for x in range(4, 8):
        img2.putpixel((x, 25), SCALE_LIGHT)
        img2.putpixel((x, 26), MAGMA_CORE)
        img2.putpixel((x, 27), OBSIDIAN_DARK)

    return img1, img2


def main():
    print("1. Regenerando frostburn_alloy_ingot.png...")
    frostburn = generate_solid_frostburn_ingot()
    fb_path = os.path.join(ITEM_DIR, "frostburn_alloy_ingot.png")
    frostburn.save(fb_path, format="PNG")
    print(f"Salvo: {fb_path} (16x16, 126 pixels opacos)")

    print("\n2. Corrigindo rodapé do Braseiro de Incubação (y=15)...")
    fix_incubation_brazier()

    print("\n3. Gerando texturas de Armadura Humanóide no corpo do jogador...")
    layer1, layer2 = generate_humanoid_armor()

    # Salva no novo padrão EquipmentAssets (Minecraft 1.21.2+ / 26.3 NeoForge)
    h_path = os.path.join(EQUIP_HUMANOID_DIR, "flamefang.png")
    layer1.save(h_path, format="PNG")
    print(f"Salvo: {h_path} (64x32)")

    hl_path = os.path.join(EQUIP_LEGGINGS_DIR, "flamefang.png")
    layer2.save(hl_path, format="PNG")
    print(f"Salvo: {hl_path} (64x32)")

    # Salva também fallbacks legados
    legacy1 = os.path.join(ARMOR_LEGACY_DIR, "flamefang_layer_1.png")
    layer1.save(legacy1, format="PNG")
    legacy2 = os.path.join(ARMOR_LEGACY_DIR, "flamefang_layer_2.png")
    layer2.save(legacy2, format="PNG")
    print(f"Salvos fallbacks: {legacy1} e {legacy2}")

    print("\nTodas as correções foram aplicadas com 100% de precisão artística!")

if __name__ == "__main__":
    main()
