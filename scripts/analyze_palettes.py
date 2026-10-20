import json, math, sys, collections
src = sys.argv[1]; out = sys.argv[2]
m = json.load(open(src))
T = m['tokens']; SK = m['styleKeys']
def hx(h): h=h.lstrip('#')[:6]; return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def tohex(c): return '#'+''.join('%02x'%round(max(0,min(1,v))*255) for v in c)
def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def delin(c): return 12.92*c if c<=0.0031308 else 1.055*c**(1/2.4)-0.055
def lum(h): r,g,b=[lin(v) for v in hx(h)]; return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b): la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
def to_oklch(h):
    r,g,b=[lin(v) for v in hx(h)]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; mm=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,mm,s=[v**(1/3) for v in (l,mm,s)]
    L=0.2104542553*l+0.7936177850*mm-0.0040720468*s; A=1.9779984951*l-2.4285922050*mm+0.4505937099*s; B=0.0259040371*l+0.7827717662*mm-0.8086757660*s
    return L, math.hypot(A,B), math.atan2(B,A)
def from_oklch(L,C,H):
    for _ in range(60):
        A=C*math.cos(H); B=C*math.sin(H)
        l=(L+0.3963377774*A+0.2158037573*B)**3; mm=(L-0.1055613458*A-0.0638541728*B)**3; s=(L-0.0894841775*A-1.2914855480*B)**3
        r=4.0767416621*l-3.3077115913*mm+0.2309699292*s; g=-1.2684380046*l+2.6097574011*mm-0.3413193965*s; b=-0.0041960863*l-0.7034186147*mm+1.7076147010*s
        if all(-1e-4<=v<=1+1e-4 for v in (r,g,b)): return tohex([delin(max(0,min(1,v))) for v in (r,g,b)])
        C*=0.95
    return tohex([delin(max(0,min(1,v))) for v in (r,g,b)])
def fix(fg, bg, target, adjust):
    """adjust='fg' or 'bg': move that color's OKLCH lightness minimally until ratio>=target"""
    c = fg if adjust=='fg' else bg; other = bg if adjust=='fg' else fg
    L,C,H = to_oklch(c)
    best=None
    for step in range(1,201):
        for d in (-1,1):
            L2=min(1,max(0,L+d*step*0.005)); h2=from_oklch(L2,C,H)
            if cr(h2,other)>=target+0.05:
                # snap near-black / near-white to pure values when they still pass
                for snap in ('#000000','#ffffff'):
                    if sum(abs(a-b) for a,b in zip(hx(h2),hx(snap)))<0.06 and cr(snap,other)>=target: return snap
                return h2
    return None
def val(mk, name): return mk['values'][T.index(name)]
def sty(mk, name): return mk['style'][SK.index(name)]
PAIRS = [
 # id, label, fg, bg, target, which-to-adjust
 ('nav','Nav title on nav bar', lambda k:k['core']['navtext'], lambda k:k['core']['navbar'], 4.5,'bg'),
 ('tab','Selected tab on tab bar', lambda k:k['core']['tabactive'], lambda k:k['core']['tabbar'], 3.0,'fg'),
 ('tabun','Unselected tab on tab bar', lambda k:val(k,'tabBarUnselectedTintColor'), lambda k:k['core']['tabbar'], 3.0,'fg'),
 ('action','White label on primary button', lambda k:val(k,'paywallPrimaryTextColor'), lambda k:k['core']['action'], 4.5,'bg'),
 ('header','Header text on header band', lambda k:sty(k,'cell-tertiary-headertext'), lambda k:k['core']['header'], 4.5,'bg'),
 ('alert','Banner text on breaking-news', lambda k:val(k,'breakingNewsBannerTextColor'), lambda k:k['core']['alert'], 4.5,'bg'),
]
res=[]
for k in m['markets']:
    row={'code':k['code'],'name':k['name'],'template':k['template'],'core':k['core'],'checks':[]}
    for pid,label,f,b,tgt,adj in PAIRS:
        fg,bg=f(k),b(k)
        if not fg or not bg: continue
        r=cr(fg,bg); ok=r>=tgt
        c={'id':pid,'label':label,'fg':fg,'bg':bg,'ratio':round(r,2),'target':tgt,'pass':ok}
        if not ok:
            nh=fix(fg,bg,tgt,adj)
            if nh is None: c['suggest']=None; row['checks'].append(c); continue
            role={'nav':'navbar','tab':'tabactive','tabun':'tabBarUnselectedTintColor','action':'action','header':'header','alert':'alert'}[pid]
            if pid=='tab' and fg in ('#000000',) and val(k,'tabBarUnselectedTintColor')=='#ffffff':
                # pattern fix: selected becomes white; unselected becomes a dimmed white that still clears 3:1
                bgc=hx(bg); dim=None
                for a in range(30,100):
                    cand=tohex([bgc[i]+(1-bgc[i])*a/100 for i in range(3)])
                    if cr(cand,bg)>=3.05: dim=cand; break
                c['suggest']={'role':'tabactive','from':fg,'to':'#ffffff','ratio':round(cr('#ffffff',bg),2),'also':{'role':'tabBarUnselectedTintColor','from':'#ffffff','to':dim,'ratio':round(cr(dim,bg),2)},'note':'Selected tab is darker than unselected; swap so selected = white, unselected = dimmed white.'}
                row['checks'].append(c); continue
            c['suggest']={'role':role,'from':fg if adj=='fg' else bg,'to':nh,'ratio':round(cr(nh,bg) if adj=='fg' else cr(fg,nh),2)}
        row['checks'].append(c)
    res.append(row)
sets=collections.defaultdict(list)
for r in res: sets[tuple(r['core'][x] for x in ['navbar','navtext','tabbar','tabactive','action','header','alert'])].append(r['code'])
summary={pid:sum(1 for r in res for c in r['checks'] if c['id']==pid and not c['pass']) for pid,*_ in PAIRS}
json.dump({'source':m['source'],'roles':['navbar','navtext','tabbar','tabactive','action','header','alert'],'summary':summary,'palettes':[{'core':dict(zip(['navbar','navtext','tabbar','tabactive','action','header','alert'],k)),'markets':v} for k,v in sorted(sets.items(),key=lambda x:-len(x[1]))],'markets':res},open(out,'w'),indent=1)
print(summary, len(sets))
