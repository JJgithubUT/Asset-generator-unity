"""Estilos de los personajes humanos (PJ-01, PJ-04..PJ-13, EN-01)."""
from humans import *

# ---------------- utilidades de prenda ----------------
def hat_wide(tones, brim=(22, 41), crown=(28, 35), crown_h=5, brim_dy=1, brim_h=4, band=None):
    def f(c, d, g):
        hy0 = g['hy0']
        if d == 'lat':
            b0, b1 = brim[0] + 1, brim[1] + 2
            cr0, cr1 = crown[0], crown[1] + 1
        else:
            b0, b1, cr0, cr1 = brim[0], brim[1], crown[0], crown[1]
        cm = c.poly([(cr0, hy0 + 2), (cr0, hy0 - crown_h + 2), (cr0 + 1, hy0 - crown_h), (cr1 - 1, hy0 - crown_h),
                     (cr1, hy0 - crown_h + 2), (cr1, hy0 + 2)])
        c.paint(c.ell(b0, hy0 + brim_dy - 1, b1, hy0 + brim_dy + brim_h - 1), tones, k=1)
        c.paint(cm, tones, k=1)
        if band:
            c.fill(c.rect(cr0, hy0 - 0, cr1, hy0 + 1), band)
    return f


def hat_cap(tones):
    def f(c, d, g):
        hy0 = g['hy0']
        x0, x1 = (27, 36) if d != 'lat' else (28, 38)
        c.paint(c.ell(x0, hy0 - 2, x1, hy0 + 5) & c.rect(x0, hy0 - 2, x1, hy0 + 3), tones, k=1)
        if d == 'lat': c.paint(c.rect(36, hy0 + 2, 40, hy0 + 3), tones, k=1)   # visera
        elif d == 'sur': c.paint(c.rect(28, hy0 + 3, 35, hy0 + 3), tones, k=1)
    return f


def hat_kerchief(tones):
    def f(c, d, g):
        hy0 = g['hy0']
        if d == 'lat':
            c.paint(c.ell(27, hy0 - 1, 38, hy0 + 8) & c.rect(27, hy0 - 1, 38, hy0 + 4), tones, k=1)
            c.paint(c.rect(27, hy0 + 3, 31, hy0 + 11), tones, k=1)
        else:
            c.paint(c.ell(26, hy0 - 1, 37, hy0 + 8) & c.rect(26, hy0 - 1, 37, hy0 + 3), tones, k=1)
            c.paint(c.rect(26, hy0 + 3, 27, hy0 + 11) | c.rect(36, hy0 + 3, 37, hy0 + 11), tones, k=1)
            if d == 'nor': c.paint(c.ell(26, hy0 - 1, 37, hy0 + 11), tones, k=1)
    return f


def hood(tones):
    def f(c, d, g):
        hy0, ty0 = g['hy0'], g['ty0']
        if d == 'lat':
            m = c.poly([(27, ty0 + 3), (28, hy0 - 1), (34, hy0 - 3), (38, hy0 + 2), (36, hy0 + 4), (33, hy0 + 5),
                        (36, ty0 + 3)])
            c.paint(m, tones, k=1)
            c.fill(c.rect(33, hy0 + 5, 37, hy0 + 11) & ~m, T['piel'][1]) if False else None
            # cara en sombra dentro de la capucha
            c.paint(c.rect(34, hy0 + 5, 37, hy0 + 8), (P['K'], P['K'], P['K']), k=1)
            c.set(36, hy0 + 6, P['c_amar'] if False else P['crema'])
        else:
            m = c.poly([(25, ty0 + 3), (26, hy0 + 1), (28, hy0 - 2), (35, hy0 - 2), (37, hy0 + 1), (38, ty0 + 3),
                        (36, ty0 + 1), (27, ty0 + 1)])
            c.paint(m, tones, k=1)
            if d == 'sur':
                c.paint(c.rect(28, hy0 + 2, 35, hy0 + 10), (P['K'], P['K'], P['K']), k=1)
                c.set(30, hy0 + 6, P['crema']); c.set(33, hy0 + 6, P['crema'])
    return f


def helmet(tones, plume=None):
    def f(c, d, g):
        hy0 = g['hy0']
        x0, x1 = (27, 36) if d != 'lat' else (28, 38)
        c.paint(c.ell(x0, hy0 - 2, x1, hy0 + 6) & c.rect(x0, hy0 - 2, x1, hy0 + 3), tones, k=1)
        if d == 'sur':
            c.paint(c.rect(31, hy0 + 3, 32, hy0 + 7), tones, k=1)       # nasal
        if plume:
            c.paint(c.rect(31, hy0 - 5, 32, hy0 - 2) if d != 'lat' else c.rect(32, hy0 - 5, 34, hy0 - 2), plume, k=1)
    return f


def belt_over(shirt_over=None, apron=None, vest=None, belt=P['tierra_o'], v_cut=True):
    """Superposiciones de torso: chaleco, delantal y cinto."""
    def f(c, d, g):
        ty0, hip, x0, x1, tm = g['ty0'], g['hip'], g['x0'], g['x1'], g['tm']
        if vest:
            if d == 'sur':
                v = tm & ~c.poly([(30, ty0 - 1), (33, ty0 - 1), (32, ty0 + 7), (31, ty0 + 7)])
                c.paint(v, vest, k=1)
            elif d == 'nor':
                c.paint(tm, vest, k=1)
            else:
                c.paint(tm & c.rect(x0 + 2, ty0, x1, hip), vest, k=1)
        if apron:
            if d == 'lat':
                c.paint(c.rect(x1 - 3, ty0 + 6, x1 + 1, hip + 5), apron, k=1)
            elif d == 'sur':
                c.paint(c.rect(28, ty0 + 5, 35, hip + 5), apron, k=1)
        if belt is not None:
            c.fill(c.rect(x0, hip - 1, x1, hip) & tm, belt)
            if d == 'sur': c.set(31, hip - 1, P['trigo']); c.set(32, hip - 1, P['trigo'])
            if d == 'lat': c.set(x1 - 1, hip - 1, P['trigo'])
    return f


def mercader_prop(c, d, g, po):
    hip = g['hip']
    if po.get('swing'):
        sx, sy = po['swing']
        hx, hy = g['hand_r'] if d in ('sur', 'nor') else g['hand_n']
        lantern(c, int(hx + sx) - 2, int(hy + sy))
        return
    if po.get('nobelt'): return
    if d == 'sur': lantern(c, 27, hip - 2)
    elif d == 'nor': lantern(c, 34, hip - 2)
    else: lantern(c, 33, hip - 2)


def mercader_style():
    return dict(
        hair=PELO_M, stubble=True, shirt=LINO, sleeve=LINO, pants=T['madera'], boots=BOTAS,
        tufts=[28, 30, 31, 34], tufts_lat=[29, 31, 32, 35],
        torso_over=belt_over(vest=T['ocre'], apron=CUERO),
        draw_prop=mercader_prop)


def mercader_poses():
    P_ = {}
    for d in ('sur', 'nor', 'lat'):
        idle = [{}, {'dy': 1}]
        run = walk_poses(d, 6, lift=4, swing=3, run=True)
        if d == 'sur':
            atk = [dict(rh=(3, -16), swing=(0, -6), nobelt=1, dy=0),
                   dict(rh=(-4, 6), swing=(1, 3), nobelt=1, dy=1),
                   dict(rh=(-1, 3), swing=(1, 4), nobelt=1, dy=1),
                   dict(rh=(0, 0), swing=(0, 1), nobelt=1, dy=0)]
        elif d == 'nor':
            atk = [dict(rh=(2, 5), swing=(0, 4), nobelt=1),
                   dict(rh=(1, -14), swing=(0, -8), nobelt=1),
                   dict(rh=(1, -8), swing=(0, -4), nobelt=1),
                   dict(rh=(0, 0), swing=(0, 1), nobelt=1)]
        else:
            atk = [dict(lh=(-9, -8), swing=(-2, 2), nobelt=1),
                   dict(lh=(12, 2), swing=(5, 3), nobelt=1, dy=1),
                   dict(lh=(9, 4), swing=(3, 4), nobelt=1, dy=1),
                   dict(lh=(2, 0), swing=(0, 3), nobelt=1)]
        P_[d] = dict(idle=idle, correr=run, atacar=atk, saltar=jump_poses(d))
    return P_


# =============================== NPC y clientes ===============================
def hammer_prop(c, d, g, po):
    hx, hy = g['hand_r']
    v = po.get('hammer', (0, -1))
    ex, ey = hx + v[0] * 9, hy + v[1] * 9
    c.paint(c.line((hx, hy), (ex, ey), 1), (P['ocre_m'], P['madera'], P['madera']), k=1)
    c.paint(c.rect(int(ex) - 3, int(ey) - 2, int(ex) + 3, int(ey) + 2), T['piedra_d'], k=1)


def basket_prop(c, d, g, po):
    hx, hy = g['hand_l']
    x, y = int(hx) - 3, int(hy) + 1
    c.paint(c.rect(x, y, x + 7, y + 5), T['ocre'], k=1)
    for i in range(3): c.set(x + 1 + i * 2, y - 1, P['fol_c']); c.set(x + 2 + i * 2, y - 2, P['fol_m'])
    c.fill(c.rect(x, y + 2, x + 7, y + 2), P['tierra'])


def spear_prop(idle_vec=(0, 10, 0, -28)):
    def f(c, d, g, po):
        hx, hy = (g['hand_r'] if d in ('sur', 'nor') else g['hand_n'])
        v = po.get('spear', idle_vec)
        spear(c, (hx + v[0], hy + v[1]), (hx + v[2], hy + v[3]))
    return f


def insignia(c, d, g):
    if d != 'sur': return
    ty0 = g['ty0']
    c.fill(c.poly([(31, ty0 + 3), (33, ty0 + 6), (31, ty0 + 9), (29, ty0 + 6)]), P['trigo'])
    c.set(31, ty0 + 6, P['crema'])


def breastplate(c, d, g):
    ty0, hip, x0, x1, tm = g['ty0'], g['hip'], g['x0'], g['x1'], g['tm']
    if d == 'lat':
        c.paint(tm & c.rect(x0, ty0, x1, hip - 4), T['piedra'], k=1)
    else:
        c.paint(tm & c.rect(x0, ty0, x1, hip - 4), T['piedra'], k=1)
    c.fill(c.rect(x0, hip - 2, x1, hip - 1) & tm, P['tierra_o'])


def tomas_style():
    return dict(shirt=T['ocre'], sleeve=T['ocre'], pants=T['tierra'], boots=BOTAS, hair=PELO_M, stubble=True,
                hat=hat_wide(T['paja'], brim=(21, 42), crown=(28, 35), crown_h=5, band=P['tierra']),
                torso_over=belt_over(apron=(P['crema'], P['piedra_c'], P['piedra_m']), belt=P['tierra_o']))


def bruno_style():
    gris = (P['piedra_c'], P['piedra_m'], P['piedra_o'])
    return dict(tw=2, shirt=LINO, sleeve=LINO, sleeve_frac=0.35, pants=T['maderat'], boots=BOTAS, hair=gris,
                beard=gris, hair_style='short',
                torso_over=belt_over(apron=T['tierra'], belt=P['tierra_o']), draw_prop=hammer_prop,
                tufts=[])


def elvira_style():
    return dict(stoop=2, tw=-1, shirt=(P['fol_m'], P['fol_o'], P['K']), sleeve=(P['fol_m'], P['fol_o'], P['K']),
                skirt=(P['tierra'], P['madera'], P['tierra_o']), pants=T['madera'], boots=BOTAS,
                hair=(P['tierra_o'], P['tierra_o'], P['K']), hair_style='long', draw_prop=basket_prop,
                tufts=[29, 34])


def inquisidor_style():
    robe = (P['piedra_m'], P['piedra_o'], P['K'])
    return dict(robe=robe, robe_len=3, shirt=robe, sleeve=robe, sleeve_frac=1.0, glove=(P['madera'], P['tierra_o'], P['K']),
                skin=(P['crema'], P['crema'], P['ocre_c']), hair=(P['piedra_m'], P['piedra_o'], P['K']),
                hair_style='short', boots=BOTAS, pants=robe,
                hat=hat_wide(robe, brim=(20, 43), crown=(28, 35), crown_h=7, band=P['piedra_c']),
                torso_over=lambda c, d, g: (belt_over(belt=P['tierra_o'])(c, d, g), insignia(c, d, g)))


def guardia_templo_style():
    return dict(shirt=T['piedra'], sleeve=T['piedra'], pants=T['piedra_d'], boots=BOTAS, hair=PELO_M,
                hat=helmet(T['piedra']), draw_prop=spear_prop(), torso_over=belt_over(belt=P['tierra_o']))


def guardia_sueldo_style():
    return dict(shirt=CUERO, sleeve=CUERO, pants=T['piedra_d'], boots=BOTAS, hair=PELO_M,
                hat=helmet(T['piedra'], plume=T['teja']),
                torso_over=lambda c, d, g: (breastplate(c, d, g)), draw_prop=spear_prop(), glove=T['piedra'])


def cliente_style(kind):
    base = dict(shirt=T['tela'], sleeve=T['tela'], pants=T['piedra'], boots=BOTAS, hair=T['madera'],
                tufts=[29, 31, 34], tufts_lat=[30, 33], skin=T['piel'])
    if kind == 'base':
        return base
    if kind == 'campesino':
        base.update(shirt=LINO, sleeve=LINO, pants=T['tierra'],
                    hat=hat_wide(T['paja'], brim=(21, 42), crown=(28, 35), crown_h=4, band=P['tierra']))
    elif kind == 'artesano':
        base.update(shirt=T['ocre'], sleeve=T['ocre'], pants=T['piedra_d'],
                    hat=hat_cap(T['madera']), torso_over=belt_over(apron=CUERO, belt=P['tierra_o']))
    elif kind == 'dama':
        base.update(shirt=LINO, sleeve=LINO, skirt=T['teja'], hair_style='long',
                    hat=hat_kerchief(T['ocre']), pants=T['piedra'])
    return base


def ladron_style():
    cap = (P['piedra_m'], P['piedra_o'], P['K'])
    return dict(stoop=3, shirt=cap, sleeve=cap, pants=(P['piedra_o'], P['K'], P['K']), boots=(P['piedra_o'], P['K'], P['K']),
                hair_style='none', hat=hood(cap), glove=T['piel'],
                torso_over=lambda c, d, g: c.fill(c.rect(g['x0'], g['hip'] - 1, g['x1'], g['hip']) & g['tm'], P['tierra_o']),
                draw_prop=ladron_prop)


def ladron_prop(c, d, g, po):
    if not po.get('bolsa'): return
    # saco de lino al hombro / en la mano
    if d == 'lat':
        x, y = 24, g['ty0'] + 3
    elif d == 'nor':
        x, y = 30, g['ty0'] + 4
    else:
        x, y = 38, g['ty0'] + 9
    c.paint(c.ell(x - 1, y, x + 7, y + 8), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)
    c.fill(c.rect(x + 2, y - 1, x + 4, y), P['tierra_o'])
    c.set(x + 3, y + 3, P['oro'])
