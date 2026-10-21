"""DEC-05: one breaking-news red for every market and both apps, #cf000e, with white text (WCAG AA).
Usage: python3 scripts/apply_core_alert.py data/brand-color-resolution.json data/source/markets.json
Run after apply_ios_default.py. Sets roles.alert to #cf000e and adds roles.alerttext (#ffffff), and
fails loudly if the pair ever drops below WCAG AA for normal text (4.5:1).
"""
import json, sys
res_path, ios_path = sys.argv[1:3]
R = json.load(open(res_path)); I = json.load(open(ios_path))
ti = I['tokens'].index('breakingNewsBannerTextColor'); IT = {m['code']: m['values'][ti] for m in I['markets']}
RED, TEXT, AA = '#cf000e', '#ffffff', 4.5
def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def lum(h): r, g, b = [lin(int(h[k:k+2], 16)/255) for k in (1, 3, 5)]; return .2126*r + .7152*g + .0722*b
cr = lambda x, y: (max(lum(x), lum(y)) + .05) / (min(lum(x), lum(y)) + .05)
ratio = round(cr(TEXT, RED), 2); assert ratio >= AA, f'{TEXT} on {RED} is {ratio}:1, below WCAG AA'
rgb = lambda h: [int(h[i:i+2], 16) for i in (1, 3, 5)] if h else None
for m in R['markets']:
    a = m['roles']['alert']
    a['previous'] = {'value': a['value'], 'evidence': a['evidence']}
    a.update(value=RED, evidence='core-alert', fix='ios' if a['ios'] != RED else None, value_rgb=rgb(RED),
             contrast={'text': TEXT, 'ratio': ratio, 'wcag': 'AA'}, note='DEC-05: one Core red; fix on iOS ASAP (contrast)')
    it = IT[m['code']]
    m['roles']['alerttext'] = {'ios': it, 'android': None, 'sheet': None, 'value': TEXT, 'evidence': 'core-alert',
        'fix': 'ios' if it != TEXT else None, 'ios_rgb': rgb(it), 'android_rgb': None, 'sheet_rgb': None, 'value_rgb': rgb(TEXT),
        'note': 'Android banner text color not in the export; confirm it is white'}
R['core_alert'] = {'rule': 'DEC-05', 'value': RED, 'text': TEXT, 'ratio': ratio}
st = {}
for m in R['markets']:
    for x in m['roles'].values(): st[x['evidence']] = st.get(x['evidence'], 0) + 1
R['stats'] = st
json.dump(R, open(res_path, 'w'), indent=1)
print(f'alert {RED} + text {TEXT}: {ratio}:1 (AA). iOS text not white in:', [c for c, v in IT.items() if v != TEXT])
