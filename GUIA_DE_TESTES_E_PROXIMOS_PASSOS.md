# 🗺️ Guia de Testes Passo a Passo & Próximos Passos
## Mod: Wings of the Wild (`wingsofthewild`) — Versão 1.0.1 (NeoForge 26.3)

---

## 📌 1. Regra Permanente de Versão & Backup no Git

> [!IMPORTANT]
> **Regra de Versionamento:** A partir da versão atual (**`1.0.1`**), sempre que o arquivo `.jar` for modificado ou recompilado após a finalização de uma tarefa por qualquer agente, o número de versão será elevado sequencialmente em `gradle.properties` (`1.0.1` ➔ `1.0.2` ➔ `1.0.3`...).
> **Backup Automático:** Todas as alterações são commitadas e enviadas diretamente para o repositório oficial no GitHub: [https://github.com/RanzimzimDev/mod-mine.git](https://github.com/RanzimzimDev/mod-mine.git).

---

## 🧪 2. Roteiro de Testes Passo a Passo (Dentro do Jogo)

Siga este roteiro dentro do seu Minecraft para validar visualmente e mecanicamente todas as novidades:

### 🐲 Teste 1: Invocar o Dragão Adulto e Animações
1. Entre no seu mundo no modo Criativo.
2. Abra o chat e digite o comando:
   ```mcfunction
   /summon wingsofthewild:flamefang ~ ~ ~
   ```
3. **O que observar:**
   - O Flamefang surgirá com o modelo 3D atualizado, sem blocos cortados ou vazados.
   - Observe a **cauda do dragão**: ela está **2.5 vezes mais larga** (37 unidades) com lâmina de magma, esporões laterais e 7 segmentos articulados com ondulação fluida.
   - Observe a animação parada (**`idle`**): ele respira de forma nobre e viva, com a cauda e o pescoço ondulando suavemente.

### 🥩 Teste 2: Alimentação, Domesticação e Comandos
1. Abra o inventário criativo na aba **Wings of the Wild** e pegue:
   - **Bagas Magmáticas Picantes** (`spicy_magma_berries`)
   - **Carne Chamuscada** (`charred_meat`)
   - **Petisco Dracônico** (`draconic_treat`)
2. Aproxime-se do Flamefang e clique nele com o **botão direito** segurando o alimento:
   - **O que observar:** Ele executará a **animação de mastigação (`eating`)** com 3 mordidas ritmadas abrindo a mandíbula para rasgar a comida e engolindo em seguida.
   - Partículas de fumaça e corações aparecerão indicando que ele foi domesticado.
3. Com o dragão domesticado:
   - Clique com o **botão direito** nele (com a mão vazia): ele sentará e deitará, ativando a **animação de sono (`sleep`)**, encolhendo as patas, fechando as asas como um escudo e enrolando a cauda.
   - Clique novamente com o botão direito para acordá-lo (**`wake_up`**): ele boceja escancarando a boca em 62°, se espreguiça e se levanta.
   - Segure **`Shift` + Botão Direito**: o dragão estufará o peito, abrirá as asas colossais de 284 unidades e executará a animação do **Rugido Titânico (`roar`)**.

### 🛡️ Teste 3: Armadura Dracônica no Corpo do Jogador
1. No inventário criativo, pegue o conjunto completo:
   - **Elmo de Flamefang** (`flamefang_helmet`)
   - **Peitoral de Flamefang** (`flamefang_chestplate`)
   - **Calças de Flamefang** (`flamefang_leggings`)
   - **Botas de Flamefang** (`flamefang_boots`)
2. Abra seu inventário (`E`) e equipe as 4 peças nos seus respectivos slots de armadura.
3. Pressione a tecla **`F5`** para ver o personagem em terceira pessoa (frente e costas):
   - **O que observar:** A armadura renderizará sobre o modelo do seu jogador com o elmo de chifres, peitoral de escamas com o núcleo *Flame Core* pulsante no esterno e grevas articuladas.

### 📖 Teste 4: Nomes em Português e Descrições (Tooltips)
1. No inventário criativo, passe o mouse sobre diferentes itens:
   - *Lingote de Brasa*, *Braseiro de Incubação*, *Núcleo de Chama*, *Ovo de Flamefang*, *Carne Chamuscada*, etc.
2. **O que observar:**
   - Todos os nomes devem estar perfeitamente traduzidos em **Português**.
   - Logo abaixo do nome, deve aparecer um texto explicativo em **cinza itálico** contendo a história ou utilidade prática de cada item.

### 🏮 Teste 5: Blocos 3D & Verificação de Transparências
1. Pegue no inventário criativo e coloque no chão:
   - **Braseiro de Incubação** (`incubation_brazier`): observe a base rente ao solo — a linha branca transparente foi eliminada.
   - **Lanterna de Brasas** (`ember_lantern`): observe o modelo 3D real, com 4 pilares de ferro, vidros translúcidos, núcleo de fogo no centro e argola articulada no topo.
   - **Crânio de Troféu Flamefang** (`flamefang_trophy_skull`): observe a escultura 3D completa estilo cabeça de dragão (focinho saliente, mandíbula, dentes afiados e chifres longos para trás).
   - **Lingote de Frostburn** (`frostburn_alloy_ingot`): confira no inventário se o ícone está totalmente sólido com bordas de gelo ciano e miolo incandescente.

### 🔨 Teste 6: Sons dos Minérios ao Quebrar
1. Coloque no chão: *Minério de Brasa*, *Minério de Adamantina Vulcânica*, *Minério de Titânio* e *Minério de Quartzo Etéreo*.
2. Mude para o modo Sobrevivência (`/gamemode survival`) e quebre-os com uma picareta.
3. **O que observar:** Todos soam como rocha firme quebrando, e minérios mais densos e raros emitem um som de quebra mais grave e abafado.

### 📜 Teste 7: Integração JEI e Estações de Trabalho
1. Pressione a tecla do **JEI** (ou pesquise `@wingsofthewild` na barra inferior).
2. Clique sobre qualquer lingote ou armadura para ver as 65 receitas cadastradas.
3. Coloque e abra com o botão direito as 3 estações interativas:
   - **Forja de Ligas Dracônica** (`draconic_foundry`): interface com 2 entradas de minérios, combustível térmico e slot de liga.
   - **Fornalha Culinária** (`draconic_hearth`): interface culinária com fogo e preparo de refeições.
   - **Bancada de Selaria** (`tack_workbench`): bancada com grade 3x3 de confecção de arreios.

---

## 🚀 3. Planejamento dos Próximos Passos (Roadmap de Desenvolvimento)

Aqui está a sequência recomendada para as próximas sessões:

### 🎯 Passo 1: Montaria & Sistema de Voo Dirigido (Gameplay Principal)
- **Equipamento de Montaria:** Permitir colocar selas (`basic_dragon_saddle`, `reinforced_flame_saddle`) no dragão domado clicando nele agachado.
- **Subir no Dragão:** Montar no dragão com botão direito quando selado.
- **Controle de Movimentação no Solo:** Teclas WASD direcionam o dragão enquanto montado.
- **Decolagem & Voo com Teclas:**
  - Pressionar `Espaço` para bater asas vigorosamente, decolar do chão e ganhar altitude (disparando a animação `fly_flap`).
  - Olhar para o horizonte ou para baixo para planar em alta velocidade (disparando a animação `glide`).
  - Tecla `Shift` para descer suavemente e pousar no solo.

### 🔥 Passo 2: Ataques de Montaria & Sopro de Magma
- **Disparo Montado:** Ao pressionar uma tecla de ataque (ou botão esquerdo montado), o dragão executa a animação de ataque e cospe uma bola de fogo explosiva (`FlameballProjectile`) ou rajada contínua de fogo contra os alvos.
- **Mordida Terrestre:** Ataque frontal contra monstros quando estiver no chão.

### 🥚 Passo 3: Sistema Vivo de Incubação do Ovo no Ninho
- Colocar o `dragon_nest` no chão e posicionar o `flamefang_egg` no centro côncavo.
- Se houver um `incubation_brazier` aceso ao lado fornecendo calor constante, o ovo começa a emitir partículas térmicas de brasas.
- Após o tempo de incubação (ou com a ajuda de combustíveis térmicos), o ovo racha e choca um **Filhote de Flamefang** (`flamefang_hatchling`), que já nasce com suas 8 animações exclusivas e segue o jogador!

### 📈 Passo 4: Crescimento & Progressão por Fases
- Alimentar o filhote com refeições ricas em magma acelera seu crescimento para a fase **Juvenil** (`flamefang_juvenile`).
- O dragão juvenil ganha força para carregar bolsas pequenas (`small_dragon_pouch`) e voos curtos, até atingir a maturidade como **Adulto**.

### 🌍 Passo 5: Geração de Ninhos e Estruturas no Mundo Selvagem
- Geração natural de ninhos e covis vulcânicos no topo de picos nevados e biomas basálticos.
- Ovos selvagens protegidos por dragões adultos territoriais.

---
*Documento gerado autonomamente pela equipe de desenvolvimento Wings of the Wild.*
