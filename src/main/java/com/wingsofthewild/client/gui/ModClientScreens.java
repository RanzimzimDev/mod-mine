package com.wingsofthewild.client.gui;

import com.wingsofthewild.init.ModMenuTypes;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

public class ModClientScreens {
    public static void registerScreens(RegisterMenuScreensEvent event) {
        event.register(ModMenuTypes.DRACONIC_FOUNDRY.get(), DraconicFoundryScreen::new);
        event.register(ModMenuTypes.DRACONIC_HEARTH.get(), DraconicHearthScreen::new);
        event.register(ModMenuTypes.TACK_WORKBENCH.get(), TackWorkbenchScreen::new);
        event.register(ModMenuTypes.DRAGON_POUCH.get(), DragonPouchScreen::new);
    }
}
