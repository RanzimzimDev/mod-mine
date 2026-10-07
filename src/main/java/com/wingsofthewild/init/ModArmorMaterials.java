package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;

public class ModArmorMaterials {
    public static final TagKey<Item> FLAMEFANG_REPAIR_MATERIALS = TagKey.create(
            Registries.ITEM,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_scale")
    );

    public static final ResourceKey<EquipmentAsset> FLAMEFANG_ASSET = ResourceKey.create(
            EquipmentAssets.ROOT_ID,
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang")
    );

    public static final ArmorMaterial FLAMEFANG = new ArmorMaterial(
            37,
            Map.of(
                    ArmorType.BOOTS, 3,
                    ArmorType.LEGGINGS, 6,
                    ArmorType.CHESTPLATE, 8,
                    ArmorType.HELMET, 3,
                    ArmorType.BODY, 11
            ),
            15,
            SoundEvents.ARMOR_EQUIP_NETHERITE,
            3.0F,
            0.1F,
            FLAMEFANG_REPAIR_MATERIALS,
            FLAMEFANG_ASSET
    );
}
