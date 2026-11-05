# Category illustrations (1200x630 SVG). Run: python3 _build/illust.py
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
G, GD, GS, GL = '#0e4a3f', '#0b3a31', '#cfe0d9', '#e6efeb'
A, AL, W, INK, MU, LN = '#d9a441', '#f3dfb4', '#ffffff', '#1b1f23', '#8a949b', '#d5dbdf'
SH = 'filter="url(#sh)"'

def wrap(body, bg='#eef3f0'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img">
<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0b3a31" flood-opacity=".14"/></filter></defs>
<rect width="1200" height="630" fill="{bg}"/>
<circle cx="1040" cy="90" r="230" fill="{GL}"/><circle cx="140" cy="560" r="170" fill="{GL}"/>
<circle cx="1090" cy="520" r="34" fill="{AL}"/><circle cx="150" cy="120" r="18" fill="{AL}"/>
<g fill="{GS}">{''.join(f'<circle cx="{960+x*26}" cy="{300+y*26}" r="4"/>' for x in range(5) for y in range(4))}</g>
{body}
</svg>'''

def lines(x, y, w, n, gap=28, c=LN, last=.6):
    return ''.join(f'<rect x="{x}" y="{y+i*gap}" width="{w if i < n-1 else w*last:.0f}" height="10" rx="5" fill="{c}"/>' for i in range(n))

def paper(x, y, w, h, extra=''):
    return f'<g {SH}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{W}"/></g>{extra}'

def check(cx, cy, r, fill=G):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/><path d="M{cx-r*.42} {cy+r*.02} l{r*.3} {r*.3} l{r*.55} -{r*.6}" fill="none" stroke="{W}" stroke-width="{r*.22:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'

def coins(x, y, n=4):
    s = ''
    for i in range(n):
        yy = y - i*22
        s += f'<ellipse cx="{x}" cy="{yy+12}" rx="62" ry="20" fill="#b8862b"/><rect x="{x-62}" y="{yy-8}" width="124" height="20" fill="#b8862b"/><ellipse cx="{x}" cy="{yy-8}" rx="62" ry="20" fill="{A}"/>'
    return s

# 1 실손의료비: receipt, cross badge, coins, capsule
def c1():
    zig = ''.join(f'L{730-i*30-15} 522 L{730-i*30-30} 505 ' for i in range(10))
    rec = f'<g {SH}><path d="M430 110 H730 V505 {zig}Z" fill="{W}"/></g>'
    rec += f'<rect x="470" y="150" width="140" height="16" rx="8" fill="{INK}"/>' + lines(470, 200, 220, 5, 32) 
    rec += f'<rect x="470" y="380" width="220" height="2" fill="{LN}"/><rect x="470" y="410" width="80" height="14" rx="7" fill="{MU}"/><rect x="590" y="400" width="100" height="32" rx="8" fill="{A}"/>'
    cross = f'<g {SH}><circle cx="330" cy="250" r="92" fill="{G}"/></g><rect x="312" y="200" width="36" height="100" rx="8" fill="{W}"/><rect x="280" y="232" width="100" height="36" rx="8" fill="{W}"/>'
    cap = f'<g transform="rotate(-30 330 450)"><rect x="270" y="425" width="120" height="50" rx="25" fill="{W}" {SH}/><path d="M330 425 h35 a25 25 0 0 1 0 50 h-35z" fill="{A}"/></g>'
    return rec + cross + cap + coins(850, 470, 5) + check(900, 220, 46)

# 2 진단비·특약: clipboard with pulse, stethoscope, shield
def c2():
    cb = paper(420, 120, 330, 420) + f'<rect x="530" y="96" width="110" height="50" rx="12" fill="{GD}"/>'
    cb += f'<rect x="460" y="190" width="250" height="120" rx="12" fill="{GL}"/><path d="M470 255 H540 L560 215 L585 295 L610 235 L625 255 H700" fill="none" stroke="{G}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    cb += lines(460, 345, 250, 4, 34) + check(700, 490, 30, A)
    st = f'<path d="M300 170 v120 a70 70 0 0 0 140 0" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M370 360 v60 a60 60 0 0 1 -120 0 v-20" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><circle cx="250" cy="390" r="30" fill="{A}" stroke="{INK}" stroke-width="10"/><circle cx="300" cy="165" r="10" fill="{INK}"/><circle cx="440" cy="165" r="10" fill="{INK}"/>'
    sh = f'<g {SH}><path d="M880 170 l110 40 v90 c0 80 -50 130 -110 160 c-60 -30 -110 -80 -110 -160 v-90z" fill="{G}"/></g><path d="M840 320 l30 30 l60 -65" fill="none" stroke="{W}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    return st + cb + sh

# 3 보험 구조 이해: policy doc with blocks + magnifier
def c3():
    d = paper(380, 100, 380, 450) + f'<rect x="420" y="140" width="160" height="18" rx="9" fill="{INK}"/>'
    for i, (w, c) in enumerate([(300, G), (220, A), (260, GS)]):
        y = 190 + i*110
        d += f'<rect x="420" y="{y}" width="12" height="80" rx="6" fill="{c}"/>' + lines(450, y+8, w, 3, 26)
    mg = f'<g {SH}><circle cx="760" cy="380" r="110" fill="{W}" fill-opacity=".55" stroke="{GD}" stroke-width="22"/></g><rect x="830" y="455" width="40" height="140" rx="18" fill="{GD}" transform="rotate(-45 850 525)"/>'
    mg += f'<rect x="700" y="360" width="120" height="14" rx="7" fill="{G}"/><rect x="700" y="390" width="80" height="14" rx="7" fill="{A}"/>'
    side = f'<g {SH}><rect x="190" y="200" width="150" height="190" rx="16" fill="{G}"/></g>' + lines(215, 235, 100, 4, 34, '#5f8f83') + check(265, 420, 34, A)
    return side + d + mg

# 4 리모델링·보장 분석: old doc -> new doc, chart
def c4():
    old = f'<g {SH}><rect x="170" y="170" width="260" height="330" rx="16" fill="#f4f5f5"/></g>' + lines(205, 215, 190, 6, 34, '#dde1e3')
    old += f'<circle cx="400" cy="200" r="38" fill="#c9cfd3"/><path d="M385 185 l30 30 M415 185 l-30 30" stroke="{W}" stroke-width="9" stroke-linecap="round"/>'
    arr = f'<path d="M470 335 h150" stroke="{A}" stroke-width="18" stroke-linecap="round"/><path d="M600 300 l40 35 l-40 35" fill="none" stroke="{A}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    new = paper(680, 130, 320, 400) + f'<rect x="715" y="170" width="140" height="16" rx="8" fill="{INK}"/>'
    for i, (h, c) in enumerate([(90, GS), (150, G), (120, G), (190, A)]):
        new += f'<rect x="{730+i*62}" y="{420-h}" width="40" height="{h}" rx="8" fill="{c}"/>'
    new += f'<rect x="715" y="430" width="250" height="3" fill="{LN}"/>' + lines(715, 455, 230, 2, 28) + check(990, 140, 44)
    return old + arr + new

# 5 가족·연령별: umbrella over family
def c5():
    um = f'<path d="M300 300 a300 210 0 0 1 600 0 q-50 -35 -100 0 q-50 -35 -100 0 q-50 -35 -100 0 q-50 -35 -100 0 q-50 -35 -100 0 q-50 -35 -100 0z" fill="{G}" {SH}/><path d="M600 300 a100 210 0 0 1 0 -210 a100 210 0 0 1 0 210" fill="#1d6656"/><rect x="594" y="70" width="12" height="40" rx="6" fill="{GD}"/>'
    def person(x, base, s, body, skin='#f2c9a5'):
        return f'<rect x="{x-38*s}" y="{base-150*s}" width="{76*s}" height="{150*s}" rx="{36*s}" fill="{body}"/><circle cx="{x}" cy="{base-190*s}" r="{34*s}" fill="{skin}"/>'
    fam = person(450, 560, 1.15, GD) + person(560, 560, 1.05, A) + person(665, 560, .78, '#5f8f83') + person(750, 560, .62, '#c98a3a')
    fam += f'<rect x="300" y="556" width="600" height="8" rx="4" fill="{GS}"/>'
    return f'<g transform="translate(0 -45)">{um}</g>' + fam + check(930, 420, 40, A)

# 6 상품별 가이드: fanned cards with icons + shield
def c6():
    def card(rot, fill, icon):
        return f'<g transform="translate({rot*5} {abs(rot)*1.5}) rotate({rot} 600 600)"><g {SH}><rect x="480" y="150" width="240" height="330" rx="20" fill="{fill}"/></g>{icon}</g>'
    heart = f'<path d="M600 300 c-60 -45 -70 -95 -30 -110 c18 -7 30 3 30 18 c0 -15 12 -25 30 -18 c40 15 30 65 -30 110z" fill="{A}"/>' + lines(530, 360, 140, 3, 28, '#5f8f83')
    car = f'<rect x="530" y="250" width="140" height="50" rx="14" fill="{G}"/><path d="M555 250 l18 -35 h54 l18 35z" fill="{G}"/><circle cx="565" cy="305" r="16" fill="{INK}"/><circle cx="635" cy="305" r="16" fill="{INK}"/>' + lines(530, 360, 140, 3, 28)
    house = f'<path d="M530 270 l70 -60 l70 60 v70 h-140z" fill="{A}"/><rect x="585" y="295" width="30" height="45" fill="{W}"/>' + lines(530, 370, 140, 3, 28)
    s = card(-16, W, car.replace('y="360"', 'y="360"')) + card(16, W, house) + card(0, G, heart)
    return s + check(880, 210, 44, A) + check(320, 210, 30)

# 7 보험금 청구: phone, docs, coins
def c7():
    docs = f'<g {SH}><rect x="200" y="200" width="250" height="320" rx="16" fill="{W}" transform="rotate(-8 325 360)"/></g><g {SH}><rect x="240" y="170" width="250" height="320" rx="16" fill="{W}"/></g>' + f'<rect x="275" y="210" width="110" height="16" rx="8" fill="{INK}"/>' + lines(275, 255, 180, 6, 32)
    ph = f'<g {SH}><rect x="560" y="90" width="230" height="450" rx="36" fill="{GD}"/></g><rect x="578" y="130" width="194" height="370" rx="18" fill="{W}"/><rect x="640" y="104" width="70" height="10" rx="5" fill="#2c5a50"/>'
    ph += check(675, 250, 52) + f'<rect x="610" y="330" width="130" height="14" rx="7" fill="{INK}"/>' + lines(610, 365, 130, 2, 28) + f'<rect x="610" y="440" width="130" height="38" rx="10" fill="{A}"/>'
    arr = f'<path d="M820 320 q50 -60 100 0" fill="none" stroke="{A}" stroke-width="14" stroke-linecap="round"/><path d="M905 290 l18 32 l-35 6" fill="none" stroke="{A}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
    return docs + ph + arr + coins(960, 500, 4)

# 8 가입·계약 제도: contract, signature, pen, stamp, calendar
def c8():
    d = paper(330, 90, 400, 470) + f'<rect x="375" y="135" width="200" height="18" rx="9" fill="{INK}"/>' + lines(375, 185, 310, 7, 32)
    d += f'<rect x="375" y="435" width="160" height="2" fill="{MU}"/><path d="M385 420 c20 -40 35 -40 40 -5 c5 30 25 -30 40 -10 c10 15 20 10 35 -5" fill="none" stroke="{G}" stroke-width="6" stroke-linecap="round"/>'
    d += f'<circle cx="640" cy="470" r="50" fill="none" stroke="{A}" stroke-width="8"/><circle cx="640" cy="470" r="34" fill="none" stroke="{A}" stroke-width="4"/><rect x="615" y="463" width="50" height="14" rx="7" fill="{A}"/>'
    pen = f'<g transform="rotate(35 800 330)" {SH}><rect x="780" y="150" width="40" height="260" rx="14" fill="{GD}"/><path d="M780 410 h40 l-20 50z" fill="{A}"/><rect x="780" y="190" width="40" height="18" fill="{A}"/></g>'
    cal = f'<g {SH}><rect x="150" y="230" width="150" height="150" rx="16" fill="{W}"/></g><rect x="150" y="230" width="150" height="40" rx="16" fill="{G}"/><rect x="150" y="254" width="150" height="16" fill="{G}"/>'
    cal += ''.join(f'<rect x="{170+x*38}" y="{290+y*30}" width="24" height="18" rx="5" fill="{A if (x,y)==(1,1) else GL}"/>' for x in range(3) for y in range(3))
    return cal + d + pen

for i, f in enumerate([c1, c2, c3, c4, c5, c6, c7, c8], 1):
    open(os.path.join(OUT, f'cat-{i}.svg'), 'w', encoding='utf-8').write(wrap(f()))
print('ok')
