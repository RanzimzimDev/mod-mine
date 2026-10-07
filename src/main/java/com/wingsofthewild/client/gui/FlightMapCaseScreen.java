package com.wingsofthewild.client.gui;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class FlightMapCaseScreen extends Screen {
    private static final int PANEL_WIDTH = 220;
    private static final int PANEL_HEIGHT = 170;

    private int altitudeTarget = 120;
    private boolean nightVisionCompass = true;

    public FlightMapCaseScreen() {
        super(Component.translatable("item.wingsofthewild.flight_map_case"));
    }

    @Override
    protected void init() {
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        // Botão para ajustar altitude de cruzeiro
        this.addRenderableWidget(Button.builder(Component.literal("§bSubir Altitude (+20m)"), button -> {
            this.altitudeTarget = Math.min(320, this.altitudeTarget + 20);
        }).pos(left + 15, top + 75).width(90).build());

        this.addRenderableWidget(Button.builder(Component.literal("§3Descer Altitude (-20m)"), button -> {
            this.altitudeTarget = Math.max(60, this.altitudeTarget - 20);
        }).pos(left + 115, top + 75).width(90).build());

        // Botão de Bússola Aérea
        this.addRenderableWidget(Button.builder(Component.literal("§6Bússola de Voo: " + (nightVisionCompass ? "§aLigada" : "§cDesligada")), button -> {
            this.nightVisionCompass = !this.nightVisionCompass;
            button.setMessage(Component.literal("§6Bússola de Voo: " + (this.nightVisionCompass ? "§aLigada" : "§cDesligada")));
        }).pos(left + 15, top + 105).width(190).build());

        // Fechar
        this.addRenderableWidget(Button.builder(CommonComponents.GUI_DONE, button -> this.onClose())
                .pos(left + 45, top + 135)
                .width(130)
                .build());
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        // Borda e fundo estilo estojo de couro náutico/aviador
        graphics.fill(left - 2, top - 2, left + PANEL_WIDTH + 2, top + PANEL_HEIGHT + 2, 0xFF2C3E50);
        graphics.fill(left, top, left + PANEL_WIDTH, top + PANEL_HEIGHT, 0xF01A252F);

        // Cabeçalho azul aeronáutico
        graphics.fill(left, top, left + PANEL_WIDTH, top + 24, 0xFF2980B9);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        graphics.centeredText(this.font, Component.literal("§f§lEstojo de Navegação Aérea"), this.width / 2, top + 8, 0xFFFFFF);

        // Coordenadas atuais do jogador
        String posStr = "§7Localização: §fX: ?, Y: ?, Z: ?";
        if (this.minecraft != null && this.minecraft.player != null) {
            BlockPos pos = this.minecraft.player.blockPosition();
            posStr = "§7Coord: §eX: " + pos.getX() + "  §bY: " + pos.getY() + "  §eZ: " + pos.getZ();
        }
        graphics.text(this.font, posStr, left + 15, top + 34, 0xFFFFFF, false);

        // Altitude de cruzeiro recomendada
        graphics.text(this.font, "§7Teto de Voo Desejado: §a" + this.altitudeTarget + " blocos", left + 15, top + 52, 0xFFFFFF, false);
    }

    @Override
    public boolean isInGameUi() {
        return false;
    }
}
