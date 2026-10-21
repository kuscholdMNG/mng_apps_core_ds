"""DEC-03: any brand color still unresolved after DEC-01 and DEC-02 takes the iOS value.
Also resolves the remaining shared roles (navtext, tabbar, tabinactive, alert) and records
the platform-only roles (iOS header, Android statusbar), and adds RGB to every value.
Usage: python3 scripts/apply_ios_default.py data/brand-color-resolution.json data/color-platform-comparison.json
Run after resolve_brand_colors.py and apply_web_alignment.py. Rewrites the resolution file in place.
"""
import json, sys
res_path, cmp_path = sys.argv[1:3]
R = json.load(open(res_path)); Cmp = {m['code']: m for m in json.load(open(cmp_path))['markets']}
def rgb(h): return [int(h[i:i+2], 16) for i in (1, 3, 5)] if h else None
def set_ios(x):
    x['previous'] = x.get('previous') or {'value': x['value'], 'evidence': x['evidence']}
    x['value'] = x['ios']; x['evidence'] = 'ios-default'; x['fix'] = 'android' if x['android'] != x['ios'] else None
for m in R['markets']:
    ro = m['roles']; c = Cmp[m['code']]['roles']
    for k in ('navbar', 'action', 'tabactive'):
        if not ro[k]['value']: set_ios(ro[k])
    # tabbar: follows navbar when each app draws its tab bar in its nav bar color; otherwise iOS
    t = c['tabbar']; nb = c['navbar']
    tb = {'ios': t['ios'], 'android': t['android'], 'sheet': None}
    if t['ios'] == nb['ios'] and t['android'] == nb['android']:
        tb.update(value=ro['navbar']['value'], evidence='follows-navbar', fix=ro['navbar']['fix'])
    elif t['ios'] == t['android']: tb.update(value=t['ios'], evidence='agree', fix=None)
    else: tb.update(value=None, evidence='unresolved'); set_ios(tb)
    ro['tabbar'] = tb
    for k in ('navtext', 'tabinactive', 'alert'):
        v = c[k]; x = {'ios': v['ios'], 'android': v['android'], 'sheet': None}
        if v['ios'] == v['android']: x.update(value=v['ios'], evidence='agree', fix=None)
        else: x.update(value=None, evidence='unresolved'); set_ios(x)
        ro[k] = x
    ro['alert']['note'] = 'PLAT-03 proposes one Core value #cf000e (passes 4.5:1); not approved yet'
    co = Cmp[m['code']]
    m['platform_only'] = {'ios': {'header': co['ios_only']['header']}, 'android': {'statusbar': co['android_only']['statusbar']}}
    for x in ro.values():
        for f in ('value', 'ios', 'android', 'sheet'):
            x[f + '_rgb'] = rgb(x.get(f))
    m['status'] = 'resolved' if all(x['value'] for x in ro.values()) else 'open'
st = {}
for m in R['markets']:
    for x in m['roles'].values(): st[x['evidence']] = st.get(x['evidence'], 0) + 1
R['stats'] = st; R['ios_default'] = {'rule': 'DEC-03'}
json.dump(R, open(res_path, 'w'), indent=1)
print(st, 'open markets:', sum(m['status'] == 'open' for m in R['markets']))
