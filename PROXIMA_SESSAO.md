# 📋 Planejamento Estratégico — Próxima Sessão de Desenvolvimento
## Mod: Wings of the Wild (Minecraft 26.3 NeoForge)

**Status Atual:** 116 / 116 Itens e Blocos Implementados, Auditados e Compilados no JAR. Modelos das 3 fases do Flamefang (Filhote, Juvenil e Adulto) estruturados no Blockbench.

---

### 🐲 1. Agente 2: Arquiteto 3D de Criaturas (`creature_model_dev`)
**Foco Exclusivo:** Refatoração Completa do Pacote de Animações do Dragão Adulto & Fases de Vida.

1. **Refatoração do Voo (`fly_flap`):**
   - Restaurar a fluidez senoidal e cinematográfica das asas largas de 284 unidades.
   - Bater de asas vigoroso com arqueamento no *upstroke* e empuxo com abertura no *downstroke*.
   - Ondulação harmônica suave da cauda em chicote no ar e recolhimento perfeito das 4 patas rentes ao ventre aerodinâmico.
   - Animação de Planeio (`glide`): Asas estendidas imóveis flutuando nas correntes de ar durante mergulhos.
2. **Novas Animações de Vida & Imersão:**
   - `eating` (Comendo): Dragão abaixa o pescoço, mastiga rítmica e avidamente a carne ou petiscos com a mandíbula abrindo e fechando, engolindo com movimento do esôfago.
   - `sleep` (Dormindo): Dragão deita no chão/ninho, recolhe as 4 patas sob o corpo, dobra as asas coladas ao tronco, curva o pescoço sobre a cauda e fecha os olhos com respiração profunda lenta.
   - `wake_up` (Acordando): Abre os olhos de lava, boceja estalando a mandíbula, estica as patas dianteiras e ergue o pescoço em postura de alerta.
   - `roar` (Rugido de Batalha): Estufa o peitoral de 60 unidades, abre as asas em intimidação e ruge para o alto.

---

### 🏛️ 2. Novo Agente: Modelador 3D de Estações & Blocos (`block_model_dev`)
**Foco Exclusivo:** Modelagem 3D anatômica e texturização no Blockbench dos blocos de chão (separado do agente de criaturas).

1. **`dragon_nest` (Ninho Dracônico Artesanal):**
   - Formato côncavo circular esculpido com galhos entrelaçados grossos, pedras de apoio e forração macia de palha chamuscada para o ovo de magma repousar no centro.
2. **`draconic_foundry` (Forja de Ligas Dracônica):**
   - Bloco com cadinho refratário superior, arco de pedra vulcânica, portas de fusão metálicas com chamas visíveis e canaletas para escoamento de liga líquida.
3. **`draconic_hearth` (Fornalha Culinária Dracônica):**
   - Chaminé rústica com grelha de cinzas, caldeirão central e compartimento térmico para cozimento de ensopados e bifes.
4. **`tack_workbench` (Bancada de Selaria Dracônica):**
   - Estrado de madeira reforçada com couro curtido esticado, rolo de tendões, ferramentas de corte de osso penduradas e fivelas.
5. **`incubation_brazier` (Braseiro de Incubação Térmica):**
   - Pedestal esculpido em ardósia com bacia de brasas eternas e labaredas térmicas para ninhos.
6. **`draconic_anvil` (Bigorna Dracônica Pesada):**
   - Bigorna maciça de pedra vulcânica com chifres frontais de dragão e entalhes de runas.
7. **`dragon_perch` (Poleiro Dracônico):**
   - Tronco esculpido com trave transversal de pouso para dragões domesticados descansarem.

---

### 💻 3. Agente 1: Engenheiro de Sistemas & Itens (`item_systems_dev`)
**Foco Exclusivo:** Telas de Interface (GUIs) & Receitas para o JEI.

1. **Interfaces Gráficas (GUIs & Containers):**
   - GUI da `draconic_foundry` (Forja de Ligas): Menu com 2 slots de minério/metal, 1 slot de combustível térmico, barra de fusão e slot de saída para a liga.
   - GUI da `draconic_hearth` (Fornalha Culinária): Menu de caldeirão com slot de ingrediente base, slot de tempero de cinzas e slot de tigela/frasco.
   - GUI da `tack_workbench` (Bancada de Selaria): Menu para costura de selas, rédeas e expansões de alforjes.
   - GUIs de Inventário Móvel do Dragão: Telas de 9 slots (`small_dragon_pouch`) e 27 slots (`large_dragon_saddlebags`) abríveis ao interagir agachado no dragão montado.
2. **Receitas de Crafting & Integração JEI (`recipes/*.json`):**
   - Geração de todas as receitas de fundição, ligas, forja de ferramentas e itens para exibição imediata e nativa no mod JEI.

---

### 🎨 4. Agente 3: Artista Pixel 2D (`pixel_artist_2d`)
**Foco Exclusivo:** Texturas das Telas de Interface (GUIs).

1. **Arte das Janelas de Interface (256x256 PNG):**
   - `draconic_foundry_gui.png`: Layout temático de pedra vulcânica escura, barras de chamas e slots de liga.
   - `draconic_hearth_gui.png`: Layout culinário rústico com indicador de brasa acesa.
   - `tack_workbench_gui.png`: Layout em tom conhaque de couro costurado com agulha e molduras de bronze.
   - `dragon_inventory_gui.png`: Layout de alforje com baú acoplado e silhueta do dragão.

---

### 🛡️ 5. Agente 4: Auditor de Qualidade (`items_qa_reviewer`)
**Foco Exclusivo:** Inspeção e Testes das Novas Funcionalidades.

1. Verificação contínua das novas GUIs, compatibilidade de pacotes de rede (packets de sincronização de menu), integridade dos novos modelos 3D de bloco e validação do JEI.

---
*Documento gerado em 2026-10-06. Pronto para disparo na próxima mensagem do usuário!*
