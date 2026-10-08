package com.wingsofthewild.block.entity;

import com.wingsofthewild.init.ModBlockEntities;
import com.wingsofthewild.init.ModItems;
import com.wingsofthewild.world.inventory.DraconicHearthMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.NonNullList;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Container;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.WorldlyContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jetbrains.annotations.Nullable;

public class DraconicHearthBlockEntity extends BlockEntity implements WorldlyContainer, net.minecraft.world.MenuProvider {
    public static final int INGREDIENT_SLOT_A = 0;
    public static final int INGREDIENT_SLOT_B = 1;
    public static final int FUEL_SLOT = 2;
    public static final int RESULT_SLOT = 3;
    public static final int CONTAINER_SIZE = 4;

    private static final int[] SLOTS_TOP = new int[]{INGREDIENT_SLOT_A, INGREDIENT_SLOT_B};
    private static final int[] SLOTS_SIDES = new int[]{FUEL_SLOT};
    private static final int[] SLOTS_BOTTOM = new int[]{RESULT_SLOT};

    private final NonNullList<ItemStack> items = NonNullList.withSize(CONTAINER_SIZE, ItemStack.EMPTY);
    private int litTime = 0;
    private int litDuration = 0;
    private int cookProgress = 0;
    private int cookTotalTime = 160;

    protected final ContainerData dataAccess = new ContainerData() {
        @Override
        public int get(int index) {
            return switch (index) {
                case 0 -> DraconicHearthBlockEntity.this.litTime;
                case 1 -> DraconicHearthBlockEntity.this.litDuration;
                case 2 -> DraconicHearthBlockEntity.this.cookProgress;
                case 3 -> DraconicHearthBlockEntity.this.cookTotalTime;
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
            switch (index) {
                case 0 -> DraconicHearthBlockEntity.this.litTime = value;
                case 1 -> DraconicHearthBlockEntity.this.litDuration = value;
                case 2 -> DraconicHearthBlockEntity.this.cookProgress = value;
                case 3 -> DraconicHearthBlockEntity.this.cookTotalTime = value;
            }
        }

        @Override
        public int getCount() {
            return 4;
        }
    };

    public DraconicHearthBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.DRACONIC_HEARTH.get(), pos, state);
    }

    public static void serverTick(Level level, BlockPos pos, BlockState state, DraconicHearthBlockEntity entity) {
        boolean wasLit = entity.litTime > 0;
        boolean changed = false;

        if (entity.litTime > 0) {
            entity.litTime--;
        }

        ItemStack inputA = entity.items.get(INGREDIENT_SLOT_A);
        ItemStack inputB = entity.items.get(INGREDIENT_SLOT_B);
        ItemStack resultOutput = entity.getCookingResult(inputA, inputB);

        boolean canCook = !resultOutput.isEmpty() && entity.canInsertResult(resultOutput);

        if (canCook) {
            if (entity.litTime <= 0) {
                ItemStack fuel = entity.items.get(FUEL_SLOT);
                int burnTime = entity.getFuelBurnTime(level, fuel);
                if (burnTime > 0) {
                    entity.litTime = burnTime;
                    entity.litDuration = burnTime;
                    if (fuel.is(Items.LAVA_BUCKET)) {
                        entity.items.set(FUEL_SLOT, new ItemStack(Items.BUCKET));
                    } else {
                        fuel.shrink(1);
                    }
                    changed = true;
                }
            }

            if (entity.litTime > 0) {
                entity.cookProgress++;
                if (entity.cookProgress >= entity.cookTotalTime) {
                    entity.cookProgress = 0;
                    entity.cookItem(resultOutput);
                    changed = true;
                }
            } else {
                if (entity.cookProgress > 0) {
                    entity.cookProgress = Math.max(0, entity.cookProgress - 2);
                }
            }
        } else {
            if (entity.cookProgress > 0) {
                entity.cookProgress = Math.max(0, entity.cookProgress - 2);
            }
        }

        if (wasLit != (entity.litTime > 0) || changed) {
            entity.setChanged();
        }
    }

    private boolean canInsertResult(ItemStack result) {
        ItemStack current = this.items.get(RESULT_SLOT);
        if (current.isEmpty()) return true;
        if (!ItemStack.isSameItemSameComponents(current, result)) return false;
        return current.getCount() + result.getCount() <= current.getMaxStackSize();
    }

    private void cookItem(ItemStack result) {
        ItemStack current = this.items.get(RESULT_SLOT);
        if (current.isEmpty()) {
            this.items.set(RESULT_SLOT, result.copy());
        } else if (ItemStack.isSameItemSameComponents(current, result)) {
            current.grow(result.getCount());
        }

        // Consume ingredients
        ItemStack inputA = this.items.get(INGREDIENT_SLOT_A);
        ItemStack inputB = this.items.get(INGREDIENT_SLOT_B);

        boolean usesB = requiresSlotB(inputA, inputB);
        if (!inputA.isEmpty()) inputA.shrink(1);
        if (usesB && !inputB.isEmpty()) inputB.shrink(1);
    }

    private boolean requiresSlotB(ItemStack a, ItemStack b) {
        if ((a.is(ModItems.SPICY_MAGMA_BERRIES.get()) && (b.is(Items.SUGAR) || b.is(Items.WHEAT)))
                || (b.is(ModItems.SPICY_MAGMA_BERRIES.get()) && (a.is(Items.SUGAR) || a.is(Items.WHEAT)))) return true;
        if ((a.is(Items.BOWL) && (b.is(ModItems.SPICY_MAGMA_BERRIES.get()) || b.is(ModItems.CHARRED_MEAT.get())))
                || (b.is(Items.BOWL) && (a.is(ModItems.SPICY_MAGMA_BERRIES.get()) || a.is(ModItems.CHARRED_MEAT.get())))) return true;
        if ((a.is(Items.SUGAR) && b.is(ModItems.RAW_EMBER.get())) || (b.is(Items.SUGAR) && a.is(ModItems.RAW_EMBER.get()))) return true;
        if ((a.is(Items.HONEYCOMB) && b.is(ModItems.VOLCANIC_ASH.get())) || (b.is(Items.HONEYCOMB) && a.is(ModItems.VOLCANIC_ASH.get()))) return true;
        if ((a.is(Items.GLASS_BOTTLE) && b.is(ModItems.SPICY_MAGMA_BERRIES.get())) || (b.is(Items.GLASS_BOTTLE) && a.is(ModItems.SPICY_MAGMA_BERRIES.get()))) return true;
        if ((a.is(Items.WHEAT) && b.is(ModItems.VOLCANIC_ASH.get())) || (b.is(Items.WHEAT) && a.is(ModItems.VOLCANIC_ASH.get()))) return true;
        return false;
    }

    private ItemStack getCookingResult(ItemStack a, ItemStack b) {
        if (a.isEmpty() && b.isEmpty()) return ItemStack.EMPTY;

        // Two-ingredient culinary recipes
        if ((a.is(ModItems.SPICY_MAGMA_BERRIES.get()) && (b.is(Items.SUGAR) || b.is(Items.WHEAT)))
                || (b.is(ModItems.SPICY_MAGMA_BERRIES.get()) && (a.is(Items.SUGAR) || a.is(Items.WHEAT)))) {
            return new ItemStack(ModItems.MOLTEN_BERRY_TART.get());
        }
        if ((a.is(Items.BOWL) && (b.is(ModItems.SPICY_MAGMA_BERRIES.get()) || b.is(ModItems.CHARRED_MEAT.get())))
                || (b.is(Items.BOWL) && (a.is(ModItems.SPICY_MAGMA_BERRIES.get()) || a.is(ModItems.CHARRED_MEAT.get())))) {
            return new ItemStack(ModItems.SMOKE_INFUSED_BROTH.get());
        }
        if ((a.is(Items.SUGAR) && b.is(ModItems.RAW_EMBER.get())) || (b.is(Items.SUGAR) && a.is(ModItems.RAW_EMBER.get()))) {
            return new ItemStack(ModItems.FIRE_CRYSTAL_CANDY.get());
        }
        if ((a.is(Items.HONEYCOMB) && b.is(ModItems.VOLCANIC_ASH.get())) || (b.is(Items.HONEYCOMB) && a.is(ModItems.VOLCANIC_ASH.get()))) {
            return new ItemStack(ModItems.BONDING_HONEYCOMB.get());
        }
        if ((a.is(Items.GLASS_BOTTLE) && b.is(ModItems.SPICY_MAGMA_BERRIES.get())) || (b.is(Items.GLASS_BOTTLE) && a.is(ModItems.SPICY_MAGMA_BERRIES.get()))) {
            return new ItemStack(ModItems.VITALITY_ESSENCE.get());
        }
        if ((a.is(Items.WHEAT) && b.is(ModItems.VOLCANIC_ASH.get())) || (b.is(Items.WHEAT) && a.is(ModItems.VOLCANIC_ASH.get()))) {
            return new ItemStack(ModItems.DRACONIC_TREAT.get(), 2);
        }

        // Single ingredient cooking
        ItemStack single = !a.isEmpty() ? a : b;
        if (single.is(Items.BEEF) || single.is(Items.PORKCHOP) || single.is(Items.MUTTON) || single.is(Items.CHICKEN) || single.is(Items.RABBIT)) {
            return new ItemStack(ModItems.CHARRED_MEAT.get());
        }
        if (single.is(Items.POTATO)) return new ItemStack(Items.BAKED_POTATO);
        if (single.is(Items.COD)) return new ItemStack(Items.COOKED_COD);
        if (single.is(Items.SALMON)) return new ItemStack(Items.COOKED_SALMON);
        if (single.is(Items.KELP)) return new ItemStack(Items.DRIED_KELP);

        return ItemStack.EMPTY;
    }

    private int getFuelBurnTime(Level level, ItemStack fuel) {
        if (fuel.isEmpty()) return 0;
        if (fuel.is(ModItems.RAW_EMBER.get())) return 1600;
        if (fuel.is(ModItems.VOLCANIC_ASH.get())) return 800;
        if (fuel.is(Items.COAL_BLOCK)) return 16000;
        if (fuel.is(Items.COAL) || fuel.is(Items.CHARCOAL)) return 1600;
        if (fuel.is(Items.BLAZE_ROD)) return 2400;
        if (fuel.is(Items.DRIED_KELP_BLOCK)) return 4000;
        if (fuel.is(Items.STICK)) return 100;
        if (fuel.is(net.minecraft.tags.ItemTags.LOGS) || fuel.is(net.minecraft.tags.ItemTags.PLANKS)) return 300;
        return 0;
    }

    @Override
    protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        ContainerHelper.saveAllItems(output, this.items);
        output.putInt("LitTime", this.litTime);
        output.putInt("LitDuration", this.litDuration);
        output.putInt("CookProgress", this.cookProgress);
        output.putInt("CookTotalTime", this.cookTotalTime);
    }

    @Override
    protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        ContainerHelper.loadAllItems(input, this.items);
        this.litTime = input.getIntOr("LitTime", 0);
        this.litDuration = input.getIntOr("LitDuration", 0);
        this.cookProgress = input.getIntOr("CookProgress", 0);
        this.cookTotalTime = input.getIntOr("CookTotalTime", 160);
    }

    @Override
    public int getContainerSize() {
        return CONTAINER_SIZE;
    }

    @Override
    public boolean isEmpty() {
        for (ItemStack stack : this.items) {
            if (!stack.isEmpty()) return false;
        }
        return true;
    }

    @Override
    public ItemStack getItem(int slot) {
        return this.items.get(slot);
    }

    @Override
    public ItemStack removeItem(int slot, int amount) {
        ItemStack result = ContainerHelper.removeItem(this.items, slot, amount);
        if (!result.isEmpty()) setChanged();
        return result;
    }

    @Override
    public ItemStack removeItemNoUpdate(int slot) {
        return ContainerHelper.takeItem(this.items, slot);
    }

    @Override
    public void setItem(int slot, ItemStack stack) {
        this.items.set(slot, stack);
        if (stack.getCount() > this.getMaxStackSize(stack)) {
            stack.setCount(this.getMaxStackSize(stack));
        }
        setChanged();
    }

    @Override
    public boolean stillValid(Player player) {
        return Container.stillValidBlockEntity(this, player);
    }

    @Override
    public void clearContent() {
        this.items.clear();
        setChanged();
    }

    @Override
    public int[] getSlotsForFace(Direction side) {
        if (side == Direction.DOWN) return SLOTS_BOTTOM;
        if (side == Direction.UP) return SLOTS_TOP;
        return SLOTS_SIDES;
    }

    @Override
    public boolean canPlaceItemThroughFace(int slot, ItemStack stack, @Nullable Direction side) {
        if (slot == RESULT_SLOT) return false;
        if (slot == FUEL_SLOT) return side != Direction.UP;
        return side != Direction.DOWN;
    }

    @Override
    public boolean canTakeItemThroughFace(int slot, ItemStack stack, Direction side) {
        return slot == RESULT_SLOT;
    }

    @Override
    public Component getDisplayName() {
        return Component.translatable("container.wingsofthewild.draconic_hearth");
    }

    @Nullable
    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new DraconicHearthMenu(
                containerId,
                playerInventory,
                this,
                this.dataAccess,
                ContainerLevelAccess.create(this.level, this.worldPosition)
        );
    }
}
