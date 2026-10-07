with open("D:/Mine/painel.html", "r", encoding="utf-8") as f:
    text = f.read()

# Update tab-equipe Agente 2
old_agent2_tag = '<span class="status-tag status-done">SUÍTE DE ANIMAÇÃO ENTREGUE (10/10)</span>'
new_agent2_tag = '<span class="status-tag status-done">ENTIDADE JAVA & GECKOLIB REGISTRADA NO JOGO</span>'

if old_agent2_tag in text:
    text = text.replace(old_agent2_tag, new_agent2_tag)
    print("[+] Tag updated in painel.html")

append_info = """            <br>• <b>Invocação no Jogo (/summon wingsofthewild:flamefang):</b> Entidade Java registrada em <code>ModEntities.java</code>, classe <code>FlamefangEntity.java</code> com GeoEntity, atributos épicos (120 HP, 12 Dano, 8 Armadura, 0.6 Voo), modelo <code>FlamefangModel.java</code>, renderizador <code>FlamefangRenderer.java</code> e registro no mod principal <code>WingsOfTheWild.java</code>. Compilado e pronto no JAR!"""

if "Nova Suíte Completa de Animações" in text and "Invocação no Jogo" not in text:
    text = text.replace("          </div>\n        </div>\n\n        <div class=\"kpi-card\" style=\"border-color: #a371f7;\">", append_info + "\n          </div>\n        </div>\n\n        <div class=\"kpi-card\" style=\"border-color: #a371f7;\">")
    print("[+] Entity info appended in painel.html")

with open("D:/Mine/painel.html", "w", encoding="utf-8") as f:
    f.write(text)
print("[SUCCESS] painel.html updated!")
