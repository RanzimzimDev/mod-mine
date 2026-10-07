package com.wingsofthewild.block.entity;

import com.wingsofthewild.block.DragonNestBlock;
import com.wingsofthewild.entity.FlamefangEntity;
import com.wingsofthewild.init.ModBlockEntities;
import com.wingsofthewild.init.ModBlocks;
import com.wingsofthewild.init.ModEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;

public class DragonNestBlockEntity extends BlockEntity {
    public static final int MAX_INCUBATION_TICKS = 1200;
    private int incubationTicks = 0;

    public DragonNestBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.DRAGON_NEST.get(), pos, state);
    }

    public int getIncubationTicks() {
        return this.incubationTicks;
    }

    public void setIncubationTicks(int ticks) {
        this.incubationTicks = Math.max(0, ticks);
        setChanged();
    }

    public void resetIncubation() {
        this.incubationTicks = 0;
        setChanged();
    }

    @Override
    protected void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("IncubationTicks", this.incubationTicks);
    }

    @Override
    protected void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        this.incubationTicks = input.getIntOr("IncubationTicks", 0);
    }

    public static boolean isHeatSource(BlockState state) {
        if (state.is(ModBlocks.INCUBATION_BRAZIER.get())) {
            return true;
        }
        if (state.is(Blocks.FIRE) || state.is(Blocks.SOUL_FIRE)) {
            return true;
        }
        if (state.is(Blocks.MAGMA_BLOCK) || state.is(Blocks.LAVA)) {
            return true;
        }
        if (state.is(Blocks.CAMPFIRE) || state.is(Blocks.SOUL_CAMPFIRE)) {
            return state.hasProperty(CampfireBlock.LIT) ? state.getValue(CampfireBlock.LIT) : true;
        }
        return false;
    }

    public static int getHeatRate(Level level, BlockPos pos) {
        int heatRate = 0;
        // Direct heat from underneath (foundation)
        BlockState belowState = level.getBlockState(pos.below());
        if (isHeatSource(belowState)) {
            heatRate += belowState.is(ModBlocks.INCUBATION_BRAZIER.get()) ? 3 : 2;
        }
        // Lateral heat from adjacent sides
        for (Direction dir : Direction.Plane.HORIZONTAL) {
            BlockState adjState = level.getBlockState(pos.relative(dir));
            if (isHeatSource(adjState)) {
                heatRate += 1;
            }
        }
        return heatRate;
    }

    public static void serverTick(Level level, BlockPos pos, BlockState state, DragonNestBlockEntity blockEntity) {
        if (!state.getValue(DragonNestBlock.HAS_EGG)) {
            if (blockEntity.incubationTicks > 0) {
                blockEntity.incubationTicks = 0;
                blockEntity.setChanged();
            }
            return;
        }

        if (!(level instanceof ServerLevel serverLevel)) {
            return;
        }

        int heat = getHeatRate(level, pos);
        if (heat > 0) {
            blockEntity.incubationTicks += heat;
            blockEntity.setChanged();

            RandomSource random = serverLevel.getRandom();

            // Thermal incubation particles
            if (random.nextFloat() < 0.35F) {
                double px = pos.getX() + 0.35 + random.nextDouble() * 0.3;
                double py = pos.getY() + 0.45 + random.nextDouble() * 0.25;
                double pz = pos.getZ() + 0.35 + random.nextDouble() * 0.3;
                serverLevel.sendParticles(ParticleTypes.FLAME, px, py, pz, 1, 0.0, 0.015, 0.0, 0.005);
            }
            if (random.nextFloat() < 0.25F) {
                double px = pos.getX() + 0.3 + random.nextDouble() * 0.4;
                double py = pos.getY() + 0.6;
                double pz = pos.getZ() + 0.3 + random.nextDouble() * 0.4;
                serverLevel.sendParticles(ParticleTypes.SMOKE, px, py, pz, 1, 0.0, 0.025, 0.0, 0.005);
            }

            // Hatching condition
            if (blockEntity.incubationTicks >= MAX_INCUBATION_TICKS) {
                hatchEgg(serverLevel, pos, state, blockEntity);
            }
        }
    }

    private static void hatchEgg(ServerLevel serverLevel, BlockPos pos, BlockState state, DragonNestBlockEntity blockEntity) {
        RandomSource random = serverLevel.getRandom();

        // Cracking and emergence sound
        serverLevel.playSound(null, pos, SoundEvents.TURTLE_EGG_BREAK, SoundSource.BLOCKS, 1.2F, 0.9F + random.nextFloat() * 0.2F);

        // Burst of thermal flame and ember particles
        serverLevel.sendParticles(ParticleTypes.FLAME, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 20, 0.25, 0.25, 0.25, 0.05);
        serverLevel.sendParticles(ParticleTypes.LAVA, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 5, 0.2, 0.2, 0.2, 0.0);

        // Spawn baby Flamefang dragon
        FlamefangEntity baby = ModEntities.FLAMEFANG.get().create(serverLevel, EntitySpawnReason.BREEDING);
        if (baby != null) {
            baby.setStage(FlamefangEntity.STAGE_HATCHLING);
            baby.snapTo(pos.getX() + 0.5, pos.getY() + 0.2, pos.getZ() + 0.5, random.nextFloat() * 360.0F, 0.0F);
            serverLevel.addFreshEntity(baby);
        }

        // Reset blockstate and incubation ticks
        serverLevel.setBlock(pos, state.setValue(DragonNestBlock.HAS_EGG, false), Block.UPDATE_ALL);
        blockEntity.incubationTicks = 0;
        blockEntity.setChanged();
    }
}
