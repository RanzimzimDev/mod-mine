package com.wingsofthewild.item;

import com.wingsofthewild.world.inventory.DragonPouchMenu;
import net.minecraft.core.component.DataComponents;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemContainerContents;
import net.minecraft.world.level.Level;

public class DragonPouchItem extends Item {
    private final int rows;

    public DragonPouchItem(Properties properties, int rows) {
        super(properties);
        this.rows = rows;
    }

    public int getRows() {
        return this.rows;
    }

    public int getSlotCount() {
        return this.rows * 9;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack held = player.getItemInHand(hand);
        if (!level.isClientSide() && player instanceof ServerPlayer serverPlayer) {
            int slotIndex = (hand == InteractionHand.MAIN_HAND) ? player.getInventory().getSelectedSlot() : 40;
            int rowCount = this.rows;
            int totalSlots = rowCount * 9;

            SimpleContainer container = new SimpleContainer(totalSlots);
            ItemContainerContents contents = held.getOrDefault(DataComponents.CONTAINER, ItemContainerContents.EMPTY);
            contents.copyInto(container.getItems());

            serverPlayer.openMenu(new SimpleMenuProvider(
                    (containerId, inventory, p) -> new DragonPouchMenu(containerId, inventory, container, held, slotIndex, rowCount),
                    held.getHoverName()
            ), buffer -> {
                buffer.writeInt(rowCount);
                buffer.writeInt(slotIndex);
            });

            level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.BUNDLE_DROP_CONTENTS, SoundSource.PLAYERS, 0.8F, 1.0F);
        }
        return InteractionResult.SUCCESS;
    }
}
