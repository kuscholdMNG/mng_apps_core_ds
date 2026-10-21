"""DEC-02: where the Cluster Audit web color is close to an app brand color, use the web color.
Usage: python3 scripts/apply_web_alignment.py data/brand-color-resolution.json data/source/cluster-audit-web-colors.json
Rewrites data/brand-color-resolution.json in place (run after resolve_brand_colors.py).

Brand role = navbar, or action for markets whose bar is white/black on both apps (legacy Tribune template).
- Resolved brand role: web within ΔE 0.05 of the chosen value -> web value (evidence 'web-close'); otherwise keep.
- Open brand role: web within ΔE 0.05 of the iOS or Android value -> web value (evidence 'web-close'); otherwise stays open.
- When the brand role is navbar and the app's action equals its navbar (standard template), action follows.
Each change keeps the earlier choice in 'previous'.
"""
import json, sys, math
res_path, web_path = sys.argv[1], sys.argv[2]
R = json.load(open(res_path)); W = {r['code']: r for r in json.load(open(web_path))['rows']}
CLOSE = 0.05
def ch(h): return [int(h[i:i+2], 16) for i in (1, 3, 5)]
def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def ok(h):
    r, g, b = [lin(v/255) for v in ch(h)]
    l=(0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m=(0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s=(0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
dE = lambda a, b: math.dist(ok(a), ok(b))
NEUTRAL = ('#ffffff', '#000000')
log = []
for m in R['markets']:
    w = W.get(m['code'])
    if not w: continue
    web = w['property_color'].lower(); ro = m['roles']
    legacy = ro['navbar']['ios'] in NEUTRAL and ro['navbar']['android'] in NEUTRAL
    brand = 'action' if legacy else 'navbar'
    targets = [brand]
    if brand == 'navbar' and ro['action']['android'] == ro['navbar']['android']: targets.append('action')
    r = ro[brand]
    if r.get('previous') is not None or r['evidence'] == 'web-close':   # already applied
        continue
    if r['value']: d = dE(web, r['value']); hit = d < CLOSE
    else:
        d = min(dE(web, r['ios']), dE(web, r['android'])); hit = d < CLOSE
    entry = {'code': m['code'], 'role': brand, 'web': web, 'before': r['value'], 'dE': round(d, 3), 'applied': hit and r['value'] != web}
    if hit and r['value'] != web:
        for t in targets:
            x = ro[t]; x['previous'] = {'value': x['value'], 'evidence': x['evidence']}
            x['value'] = web; x['evidence'] = 'web-close'
            x['fix'] = 'both' if x['ios'] != web and x['android'] != web else ('ios' if x['android'] == web else ('android' if x['ios'] == web else None))
    log.append(entry)
for m in R['markets']:
    m['status'] = 'resolved' if all(x['value'] for x in m['roles'].values()) else 'open'
R['web_alignment'] = {'rule': 'DEC-02', 'close_dE': CLOSE, 'log': log}
st = {}
for m in R['markets']:
    for x in m['roles'].values(): st[x['evidence']] = st.get(x['evidence'], 0) + 1
R['stats'] = st
json.dump(R, open(res_path, 'w'), indent=1)
print('changed', sum(e['applied'] for e in log), 'kept', sum(not e['applied'] for e in log), st)
