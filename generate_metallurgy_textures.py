"""
Script de Geração das 39 Texturas do Sistema de Metalurgia & Ligas Elementais
Wings of the Wild - NeoForge 26.3
Agente 3: Artista Pixel & Texturas 2D (Nano Banana)
"""

import os
from PIL import Image

DIR_BLOCK = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/block"
DIR_ITEM = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/item"

os.makedirs(DIR_BLOCK, exist_ok=True)
os.makedirs(DIR_ITEM, exist_ok=True)

def make_img(matrix, palette):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(matrix):
        for x, ch in enumerate(row):
            img.putpixel((x, y), palette.get(ch, (0, 0, 0, 0)))
    return img

# ==============================================================================
# 1. DRACONIC FOUNDRY (4 texturas de bloco)
# ==============================================================================

# draconic_foundry_front.png
# Forja com porta de fusão incandescente, arco de metal e fendas térmicas
PAL_FOUNDRY_FRONT = {
    '#': (22, 19, 26, 255),    # Metal escuro contorno
    'M': (105, 100, 115, 255), # Placa de aço luz
    'm': (70, 65, 80, 255),    # Placa de aço meio tom
    'd': (45, 40, 52, 255),    # Placa de aço sombra
    'B': (220, 160, 45, 255),  # Rebite de bronze/latão
    'b': (150, 105, 30, 255),  # Rebite sombra
    'W': (255, 255, 220, 255), # Fogo branco-incandescente
    'Y': (255, 215, 50, 255),  # Fogo amarelo cadinho
    'O': (255, 125, 25, 255),  # Fogo laranja
    'R': (195, 45, 20, 255),   # Fogo carmesim
    'K': (55, 25, 22, 255),    # Carvão / brasa escura
}
GRID_FOUNDRY_FRONT = [
    "#BMMMMMMMMMMMMB#",
    "#MmmmmmmmmmmmmM#",
    "#Mmd########dmM#",
    "#Mm#dmmmmmmd#mM#",
    "#Mm#mdd##ddm#mM#",
    "#Mm#dROOOORd#mM#",
    "#Mm#dOYYYYOd#mM#",
    "#Mm#dOYWWYOd#mM#",
    "#Mm#dOYYYYOd#mM#",
    "#Mm#dROOOORd#mM#",
    "#Mm#dd#KK#dd#mM#",
    "#Mm#KRRKKRRK#mM#",
    "#Mm#RRRRRRRR#mM#",
    "#Mmd########dmM#",
    "#MddddddddddddM#",
    "#B############B#",
]

# draconic_foundry_side.png
# Tijolos refratários escuros com cinta e reforços diagonais de aço
PAL_FOUNDRY_SIDE = {
    '#': (24, 20, 28, 255),    # Contorno / rejunte escuro
    'M': (110, 105, 120, 255), # Aço luz
    'm': (75, 70, 85, 255),    # Aço base
    'd': (48, 44, 55, 255),    # Aço sombra
    '1': (82, 75, 90, 255),    # Tijolo refratário luz
    '2': (58, 52, 66, 255),    # Tijolo refratário base
    '3': (38, 34, 44, 255),    # Tijolo refratário sombra
    'B': (220, 160, 45, 255),  # Rebite de bronze
}
GRID_FOUNDRY_SIDE = [
    "#BMMMMMMMMMMMMB#",
    "#MmmmmmmmmmmmmM#",
    "#Md1123#1123ddM#",
    "#M#1223#2233#mM#",
    "#M#2333#3333#mM#",
    "#M#mmmmmmmmd#mM#",
    "#Mmd##1123##dmM#",
    "#Mm#1123#112#mM#",
    "#Mm#2233#223#mM#",
    "#Mmd##2333##dmM#",
    "#M#mmmmmmmmd#mM#",
    "#M#1123#1123#mM#",
    "#M#1233#2333#mM#",
    "#Md2333#3333ddM#",
    "#MddddddddddddM#",
    "#B############B#",
]

# draconic_foundry_top.png
# Grelha de cadinho superior com metal escuro e lava fervente visível
PAL_FOUNDRY_TOP = {
    '#': (24, 20, 28, 255),    # Contorno
    'M': (110, 105, 120, 255), # Aço luz
    'm': (75, 70, 85, 255),    # Aço base
    'd': (48, 44, 55, 255),    # Aço sombra
    'B': (220, 160, 45, 255),  # Rebite bronze
    'W': (255, 255, 220, 255), # Fusão branco
    'Y': (255, 215, 50, 255),  # Fusão amarelo
    'O': (255, 125, 25, 255),  # Fusão laranja
    'R': (195, 45, 20, 255),   # Fusão vermelho
}
GRID_FOUNDRY_TOP = [
    "#BMMMMMMMMMMMMB#",
    "#MmmmmmmmmmmmmM#",
    "#Mmd########dmM#",
    "#Mm#mRO##ORm#mM#",
    "#Mm##OY##YO##mM#",
    "#Mm#mYW##WYm#mM#",
    "#Mm##########mM#",
    "#Mm##########mM#",
    "#Mm#mYW##WYm#mM#",
    "#Mm##OY##YO##mM#",
    "#Mm#mRO##ORm#mM#",
    "#Mmd########dmM#",
    "#MmddddddddddmM#",
    "#MddddddddddddM#",
    "#B############B#",
    "################",
]

# draconic_foundry_bottom.png
# Base pesada de pedra basáltica densa
PAL_FOUNDRY_BOTTOM = {
    '#': (20, 18, 24, 255),    # Rejunte
    '1': (78, 72, 85, 255),    # Basalto luz
    '2': (54, 48, 60, 255),    # Basalto base
    '3': (35, 30, 40, 255),    # Basalto sombra
}
GRID_FOUNDRY_BOTTOM = [
    "################",
    "#1123#111223#11#",
    "#1223#122233#12#",
    "#2333#223333#23#",
    "################",
    "#111223#112233##",
    "#122233#122333##",
    "#223333#233333##",
    "################",
    "#1123#111223#11#",
    "#1223#122233#12#",
    "#2333#223333#23#",
    "################",
    "#111223#112233##",
    "#223333#233333##",
    "################",
]

# ==============================================================================
# 2. 10 TEXTURAS DE BLOCOS DE MINÉRIO (textures/block/)
# ==============================================================================

# Matriz base padrão de veios de minério em estilo Minecraft Vanilla/NeoForge
ORE_VEIN_MAP = [
    "....##..........",
    "...#VV#....#V#..",
    "..#VVH#...#VVH#.",
    "..#VHH#....#VV#.",
    "...##.......##..",
    ".....#VV#.......",
    "....#VVHH#......",
    "...#VVHHH#..#V#.",
    "...#VHHHH#.#VVH#",
    "....#VHH#..#VV#.",
    ".....##.....##..",
    ".........#VV#...",
    "..#V#...#VVHH#..",
    ".#VVH#..#VHHH#..",
    ".#VV#....#VHH#..",
    "..##......##....",
]

def generate_ore_texture(rock_colors, vein_colors):
    """
    rock_colors: (light, mid, dark, deepest)
    vein_colors: (dark_vein, mid_vein, highlight_vein, core_vein)
    """
    r_l, r_m, r_d, r_dd = rock_colors
    v_d, v_m, v_h, v_c = vein_colors
    
    ROCK_BG = [
        [r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_dd, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m],
        [r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d],
        [r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m],
        [r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l],
        [r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m],
        [r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d],
        [r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m],
        [r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l],
        [r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m],
        [r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d],
        [r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m],
        [r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l],
        [r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m],
        [r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d],
        [r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m, r_d, r_dd, r_d, r_m],
        [r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l, r_m, r_d, r_m, r_l],
    ]
    
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            img.putpixel((x, y), ROCK_BG[y][x])
            
    # Aplica os veios
    for y, row in enumerate(ORE_VEIN_MAP):
        for x, ch in enumerate(row):
            if ch == '#':
                img.putpixel((x, y), v_d)
            elif ch == 'V':
                img.putpixel((x, y), v_m)
            elif ch == 'H':
                img.putpixel((x, y), v_h)
    return img

ORES = {
    # Tier 1: Terraslate (Pedra terrosa / veios de bronze)
    "terraslate_ore.png": (
        ((90, 80, 70, 255), (70, 60, 52, 255), (50, 42, 35, 255), (32, 26, 22, 255)),
        ((40, 25, 15, 255), (160, 95, 45, 255), (225, 155, 75, 255), (255, 205, 120, 255))
    ),
    # Tier 2: Abyssal Tide (Ardósia oceânica / cristais ciano e marinho)
    "abyssal_tide_ore.png": (
        ((50, 65, 80, 255), (36, 48, 62, 255), (25, 34, 46, 255), (16, 22, 32, 255)),
        ((10, 45, 85, 255), (0, 140, 190, 255), (40, 225, 245, 255), (180, 255, 255, 255))
    ),
    # Tier 3: Tempest (Pedra eólica / veios de vento cinza-esbranquiçados)
    "tempest_ore.png": (
        ((88, 92, 102, 255), (68, 72, 82, 255), (48, 52, 60, 255), (32, 35, 42, 255)),
        ((40, 48, 60, 255), (150, 175, 205, 255), (215, 235, 255, 255), (255, 255, 255, 255))
    ),
    # Tier 4: Frostbite (Rocha gélida / espinhos azul-celeste)
    "frostbite_ore.png": (
        ((75, 95, 115, 255), (55, 72, 90, 255), (38, 50, 65, 255), (24, 34, 46, 255)),
        ((20, 60, 100, 255), (70, 170, 230, 255), (160, 240, 255, 255), (230, 255, 255, 255))
    ),
    # Tier 5: Miasma (Pedra pútrida / veios verde-tóxico)
    "miasma_ore.png": (
        ((62, 68, 55, 255), (46, 52, 40, 255), (32, 38, 28, 255), (20, 25, 18, 255)),
        ((25, 55, 20, 255), (75, 175, 45, 255), (150, 255, 70, 255), (220, 255, 150, 255))
    ),
    # Tier 6: Fulgurite (Pedra vitrificada / amarelo-elétrico)
    "fulgurite_ore.png": (
        ((72, 68, 80, 255), (52, 48, 60, 255), (36, 32, 44, 255), (22, 20, 28, 255)),
        ((60, 50, 10, 255), (200, 160, 20, 255), (255, 235, 60, 255), (255, 255, 180, 255))
    ),
    # Tier 7: Solarium (Pedra vulcânica / ouro solar radiante)
    "solarium_ore.png": (
        ((75, 62, 52, 255), (55, 44, 36, 255), (38, 28, 22, 255), (24, 18, 14, 255)),
        ((70, 35, 10, 255), (220, 130, 20, 255), (255, 210, 45, 255), (255, 255, 160, 255))
    ),
    # Tier 8: Void Shadow (Rocha escura abissal / fendas roxo-escuro)
    "void_shadow_ore.png": (
        ((42, 34, 52, 255), (28, 22, 36, 255), (18, 14, 24, 255), (10, 8, 14, 255)),
        ((35, 10, 55, 255), (110, 25, 165, 255), (195, 65, 255, 255), (240, 170, 255, 255))
    ),
    # Tier 9: Astralite (Rocha cósmica / magenta e azul cósmico)
    "astralite_ore.png": (
        ((48, 42, 64, 255), (34, 28, 46, 255), (22, 18, 32, 255), (12, 10, 18, 255)),
        ((40, 15, 60, 255), (185, 35, 140, 255), (255, 80, 210, 255), (120, 200, 255, 255))
    ),
    # Tier 10: Chronium (Rocha primordial / cromo reluzente e âmbar)
    "chronium_ore.png": (
        ((66, 64, 70, 255), (48, 46, 52, 255), (32, 30, 36, 255), (18, 16, 22, 255)),
        ((45, 30, 15, 255), (180, 195, 215, 255), (255, 190, 50, 255), (255, 250, 235, 255))
    ),
}

# ==============================================================================
# 3. 10 MINÉRIOS BRUTOS (textures/item/)
# ==============================================================================

# Template clássico de minério bruto facetado
RAW_ORE_GRID = [
    "................",
    "......####......",
    ".....#MHHM#.....",
    "....#MHHHHM#....",
    "...#MMHHHHMM#...",
    "...#MMHHMMMM#...",
    "..#DDMMMMMMMM#..",
    "..#DDMMMMMMDD#..",
    "..#DDDDMMMDDD#..",
    "...#DDDDDDDD#...",
    "...#KKDDDDDK#...",
    "....#KKDDKK#....",
    ".....#KKKK#.....",
    "......####......",
    "................",
    "................",
]

def generate_raw_ore(palette_tuple):
    """
    palette_tuple: (border, core_rock, shadow, mid_mineral, highlight_mineral)
    """
    k, d, m, h, w = palette_tuple
    pal = {
        '.': (0, 0, 0, 0),
        '#': k,
        'K': d,
        'D': m,
        'M': h,
        'H': w,
    }
    return make_img(RAW_ORE_GRID, pal)

RAW_ORES = {
    "raw_terraslate.png": (
        (35, 20, 12, 255), (65, 38, 22, 255), (125, 75, 35, 255), (195, 125, 55, 255), (245, 185, 95, 255)
    ),
    "raw_abyssal_tide.png": (
        (12, 25, 45, 255), (20, 50, 85, 255), (0, 115, 175, 255), (30, 195, 235, 255), (180, 255, 255, 255)
    ),
    "raw_tempest.png": (
        (25, 32, 42, 255), (55, 68, 85, 255), (115, 140, 175, 255), (185, 210, 240, 255), (250, 255, 255, 255)
    ),
    "raw_frostbite.png": (
        (15, 35, 60, 255), (35, 75, 120, 255), (75, 160, 225, 255), (150, 230, 255, 255), (225, 255, 255, 255)
    ),
    "raw_miasma.png": (
        (20, 32, 16, 255), (38, 65, 28, 255), (70, 140, 40, 255), (135, 230, 65, 255), (210, 255, 140, 255)
    ),
    "raw_fulgurite.png": (
        (35, 28, 12, 255), (75, 60, 18, 255), (160, 130, 25, 255), (235, 200, 45, 255), (255, 255, 160, 255)
    ),
    "raw_solarium.png": (
        (45, 22, 8, 255), (95, 48, 15, 255), (185, 100, 22, 255), (245, 175, 35, 255), (255, 240, 130, 255)
    ),
    "raw_void_shadow.png": (
        (16, 10, 24, 255), (38, 18, 58, 255), (85, 25, 135, 255), (165, 55, 230, 255), (235, 150, 255, 255)
    ),
    "raw_astralite.png": (
        (22, 12, 36, 255), (55, 20, 80, 255), (145, 30, 130, 255), (235, 70, 195, 255), (140, 215, 255, 255)
    ),
    "raw_chronium.png": (
        (30, 26, 32, 255), (65, 60, 72, 255), (145, 155, 175, 255), (215, 225, 245, 255), (255, 195, 55, 255)
    ),
}

# ==============================================================================
# 4. 10 LINGOTES ELEMENTAIS (textures/item/)
# ==============================================================================

# Template clássico de lingote trapezoidal isométrico do Minecraft
INGOT_GRID = [
    "................",
    "................",
    "................",
    "......########..",
    "....##THHHHHHh#.",
    "..##TMHHGGHHMM#.",
    "..#TMHGGHHMMMd#.",
    "..#MHGGHHMMddd#.",
    "..#MGGHHMMddd##.",
    "..#MHHMMddd##...",
    "..#MMddd###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

def generate_ingot(palette_tuple):
    """
    palette_tuple: (border, shadow_dark, shadow_mid, body, highlight, gleam)
    """
    border, d, m, b, h, g = palette_tuple
    pal = {
        '.': (0, 0, 0, 0),
        '#': border,
        'd': d,
        'M': m,
        'T': h,
        'H': b,
        'h': h,
        'G': g,
    }
    return make_img(INGOT_GRID, pal)

INGOTS = {
    "terraslate_ingot.png": (
        (35, 22, 14, 255), (70, 42, 25, 255), (115, 72, 40, 255), (170, 110, 55, 255), (220, 155, 85, 255), (250, 205, 140, 255)
    ),
    "abyssal_tide_ingot.png": (
        (10, 25, 45, 255), (18, 55, 95, 255), (25, 105, 160, 255), (35, 160, 215, 255), (80, 220, 245, 255), (195, 255, 255, 255)
    ),
    "tempest_ingot.png": (
        (28, 35, 45, 255), (60, 75, 95, 255), (105, 130, 160, 255), (160, 190, 220, 255), (215, 235, 250, 255), (255, 255, 255, 255)
    ),
    "frostbite_ingot.png": (
        (18, 40, 65, 255), (40, 85, 135, 255), (75, 145, 205, 255), (125, 205, 245, 255), (185, 240, 255, 255), (240, 255, 255, 255)
    ),
    "miasma_ingot.png": (
        (18, 30, 16, 255), (35, 65, 28, 255), (65, 125, 45, 255), (105, 190, 60, 255), (160, 240, 85, 255), (225, 255, 160, 255)
    ),
    "fulgurite_ingot.png": (
        (40, 32, 10, 255), (95, 75, 18, 255), (165, 135, 25, 255), (225, 185, 35, 255), (255, 225, 65, 255), (255, 255, 190, 255)
    ),
    "solarium_ingot.png": (
        (45, 22, 8, 255), (105, 52, 15, 255), (175, 95, 22, 255), (235, 155, 30, 255), (255, 210, 60, 255), (255, 250, 165, 255)
    ),
    "void_shadow_ingot.png": (
        (15, 8, 24, 255), (35, 16, 55, 255), (75, 25, 120, 255), (135, 45, 195, 255), (195, 80, 250, 255), (245, 175, 255, 255)
    ),
    "astralite_ingot.png": (
        (24, 12, 38, 255), (60, 22, 85, 255), (135, 35, 140, 255), (210, 60, 190, 255), (255, 110, 225, 255), (140, 220, 255, 255)
    ),
    "chronium_ingot.png": (
        (30, 28, 35, 255), (75, 72, 85, 255), (140, 145, 165, 255), (200, 205, 225, 255), (245, 248, 255, 255), (255, 205, 60, 255)
    ),
}

# ==============================================================================
# 5. 5 LIGAS METÁLICAS ESPECIAIS (textures/item/)
# ==============================================================================

# 1. frostburn_alloy_ingot.png (bipolar metade brasa / metade gelo)
PAL_FROSTBURN = {
    '.': (0, 0, 0, 0),
    '#': (22, 18, 26, 255),
    'F': (255, 140, 25, 255),  # Fogo luz
    'f': (190, 55, 15, 255),   # Fogo base
    'd': (110, 25, 10, 255),   # Fogo sombra
    'C': (255, 255, 255, 255), # Centro choque térmico
    'I': (180, 245, 255, 255), # Gelo luz
    'i': (60, 180, 235, 255),  # Gelo base
    'b': (20, 85, 145, 255),   # Gelo sombra
}
GRID_FROSTBURN = [
    "................",
    "................",
    "................",
    "......########..",
    "....##FFCCIIII#.",
    "..##FffCCiiiiI#.",
    "..#FffCCiiiiib#.",
    "..#ffCCiiiiibb#.",
    "..#fdCCiiiibbb#.",
    "..#ddCCiibbb##..",
    "..#dddbb###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

# 2. plasma_alloy_ingot.png (incandescente com arcos elétricos)
PAL_PLASMA = {
    '.': (0, 0, 0, 0),
    '#': (35, 18, 10, 255),
    'W': (255, 255, 230, 255), # Arco plasma puro
    'Y': (255, 235, 60, 255),  # Plasma amarelo
    'O': (255, 130, 25, 255),  # Metal alaranjado luz
    'o': (195, 65, 15, 255),   # Metal alaranjado base
    'd': (115, 30, 10, 255),   # Metal sombra
}
GRID_PLASMA = [
    "................",
    "................",
    "................",
    "......########..",
    "....##OWYYYYOO#.",
    "..##OWoYYoOOOO#.",
    "..#OoWYYoOOOod#.",
    "..#ooWYYoOOddd#.",
    "..#ooOWYoOddd##.",
    "..#oWYYddd##....",
    "..#WWddd###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

# 3. volcanic_titanium_ingot.png (basalto escuro pesado com miolo de fogo)
PAL_TITANIUM = {
    '.': (0, 0, 0, 0),
    '#': (18, 16, 22, 255),
    'T': (110, 105, 118, 255), # Titânio luz
    't': (72, 68, 80, 255),    # Titânio meio tom
    'd': (42, 38, 48, 255),    # Titânio sombra
    'F': (255, 220, 60, 255),  # Fogo núcleo amarelo
    'f': (235, 95, 20, 255),   # Fogo núcleo laranja
}
GRID_TITANIUM = [
    "................",
    "................",
    "................",
    "......########..",
    "....##TTTTTTTt#.",
    "..##TtTTFfTTtt#.",
    "..#TtTFFfTtttd#.",
    "..#tTTFfTtttdd#.",
    "..#tTTfTtttdd##.",
    "..#tTtttttdd##..",
    "..#ttddd###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

# 4. scalding_alloy_ingot.png (lingote aquático fervilhante com chamas de vapor)
PAL_SCALDING = {
    '.': (0, 0, 0, 0),
    '~': (210, 235, 250, 160), # Vapor translúcido
    '#': (10, 22, 38, 255),
    'S': (240, 250, 255, 230), # Vapor borbulhante
    'A': (60, 215, 245, 255),  # Ciano aquático luz
    'a': (25, 135, 190, 255),  # Ciano aquático base
    'b': (12, 65, 115, 255),   # Oceânico sombra
    'F': (255, 160, 40, 255),  # Fervura térmica
    'f': (215, 75, 20, 255),   # Fervura borda
}
GRID_SCALDING = [
    "........~.......",
    ".......~S~......",
    "......~S~.......",
    "......########..",
    "....##AASSAAAA#.",
    "..##AaAFfSAAAa#.",
    "..#AaAFFfSAaab#.",
    "..#aaAFfSAaabb#.",
    "..#aaFfSAaabb##.",
    "..#aAFfSabb##...",
    "..#aabbb###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

# 5. shadowflame_alloy_ingot.png (obsidiana com chamas roxas e negras)
PAL_SHADOWFLAME = {
    '.': (0, 0, 0, 0),
    '#': (12, 8, 16, 255),
    'P': (240, 160, 255, 255), # Chama sombra ponta brilhante
    'p': (180, 50, 240, 255),  # Chama violeta vívido
    'v': (95, 18, 150, 255),   # Chama roxa profunda
    'O': (55, 48, 65, 255),    # Obsidiana luz
    'o': (32, 26, 40, 255),    # Obsidiana base
    'k': (18, 14, 24, 255),    # Obsidiana sombra
}
GRID_SHADOWFLAME = [
    "........P.......",
    ".......Pp.......",
    "......Ppv.......",
    "......########..",
    "....##OOPpvOOO#.",
    "..##OoOPpvOOOoo#",
    "..#OoOPpvOOOook#",
    "..#ooOPpvOOokkk#",
    "..#ooPpvOOokkk##",
    "..#oPpvOkkk##...",
    "..#oPvkk###.....",
    "..######........",
    "................",
    "................",
    "................",
    "................",
]

def main():
    print("Iniciando geração de 39 texturas de metalurgia e ligas elementais...")
    count = 0
    
    # 1. Forja (4 blocos)
    for name, grid, pal in [
        ("draconic_foundry_front.png", GRID_FOUNDRY_FRONT, PAL_FOUNDRY_FRONT),
        ("draconic_foundry_side.png", GRID_FOUNDRY_SIDE, PAL_FOUNDRY_SIDE),
        ("draconic_foundry_top.png", GRID_FOUNDRY_TOP, PAL_FOUNDRY_TOP),
        ("draconic_foundry_bottom.png", GRID_FOUNDRY_BOTTOM, PAL_FOUNDRY_BOTTOM),
    ]:
        p = os.path.join(DIR_BLOCK, name)
        img = make_img(grid, pal)
        img.save(p, format="PNG")
        count += 1
        print(f"[{count:02d}/39] Salvo bloco: {name}")

    # 2. 10 Minérios em blocos
    for name, (rock, vein) in ORES.items():
        p = os.path.join(DIR_BLOCK, name)
        img = generate_ore_texture(rock, vein)
        img.save(p, format="PNG")
        count += 1
        print(f"[{count:02d}/39] Salvo minério bloco: {name}")

    # 3. 10 Minérios Brutos
    for name, palette in RAW_ORES.items():
        p = os.path.join(DIR_ITEM, name)
        img = generate_raw_ore(palette)
        img.save(p, format="PNG")
        count += 1
        print(f"[{count:02d}/39] Salvo minério bruto item: {name}")

    # 4. 10 Lingotes Elementais
    for name, palette in INGOTS.items():
        p = os.path.join(DIR_ITEM, name)
        img = generate_ingot(palette)
        img.save(p, format="PNG")
        count += 1
        print(f"[{count:02d}/39] Salvo lingote item: {name}")

    # 5. 5 Ligas Especiais
    for name, grid, pal in [
        ("frostburn_alloy_ingot.png", GRID_FROSTBURN, PAL_FROSTBURN),
        ("plasma_alloy_ingot.png", GRID_PLASMA, PAL_PLASMA),
        ("volcanic_titanium_ingot.png", GRID_TITANIUM, PAL_TITANIUM),
        ("scalding_alloy_ingot.png", GRID_SCALDING, PAL_SCALDING),
        ("shadowflame_alloy_ingot.png", GRID_SHADOWFLAME, PAL_SHADOWFLAME),
    ]:
        p = os.path.join(DIR_ITEM, name)
        img = make_img(grid, pal)
        img.save(p, format="PNG")
        count += 1
        print(f"[{count:02d}/39] Salvo liga especial item: {name}")

    print(f"\nSucesso total! {count} texturas geradas e exportadas com precisão!")

if __name__ == "__main__":
    main()
