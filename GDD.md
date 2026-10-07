# 🐉 Wings of the Wild — Documento de Design de Jogo (GDD)

**Versão do Minecraft:** 26.3 (Wilderness Bound)  
**Mod Loader:** NeoForge  
**Mod ID:** `wingsofthewild`  
**Nome Oficial:** Wings of the Wild  
**Diretório do Projeto:** `D:\Mine/` (com junção transparente na Área de Trabalho)

---

## 📖 Visão Geral do Projeto
O **Wings of the Wild** é um mod focado em criaturas dracônicas que combinam a estética majestosa e física de voo de dragões (inspirado em *Isle of Berk*) com a identidade de **Pokémon**, adaptados para um estilo **rústico, selvagem e imersivo** no Minecraft.

---

## 🧭 Pilares de Design

### 🥚 Pilar 1: O Ciclo do Flamefang (Ninhos, Quests e Adoção)

#### 1. Descoberta & Ninho Selvagem no Mundo
* **Origem do Ovo:** O jogador deve escalar **picos de montanhas altas ou platôs vulcânicos**.
* **O Guardião:** O ninho selvagem é protegido ferozmente por um **Flamefang adulto territorial**. O jogador precisa enfrentá-lo ou usar furtividade/distrações para resgatar o ovo.

#### 2. Incubação & Defesa Noturna
* **Ninho Térmico Artesanal:** Bloco criado pelo jogador para depositar o ovo em segurança.
* **Estágios Visuais de Eclosão:**
  * *Estágio 1 (Frio/Dormindo):* Casca escura e opaca.
  * *Estágio 2 (Aquecendo):* Surgem veios incandescentes e partículas sutis de fumaça.
  * *Estágio 3 (Rachando):* Fissuras visíveis na casca, faíscas brilhantes e sons de batidas de dentro do ovo.
* **A Quest de Defesa:** O calor mágico do ovo atrai monstros hostis da floresta à noite (zumbis, esqueletos, aranhas). O jogador precisa defender o ninho até a eclosão.

#### 3. Crescimento & Personalidade
* **Sistema Híbrido de Crescimento:** O Flamefang possui um tempo natural de desenvolvimento, mas **alimentá-lo ativamente com rações especiais da Fornalha Dracônica reduz significativamente o tempo de crescimento**.
* **Traços de Personalidade Únicos:** Cada dragão possui particularidades:
  * O filhote de Flamefang tem medo natural de água e chuva (procura abrigo).
  * Adora dormir enroladinho perto de fogueiras e fontes de calor.
  * Reações de humor (brincalhão, dócil, protetor ou arisco).

---

### 🔥 Pilar 2: Primeira Espécie — Flamefang (Presa Flamejante)

* **Inspiração:** Silhueta imponente do *Charizard*, reinterpretada com estética selvagem e rústica.
* **Características Visuais:**
  * **Textura & Cores:** Escamas em tons de carvão/obsidiana com vermelho-carmim rústico, ventre acinzentado endurecido e membranas de asa cor de brasa desgastada.
  * **Cabeça & Chifres:** Dois chifres dracônicos curvados, dentes protuberantes e olhos amarelados predatórios.
  * **Cauda Flamejante:** Chama viva na ponta da cauda com partículas de brasas e iluminação dinâmica.
  * *(Backlog futuro: Variante Shiny rara nos arquivos de textura).*
* **Combate & Sopro de Fogo:**
  * **Barra de Fôlego/Energia:** Quando montado, o jogador ativa o sopro contínuo de chamas.
  * O fôlego dura alguns segundos de fogo devastador, após o qual o Flamefang se cansa e precisa de um tempo de recarga (cooldown) para recuperar o ar.

---

### 🦅 Pilar 3: Estações de Trabalho com GUI Própria & Voo Físico

#### 1. Fornalha Culinária Dracônica (`draconic_hearth`)
* **Interface Gráfica (GUI) Própria:** Tela temática com slots para caldeirão de ingredientes e combustível térmico.
* Usada exclusivamente para criar as refeições personalizadas de doma e crescimento dracônico.

#### 2. Bancada de Selaria Dracônica (`tack_workbench`)
* **Interface Gráfica (GUI) Própria:** Mesa de alfaiataria e ferraria para arreios e selas.
* **Economia Fechada (100% Itens do Mod):** As receitas desta bancada exigem **exclusivamente itens do próprio mod**:
  * Escamas trocadas pelo dragão durante o crescimento.
  * Couro Dracônico tratado.
  * Fivelas e tiras forjadas a partir de materiais dracônicos.
* **Equipamentos Fabricáveis:**
  * Sela do Flamefang (habilita montaria e controle de voo).
  * Alforjes Dracônicos (adicionam inventário para viagens).
  * Armaduras de proteção.

#### 3. Sistema de Voo Físico (Estilo Isle of Berk)
* `Espaço`: Batida de asas com impulso vertical (consome estamina).
* `W / Olhar para baixo`: Mergulho em alta velocidade com efeito de túnel de vento cortante.
* `Olhar para cima`: Converte a velocidade do mergulho em altitude de subida.
* `HUD`: Barra de estamina de voo + barra de fôlego do sopro de fogo.

---

## 🏗️ Estrutura de Itens & Blocos do Projeto

O mod possui um catálogo detalhado de **80 itens e blocos da Versão 1.0** (com meta de expansão de até **~200 itens**) com rastreamento de progresso individual em:  
👉 **[D:\Mine\ITENS.md](file:///D:/Mine/ITENS.md)**

Todas as ideias novas surgidas durante a produção da v1.0 são arquivadas no:  
👉 **[D:\Mine\IDEIAS.md](file:///D:/Mine/IDEIAS.md)** (para entrarem a partir da v1.1)

```text
wingsofthewild/
├── Blocos (Com GUIs customizadas)
│   ├── dragon_nest              # Ninho artesanal para incubação
│   ├── draconic_hearth          # Fornalha culinária com GUI temática
│   └── tack_workbench           # Bancada de selaria com GUI temática
├── Itens (Ingredientes & Equipamentos do Mod)
│   ├── flamefang_egg            # Ovo com estados de rachadura
│   ├── flamefang_scale          # Escama caída (usada na selaria)
│   ├── draconic_leather         # Couro tratado do mod
│   ├── dragon_saddle            # Sela do mod
│   ├── draconic_treat           # Petisco acelerador de crescimento
│   └── ash_stew                 # Ensopado nutritivo
└── Entidade
    └── flamefang                # Entidade completa (Hatchling, Juvenil e Adulto)
```

---

## 📝 Diário de Bordo & Decisões
- **[2026-10-06]**: Nome da primeira criatura: **Flamefang**.
- **[2026-10-06]**: Crescimento híbrido: tempo natural acelerado por rações da Fornalha.
- **[2026-10-06]**: Personalidade para cada dragão (filhote com medo de água e amor por calor).
- **[2026-10-06]**: Sopro de fogo com barra de fôlego e tempo de descanso.
- **[2026-10-06]**: Todas as estações de trabalho terão interfaces gráficas (GUIs) exclusivas.
- **[2026-10-06]**: Bancada de Selaria usará 100% itens exclusivos do mod (escamas, couros dracônicos).
- **[2026-10-06]**: Ninho selvagem no topo de montanhas protegido por um Flamefang adulto.
