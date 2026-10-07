package com.wingsofthewild.item;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

public class EmberSwordItem extends Item {
    public EmberSwordItem(Properties properties) {
        super(properties);
    }

    @Override
    public void postHurtEnemy(ItemStack itemStack, LivingEntity mob, LivingEntity attacker) {
        mob.igniteForSeconds(4.0F);
        super.postHurtEnemy(itemStack, mob, attacker);
    }
}
