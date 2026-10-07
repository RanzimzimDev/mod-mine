package com.wingsofthewild.init;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.world.inventory.DraconicFoundryMenu;
import com.wingsofthewild.world.inventory.DraconicHearthMenu;
import com.wingsofthewild.world.inventory.TackWorkbenchMenu;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.common.extensions.IMenuTypeExtension;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModMenuTypes {
    public static final DeferredRegister<MenuType<?>> MENUS = DeferredRegister.create(BuiltInRegistries.MENU, WingsOfTheWild.MODID);

    public static final DeferredHolder<MenuType<?>, MenuType<DraconicFoundryMenu>> DRACONIC_FOUNDRY = MENUS.register(
            "draconic_foundry",
            () -> IMenuTypeExtension.create((windowId, inv, data) -> new DraconicFoundryMenu(windowId, inv))
    );

    public static final DeferredHolder<MenuType<?>, MenuType<DraconicHearthMenu>> DRACONIC_HEARTH = MENUS.register(
            "draconic_hearth",
            () -> IMenuTypeExtension.create((windowId, inv, data) -> new DraconicHearthMenu(windowId, inv))
    );

    public static final DeferredHolder<MenuType<?>, MenuType<TackWorkbenchMenu>> TACK_WORKBENCH = MENUS.register(
            "tack_workbench",
            () -> IMenuTypeExtension.create((windowId, inv, data) -> new TackWorkbenchMenu(windowId, inv))
    );
}
