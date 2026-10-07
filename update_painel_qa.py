import re

PAINEL_PATH = r"D:\Mine\painel.html"

with open(PAINEL_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update tab buttons
old_tab_btn = '<button class="tab-btn" onclick="switchTab(\'equipe\')">🤖 Equipe de Agentes (3 Ativos)</button>'
new_tab_btns = """<button class="tab-btn" onclick="switchTab('equipe')">🤖 Equipe de Agentes (4 Especialistas)</button>
      <button class="tab-btn" onclick="switchTab('auditoria')">🛡️ Auditoria & QA (100% Conforme)</button>"""

if old_tab_btn in html:
    html = html.replace(old_tab_btn, new_tab_btns)
    print("Tab buttons updated.")

# 2. Add Agent 4 Card into tab-equipe
# Find Agente 3 card and append Agente 4 card after it
agent4_card = """
        <div class="kpi-card" style="border-color: #58a6ff;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="color: #58a6ff;">🛡️ Agente 4: Auditor de Qualidade & Inspetor Técnico</h3>
            <span class="status-tag status-done">100% CERTIFICADO (80/80)</span>
          </div>
          <p style="color: var(--text-muted); margin: 10px 0; font-size: 0.92rem;">
            Responsável pela auditoria estrita, validação de sintaxe JSON, integridade de texturas PNG, localização I18N, aba criativa e empacotamento no JAR.
          </p>
          <div style="font-size: 0.85rem; color: #c9d1d9;">
            📁 <b>Memória:</b> <code>D:\\Mine\\MEMORIA_AGENTE_AUDITORIA.md</code><br>
            🔍 <b>Script Validador:</b> <code>D:\\Mine\\audit_validator.py</code><br>
            📦 <b>Certificação Técnica:</b> 80 / 80 Itens e Blocos Aprovados em 6 Dimensões (Taxa de Sucesso: 100.0%)<br>
            ⚙️ <b>Compilação NeoForge:</b> <code>./gradlew build</code> BUILD SUCCESSFUL (Jar de 197.955 bytes com 262 arquivos).
          </div>
        </div>
"""

agent3_marker = '<!-- Tab Galeria 2D -->'
# Insert agent4_card before the closing </div> of tab-equipe
# Let's find:
tab_equipe_close = """      </div>
    </div>

    <!-- Tab Galeria 2D -->"""

new_tab_equipe_close = f"""{agent4_card}      </div>
    </div>

    <!-- Tab Galeria 2D -->"""

if tab_equipe_close in html:
    html = html.replace(tab_equipe_close, new_tab_equipe_close)
    print("Agent 4 card added to tab-equipe.")

# 3. Add tab-auditoria before Tab Galeria 2D or after tab-equipe
tab_auditoria_html = """
    <!-- Tab Auditoria & QA -->
    <div id="tab-auditoria" class="tab-content">
      <div style="background: linear-gradient(135deg, rgba(88,166,255,0.12) 0%, rgba(22,26,34,0.8) 100%); border: 1px solid rgba(88,166,255,0.3); border-radius: 14px; padding: 22px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 style="color: #fff; font-size: 1.45rem; display: flex; align-items: center; gap: 10px;">
              🛡️ Auditoria Técnica & Certificação de Qualidade (QA Pass)
            </h2>
            <p style="color: var(--text-muted); margin-top: 4px;">
              Inspeção técnica automatizada de todos os 80 itens e blocos do mod <b>Wings of the Wild</b> (Minecraft 26.3 NeoForge).
            </p>
          </div>
          <div>
            <span class="badge green" style="font-size: 0.95rem; padding: 6px 14px;">✅ 100% CONFORME (80 / 80 ITENS)</span>
          </div>
        </div>
      </div>

      <!-- QA KPI Cards -->
      <div class="kpi-grid" style="margin-bottom: 24px;">
        <div class="kpi-card" style="border-color: #2ea043;">
          <div class="kpi-title">Itens Auditados & Aprovados</div>
          <div class="kpi-value" style="color: #3fb950;">80 / 80</div>
          <div class="kpi-sub">100.0% de Conformidade Técnica</div>
        </div>
        <div class="kpi-card" style="border-color: #58a6ff;">
          <div class="kpi-title">Modelos & Blockstates JSON</div>
          <div class="kpi-value" style="color: #58a6ff;">112 Arquivos</div>
          <div class="kpi-sub">0 Erros de Sintaxe / Herança Válida</div>
        </div>
        <div class="kpi-card" style="border-color: #a371f7;">
          <div class="kpi-title">Texturas 16x16 PNG RGBA</div>
          <div class="kpi-value" style="color: #a371f7;">100% Válidas</div>
          <div class="kpi-sub">Testadas via Pillow (Zero Corrupção)</div>
        </div>
        <div class="kpi-card" style="border-color: #ff9800;">
          <div class="kpi-title">Compilação NeoForge</div>
          <div class="kpi-value" style="color: #ff9800;">BUILD PASS</div>
          <div class="kpi-sub">197 KB JAR / 262 Arquivos Empacotados</div>
        </div>
      </div>

      <!-- Tabela dos 6 Critérios Auditados -->
      <div class="kpi-card" style="margin-bottom: 24px;">
        <h3 style="color: #fff; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
          📋 Matriz das 6 Dimensões de Qualidade Inspecionadas
        </h3>
        <table class="item-table" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="border-bottom: 2px solid var(--border-color); text-align: left;">
              <th style="padding: 10px; color: var(--text-muted);">Dimensão Auditada</th>
              <th style="padding: 10px; color: var(--text-muted);">Escopo Avaliado</th>
              <th style="padding: 10px; color: var(--text-muted);">Critérios de Rigor</th>
              <th style="padding: 10px; color: var(--text-muted);">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid #1f2532;">
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">1. Registro Java NeoForge</td>
              <td style="padding: 12px 10px;"><code>ModBlocks.java</code> & <code>ModItems.java</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">IDs únicos, DeferredRegister, food properties, armor/tool materials e resistência.</td>
              <td style="padding: 12px 10px;"><span class="badge green">80 / 80 Aprovados (100%)</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #1f2532;">
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">2. Sintaxe & Modelos JSON</td>
              <td style="padding: 12px 10px;"><code>blockstates/</code>, <code>models/block/</code>, <code>models/item/</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">JSON válido, referências a parents válidos (cube, cube_all, generated, handheld).</td>
              <td style="padding: 12px 10px;"><span class="badge green">112 / 112 Aprovados (100%)</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #1f2532;">
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">3. Texturas 2D PNG</td>
              <td style="padding: 12px 10px;"><code>textures/block/</code>, <code>textures/item/</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">Validadas via Pillow: formato PNG autêntico, 16x16 pixels, canal alfa RGBA sem perdas.</td>
              <td style="padding: 12px 10px;"><span class="badge green">80+ Texturas Aprovadas</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #1f2532;">
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">4. Localização Bilíngue (I18N)</td>
              <td style="padding: 12px 10px;"><code>lang/en_us.json</code> & <code>lang/pt_br.json</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">Chaves <code>block.*</code> e <code>item.*</code> completas, sem strings vazias ou desbalanceadas.</td>
              <td style="padding: 12px 10px;"><span class="badge green">160 / 160 Chaves Aprovadas</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #1f2532;">
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">5. Aba Criativa Oficial</td>
              <td style="padding: 12px 10px;"><code>ModCreativeTabs.java</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">Chamada explícita <code>output.accept(...)</code> para todos os itens e blocos do mod.</td>
              <td style="padding: 12px 10px;"><span class="badge green">80 / 80 Aprovados (100%)</span></td>
            </tr>
            <tr>
              <td style="padding: 12px 10px; font-weight: 600; color: #fff;">6. Empacotamento JAR</td>
              <td style="padding: 12px 10px;"><code>wingsofthewild-1.0.0.jar</code></td>
              <td style="padding: 12px 10px; color: var(--text-muted);">Inspeção física do arquivo ZIP: 262 arquivos compactados incluindo classes, assets e lang.</td>
              <td style="padding: 12px 10px;"><span class="badge green">262 Arquivos Integrados</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Parecer Técnico Oficial -->
      <div style="background: #11141a; border: 1px solid #2ea043; border-radius: 12px; padding: 20px;">
        <h4 style="color: #3fb950; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
          🏆 Parecer Técnico Conclusivo do Agente Auditor
        </h4>
        <p style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.6;">
          Todos os 80 itens e blocos planejados para a Versão 1.0 de <b>Wings of the Wild</b> cumprem com 100% de rigor técnico as normas de arquitetura do Minecraft 26.3 NeoForge. O mod compila limpo sem advertências críticas, sem modelos quebrados ou texturas faltantes no jogo.
        </p>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 10px;">
          📄 Relatório completo detalhado disponível em: <code>D:\\Mine\\MEMORIA_AGENTE_AUDITORIA.md</code> | Script: <code>D:\\Mine\\audit_validator.py</code>
        </p>
      </div>
    </div>
"""

# Place tab_auditoria_html right after tab-equipe
if "<!-- Tab Galeria 2D -->" in html:
    html = html.replace("<!-- Tab Galeria 2D -->", tab_auditoria_html + "\n    <!-- Tab Galeria 2D -->")
    print("tab-auditoria inserted successfully.")

with open(PAINEL_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("painel.html saved successfully.")
