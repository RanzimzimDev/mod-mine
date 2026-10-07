package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, WingsOfTheWild.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> WINGS_OF_THE_WILD_TAB =
            CREATIVE_MODE_TABS.register("wings_of_the_wild_tab", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.wingsofthewild"))
                    .withTabsBefore(CreativeModeTabs.COMBAT)
                    .icon(() -> ModItems.FLAMEFANG_SCALE.get().getDefaultInstance())
                    .displayItems((parameters, output) -> {
                        // Blocos Utilitários, Minérios e Decoração
                        output.accept(ModBlocks.DRAGON_NEST.get());
                        output.accept(ModBlocks.DRACONIC_HEARTH.get());
                        output.accept(ModBlocks.TACK_WORKBENCH.get());
                        output.accept(ModBlocks.INCUBATION_BRAZIER.get());
                        output.accept(ModBlocks.DRACONIC_ANVIL.get());
                        output.accept(ModBlocks.EMBER_ORE.get());
                        output.accept(ModBlocks.DEEPSLATE_EMBER_ORE.get());
                        output.accept(ModBlocks.RAW_EMBER_BLOCK.get());
                        output.accept(ModBlocks.DRACONIC_STONE.get());
                        output.accept(ModBlocks.DRACONIC_STONE_BRICKS.get());
                        output.accept(ModBlocks.CHISELED_DRACONIC_BRICKS.get());
                        output.accept(ModBlocks.EMBER_LANTERN.get());
                        output.accept(ModBlocks.DRACONIC_BRAZIER_STANDING.get());
                        output.accept(ModBlocks.FLAMEFANG_TROPHY_SKULL.get());
                        output.accept(ModBlocks.CHARRED_NEST_STRAW.get());
                        output.accept(ModBlocks.DRAGON_PERCH.get());

                        // Materiais e Matérias-Primas
                        output.accept(ModItems.RAW_EMBER.get());
                        output.accept(ModItems.EMBER_INGOT.get());
                        output.accept(ModItems.FLAME_CORE.get());
                        output.accept(ModItems.FLAMEFANG_SCALE.get());
                        output.accept(ModItems.RAW_DRACONIC_HIDE.get());
                        output.accept(ModItems.TANNED_DRACONIC_LEATHER.get());
                        output.accept(ModItems.DRAGON_BONE.get());
                        output.accept(ModItems.DRACONIC_SINEW.get());
                        output.accept(ModItems.VOLCANIC_ASH.get());
                        output.accept(ModItems.SULFUR_CRYSTAL.get());
                        // Materiais Intermediários e Relíquias (76 a 80)
                        output.accept(ModItems.FLAMEFANG_SHED_TOOTH.get());
                        output.accept(ModItems.REFINED_EMBER_CORE.get());
                        output.accept(ModItems.CHARRED_BONE_NEEDLE.get());
                        output.accept(ModItems.HARDENED_SCALE_PLATE.get());
                        output.accept(ModItems.ANCIENT_DRAGON_RELIC.get());

                        // Ciclo de Vida, Ovos e Cuidados Dracônicos
                        output.accept(ModItems.FLAMEFANG_EGG.get());
                        output.accept(ModItems.CRACKED_FLAMEFANG_EGG_1.get());
                        output.accept(ModItems.CRACKED_FLAMEFANG_EGG_2.get());
                        output.accept(ModItems.DRAGON_BRUSH.get());
                        output.accept(ModItems.DRAGON_FLUTE.get());
                        output.accept(ModItems.DRAGON_STAFF.get());
                        output.accept(ModItems.BONDING_COLLAR.get());

                        // Culinária e Nutrição Dracônica (26 a 35 + 71 a 75)
                        output.accept(ModItems.SPICY_MAGMA_BERRIES.get());
                        output.accept(ModItems.CHARRED_MEAT.get());
                        output.accept(ModItems.ASH_STEW.get());
                        output.accept(ModItems.DRACONIC_TREAT.get());
                        output.accept(ModItems.SULFUR_BISCUIT.get());
                        output.accept(ModItems.FIRE_PEPPER.get());
                        output.accept(ModItems.BLAZING_JERKY.get());
                        output.accept(ModItems.HEARTY_DRAGON_MASH.get());
                        output.accept(ModItems.GLOW_KELP_ROLL.get());
                        output.accept(ModItems.FLAME_DRAUGHT.get());
                        output.accept(ModItems.FIRE_CRYSTAL_CANDY.get());
                        output.accept(ModItems.SMOKE_INFUSED_BROTH.get());
                        output.accept(ModItems.MOLTEN_BERRY_TART.get());
                        output.accept(ModItems.BONDING_HONEYCOMB.get());
                        output.accept(ModItems.VITALITY_ESSENCE.get());

                        // Selaria e Equipamentos do Dragão (36 a 43)
                        output.accept(ModItems.BASIC_DRAGON_SADDLE.get());
                        output.accept(ModItems.REINFORCED_FLAME_SADDLE.get());
                        output.accept(ModItems.SMALL_DRAGON_POUCH.get());
                        output.accept(ModItems.LARGE_DRAGON_SADDLEBAGS.get());
                        output.accept(ModItems.FLAMEFANG_SCALE_ARMOR.get());
                        output.accept(ModItems.EMBER_PLATED_ARMOR.get());
                        output.accept(ModItems.DRAGON_HEADSTALL.get());
                        output.accept(ModItems.FLIGHT_GOGGLES.get());

                        // Equipamentos Táticos e Voo Avançado (65 a 70)
                        output.accept(ModItems.DRAGON_HORN.get());
                        output.accept(ModItems.REINFORCED_REINS.get());
                        output.accept(ModItems.TAIL_FLAME_GUARD.get());
                        output.accept(ModItems.FLIGHT_MAP_CASE.get());
                        output.accept(ModItems.DRAGON_BEACON_FIRE.get());
                        output.accept(ModItems.SADDLE_CHEST_UPGRADE.get());

                        // Ferramentas, Armas e Conhecimento (44 a 50)
                        output.accept(ModItems.EMBER_SWORD.get());
                        output.accept(ModItems.EMBER_PICKAXE.get());
                        output.accept(ModItems.EMBER_AXE.get());
                        output.accept(ModItems.EMBER_SHOVEL.get());
                        output.accept(ModItems.FLAMEFANG_DAGGER.get());
                        output.accept(ModItems.DRAGON_WHISTLE.get());
                        output.accept(ModItems.DRAGONOLOGIST_TOME.get());

                        // Armadura de Escamas do Jogador e Vestimentas (59 a 64)
                        output.accept(ModItems.FLAMEFANG_HELMET.get());
                        output.accept(ModItems.FLAMEFANG_CHESTPLATE.get());
                        output.accept(ModItems.FLAMEFANG_LEGGINGS.get());
                        output.accept(ModItems.FLAMEFANG_BOOTS.get());
                        output.accept(ModItems.DRAGON_HANDLER_GLOVES.get());
                        output.accept(ModItems.DRAGON_RIDERS_CLOAK.get());

                        // Metalurgia & Ligas Elementais (Tinkers' Style - 81 a 116)
                        // Forja e Minérios de Bloco
                        output.accept(ModBlocks.DRACONIC_FOUNDRY.get());
                        output.accept(ModBlocks.TERRASLATE_ORE.get());
                        output.accept(ModBlocks.ABYSSAL_TIDE_ORE.get());
                        output.accept(ModBlocks.TEMPEST_ORE.get());
                        output.accept(ModBlocks.FROSTBITE_ORE.get());
                        output.accept(ModBlocks.MIASMA_ORE.get());
                        output.accept(ModBlocks.FULGURITE_ORE.get());
                        output.accept(ModBlocks.SOLARIUM_ORE.get());
                        output.accept(ModBlocks.VOID_SHADOW_ORE.get());
                        output.accept(ModBlocks.ASTRALITE_ORE.get());
                        output.accept(ModBlocks.CHRONIUM_ORE.get());

                        // Minérios Brutos Elementais
                        output.accept(ModItems.RAW_TERRASLATE.get());
                        output.accept(ModItems.RAW_ABYSSAL_TIDE.get());
                        output.accept(ModItems.RAW_TEMPEST.get());
                        output.accept(ModItems.RAW_FROSTBITE.get());
                        output.accept(ModItems.RAW_MIASMA.get());
                        output.accept(ModItems.RAW_FULGURITE.get());
                        output.accept(ModItems.RAW_SOLARIUM.get());
                        output.accept(ModItems.RAW_VOID_SHADOW.get());
                        output.accept(ModItems.RAW_ASTRALITE.get());
                        output.accept(ModItems.RAW_CHRONIUM.get());

                        // Lingotes e Gemas Elementais
                        output.accept(ModItems.TERRASLATE_INGOT.get());
                        output.accept(ModItems.ABYSSAL_TIDE_INGOT.get());
                        output.accept(ModItems.TEMPEST_INGOT.get());
                        output.accept(ModItems.FROSTBITE_INGOT.get());
                        output.accept(ModItems.MIASMA_INGOT.get());
                        output.accept(ModItems.FULGURITE_INGOT.get());
                        output.accept(ModItems.SOLARIUM_INGOT.get());
                        output.accept(ModItems.VOID_SHADOW_INGOT.get());
                        output.accept(ModItems.ASTRALITE_INGOT.get());
                        output.accept(ModItems.CHRONIUM_INGOT.get());

                        // Ligas Metálicas Especiais
                        output.accept(ModItems.FROSTBURN_ALLOY_INGOT.get());
                        output.accept(ModItems.PLASMA_ALLOY_INGOT.get());
                        output.accept(ModItems.VOLCANIC_TITANIUM_INGOT.get());
                        output.accept(ModItems.SCALDING_ALLOY_INGOT.get());
                        output.accept(ModItems.SHADOWFLAME_ALLOY_INGOT.get());
                    })
                    .build());
}
