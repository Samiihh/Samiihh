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
body.append(f'<text x="32" y="311" font-size="12" fill="#91A4B8" font-family="monospace">Fonte: contribuições públicas de Samiihh • atualizado em {today.isoformat()}</text>')
out='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="340" viewBox="0 0 1000 340">'+''.join(body)+'</svg>'
pathlib.Path('assets/contribuicoes-binario.svg').write_text(out,encoding='utf-8')
