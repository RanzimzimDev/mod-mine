# 🐉 Wings of the Wild - Guia de Testes da Versão 1.0.8

> O arquivo `wingsofthewild-1.0.8.jar` já foi compilado e instalado em `D:\Minecraft\.minecraft\versions\Mod\mods\`.
> Todas as correções relatadas foram implementadas e verificadas.

---

## 📋 Resumo das Correções Implementadas

1. **Animações dos Dragões (Adulto, Juvenil e Filhote):**
   - Os identificadores de animação do GeckoLib foram mapeados e sincronizados para as chamadas diretas (`idle`, `walk`, `fly_flap`, `glide`, `attack_bite`, `attack_fireball`, `roar`, `sleep`, `eating`).
   - Sombra do filhote reduzida dinamicamente conforme a escala da criatura (`0.35x`).

2. **Controle de Montaria & Voo Rebalanceado:**
   - **Controle WASD Real:** O dragão agora lê diretamente as teclas do jogador (`W` avança, `S` reduz/recua, `A` e `D` manobram lateralmente). O dragão não anda mais sozinho ao montar!
   - **Velocidade Calibrada:** Velocidade de cruzeiro reduzida para um voo estável e manobrável (`0.16F` batendo asas, `0.28F` planando).
   - **Descida Segura com Shift:** Pressionar `Shift` no ar não derruba mais o jogador no vácuo! O dragão inicia uma descida suave até tocar o solo. O desmonte só ocorre de forma segura no chão ou em segurança. Caso ocorra desmonte no alto, o jogador recebe efeito de *Queda Lenta (Slow Falling)* preventivo.

3. **Combate Montado:**
   - **Botão Esquerdo:** Agora ataca com mordida voraz no solo e cospe bolas de fogo no ar.
   - **Tecla R:** Dispara bola de fogo explosiva com animação dracônica.

4. **Novo Sistema de Crescimento e Idade (Temporizado):**
   - **Filhote -> Juvenil:** 10 minutos de tempo natural. Pode ser acelerado com comidas magmáticas para até **5 minutos** no mínimo.
   - **Juvenil -> Adulto:** 30 minutos de tempo natural. Pode ser acelerado com comidas magmáticas para até **15 minutos** no mínimo.
   - O progresso de idade é salvo permanentemente no NBT da entidade.

5. **Bancadas & GUIs com BlockEntities e Persistência:**
   - **Forja de Ligas (`draconic_foundry`):** Possui 4 slots (Entrada A, Entrada B, Combustível, Saída). Funde ligas e minérios elementais sem perder nenhum item ao fechar o inventário!
   - **Fornalha Culinária (`draconic_hearth`):** Possui 4 slots (Ingrediente A, Ingrediente B, Combustível, Saída). Prepara pratos culinários dracônicos com cozimento ativo e persistente.

6. **Tomo do Dragonologista & Estojo de Mapas:**
   - Cores de texto corrigidas para ARGB com 100% de opacidade (`0xFF`), tornando todas as páginas, capítulos e coordenadas perfeitamente legíveis.

7. **Luvas de Domador (`dragon_handler_gloves`):**
   - Agora concede **Resistência ao Fogo e Calor** permanente enquanto segurada na mão principal ou na mão secundária (*off-hand*), permitindo resgatar ovos de ninhos em brasa com total segurança.

8. **Drops de Minérios Corrigidos:**
   - Tabelas de loot atualizadas para o padrão 26.3: quebrar com picareta de ferro/diamante sem toque suave agora dropa os minérios e gemas brutos (`raw_ember`, `raw_terraslate`, etc.) com bônus de Fortuna!

---

## 🧪 Roteiro de Testes Passo a Passo

### Teste 1: Montaria, WASD e Descida Suave com Voo
1. Pegue um ovo de spawn do Flamefang Adulto: `/give @p wingsofthewild:flamefang_spawn_egg`
2. Pegue uma sela: `/give @p wingsofthewild:basic_dragon_saddle` e bagas magmáticas `/give @p wingsofthewild:spicy_magma_berries 16`
3. Dome o dragão clicando nele com as bagas e agache com a sela na mão para equipá-la.
4. Monte com botão direito (sem agachar).
5. **Verificação de Solo:** Note que o dragão fica parado. Pressione `W`, `A`, `S`, `D` e veja que ele responde exatamente ao seu comando, tocando a animação `walk` ou `idle`!
6. **Decolagem:** Pressione `Espaço` para bater as asas e decolar. Observe a animação `fly_flap`.
7. **Planar:** Olhe para o horizonte ou ligeiramente para baixo (`> 12°`) e segure `W` para planar em alta velocidade com a animação `glide`.
8. **Descida Suave com Shift:** Enquanto estiver voando alto, pressione `Shift`. Observe que você **não cai do dragão**: ele desce suavemente em direção ao solo e pousa!
9. **Ataques:**
   - No solo: dê um clique com o **Botão Esquerdo** do mouse para executar a mordida (`attack_bite`).
   - No ar: dê um clique com o **Botão Esquerdo** ou aperte a tecla **R** para cuspir uma bola de fogo explosiva (`attack_fireball`).

---

### Teste 2: Crescimento por Fases (Filhote e Juvenil)
1. Pegue o ninho e o ovo:
   `/give @p wingsofthewild:dragon_nest`
   `/give @p wingsofthewild:flamefang_egg`
   `/give @p wingsofthewild:incubation_brazier`
2. Coloque o ninho sobre ou ao lado do braseiro aceso, coloque o ovo no centro com o botão direito.
3. Aguarde ou use pó de brasa para chocar o filhote.
4. Observe o modelo do filhote: a sombra agora é pequena e proporcional ao seu tamanho!
5. Alimente o filhote com `/give @p wingsofthewild:draconic_treat 10`:
   - Note os corações e partículas de crescimento.
   - O dragão precisará de pelo menos 5 minutos para se tornar Juvenil (ou 10 minutos se você não o alimentar).
   - Quando juvenil, precisará de pelo menos 15 minutos (ou 30 minutos sem alimentação) para se tornar adulto.

---

### Teste 3: Forja de Ligas (`draconic_foundry`)
1. Coloque a bancada no chão: `/give @p wingsofthewild:draconic_foundry`
2. Abra a GUI com botão direito.
3. **Itens para Teste:**
   - **Combustível:** Coloque carvão (`minecraft:coal`) ou brasa (`wingsofthewild:raw_ember`) no slot inferior de combustível.
   - **Entrada A:** Coloque 1x Minério de Brasa Bruta (`wingsofthewild:raw_ember`).
   - **Entrada B:** Deixe vazio (ou coloque outro `raw_ember` para criar o Núcleo Purificado!).
4. Feche a GUI (`ESC`), aguarde 5 segundos e abra novamente:
   - **Verificação:** Os itens continuam exatamente onde você colocou!
   - A barra de chama acende e a seta de fundição avança.
   - O item no slot de saída será o **Lingote de Brasa** (`wingsofthewild:ember_ingot`) ou **Núcleo de Brasa Purificado** (`wingsofthewild:refined_ember_core`)!

---

### Teste 4: Fornalha Culinária (`draconic_hearth`)
1. Coloque a bancada no chão: `/give @p wingsofthewild:draconic_hearth`
2. Abra a GUI.
3. **Itens para Teste:**
   - **Combustível:** Coloque carvão ou cinzas vulcânicas (`wingsofthewild:volcanic_ash`).
   - **Ingrediente A:** Coloque Bagas Magmáticas (`wingsofthewild:spicy_magma_berries`).
   - **Ingrediente B:** Coloque Açúcar (`minecraft:sugar`) ou Tigela (`minecraft:bowl`).
4. Feche a GUI e abra novamente:
   - Os itens permanecem no inventário do bloco.
   - O cozimento produz a **Torta de Bagas Vulcânicas** (`wingsofthewild:molten_berry_tart`) ou **Caldo Defumado** (`wingsofthewild:smoke_infused_broth`)!

---

### Teste 5: Tomo do Dragonologista & Estojo de Mapas
1. Pegue o tomo: `/give @p wingsofthewild:dragonologist_tome`
2. Clique com botão direito para abrir:
   - As páginas agora exibem textos nítidos em preto, dourado e vermelho escuro com o indicador de páginas no canto superior!
3. Pegue o estojo: `/give @p wingsofthewild:flight_map_case`
4. Clique com botão direito para abrir:
   - As coordenadas reais e as configurações de teto de voo agora estão totalmente visíveis e em alto contraste.

---

### Teste 6: Luvas de Domador na Mão Secundária (Off-hand)
1. Pegue as luvas: `/give @p wingsofthewild:dragon_handler_gloves`
2. Coloque as luvas na mão secundária (`Tecla F`):
   - Observe que você recebe o efeito de **Resistência ao Fogo** instantaneamente enquanto as estiver segurando!
3. Entre na lava ou no fogo: você não tomará dano térmico!

---

### Teste 7: Mineração dos Minérios
1. Pegue uma picareta de ferro ou diamante comum (sem toque suave): `/give @p minecraft:iron_pickaxe`
2. Coloque no chão qualquer minério:
   - `/give @p wingsofthewild:ember_ore`
   - `/give @p wingsofthewild:terraslate_ore`
   - `/give @p wingsofthewild:frostbite_ore`
3. Quebre os blocos no modo sobrevivência:
   - Eles irão dropar seus respectivos fragmentos brutos (`raw_ember`, `raw_terraslate`, etc.) prontos para serem fundidos na Forja de Ligas!
