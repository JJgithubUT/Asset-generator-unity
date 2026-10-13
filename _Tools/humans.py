"""Motor de humanoides 64x64 (44 px de alto, pivote Bottom). 3 orientaciones: sur, nor, lat (derecha)."""
import math
import numpy as np
from common import *

LINO = (P['crema'], P['crema'], P['piedra_c'])
CUERO = (P['ocre_m'], P['tierra'], P['tierra_o'])
BOTAS = (P['tierra'], P['tierra_o'], P['K'])
PELO_M = (P['tierra'], P['madera'], P['tierra_o'])


def dark(t):
    return (t[1], t[2], t[2])


def lantern(c, x, y, lit=True):
    """Farol de mano 5x7. (x,y) = esquina sup-izq."""
    frame = (P['tierra'], P['tierra_o'], P['K'])
    c.paint(c.rect(x + 1, y, x + 3, y), frame, k=1)                 # tapa
    c.set(x + 2, y - 1, P['tierra_o'])                               # asa
    c.paint(c.rect(x, y + 1, x + 4, y + 6), frame, k=1)
    glass = c.rect(x + 1, y + 2, x + 3, y + 5)
    c.fill(glass, P['fuego'] if lit else P['piedra_o'])
    if lit:
        c.set(x + 2, y + 3, P['trigo']); c.set(x + 2, y + 4, P['trigo'])


def spear(c, p0, p1, tip=True):
    c.paint(c.line(p0, p1, 1), (P['ocre_m'], P['madera'], P['madera']), k=1)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = max(1, math.hypot(dx, dy))
    ux, uy = dx / n, dy / n
    if tip:
        tx, ty = p1[0], p1[1]
        c.fill(c.line((tx, ty), (tx + ux * 4, ty + uy * 4), 2), P['piedra_c'])
        c.set(int(round(tx + ux * 4)), int(round(ty + uy * 4)), P['crema'])


def arm(c, p0, p1, sleeve, skin, frac=0.78, w=3, hand=True, hand_t=None):
    """brazo = linea gruesa de manga + mano de 3x3 (o 2x2)."""
    q = (p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac)
    c.paint(c.line(p0, q, w), sleeve, k=1)
    if frac < 1:
        c.paint(c.line(q, p1, w), skin, k=1)
    if hand:
        x, y = int(round(p1[0])), int(round(p1[1]))
        c.paint(c.rect(x - 1, y - 1, x + 1, y + 1), hand_t or skin, k=1)


def draw_human(d, po, st):
    """d: 'sur' | 'nor' | 'lat'. po: pose. st: estilo. Devuelve Cv 64x64 con contorno."""
    c = Cv(64, 64)
    dy = po.get('dy', 0)
    up = po.get('up', 0)
    cr = po.get('crouch', 0)
    oy = -up
    stoop = st.get('stoop', 0)
    tw = st.get('tw', 0)
    skin = st.get('skin', T['piel'])
    shirt = st.get('shirt', LINO)
    pants = st.get('pants', T['madera'])
    boots = st.get('boots', BOTAS)
    hair = st.get('hair', PELO_M)
    sleeve = st.get('sleeve', shirt)
    sleeve_frac = st.get('sleeve_frac', 0.78)
    robe = st.get('robe')           # tonos de tunica larga o None
    robe_len = st.get('robe_len', 4)
    hat = st.get('hat')             # funcion(c, d, g)
    hair_style = st.get('hair_style', 'short')
    beard = st.get('beard')         # tonos o None
    stubble = st.get('stubble', False)
    face_extra = st.get('face_extra')
    glove = st.get('glove')
    skirt = st.get('skirt')
    hip_y = 46 + cr + oy
    fb = 62 + oy
    ty0 = 33 + stoop + dy + cr + oy
    hy0 = 21 + stoop + dy + cr + oy
    lf = po.get('lf', (0, 0))
    rf = po.get('rf', (0, 0))
    lh = po.get('lh', (0, 0))
    rh = po.get('rh', (0, 0))
    g = {'ty0': ty0, 'hy0': hy0, 'hip': hip_y, 'fb': fb, 'tw': tw}

    def legs_front():
        for (x0, x1, f) in ((28 - (tw > 1), 31, lf), (33, 36 + (tw > 1), rf)):
            bottom = fb - int(f[1])
            ltop = hip_y - 1
            lbot = bottom - 3
            if lbot >= ltop:
                c.paint(c.rect(x0, ltop, x1, lbot), pants, k=1)
            bx0 = x0 - (1 if x0 < 32 else 0)
            bx1 = x1 + (0 if x0 < 32 else 1)
            c.paint(c.rect(bx0 + int(f[0]), bottom - 3, bx1 + int(f[0]), bottom), boots, k=1)

    def robe_front(hem):
        pts = [(26 - tw, hip_y - 6), (37 + tw, hip_y - 6), (38 + tw, hem), (25 - tw, hem)]
        c.paint(c.poly(pts), robe, k=1)

    if d in ('sur', 'nor'):
        back = d == 'nor'
        legs_front()
        if robe:
            hem = fb - robe_len - (1 if (lf[1] or rf[1]) else 0)
            robe_front(hem)
        if skirt:
            hem = fb - 3 - (1 if (lf[1] or rf[1]) else 0)
            sw = po.get('sway', 0)
            c.paint(c.poly([(26 - tw, hip_y - 5), (37 + tw, hip_y - 5), (39 + tw + sw, hem), (24 - tw + sw, hem)]), skirt, k=1)
        # torso
        x0, x1 = 26 - tw, 37 + tw
        tor = c.poly([(x0 + 1, ty0), (x1 - 1, ty0), (x1, ty0 + 1), (x1, hip_y), (x0, hip_y), (x0, ty0 + 1)])
        if robe:
            c.paint(tor, robe, k=1)
        else:
            c.paint(tor, shirt, k=1)
        g.update(x0=x0, x1=x1, tm=tor)
        st_over = st.get('torso_over')
        if st_over: st_over(c, d, g)
        # cabeza
        head = c.ell(27, hy0, 36, hy0 + 11)
        if back:
            c.paint(head, hair, k=1)
            c.paint(c.rect(29, hy0 + 9, 34, hy0 + 11) & head, skin, k=1)  # nuca
            if hair_style == 'long': c.paint(c.rect(27, hy0 + 6, 36, hy0 + 12), hair, k=1)
        else:
            c.paint(head, skin, k=1)
            top = c.rect(26, hy0 - 1, 37, hy0 + 3) & head
            sides = (c.rect(26, hy0, 27, hy0 + 7) | c.rect(36, hy0, 37, hy0 + 7)) & head
            if hair_style == 'none':
                top = top & False; sides = sides & False
            c.paint(top | sides, hair, k=1)
            if hair_style == 'long':
                c.paint(c.rect(26, hy0 + 4, 27, hy0 + 11) | c.rect(36, hy0 + 4, 37, hy0 + 11), hair, k=1)
            ey = hy0 + 6
            c.set(29, ey, K); c.set(34, ey, K)
            if stubble:
                for xx in range(28, 36):
                    for yy in (hy0 + 8, hy0 + 9, hy0 + 10):
                        if (xx + yy) % 2 == 0 and head[yy, xx]: c.set(xx, yy, P['tierra'])
                c.set(29, ey + 1, P['ocre_m']); c.set(34, ey + 1, P['ocre_m'])   # ojeras
            if beard:
                bm = c.rect(27, hy0 + 8, 36, hy0 + 12) & head
                c.paint(bm, beard, k=1)
                c.set(31, hy0 + 8, skin[1]); c.set(32, hy0 + 8, skin[1])   # boca
            if face_extra: face_extra(c, d, g)
        for tx in st.get('tufts', []): c.set(tx, hy0 - 1, hair[1])
        # sombrero / capucha
        if hat: hat(c, d, g)
        # brazos
        sh_y = ty0 + 2
        arm(c, (24 - tw, sh_y), (24 - tw + lh[0] - 0, 45 + stoop + cr + oy + lh[1] + dy), sleeve, skin, sleeve_frac, hand_t=glove)
        arm(c, (39 + tw, sh_y), (39 + tw + rh[0], 45 + stoop + cr + oy + rh[1] + dy), sleeve, skin, sleeve_frac, hand_t=glove)
        g['hand_l'] = (24 - tw + lh[0], 45 + stoop + cr + oy + lh[1] + dy)
        g['hand_r'] = (39 + tw + rh[0], 45 + stoop + cr + oy + rh[1] + dy)
        if st.get('front_over'): st['front_over'](c, d, g, po)
    else:  # lateral derecha
        # pierna lejana, pierna cercana
        def side_leg(f, tones_p, tones_b):
            bottom = fb - int(f[1])
            fx = 32 + int(f[0])
            top = hip_y - 1
            if bottom - 3 > top:
                c.paint(c.line((32, top), (fx, bottom - 3), 4), tones_p, k=1)
            else:
                c.paint(c.rect(30, top, 33, top + 2), tones_p, k=1)
            c.paint(c.rect(fx - 2, bottom - 3, fx + 3, bottom), tones_b, k=1)
        side_leg(rf, dark(pants), dark(boots))   # lejana = rf
        # brazo lejano
        far_sh = (32, ty0 + 2)
        far_hand = (32 + rh[0] + 0, 45 + stoop + cr + oy + rh[1] + dy)
        if not st.get('far_arm_hidden'):
            arm(c, far_sh, far_hand, dark(sleeve), dark(skin), sleeve_frac, hand_t=dark(glove) if glove else None)
        side_leg(lf, pants, boots)
        if robe:
            hem = fb - robe_len - (1 if (lf[1] or rf[1]) else 0)
            pts = [(28 - tw, hip_y - 6), (36 + tw, hip_y - 6), (37 + tw, hem), (26 - tw, hem)]
            c.paint(c.poly(pts), robe, k=1)
        if skirt:
            hem = fb - 3 - (1 if (lf[1] or rf[1]) else 0)
            c.paint(c.poly([(28 - tw, hip_y - 5), (36 + tw, hip_y - 5), (39 + tw + po.get('sway', 0), hem), (25 - tw + po.get('sway', 0), hem)]), skirt, k=1)
        x0, x1 = 28 - tw, 36 + tw
        tor = c.poly([(x0 + 1, ty0), (x1 - 1, ty0), (x1, ty0 + 1), (x1, hip_y), (x0, hip_y), (x0, ty0 + 1)])
        c.paint(tor, robe if robe else shirt, k=1)
        g.update(x0=x0, x1=x1, tm=tor)
        if st.get('torso_over'): st['torso_over'](c, d, g)
        head = c.ell(28, hy0, 37, hy0 + 11)
        c.paint(head, skin, k=1)
        hairm = (c.rect(27, hy0 - 1, 38, hy0 + 3) | c.rect(27, hy0, 31, hy0 + 8)) & head
        if hair_style == 'none': hairm &= False
        if hair_style == 'long': hairm |= c.rect(27, hy0, 31, hy0 + 12) & c.rect(27, hy0, 33, hy0 + 12)
        c.paint(hairm, hair, k=1)
        c.set(38, hy0 + 7, skin[1])      # nariz
        c.set(36, hy0 + 6, K)            # ojo
        if stubble:
            for xx in range(32, 37):
                for yy in (hy0 + 8, hy0 + 9, hy0 + 10):
                    if (xx + yy) % 2 == 0 and head[yy, xx]: c.set(xx, yy, P['tierra'])
            c.set(36, hy0 + 7, P['ocre_m'])
        if beard:
            bm = c.rect(32, hy0 + 8, 38, hy0 + 12) & head
            c.paint(bm, beard, k=1)
        if face_extra: face_extra(c, d, g)
        for tx in st.get('tufts_lat', []): c.set(tx, hy0 - 1, hair[1])
        if hat: hat(c, d, g)
        near_sh = (32, ty0 + 2)
        near_hand = (32 + lh[0], 45 + stoop + cr + oy + lh[1] + dy)
        arm(c, near_sh, near_hand, sleeve, skin, sleeve_frac, hand_t=glove)
        g['hand_n'] = near_hand
        g['hand_f'] = far_hand
        if st.get('front_over'): st['front_over'](c, d, g, po)
    if st.get('draw_prop'): st['draw_prop'](c, d, g, po)
    if not po.get('no_outline'):
        c.outline()
    return c


# ---------------------------------------------------------------------------------------------
# Generadores de poses
# ---------------------------------------------------------------------------------------------
def idle_poses(n=2, d='sur'):
    return [{'dy': i % 2} if i == 1 else {'dy': 0} for i in range(n)]


def walk_poses(d, n=6, lift=3, swing=2, run=False):
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        if d in ('sur', 'nor'):
            sa = math.sin(t)
            lfi = (0, int(round(max(0, sa) * lift)))
            rfi = (0, int(round(max(0, -sa) * lift)))
            dy = 1 if abs(sa) < 0.35 else 0
            lh = (0, int(round(swing * sa)))
            rh = (0, int(round(-swing * sa)))
            if run:
                lh = (-1 if lh[1] < 0 else 0, lh[1] * 2); rh = (1 if rh[1] < 0 else 0, rh[1] * 2)
            out.append({'dy': dy, 'lf': lfi, 'rf': rfi, 'lh': lh, 'rh': rh})
        else:
            sx = 5 if run else 4
            lfi = (int(round(sx * math.sin(t))), int(round(max(0, math.cos(t)) * lift)))
            rfi = (int(round(-sx * math.sin(t))), int(round(max(0, -math.cos(t)) * lift)))
            dy = 1 if abs(math.cos(t)) < 0.35 else 0
            lh = (int(round(-(5 if run else 4) * math.sin(t))), -1 if run else 0)
            rh = (int(round((5 if run else 4) * math.sin(t))), -1 if run else 0)
            out.append({'dy': dy, 'lf': lfi, 'rf': rfi, 'lh': lh, 'rh': rh})
    return out


def jump_poses(d):
    if d == 'lat':
        arms = [((-3, 1), (-3, 1)), ((3, -6), (4, -5)), ((5, -8), (6, -7)), ((4, -6), (5, -5)), ((-1, 2), (-1, 2))]
    else:
        arms = [((0, 2), (0, 2)), ((-1, -9), (1, -9)), ((-4, -6), (4, -6)), ((-2, -9), (2, -9)), ((0, 3), (0, 3))]
    P_ = [
        dict(crouch=3, dy=0, lf=(0, 0), rf=(0, 0)),
        dict(up=3, crouch=0, lf=(0, 0), rf=(0, 0)),
        dict(up=7, lf=(0, 3), rf=(0, 3)),
        dict(up=4, lf=(0, 0), rf=(0, 0)),
        dict(crouch=3, dy=0, lf=(0, 0), rf=(0, 0)),
    ]
    if d == 'lat':
        P_[2]['lf'] = (4, 4); P_[2]['rf'] = (-3, 2)
        P_[3]['lf'] = (2, 1); P_[3]['rf'] = (-1, 0)
    out = []
    for p, (l, r) in zip(P_, arms):
        p = dict(p); p['lh'] = l; p['rh'] = r
        out.append(p)
    return out
