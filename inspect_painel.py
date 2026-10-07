import re

with open(r"D:\Mine\painel.html", "r", encoding="utf-8") as f:
    content = f.read()

headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', content, re.DOTALL)
print("Headings in painel.html:")
for h in headings:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    print(f" - {clean.encode('ascii', 'replace').decode('ascii')}")

cards = re.findall(r'class=[\"\']kpi-card[\"\'][^>]*>(.*?)</div>', content, re.DOTALL)
print(f"\nTotal KPI cards: {len(cards)}")
