package com.wingsofthewild.client.gui;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class DragonHornScreen extends Screen {
    private static final int PANEL_WIDTH = 200;
    private static final int PANEL_HEIGHT = 160;

    private String lastCommandIssued = "Nenhum comando emitido.";

    public DragonHornScreen() {
        super(Component.translatable("item.wingsofthewild.dragon_horn"));
    }

    @Override
    protected void init() {
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        // Botão 1: Chamar Todos (Follow)
        this.addRenderableWidget(Button.builder(Component.literal("§6📯 Chamar Todos (Seguir)"), button -> {
            issueHornCommand("Seguir Jogador");
        }).pos(left + 15, top + 35).width(170).build());

        // Botão 2: Ficar / Sentar (Stay)
        this.addRenderableWidget(Button.builder(Component.literal("§e🛡 Modo Guarda (Ficar)"), button -> {
            issueHornCommand("Permanecer no Local");
        }).pos(left + 15, top + 62).width(170).build());

        // Botão 3: Dispersar / Pousar (Wander)
        this.addRenderableWidget(Button.builder(Component.literal("§a🪶 Pousar e Descansar"), button -> {
            issueHornCommand("Pouso Ordenado");
        }).pos(left + 15, top + 89).width(170).build());

        // Botão Fechar
        this.addRenderableWidget(Button.builder(CommonComponents.GUI_DONE, button -> this.onClose())
                .pos(left + 35, top + 125)
                .width(130)
                .build());
    }

    private void issueHornCommand(String cmd) {
        this.lastCommandIssued = "§2Ordem: " + cmd + "!";
        if (this.minecraft != null && this.minecraft.player != null) {
            // Toca som de berrante / chifre para feedback auditivo imediato
            this.minecraft.player.level().playSound(
                    this.minecraft.player,
                    this.minecraft.player.blockPosition(),
                    SoundEvents.GOAT_HORN_SOUND_VARIANTS.get(0).value(),
                    SoundSource.PLAYERS,
                    1.5F,
                    0.85F
            );
            this.minecraft.player.sendSystemMessage(
                    Component.literal("§6[Berrante Dracônico] §fComando emitido aos dragões: §e" + cmd)
            );
        }
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        // Moldura em tom de bronze vulcânico / ardósia
        graphics.fill(left - 2, top - 2, left + PANEL_WIDTH + 2, top + PANEL_HEIGHT + 2, 0xFF4A2511);
        graphics.fill(left, top, left + PANEL_WIDTH, top + PANEL_HEIGHT, 0xE01C1A24);

        // Barra decorativa do topo
        graphics.fill(left, top, left + PANEL_WIDTH, top + 24, 0xFF632B12);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        int left = (this.width - PANEL_WIDTH) / 2;
        int top = (this.height - PANEL_HEIGHT) / 2;

        // Título centralizado
        graphics.centeredText(this.font, Component.literal("§6§lBerrante Dracônico"), this.width / 2, top + 8, 0xFFFFFF);

        // Feedback de comando no rodapé do painel
        graphics.centeredText(this.font, Component.literal(this.lastCommandIssued), this.width / 2, top + 114, 0xCCCCCC);
    }

    @Override
    public boolean isInGameUi() {
        return false;
    }
}
