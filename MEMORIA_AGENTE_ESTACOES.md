# 🏛️ Memória de Trabalho — Agente 5: Arquiteto 3D de Blocos & Estações de Trabalho (Workstations)

**Identificador do Agente:** `workstation_3d_architect`  
**Escopo Exclusivo:**
* Modelagem geométrica 3D e texturização de blocos interativos e Estações de Trabalho (Workstations) do mod **Wings of the Wild** (Minecraft 26.3 NeoForge).
* Criação de arquivos nativos Blockbench (`.bbmodel`) em `D:\Mine\models\blocks\`.
* Geração de modelos JSON para Minecraft em `src/main/resources/assets/wingsofthewild/models/block/` com elementos geométricos 3D completos, mapeamento UV exato e transformações de exibição (`display`).
* Compatibilidade e sincronização perfeita com `blockstates/` e `models/item/`.

⛔ **REGRA DE NÃO-SOBREPOSIÇÃO (ESTRITA):**
* NUNCA alterar entidades vivas/dragões GeckoLib (pertence ao Agente 2).
* NUNCA sobrescrever lógicas de gameplay em Java sem necessidade de registro de blocos (pertence ao Agente 1).
* NUNCA desenhar ou sobrescrever ícones de itens 2D (pertence ao Agente 3).

📌 **DIRETRIZ PERMANENTE DE REGISTRO E PAINEL (APPEND-ONLY):**
* Este arquivo é de manutenção contínua e estritamente **APPEND-ONLY**, preservando o histórico de todas as iterações e modelos criados.
* O painel `D:\Mine\painel.html` deve ser atualizado para refletir o status de modelagem 3D das estações de trabalho e os arquivos entregues.

---

## 🏛️ HISTÓRICO PERMANENTE DE MODELAGEM 3D (REGISTRO CUMULATIVO)

### ✅ Rodada 1 — Modelagem 3D das 7 Estações de Trabalho Oficiais (Concluída em 2026-10-07)

Todas as 7 estações de trabalho do mod foram integralmente projetadas, modeladas em 3D cúbico detalhado e validadas:

#### 1. `dragon_nest` (Ninho Dracônico Artesanal)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\dragon_nest.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/dragon_nest.json`
* **Quantidade de Elementos 3D:** 28 cubos geométricos.
* **Dimensões & Geometria:**
  - Diâmetro externo imponente de 26x26 unidades (X: -5 a 21, Z: -5 a 21), ultrapassando a grade rígida de 16x16 para uma silhueta orgânica e imersiva.
  - Cavidade côncava central rebaixada em `Y = 0.5 a 1.5`, acolchoada com anel de transição suave em palha chamuscada (`charred_nest_straw`), moldada sob medida para acolher o `flamefang_egg` (8x8x10) de forma estável.
  - 8 blocos de pedras basálticas de ancoragem (`draconic_stone`) nos cantos diagonais e eixos cardeais, ancorando o ninho ao solo e transmitindo peso geotérmico.
  - Borda elevada em cesto octogonal (`Y = 2 a 5.5`) com galhos grossos e nós diagonais entrelaçados rotacionados a 45°, encimados por ramos e gravetos rústicos salientes (`Y = 5 a 7`).
* **Texturas Mapeadas:** `dragon_nest.png`, `charred_nest_straw.png`, `draconic_stone.png` (Partícula: `dragon_nest`).

#### 2. `draconic_foundry` (Forja de Ligas Dracônica)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\draconic_foundry.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/draconic_foundry.json`
* **Quantidade de Elementos 3D:** 24 cubos geométricos.
* **Dimensões & Geometria:**
  - Plinto inferior reforçado de tijolos vulcânicos (`[0, 0, 0]` a `[16, 3, 16]`) com gola chanfrada intermediária (`[0.5, 3, 0.5]` a `[15.5, 4, 15.5]`).
  - Câmara de combustão frontal em arco com pilares laterais chanfrados, abertura recuada com leito de brasas incandescentes e grelha de retenção de carvão.
  - Calha lateral saliente de vazamento de metal líquido no flanco leste (`X = 14 a 18.5`), com paredes de retenção, canal de liga metálica fundida e bico de vertimento em gota.
  - Cadinho refratário monumental no topo (`Y = 12 a 16`), com paredes octogonais espessas, bacia oca, banho de liga líquida incandescente e 4 grampos/abraçadeiras vulcânicas de retenção nos vértices.
* **Texturas Mapeadas:** `draconic_foundry_front.png`, `draconic_foundry_side.png`, `draconic_foundry_top.png`, `draconic_foundry_bottom.png` (Partícula: `draconic_foundry_front`).

#### 3. `draconic_hearth` (Fornalha Culinária Dracônica)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\draconic_hearth.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/draconic_hearth.json`
* **Quantidade de Elementos 3D:** 20 cubos geométricos.
* **Dimensões & Geometria:**
  - Base pesada de cantaria rústica com compartimento inferior dedicado para gaveta de cinzas e puxador metálico em relevo.
  - Pilares de sustentação e câmara aberta frontal abrigando braseiro de cozimento ardente.
  - Grelha superior de barras de ferro cruzadas e caldeirão de cocção volumétrico suspenso por gancho de sustentação.
  - Chaminé rústica de pedra nos fundos ascendendo até `Y = 16.5`, equipada com fuste de exaustão, 3 respiradouros laterais e frontais para saída de vapores e coroa com cimalha chanfrada de proteção.
* **Texturas Mapeadas:** `draconic_hearth_front.png`, `draconic_hearth_side.png`, `draconic_hearth_top.png`, `draconic_hearth_bottom.png` (Partícula: `draconic_hearth_front`).

#### 4. `tack_workbench` (Bancada de Selaria Dracônica)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\tack_workbench.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/tack_workbench.json`
* **Quantidade de Elementos 3D:** 22 cubos geométricos.
* **Dimensões & Geometria:**
  - 4 pernas estruturais chanfradas de carvalho escuro com travessas horizontais de reforço e prateleira inferior de armazenamento para couros e ferramentas.
  - Tampo maciço em madeira nobre sobreposto por esteira de trabalho em couro cru esticado com costuras perimetrais e régua traseira de retenção de ferramentas.
  - Gaveta central de marcenaria fina com puxador torneado em osso dracônico.
  - Barra frontal de suporte com ferramentas artesanais de entalhe em osso penduradas (sovela/estilete e agulha de perfuração de arreios).
  - Suporte duplo lateral com eixo cilíndrico abrigando um rolo espesso de tendão dracônico (`draconic_sinew`) pronto para costura de bardas e selas.
* **Texturas Mapeadas:** `tack_workbench_top.png`, `tack_workbench_front.png`, `tack_workbench_side.png`, `tack_workbench_bottom.png` (Partícula: `tack_workbench_top`).

#### 5. `incubation_brazier` (Braseiro de Incubação Térmica)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\incubation_brazier.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/incubation_brazier.json`
* **Quantidade de Elementos 3D:** 19 cubos geométricos.
* **Dimensões & Geometria:**
  - Pedestal escalonado de ardósia cinzelada em 2 níveis e fuste de coluna central octogonal esculpido, coroado por capitel saliente.
  - Bacia superior de braseiro em cantaria vulcânica com taça cônica e poço de magma perpétuo pulsante com núcleo de fogo concentrado até `Y = 17`.
  - 4 garras/talões arqueados de ferro forjado ancorados na borda externa que sobem e curvam-se para dentro com pontas em gancho, focalizando o raio térmico emitido para os ninhos circundantes.
* **Texturas Mapeadas:** `incubation_brazier_top.png`, `incubation_brazier_side.png`, `incubation_brazier_bottom.png` (Partícula: `incubation_brazier_top`).

#### 6. `draconic_anvil` (Bigorna Dracônica)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\draconic_anvil.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/draconic_anvil.json`
* **Quantidade de Elementos 3D:** 17 cubos geométricos.
* **Dimensões & Geometria:**
  - Base pesada escalonada de obsidiana de alta densidade (`[2, 0, 2]` a `[14, 4, 14]`), cintura afunilada com veios de magma líquido e pescoço estrutural de suporte.
  - Corpo maciço de forjamento com placas laterais entalhadas em runas incandescentes e abas de dispersão de impacto.
  - Mesa plana superior de golpe em obsidiana pura polida com relevos rúnicos para forja de ligas pesadas.
  - Talão posterior robusto chanfrado e chifres frontais duplos de dragão esculpidos, projetando-se para a frente e curvando-se para cima até pontas afiladas (`Z = 0 a -6`, `Y = 10.5 a 16.5`).
* **Texturas Mapeadas:** `draconic_anvil_top.png`, `draconic_anvil_side.png`, `draconic_anvil_bottom.png` (Partícula: `draconic_anvil_top`).

#### 7. `dragon_perch` (Poleiro Dracônico)
* **Arquivo Blockbench:** `D:\Mine\models\blocks\dragon_perch.bbmodel`
* **Modelo Minecraft:** `src/main/resources/assets/wingsofthewild/models/block/dragon_perch.json`
* **Quantidade de Elementos 3D:** 16 cubos geométricos.
* **Dimensões & Geometria:**
  - Sapata de apoio em madeira de lei com cintas e placas de ancoragem para fixação em rocha ou solo.
  - Mastro vertical central espesso reforçado com anéis cilíndricos de ferro forjado e suporte de junção em abraçadeira.
  - Duas mãos-francesas diagonais em barra de ferro travando a viga transversal.
  - Trave transversal chanfrada de 26 unidades de envergadura (`X = -5 a 21`), com trilho superior chanfrado para pouso de garras dracônicas, ranhuras de fricção antiderrapante e ponteiras de ferro reforçado com olhais de suspensão para correntes e amarras.
* **Texturas Mapeadas:** `dragon_perch_top.png`, `dragon_perch_side.png`, `dragon_perch_bottom.png` (Partícula: `dragon_perch_side`).

---

### 🔍 MATRIZ DE CERTIFICAÇÃO TÉCNICA (QA & COMPATIBILIDADE)
* ✅ **Coordenadas Vanilla Válidas:** Todos os vértices contidos no intervalo legal `[-16.0, 32.0]`.
* ✅ **Rotações de Eixo Único:** Rotações apenas em eixos permitidos com ângulos permitidos pelo Minecraft Java Edition (`-45°`, `0°`, `+45°`).
* ✅ **Mapeamento UV Preciso:** Todas as coordenadas UV no espaço `[0.0, 16.0]` mapeadas sem distorção para as texturas 16x16 PNG RGBA oficiais.
* ✅ **Partículas de Quebra Configuradas:** Tag `particle` definida com caminhos válidos em todos os modelos JSON.
* ✅ **Blockbench `.bbmodel` 100% Autónomos:** Todos os 7 arquivos `.bbmodel` contêm imagens em base64 embutidas (`source: data:image/png;base64,...`), abrindo diretamente no Blockbench sem alertas de textura ausente.
* ✅ **Transforms de Exibição Completos:** Modos `gui`, `ground`, `thirdperson`, `firstperson` e `fixed` calibrados em perspectiva isométrica para ícones nítidos no inventário e na mão do jogador.
* ✅ **Blockstates & Item Models:** Sincronizados com `wingsofthewild:block/<nome>`.

---

### ✅ Rodada 2 — Correção e Remodelagem 3D dos Blocos com Transparência (Concluída em 2026-10-07)

Atendendo ao feedback de testes in-game sobre artefatos de transparência e oclusão em cubos vazados, foram remodelados e certificados 3 blocos:

#### 1. `ember_lantern` (Lanterna de Brasas 3D Dracônica)
* **Arquivos Gerados:** `D:\Mine\models\blocks\ember_lantern.bbmodel` e `src/main/resources/assets/wingsofthewild/models/block/ember_lantern.json`.
* **Quantidade de Elementos 3D:** 18 cubos geométricos (eliminando o antigo `cube_all` oco).
* **Estrutura & Detalhes:**
  - Base de metal chanfrada em cantaria forjada (`[5, 0, 5]` a `[11, 2, 11]`).
  - 4 pilares de ferro escuro nos cantos estruturando a câmara de luz (`Y = 2 a 7`).
  - 4 painéis de vidro translúcido nas quatro faces.
  - Núcleo de brasa incandescente ardendo e pulsando no centro geométrico (`[6.8, 3.2, 6.8]` a `[9.2, 5.8, 9.2]`) com espícula vertical de chama.
  - Cúpula de metal superior escalonada em dois níveis chanfrados com colarinho de exaustão central (`Y = 7 a 10.2`).
  - Alça e argola de ferro forjado superior articulada com haste e elo circular (`Y = 10.2 a 14`).
* **Textura:** Mapeamento UV calibrado sobre `ember_lantern.png` (min_alpha = 255 em todos os componentes opacos, sem artefatos vazados).

#### 2. `flamefang_trophy_skull` (Crânio de Troféu de Flamefang)
* **Arquivos Gerados:** `D:\Mine\models\blocks\flamefang_trophy_skull.bbmodel` e `src/main/resources/assets/wingsofthewild/models/block/flamefang_trophy_skull.json`.
* **Quantidade de Elementos 3D:** 25 cubos geométricos (estilo mob head / dragon head tridimensional).
* **Estrutura & Detalhes:**
  - Suporte/toco cervical de assentamento plano no chão (`[5, 0, 8]` a `[11, 3, 14]`, `Y = 0` a `3`), garantindo estabilidade física.
  - Caixa craniana tridimensional escalonada em dois níveis com placa frontal espessa.
  - Focinho reptiliano em blocos saliente para a frente (`Z = -5` a `6`), com crista nasal chanfrada e narinas.
  - Mandíbula inferior volumétrica e queixo ossudo.
  - Sobrancelhas ósseas proeminentes protegendo órbitas oculares profundas e sombrias.
  - Dentes e presas afiadas de Flamefang (fileiras superiores e inferiores em marfim/esmalte).
  - Par de chifres pontiagudos curvados para trás e para cima (`Z = 10` a `21`, `Y = 10` a `15.5`).
  - Esporões ósseos nas bochechas laterais (jugal spikes).
* **Textura:** `flamefang_trophy_skull_front.png` com UVs restritos às áreas sólidas de marfim, órbitas escuras e chifres de obsidiana (zero transparência).

#### 3. `incubation_brazier` (Braseiro de Incubação Térmica — Correção do Rodapé)
* **Arquivos Atualizados:** `D:\Mine\models\blocks\incubation_brazier.bbmodel` e `src/main/resources/assets/wingsofthewild/models/block/incubation_brazier.json`.
* **Correções Aplicadas:**
  - Pedestal de base assentado perfeitamente no chão de `Y = 0` a `Y = 2.5` (`[1, 0, 1]` a `[15, 2.5, 15]`), com `cullface: "down"`.
  - Textura do rodapé e colar intermediário mapeadas para `incubation_brazier_bottom.png` (textura 100% opaca, sem nenhum pixel transparente), eliminando completamente a folga transparente e linhas invisíveis relatadas in-game.
  - UVs do fuste da coluna fixados estritamente na faixa segura `Y = 4..10` de `incubation_brazier_side.png`, evitando a linha vazada de índice 15.
