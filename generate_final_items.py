"""
Script para desenhar pixel a pixel as texturas dos itens 59 a 80
do mod Wings of the Wild para Minecraft 26.3 NeoForge.
Agente 3 - Artista Pixel & Texturas 2D (Nano Banana)
"""

import os
from PIL import Image

OUTPUT_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/item"

def create_item_image(pixel_matrix, palette):
    """
    Cria uma imagem 16x16 RGBA a partir de uma matriz de 16 strings (cada uma com 16 chars)
    e um dicionário mapeando cada caractere para (R, G, B, A).
    """
    assert len(pixel_matrix) == 16, f"Esperava 16 linhas, recebeu {len(pixel_matrix)}"
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(pixel_matrix):
        assert len(row) == 16, f"Linha {y} deve ter 16 caracteres, tem {len(row)}: '{row}'"
        for x, char in enumerate(row):
            color = palette.get(char, (0, 0, 0, 0))
            img.putpixel((x, y), color)
    return img

ITEMS = {}

# ==============================================================================
# 59. flamefang_helmet (Elmo de Escamas de Flamefang)
# Capacete dracônico com chifres, viseira de brasa e escamas de obsidiana
# ==============================================================================
PAL_HELMET = {
    '.': (0, 0, 0, 0),
    '#': (22, 19, 28, 255),    # Contorno obsidiana escuro
    'H': (255, 215, 70, 255),   # Ponta do chifre incandescente / ouro
    'h': (230, 110, 30, 255),   # Chifre brasa média
    'b': (150, 50, 20, 255),    # Chifre base / osso queimado
    '1': (45, 25, 30, 255),     # Sombra profunda de escama
    '2': (84, 31, 35, 255),     # Escama corpo base
    '3': (140, 43, 30, 255),    # Escama tom médio carmesim
    '4': (186, 60, 36, 255),    # Escama luz
    'E': (255, 225, 80, 255),   # Olho/fenda viseira brilhante
    'e': (255, 120, 20, 255),   # Olho/fenda brilho térmico
}
GRID_HELMET = [
    ".H............H.",
    ".#h..........h#.",
    ".#hb########bh#.",
    "..#443333334#...",
    ".#44432223444#..",
    ".#43321112334#..",
    ".#33##1111##3#..",
    ".#3#Ee#11#Ee#3#.",
    ".#2#ee#11#ee#2#.",
    ".#22##1111##22#.",
    "..#222####222#..",
    "..#21#....#12#..",
    "...#1#....#1#...",
    "...#1#....#1#...",
    "....##....##....",
    "................",
]
ITEMS["flamefang_helmet.png"] = (GRID_HELMET, PAL_HELMET)

# ==============================================================================
# 60. flamefang_chestplate (Peitoral de Escamas de Flamefang)
# Ombreiras pontiagudas, escamas sobrepostas e núcleo de brasa no peito
# ==============================================================================
PAL_CHEST = {
    '.': (0, 0, 0, 0),
    '#': (22, 19, 28, 255),    # Contorno obsidiana
    '1': (42, 22, 28, 255),    # Sombra de escama
    '2': (80, 28, 32, 255),    # Tom base
    '3': (135, 42, 30, 255),   # Meio tom
    '4': (185, 62, 35, 255),   # Brilho de escama
    'C': (255, 235, 90, 255),  # Centro da gema de brasa (núcleo)
    'c': (255, 130, 30, 255),  # Borda da gema
    'r': (180, 30, 20, 255),   # Engaste rubi
}
GRID_CHEST = [
    ".##........##...",
    "#43#......#43#..",
    "#443#....#443#..",
    "#4443####4443#..",
    ".#4432112344#...",
    ".#3321cc1233#...",
    "..#21rCCr12#....",
    "..#32rCCr23#....",
    "..#431cc134#....",
    "..#44322344#....",
    "..#34322343#....",
    "...#332233#.....",
    "...#232232#.....",
    "....#2112#......",
    ".....####.......",
    "................",
]
ITEMS["flamefang_chestplate.png"] = (GRID_CHEST, PAL_CHEST)

# ==============================================================================
# 61. flamefang_leggings (Calças de Escamas de Flamefang)
# Cinto com fivela de brasa, placas de coxa e joelheiras reforçadas
# ==============================================================================
PAL_LEGGINGS = {
    '.': (0, 0, 0, 0),
    '#': (22, 19, 28, 255),    # Contorno
    'B': (255, 190, 50, 255),  # Fivela de brasa / ouro
    'b': (180, 110, 30, 255),  # Borda fivela
    '1': (42, 22, 28, 255),    # Sombra
    '2': (78, 28, 32, 255),    # Base
    '3': (135, 42, 30, 255),   # Meio tom
    '4': (185, 62, 35, 255),   # Destaque
    'k': (255, 120, 25, 255),  # Destaque de joelheira
}
GRID_LEGGINGS = [
    "...########.....",
    "..#433bBBb3#....",
    ".#4432bBBb23#...",
    ".#43211111234#..",
    ".#432#1111#234#.",
    ".#321#....#123#.",
    ".#321#....#123#.",
    ".#432#....#124#.",
    ".#3k2#....#1k3#.",
    ".#432#....#124#.",
    ".#321#....#123#.",
    ".#321#....#123#.",
    ".#211#....#112#.",
    ".#211#....#112#.",
    "..###......###..",
    "................",
]
ITEMS["flamefang_leggings.png"] = (GRID_LEGGINGS, PAL_LEGGINGS)

# ==============================================================================
# 62. flamefang_boots (Botas de Escamas de Flamefang)
# Botas térmicas de escamas com solado isolante de obsidiana e pontas de brasa
# ==============================================================================
PAL_BOOTS = {
    '.': (0, 0, 0, 0),
    '#': (22, 19, 28, 255),    # Contorno
    '1': (40, 22, 28, 255),    # Sombra
    '2': (76, 28, 32, 255),    # Base
    '3': (135, 42, 30, 255),   # Meio tom
    '4': (185, 62, 35, 255),   # Luz
    'F': (255, 140, 30, 255),  # Pique de calor na biqueira
    'f': (210, 70, 20, 255),   # Transição térmica
    'S': (55, 50, 60, 255),    # Sola isolante
}
GRID_BOOTS = [
    "................",
    "................",
    "................",
    "................",
    "..####....####..",
    ".#4332#..#4332#.",
    ".#4321#..#4321#.",
    ".#4321#..#4321#.",
    ".#4321#..#4321#.",
    ".#4321#..#4321#.",
    "#43211#..#43211#",
    "#43211###432111#",
    "#Ff3211#Ff32111#",
    "#SSSSSS##SSSSSS#",
    ".######..######.",
    "................",
]
ITEMS["flamefang_boots.png"] = (GRID_BOOTS, PAL_BOOTS)

# ==============================================================================
# 63. dragon_handler_gloves (Luvas de Domador Reforçadas)
# Par de luvas de couro curtido resistente com placas de escamas térmicas e fivela
# ==============================================================================
PAL_GLOVES = {
    '.': (0, 0, 0, 0),
    '#': (32, 18, 12, 255),    # Contorno couro escuro
    'L': (186, 136, 62, 255),  # Couro destaque
    'l': (140, 85, 38, 255),   # Couro meio tom
    'd': (85, 45, 20, 255),    # Couro sombra
    'G': (255, 200, 50, 255),  # Fivela de latão / ouro
    'g': (190, 130, 30, 255),  # Borda da fivela
    'S': (160, 45, 30, 255),   # Placa de escama térmica
    's': (90, 25, 25, 255),    # Sombra da escama térmica
}
GRID_GLOVES = [
    "................",
    "................",
    ".####......####.",
    "#LLll#....#LLll#",
    "#Lllld#..#Lllld#",
    "#gGGg#....#gGGg#",
    "#Lllld#..#Lllld#",
    "#LSSsd#..#LSSsd#",
    "#LSSsd#..#LSSsd#",
    "#lllld#..#lllld#",
    "#ll#ld#..#ll#ld#",
    "#ll##d#..#ll##d#",
    ".#ld##....#ld##.",
    "..##.......##...",
    "................",
    "................",
]
ITEMS["dragon_handler_gloves.png"] = (GRID_GLOVES, PAL_GLOVES)

# ==============================================================================
# 64. dragon_riders_cloak (Capa do Cavaleiro de Dragão)
# Capa esvoaçante carmesim com broche de garra de dragão e barra recortada
# ==============================================================================
PAL_CLOAK = {
    '.': (0, 0, 0, 0),
    '#': (25, 14, 20, 255),    # Contorno
    'G': (255, 215, 60, 255),  # Broche de ouro
    'g': (190, 140, 30, 255),  # Sombra do broche
    'F': (220, 195, 165, 255), # Pelo / colarinho de lã
    'f': (160, 135, 110, 255), # Sombra do colarinho
    '1': (60, 18, 25, 255),    # Sombra profunda da capa
    '2': (105, 24, 32, 255),   # Carmesim escuro
    '3': (165, 38, 38, 255),   # Carmesim vívido
    '4': (215, 65, 45, 255),   # Destaque de dobra no vento
    'E': (255, 175, 40, 255),  # Bordado dourado da barra
}
GRID_CLOAK = [
    "......####......",
    ".....#gGGg#.....",
    "....#FffffF#....",
    "...#F333333F#...",
    "..#443322211#...",
    "..#433221111#...",
    ".#44332211111#..",
    ".#43322111111#..",
    ".#443322111111#.",
    "#4433221111111#.",
    "#4332211#11111#.",
    "#E#321#E##11#E#.",
    "###21###..###.#.",
    "..###...........",
    "................",
    "................",
]
ITEMS["dragon_riders_cloak.png"] = (GRID_CLOAK, PAL_CLOAK)

# ==============================================================================
# 65. dragon_horn (Berrante de Batalha Dracônico)
# Berrante espiralado talhado de osso fóssil com bocais e runas de magma
# ==============================================================================
PAL_HORN = {
    '.': (0, 0, 0, 0),
    '#': (28, 20, 15, 255),    # Contorno
    'B': (240, 185, 55, 255),  # Bocal / cinta de bronze
    'b': (165, 115, 30, 255),  # Sombra de bronze
    '4': (240, 230, 205, 255), # Marfim luz
    '3': (200, 185, 155, 255), # Marfim base
    '2': (155, 135, 105, 255), # Marfim sombra
    '1': (105, 85, 65, 255),   # Marfim escuro
    'R': (255, 115, 25, 255),  # Runa mágica incandescente
    'r': (190, 45, 15, 255),   # Borda da runa
    'O': (35, 22, 18, 255),    # Interior escuro da boca do berrante
}
GRID_HORN = [
    "...###..........",
    "..#BbB#.........",
    "..#bBb#.........",
    "..#432#.........",
    "...#432#........",
    "...#4R32#.......",
    "....#4R32#......",
    "....#43r32#.....",
    ".....#43212#....",
    ".....#4R3212#...",
    ".....#432bBb2#..",
    "....#432bBBb2#..",
    "....#432bOOOb#..",
    "....#3211bOb#...",
    ".....######.....",
    "................",
]
ITEMS["dragon_horn.png"] = (GRID_HORN, PAL_HORN)

# ==============================================================================
# 66. reinforced_reins (Rédeas de Tendão Reforçadas)
# Rédeas trançadas de tendão dracônico dourado com pegador de couro e argolas
# ==============================================================================
PAL_REINS = {
    '.': (0, 0, 0, 0),
    '#': (30, 20, 12, 255),    # Contorno
    'G': (245, 195, 55, 255),  # Tendão dourado / latão luz
    'g': (185, 135, 35, 255),  # Tendão dourado meio tom
    'd': (125, 85, 25, 255),   # Tendão sombra
    'L': (165, 85, 35, 255),   # Couro empunhadura
    'l': (105, 50, 20, 255),   # Couro sombra
    'I': (180, 185, 195, 255), # Argola metálica luz
    'i': (100, 105, 115, 255), # Argola metálica sombra
}
GRID_REINS = [
    "......####......",
    ".....#LLlL#.....",
    "....#LllllL#....",
    "...#Gg#ll#gG#...",
    "..#Gg#....#gG#..",
    "..#dG#....#Gd#..",
    ".#Gg#......#gG#.",
    ".#dG#......#Gd#.",
    ".#Gg#......#gG#.",
    ".#dG#......#Gd#.",
    ".#iI#......#Ii#.",
    "#i##I#....#I##i#",
    "#iIIi#....#iIIi#",
    ".####......####.",
    "................",
    "................",
]
ITEMS["reinforced_reins.png"] = (GRID_REINS, PAL_REINS)

# ==============================================================================
# 67. tail_flame_guard (Protetor de Cauda Metálico)
# Armadura cônica articulada com frestas de grelha onde a chama queima segura
# ==============================================================================
PAL_TAIL = {
    '.': (0, 0, 0, 0),
    '#': (22, 20, 26, 255),    # Contorno metal escuro
    'M': (155, 150, 165, 255), # Aço luz
    'm': (105, 100, 115, 255), # Aço meio tom
    'd': (65, 60, 75, 255),    # Aço sombra
    'B': (235, 180, 50, 255),  # Rebites de bronze
    'F': (255, 240, 100, 255), # Chama central quente
    'f': (255, 140, 25, 255),  # Chama corpo alaranjado
    'r': (200, 45, 15, 255),   # Chama ponta avermelhada
}
GRID_TAIL = [
    "...........##...",
    "..........#fF#..",
    ".........#rfF#..",
    "........#d#f##..",
    ".......#Mm#r#...",
    "......#Mm#fF#...",
    ".....#Mm#rfF#...",
    "....#Mm#d#f##...",
    "...#BMmd#r#.....",
    "..#MMmmd#d#.....",
    ".#MMmmdd#.......",
    "#BMMmmddB#......",
    "#MMmmmddd#......",
    ".#MMmmdd#.......",
    "..######........",
    "................",
]
ITEMS["tail_flame_guard.png"] = (GRID_TAIL, PAL_TAIL)

# ==============================================================================
# 68. flight_map_case (Estojo de Cartografia de Voo)
# Tubo de couro rústico diagonal com cintas de latão e pergaminho exposto
# ==============================================================================
PAL_MAP = {
    '.': (0, 0, 0, 0),
    '#': (30, 18, 10, 255),    # Contorno
    'B': (245, 195, 55, 255),  # Metal latão
    'b': (175, 125, 30, 255),  # Latão sombra
    'L': (175, 110, 50, 255),  # Couro luz
    'l': (130, 70, 30, 255),   # Couro base
    'd': (80, 40, 15, 255),    # Couro sombra
    'P': (245, 235, 195, 255), # Pergaminho luz
    'p': (205, 185, 145, 255), # Pergaminho base
    'x': (140, 70, 40, 255),   # Traço do mapa no pergaminho
}
GRID_MAP = [
    "............###.",
    "...........#PpP#",
    "..........#PxP#.",
    ".........#bBbp#.",
    "........#BbBb#..",
    ".......#LllLd#..",
    "......#LllLd#...",
    ".....#bBbBb#....",
    "....#LllLd#.....",
    "...#LllLd#......",
    "..#bBbBb#.......",
    ".#bBbBb#........",
    "#BbBb##.........",
    "#bbd#...........",
    ".###............",
    "................",
]
ITEMS["flight_map_case.png"] = (GRID_MAP, PAL_MAP)

# ==============================================================================
# 69. dragon_beacon_fire (Fogo de Sinalização Dracônica)
# Braseiro de ferro com chama mágica e fumaça viva de sinalização magenta/laranja
# ==============================================================================
PAL_BEACON = {
    '.': (0, 0, 0, 0),
    '#': (24, 20, 26, 255),    # Contorno
    'S': (255, 90, 180, 255),  # Fumaça mágica magenta viva
    's': (180, 40, 120, 255),  # Fumaça tom sombra
    'Y': (255, 240, 110, 255), # Fogo centro amarelo
    'O': (255, 130, 30, 255),  # Fogo laranja
    'R': (210, 40, 25, 255),   # Fogo carmesim
    'M': (130, 130, 140, 255), # Ferro luz
    'm': (80, 80, 90, 255),    # Ferro base
    'd': (45, 45, 52, 255),    # Ferro sombra
}
GRID_BEACON = [
    "........#S#.....",
    ".......#SsS#....",
    "......#SsY#.....",
    "......#SYs#.....",
    ".....#sYYO#.....",
    "....#sYOYYs#....",
    "...#sOYOYOs#....",
    "...#ROYYORs#....",
    "..#RROOORR#.....",
    "..#d####d#......",
    "..#MmMMmM#......",
    "..#mmmmmd#......",
    "...#m##m#.......",
    "..#Mm##mM#......",
    "..##....##......",
    "................",
]
ITEMS["dragon_beacon_fire.png"] = (GRID_BEACON, PAL_BEACON)

# ==============================================================================
# 70. saddle_chest_upgrade (Expansão de Alforje Dracônico)
# Módulo expansível de couro com sanfona lateral, fecho de asa e ferragens
# ==============================================================================
PAL_UPGRADE = {
    '.': (0, 0, 0, 0),
    '#': (28, 16, 10, 255),    # Contorno
    'G': (255, 215, 60, 255),  # Fecho de asa em ouro
    'g': (185, 135, 30, 255),  # Sombra do ouro
    'L': (180, 115, 55, 255),  # Couro luz
    'l': (135, 75, 32, 255),   # Couro meio tom
    'd': (85, 42, 16, 255),    # Couro sombra
    'A': (215, 160, 100, 255), # Sanfona/fole luz
    'a': (145, 95, 55, 255),   # Sanfona fole sombra
}
GRID_UPGRADE = [
    "................",
    "................",
    "...##########...",
    "..#gGGGGGGGGg#..",
    ".#gGLLLLLLLLGg#.",
    ".#GLllllllllLG#.",
    ".#a#lggGGggl#A#.",
    ".#A#lGgGGgGl#a#.",
    ".#a#ldgGGgdl#A#.",
    ".#A#lddddddl#a#.",
    ".#gGddddddddGg#.",
    "..#gGGGGGGGGg#..",
    "...##########...",
    "................",
    "................",
    "................",
]
ITEMS["saddle_chest_upgrade.png"] = (GRID_UPGRADE, PAL_UPGRADE)

# ==============================================================================
# 71. fire_crystal_candy (Doce de Cristal de Fogo)
# Cristal de açúcar de fogo translúcido em espeto rústico de madeira chamuscada
# ==============================================================================
PAL_CANDY = {
    '.': (0, 0, 0, 0),
    '#': (35, 15, 18, 255),    # Contorno cristal
    'W': (255, 255, 230, 255), # Brilho especular puro
    'Y': (255, 220, 80, 255),  # Cristal amarelo quente
    'O': (255, 135, 35, 255),  # Cristal laranja
    'R': (210, 45, 30, 255),   # Cristal rubi
    'D': (120, 25, 25, 255),   # Cristal sombra profunda
    's': (140, 95, 50, 255),   # Graveto madeira luz
    't': (85, 50, 25, 255),    # Graveto madeira base
    'k': (40, 25, 15, 255),    # Graveto chamuscado sombra
}
GRID_CANDY = [
    "........####....",
    ".......#WYYO#...",
    "......#WYYOYO#..",
    ".....#WYOYYORD#.",
    ".....#YOYYORDD#.",
    "....#WOYYORDD#..",
    "....#OYYORDD#...",
    ".....#YYORD#....",
    "......#ORD#.....",
    ".....#kt##......",
    "....#kt#........",
    "...#st#.........",
    "..#st#..........",
    ".#kt#...........",
    ".##.............",
    "................",
]
ITEMS["fire_crystal_candy.png"] = (GRID_CANDY, PAL_CANDY)

# ==============================================================================
# 72. smoke_infused_broth (Caldo Defumado Revigorante)
# Tigela rústica com caldo fumegante vermelho-acastanhado e volutas de fumaça
# ==============================================================================
PAL_BROTH = {
    '.': (0, 0, 0, 0),
    '#': (30, 18, 12, 255),    # Contorno
    '~': (220, 215, 210, 210), # Fumaça vapor translúcido
    '^': (170, 160, 155, 180), # Fumaça vapor suave
    'S': (255, 135, 35, 255),  # Especiaria de brasa / pedaço
    'R': (195, 65, 30, 255),   # Caldo quente tom vivo
    'r': (140, 40, 22, 255),   # Caldo tom médio
    'd': (85, 25, 18, 255),    # Caldo tom profundo
    'W': (165, 105, 55, 255),  # Tigela de madeira luz
    'w': (115, 65, 30, 255),   # Tigela madeira base
    'k': (65, 35, 15, 255),    # Tigela madeira sombra
}
GRID_BROTH = [
    ".....~..........",
    "....~^...~......",
    ".....~..~^......",
    "....~^...~......",
    "...~^...~^......",
    "....~....~......",
    "..############..",
    ".#WwRRrSRRrrrw#.",
    "#WwRRrSRRrrrwk#.",
    "#Wwwwwwwwwwkkk#.",
    "#Wwwwwwwwwwkkk#.",
    ".#Wwwwwwwwkkk#..",
    "..#Wwwwwwkkk#...",
    "...#Wwwwwkk#....",
    "....######......",
    "................",
]
ITEMS["smoke_infused_broth.png"] = (GRID_BROTH, PAL_BROTH)

# ==============================================================================
# 73. molten_berry_tart (Torta de Bagas Vulcânicas)
# Torta crocante dourada com recheio borbulhante de bagas magmáticas vermelhas
# ==============================================================================
PAL_TART = {
    '.': (0, 0, 0, 0),
    '#': (35, 20, 10, 255),    # Contorno
    'C': (240, 185, 80, 255),  # Massa da torta luz
    'c': (195, 135, 45, 255),  # Massa tom médio
    'k': (130, 80, 25, 255),   # Massa assada sombra
    'M': (255, 220, 90, 255),  # Magma borbulhante luz
    'B': (255, 100, 40, 255),  # Baga vulcânica brilhante
    'b': (195, 30, 40, 255),   # Baga purpúrea / escarlate
    'd': (115, 15, 25, 255),   # Recheio sombra
}
GRID_TART = [
    "................",
    "................",
    "......####......",
    "....##CcCc##....",
    "...#CcBbMBbCc#..",
    "..#CcBBddBBbCc#.",
    ".#CcBBMddMBBbCc#",
    ".#c#cCbMMbCc#c#.",
    "#Cc#CcBbBbCc#Cck",
    "#cc#kCcCcCck#ckk",
    "#cc#kkkkkkkk#ckk",
    ".#cccccccccckk#.",
    "..#kcccckckkk#..",
    "...#kkkkkkkk#...",
    "....########....",
    "................",
]
ITEMS["molten_berry_tart.png"] = (GRID_TART, PAL_TART)

# ==============================================================================
# 74. bonding_honeycomb (Favo de Mel Dracônico)
# Alvéolos hexagonais de cera dourada transbordando de mel dracônico ardente
# ==============================================================================
PAL_HONEY = {
    '.': (0, 0, 0, 0),
    '#': (35, 22, 8, 255),     # Contorno
    'W': (245, 205, 85, 255),  # Cera luz
    'w': (190, 145, 45, 255),  # Cera base
    'k': (130, 90, 25, 255),   # Cera sombra
    'H': (255, 240, 120, 255), # Mel líquido brilho
    'h': (255, 185, 40, 255),  # Mel dourado vibrante
    'd': (200, 120, 20, 255),  # Mel âmbar escuro
}
GRID_HONEY = [
    "....####........",
    "...#WwwW#...##..",
    "..#Wwhhww#.#WW#.",
    ".#WwhHHhww#WhhW#",
    ".#wwhHHhww#whhW#",
    ".#kwwddkww#whhW#",
    "..#kk##kww#wddk#",
    "....#Wwhhww#kk#.",
    "...#WwhHHhww#...",
    "...#wwhHHhww#...",
    "...#kwwddkww#...",
    "....#kk##wwh#...",
    "........#Hhh#...",
    "........#Hhh#...",
    ".........#h#....",
    "................",
]
ITEMS["bonding_honeycomb.png"] = (GRID_HONEY, PAL_HONEY)

# ==============================================================================
# 75. vitality_essence (Essência de Vitalidade)
# Frasco de vidro em formato de coração/lágrima com elixir rubi cintilante
# ==============================================================================
PAL_ESSENCE = {
    '.': (0, 0, 0, 0),
    '#': (22, 16, 25, 255),    # Contorno
    'K': (175, 120, 60, 255),  # Rolha de cortiça
    'k': (115, 70, 30, 255),   # Rolha sombra
    'G': (230, 245, 255, 220), # Vidro reflexo branco
    'g': (160, 190, 215, 160), # Vidro brilho sutil
    'V': (255, 230, 180, 255), # Núcleo de vida radiante
    'R': (255, 60, 100, 255),  # Elixir rubi vivo
    'r': (190, 25, 60, 255),   # Elixir rubi médio
    'd': (110, 15, 40, 255),   # Elixir rubi sombra
}
GRID_ESSENCE = [
    "......####......",
    ".....#KKkk#.....",
    ".....#Kkkk#.....",
    "....##gggg##....",
    "...#GG####gg#...",
    "..#GG#RrrR#gg#..",
    ".#GG#RRrrRR#gg#.",
    ".#G#RRRVVRRR#g#.",
    "#G#RRRVVVVRRR#g#",
    "#G#RRRVVVRRRd#g#",
    "#G#rRRRVVRRdd#g#",
    ".#g#rrRRRddd#g#.",
    "..#g#rrRddd#g#..",
    "...#gg#ddd#gg#..",
    "....##dddd##....",
    "......####......",
]
ITEMS["vitality_essence.png"] = (GRID_ESSENCE, PAL_ESSENCE)

# ==============================================================================
# 76. flamefang_shed_tooth (Dente Descartado de Flamefang)
# Dente afiado curvo com raiz fóssil e ponta de brasa incandescente
# ==============================================================================
PAL_TOOTH = {
    '.': (0, 0, 0, 0),
    '#': (30, 20, 18, 255),    # Contorno
    'R': (90, 75, 65, 255),    # Raiz fóssil escura
    'r': (60, 50, 42, 255),    # Raiz fóssil sombra
    '4': (245, 240, 225, 255), # Esmalte dente luz
    '3': (210, 200, 180, 255), # Esmalte dente médio
    '2': (165, 150, 130, 255), # Esmalte dente sombra
    'F': (255, 200, 70, 255),  # Ponta quente brasa pura
    'f': (235, 90, 25, 255),   # Borda quente
}
GRID_TOOTH = [
    ".............##.",
    "............#F#.",
    "...........#Ff#.",
    "..........#4Ff#.",
    ".........#443f#.",
    "........#4433##.",
    ".......#44332#..",
    "......#44332#...",
    ".....#44332#....",
    "....#44332#.....",
    "...#R4332#......",
    "..#RrR32#.......",
    ".#RRrr##........",
    ".#rr##..........",
    "..##............",
    "................",
]
ITEMS["flamefang_shed_tooth.png"] = (GRID_TOOTH, PAL_TOOTH)

# ==============================================================================
# 77. refined_ember_core (Núcleo de Brasa Purificado)
# Joia octogonal de fogo puro envolta em engaste rúnico de ouro e metal escuro
# ==============================================================================
PAL_CORE = {
    '.': (0, 0, 0, 0),
    '#': (28, 18, 22, 255),    # Contorno
    'G': (255, 220, 70, 255),  # Ouro engaste luz
    'g': (190, 140, 30, 255),  # Ouro engaste base
    'W': (255, 255, 235, 255), # Núcleo branco-incandescente
    'Y': (255, 225, 60, 255),  # Núcleo amarelo solar
    'O': (255, 130, 25, 255),  # Núcleo laranja
    'R': (200, 40, 20, 255),   # Núcleo rubi
    'D': (120, 20, 20, 255),   # Núcleo sombra profunda
}
GRID_CORE = [
    "......####......",
    "....##gGGg##....",
    "...#gG####Gg#...",
    "..#gG#YYYY#Gg#..",
    ".#gG#YYYYYY#Gg#.",
    ".#G#YYOWWOYY#G#.",
    "#g#YYOWWWWOYY#g#",
    "#G#YOOWWWWOOY#G#",
    "#G#YOOWWWWOOY#G#",
    "#g#YYOWWWWOYY#g#",
    ".#G#YYORROYY#G#.",
    ".#gG#YRDRRY#Gg#.",
    "..#gG#RRRR#Gg#..",
    "...#gG####Gg#...",
    "....##gGGg##....",
    "......####......",
]
ITEMS["refined_ember_core.png"] = (GRID_CORE, PAL_CORE)

# ==============================================================================
# 78. charred_bone_needle (Agulha de Osso Carbonizado)
# Agulha esguia de osso polido com fio de tendão dourado passando pelo olho
# ==============================================================================
PAL_NEEDLE = {
    '.': (0, 0, 0, 0),
    '#': (25, 20, 22, 255),    # Contorno
    'T': (255, 215, 60, 255),  # Tendão dourado fio luz
    't': (195, 145, 30, 255),  # Tendão fio meio tom
    'B': (235, 230, 215, 255), # Osso polido marfim luz
    'b': (185, 175, 160, 255), # Osso tom médio
    'C': (95, 85, 80, 255),    # Osso carbonizado transição
    'c': (45, 40, 42, 255),    # Osso queimado ponta
}
GRID_NEEDLE = [
    "....##..........",
    "...#Tt##........",
    "..#T##Tt#.......",
    "..#t#Bb#T#......",
    "..#t#..#t#......",
    "...#t#Bb#.......",
    "....#t#Bb#......",
    ".....#t#Bb#.....",
    "......#t#Bb#....",
    ".......#t#Bb#...",
    "........#t#Cb#..",
    ".........##Cb#..",
    "..........#Cc#..",
    "...........#c#..",
    "............##..",
    "................",
]
ITEMS["charred_bone_needle.png"] = (GRID_NEEDLE, PAL_NEEDLE)

# ==============================================================================
# 79. hardened_scale_plate (Placa Prensada de Escamas)
# Placa retangular reforçada com rebites de canto e textura escamosa densa
# ==============================================================================
PAL_PLATE = {
    '.': (0, 0, 0, 0),
    '#': (22, 18, 24, 255),    # Contorno armação
    'M': (150, 145, 160, 255), # Rebite / armação metal luz
    'm': (95, 90, 105, 255),   # Armação metal base
    'R': (245, 190, 50, 255),  # Rebite bronze nos 4 cantos
    '4': (185, 65, 38, 255),   # Escama prensada luz
    '3': (140, 42, 30, 255),   # Escama prensada meio tom
    '2': (85, 28, 28, 255),    # Escama base
    '1': (45, 22, 25, 255),    # Escama sombra
}
GRID_PLATE = [
    "................",
    "..############..",
    ".#MmmMmmmmmmmM#.",
    ".#mR#443211#Rm#.",
    ".#m#44321144#m#.",
    ".#m#43211443#m#.",
    ".#m#32114432#m#.",
    ".#m#21144321#m#.",
    ".#m#11443211#m#.",
    ".#m#14432111#m#.",
    ".#m#44321143#m#.",
    ".#mR#432111#Rm#.",
    ".#MmmMmmmmmmmM#.",
    "..############..",
    "................",
    "................",
]
ITEMS["hardened_scale_plate.png"] = (GRID_PLATE, PAL_PLATE)

# ==============================================================================
# 80. ancient_dragon_relic (Relíquia Dracônica Antiga)
# Amuleto circular de ouro antigo com runas desgastadas e olho de dragão central
# ==============================================================================
PAL_RELIC = {
    '.': (0, 0, 0, 0),
    '#': (25, 18, 20, 255),    # Contorno
    'G': (245, 205, 65, 255),  # Ouro antigo luz
    'g': (185, 140, 35, 255),  # Ouro antigo base
    'd': (115, 80, 20, 255),   # Ouro antigo sombra
    'O': (35, 22, 25, 255),    # Fundo obsidiana
    'E': (255, 235, 90, 255),  # Olho do dragão pupila luz
    'e': (255, 125, 25, 255),  # Olho esclera incandescente
    'P': (15, 10, 15, 255),    # Fenda vertical da pupila
}
GRID_RELIC = [
    "......####......",
    "....##gGGg##....",
    "...#gG#dd#Gg#...",
    "..#gG#OOOO#Gg#..",
    ".#gG#OOeeOO#Gg#.",
    ".#G#OOeeeeOO#G#.",
    "#g#OOeePEeeOO#g#",
    "#G#OdeePPEedO#G#",
    "#G#OdeePPEedO#G#",
    "#g#OOeePEeeOO#g#",
    ".#G#OOeeeeOO#G#.",
    ".#gG#OOeeOO#Gg#.",
    "..#gG#OOOO#Gg#..",
    "...#gG#dd#Gg#...",
    "....##gGGg##....",
    "......####......",
]
ITEMS["ancient_dragon_relic.png"] = (GRID_RELIC, PAL_RELIC)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Gerando texturas para {len(ITEMS)} itens...")
    
    for filename, (grid, palette) in ITEMS.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        img = create_item_image(grid, palette)
        img.save(out_path, format="PNG")
        print(f"Salvo: {filename} ({img.size[0]}x{img.size[1]}) em {out_path}")
        
    print("\nTodas as 22 texturas foram geradas com sucesso!")

if __name__ == "__main__":
    main()
