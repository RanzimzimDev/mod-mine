package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.item.DragonHandlerGlovesItem;
import com.wingsofthewild.item.DragonHornItem;
import com.wingsofthewild.item.DragonPouchItem;
import com.wingsofthewild.item.DragonologistTomeItem;
import com.wingsofthewild.item.EmberSwordItem;
import com.wingsofthewild.item.FlightMapCaseItem;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.equipment.ArmorType;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(WingsOfTheWild.MODID);

    // Item 09: Fragmento de Brasa Bruta
    public static final DeferredItem<Item> RAW_EMBER = ITEMS.registerSimpleItem("raw_ember");

    // Item 10: Lingote de Brasa
    public static final DeferredItem<Item> EMBER_INGOT = ITEMS.registerSimpleItem("ember_ingot");

    // Item 11: Escama de Flamefang (Material chave para selaria e armaduras)
    public static final DeferredItem<Item> FLAMEFANG_SCALE = ITEMS.registerSimpleItem("flamefang_scale");

    // Item 19: Ovo de Flamefang (Intacto)
    public static final DeferredItem<Item> FLAMEFANG_EGG = ITEMS.registerSimpleItem("flamefang_egg",
            properties -> properties.stacksTo(16));

    // Item 26: Bagas Magmáticas Picantes (Comida de filhote)
    public static final DeferredItem<Item> SPICY_MAGMA_BERRIES = ITEMS.registerSimpleItem("spicy_magma_berries",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(2)
                    .saturationModifier(0.3F)
                    .alwaysEdible()
                    .build()));

    // Item 27: Bife Carbonizado em Brasas (Carne selada com cinzas)
    public static final DeferredItem<Item> CHARRED_MEAT = ITEMS.registerSimpleItem("charred_meat",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(6)
                    .saturationModifier(0.8F)
                    .build()));

    // Item 28: Ensopado Nutritivo de Cinzas (Refeição que reduz o tempo de crescimento)
    public static final DeferredItem<Item> ASH_STEW = ITEMS.registerSimpleItem("ash_stew",
            properties -> properties
                    .stacksTo(1)
                    .usingConvertsTo(Items.BOWL)
                    .food(new FoodProperties.Builder()
                            .nutrition(8)
                            .saturationModifier(0.8F)
                            .alwaysEdible()
                            .build()));

    // Item 29: Petisco Dracônico Crocante (Biscoito crocante que aumenta o afeto)
    public static final DeferredItem<Item> DRACONIC_TREAT = ITEMS.registerSimpleItem("draconic_treat",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(3)
                    .saturationModifier(0.4F)
                    .alwaysEdible()
                    .build()));

    // Item 44: Espada de Brasas (Incendeia alvos atingidos)
    public static final DeferredItem<Item> EMBER_SWORD = ITEMS.registerItem("ember_sword",
            EmberSwordItem::new,
            properties -> properties.sword(ModToolMaterials.EMBER, 3.0F, -2.4F));

    // Item 45: Picareta de Brasas (Quebra rochas em alta velocidade)
    public static final DeferredItem<Item> EMBER_PICKAXE = ITEMS.registerSimpleItem("ember_pickaxe",
            properties -> properties.pickaxe(ModToolMaterials.EMBER, 1.0F, -2.8F));

    // Item 15: Couro Dracônico Bruto (Pele grossa de répteis ancestrais)
    public static final DeferredItem<Item> RAW_DRACONIC_HIDE = ITEMS.registerSimpleItem("raw_draconic_hide");

    // Item 16: Couro Dracônico Curtido (Couro tratado, base para selas)
    public static final DeferredItem<Item> TANNED_DRACONIC_LEATHER = ITEMS.registerSimpleItem("tanned_draconic_leather");

    // Item 22: Escova Dracônica (Ferramenta para escovar o dragão e recolher escamas)
    public static final DeferredItem<Item> DRAGON_BRUSH = ITEMS.registerSimpleItem("dragon_brush",
            properties -> properties.durability(64));

    // Item 23: Flauta Dracônica de Osso (Instrumento de comando: Seguir, Ficar, Proteger)
    public static final DeferredItem<Item> DRAGON_FLUTE = ITEMS.registerSimpleItem("dragon_flute",
            properties -> properties.stacksTo(1));

    // Item 36: Sela Dracônica Rústica (Sela básica para montaria no dragão adulto)
    public static final DeferredItem<Item> BASIC_DRAGON_SADDLE = ITEMS.registerSimpleItem("basic_dragon_saddle",
            properties -> properties.stacksTo(1));

    // Item 37: Sela Reforçada de Brasas (Sela avançada com estribos de lingote de brasa)
    public static final DeferredItem<Item> REINFORCED_FLAME_SADDLE = ITEMS.registerSimpleItem("reinforced_flame_saddle",
            properties -> properties.stacksTo(1));

    // Item 40: Armadura de Escamas de Flamefang (Proteção barda para o corpo e asas do dragão)
    public static final DeferredItem<Item> FLAMEFANG_SCALE_ARMOR = ITEMS.registerSimpleItem("flamefang_scale_armor",
            properties -> properties.stacksTo(1));

    // Item 12: Cinzas Vulcânicas (Poeira mineral coletada em ninhos; tempero dracônico)
    public static final DeferredItem<Item> VOLCANIC_ASH = ITEMS.registerSimpleItem("volcanic_ash");

    // Item 13: Cristal de Enxofre (Mineral picante usado em receitas culinárias)
    public static final DeferredItem<Item> SULFUR_CRYSTAL = ITEMS.registerSimpleItem("sulfur_crystal");

    // Item 14: Tendão Dracônico (Corda fibrosa ultra-resistente para arreios e selaria)
    public static final DeferredItem<Item> DRACONIC_SINEW = ITEMS.registerSimpleItem("draconic_sinew");

    // Item 17: Núcleo de Chamas (Joia incandescente rara encontrada em ninhos selvagens)
    public static final DeferredItem<Item> FLAME_CORE = ITEMS.registerSimpleItem("flame_core");

    // Item 18: Osso Dracônico (Osso rígido e leve para cabos e armações)
    public static final DeferredItem<Item> DRAGON_BONE = ITEMS.registerSimpleItem("dragon_bone");

    // Item 38: Alforje Dracônico Pequeno (Bolsa portátil com 9 slots de inventário)
    public static final DeferredItem<DragonPouchItem> SMALL_DRAGON_POUCH = ITEMS.registerItem("small_dragon_pouch",
            props -> new DragonPouchItem(props, 1),
            properties -> properties.stacksTo(1));

    // Item 20: Ovo de Flamefang (Fissurado - Estágio 2 de incubação)
    public static final DeferredItem<Item> CRACKED_FLAMEFANG_EGG_1 = ITEMS.registerSimpleItem("cracked_flamefang_egg_1",
            properties -> properties.stacksTo(16));

    // Item 21: Ovo de Flamefang (Prestes a Eclodir - Estágio 3 de incubação)
    public static final DeferredItem<Item> CRACKED_FLAMEFANG_EGG_2 = ITEMS.registerSimpleItem("cracked_flamefang_egg_2",
            properties -> properties.stacksTo(16));

    // Item 24: Bastão de Comando Dracônico (Aponta alvos e pousos)
    public static final DeferredItem<Item> DRAGON_STAFF = ITEMS.registerSimpleItem("dragon_staff",
            properties -> properties.stacksTo(1));

    // Item 25: Coleira de Vínculo (Identificador e afeto do dragão)
    public static final DeferredItem<Item> BONDING_COLLAR = ITEMS.registerSimpleItem("bonding_collar",
            properties -> properties.stacksTo(1));

    // Item 30: Biscoito de Enxofre (Fortalece a defesa e regenera o dragão)
    public static final DeferredItem<Item> SULFUR_BISCUIT = ITEMS.registerSimpleItem("sulfur_biscuit",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(4)
                    .saturationModifier(0.5F)
                    .alwaysEdible()
                    .build()));

    // Item 31: Pimenta Vulcânica (Vegetal aromático picante para receitas)
    public static final DeferredItem<Item> FIRE_PEPPER = ITEMS.registerSimpleItem("fire_pepper",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(2)
                    .saturationModifier(0.4F)
                    .alwaysEdible()
                    .build()));

    // Item 32: Carne Seca Flamejante (Provisão portátil de longa duração)
    public static final DeferredItem<Item> BLAZING_JERKY = ITEMS.registerSimpleItem("blazing_jerky",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(7)
                    .saturationModifier(0.9F)
                    .build()));

    // Item 33: Papa Encorpada de Filhote (Alimento leve para as primeiras horas)
    public static final DeferredItem<Item> HEARTY_DRAGON_MASH = ITEMS.registerSimpleItem("hearty_dragon_mash",
            properties -> properties
                    .stacksTo(1)
                    .usingConvertsTo(Items.BOWL)
                    .food(new FoodProperties.Builder()
                            .nutrition(6)
                            .saturationModifier(0.7F)
                            .alwaysEdible()
                            .build()));

    // Item 34: Rolo de Algas Incandescentes (Melhora respiração e fôlego subaquático)
    public static final DeferredItem<Item> GLOW_KELP_ROLL = ITEMS.registerSimpleItem("glow_kelp_roll",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(5)
                    .saturationModifier(0.6F)
                    .build()));

    // Item 35: Elixir de Brasas (Recarrega instantaneamente o fôlego de fogo)
    public static final DeferredItem<Item> FLAME_DRAUGHT = ITEMS.registerSimpleItem("flame_draught",
            properties -> properties
                    .stacksTo(16)
                    .usingConvertsTo(Items.GLASS_BOTTLE)
                    .food(new FoodProperties.Builder()
                            .nutrition(1)
                            .saturationModifier(0.2F)
                            .alwaysEdible()
                            .build()));

    // Item 39: Alforje Dracônico Grande (Bolsa portátil com 27 slots de inventário móvel)
    public static final DeferredItem<DragonPouchItem> LARGE_DRAGON_SADDLEBAGS = ITEMS.registerItem("large_dragon_saddlebags",
            props -> new DragonPouchItem(props, 3),
            properties -> properties.stacksTo(1));

    // Item 41: Armadura Revestida de Brasa (Máxima proteção contra projéteis e impacto)
    public static final DeferredItem<Item> EMBER_PLATED_ARMOR = ITEMS.registerSimpleItem("ember_plated_armor",
            properties -> properties.stacksTo(1));

    // Item 42: Cabresto Dracônico com Rédeas (Melhora a precisão de curva no ar)
    public static final DeferredItem<Item> DRAGON_HEADSTALL = ITEMS.registerSimpleItem("dragon_headstall",
            properties -> properties.stacksTo(1));

    // Item 43: Óculos de Voo do Cavaleiro (Elimina embaçamento em alta velocidade)
    public static final DeferredItem<Item> FLIGHT_GOGGLES = ITEMS.registerSimpleItem("flight_goggles",
            properties -> properties.stacksTo(1));

    // Item 46: Machado de Brasas (Corta madeiras e causa dano flamejante)
    public static final DeferredItem<Item> EMBER_AXE = ITEMS.registerSimpleItem("ember_axe",
            properties -> properties.axe(ModToolMaterials.EMBER, 5.0F, -3.0F));

    // Item 47: Pá de Brasas (Derrete neve e cava solos endurecidos rapidamente)
    public static final DeferredItem<Item> EMBER_SHOVEL = ITEMS.registerSimpleItem("ember_shovel",
            properties -> properties.shovel(ModToolMaterials.EMBER, 1.5F, -3.0F));

    // Item 48: Adaga de Dente de Flamefang (Lâmina curta e ágil forjada com dentes descartados)
    public static final DeferredItem<Item> FLAMEFANG_DAGGER = ITEMS.registerSimpleItem("flamefang_dagger",
            properties -> properties.sword(ModToolMaterials.EMBER, 2.0F, -1.8F));

    // Item 49: Apito de Resgate Dracônico (Chama seu dragão para resgate no ar)
    public static final DeferredItem<Item> DRAGON_WHISTLE = ITEMS.registerSimpleItem("dragon_whistle",
            properties -> properties.stacksTo(1));

    // Item 50: Tomo do Dragonologista (Livro guia com ilustrações das espécies e receitas)
    public static final DeferredItem<Item> DRAGONOLOGIST_TOME = ITEMS.registerItem("dragonologist_tome",
            DragonologistTomeItem::new,
            properties -> properties.stacksTo(1));

    // --- Categoria 8: Armadura de Escamas do Jogador & Vestimentas (59 a 64) ---
    // Item 59: Elmo de Escamas de Flamefang (Concede visão sob a lava e proteção dracônica)
    public static final DeferredItem<Item> FLAMEFANG_HELMET = ITEMS.registerSimpleItem("flamefang_helmet",
            properties -> properties.humanoidArmor(ModArmorMaterials.FLAMEFANG, ArmorType.HELMET).fireResistant());

    // Item 60: Peitoral de Escamas de Flamefang (Armadura torácica com imunidade a queimaduras)
    public static final DeferredItem<Item> FLAMEFANG_CHESTPLATE = ITEMS.registerSimpleItem("flamefang_chestplate",
            properties -> properties.humanoidArmor(ModArmorMaterials.FLAMEFANG, ArmorType.CHESTPLATE).fireResistant());

    // Item 61: Calças de Escamas de Flamefang (Calças reforçadas com placas articulares)
    public static final DeferredItem<Item> FLAMEFANG_LEGGINGS = ITEMS.registerSimpleItem("flamefang_leggings",
            properties -> properties.humanoidArmor(ModArmorMaterials.FLAMEFANG, ArmorType.LEGGINGS).fireResistant());

    // Item 62: Botas de Escamas de Flamefang (Botas imunes ao dano de magma/fogo)
    public static final DeferredItem<Item> FLAMEFANG_BOOTS = ITEMS.registerSimpleItem("flamefang_boots",
            properties -> properties.humanoidArmor(ModArmorMaterials.FLAMEFANG, ArmorType.BOOTS).fireResistant());

    // Item 63: Luvas de Domador Reforçadas (Luvas isolantes para manusear ovos quentes)
    public static final DeferredItem<Item> DRAGON_HANDLER_GLOVES = ITEMS.registerItem("dragon_handler_gloves",
            DragonHandlerGlovesItem::new,
            properties -> properties.stacksTo(1).fireResistant());

    // Item 64: Capa do Cavaleiro de Dragão (Capa dorsal de viagem para voo)
    public static final DeferredItem<Item> DRAGON_RIDERS_CLOAK = ITEMS.registerSimpleItem("dragon_riders_cloak",
            properties -> properties.stacksTo(1).fireResistant());

    // --- Categoria 9: Equipamentos Táticos & Voo Avançado (65 a 70) ---
    // Item 65: Berrante de Batalha Dracônico (Afugenta monstros e convoca o dragão)
    public static final DeferredItem<Item> DRAGON_HORN = ITEMS.registerItem("dragon_horn",
            DragonHornItem::new,
            properties -> properties.stacksTo(1));

    // Item 66: Rédeas de Tendão Reforçadas (Componente de alta resistência para selaria)
    public static final DeferredItem<Item> REINFORCED_REINS = ITEMS.registerSimpleItem("reinforced_reins",
            properties -> properties.stacksTo(16));

    // Item 67: Protetor de Cauda Metálico (Armadura de cauda que protege a chama da chuva)
    public static final DeferredItem<Item> TAIL_FLAME_GUARD = ITEMS.registerSimpleItem("tail_flame_guard",
            properties -> properties.stacksTo(1).fireResistant());

    // Item 68: Estojo de Cartografia de Voo (Permite consultar mapas sem largar as rédeas)
    public static final DeferredItem<Item> FLIGHT_MAP_CASE = ITEMS.registerItem("flight_map_case",
            FlightMapCaseItem::new,
            properties -> properties.stacksTo(1));

    // Item 69: Fogo de Sinalização Dracônica (Coluna de fumaça colorida visível a longa distância)
    public static final DeferredItem<Item> DRAGON_BEACON_FIRE = ITEMS.registerSimpleItem("dragon_beacon_fire",
            properties -> properties.stacksTo(16));

    // Item 70: Expansão de Alforje Dracônico (Módulo de melhoria de inventário da sela)
    public static final DeferredItem<Item> SADDLE_CHEST_UPGRADE = ITEMS.registerSimpleItem("saddle_chest_upgrade",
            properties -> properties.stacksTo(16));

    // --- Categoria 10: Culinária Especializada & Poções Dracônicas (71 a 75) ---
    // Item 71: Doce de Cristal de Fogo (Açúcar cristalizado que deixa o filhote alegre)
    public static final DeferredItem<Item> FIRE_CRYSTAL_CANDY = ITEMS.registerSimpleItem("fire_crystal_candy",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(3)
                    .saturationModifier(0.4F)
                    .alwaysEdible()
                    .build()));

    // Item 72: Caldo Defumado Revigorante (Sopa espessa que recupera a estamina após voo longo)
    public static final DeferredItem<Item> SMOKE_INFUSED_BROTH = ITEMS.registerSimpleItem("smoke_infused_broth",
            properties -> properties
                    .stacksTo(1)
                    .usingConvertsTo(Items.BOWL)
                    .food(new FoodProperties.Builder()
                            .nutrition(7)
                            .saturationModifier(0.8F)
                            .alwaysEdible()
                            .build()));

    // Item 73: Torta de Bagas Vulcânicas (Refeição dracônica balanceada consumível)
    public static final DeferredItem<Item> MOLTEN_BERRY_TART = ITEMS.registerSimpleItem("molten_berry_tart",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(6)
                    .saturationModifier(0.7F)
                    .alwaysEdible()
                    .build()));

    // Item 74: Favo de Mel Dracônico (Mel silvestre que acalma dragões territoriais)
    public static final DeferredItem<Item> BONDING_HONEYCOMB = ITEMS.registerSimpleItem("bonding_honeycomb",
            properties -> properties.food(new FoodProperties.Builder()
                    .nutrition(4)
                    .saturationModifier(0.5F)
                    .alwaysEdible()
                    .build()));

    // Item 75: Essência de Vitalidade (Tônico medicinal de emergência para recuperação dracônica)
    public static final DeferredItem<Item> VITALITY_ESSENCE = ITEMS.registerSimpleItem("vitality_essence",
            properties -> properties
                    .stacksTo(16)
                    .usingConvertsTo(Items.GLASS_BOTTLE)
                    .food(new FoodProperties.Builder()
                            .nutrition(4)
                            .saturationModifier(0.6F)
                            .alwaysEdible()
                            .build()));

    // --- Categoria 11: Materiais Intermediários & Relíquias (76 a 80) ---
    // Item 76: Dente Descartado de Flamefang (Dente pontiagudo usado para lâminas)
    public static final DeferredItem<Item> FLAMEFANG_SHED_TOOTH = ITEMS.registerSimpleItem("flamefang_shed_tooth");

    // Item 77: Núcleo de Brasa Purificado (Matéria-prima alquímica forjada para itens arcanos)
    public static final DeferredItem<Item> REFINED_EMBER_CORE = ITEMS.registerSimpleItem("refined_ember_core",
            properties -> properties.fireResistant());

    // Item 78: Agulha de Osso Carbonizado (Ferramenta fina para receitas avançadas de selaria)
    public static final DeferredItem<Item> CHARRED_BONE_NEEDLE = ITEMS.registerSimpleItem("charred_bone_needle");

    // Item 79: Placa Prensada de Escamas (Blindagem intermediária para forja pesada)
    public static final DeferredItem<Item> HARDENED_SCALE_PLATE = ITEMS.registerSimpleItem("hardened_scale_plate");

    // Item 80: Relíquia Dracônica Antiga (Artefato lendário raro encontrado em ninhos remotos)
    public static final DeferredItem<Item> ANCIENT_DRAGON_RELIC = ITEMS.registerSimpleItem("ancient_dragon_relic",
            properties -> properties.stacksTo(1).rarity(Rarity.RARE).fireResistant());

    // --- Categoria 12: Sistema de Metalurgia & Ligas Elementais (Tinkers' Style - Itens 81 a 116) ---

    // 10 Minérios Brutos Elementais
    // Item 92: Terralita Bruta (Tier 1 Terra)
    public static final DeferredItem<Item> RAW_TERRASLATE = ITEMS.registerSimpleItem("raw_terraslate");

    // Item 93: Maré Abissal Bruta (Tier 2 Água)
    public static final DeferredItem<Item> RAW_ABYSSAL_TIDE = ITEMS.registerSimpleItem("raw_abyssal_tide");

    // Item 94: Tempestade Bruta (Tier 3 Vento)
    public static final DeferredItem<Item> RAW_TEMPEST = ITEMS.registerSimpleItem("raw_tempest");

    // Item 95: Congelamento Bruto (Tier 4 Gelo)
    public static final DeferredItem<Item> RAW_FROSTBITE = ITEMS.registerSimpleItem("raw_frostbite");

    // Item 96: Miasma Bruto (Tier 5 Veneno)
    public static final DeferredItem<Item> RAW_MIASMA = ITEMS.registerSimpleItem("raw_miasma");

    // Item 97: Fulgurita Bruta (Tier 6 Trovão)
    public static final DeferredItem<Item> RAW_FULGURITE = ITEMS.registerSimpleItem("raw_fulgurite");

    // Item 98: Solarium Bruto (Tier 7 Luz)
    public static final DeferredItem<Item> RAW_SOLARIUM = ITEMS.registerSimpleItem("raw_solarium");

    // Item 99: Sombra do Vazio Bruta (Tier 8 Trevas)
    public static final DeferredItem<Item> RAW_VOID_SHADOW = ITEMS.registerSimpleItem("raw_void_shadow");

    // Item 100: Astralita Bruta (Tier 9 Éter)
    public static final DeferredItem<Item> RAW_ASTRALITE = ITEMS.registerSimpleItem("raw_astralite",
            properties -> properties.fireResistant());

    // Item 101: Cronita Bruta (Tier 10 Caos / Tempo)
    public static final DeferredItem<Item> RAW_CHRONIUM = ITEMS.registerSimpleItem("raw_chronium",
            properties -> properties.fireResistant().rarity(Rarity.EPIC));

    // 10 Lingotes / Gemas Elementais Refinados
    // Item 102: Lingote de Terralita (Tier 1 Terra)
    public static final DeferredItem<Item> TERRASLATE_INGOT = ITEMS.registerSimpleItem("terraslate_ingot");

    // Item 103: Lingote da Maré Abissal (Tier 2 Água)
    public static final DeferredItem<Item> ABYSSAL_TIDE_INGOT = ITEMS.registerSimpleItem("abyssal_tide_ingot");

    // Item 104: Lingote da Tempestade (Tier 3 Vento)
    public static final DeferredItem<Item> TEMPEST_INGOT = ITEMS.registerSimpleItem("tempest_ingot");

    // Item 105: Lingote do Congelamento (Tier 4 Gelo)
    public static final DeferredItem<Item> FROSTBITE_INGOT = ITEMS.registerSimpleItem("frostbite_ingot");

    // Item 106: Lingote de Miasma (Tier 5 Veneno)
    public static final DeferredItem<Item> MIASMA_INGOT = ITEMS.registerSimpleItem("miasma_ingot");

    // Item 107: Lingote de Fulgurita (Tier 6 Trovão)
    public static final DeferredItem<Item> FULGURITE_INGOT = ITEMS.registerSimpleItem("fulgurite_ingot");

    // Item 108: Lingote de Solarium (Tier 7 Luz)
    public static final DeferredItem<Item> SOLARIUM_INGOT = ITEMS.registerSimpleItem("solarium_ingot");

    // Item 109: Lingote da Sombra do Vazio (Tier 8 Trevas)
    public static final DeferredItem<Item> VOID_SHADOW_INGOT = ITEMS.registerSimpleItem("void_shadow_ingot");

    // Item 110: Lingote de Astralita (Tier 9 Éter)
    public static final DeferredItem<Item> ASTRALITE_INGOT = ITEMS.registerSimpleItem("astralite_ingot",
            properties -> properties.fireResistant().rarity(Rarity.RARE));

    // Item 111: Lingote de Cronita (Tier 10 Caos / Tempo)
    public static final DeferredItem<Item> CHRONIUM_INGOT = ITEMS.registerSimpleItem("chronium_ingot",
            properties -> properties.fireResistant().rarity(Rarity.EPIC));

    // 5 Ligas Metálicas Especiais Forjadas na Forja Dracônica
    // Item 112: Lingote de Queimadura Glacial (Frostburn Alloy - Gelo + Fogo/Brasa)
    public static final DeferredItem<Item> FROSTBURN_ALLOY_INGOT = ITEMS.registerSimpleItem("frostburn_alloy_ingot",
            properties -> properties.fireResistant());

    // Item 113: Lingote de Liga de Plasma (Plasma Alloy - Trovão + Luz)
    public static final DeferredItem<Item> PLASMA_ALLOY_INGOT = ITEMS.registerSimpleItem("plasma_alloy_ingot",
            properties -> properties.fireResistant().rarity(Rarity.RARE));

    // Item 114: Lingote de Titânio Vulcânico (Volcanic Titanium - Brasa + Terra)
    public static final DeferredItem<Item> VOLCANIC_TITANIUM_INGOT = ITEMS.registerSimpleItem("volcanic_titanium_ingot",
            properties -> properties.fireResistant());

    // Item 115: Lingote de Liga Escaldante (Scalding Alloy - Maré + Brasa)
    public static final DeferredItem<Item> SCALDING_ALLOY_INGOT = ITEMS.registerSimpleItem("scalding_alloy_ingot",
            properties -> properties.fireResistant());

    // Item 116: Lingote de Chama Sombria (Shadowflame Alloy - Vazio + Chamas)
    public static final DeferredItem<Item> SHADOWFLAME_ALLOY_INGOT = ITEMS.registerSimpleItem("shadowflame_alloy_ingot",
            properties -> properties.fireResistant().rarity(Rarity.RARE));
}
