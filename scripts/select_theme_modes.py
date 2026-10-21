"""DEC-06: pick the 20 markets that get a mode in the Figma 'Brand theme' collection (plan limit: 20 modes).
Usage: python3 scripts/select_theme_modes.py   -> data/figma-theme-modes.json
Rule: the required markets first, then the most visually different market from each cluster not yet covered,
then the most different markets overall until 20. 'Different' = smallest mean OKLab distance to any picked
market across the 6 brand roles (greedy max-min). Decommissioned / not-using apps are skipped.
"""
import json, math
REQUIRED = ['OCR', 'TDP', 'TCCDR', 'SS', 'MC', 'CT', 'TMN', 'TDH', 'TBH']
EXCLUDE = {'BS': 'decommissioned Nov 1 2026', 'TB': 'decommissioned Dec 2024', 'TBCP': 'not using', 'TROT': 'not using'}
LIMIT = 20
NEAR_DUP = 0.03   # a cluster's best pick closer than this to a picked market adds nothing; skip that cluster
d = json.load(open('data/brand-color-resolution.json'))
aud = {r['code']: r['cluster'] for r in json.load(open('data/source/cluster-audit-web-colors.json'))['rows']}
mg = {r[1].upper(): r[2].strip() for r in json.load(open('data/source/migration-sheet-brand-colors.json'))['rows']}
def cl(c):
    a = aud.get(c); m = mg.get(c, '')
    if a == 'TRIB' or m in ('TripPub', 'Tribune'): return 'Tribune'
    return a or m or None
R = ['navbar', 'navtext', 'tabbar', 'tabactive', 'tabinactive', 'action']
P = {m['code']: [m['roles'][r]['value'] for r in R] for m in d['markets']}; N = {m['code']: m['name'] for m in d['markets']}
def ch(h): return [int(h[i:i+2], 16) for i in (1, 3, 5)]
def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def ok(h):
    r, g, b = [lin(v/255) for v in ch(h)]
    l=(0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m=(0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s=(0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
dist = lambda a, b: sum(math.dist(ok(P[a][i]), ok(P[b][i])) for i in range(len(R))) / len(R)
sel = list(REQUIRED); why = {c: 'required' for c in REQUIRED}; skipped = {}
best = lambda cands: max(cands, key=lambda c: (min(dist(c, s) for s in sel), c))
for k in sorted({cl(c) for c in P if c not in EXCLUDE and cl(c)}):
    if k in {cl(c) for c in sel}: continue
    c = best([c for c in P if cl(c) == k and c not in EXCLUDE])
    if min(dist(c, s) for s in sel) < NEAR_DUP: skipped[k] = c; continue
    sel.append(c); why[c] = f'covers cluster {k}'
while len(sel) < LIMIT:
    c = best([c for c in P if c not in sel and c not in EXCLUDE]); sel.append(c); why[c] = 'most different remaining'
out = [{'code': c, 'name': N[c], 'cluster': cl(c), 'why': why[c], 'nearest': min((s for s in sel if s != c), key=lambda s: dist(c, s)),
        'nearest_dE': round(min(dist(c, s) for s in sel if s != c), 3)} for c in sel]
json.dump({'rule': 'DEC-06', 'limit': LIMIT, 'excluded': EXCLUDE, 'modes': out, 'clusters_skipped_as_duplicates': skipped,
           'no_cluster': sorted(c for c in P if not cl(c))}, open('data/figma-theme-modes.json', 'w'), indent=1)
for o in out: print(o['code'], o['why'], o['nearest'], o['nearest_dE'])
