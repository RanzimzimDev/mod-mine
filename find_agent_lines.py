with open(r"D:\Mine\painel.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Agente 1" in line or "Agente 2" in line or "Agente 3" in line:
        print(f"Line {i+1}: {ascii(line.strip()[:80])}")
