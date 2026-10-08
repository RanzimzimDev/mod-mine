package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.block.entity.DragonNestBlockEntity;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlockEntities {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, WingsOfTheWild.MODID);

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<DragonNestBlockEntity>> DRAGON_NEST =
            BLOCK_ENTITIES.register("dragon_nest",
                    () -> new BlockEntityType<>(DragonNestBlockEntity::new, ModBlocks.DRAGON_NEST.get())
            );

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<com.wingsofthewild.block.entity.DraconicFoundryBlockEntity>> DRACONIC_FOUNDRY =
            BLOCK_ENTITIES.register("draconic_foundry",
                    () -> new BlockEntityType<>(com.wingsofthewild.block.entity.DraconicFoundryBlockEntity::new, ModBlocks.DRACONIC_FOUNDRY.get())
            );

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<com.wingsofthewild.block.entity.DraconicHearthBlockEntity>> DRACONIC_HEARTH =
            BLOCK_ENTITIES.register("draconic_hearth",
                    () -> new BlockEntityType<>(com.wingsofthewild.block.entity.DraconicHearthBlockEntity::new, ModBlocks.DRACONIC_HEARTH.get())
            );
}
