package com.wingsofthewild.block;

import com.wingsofthewild.block.entity.DragonNestBlockEntity;
import com.wingsofthewild.init.ModBlockEntities;
import com.wingsofthewild.init.ModItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

public class DragonNestBlock extends Block implements EntityBlock {
    public static final BooleanProperty HAS_EGG = BooleanProperty.create("has_egg");
    private static final VoxelShape SHAPE = Block.box(0.0, 0.0, 0.0, 16.0, 7.0, 16.0);

    public DragonNestBlock(BlockBehaviour.Properties properties) {
        super(properties);
        this.registerDefaultState(this.stateDefinition.any().setValue(HAS_EGG, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(HAS_EGG);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    protected InteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        if (stack.is(ModItems.FLAMEFANG_EGG.get()) && !state.getValue(HAS_EGG)) {
            if (!level.isClientSide()) {
                if (!player.getAbilities().instabuild) {
                    stack.shrink(1);
                }
                level.setBlock(pos, state.setValue(HAS_EGG, true), Block.UPDATE_ALL);
                if (level.getBlockEntity(pos) instanceof DragonNestBlockEntity nestEntity) {
                    nestEntity.resetIncubation();
                }
                level.playSound(null, pos, SoundEvents.CHICKEN_EGG, SoundSource.BLOCKS, 1.0F, 1.0F);
            }
            return InteractionResult.SUCCESS;
        }

        if (state.getValue(HAS_EGG) && (stack.is(ModItems.REFINED_EMBER_CORE.get()) || stack.is(net.minecraft.world.item.Items.BLAZE_POWDER) || stack.is(net.minecraft.world.item.Items.FIRE_CHARGE))) {
            if (!level.isClientSide()) {
                if (!player.getAbilities().instabuild) {
                    stack.shrink(1);
                }
                if (level.getBlockEntity(pos) instanceof DragonNestBlockEntity nestEntity) {
                    nestEntity.setIncubationTicks(nestEntity.getIncubationTicks() + 300);
                }
                level.playSound(null, pos, SoundEvents.FIRECHARGE_USE, SoundSource.BLOCKS, 1.0F, 1.2F);
                if (level instanceof ServerLevel sl) {
                    sl.sendParticles(ParticleTypes.FLAME, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 12, 0.2, 0.2, 0.2, 0.05);
                }
            }
            return InteractionResult.SUCCESS;
        }
        return super.useItemOn(stack, state, level, pos, player, hand, hitResult);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (state.getValue(HAS_EGG)) {
            if (!level.isClientSide()) {
                ItemStack eggStack = new ItemStack(ModItems.FLAMEFANG_EGG.get());
                if (!player.getInventory().add(eggStack)) {
                    popResource(level, pos, eggStack);
                }
                level.setBlock(pos, state.setValue(HAS_EGG, false), Block.UPDATE_ALL);
                if (level.getBlockEntity(pos) instanceof DragonNestBlockEntity nestEntity) {
                    nestEntity.resetIncubation();
                }
                level.playSound(null, pos, SoundEvents.CHICKEN_EGG, SoundSource.BLOCKS, 1.0F, 1.2F);
            }
            return InteractionResult.SUCCESS;
        }
        return super.useWithoutItem(state, level, pos, player, hitResult);
    }

    @Override
    public void destroy(LevelAccessor level, BlockPos pos, BlockState state) {
        if (state.getValue(HAS_EGG) && level instanceof Level lvl && !lvl.isClientSide()) {
            popResource(lvl, pos, new ItemStack(ModItems.FLAMEFANG_EGG.get()));
        }
        super.destroy(level, pos, state);
    }

    @Nullable
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new DragonNestBlockEntity(pos, state);
    }

    @Nullable
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> blockEntityType) {
        if (level.isClientSide()) {
            return null;
        }
        return blockEntityType == ModBlockEntities.DRAGON_NEST.get()
                ? (lvl, p, st, be) -> DragonNestBlockEntity.serverTick(lvl, p, st, (DragonNestBlockEntity) be)
                : null;
    }
}
