#!/usr/bin/env python3
"""Gera terminal SVG animado com contribuições públicas reais de Samiihh."""
import datetime as dt
import html
import json
import pathlib
import urllib.request

USER = 'Samiihh'
API = f'https://github-contributions-api.jogruber.de/v4/{USER}?y=last'
request = urllib.request.Request(API, headers={'User-Agent': 'Samiihh-profile-README/1.0'})
with urllib.request.urlopen(request, timeout=35) as response:
    payload = json.load(response)
counts = {item['date']: int(item['count']) for item in payload['contributions']}
today = dt.date.today()
# 53 semanas, alinhadas de domingo a sábado, com dias futuros vazios.
start = today - dt.timedelta(days=364)
start -= dt.timedelta(days=(start.weekday() + 1) % 7)
weeks = []
for w in range(53):
    weeks.append([(start + dt.timedelta(days=w * 7 + d), counts.get((start + dt.timedelta(days=w * 7 + d)).isoformat(), 0)) for d in range(7)])

W, H = 1060, 350
left, top, dx, dy = 83, 137, 17.5, 19
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribuições públicas em binário de @{USER}, com varredura azul animada">',
'''<defs>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE" stop-opacity="0"/><stop offset="1" stop-color="#22D3EE" stop-opacity=".34"/></linearGradient>
<clipPath id="matrix"><rect x="82" y="129" width="935" height="139"/></clipPath>
</defs>
<rect x="1" y="1" width="1058" height="348" rx="17" fill="#0C111A" stroke="#2A3B50" stroke-width="2"/>
<path d="M1 47H1059" stroke="#263749"/>
<path d="M18 1H1042Q1059 1 1059 18V47H1V18Q1 1 18 1" fill="#171F2B"/>
<circle cx="24" cy="24" r="6" fill="#FF625D"/><circle cx="43" cy="24" r="6" fill="#FFBF43"/><circle cx="62" cy="24" r="6" fill="#2CCB67"/>
<text x="530" y="29" text-anchor="middle" font-size="13" fill="#9CAFC3" font-family="monospace">contribuicoes.bin — compilando @Samiihh</text>
<text x="24" y="84" font-size="15" fill="#3AD5F5" font-weight="bold" font-family="monospace">$ git log --since="1 ano" | compilar --binario</text>
''']
months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
last_month = None
for w, days in enumerate(weeks):
    d = days[0][0]
    if d.month != last_month:
        if w < 50:
            parts.append(f'<text x="{left + w * dx:.1f}" y="118" font-size="11" fill="#A2B5C8" font-family="monospace">{months[d.month-1]}</text>')
        last_month = d.month
for row, label in [(0, 'dom'), (2, 'ter'), (4, 'qui'), (6, 'sáb')]:
    parts.append(f'<text x="27" y="{top + row * dy}" font-size="11" fill="#91A6B8" font-family="monospace">{label}</text>')
valid_total = 0
for w, days in enumerate(weeks):
    for row, (date, count) in enumerate(days):
        if date > today or date < today - dt.timedelta(days=364):
            continue
        valid_total += count
        active = count > 0
        color = '#67E8F9' if count >= 4 else '#2FC9F0' if active else '#33465A'
        parts.append(f'<text x="{left + w*dx:.1f}" y="{top + row*dy}" font-size="12" font-family="monospace" fill="{color}" opacity="{1 if active else .62}">{1 if active else 0}</text>')
parts.append('''<g clip-path="url(#matrix)">
<rect x="82" y="129" width="38" height="139" fill="url(#beam)"><animate attributeName="x" values="44;1017;44" dur="8s" repeatCount="indefinite"/></rect>
<rect x="82" y="129" width="3" height="139" fill="#42E5F8" opacity=".95"><animate attributeName="x" values="82;1017;82" dur="8s" repeatCount="indefinite"/></rect>
</g>
<text x="25" y="300" fill="#A6B9CC" font-size="13" font-family="monospace">[</text>
<rect x="38" y="288" width="736" height="13" rx="3" fill="#1D2938"/>
<rect x="38" y="288" width="736" height="13" rx="3" fill="#29BFEA"><animate attributeName="width" values="0;736;736" keyTimes="0;0.83;1" dur="8s" repeatCount="indefinite"/></rect>
<text x="783" y="300" fill="#A6B9CC" font-size="13" font-family="monospace">]</text>
<text x="805" y="300" fill="#43DDF6" font-size="13" font-family="monospace">compilando...</text>
''')
parts.append(f'<text x="25" y="329" font-size="13" font-family="monospace" fill="#65E6F4">✓ {valid_total} contribuições compiladas · 0 erros · 0 warnings</text>')
parts.append('</svg>')
out = pathlib.Path('assets/contribuicoes-binario.svg')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(''.join(parts), encoding='utf-8')
print(f'Gerado {out} com {valid_total} contribuições públicas no período.')
