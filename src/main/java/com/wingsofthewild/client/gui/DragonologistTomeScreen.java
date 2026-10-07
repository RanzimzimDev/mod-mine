package com.wingsofthewild.client.gui;

import net.minecraft.ChatFormatting;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.PageButton;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.api.distmarker.OnlyIn;

import java.util.ArrayList;
import java.util.List;

@OnlyIn(Dist.CLIENT)
public class DragonologistTomeScreen extends Screen {
    private static final Identifier BOOK_TEXTURE = Identifier.withDefaultNamespace("textures/gui/book.png");
    private static final int IMAGE_WIDTH = 192;
    private static final int IMAGE_HEIGHT = 192;

    private int currentPage = 0;
    private final List<BookPage> pages = new ArrayList<>();
    private PageButton forwardButton;
    private PageButton backButton;

    public record BookPage(String title, String chapter, String[] lines) {}

    public DragonologistTomeScreen() {
        super(Component.translatable("item.wingsofthewild.dragonologist_tome"));
        setupPages();
    }

    private void setupPages() {
        pages.add(new BookPage(
                "Tomo dos Dragões",
                "§4§lCapítulo I: Origens",
                new String[]{
                        "§8Bem-vindo, pesquisador.",
                        "",
                        "As terras primitivas",
                        "abrigam feras antigas",
                        "forjadas no próprio",
                        "fogo do centro da terra.",
                        "",
                        "Este compêndio reúne",
                        "o conhecimento sobre",
                        "a espécie Flamefang."
                }
        ));

        pages.add(new BookPage(
                "Flamefang Adulto",
                "§c§lFisiologia & Voo",
                new String[]{
                        "§0O §4Flamefang Adulto§0",
                        "possui escamas de basalto",
                        "e magma fervente.",
                        "",
                        "§0- §6Envergadura:§0 7 blocos",
                        "§0- §6Respiração:§0 Chamas",
                        "§0- §6Dieta:§0 Carnes assadas",
                        "  e bagas magmáticas.",
                        "",
                        "Para montá-lo, use uma",
                        "§4Sela Dracônica§0 artesanal."
                }
        ));

        pages.add(new BookPage(
                "Ninho & Incubação",
                "§6§lCiclo de Vida",
                new String[]{
                        "§0Os ovos necessitam de",
                        "calor extremo contínuo.",
                        "",
                        "§01. Construa um §6Ninho§0",
                        "   com palha chamuscada.",
                        "§02. Aqueça a base com",
                        "   um §4Braseiro Térmico§0.",
                        "§03. Aguarde as fendas",
                        "   indicando eclosão!"
                }
        ));

        pages.add(new BookPage(
                "Metalurgia & Forja",
                "§5§lLigas Dracônicas",
                new String[]{
                        "§0Na §5Forja de Ligas§0,",
                        "combine minérios raros:",
                        "",
                        "§0- §6Liga de Brasas:§0",
                        "  Minério Bruta + Basalto.",
                        "§0- §bLiga Escaldante:§0",
                        "  Brasa + Gelo Eterno.",
                        "§0- §dLiga de Plasma:§0",
                        "  Solarium + Fulgurite."
                }
        ));

        pages.add(new BookPage(
                "Comandos & Berrante",
                "§2§lAdestramento",
                new String[]{
                        "§0Utilize o §2Berrante§0",
                        "para controlar seus dragões:",
                        "",
                        "§0- §2Seguir / Ficar:§0",
                        "  Aperte no berrante.",
                        "§0- §cModo Guarda:§0",
                        "  Protege sua base.",
                        "§0- §bEstojo de Mapas:§0",
                        "  Navegação de voo."
                }
        ));
    }

    @Override
    protected void init() {
        int x = (this.width - IMAGE_WIDTH) / 2;
        int y = (this.height - IMAGE_HEIGHT) / 2;

        this.addRenderableWidget(Button.builder(CommonComponents.GUI_DONE, button -> this.onClose())
                .pos(this.width / 2 - 100, y + IMAGE_HEIGHT + 4)
                .width(200)
                .build());

        this.forwardButton = this.addRenderableWidget(new PageButton(x + 116, y + 159, true, button -> {
            if (this.currentPage < this.pages.size() - 1) {
                this.currentPage++;
                this.updateButtonVisibility();
            }
        }, true));

        this.backButton = this.addRenderableWidget(new PageButton(x + 43, y + 159, false, button -> {
            if (this.currentPage > 0) {
                this.currentPage--;
                this.updateButtonVisibility();
            }
        }, true));

        this.updateButtonVisibility();
    }

    private void updateButtonVisibility() {
        this.forwardButton.visible = this.currentPage < this.pages.size() - 1;
        this.backButton.visible = this.currentPage > 0;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractBackground(graphics, mouseX, mouseY, partialTick);
        int x = (this.width - IMAGE_WIDTH) / 2;
        int y = (this.height - IMAGE_HEIGHT) / 2;
        graphics.blit(RenderPipelines.GUI_TEXTURED, BOOK_TEXTURE, x, y, 0.0F, 0.0F, IMAGE_WIDTH, IMAGE_HEIGHT, 256, 256);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);

        int x = (this.width - IMAGE_WIDTH) / 2;
        int y = (this.height - IMAGE_HEIGHT) / 2;

        if (this.currentPage >= 0 && this.currentPage < this.pages.size()) {
            BookPage page = this.pages.get(this.currentPage);

            // Indicador de página (ex: "1 de 5")
            String pageIndicator = (this.currentPage + 1) + " / " + this.pages.size();
            graphics.text(this.font, pageIndicator, x + 138 - this.font.width(pageIndicator), y + 16, 0x888888, false);

            // Título do capítulo
            graphics.text(this.font, page.chapter, x + 36, y + 30, 0x000000, false);

            // Linhas de texto
            int lineY = y + 46;
            for (String line : page.lines) {
                graphics.text(this.font, line, x + 36, lineY, 0x333333, false);
                lineY += 10;
            }
        }
    }

    @Override
    public boolean isInGameUi() {
        return false;
    }
}
