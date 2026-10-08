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
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.PlayerRideableJumping;
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
import net.minecraft.world.entity.projectile.hurtingprojectile.LargeFireball;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

public class FlamefangEntity extends TamableAnimal implements GeoEntity, PlayerRideableJumping {

    public static final int STAGE_HATCHLING = 0;
    public static final int STAGE_JUVENILE = 1;
    public static final int STAGE_ADULT = 2;

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
    private static final EntityDataAccessor<Boolean> DATA_SADDLED =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_ARMORED =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Integer> DATA_STAGE =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Integer> DATA_GROWTH_PROGRESS =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Boolean> DATA_BITING =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Boolean> DATA_SHOOTING_FIREBALL =
            SynchedEntityData.defineId(FlamefangEntity.class, EntityDataSerializers.BOOLEAN);

    private final AnimatableInstanceCache geoCache = GeckoLibUtil.createInstanceCache(this);
    private int roarTicks = 0;
    private int eatingTicks = 0;
    private int biteTicks = 0;
    private int fireballTicks = 0;
    private int fireballCooldown = 0;
    private int ageTicks = 0;

    public FlamefangEntity(EntityType<? extends TamableAnimal> entityType, Level level) {
        super(entityType, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 120.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.32D)
                .add(Attributes.ATTACK_DAMAGE, 14.0D)
                .add(Attributes.ARMOR, 8.0D)
                .add(Attributes.FOLLOW_RANGE, 48.0D)
                .add(Attributes.FLYING_SPEED, 0.6D)
                .add(Attributes.SCALE, 1.0D);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_FLYING, false);
        builder.define(DATA_GLIDING, false);
        builder.define(DATA_SLEEPING, false);
        builder.define(DATA_ROARING, false);
        builder.define(DATA_EATING, false);
        builder.define(DATA_SADDLED, false);
        builder.define(DATA_ARMORED, false);
        builder.define(DATA_STAGE, STAGE_ADULT);
        builder.define(DATA_GROWTH_PROGRESS, 0);
        builder.define(DATA_BITING, false);
        builder.define(DATA_SHOOTING_FIREBALL, false);
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

        if (this.biteTicks > 0) {
            this.biteTicks--;
            if (this.biteTicks == 0) {
                this.setBiting(false);
            }
        }

        if (this.fireballTicks > 0) {
            this.fireballTicks--;
            if (this.fireballTicks == 0) {
                this.setShootingFireball(false);
            }
        }

        if (this.fireballCooldown > 0) {
            this.fireballCooldown--;
        }

        // Natural growth aging
        if (!this.level().isClientSide()) {
            if (this.getStage() == STAGE_HATCHLING) {
                this.ageTicks++;
                if (this.ageTicks >= 12000) { // 10 minutes natural time
                    this.setStage(STAGE_JUVENILE);
                    this.ageTicks = 0;
                    this.playSound(SoundEvents.PLAYER_LEVELUP, 1.4F, 1.1F);
                    if (this.level() instanceof ServerLevel sl) {
                        sl.sendParticles(ParticleTypes.HAPPY_VILLAGER, this.getX(), this.getY() + 0.5, this.getZ(), 20, 0.5, 0.5, 0.5, 0.1);
                        sl.sendParticles(ParticleTypes.FLAME, this.getX(), this.getY() + 0.5, this.getZ(), 15, 0.4, 0.4, 0.4, 0.05);
                    }
                }
            } else if (this.getStage() == STAGE_JUVENILE) {
                this.ageTicks++;
                if (this.ageTicks >= 36000) { // 30 minutes natural time
                    this.setStage(STAGE_ADULT);
                    this.ageTicks = 0;
                    this.playSound(SoundEvents.ENDER_DRAGON_GROWL, 1.2F, 1.0F);
                    this.playSound(SoundEvents.PLAYER_LEVELUP, 1.5F, 1.0F);
                    if (this.level() instanceof ServerLevel sl) {
                        sl.sendParticles(ParticleTypes.FLAME, this.getX(), this.getY() + 1.0, this.getZ(), 30, 0.8, 0.8, 0.8, 0.1);
                        sl.sendParticles(ParticleTypes.LAVA, this.getX(), this.getY() + 1.0, this.getZ(), 10, 0.5, 0.5, 0.5, 0.0);
                    }
                }
            }
        }
    }

    // --- Life Stages & Growth ---
    public int getStage() {
        return this.entityData.get(DATA_STAGE);
    }

    public void setStage(int stage) {
        this.entityData.set(DATA_STAGE, stage);
        this.setBaby(stage < STAGE_ADULT);
        double scale = switch (stage) {
            case STAGE_HATCHLING -> 0.35D;
            case STAGE_JUVENILE -> 0.65D;
            default -> 1.0D;
        };
        var attr = this.getAttribute(Attributes.SCALE);
        if (attr != null) {
            attr.setBaseValue(scale);
        }
        this.refreshDimensions();
    }

    public int getGrowthProgress() {
        return this.entityData.get(DATA_GROWTH_PROGRESS);
    }

    public void setGrowthProgress(int progress) {
        this.entityData.set(DATA_GROWTH_PROGRESS, progress);
    }

    // --- State Getters & Setters ---
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
            this.roarTicks = 70;
        }
    }

    public boolean isEating() {
        return this.entityData.get(DATA_EATING);
    }

    public void setEating(boolean eating) {
        this.entityData.set(DATA_EATING, eating);
        if (eating) {
            this.eatingTicks = 40;
        }
    }

    public boolean isBiting() {
        return this.entityData.get(DATA_BITING);
    }

    public void setBiting(boolean biting) {
        this.entityData.set(DATA_BITING, biting);
        if (biting) {
            this.biteTicks = 15;
        }
    }

    public boolean isShootingFireball() {
        return this.entityData.get(DATA_SHOOTING_FIREBALL);
    }

    public void setShootingFireball(boolean shooting) {
        this.entityData.set(DATA_SHOOTING_FIREBALL, shooting);
        if (shooting) {
            this.fireballTicks = 20;
        }
    }

    public boolean isSaddled() {
        return this.entityData.get(DATA_SADDLED);
    }

    public void setSaddled(boolean saddled) {
        this.entityData.set(DATA_SADDLED, saddled);
    }

    public boolean isArmored() {
        return this.entityData.get(DATA_ARMORED);
    }

    public void setArmored(boolean armored) {
        this.entityData.set(DATA_ARMORED, armored);
    }

    // --- Interaction & Feeding ---
    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack itemstack = player.getItemInHand(hand);

        // Magma Food / Growth Feeding
        if (this.isMagmaFood(itemstack)) {
            if (!this.level().isClientSide()) {
                this.setEating(true);
                itemstack.consume(1, player);
                this.playSound(SoundEvents.GENERIC_EAT.value(), 1.0F, 0.8F);

                if (!this.isTame()) {
                    if (this.random.nextInt(3) == 0) {
                        this.tame(player);
                        this.level().broadcastEntityEvent(this, (byte) 7);
                    } else {
                        this.level().broadcastEntityEvent(this, (byte) 6);
                    }
                }

                if (this.getStage() == STAGE_HATCHLING) {
                    // Natural: 10 min (12,000 ticks). With feeding: minimum 5 min (6,000 ticks)
                    if (this.ageTicks < 6000) {
                        this.ageTicks = Math.min(this.ageTicks + 1200, 5999);
                    } else {
                        this.ageTicks = Math.min(this.ageTicks + 1200, 12000);
                        if (this.ageTicks >= 12000) {
                            this.setStage(STAGE_JUVENILE);
                            this.ageTicks = 0;
                            this.playSound(SoundEvents.PLAYER_LEVELUP, 1.4F, 1.1F);
                            if (this.level() instanceof ServerLevel sl) {
                                sl.sendParticles(ParticleTypes.HAPPY_VILLAGER, this.getX(), this.getY() + 0.5, this.getZ(), 20, 0.5, 0.5, 0.5, 0.1);
                                sl.sendParticles(ParticleTypes.FLAME, this.getX(), this.getY() + 0.5, this.getZ(), 15, 0.4, 0.4, 0.4, 0.05);
                            }
                            player.sendSystemMessage(Component.translatable("message.wingsofthewild.dragon_grew_juvenile"));
                        }
                    }
                    if (this.level() instanceof ServerLevel sl) {
                        sl.sendParticles(ParticleTypes.HEART, this.getX(), this.getY() + 0.4, this.getZ(), 5, 0.3, 0.3, 0.3, 0.05);
                    }
                } else if (this.getStage() == STAGE_JUVENILE) {
                    // Natural: 30 min (36,000 ticks). With feeding: minimum 15 min (18,000 ticks)
                    if (this.ageTicks < 18000) {
                        this.ageTicks = Math.min(this.ageTicks + 2400, 17999);
                    } else {
                        this.ageTicks = Math.min(this.ageTicks + 2400, 36000);
                        if (this.ageTicks >= 36000) {
                            this.setStage(STAGE_ADULT);
                            this.ageTicks = 0;
                            this.playSound(SoundEvents.ENDER_DRAGON_GROWL, 1.2F, 1.0F);
                            this.playSound(SoundEvents.PLAYER_LEVELUP, 1.5F, 1.0F);
                            if (this.level() instanceof ServerLevel sl) {
                                sl.sendParticles(ParticleTypes.FLAME, this.getX(), this.getY() + 1.0, this.getZ(), 30, 0.8, 0.8, 0.8, 0.1);
                                sl.sendParticles(ParticleTypes.LAVA, this.getX(), this.getY() + 1.0, this.getZ(), 10, 0.5, 0.5, 0.5, 0.0);
                            }
                            player.sendSystemMessage(Component.translatable("message.wingsofthewild.dragon_grew_adult"));
                        }
                    }
                    if (this.level() instanceof ServerLevel sl) {
                        sl.sendParticles(ParticleTypes.HEART, this.getX(), this.getY() + 0.7, this.getZ(), 7, 0.4, 0.4, 0.4, 0.05);
                    }
                } else {
                    if (this.getHealth() < this.getMaxHealth()) {
                        this.heal(20.0F);
                    }
                }
            }
            return InteractionResult.SUCCESS;
        }

        // Tamed Owner Interactions
        if (this.isTame() && this.isOwnedBy(player)) {
            // Equip saddle (Adult dragons only)
            if (this.getStage() == STAGE_ADULT && !this.isSaddled()
                    && (itemstack.is(ModItems.BASIC_DRAGON_SADDLE.get()) || itemstack.is(ModItems.REINFORCED_FLAME_SADDLE.get()))) {
                if (!this.level().isClientSide()) {
                    this.setSaddled(true);
                    itemstack.consume(1, player);
                    this.playSound(SoundEvents.HORSE_SADDLE.value(), 1.0F, 1.0F);
                }
                return InteractionResult.SUCCESS;
            }

            // Mount saddled adult dragon (not sneaking)
            if (this.getStage() == STAGE_ADULT && this.isSaddled() && !player.isSecondaryUseActive()) {
                if (!this.level().isClientSide()) {
                    player.startRiding(this);
                }
                return InteractionResult.SUCCESS;
            }

            // Sneak interaction: Roar
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

    public boolean isMagmaFood(ItemStack stack) {
        return stack.is(ModItems.SPICY_MAGMA_BERRIES.get())
                || stack.is(ModItems.CHARRED_MEAT.get())
                || stack.is(ModItems.FIRE_CRYSTAL_CANDY.get())
                || stack.is(ModItems.SMOKE_INFUSED_BROTH.get())
                || stack.is(ModItems.MOLTEN_BERRY_TART.get())
                || stack.is(ModItems.DRACONIC_TREAT.get())
                || stack.is(ModItems.VITALITY_ESSENCE.get());
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return isMagmaFood(stack);
    }

    // --- Riding & Flight System (Passo 1) ---
    @Nullable
    @Override
    public LivingEntity getControllingPassenger() {
        return this.getFirstPassenger() instanceof Player player && this.isSaddled() ? player : null;
    }

    @Override
    protected Vec3 getPassengerAttachmentPoint(Entity passenger, EntityDimensions dimensions, float scale) {
        return new Vec3(0.0D, 3.6D * scale, -0.1D * scale);
    }

    @Override
    public void onPlayerJump(int jumpScale) {
        if (this.isSaddled()) {
            if (this.onGround()) {
                // Take off from ground
                this.setFlying(true);
                this.setGliding(false);
                this.setDeltaMovement(this.getDeltaMovement().add(0.0D, 0.95D, 0.0D));
                this.playSound(SoundEvents.ENDER_DRAGON_FLAP, 1.4F, 0.85F);
            } else if (this.isFlying()) {
                // Altitude gain flap in flight
                this.setDeltaMovement(this.getDeltaMovement().add(0.0D, 0.45D, 0.0D));
                this.playSound(SoundEvents.ENDER_DRAGON_FLAP, 1.1F, 1.0F);
            }
        }
    }

    @Override
    public boolean canJump() {
        return this.isSaddled() && this.getStage() == STAGE_ADULT;
    }

    @Override
    public void handleStartJump(int jumpScale) {
        this.onPlayerJump(jumpScale);
    }

    @Override
    public void handleStopJump() {
    }

    @Override
    protected void tickRidden(Player passenger, Vec3 travelVector) {
        super.tickRidden(passenger, travelVector);

        // Orient dragon with rider's gaze
        this.setRot(passenger.getYRot(), passenger.getXRot() * 0.5F);
        this.yRotO = this.yBodyRot = this.yHeadRot = this.getYRot();
        this.xRotO = this.getXRot();

        if (this.isFlying()) {
            this.resetFallDistance();

            // Land when touching ground
            if (this.onGround() && this.getDeltaMovement().y <= 0) {
                this.setFlying(false);
                this.setGliding(false);
            }

            // Glide when aiming down (> 12 degrees pitch) and moving forward
            if (passenger.getXRot() > 12.0F && passenger.zza > 0) {
                this.setGliding(true);
                Vec3 look = passenger.getLookAngle();
                double glideBoost = 0.03D;
                this.setDeltaMovement(this.getDeltaMovement().add(look.x * glideBoost, look.y * 0.02D, look.z * glideBoost));
            } else {
                this.setGliding(false);
            }

            // Smooth descent if looking down or crouching/shift
            if (passenger.getXRot() > 25.0F) {
                this.setDeltaMovement(this.getDeltaMovement().add(0.0D, -0.04D, 0.0D));
            }
            if (passenger.isShiftKeyDown() || passenger.isCrouching()) {
                this.setDeltaMovement(this.getDeltaMovement().add(0.0D, -0.06D, 0.0D));
            }
        }
    }

    @Override
    protected Vec3 getRiddenInput(Player player, Vec3 travelVector) {
        // Read rider WASD input directly: xxa = Strafe (A/D), zza = Forward (W/S)
        float sideways = player.xxa * 0.5F;
        float forward = player.zza;
        if (forward <= 0.0F) {
            forward *= 0.25F; // Backing up is slow
        }
        return new Vec3(sideways, 0.0D, forward);
    }

    @Override
    protected float getRiddenSpeed(Player player) {
        float baseSpeed = (float) this.getAttributeValue(Attributes.MOVEMENT_SPEED);
        if (this.isFlying()) {
            return this.isGliding() ? 0.28F : 0.16F;
        }
        return baseSpeed * 0.85F;
    }

    @Override
    public void travel(Vec3 travelVector) {
        if (this.isAlive()) {
            if (this.isVehicle() && this.getControllingPassenger() instanceof Player player) {
                if (this.isFlying()) {
                    // Full 3D flight physics
                    this.moveRelative(this.getRiddenSpeed(player), travelVector);
                    this.move(MoverType.SELF, this.getDeltaMovement());
                    Vec3 motion = this.getDeltaMovement();
                    double drag = 0.91D;
                    double gravity = this.isGliding() ? -0.005D : -0.015D;
                    this.setDeltaMovement(motion.x * drag, (motion.y + gravity) * 0.98D, motion.z * drag);
                    return;
                }
            }
        }
        super.travel(travelVector);
    }

    // --- Mounted & Ground Combat Attacks (Passo 2) ---
    public void shootFireball(LivingEntity shooter) {
        if (this.fireballCooldown > 0) return;
        this.fireballCooldown = 20;
        this.setShootingFireball(true);

        if (!this.level().isClientSide() && this.level() instanceof ServerLevel serverLevel) {
            Vec3 look = shooter.getLookAngle();
            Vec3 spawnPos = this.position().add(0, this.getEyeHeight() * 0.85, 0).add(look.scale(2.2));

            LargeFireball fireball = new LargeFireball(EntityTypes.FIREBALL, serverLevel);
            fireball.setOwner(this);
            fireball.setPos(spawnPos.x, spawnPos.y, spawnPos.z);
            fireball.setDeltaMovement(look.normalize().scale(1.2D));
            serverLevel.addFreshEntity(fireball);

            serverLevel.playSound(null, this.blockPosition(), SoundEvents.GHAST_SHOOT, SoundSource.PLAYERS, 1.5F, 0.8F);
            serverLevel.playSound(null, this.blockPosition(), SoundEvents.ENDER_DRAGON_SHOOT, SoundSource.PLAYERS, 1.0F, 1.2F);
        }
    }

    public void performBiteAttack() {
        this.setBiting(true);

        if (!this.level().isClientSide() && this.level() instanceof ServerLevel serverLevel) {
            this.playSound(SoundEvents.RAVAGER_ATTACK, 1.2F, 0.9F);
            Vec3 front = this.position().add(this.getLookAngle().scale(2.5));
            AABB hitBox = new AABB(
                    front.x - 2.0, front.y - 1.5, front.z - 2.0,
                    front.x + 2.0, front.y + 2.5, front.z + 2.0
            );
            for (LivingEntity target : serverLevel.getEntitiesOfClass(LivingEntity.class, hitBox,
                    e -> e != this && !this.isAlliedTo(e) && e != this.getControllingPassenger())) {
                target.hurtServer(serverLevel, this.damageSources().mobAttack(this), 16.0F);
                target.setRemainingFireTicks(60);
            }
        }
    }

    // --- Persistence ---
    @Override
    public void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        output.putBoolean("Flying", this.isFlying());
        output.putBoolean("Saddled", this.isSaddled());
        output.putBoolean("Armored", this.isArmored());
        output.putInt("DragonStage", this.getStage());
        output.putInt("GrowthProgress", this.getGrowthProgress());
        output.putInt("AgeTicks", this.ageTicks);
    }

    @Override
    public void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        this.setFlying(input.getBooleanOr("Flying", false));
        this.setSaddled(input.getBooleanOr("Saddled", false));
        this.setArmored(input.getBooleanOr("Armored", false));
        this.setStage(input.getIntOr("DragonStage", STAGE_ADULT));
        this.setGrowthProgress(input.getIntOr("GrowthProgress", 0));
        this.ageTicks = input.getIntOr("AgeTicks", 0);
    }

    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob otherParent) {
        FlamefangEntity baby = ModEntities.FLAMEFANG.get().create(level, EntitySpawnReason.BREEDING);
        if (baby != null) {
            baby.setStage(STAGE_HATCHLING);
        }
        return baby;
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

        // 2. Action Controller: Eating, Roar, Bite, Fireball
        controllers.add(new AnimationController<FlamefangEntity>("actions", 4, state -> {
            if (this.isBiting()) {
                return state.setAndContinue(RawAnimation.begin().thenPlay("attack_bite"));
            }
            if (this.isShootingFireball()) {
                return state.setAndContinue(RawAnimation.begin().thenPlay("attack_fireball"));
            }
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
