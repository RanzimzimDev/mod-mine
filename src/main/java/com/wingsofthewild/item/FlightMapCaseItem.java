package com.wingsofthewild.item;

import com.wingsofthewild.client.gui.FlightMapCaseScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class FlightMapCaseItem extends Item {
    public FlightMapCaseItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide()) {
            openMapCaseScreen();
        }
        return InteractionResult.SUCCESS;
    }

    private void openMapCaseScreen() {
        Minecraft.getInstance().setScreenAndShow(new FlightMapCaseScreen());
    }
}
