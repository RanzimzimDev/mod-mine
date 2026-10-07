package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.block.DraconicFoundryBlock;
import com.wingsofthewild.block.DraconicHearthBlock;
import com.wingsofthewild.block.TackWorkbenchBlock;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Function;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(WingsOfTheWild.MODID);

    // Sons de pedra calibrados por dureza (pitch mais grave conforme o nível de dureza/tier)
    public static final SoundType TIER_STONE_1 = new SoundType(1.0F, 0.95F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_2 = new SoundType(1.0F, 0.90F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_3 = new SoundType(1.0F, 0.85F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_4 = new SoundType(1.0F, 0.80F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_5 = new SoundType(1.0F, 0.76F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_6 = new SoundType(1.0F, 0.72F, SoundEvents.STONE_BREAK, SoundEvents.STONE_STEP, SoundEvents.STONE_PLACE, SoundEvents.STONE_HIT, SoundEvents.STONE_FALL);
    public static final SoundType TIER_STONE_7 = new SoundType(1.0F, 0.68F, SoundEvents.DEEPSLATE_BREAK, SoundEvents.DEEPSLATE_STEP, SoundEvents.DEEPSLATE_PLACE, SoundEvents.DEEPSLATE_HIT, SoundEvents.DEEPSLATE_FALL);
    public static final SoundType TIER_STONE_8 = new SoundType(1.0F, 0.64F, SoundEvents.DEEPSLATE_BREAK, SoundEvents.DEEPSLATE_STEP, SoundEvents.DEEPSLATE_PLACE, SoundEvents.DEEPSLATE_HIT, SoundEvents.DEEPSLATE_FALL);
    public static final SoundType TIER_STONE_9 = new SoundType(1.0F, 0.60F, SoundEvents.DEEPSLATE_BREAK, SoundEvents.DEEPSLATE_STEP, SoundEvents.DEEPSLATE_PLACE, SoundEvents.DEEPSLATE_HIT, SoundEvents.DEEPSLATE_FALL);
    public static final SoundType TIER_STONE_10 = new SoundType(1.0F, 0.54F, SoundEvents.DEEPSLATE_BREAK, SoundEvents.DEEPSLATE_STEP, SoundEvents.DEEPSLATE_PLACE, SoundEvents.DEEPSLATE_HIT, SoundEvents.DEEPSLATE_FALL);

    // Bloco 01: Ninho Dracônico Artesanal (Bloco rústico de palha e gravetos para chocar ovos)
    public static final DeferredBlock<Block> DRAGON_NEST = registerBlock("dragon_nest",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_BROWN)
                    .strength(0.8F)
                    .sound(SoundType.GRASS)
            )
    );

    // Bloco 02: Fornalha Culinária Dracônica (Estação culinária para rações e ensopados dracônicos)
    public static final DeferredBlock<Block> DRACONIC_HEARTH = registerBlock("draconic_hearth",
            properties -> new DraconicHearthBlock(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 03: Bancada de Selaria Dracônica (Mesa de costura e criação de equipamentos de montaria)
    public static final DeferredBlock<Block> TACK_WORKBENCH = registerBlock("tack_workbench",
            properties -> new TackWorkbenchBlock(properties
                    .mapColor(MapColor.WOOD)
                    .strength(2.5F)
                    .sound(SoundType.WOOD)
            )
    );

    // Bloco 04: Braseiro de Incubação Térmica (Emite calor contínuo para acelerar ninhos próximos)
    public static final DeferredBlock<Block> INCUBATION_BRAZIER = registerBlock("incubation_brazier",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(3.0F)
                    .sound(SoundType.LANTERN)
                    .lightLevel(state -> 15)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 05: Bigorna Dracônica (Usada para forjar e reparar equipamentos pesados de escamas)
    public static final DeferredBlock<Block> DRACONIC_ANVIL = registerBlock("draconic_anvil",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(5.0F, 1200.0F)
                    .sound(SoundType.ANVIL)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 06: Minério de Brasas (Minério vulcânico de montanhas)
    public static final DeferredBlock<Block> EMBER_ORE = registerBlock("ember_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.0F, 3.0F)
                    .requiresCorrectToolForDrops()
                    .sound(TIER_STONE_1)
            )
    );

    // Bloco 07: Minério de Brasas de Ardósia (Variante profunda das camadas inferiores do mundo)
    public static final DeferredBlock<Block> DEEPSLATE_EMBER_ORE = registerBlock("deepslate_ember_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.DEEPSLATE)
                    .strength(4.5F, 3.0F)
                    .sound(TIER_STONE_4)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 08: Bloco de Brasa Bruta (Bloco compacto para armazenamento mineral)
    public static final DeferredBlock<Block> RAW_EMBER_BLOCK = registerBlock("raw_ember_block",
            properties -> new Block(properties
                    .mapColor(MapColor.FIRE)
                    .strength(5.0F, 6.0F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 51: Pedra Dracônica (Rocha vulcânica polida resistente a explosões)
    public static final DeferredBlock<Block> DRACONIC_STONE = registerBlock("draconic_stone",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F, 12.0F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 52: Tijolos de Pedra Dracônica (Alvenaria estilizada para fortalezas)
    public static final DeferredBlock<Block> DRACONIC_STONE_BRICKS = registerBlock("draconic_stone_bricks",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F, 12.0F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 53: Tijolos Dracônicos Cinzelados (Bloco decorativo com entalhe em relevo)
    public static final DeferredBlock<Block> CHISELED_DRACONIC_BRICKS = registerBlock("chiseled_draconic_bricks",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F, 12.0F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 54: Lanterna de Brasas (Iluminação quente com brasas flutuantes)
    public static final DeferredBlock<Block> EMBER_LANTERN = registerBlock("ember_lantern",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(3.5F)
                    .sound(SoundType.LANTERN)
                    .lightLevel(state -> 15)
                    .noOcclusion()
            )
    );

    // Bloco 55: Braseiro Cerimonial de Pedestal (Tocha alta de pedra e fogo eterno)
    public static final DeferredBlock<Block> DRACONIC_BRAZIER_STANDING = registerBlock("draconic_brazier_standing",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .lightLevel(state -> 15)
            )
    );

    // Bloco 56: Crânio Esculpido de Flamefang (Troféu rústico decorativo)
    public static final DeferredBlock<Block> FLAMEFANG_TROPHY_SKULL = registerBlock("flamefang_trophy_skull",
            properties -> new Block(properties
                    .mapColor(MapColor.QUARTZ)
                    .strength(2.0F)
                    .sound(SoundType.BONE_BLOCK)
            )
    );

    // Bloco 57: Palha Chamuscada de Ninho (Bloco macio inflamável para ninhos)
    public static final DeferredBlock<Block> CHARRED_NEST_STRAW = registerBlock("charred_nest_straw",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_BROWN)
                    .strength(0.6F)
                    .sound(SoundType.GRASS)
            )
    );

    // Bloco 58: Poleiro Dracônico (Bloco de pouso onde dragões domesticados descansam)
    public static final DeferredBlock<Block> DRAGON_PERCH = registerBlock("dragon_perch",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.0F)
                    .sound(SoundType.STONE)
            )
    );

    // --- Categoria 12: Sistema de Metalurgia & Ligas Elementais (Tinkers' Style) ---
    // Bloco 81: Forja de Ligas Dracônica (draconic_foundry - força 4.0F, resistência 12.0F, luz 14)
    public static final DeferredBlock<Block> DRACONIC_FOUNDRY = registerBlock("draconic_foundry",
            properties -> new DraconicFoundryBlock(properties
                    .mapColor(MapColor.METAL)
                    .strength(4.0F, 12.0F)
                    .sound(SoundType.NETHERITE_BLOCK)
                    .lightLevel(state -> 14)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 82: Minério de Terralita (Tier 1 Terra - dureza 3.0F)
    public static final DeferredBlock<Block> TERRASLATE_ORE = registerBlock("terraslate_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.0F, 3.0F)
                    .sound(TIER_STONE_1)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 83: Minério da Maré Abissal (Tier 2 Água - dureza 3.5F)
    public static final DeferredBlock<Block> ABYSSAL_TIDE_ORE = registerBlock("abyssal_tide_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_LIGHT_BLUE)
                    .strength(3.5F, 3.5F)
                    .sound(TIER_STONE_2)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 84: Minério da Tempestade (Tier 3 Vento - dureza 4.0F)
    public static final DeferredBlock<Block> TEMPEST_ORE = registerBlock("tempest_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_CYAN)
                    .strength(4.0F, 4.0F)
                    .sound(TIER_STONE_3)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 85: Minério do Congelamento (Tier 4 Gelo - dureza 4.5F)
    public static final DeferredBlock<Block> FROSTBITE_ORE = registerBlock("frostbite_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.ICE)
                    .strength(4.5F, 4.5F)
                    .sound(TIER_STONE_4)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 86: Minério de Miasma (Tier 5 Veneno - dureza 5.0F)
    public static final DeferredBlock<Block> MIASMA_ORE = registerBlock("miasma_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(5.0F, 5.0F)
                    .sound(TIER_STONE_5)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 87: Minério de Fulgurita (Tier 6 Trovão - dureza 5.5F)
    public static final DeferredBlock<Block> FULGURITE_ORE = registerBlock("fulgurite_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_YELLOW)
                    .strength(5.5F, 6.0F)
                    .sound(TIER_STONE_6)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 88: Minério de Solarium (Tier 7 Luz - dureza 6.5F, luz 10)
    public static final DeferredBlock<Block> SOLARIUM_ORE = registerBlock("solarium_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.GOLD)
                    .strength(6.5F, 8.0F)
                    .sound(TIER_STONE_7)
                    .lightLevel(state -> 10)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 89: Minério da Sombra do Vazio (Tier 8 Trevas - dureza 7.5F)
    public static final DeferredBlock<Block> VOID_SHADOW_ORE = registerBlock("void_shadow_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_BLACK)
                    .strength(7.5F, 10.0F)
                    .sound(TIER_STONE_8)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 90: Minério de Astralita (Tier 9 Éter - dureza 9.0F, resistência 20.0F, luz 12)
    public static final DeferredBlock<Block> ASTRALITE_ORE = registerBlock("astralite_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.DIAMOND)
                    .strength(9.0F, 20.0F)
                    .sound(TIER_STONE_9)
                    .lightLevel(state -> 12)
                    .requiresCorrectToolForDrops()
            )
    );

    // Bloco 91: Minério de Cronita (Tier 10 Caos/Tempo - dureza 11.0F, resistência 1200.0F, luz 15)
    public static final DeferredBlock<Block> CHRONIUM_ORE = registerBlock("chronium_ore",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_MAGENTA)
                    .strength(11.0F, 1200.0F)
                    .sound(TIER_STONE_10)
                    .lightLevel(state -> 15)
                    .requiresCorrectToolForDrops()
            )
    );

    private static <T extends Block> DeferredBlock<T> registerBlock(String name, Function<BlockBehaviour.Properties, T> function) {
        DeferredBlock<T> block = BLOCKS.registerBlock(name, function);
        ModItems.ITEMS.registerSimpleBlockItem(name, block);
        return block;
    }
}
