"""OB-01..OB-30 objetos del mundo (contorno 1 px, pivote Bottom)."""
import math
import numpy as np
from common import *

WOOD = (P['ocre_m'], P['madera'], P['tierra_o'])


def blank(n): return Cv(n, n)


def oak(var):
    c = blank(64)
    # tronco
    c.paint(c.poly([(27, 63), (29, 44), (35, 44), (37, 63)]), T['tierra'], k=1)
    c.set(30, 56, P['tierra_o']); c.set(33, 50, P['tierra_o'])
    if var == 0: blobs = [(32, 22, 17), (20, 30, 12), (44, 30, 12), (32, 36, 11)]
    elif var == 1: blobs = [(26, 24, 15), (42, 26, 14), (34, 14, 11), (30, 38, 10)]
    else: blobs = [(32, 18, 14), (18, 28, 11), (46, 24, 12), (30, 34, 12), (44, 38, 8)]
    for (x, y, r) in blobs:
        c.paint(c.ell(x - r, y - int(r * 0.9), x + r, y + int(r * 0.9)), T['fol'], k=2)
    # sombra interior: ramas visibles
    c.fill(c.line((32, 44), (28, 38), 1), P['tierra_o'])
    r = np.random.RandomState(var)
    for _ in range(16):
        x, y = r.randint(14, 50), r.randint(8, 40)
        if c.a[y, x, 3] and tuple(c.a[y, x, :3]) == P['fol_m']:
            c.set(x, y, P['fol_c']); c.set(x + 1, y + 1, P['fol_o'])
    c.outline()
    return c


def stump():
    c = blank(32)
    c.paint(c.rect(6, 16, 25, 28), T['tierra'], k=1)
    c.paint(c.ell(5, 10, 26, 22), (P['ocre_c'], P['ocre_c'], P['ocre_m']), k=1)
    c.paint(c.ell(10, 13, 21, 19), (P['ocre_m'], P['ocre_m'], P['ocre_c']), k=1)
    c.fill(c.ell(14, 15, 17, 17), P['ocre_c'])
    c.fill(c.rect(7, 24, 8, 28), P['tierra_o'])
    c.outline()
    return c


def sapling(phase):
    c = blank(32)
    if phase == 0:
        c.fill(c.line((16, 29), (16, 22), 1), P['fol_m'])
        c.paint(c.ell(11, 18, 16, 22), T['fol'], k=1); c.paint(c.ell(16, 16, 21, 21), T['fol'], k=1)
        c.paint(c.ell(10, 27, 21, 30), T['tierra'], k=1)
    elif phase == 1:
        c.paint(c.rect(15, 18, 17, 30), T['tierra'], k=1)
        c.paint(c.ell(8, 6, 24, 20), T['fol'], k=2)
    else:
        c.paint(c.rect(14, 16, 18, 31), T['tierra'], k=1)
        c.paint(c.ell(3, 1, 28, 20), T['fol'], k=2); c.paint(c.ell(8, 10, 24, 22), T['fol'], k=1)
    c.outline()
    return c


def herbs(full):
    c = blank(32)
    c.paint(c.ell(6, 24, 26, 30), T['tierra'], k=1)
    if full:
        for x, h in ((9, 10), (14, 14), (19, 11), (23, 8)):
            c.paint(c.ell(x - 2, 30 - h - 4, x + 3, 28), T['fol'], k=1)
        for x, y in ((11, 14), (21, 12)): c.set(x, y, P['crema']); c.set(x + 1, y, P['trigo'])
    else:
        for x in (11, 16, 21): c.set(x, 26, P['fol_m']); c.set(x, 25, P['fol_o'])
    c.outline()
    return c


def mushrooms(full):
    c = blank(32)
    c.paint(c.ell(6, 24, 26, 30), T['tierra'], k=1)
    if full:
        for x, y, r in ((10, 20, 4), (19, 16, 5), (23, 22, 3)):
            c.paint(c.rect(x - 1, y, x + 1, 26), T['paja'] if False else (P['crema'], P['crema'], P['piedra_c']), k=1)
            c.paint(c.ell(x - r, y - r + 1, x + r, y + 1), (P['ocre_m'], P['teja'], P['tierra_o']), k=1)
            c.set(x - 1, y - 2, P['crema'])
    else:
        c.set(16, 25, P['crema'])
    c.outline()
    return c


def plot(seeded):
    c = blank(32)
    c.paint(c.rect(1, 4, 30, 28), (P['tierra'], P['tierra'], P['tierra_o']), k=1)
    for y in range(8, 26, 6): c.fill(c.rect(3, y, 28, y + 1), P['tierra_o'])
    if seeded:
        for x in (7, 15, 23):
            for y in (10, 18): c.set(x, y, P['ocre_c']); c.set(x + 1, y, P['ocre_m'])
    c.outline()
    return c


def crop(kind, phase):
    c = blank(32)
    c.paint(c.rect(2, 22, 29, 30), (P['tierra'], P['tierra'], P['tierra_o']), k=1)
    if kind == 'trigo':
        cols = [(P['fol_c'], P['fol_m']), (P['fol_m'], P['trigo']), (P['trigo'], P['ocre_m'])][phase]
        for x in (7, 12, 17, 22):
            h = [5, 11, 17][phase]
            c.fill(c.line((x, 24), (x + (phase > 0) * 1, 24 - h), 1), cols[0])
            if phase == 2:
                c.fill(c.rect(x, 24 - h - 3, x + 1, 24 - h), P['trigo'])
    elif kind == 'nabo':
        c.paint(c.ell(9, 8 + (2 - phase) * 4, 22, 20 + (2 - phase) * 2), T['fol'], k=1) if phase < 2 else None
        for dx in (-3, 0, 3):
            c.fill(c.line((16, 22), (16 + dx * (phase + 1), 22 - 5 - phase * 4), 1), P['fol_m'])
        if phase == 2:
            c.paint(c.ell(11, 18, 21, 27), (P['crema'], P['crema'], P['lila']), k=1)
            c.fill(c.rect(11, 18, 21, 20), P['violeta']); c.fill(c.rect(11, 18, 21, 18), P['lila'])
    else:
        cols = [P['fol_c'], P['fol_m']]
        c.paint(c.ell(7, 12 - phase * 2, 25, 24), T['fol'], k=1)
        if phase == 2:
            c.paint(c.ell(8, 12, 24, 26), (P['trigo'], P['fuego'], P['teja']), k=1)
            c.fill(c.rect(15, 9, 17, 12), P['fol_o'])
            c.fill(c.rect(15, 14, 15, 24), P['teja']); c.fill(c.rect(20, 14, 20, 24), P['teja'])
    c.outline()
    return c


def awning(c, x0, x1, y, cols):
    for i, x in enumerate(range(x0, x1, 4)):
        col = cols[i % 2]
        c.paint(c.rect(x, y, min(x + 3, x1), y + 6), (col, col, P['K'] if False else P['tierra_o']), k=1)


def shelf(full):
    c = blank(64)
    c.paint(c.rect(4, 6, 59, 62), WOOD, k=1)
    c.fill(c.rect(7, 9, 56, 59), P['tierra_o'])
    for y in (24, 41):
        c.paint(c.rect(5, y, 58, y + 3), WOOD, k=1)
    if full:
        for row, y in enumerate((14, 31, 48)):
            for i, x in enumerate(range(9, 53, 11)):
                kind = (row + i) % 3
                if kind == 0: c.paint(c.rect(x, y, x + 7, y + 8), T['ocre'], k=1)
                elif kind == 1: c.paint(c.ell(x, y - 1, x + 7, y + 8), T['fol'], k=1)
                else: c.paint(c.rect(x, y + 1, x + 6, y + 8), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.outline()
    return c


def counter():
    c = blank(64)
    c.paint(c.rect(2, 26, 61, 62), WOOD, k=1)
    c.paint(c.rect(0, 20, 63, 29), (P['ocre_m'], P['ocre_m'], P['madera']), k=1)
    for x in (16, 32, 48): c.fill(c.rect(x, 31, x, 60), P['tierra_o'])
    c.fill(c.rect(6, 22, 12, 24), P['crema'])   # libro de cuentas
    c.paint(c.rect(46, 18, 53, 25), T['paja'], k=1)
    c.outline()
    return c


def bed():
    c = blank(64)
    c.paint(c.rect(4, 14, 59, 62), WOOD, k=1)
    c.paint(c.rect(8, 22, 55, 58), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)
    c.paint(c.rect(8, 40, 55, 58), (P['fol_m'] if False else P['teja'], P['teja'], P['tierra_o']), k=1)
    c.paint(c.rect(12, 24, 34, 34), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.paint(c.rect(4, 8, 59, 15), WOOD, k=1)
    c.outline()
    return c


def stall(colors, extra):
    c = blank(64)
    c.paint(c.rect(6, 34, 57, 62), WOOD, k=1)
    c.paint(c.rect(4, 30, 59, 38), (P['ocre_m'], P['ocre_m'], P['madera']), k=1)
    c.paint(c.rect(7, 12, 9, 34), WOOD, k=1); c.paint(c.rect(54, 12, 56, 34), WOOD, k=1)
    for i, x in enumerate(range(3, 61, 6)):
        col = colors[i % 2]
        c.paint(c.poly([(x, 4), (x + 5, 4), (x + 5, 14), (x + 2, 17), (x, 14)]), (col, col, P['tierra_o']), k=1)
    extra(c)
    c.outline()
    return c


def ex_tomas(c):
    for i, x in enumerate(range(10, 52, 9)):
        c.paint(c.ell(x, 26, x + 7, 33), T['paja'], k=1)


def ex_bruno(c):
    c.paint(c.rect(10, 22, 26, 30), T['piedra_d'], k=1); c.paint(c.rect(14, 29, 22, 34), T['piedra_d'], k=1)
    c.paint(c.rect(38, 24, 52, 33), (P['fuego'], P['teja'], P['tierra_o']), k=1)    # fragua con brasa
    c.set(42, 26, P['trigo']); c.set(46, 27, P['trigo'])


def ex_elvira(c):
    for x in (12, 24, 36, 46):
        c.paint(c.ell(x, 24, x + 6, 33), T['fol'], k=1)
        c.set(x + 2, 25, P['crema'])


def ex_inq(c):
    c.paint(c.rect(26, 22, 37, 32), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.fill(c.poly([(31, 23), (34, 27), (31, 31), (28, 27)]), P['trigo'])


def ex_guard(c):
    spear(c, (16, 33), (16, 18)) if False else None
    c.paint(c.rect(12, 22, 18, 33), T['piedra'], k=1); c.paint(c.rect(44, 22, 50, 33), T['piedra'], k=1)


def spear(c, a, b):
    c.fill(c.line(a, b, 1), P['madera'])


def door(reinforced):
    c = blank(64)
    c.paint(c.rect(6, 4, 57, 62), T['piedra'], k=1)
    c.paint(c.poly([(14, 62), (14, 18), (24, 8), (40, 8), (50, 18), (50, 62)]), WOOD, k=2)
    for x in (22, 32, 42): c.fill(c.rect(x, 12, x, 62), P['tierra_o'])
    c.set(44, 40, P['trigo']); c.set(44, 41, P['ocre_m'])
    if reinforced:
        for y in (22, 38, 54):
            c.paint(c.rect(14, y, 50, y + 3), T['piedra_d'], k=1)
        for x in (18, 46):
            for y in (23, 39, 55): c.set(x, y, P['piedra_c'])
    c.outline()
    return c


def lamp(lit):
    c = blank(32)
    c.paint(c.rect(14, 2, 16, 8), T['piedra_d'], k=1)
    c.paint(c.rect(9, 8, 21, 25), (P['tierra'], P['tierra_o'], P['K']), k=1)
    c.fill(c.rect(11, 11, 19, 22), P['fuego'] if lit else P['piedra_o'])
    if lit:
        c.fill(c.rect(13, 14, 17, 20), P['trigo']); c.fill(c.rect(15, 16, 15, 18), P['crema'])
    c.paint(c.rect(7, 25, 23, 28), (P['tierra'], P['tierra_o'], P['K']), k=1)
    c.outline()
    return c


def woodpile():
    c = blank(64)
    # troncos apilados en cabana; sin fuego, sin brasas, vacia
    for i, y in enumerate((52, 40, 28)):
        for x in range(8 + i * 5, 54 - i * 5, 10):
            c.paint(c.ell(x, y, x + 12, y + 11), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
            c.fill(c.ell(x + 8, y + 3, x + 11, y + 8), P['ocre_c'])
    c.paint(c.ell(22, 18, 40, 30), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
    c.outline()
    return c


def gravestone(v):
    c = blank(32)
    if v == 0: m = c.poly([(9, 30), (9, 10), (12, 5), (20, 5), (23, 10), (23, 30)])
    elif v == 1: m = c.poly([(8, 30), (8, 8), (24, 8), (24, 30)])
    else: m = c.poly([(10, 30), (10, 14), (16, 4), (22, 14), (22, 30)])
    c.paint(m, T['piedra'], k=1)
    c.fill(c.rect(14, 12, 17, 12), P['piedra_o']) if v != 2 else None
    c.fill(c.poly([(15, 13), (18, 17), (15, 21), (12, 17)]), P['piedra_o'])  # rombo (sin simbolos religiosos reales)
    c.fill(c.rect(5, 29, 26, 31), P['fol_m'])
    c.outline()
    return c


def cemetery_gate(open_):
    c = blank(64)
    c.paint(c.rect(2, 8, 11, 62), T['piedra'], k=1); c.paint(c.rect(52, 8, 61, 62), T['piedra'], k=1)
    c.paint(c.rect(0, 4, 13, 12), T['piedra'], k=1); c.paint(c.rect(50, 4, 63, 12), T['piedra'], k=1)
    if not open_:
        for x in range(14, 50, 6):
            c.paint(c.rect(x, 14, x + 1, 62), (P['piedra_c'], P['piedra_m'], P['K']), k=1)
            c.set(x, 13, P['piedra_c'])
        c.fill(c.rect(14, 28, 49, 29), P['K']); c.fill(c.rect(14, 48, 49, 49), P['K'])
        c.paint(c.line((14, 30), (49, 46), 2), (P['piedra_c'], P['piedra_m'], P['piedra_o']), k=1)   # cadena
        c.paint(c.rect(29, 36, 34, 42), (P['trigo'], P['ocre_m'], P['tierra']), k=1)                  # candado
    else:
        c.paint(c.poly([(14, 14), (20, 16), (20, 62), (14, 62)]), (P['piedra_c'], P['piedra_m'], P['K']), k=1)
        c.paint(c.poly([(49, 14), (43, 16), (43, 62), (49, 62)]), (P['piedra_c'], P['piedra_m'], P['K']), k=1)
    c.outline()
    return c


def acorn(frame=None, old=False):
    c = blank(32)
    body = (P['ocre_m'], P['ocre_c'] if False else P['trigo'], P['tierra']) if old else (P['ocre_c'], P['ocre_m'], P['tierra'])
    s = 1 if old else 0
    c.paint(c.ell(10 - s * 2, 14 - s * 2, 21 + s * 2, 27), body, k=1)
    c.paint(c.ell(8 - s * 2, 9 - s * 2, 23 + s * 2, 17), (P['ocre_m'], P['tierra'], P['tierra_o']), k=1)
    c.fill(c.rect(15, 6 - s * 2, 16, 9 - s * 2), P['tierra_o'])
    c.outline()
    if frame is not None:
        # brillo: cuatro puntos que orbitan (cuadrado de 3 px, sin alfa parcial)
        pos = [(5, 8), (24, 6), (25, 20), (5, 22)][frame]
        col = P['oro'] if old else P['crema']
        gl = Cv(32, 32)
        x, y = pos
        gl.set(x, y, col); gl.set(x - 1, y, col); gl.set(x + 1, y, col); gl.set(x, y - 1, col); gl.set(x, y + 1, col)
        c.blit(gl)
    return c


def coin(frame):
    c = blank(32)
    w = [10, 6, 2, 6][frame]
    c.paint(c.ell(16 - w, 8, 16 + w, 24), (P['oro'], P['trigo'], P['ocre_m']), k=1)
    if w > 3: c.fill(c.ell(16 - w + 3, 11, 16 + w - 3, 21), P['trigo'])
    c.outline()
    return c


def signpost():
    c = blank(32)
    c.paint(c.rect(14, 12, 17, 31), T['maderat'], k=1)
    c.paint(c.poly([(3, 3), (24, 3), (29, 8), (24, 13), (3, 13)]), WOOD, k=1)
    c.fill(c.rect(7, 8, 19, 8), P['tierra_o'])
    c.set(22, 8, P['crema']); c.set(23, 8, P['crema'])
    c.outline()
    return c


def cart():
    c = blank(64)
    c.paint(c.rect(6, 22, 57, 46), WOOD, k=1)
    for x in range(10, 54, 9):
        c.paint(c.rect(x, 12, x + 6, 26), (P['ocre_c'], P['ocre_m'], P['madera']), k=1)
        c.fill(c.ell(x + 1, 10, x + 5, 14), P['ocre_c'])
    for x in (14, 44):
        c.paint(c.ell(x - 8, 38, x + 8, 62), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
        c.fill(c.ell(x - 5, 42, x + 5, 58), P['tierra_o'])
        c.fill(c.rect(x - 1, 40, x, 60), P['ocre_m']); c.fill(c.rect(x - 6, 50, x + 6, 50), P['ocre_m'])
    c.fill(c.line((56, 40), (62, 52), 1), P['madera'])
    c.outline()
    return c


def barrel_boxes(v):
    c = blank(32)
    if v == 0:
        c.paint(c.ell(6, 3, 25, 29), WOOD, k=2)
        for y in (9, 21): c.fill(c.rect(7, y, 24, y), P['piedra_o'])
        c.fill(c.ell(8, 4, 23, 11), P['ocre_m'])
    elif v == 1:
        c.paint(c.rect(3, 12, 17, 29), WOOD, k=1); c.paint(c.rect(15, 18, 29, 30), WOOD, k=1)
        c.fill(c.line((4, 13), (16, 28), 1), P['tierra_o']); c.fill(c.line((16, 19), (28, 29), 1), P['tierra_o'])
    else:
        c.paint(c.ell(2, 12, 15, 30), WOOD, k=1); c.paint(c.rect(16, 14, 29, 30), WOOD, k=1)
        c.fill(c.rect(16, 20, 29, 20), P['tierra_o'])
    c.outline()
    return c


def char_shadow():
    c = blank(32)
    c.fill(c.ell(4, 22, 27, 30), P['K'], 90)       # unica sombra semitransparente autorizada (OB-29)
    return c


def marker_e():
    c = blank(32)
    c.paint(c.rect(7, 5, 24, 22), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.fill(c.rect(7, 22, 24, 24), P['piedra_m'])
    g = ['XXXXX', 'X....', 'X....', 'XXXX.', 'X....', 'X....', 'XXXXX']
    for j, row in enumerate(g):
        for i, ch in enumerate(row):
            if ch == 'X': c.set(11 + i, 8 + j, P['K']); c.set(12 + i, 8 + j, P['K'])
    c.outline()
    return c


def strip(frames): return hstack(frames)


def build():
    def out(c, name, oid): save(c, f'Objects/{name}.png', oid)
    for i in range(3): out(oak(i), f'spr_obj_roble_{i + 1:02d}', 'OB-01')
    out(stump(), 'spr_obj_tocon', 'OB-02')
    out(strip([sapling(i) for i in range(3)]), 'spr_obj_roble_joven', 'OB-03')
    out(strip([herbs(1), herbs(0)]), 'spr_obj_hierbas', 'OB-04')
    out(strip([mushrooms(1), mushrooms(0)]), 'spr_obj_hongos', 'OB-05')
    out(strip([plot(0), plot(1)]), 'spr_obj_parcela', 'OB-06')
    for kind, oid in (('trigo', 'OB-07'), ('nabo', 'OB-08'), ('calabaza', 'OB-09')):
        out(strip([crop(kind, p) for p in range(3)]), f'spr_obj_cultivo_{kind}', oid)
    out(strip([shelf(0), shelf(1)]), 'spr_obj_estante', 'OB-10')
    out(counter(), 'spr_obj_mostrador', 'OB-11')
    out(bed(), 'spr_obj_cama', 'OB-12')
    out(stall((P['trigo'], P['crema']), ex_tomas), 'spr_obj_puesto_tomas', 'OB-13')
    out(stall((P['piedra_m'], P['piedra_c']), ex_bruno), 'spr_obj_puesto_bruno', 'OB-14')
    out(stall((P['fol_m'], P['fol_c']), ex_elvira), 'spr_obj_puesto_elvira', 'OB-15')
    out(stall((P['piedra_o'], P['piedra_m']), ex_inq), 'spr_obj_puesto_inquisidor', 'OB-16')
    out(stall((P['teja'], P['crema']), ex_guard), 'spr_obj_puesto_guardias', 'OB-17')
    out(strip([door(0), door(1)]), 'spr_obj_puerta_tienda', 'OB-18')
    out(strip([lamp(1), lamp(0)]), 'spr_obj_farol_fachada', 'OB-19')
    out(woodpile(), 'spr_obj_pila_lena', 'OB-20')
    out(strip([gravestone(i) for i in range(3)]), 'spr_obj_lapida', 'OB-21')
    out(strip([cemetery_gate(0), cemetery_gate(1)]), 'spr_obj_porton_cementerio', 'OB-22')
    out(strip([acorn()] + [acorn(i) for i in range(4)]), 'spr_obj_bellota', 'OB-23')
    out(strip([acorn(old=True)] + [acorn(i, True) for i in range(4)]), 'spr_obj_bellota_antigua', 'OB-24')
    out(strip([coin(i) for i in range(4)]), 'spr_obj_moneda', 'OB-25')
    out(signpost(), 'spr_obj_letrero_sendero', 'OB-26')
    out(cart(), 'spr_obj_carro_lena', 'OB-27')
    out(strip([barrel_boxes(i) for i in range(3)]), 'spr_obj_barril_cajas', 'OB-28')
    out(char_shadow(), 'spr_obj_sombra', 'OB-29')
    out(marker_e(), 'spr_obj_marcador_e', 'OB-30')


if __name__ == '__main__':
    build()
