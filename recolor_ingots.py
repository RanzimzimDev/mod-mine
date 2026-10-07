import os
from PIL import Image

vanilla_iron = Image.open(r"D:\Mine\iron_ingot.png").convert("RGBA")
w, h = vanilla_iron.size

# Paletas com (shadow, midtone, highlight) para cada tipo de lingote
# Tonalidades elementais:
palettes = {
    "ember_ingot": ((90, 20, 10), (220, 70, 20), (255, 180, 50)),            # Fogo/Brasa incandescente
    "terraslate_ingot": ((50, 45, 40), (120, 100, 80), (190, 170, 140)),     # Terra/Basalto/Rocha
    "abyssal_tide_ingot": ((10, 40, 80), (30, 110, 190), (100, 210, 255)),   # Agua/Abissal
    "tempest_ingot": ((50, 80, 90), (100, 180, 190), (200, 245, 250)),       # Vento/Tempestade
    "frostbite_ingot": ((60, 110, 160), (130, 200, 240), (230, 250, 255)),   # Gelo eterno
    "miasma_ingot": ((40, 15, 60), (100, 40, 140), (190, 110, 240)),         # Veneno/Miasma roxo escuro
    "fulgurite_ingot": ((100, 80, 10), (220, 190, 30), (255, 250, 120)),      # Relampago/Eletricidade amarelo choque
    "solarium_ingot": ((140, 60, 10), (255, 140, 20), (255, 240, 100)),       # Sol/Solar dourado radiante
    "void_shadow_ingot": ((15, 10, 25), (45, 35, 65), (110, 95, 145)),       # Vazio/Sombra obsidiana
    "astralite_ingot": ((30, 20, 70), (90, 70, 170), (180, 160, 255)),       # Astral/Cosmico azul-violeta
    "chronium_ingot": ((60, 50, 70), (140, 120, 160), (225, 215, 240)),      # Tempo/Crono metal platinado mistico
    "volcanic_titanium_ingot": ((40, 40, 45), (100, 95, 105), (200, 190, 210)),# Titanio Vulcanico cinza aco escuro
    "frostburn_alloy_ingot": ((30, 80, 110), (90, 180, 210), (255, 160, 100)),# Liga Gelo + Brasa (azul c/ pontas alaranjadas)
    "scalding_alloy_ingot": ((110, 30, 30), (210, 80, 40), (255, 210, 100)),  # Liga Escaldante
    "shadowflame_alloy_ingot": ((35, 15, 50), (120, 40, 90), (240, 90, 120)), # Liga Chama Sombria
    "plasma_alloy_ingot": ((120, 20, 80), (220, 60, 160), (255, 200, 250))    # Liga Plasma fucsia eletrico
}

def interpolate_color(val_norm, c_low, c_mid, c_high):
    # val_norm de 0.0 a 1.0
    if val_norm <= 0.5:
        factor = val_norm / 0.5
        r = int(c_low[0] + (c_mid[0] - c_low[0]) * factor)
        g = int(c_low[1] + (c_mid[1] - c_low[1]) * factor)
        b = int(c_low[2] + (c_mid[2] - c_low[2]) * factor)
    else:
        factor = (val_norm - 0.5) / 0.5
        r = int(c_mid[0] + (c_high[0] - c_mid[0]) * factor)
        g = int(c_mid[1] + (c_high[1] - c_mid[1]) * factor)
        b = int(c_high[2] + (c_high[2] - c_mid[2]) * factor)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

out_dir = r"D:\Mine\src\main\resources\assets\wingsofthewild\textures\item"

for name, (c_low, c_mid, c_high) in palettes.items():
    new_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            r, g, b, a = vanilla_iron.getpixel((x, y))
            if a > 0:
                # Luminancia do pixel original de ferro (de 53 a 255)
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                # normalizar lum entre 0 e 1 baseado na escala do iron ingot
                norm = max(0.0, min(1.0, (lum - 45.0) / (255.0 - 45.0)))
                # cor mapeada
                nr, ng, nb = interpolate_color(norm, c_low, c_mid, c_high)
                new_img.putpixel((x, y), (nr, ng, nb, a))
    
    target_path = os.path.join(out_dir, f"{name}.png")
    new_img.save(target_path)
    print(f"Salvo padrao vanilla para: {name}.png")
