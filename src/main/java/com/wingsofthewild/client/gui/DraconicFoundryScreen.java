package com.wingsofthewild.client.gui;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.world.inventory.DraconicFoundryMenu;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class DraconicFoundryScreen extends AbstractContainerScreen<DraconicFoundryMenu> {
    private static final Identifier TEXTURE = Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "textures/gui/container/draconic_foundry.png");

    public DraconicFoundryScreen(DraconicFoundryMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
    }

    @Override
    protected void init() {
        super.init();
        this.titleLabelX = (this.imageWidth - this.font.width(this.title)) / 2;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float a) {
        super.extractBackground(graphics, mouseX, mouseY, a);
        int xo = this.leftPos;
        int yo = this.topPos;
        graphics.blit(RenderPipelines.GUI_TEXTURED, TEXTURE, xo, yo, 0.0F, 0.0F, this.imageWidth, this.imageHeight, 256, 256);

        // Se estiver acesa, renderiza a chama de fusão
        if (this.menu.isLit()) {
            int litProgress = this.menu.getLitProgress();
            graphics.blit(RenderPipelines.GUI_TEXTURED, TEXTURE, xo + 56, yo + 36 + 12 - litProgress, 176.0F, 12.0F - litProgress, 14, litProgress + 1, 256, 256);
        }

        // Renderiza a seta de progresso da liga metálica
        int burnProgress = this.menu.getBurnProgress();
        graphics.blit(RenderPipelines.GUI_TEXTURED, TEXTURE, xo + 92, yo + 35, 176.0F, 14.0F, burnProgress + 1, 16, 256, 256);
    }
}
