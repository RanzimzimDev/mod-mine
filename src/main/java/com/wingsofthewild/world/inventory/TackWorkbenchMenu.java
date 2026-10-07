package com.wingsofthewild.world.inventory;

import com.wingsofthewild.init.ModBlocks;
import com.wingsofthewild.init.ModMenuTypes;
import net.minecraft.network.protocol.game.ClientboundContainerSetSlotPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.Container;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.item.crafting.RecipeType;
import org.jspecify.annotations.Nullable;

import java.util.Optional;

public class TackWorkbenchMenu extends AbstractCraftingMenu {
    public static final int RESULT_SLOT = 0;
    private static final int CRAFT_SLOT_START = 1;
    private static final int CRAFT_SLOT_COUNT = 9;
    private static final int INV_SLOT_START = 10;
    private static final int INV_SLOT_END = 37;
    private static final int HOTBAR_SLOT_START = 37;
    private static final int HOTBAR_SLOT_END = 46;

    private final ContainerLevelAccess access;
    private final Player player;
    private boolean placingRecipe;

    public TackWorkbenchMenu(int containerId, Inventory playerInventory) {
        this(containerId, playerInventory, ContainerLevelAccess.NULL);
    }

    public TackWorkbenchMenu(int containerId, Inventory playerInventory, ContainerLevelAccess access) {
        super(ModMenuTypes.TACK_WORKBENCH.get(), containerId, 3, 3);
        this.access = access;
        this.player = playerInventory.player;

        // Slot de Saída dos Equipamentos Dracônicos
        this.addResultSlot(this.player, 124, 35);

        // Grade 3x3 de Alfaiataria & Selaria Dracônica
        this.addCraftingGridSlots(30, 17);

        // Inventário e Hotbar do Jogador
        this.addStandardInventorySlots(playerInventory, 8, 84);
    }

    protected static void updateCraftingResult(
            AbstractContainerMenu menu,
            ServerLevel level,
            Player player,
            CraftingContainer container,
            ResultContainer resultSlots,
            @Nullable RecipeHolder<CraftingRecipe> recipeHint
    ) {
        CraftingInput input = container.asCraftInput();
        ServerPlayer serverPlayer = (ServerPlayer) player;
        ItemStack result = ItemStack.EMPTY;
        Optional<RecipeHolder<CraftingRecipe>> maybeRecipe = level.getServer().getRecipeManager().getRecipeFor(RecipeType.CRAFTING, input, level, recipeHint);
        if (maybeRecipe.isPresent()) {
            RecipeHolder<CraftingRecipe> recipeHolder = maybeRecipe.get();
            CraftingRecipe craftingRecipe = recipeHolder.value();
            if (resultSlots.setRecipeUsed(serverPlayer, recipeHolder)) {
                ItemStack recipeResult = craftingRecipe.assemble(input);
                if (recipeResult.isItemEnabled(level.enabledFeatures())) {
                    result = recipeResult;
                }
            }
        }

        resultSlots.setItem(0, result);
        menu.setRemoteSlot(0, result);
        serverPlayer.connection.send(new ClientboundContainerSetSlotPacket(menu.containerId, menu.incrementStateId(), 0, result));
    }

    @Override
    public void slotsChanged(Container container) {
        if (!this.placingRecipe) {
            this.access.execute((level, pos) -> {
                if (level instanceof ServerLevel serverLevel) {
                    updateCraftingResult(this, serverLevel, this.player, this.craftSlots, this.resultSlots, null);
                }
            });
        }
    }

    @Override
    public void beginPlacingRecipe() {
        this.placingRecipe = true;
    }

    @Override
    public void finishPlacingRecipe(ServerLevel level, RecipeHolder<CraftingRecipe> recipe) {
        this.placingRecipe = false;
        updateCraftingResult(this, level, this.player, this.craftSlots, this.resultSlots, recipe);
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        this.access.execute((level, pos) -> this.clearContainer(player, this.craftSlots));
    }

    @Override
    protected Player owner() {
        return this.player;
    }

    @Override
    public Slot getResultSlot() {
        return this.slots.get(0);
    }

    @Override
    public java.util.List<Slot> getInputGridSlots() {
        return this.slots.subList(1, 10);
    }

    @Override
    public RecipeBookType getRecipeBookType() {
        return RecipeBookType.CRAFTING;
    }

    @Override
    public boolean stillValid(Player player) {
        return stillValid(this.access, player, ModBlocks.TACK_WORKBENCH.get());
    }

    @Override
    public ItemStack quickMoveStack(Player player, int slotIndex) {
        ItemStack clicked = ItemStack.EMPTY;
        Slot slot = this.slots.get(slotIndex);
        if (slot != null && slot.hasItem()) {
            ItemStack stack = slot.getItem();
            clicked = stack.copy();
            if (slotIndex == RESULT_SLOT) {
                stack.getItem().onCraftedBy(stack, player);
                if (!this.moveItemStackTo(stack, INV_SLOT_START, HOTBAR_SLOT_END, true)) {
                    return ItemStack.EMPTY;
                }
                slot.onQuickCraft(stack, clicked);
            } else if (slotIndex >= INV_SLOT_START && slotIndex < HOTBAR_SLOT_END) {
                if (!this.moveItemStackTo(stack, CRAFT_SLOT_START, INV_SLOT_START, false)) {
                    if (slotIndex < INV_SLOT_END) {
                        if (!this.moveItemStackTo(stack, HOTBAR_SLOT_START, HOTBAR_SLOT_END, false)) {
                            return ItemStack.EMPTY;
                        }
                    } else if (!this.moveItemStackTo(stack, INV_SLOT_START, INV_SLOT_END, false)) {
                        return ItemStack.EMPTY;
                    }
                }
            } else if (!this.moveItemStackTo(stack, INV_SLOT_START, HOTBAR_SLOT_END, false)) {
                return ItemStack.EMPTY;
            }

            if (stack.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }

            if (stack.getCount() == clicked.getCount()) {
                return ItemStack.EMPTY;
            }

            slot.onTake(player, stack);
        }

        return clicked;
    }
}
