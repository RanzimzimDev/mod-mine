package com.wingsofthewild.world.inventory;

import com.wingsofthewild.init.ModMenuTypes;
import com.wingsofthewild.item.DragonPouchItem;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemContainerContents;

public class DragonPouchMenu extends AbstractContainerMenu {
    private final Container container;
    private final int containerRows;
    private final ItemStack pouchStack;
    private final int blockedSlot;

    public DragonPouchMenu(int containerId, Inventory playerInventory, int rows, int blockedSlot) {
        this(containerId, playerInventory, new SimpleContainer(rows * 9), ItemStack.EMPTY, blockedSlot, rows);
    }

    public DragonPouchMenu(int containerId, Inventory playerInventory, Container container, ItemStack pouchStack, int blockedSlot, int rows) {
        super(ModMenuTypes.DRAGON_POUCH.get(), containerId);
        checkContainerSize(container, rows * 9);
        this.container = container;
        this.containerRows = rows;
        this.pouchStack = pouchStack;
        this.blockedSlot = blockedSlot;

        container.startOpen(playerInventory.player);

        // 1. Grade da Bolsa Dracônica (9 ou 27 slots)
        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < 9; x++) {
                this.addSlot(new Slot(container, x + y * 9, 8 + x * 18, 18 + y * 18) {
                    @Override
                    public boolean mayPlace(ItemStack stack) {
                        return !(stack.getItem() instanceof DragonPouchItem);
                    }
                });
            }
        }

        // 2. Inventário do Jogador (3 linhas de 9 slots)
        int inventoryTop = 18 + rows * 18 + 13;
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                int slotIndex = col + row * 9 + 9;
                int x = 8 + col * 18;
                int y = inventoryTop + row * 18;
                if (slotIndex == blockedSlot) {
                    this.addSlot(new Slot(playerInventory, slotIndex, x, y) {
                        @Override
                        public boolean mayPickup(Player player) {
                            return false;
                        }
                    });
                } else {
                    this.addSlot(new Slot(playerInventory, slotIndex, x, y));
                }
            }
        }

        // 3. Hotbar do Jogador (1 linha de 9 slots)
        int hotbarTop = inventoryTop + 58;
        for (int col = 0; col < 9; col++) {
            int slotIndex = col;
            int x = 8 + col * 18;
            int y = hotbarTop;
            if (slotIndex == blockedSlot) {
                this.addSlot(new Slot(playerInventory, slotIndex, x, y) {
                    @Override
                    public boolean mayPickup(Player player) {
                        return false;
                    }
                });
            } else {
                this.addSlot(new Slot(playerInventory, slotIndex, x, y));
            }
        }
    }

    public int getRowCount() {
        return this.containerRows;
    }

    public Container getContainer() {
        return this.container;
    }

    @Override
    public boolean stillValid(Player player) {
        return this.container.stillValid(player);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int slotIndex) {
        ItemStack clicked = ItemStack.EMPTY;
        Slot slot = this.slots.get(slotIndex);
        if (slot != null && slot.hasItem()) {
            ItemStack stack = slot.getItem();
            clicked = stack.copy();
            int pouchSlots = this.containerRows * 9;

            if (slotIndex < pouchSlots) {
                // Da bolsa para o inventário do jogador
                if (!this.moveItemStackTo(stack, pouchSlots, this.slots.size(), true)) {
                    return ItemStack.EMPTY;
                }
            } else {
                // Não permitir guardar uma bolsa dentro de outra bolsa
                if (stack.getItem() instanceof DragonPouchItem) {
                    return ItemStack.EMPTY;
                }
                // Do inventário para a bolsa
                if (!this.moveItemStackTo(stack, 0, pouchSlots, false)) {
                    return ItemStack.EMPTY;
                }
            }

            if (stack.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
        }
        return clicked;
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        this.container.stopOpen(player);
        savePouchContents();
    }

    @Override
    public void slotsChanged(Container container) {
        super.slotsChanged(container);
        savePouchContents();
    }

    private void savePouchContents() {
        if (!this.pouchStack.isEmpty()) {
            java.util.List<ItemStack> items = new java.util.ArrayList<>();
            for (int i = 0; i < this.container.getContainerSize(); i++) {
                items.add(this.container.getItem(i));
            }
            this.pouchStack.set(DataComponents.CONTAINER, ItemContainerContents.fromItems(items));
        }
    }
}
