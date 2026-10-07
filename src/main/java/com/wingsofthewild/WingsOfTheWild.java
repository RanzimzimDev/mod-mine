package com.wingsofthewild;

import com.mojang.logging.LogUtils;
import com.wingsofthewild.client.gui.ModClientScreens;
import com.wingsofthewild.client.renderer.FlamefangRenderer;
import com.wingsofthewild.entity.FlamefangEntity;
import com.wingsofthewild.init.ModBlocks;
import com.wingsofthewild.init.ModCreativeTabs;
import com.wingsofthewild.init.ModEntities;
import com.wingsofthewild.init.ModItems;
import com.wingsofthewild.init.ModMenuTypes;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import org.slf4j.Logger;

@Mod(WingsOfTheWild.MODID)
public class WingsOfTheWild {
    public static final String MODID = "wingsofthewild";
    public static final Logger LOGGER = LogUtils.getLogger();

    public WingsOfTheWild(IEventBus modEventBus, ModContainer modContainer) {
        LOGGER.info("Iniciando Wings of the Wild - Versao 26.3");

        // Registrando Blocos, Itens, Entidades, Menus e Abas Criativas no Barramento de Eventos
        ModBlocks.BLOCKS.register(modEventBus);
        com.wingsofthewild.init.ModBlockEntities.BLOCK_ENTITIES.register(modEventBus);
        ModItems.ITEMS.register(modEventBus);
        ModEntities.ENTITIES.register(modEventBus);
        ModMenuTypes.MENUS.register(modEventBus);
        ModCreativeTabs.CREATIVE_MODE_TABS.register(modEventBus);

        // Registro de Atributos de Entidades
        modEventBus.addListener(this::registerAttributes);
        modEventBus.addListener(this::registerPayloads);

        // Registro de Telas de GUI e Renderizadores de Entidade no Cliente
        if (FMLEnvironment.getDist() == Dist.CLIENT) {
            modEventBus.addListener(ModClientScreens::registerScreens);
            modEventBus.addListener(this::registerRenderers);
            modEventBus.addListener(com.wingsofthewild.client.ModClientEvents::registerKeyMappings);
        }

        modEventBus.addListener(this::commonSetup);
    }

    private void registerPayloads(final net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent event) {
        net.neoforged.neoforge.network.registration.PayloadRegistrar registrar = event.registrar("1");
        registrar.playToServer(
                com.wingsofthewild.network.DragonAttackPayload.TYPE,
                com.wingsofthewild.network.DragonAttackPayload.STREAM_CODEC,
                com.wingsofthewild.network.DragonAttackPayload::handle
        );
    }

    private void registerAttributes(final EntityAttributeCreationEvent event) {
        LOGGER.info("Wings of the Wild: Registrando atributos para FlamefangEntity...");
        event.put(ModEntities.FLAMEFANG.get(), FlamefangEntity.createAttributes().build());
    }

    private void registerRenderers(final EntityRenderersEvent.RegisterRenderers event) {
        LOGGER.info("Wings of the Wild: Registrando renderizador GeckoLib para Flamefang...");
        event.registerEntityRenderer(ModEntities.FLAMEFANG.get(), FlamefangRenderer::new);
    }

    private void commonSetup(final FMLCommonSetupEvent event) {
        LOGGER.info("Wings of the Wild: Setup comum inicializado com sucesso!");
    }
}
