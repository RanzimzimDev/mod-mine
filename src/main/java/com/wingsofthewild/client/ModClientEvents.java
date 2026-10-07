package com.wingsofthewild.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import com.wingsofthewild.network.DragonAttackPayload;
import net.minecraft.ChatFormatting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.network.ClientPacketDistributor;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

@EventBusSubscriber(modid = WingsOfTheWild.MODID, value = Dist.CLIENT)
public class ModClientEvents {

    public static final KeyMapping KEY_DRAGON_ATTACK = new KeyMapping(
            "key.wingsofthewild.dragon_attack",
            InputConstants.KEY_R,
            KeyMapping.Category.GAMEPLAY
    );

    public static void registerKeyMappings(RegisterKeyMappingsEvent event) {
        event.register(KEY_DRAGON_ATTACK);
    }

    @SubscribeEvent
    public static void onClientTick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player != null && mc.player.getVehicle() instanceof FlamefangEntity dragon) {
            while (KEY_DRAGON_ATTACK.consumeClick()) {
                ClientPacketDistributor.sendToServer(new DragonAttackPayload(1)); // Fireball
            }
            if (mc.options.keyAttack.consumeClick()) {
                ClientPacketDistributor.sendToServer(new DragonAttackPayload(0)); // Bite on ground, Fireball in air
            }
        }
    }

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {
        ItemStack stack = event.getItemStack();
        if (stack.isEmpty()) return;

        Identifier id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        if (id != null && WingsOfTheWild.MODID.equals(id.getNamespace())) {
            String path = id.getPath();
            String itemDescKey = "item." + WingsOfTheWild.MODID + "." + path + ".desc";
            String blockDescKey = "block." + WingsOfTheWild.MODID + "." + path + ".desc";

            Language lang = Language.getInstance();
            if (lang.has(itemDescKey)) {
                event.getToolTip().add(Component.translatable(itemDescKey).withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
            } else if (lang.has(blockDescKey)) {
                event.getToolTip().add(Component.translatable(blockDescKey).withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
            }
        }
    }
}
