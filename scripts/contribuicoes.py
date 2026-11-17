#!/usr/bin/env python3
"""Renderiza contribuições públicas reais em visual binário, sem valores fictícios."""
import json, urllib.request, html, pathlib, datetime
url='https://github-contributions-api.jogruber.de/v4/Samiihh?y=last'
req=urllib.request.Request(url,headers={'User-Agent':'Samiihh-README-generator'})
with urllib.request.urlopen(req,timeout=30) as resp: data=json.load(resp)
contrib={x['date']:int(x['count']) for x in data['contributions']}
today=datetime.date.today(); start=today-datetime.timedelta(days=364)
start-=datetime.timedelta(days=(start.weekday()+1)%7)
weeks=[]
for week in range(53):
    cells=[]
    for day in range(7):
        d=start+datetime.timedelta(days=week*7+day)
        cells.append(contrib.get(d.isoformat(),0) if d<=today else None)
    weeks.append(cells)
colors=['#15283A','#1C4A67','#167AA1','#22B8D6','#7DEBFA']
body=['<rect width="100%" height="100%" rx="16" fill="#0D1117"/>','<rect x="10" y="10" width="980" height="320" rx="14" fill="#101C2B" stroke="#25445B"/>','<text x="32" y="43" font-size="18" font-weight="bold" font-family="monospace" fill="#38BDF8">$ git contributions --compile --binary</text>','<text x="32" y="66" font-size="12" font-family="monospace" fill="#91A4B8">Cada bloco representa um dia; intensidade = contribuições públicas</text>']
for wi,days in enumerate(weeks):
    for di,count in enumerate(days):
        if count is None: continue
        level=0 if count==0 else 1 if count<=2 else 2 if count<=5 else 3 if count<=9 else 4
        x=32+wi*17.5;y=84+di*29
        body.append(f'<rect x="{x:.1f}" y="{y}" width="15" height="24" rx="3" fill="{colors[level]}"/>')
        body.append(f'<text x="{x+7.5:.1f}" y="{y+16}" font-size="12" font-weight="bold" text-anchor="middle" fill="{("#7895A8" if level==0 else "#051622")}" font-family="monospace">{1 if count else 0}</text>')
# Linha de varredura animada sobre a matriz binária.
# O SVG é regenerado diariamente, portanto o efeito precisa estar neste script.
body.append('<defs><linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE" stop-opacity="0"/><stop offset="0.5" stop-color="#67E8F9" stop-opacity="0.95"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></linearGradient><clipPath id="grid-clip"><rect x="30" y="82" width="932" height="202" rx="4"/></clipPath></defs>')
body.append('<g clip-path="url(#grid-clip)"><rect x="30" y="82" width="932" height="3" fill="url(#scan)" opacity="0.95"><animate attributeName="y" values="82;281;82" dur="6s" repeatCount="indefinite"/></rect><rect x="30" y="82" width="932" height="16" fill="#22D3EE" opacity="0.10"><animate attributeName="y" values="82;265;82" dur="6s" repeatCount="indefinite"/></rect></g>')
body.append(f'<text x="32" y="311" font-size="12" fill="#91A4B8" font-family="monospace">Fonte: contribuições públicas de Samiihh • atualizado em {today.isoformat()}</text>')
out='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="340" viewBox="0 0 1000 340">'+''.join(body)+'</svg>'
pathlib.Path('assets/contribuicoes-binario.svg').write_text(out,encoding='utf-8')
