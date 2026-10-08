package com.wingsofthewild.event;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.EntityMountEvent;

@EventBusSubscriber(modid = WingsOfTheWild.MODID)
public class ModCommonEvents {

    @SubscribeEvent
    public static void onEntityMount(EntityMountEvent event) {
        if (event.isDismounting() && event.getEntityBeingMounted() instanceof FlamefangEntity dragon) {
            // Prevent accidental mid-air dismount when pressing shift during flight
            if (dragon.isFlying() && !dragon.onGround()) {
                event.setCanceled(true);
                // Trigger smooth descent towards the ground
                dragon.setDeltaMovement(dragon.getDeltaMovement().add(0.0D, -0.08D, 0.0D));
            } else if (event.getEntityMounting() instanceof LivingEntity rider) {
                // Safety slow falling if dismounted high up
                if (!dragon.onGround()) {
                    rider.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING, 200, 0));
                }
            }
        }
    }
}
