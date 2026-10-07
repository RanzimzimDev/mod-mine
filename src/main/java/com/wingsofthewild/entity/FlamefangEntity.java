package com.wingsofthewild.entity;

import com.geckolib.animatable.GeoEntity;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.animation.AnimationController;
import com.geckolib.animation.RawAnimation;
import com.geckolib.animation.object.PlayState;
import com.geckolib.util.GeckoLibUtil;
import com.wingsofthewild.init.ModEntities;
import com.wingsofthewild.init.ModItems;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowOwnerGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.SitWhenOrderedToGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.OwnerHurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.OwnerHurtTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class FlamefangEntity extends TamableAnimal implements GeoEntity {

    private static final EntityDataAccessor<Boolean> DATA_FLYING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_GLIDING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_SLEEPING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_ROARING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_EATING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);

    private final AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);
    private int roarTicks = 0;
    private int eatingTicks = 0;

    public FlamefangEntity(EntityType<? extends TamableAnimal> entityType, Level level) {
        super(entityType, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 120.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.32D)
                .add(Attributes.ATTACK_DAMAGE, 12.0D)
                .add(Attributes.ARMOR, 8.0D)
                .add(Attributes.FOLLOW_RANGE, 48.0D)
                .add(Attributes.FLYING_SPEED, 0.6D);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_FLYING, false);
        builder.define(DATA_GLIDING, false);
        builder.define(DATA_SLEEPING, false);
        builder.define(DATA_ROARING, false);
        builder.define(DATA_EATING, false);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(1, new FloatGoal(this));
        this.goalSelector.addGoal(2, new SitWhenOrderedToGoal(this));
        this.goalSelector.addGoal(3, new MeleeAttackGoal(this, 1.25D, true));
        this.goalSelector.addGoal(4, new FollowOwnerGoal(this, 1.2D, 10.0F, 3.0F));
        this.goalSelector.addGoal(5, new BreedGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(8, new RandomLookAroundGoal(this));

        this.targetSelector.addGoal(1, new OwnerHurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new OwnerHurtTargetGoal(this));
        this.targetSelector.addGoal(3, new HurtByTargetGoal(this));
    }

    @Override
    public void aiStep() {
        super.aiStep();

        if (this.roarTicks > 0) {
            this.roarTicks--;
            if (this.roarTicks == 0) {
                this.setRoaring(false);
            }
        }

        if (this.eatingTicks > 0) {
            this.eatingTicks--;
            if (this.eatingTicks == 0) {
                this.setEating(false);
            }
        }
    }

    public boolean isFlying() {
        return this.entityData.get(DATA_FLYING);
    }

    public void setFlying(boolean flying) {
        this.entityData.set(DATA_FLYING, flying);
    }

    public boolean isGliding() {
        return this.entityData.get(DATA_GLIDING);
    }

    public void setGliding(boolean gliding) {
        this.entityData.set(DATA_GLIDING, gliding);
    }

    public boolean isSleepingDragon() {
        return this.entityData.get(DATA_SLEEPING);
    }

    public void setSleepingDragon(boolean sleeping) {
        this.entityData.set(DATA_SLEEPING, sleeping);
    }

    public boolean isRoaring() {
        return this.entityData.get(DATA_ROARING);
    }

    public void setRoaring(boolean roaring) {
        this.entityData.set(DATA_ROARING, roaring);
        if (roaring) {
            this.roarTicks = 70; // 3.5 segundos
        }
    }

    public boolean isEating() {
        return this.entityData.get(DATA_EATING);
    }

    public void setEating(boolean eating) {
        this.entityData.set(DATA_EATING, eating);
        if (eating) {
            this.eatingTicks = 64; // 3.2 segundos
        }
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack itemstack = player.getItemInHand(hand);

        if (this.isFood(itemstack)) {
            if (!this.level().isClientSide()) {
                if (!this.isTame()) {
                    if (this.random.nextInt(3) == 0) {
                        this.tame(player);
                        this.level().broadcastEntityEvent(this, (byte) 7);
                    } else {
                        this.level().broadcastEntityEvent(this, (byte) 6);
                    }
                } else if (this.getHealth() < this.getMaxHealth()) {
                    this.heal(15.0F);
                }
                this.setEating(true);
                itemstack.consume(1, player);
                this.playSound(SoundEvents.GENERIC_EAT.value(), 1.0F, 0.8F);
            }
            return InteractionResult.SUCCESS;
        }

        if (this.isTame() && this.isOwnedBy(player)) {
            if (player.isSecondaryUseActive()) {
                this.setRoaring(true);
                this.playSound(SoundEvents.ENDER_DRAGON_GROWL, 1.2F, 0.9F);
                return InteractionResult.SUCCESS;
            } else if (!this.isFlying()) {
                this.setOrderedToSit(!this.isOrderedToSit());
                return InteractionResult.SUCCESS;
            }
        }

        return super.mobInteract(player, hand);
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(ModItems.SPICY_MAGMA_BERRIES.get())
                || stack.is(ModItems.CHARRED_MEAT.get())
                || stack.is(ModItems.DRACONIC_TREAT.get());
    }

    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob otherParent) {
        return ModEntities.FLAMEFANG.get().create(level, EntitySpawnReason.BREEDING);
    }

    @Override
    public boolean fireImmune() {
        return true;
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource damageSource, float amount) {
        if (damageSource.is(net.minecraft.tags.DamageTypeTags.IS_FIRE)) {
            return false;
        }
        return super.hurtServer(level, damageSource, amount);
    }

    // --- GeckoLib 5.5.7 Animation System ---
    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        // 1. Locomotion Controller: Idle, Walk, Fly Flap, Glide, Sleep
        controllers.add(new AnimationController<FlamefangEntity>("movement", 5, state -> {
            if (this.isSleepingDragon() || this.isOrderedToSit()) {
                return state.setAndContinue(RawAnimation.begin().thenLoop("sleep"));
            }
            if (this.isFlying()) {
                if (this.isGliding()) {
                    return state.setAndContinue(RawAnimation.begin().thenLoop("glide"));
                }
                return state.setAndContinue(RawAnimation.begin().thenLoop("fly_flap"));
            }
            if (state.isMoving()) {
                return state.setAndContinue(RawAnimation.begin().thenLoop("walk"));
            }
            return state.setAndContinue(RawAnimation.begin().thenLoop("idle"));
        }));

        // 2. Action Controller: Eating, Roar, Bite
        controllers.add(new AnimationController<FlamefangEntity>("actions", 4, state -> {
            if (this.isRoaring()) {
                return state.setAndContinue(RawAnimation.begin().thenPlay("roar"));
            }
            if (this.isEating()) {
                return state.setAndContinue(RawAnimation.begin().thenLoop("eating"));
            }
            return PlayState.STOP;
        }));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.geoCache;
    }
}
