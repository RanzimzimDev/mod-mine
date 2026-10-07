package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ToolMaterial;

public class ModToolMaterials {
    public static final TagKey<Item> EMBER_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "ember_tool_materials")
    );

    public static final ToolMaterial EMBER = new ToolMaterial(
            BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
            1561,
            8.0F,
            3.0F,
            14,
            EMBER_TOOL_MATERIALS
    );

    // --- Tiers Elementais de Metalurgia (Tinkers' Style - Tiers 1 a 10) ---

    // Tier 1: Terralita (Terra)
    public static final TagKey<Item> TERRASLATE_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "terraslate_tool_materials")
    );
    public static final ToolMaterial TERRASLATE = new ToolMaterial(
            BlockTags.INCORRECT_FOR_IRON_TOOL,
            450,
            6.5F,
            2.0F,
            10,
            TERRASLATE_TOOL_MATERIALS
    );

    // Tier 2: Maré Abissal (Água)
    public static final TagKey<Item> ABYSSAL_TIDE_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "abyssal_tide_tool_materials")
    );
    public static final ToolMaterial ABYSSAL_TIDE = new ToolMaterial(
            BlockTags.INCORRECT_FOR_IRON_TOOL,
            650,
            7.0F,
            2.5F,
            12,
            ABYSSAL_TIDE_TOOL_MATERIALS
    );

    // Tier 3: Tempestade (Vento)
    public static final TagKey<Item> TEMPEST_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "tempest_tool_materials")
    );
    public static final ToolMaterial TEMPEST = new ToolMaterial(
            BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
            900,
            8.0F,
            3.0F,
            14,
            TEMPEST_TOOL_MATERIALS
    );

    // Tier 4: Congelamento (Gelo)
    public static final TagKey<Item> FROSTBITE_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "frostbite_tool_materials")
    );
    public static final ToolMaterial FROSTBITE = new ToolMaterial(
            BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
            1200,
            8.5F,
            3.5F,
            15,
            FROSTBITE_TOOL_MATERIALS
    );

    // Tier 5: Miasma (Veneno)
    public static final TagKey<Item> MIASMA_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "miasma_tool_materials")
    );
    public static final ToolMaterial MIASMA = new ToolMaterial(
            BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
            1500,
            9.0F,
            4.0F,
            16,
            MIASMA_TOOL_MATERIALS
    );

    // Tier 6: Fulgurita (Trovão)
    public static final TagKey<Item> FULGURITE_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "fulgurite_tool_materials")
    );
    public static final ToolMaterial FULGURITE = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            1900,
            10.0F,
            4.5F,
            18,
            FULGURITE_TOOL_MATERIALS
    );

    // Tier 7: Solarium (Luz)
    public static final TagKey<Item> SOLARIUM_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "solarium_tool_materials")
    );
    public static final ToolMaterial SOLARIUM = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            2400,
            11.5F,
            5.0F,
            20,
            SOLARIUM_TOOL_MATERIALS
    );

    // Tier 8: Sombra do Vazio (Trevas)
    public static final TagKey<Item> VOID_SHADOW_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "void_shadow_tool_materials")
    );
    public static final ToolMaterial VOID_SHADOW = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            3000,
            13.0F,
            6.0F,
            22,
            VOID_SHADOW_TOOL_MATERIALS
    );

    // Tier 9: Astralita (Éter)
    public static final TagKey<Item> ASTRALITE_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "astralite_tool_materials")
    );
    public static final ToolMaterial ASTRALITE = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            3800,
            15.0F,
            7.0F,
            25,
            ASTRALITE_TOOL_MATERIALS
    );

    // Tier 10: Cronita (Caos / Tempo)
    public static final TagKey<Item> CHRONIUM_TOOL_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "chronium_tool_materials")
    );
    public static final ToolMaterial CHRONIUM = new ToolMaterial(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            5000,
            18.0F,
            8.5F,
            30,
            CHRONIUM_TOOL_MATERIALS
    );
}
