package com.wingsofthewild.block.entity;

import com.wingsofthewild.init.ModBlockEntities;
import com.wingsofthewild.init.ModItems;
import com.wingsofthewild.world.inventory.DraconicFoundryMenu;
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

public class DraconicFoundryBlockEntity extends BlockEntity implements WorldlyContainer, net.minecraft.world.MenuProvider {
    public static final int INPUT_SLOT_A = 0;
    public static final int INPUT_SLOT_B = 1;
    public static final int FUEL_SLOT = 2;
    public static final int RESULT_SLOT = 3;
    public static final int CONTAINER_SIZE = 4;

    private static final int[] SLOTS_TOP = new int[]{INPUT_SLOT_A, INPUT_SLOT_B};
    private static final int[] SLOTS_SIDES = new int[]{FUEL_SLOT};
    private static final int[] SLOTS_BOTTOM = new int[]{RESULT_SLOT};

    private final NonNullList<ItemStack> items = NonNullList.withSize(CONTAINER_SIZE, ItemStack.EMPTY);
    private int litTime = 0;
    private int litDuration = 0;
    private int cookingProgress = 0;
    private int cookingTotalTime = 200;

    protected final ContainerData dataAccess = new ContainerData() {
        @Override
        public int get(int index) {
            return switch (index) {
                case 0 -> DraconicFoundryBlockEntity.this.litTime;
                case 1 -> DraconicFoundryBlockEntity.this.litDuration;
                case 2 -> DraconicFoundryBlockEntity.this.cookingProgress;
                case 3 -> DraconicFoundryBlockEntity.this.cookingTotalTime;
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
            switch (index) {
                case 0 -> DraconicFoundryBlockEntity.this.litTime = value;
                case 1 -> DraconicFoundryBlockEntity.this.litDuration = value;
                case 2 -> DraconicFoundryBlockEntity.this.cookingProgress = value;
                case 3 -> DraconicFoundryBlockEntity.this.cookingTotalTime = value;
            }
        }

        @Override
        public int getCount() {
            return 4;
        }
    };

    public DraconicFoundryBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.DRACONIC_FOUNDRY.get(), pos, state);
    }

    public static void serverTick(Level level, BlockPos pos, BlockState state, DraconicFoundryBlockEntity entity) {
        boolean wasLit = entity.litTime > 0;
        boolean changed = false;

        if (entity.litTime > 0) {
            entity.litTime--;
        }

        ItemStack inputA = entity.items.get(INPUT_SLOT_A);
        ItemStack inputB = entity.items.get(INPUT_SLOT_B);
        ItemStack resultOutput = entity.getSmeltingResult(inputA, inputB);

        boolean canSmelt = !resultOutput.isEmpty() && entity.canInsertResult(resultOutput);

        if (canSmelt) {
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
                entity.cookingProgress++;
                if (entity.cookingProgress >= entity.cookingTotalTime) {
                    entity.cookingProgress = 0;
                    entity.smeltItem(resultOutput);
                    changed = true;
                }
            } else {
                if (entity.cookingProgress > 0) {
                    entity.cookingProgress = Math.max(0, entity.cookingProgress - 2);
                }
            }
        } else {
            if (entity.cookingProgress > 0) {
                entity.cookingProgress = Math.max(0, entity.cookingProgress - 2);
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

    private void smeltItem(ItemStack result) {
        ItemStack current = this.items.get(RESULT_SLOT);
        if (current.isEmpty()) {
            this.items.set(RESULT_SLOT, result.copy());
        } else if (ItemStack.isSameItemSameComponents(current, result)) {
            current.grow(result.getCount());
        }

        // Consume inputs
        ItemStack inputA = this.items.get(INPUT_SLOT_A);
        ItemStack inputB = this.items.get(INPUT_SLOT_B);

        // Check if both or one are required
        boolean usesB = requiresSlotB(inputA, inputB);
        if (!inputA.isEmpty()) inputA.shrink(1);
        if (usesB && !inputB.isEmpty()) inputB.shrink(1);
    }

    private boolean requiresSlotB(ItemStack a, ItemStack b) {
        if (a.is(ModItems.RAW_EMBER.get()) && b.is(ModItems.RAW_EMBER.get())) return true;
        if (a.is(ModItems.RAW_EMBER.get()) && b.is(Items.IRON_INGOT)) return true;
        if (a.is(Items.IRON_INGOT) && b.is(ModItems.RAW_EMBER.get())) return true;
        if (a.is(ModItems.FLAMEFANG_SHED_TOOTH.get()) && b.is(ModItems.EMBER_INGOT.get())) return true;
        if (a.is(ModItems.EMBER_INGOT.get()) && b.is(ModItems.FLAMEFANG_SHED_TOOTH.get())) return true;
        return false;
    }

    private ItemStack getSmeltingResult(ItemStack a, ItemStack b) {
        if (a.isEmpty() && b.isEmpty()) return ItemStack.EMPTY;

        // Two-ingredient alloy recipes
        if (a.is(ModItems.RAW_EMBER.get()) && b.is(ModItems.RAW_EMBER.get())) {
            return new ItemStack(ModItems.REFINED_EMBER_CORE.get());
        }
        if ((a.is(ModItems.RAW_EMBER.get()) && b.is(Items.IRON_INGOT)) || (a.is(Items.IRON_INGOT) && b.is(ModItems.RAW_EMBER.get()))) {
            return new ItemStack(ModItems.HARDENED_SCALE_PLATE.get());
        }
        if ((a.is(ModItems.FLAMEFANG_SHED_TOOTH.get()) && b.is(ModItems.EMBER_INGOT.get())) || (a.is(ModItems.EMBER_INGOT.get()) && b.is(ModItems.FLAMEFANG_SHED_TOOTH.get()))) {
            return new ItemStack(ModItems.FLAMEFANG_DAGGER.get());
        }

        // Single-ingredient smelting (Slot A or Slot B)
        ItemStack single = !a.isEmpty() ? a : b;
        if (single.is(ModItems.RAW_EMBER.get())) return new ItemStack(ModItems.EMBER_INGOT.get());
        if (single.is(ModItems.RAW_TERRASLATE.get())) return new ItemStack(ModItems.TERRASLATE_INGOT.get());
        if (single.is(ModItems.RAW_ABYSSAL_TIDE.get())) return new ItemStack(ModItems.ABYSSAL_TIDE_INGOT.get());
        if (single.is(ModItems.RAW_TEMPEST.get())) return new ItemStack(ModItems.TEMPEST_INGOT.get());
        if (single.is(ModItems.RAW_FROSTBITE.get())) return new ItemStack(ModItems.FROSTBITE_INGOT.get());
        if (single.is(ModItems.RAW_MIASMA.get())) return new ItemStack(ModItems.MIASMA_INGOT.get());
        if (single.is(ModItems.RAW_FULGURITE.get())) return new ItemStack(ModItems.FULGURITE_INGOT.get());
        if (single.is(ModItems.RAW_SOLARIUM.get())) return new ItemStack(ModItems.SOLARIUM_INGOT.get());
        if (single.is(ModItems.RAW_VOID_SHADOW.get())) return new ItemStack(ModItems.VOID_SHADOW_INGOT.get());
        if (single.is(ModItems.RAW_ASTRALITE.get())) return new ItemStack(ModItems.ASTRALITE_INGOT.get());
        if (single.is(ModItems.RAW_CHRONIUM.get())) return new ItemStack(ModItems.CHRONIUM_INGOT.get());

        // Vanilla ores compatibility
        if (single.is(Items.RAW_IRON) || single.is(Items.IRON_ORE) || single.is(Items.DEEPSLATE_IRON_ORE)) {
            return new ItemStack(Items.IRON_INGOT);
        }
        if (single.is(Items.RAW_GOLD) || single.is(Items.GOLD_ORE) || single.is(Items.DEEPSLATE_GOLD_ORE)) {
            return new ItemStack(Items.GOLD_INGOT);
        }
        if (single.is(Items.RAW_COPPER) || single.is(Items.COPPER_ORE) || single.is(Items.DEEPSLATE_COPPER_ORE)) {
            return new ItemStack(Items.COPPER_INGOT);
        }

        return ItemStack.EMPTY;
    }

    private int getFuelBurnTime(Level level, ItemStack fuel) {
        if (fuel.isEmpty()) return 0;
        if (fuel.is(ModItems.REFINED_EMBER_CORE.get())) return 6400;
        if (fuel.is(ModItems.RAW_EMBER.get())) return 1600;
        if (fuel.is(ModItems.VOLCANIC_ASH.get())) return 800;
        if (fuel.is(Items.LAVA_BUCKET)) return 20000;
        if (fuel.is(Items.BLAZE_ROD)) return 2400;
        if (fuel.is(Items.COAL_BLOCK)) return 16000;
        if (fuel.is(Items.COAL) || fuel.is(Items.CHARCOAL)) return 1600;
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
        output.putInt("CookingProgress", this.cookingProgress);
        output.putInt("CookingTotalTime", this.cookingTotalTime);
    }

    @Override
    protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        ContainerHelper.loadAllItems(input, this.items);
        this.litTime = input.getIntOr("LitTime", 0);
        this.litDuration = input.getIntOr("LitDuration", 0);
        this.cookingProgress = input.getIntOr("CookingProgress", 0);
        this.cookingTotalTime = input.getIntOr("CookingTotalTime", 200);
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
        return Component.translatable("container.wingsofthewild.draconic_foundry");
    }

    @Nullable
    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new DraconicFoundryMenu(
                containerId,
                playerInventory,
                this,
                this.dataAccess,
                ContainerLevelAccess.create(this.level, this.worldPosition)
        );
    }
}
