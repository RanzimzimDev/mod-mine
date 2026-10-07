package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModEntities {
    public static final DeferredRegister.Entities ENTITIES = DeferredRegister.createEntities(WingsOfTheWild.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<FlamefangEntity>> FLAMEFANG = ENTITIES.registerEntityType(
            "flamefang",
            FlamefangEntity::new,
            MobCategory.CREATURE,
            builder -> builder.sized(3.5F, 5.0F).fireImmune()
    );
}
