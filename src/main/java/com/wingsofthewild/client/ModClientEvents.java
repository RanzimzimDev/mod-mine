package com.wingsofthewild.client;

import com.wingsofthewild.WingsOfTheWild;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

@EventBusSubscriber(modid = WingsOfTheWild.MODID, value = Dist.CLIENT)
public class ModClientEvents {

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
