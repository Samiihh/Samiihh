#!/usr/bin/env python3
"""Gera painéis SVG do README usando dados públicos reais do GitHub."""
import html, json, os, pathlib, urllib.request

USER, API = "Samiihh", "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def github(path):
    headers = {"Accept":"application/vnd.github+json", "User-Agent":f"{USER}-profile-readme", "X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN: headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(f"{API}{path}", headers=headers), timeout=35) as response:
        return json.load(response)

def terminal(title, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="330" viewBox="0 0 520 330" role="img" aria-label="{html.escape(label)}"><style>.m{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.l{{font:12px ui-monospace,SFMono-Regular,Consolas,monospace;fill:#91A4B8}}.v{{font:bold 18px ui-monospace,SFMono-Regular,Consolas,monospace;fill:#E6F7FF}}</style><rect x="1" y="1" width="518" height="328" rx="16" fill="#0C111A" stroke="#28445E" stroke-width="2"/><path d="M1 48H519" stroke="#28445E"/><path d="M17 1H503Q519 1 519 17V48H1V17Q1 1 17 1" fill="#111C29"/><circle cx="23" cy="24" r="6" fill="#FF625D"/><circle cx="43" cy="24" r="6" fill="#FFBF43"/><circle cx="63" cy="24" r="6" fill="#2CCB67"/><text x="260" y="29" text-anchor="middle" class="m" font-size="13" fill="#A7BCD0">{title}</text>{body}</svg>'''

def stats_svg(profile, repos):
    own = [r for r in repos if not r.get("fork")]
    values = [("repositórios",profile["public_repos"]),("seguidores",profile["followers"]),("seguindo",profile["following"]),("estrelas",sum(r["stargazers_count"] for r in own)),("forks",sum(r["forks_count"] for r in own)),("projetos próprios",len(own))]
    rows=[]
    for i,(name,value) in enumerate(values):
        x,y=34+(i%2)*245,160+(i//2)*43
        rows.append(f'<text x="{x}" y="{y}" class="l">{name}</text><text x="{x}" y="{y+22}" class="v">{value}</text>')
    body=f'<text x="28" y="82" class="m" font-size="14" fill="#38BDF8">$ github-stats --user @{USER}</text><text x="28" y="110" class="m" font-size="12" fill="#22D3EE">✓ dados públicos sincronizados</text><path d="M28 127H492" stroke="#1D3348"/>{"".join(rows)}<text x="28" y="307" class="m" font-size="11" fill="#607A91">fonte: api.github.com</text>'
    return terminal("stats.sh",body,f"Estatísticas públicas do GitHub de @{USER}")

def languages_svg(languages):
    colors=["#38BDF8","#22D3EE","#0EA5E9","#67E8F9","#2563EB","#7DD3FC"]
    top=sorted(languages.items(),key=lambda x:x[1],reverse=True)[:6]; total=sum(v for _,v in top) or 1
    bars=[]; rows=[]; cursor=28.0
    for i,(name,value) in enumerate(top):
        pct=value*100/total; width=464*pct/100; y=174+i*21
        bars.append(f'<rect x="{cursor:.2f}" y="126" width="{width+.3:.2f}" height="14" fill="{colors[i]}"/>'); cursor+=width
        rows.append(f'<circle cx="34" cy="{y-4}" r="4" fill="{colors[i]}"/><text x="47" y="{y}" class="m" font-size="13" fill="#DCEAF5">{html.escape(name)}</text><text x="488" y="{y}" text-anchor="end" class="l">{pct:.1f}%</text>')
    body=f'<defs><clipPath id="bar"><rect x="28" y="126" width="464" height="14" rx="7"/></clipPath></defs><text x="28" y="82" class="m" font-size="14" fill="#38BDF8">$ linguist --top 6 --format json</text><text x="28" y="108" class="m" font-size="12" fill="#22D3EE">{{ "owner": "{USER}", "status": "ok" }}</text><g clip-path="url(#bar)">{"".join(bars)}</g>{"".join(rows)}<text x="28" y="307" class="m" font-size="11" fill="#607A91">bytes de código em repositórios públicos próprios</text>'
    return terminal("linguagens.json",body,f"Linguagens públicas mais usadas por @{USER}")

profile=github(f"/users/{USER}"); repos=github(f"/users/{USER}/repos?per_page=100&type=owner&sort=updated"); languages={}
for repo in repos:
    if repo.get("fork"): continue
    for name,size in github(repo["languages_url"].removeprefix(API)).items(): languages[name]=languages.get(name,0)+size
out=pathlib.Path("assets"); out.mkdir(exist_ok=True)
(out/"stats.svg").write_text(stats_svg(profile,repos),encoding="utf-8")
(out/"linguagens.svg").write_text(languages_svg(languages),encoding="utf-8")
print(f"Painéis gerados: {len(repos)} repositórios, {len(languages)} linguagens.")
