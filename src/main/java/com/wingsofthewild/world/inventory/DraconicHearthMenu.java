package com.wingsofthewild.world.inventory;

import com.wingsofthewild.init.ModBlocks;
import com.wingsofthewild.init.ModMenuTypes;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.*;
import net.minecraft.world.item.ItemStack;

public class DraconicHearthMenu extends AbstractContainerMenu {
    public static final int INGREDIENT_SLOT_A = 0;
    public static final int INGREDIENT_SLOT_B = 1;
    public static final int FUEL_SLOT = 2;
    public static final int RESULT_SLOT = 3;
    public static final int CONTAINER_SLOT_COUNT = 4;

    private static final int INV_SLOT_START = 4;
    private static final int INV_SLOT_END = 31;
    private static final int HOTBAR_SLOT_START = 31;
    private static final int HOTBAR_SLOT_END = 40;

    private final Container container;
    private final ContainerData data;
    private final ContainerLevelAccess access;

    public DraconicHearthMenu(int containerId, Inventory playerInventory) {
        this(containerId, playerInventory, new SimpleContainer(CONTAINER_SLOT_COUNT), new SimpleContainerData(4), ContainerLevelAccess.NULL);
    }

    public DraconicHearthMenu(int containerId, Inventory playerInventory, Container container, ContainerData data, ContainerLevelAccess access) {
        super(ModMenuTypes.DRACONIC_HEARTH.get(), containerId);
        checkContainerSize(container, CONTAINER_SLOT_COUNT);
        checkContainerDataCount(data, 4);

        this.container = container;
        this.data = data;
        this.access = access;

        container.startOpen(playerInventory.player);

        // Slot 0: Ingrediente Principal (Carne vulcânica, bagas fundidas, mel)
        this.addSlot(new Slot(container, INGREDIENT_SLOT_A, 45, 19));

        // Slot 1: Ingrediente Secundário / Tempero / Tigela
        this.addSlot(new Slot(container, INGREDIENT_SLOT_B, 67, 19));

        // Slot 2: Combustível Culinário Térmico (Brasa, carvão vegetal, gravetos vulcânicos)
        this.addSlot(new Slot(container, FUEL_SLOT, 56, 53));

        // Slot 3: Prato Dracônico Preparado (Apenas retirada)
        this.addSlot(new Slot(container, RESULT_SLOT, 126, 35) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }
        });

        // Inventário e Hotbar do Jogador
        this.addStandardInventorySlots(playerInventory, 8, 84);

        // Sincronização de dados de cocção culinária
        this.addDataSlots(data);
    }

    public boolean isLit() {
        return this.data.get(0) > 0;
    }

    public int getLitProgress() {
        int litDuration = this.data.get(1);
        if (litDuration == 0) {
            litDuration = 200;
        }
        return this.data.get(0) * 13 / litDuration;
    }

    public int getCookProgress() {
        int cookingProgress = this.data.get(2);
        int cookingTotalTime = this.data.get(3);
        if (cookingTotalTime == 0) {
            cookingTotalTime = 200;
        }
        return cookingProgress * 24 / cookingTotalTime;
    }

    @Override
    public boolean stillValid(Player player) {
        return stillValid(this.access, player, ModBlocks.DRACONIC_HEARTH.get());
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack itemstack = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot != null && slot.hasItem()) {
            ItemStack slotStack = slot.getItem();
            itemstack = slotStack.copy();

            if (index == RESULT_SLOT) {
                if (!this.moveItemStackTo(slotStack, INV_SLOT_START, HOTBAR_SLOT_END, true)) {
                    return ItemStack.EMPTY;
                }
                slot.onQuickCraft(slotStack, itemstack);
            } else if (index != FUEL_SLOT && index != INGREDIENT_SLOT_A && index != INGREDIENT_SLOT_B) {
                // Do inventário para o fogão dracônico
                if (!this.moveItemStackTo(slotStack, INGREDIENT_SLOT_A, INGREDIENT_SLOT_B + 1, false)) {
                    if (!this.moveItemStackTo(slotStack, FUEL_SLOT, FUEL_SLOT + 1, false)) {
                        if (index >= INV_SLOT_START && index < INV_SLOT_END) {
                            if (!this.moveItemStackTo(slotStack, HOTBAR_SLOT_START, HOTBAR_SLOT_END, false)) {
                                return ItemStack.EMPTY;
                            }
                        } else if (index >= HOTBAR_SLOT_START && index < HOTBAR_SLOT_END && !this.moveItemStackTo(slotStack, INV_SLOT_START, INV_SLOT_END, false)) {
                            return ItemStack.EMPTY;
                        }
                    }
                }
            } else if (!this.moveItemStackTo(slotStack, INV_SLOT_START, HOTBAR_SLOT_END, false)) {
                return ItemStack.EMPTY;
            }

            if (slotStack.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }

            if (slotStack.getCount() == itemstack.getCount()) {
                return ItemStack.EMPTY;
            }

            slot.onTake(player, slotStack);
        }

        return itemstack;
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        this.container.stopOpen(player);
    }
}
