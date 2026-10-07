"""
Gerador de Texturas de Janelas de Interface (GUIs) 256x256 para o mod Wings of the Wild
Agente 3 - Artista Pixel & Texturas 2D (Nano Banana)
"""

import os
from PIL import Image, ImageDraw

OUTPUT_DIR = "D:/Mine/src/main/resources/assets/wingsofthewild/textures/gui/container"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_base_canvas():
    """Cria o canvas 256x256 RGBA com fundo totalmente transparente."""
    return Image.new("RGBA", (256, 256), (0, 0, 0, 0))

def draw_window_frame(img, fill_color, border_light, border_dark, w=176, h=166):
    """
    Desenha o corpo principal da janela (176x166) com chanfros clássicos 3D do Minecraft.
    """
    draw = ImageDraw.Draw(img)
    # Preenchimento principal
    draw.rectangle([0, 0, w - 1, h - 1], fill=fill_color)
    
    # Borda externa superior e esquerda (luz)
    draw.line([(0, 0), (w - 1, 0)], fill=border_light, width=1)
    draw.line([(0, 0), (0, h - 1)], fill=border_light, width=1)
    draw.line([(1, 1), (w - 2, 1)], fill=border_light, width=1)
    draw.line([(1, 1), (1, h - 2)], fill=border_light, width=1)
    
    # Borda externa inferior e direita (sombra)
    draw.line([(0, h - 1), (w - 1, h - 1)], fill=border_dark, width=1)
    draw.line([(w - 1, 0), (w - 1, h - 1)], fill=border_dark, width=1)
    draw.line([(1, h - 2), (w - 2, h - 2)], fill=border_dark, width=1)
    draw.line([(w - 2, 1), (w - 2, h - 2)], fill=border_dark, width=1)

def apply_texture_noise(img, x0, y0, x1, y1, palette):
    """Aplica granulação sutil e natural de material (pedra, couro, metal)."""
    import random
    rnd = random.Random(42)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if rnd.random() < 0.28:
                c = rnd.choice(palette)
                img.putpixel((x, y), c)

def draw_slot(img, x, y, size=18, cav_color=(30, 26, 34, 255), s_dark=(20, 16, 22, 255), s_light=(85, 78, 95, 255)):
    """
    Desenha um slot de inventário 18x18 (ou custom) chanfrado com cavidade interior.
    """
    draw = ImageDraw.Draw(img)
    # Cavidade interna
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=cav_color)
    
    # Chanfro interno: topo e esquerda escuros (recesso)
    draw.line([(x, y), (x + size - 1, y)], fill=s_dark)
    draw.line([(x, y), (x, y + size - 1)], fill=s_dark)
    
    # Chanfro interno: base e direita claros (recesso de luz)
    draw.line([(x, y + size - 1), (x + size - 1, y + size - 1)], fill=s_light)
    draw.line([(x + size - 1, y), (x + size - 1, y + size - 1)], fill=s_light)

def draw_large_slot(img, x, y, size=26, cav_color=(32, 26, 36, 255), s_dark=(18, 14, 22, 255), s_light=(95, 85, 110, 255), rim_gold=None):
    """Desenha slot ampliado de resultado (26x26)."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=cav_color)
    
    draw.line([(x, y), (x + size - 1, y)], fill=s_dark, width=2)
    draw.line([(x, y), (x, y + size - 1)], fill=s_dark, width=2)
    draw.line([(x, y + size - 1), (x + size - 1, y + size - 1)], fill=s_light, width=2)
    draw.line([(x + size - 1, y), (x + size - 1, y + size - 1)], fill=s_light, width=2)
    
    if rim_gold:
        draw.rectangle([x - 1, y - 1, x + size, y + size], outline=rim_gold)

def draw_player_inventory(img, cav_color, s_dark, s_light):
    """
    Desenha os slots clássicos do inventário do jogador (9x3 em y=83)
    e da hotbar (9x1 em y=141).
    """
    # 9x3 Principal
    for row in range(3):
        for col in range(9):
            x = 7 + col * 18
            y = 83 + row * 18
            draw_slot(img, x, y, 18, cav_color, s_dark, s_light)
            
    # 9x1 Hotbar
    for col in range(9):
        x = 7 + col * 18
        y = 141
        draw_slot(img, x, y, 18, cav_color, s_dark, s_light)

def draw_progress_arrow(img, x, y, filled=False, theme="magma"):
    """
    Desenha a seta/indicador de progresso (24x17 pixels).
    """
    # Matriz 24x17
    # '.' = transparente, '#' = borda, 'F' = preenchimento
    GRID = [
        "........................",
        "#################.......",
        "#FFFFFFFFFFFFFFFF#......",
        "#FFFFFFFFFFFFFFFFF#.....",
        "#FFFFFFFFFFFFFFFFFF#....",
        "#FFFFFFFFFFFFFFFFFFF#...",
        "#FFFFFFFFFFFFFFFFFFFF#..",
        "#FFFFFFFFFFFFFFFFFFFFF#.",
        "#FFFFFFFFFFFFFFFFFFFFFF#",
        "#FFFFFFFFFFFFFFFFFFFFF#.",
        "#FFFFFFFFFFFFFFFFFFFF#..",
        "#FFFFFFFFFFFFFFFFFFF#...",
        "#FFFFFFFFFFFFFFFFFF#....",
        "#FFFFFFFFFFFFFFFFF#.....",
        "#FFFFFFFFFFFFFFFF#......",
        "#################.......",
        "........................",
    ]
    if not filled:
        # Silhueta vazia / recesso de pedra
        pal = {
            '#': (22, 18, 26, 255),
            'F': (36, 32, 42, 255),
        }
    else:
        if theme == "magma":
            # Magma incandescente
            pal = {
                '#': (45, 15, 10, 255),
                'F': (255, 140, 25, 255),
            }
        elif theme == "cooking":
            pal = {
                '#': (45, 25, 10, 255),
                'F': (255, 190, 50, 255),
            }
        else:
            pal = {
                '#': (35, 20, 10, 255),
                'F': (245, 205, 70, 255),
            }
    for ry, row in enumerate(GRID):
        for rx, ch in enumerate(row):
            if ch in pal:
                img.putpixel((x + rx, y + ry), pal[ch])

def draw_flame_icon(img, x, y, filled=False, theme="fire"):
    """
    Desenha o ícone clássico de chama de combustível (14x14).
    """
    GRID = [
        "......##......",
        ".....#FF#.....",
        "....#FFFF#....",
        "...#FFFFFF#...",
        "...#FFFFFF#...",
        "..#FFFFFFFF#..",
        "..#FFFFFFFF#..",
        ".#FFFFFFFFFF#.",
        ".#FFFFFFFFFF#.",
        "#FFFFFFFFFFFF#",
        "#FFFFFFFFFFFF#",
        "#FFFFFFFFFFFF#",
        ".#FFFFFFFFFF#.",
        "..##########..",
    ]
    if not filled:
        pal = {
            '#': (24, 18, 22, 255),
            'F': (38, 30, 36, 255),
        }
    else:
        pal = {
            '#': (60, 15, 10, 255),
            'F': (255, 130, 20, 255),
        }
    for ry, row in enumerate(GRID):
        for rx, ch in enumerate(row):
            if ch in pal:
                img.putpixel((x + rx, y + ry), pal[ch])


# ==============================================================================
# 1. DRACONIC FOUNDRY (draconic_foundry.png)
# ==============================================================================
def generate_draconic_foundry():
    img = create_base_canvas()
    
    # Fundo de basalto/pedra vulcânica refratária
    bg_color = (45, 40, 52, 255)
    b_light = (88, 80, 98, 255)
    b_dark = (22, 18, 26, 255)
    draw_window_frame(img, bg_color, b_light, b_dark)
    
    # Granulação de pedra de forja
    stone_palette = [
        (40, 35, 46, 255),
        (48, 43, 56, 255),
        (52, 46, 60, 255),
        (36, 32, 42, 255)
    ]
    apply_texture_noise(img, 2, 2, 174, 164, stone_palette)
    
    # Faixa superior de metal com rebites
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 5, 169, 13], fill=(32, 28, 38, 255))
    draw.line([(6, 13), (169, 13)], fill=b_light)
    # Rebites de bronze nos cantos da forja
    for rx, ry in [(9, 8), (28, 8), (147, 8), (166, 8)]:
        draw.ellipse([rx - 2, ry - 2, rx + 1, ry + 1], fill=(225, 165, 45, 255), outline=(140, 95, 25, 255))
        
    # Moldura decorativa em arco para a área de fundição
    draw.rectangle([34, 14, 150, 75], fill=(35, 30, 42, 255), outline=(65, 58, 75, 255))
    
    # Slots de Entrada de Minérios (2 slots superiores convergentes)
    s_dark = (18, 14, 22, 255)
    s_light = (78, 70, 88, 255)
    cav_color = (24, 20, 28, 255)
    
    draw_slot(img, 42, 19, 18, cav_color, s_dark, s_light)
    draw_slot(img, 64, 19, 18, cav_color, s_dark, s_light)
    
    # Slot de Combustível (inferior)
    draw_slot(img, 53, 53, 18, cav_color, s_dark, s_light)
    
    # Chama de combustível no centro
    draw_flame_icon(img, 55, 38, filled=False)
    
    # Seta de progresso de fusão de magma (vazia na janela principal)
    draw_progress_arrow(img, 86, 35, filled=False)
    
    # Slot de Saída Ampliado para Lingote / Liga (26x26)
    draw_large_slot(img, 116, 31, 26, (20, 16, 24, 255), s_dark, (110, 95, 125, 255), rim_gold=(235, 130, 30, 255))
    
    # Slots do Inventário do Jogador e Hotbar
    draw_player_inventory(img, cav_color, s_dark, s_light)
    
    # --- ÁREA DE SPRITES ATIVOS (x >= 176) ---
    # Chama acesa animada em (176, 0)
    draw_flame_icon(img, 176, 0, filled=True, theme="fire")
    # Seta de progresso de magma acesa em (176, 14)
    draw_progress_arrow(img, 176, 14, filled=True, theme="magma")
    
    return img


# ==============================================================================
# 2. DRACONIC HEARTH (draconic_hearth.png)
# ==============================================================================
def generate_draconic_hearth():
    img = create_base_canvas()
    
    # Fundo rústico de pedra e tijolos de cinzas
    bg_color = (58, 52, 48, 255)
    b_light = (108, 98, 90, 255)
    b_dark = (28, 24, 22, 255)
    draw_window_frame(img, bg_color, b_light, b_dark)
    
    # Granulação de pedra e tijolo culinário
    hearth_palette = [
        (52, 46, 42, 255),
        (64, 58, 52, 255),
        (68, 60, 55, 255),
        (46, 40, 36, 255)
    ]
    apply_texture_noise(img, 2, 2, 174, 164, hearth_palette)
    
    # Faixa superior com arcos de fornalha
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 5, 169, 13], fill=(42, 36, 32, 255))
    draw.line([(6, 13), (169, 13)], fill=b_light)
    
    # Área central de cocção
    draw.rectangle([24, 14, 154, 75], fill=(45, 38, 35, 255), outline=(78, 68, 62, 255))
    
    s_dark = (22, 18, 16, 255)
    s_light = (95, 84, 78, 255)
    cav_color = (28, 22, 20, 255)
    
    # 3 Slots de Cozimento (carne, vegetal, cinzas)
    draw_slot(img, 30, 19, 18, cav_color, s_dark, s_light)
    draw_slot(img, 48, 19, 18, cav_color, s_dark, s_light)
    draw_slot(img, 66, 19, 18, cav_color, s_dark, s_light)
    
    # Slot de Combustível / Brasa
    draw_slot(img, 48, 53, 18, cav_color, s_dark, s_light)
    
    # Chama de calor ativa / vazia
    draw_flame_icon(img, 50, 38, filled=False)
    
    # Seta de progresso culinária
    draw_progress_arrow(img, 88, 35, filled=False)
    
    # Slot de Saída Ampliado para Ensopado / Prato Dracônico
    draw_large_slot(img, 120, 31, 26, cav_color, s_dark, s_light, rim_gold=(245, 175, 45, 255))
    
    # Slots do Jogador e Hotbar
    draw_player_inventory(img, cav_color, s_dark, s_light)
    
    # --- ÁREA DE SPRITES ATIVOS (x >= 176) ---
    draw_flame_icon(img, 176, 0, filled=True, theme="fire")
    draw_progress_arrow(img, 176, 14, filled=True, theme="cooking")
    
    return img


# ==============================================================================
# 3. TACK WORKBENCH (tack_workbench.png)
# ==============================================================================
def generate_tack_workbench():
    img = create_base_canvas()
    
    # Fundo em couro conhaque nobre curtido
    bg_color = (150, 92, 45, 255)
    b_light = (195, 130, 75, 255)
    b_dark = (85, 45, 20, 255)
    draw_window_frame(img, bg_color, b_light, b_dark)
    
    # Granulação de textura de couro
    leather_palette = [
        (140, 85, 40, 255),
        (160, 100, 50, 255),
        (165, 105, 55, 255),
        (135, 80, 36, 255)
    ]
    apply_texture_noise(img, 2, 2, 174, 164, leather_palette)
    
    draw = ImageDraw.Draw(img)
    # Pesponto artesanal duplo ao redor da borda (costura)
    stitch_dark = (75, 40, 18, 255)
    stitch_light = (235, 195, 120, 255)
    for x in range(6, 170, 3):
        draw.point((x, 5), fill=stitch_light)
        draw.point((x, 160), fill=stitch_dark)
    for y in range(6, 160, 3):
        draw.point((5, y), fill=stitch_light)
        draw.point((170, y), fill=stitch_dark)
        
    # Cantoneiras de latão batido nos 4 cantos
    for cx, cy in [(3, 3), (167, 3), (3, 157), (167, 157)]:
        draw.rectangle([cx, cy, cx + 5, cy + 5], fill=(225, 175, 50, 255), outline=(150, 105, 25, 255))
        
    # Área central de costura e alfaiataria dracônica
    draw.rectangle([22, 15, 154, 75], fill=(125, 72, 32, 255), outline=(85, 45, 18, 255))
    
    s_dark = (55, 28, 12, 255)
    s_light = (185, 120, 65, 255)
    cav_color = (95, 50, 22, 255)
    
    # 4 Slots de Confecção de Selas & Arreios:
    # Slot 1: Base de Couro/Sela
    draw_slot(img, 32, 25, 18, cav_color, s_dark, s_light)
    # Slot 2: Placas de Escamas / Blindagem
    draw_slot(img, 54, 25, 18, cav_color, s_dark, s_light)
    # Slot 3: Tendões / Linha de costura
    draw_slot(img, 76, 25, 18, cav_color, s_dark, s_light)
    # Slot 4: Alforje / Fivela de Expansão (inferior)
    draw_slot(img, 54, 47, 18, cav_color, s_dark, s_light)
    
    # Seta de confecção artesanal
    draw_progress_arrow(img, 98, 35, filled=False)
    
    # Slot de Saída Ampliado para Sela / Equipamento Costurado
    draw_large_slot(img, 126, 31, 26, (75, 38, 16, 255), s_dark, s_light, rim_gold=(255, 215, 60, 255))
    
    # Slots do Jogador e Hotbar com tons quentes de couro
    draw_player_inventory(img, cav_color, s_dark, s_light)
    
    # --- ÁREA DE SPRITES ATIVOS (x >= 176) ---
    draw_progress_arrow(img, 176, 0, filled=True, theme="tack")
    
    return img


# ==============================================================================
# 4. DRAGON INVENTORY (dragon_inventory.png)
# ==============================================================================
def generate_dragon_inventory():
    img = create_base_canvas()
    
    # Fundo dracônico escuro com placas de armadura e couro
    bg_color = (48, 42, 52, 255)
    b_light = (95, 85, 105, 255)
    b_dark = (22, 18, 26, 255)
    draw_window_frame(img, bg_color, b_light, b_dark)
    
    # Granulação
    dragon_palette = [
        (42, 36, 46, 255),
        (52, 46, 58, 255),
        (58, 50, 64, 255),
        (36, 30, 40, 255)
    ]
    apply_texture_noise(img, 2, 2, 174, 164, dragon_palette)
    
    s_dark = (18, 14, 22, 255)
    s_light = (82, 74, 92, 255)
    cav_color = (26, 22, 30, 255)
    
    # 3 Slots Especiais de Equipamento do Dragão no lado esquerdo (x=8)
    # Slot 1: Sela (y=18)
    draw_slot(img, 8, 18, 18, cav_color, s_dark, s_light)
    # Silhueta sutil de sela no fundo do slot
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 24, 21, 28], fill=(55, 45, 65, 255))
    draw.point((16, 23), fill=(75, 60, 90, 255))
    
    # Slot 2: Armadura Barda de Escamas (y=36)
    draw_slot(img, 8, 36, 18, cav_color, s_dark, s_light)
    # Silhueta sutil de peitoral
    draw.rectangle([12, 42, 21, 46], fill=(55, 45, 65, 255))
    draw.point((16, 41), fill=(75, 60, 90, 255))
    
    # Slot 3: Cabresto / Berrante / Protetor (y=54)
    draw_slot(img, 8, 54, 18, cav_color, s_dark, s_light)
    # Silhueta de berrante/rédeas
    draw.arc([12, 58, 21, 66], 0, 180, fill=(75, 60, 90, 255))
    
    # Viewport Central para Renderização 3D do Dragão
    # Caixa rebaixada de pedra de obsidiana (x=29 a 76, y=17 a 72)
    draw.rectangle([29, 17, 76, 72], fill=(18, 15, 22, 255), outline=(65, 55, 75, 255))
    # Efeito sutil de pedestal de brasa sob o dragão
    draw.ellipse([34, 60, 71, 70], fill=(30, 20, 28, 255), outline=(50, 30, 40, 255))
    
    # Grade de Alforje do Dragão no lado direito (5 colunas x 3 linhas = 15 slots)
    # Alinhada de x=80 a 169, y=18 a 71
    for row in range(3):
        for col in range(5):
            x = 80 + col * 18
            y = 18 + row * 18
            draw_slot(img, x, y, 18, cav_color, s_dark, s_light)
            
    # Slots do Jogador e Hotbar
    draw_player_inventory(img, cav_color, s_dark, s_light)
    
    return img


def main():
    print("Gerando texturas de Janelas de Interface (GUIs 256x256)...")
    
    foundry = generate_draconic_foundry()
    foundry_path = os.path.join(OUTPUT_DIR, "draconic_foundry.png")
    foundry.save(foundry_path, format="PNG")
    print(f"[1/4] Salvo: draconic_foundry.png ({foundry.size}) em {foundry_path}")
    
    hearth = generate_draconic_hearth()
    hearth_path = os.path.join(OUTPUT_DIR, "draconic_hearth.png")
    hearth.save(hearth_path, format="PNG")
    print(f"[2/4] Salvo: draconic_hearth.png ({hearth.size}) em {hearth_path}")
    
    workbench = generate_tack_workbench()
    workbench_path = os.path.join(OUTPUT_DIR, "tack_workbench.png")
    workbench.save(workbench_path, format="PNG")
    print(f"[3/4] Salvo: tack_workbench.png ({workbench.size}) em {workbench_path}")
    
    dragon_inv = generate_dragon_inventory()
    dragon_inv_path = os.path.join(OUTPUT_DIR, "dragon_inventory.png")
    dragon_inv.save(dragon_inv_path, format="PNG")
    print(f"[4/4] Salvo: dragon_inventory.png ({dragon_inv.size}) em {dragon_inv_path}")
    
    print("\nTodas as 4 GUIs 256x256 foram geradas com sucesso absoluto!")

if __name__ == "__main__":
    main()
