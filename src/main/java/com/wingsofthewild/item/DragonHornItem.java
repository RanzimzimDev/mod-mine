package com.wingsofthewild.item;

import com.wingsofthewild.client.gui.DragonHornScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class DragonHornItem extends Item {
    public DragonHornItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide()) {
            openHornScreen();
        }
        return InteractionResult.SUCCESS;
    }

    private void openHornScreen() {
        Minecraft.getInstance().setScreenAndShow(new DragonHornScreen());
    }
}
