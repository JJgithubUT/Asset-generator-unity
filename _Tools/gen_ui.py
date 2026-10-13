"""IT-01..11 iconos de inventario, UI-01..33 interfaz, FX-01..07 particulas."""
import math
import numpy as np
from common import *
import pixfont

WOOD = (P['ocre_m'], P['madera'], P['tierra_o'])
SACK = (P['crema'], P['ocre_c'], P['ocre_m'])


# ======================================================== ITEMS 32x32
def sack(label, shape):
    c = Cv(32, 32)
    if shape == 0:      # alto
        m = c.poly([(9, 30), (8, 14), (11, 8), (21, 8), (24, 14), (23, 30)])
    elif shape == 1:    # redondo
        m = c.ell(5, 9, 26, 30)
    else:               # achatado ancho
        m = c.poly([(4, 30), (3, 18), (8, 11), (24, 11), (29, 18), (28, 30)])
    c.paint(m, SACK, k=2)
    c.paint(c.rect(11, 6, 20, 9), SACK, k=1)                  # boca
    c.fill(c.rect(11, 9, 20, 10), P['tierra_o'])               # cuerda
    c.paint(c.rect(11, 17, 20, 25), (label, label, P['tierra_o']), k=1)   # etiqueta de color
    c.set(15, 20, P['K']); c.set(16, 21, P['K']); c.set(15, 22, P['K'])
    c.outline()
    return c


def it_trigo():
    c = Cv(32, 32)
    for i, x in enumerate((9, 14, 19, 24)):
        c.fill(c.line((x - 2 + i, 29), (x, 12), 1), P['ocre_m'])
        for k in range(5):
            y = 5 + k * 3
            c.paint(c.ell(x - 3, y, x + 1, y + 3), T['paja'], k=1)
            c.paint(c.ell(x, y + 1, x + 4, y + 4), T['paja'], k=1)
    c.fill(c.rect(8, 22, 25, 24), P['tierra'])
    c.outline()
    return c


def it_nabo():
    c = Cv(32, 32)
    c.paint(c.poly([(6, 14), (26, 14), (21, 28), (16, 31), (11, 28)]), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.fill(c.rect(7, 14, 25, 18), P['violeta']); c.fill(c.rect(8, 14, 20, 14), P['lila'])
    for dx in (-5, 0, 5):
        c.paint(c.line((16, 14), (16 + dx, 3), 3), T['fol'], k=1)
    c.outline()
    return c


def it_calabaza():
    c = Cv(32, 32)
    c.paint(c.ell(3, 9, 28, 30), (P['trigo'], P['fuego'], P['teja']), k=2)
    for x in (10, 16, 22): c.fill(c.line((x, 11), (x, 28), 1), P['teja'])
    c.paint(c.rect(14, 4, 17, 10), T['fol'], k=1)
    c.outline()
    return c


def it_lena():
    c = Cv(32, 32)
    for (x, y) in ((3, 18), (13, 18), (8, 9)):
        c.paint(c.rect(x, y, x + 17, y + 8), WOOD, k=1)
        c.paint(c.ell(x + 14, y, x + 20, y + 8), (P['ocre_c'], P['ocre_m'], P['tierra']), k=1)
        c.fill(c.ell(x + 16, y + 3, x + 18, y + 5), P['tierra_o'])
        c.fill(c.line((x + 2, y + 3), (x + 10, y + 3), 1), P['tierra_o'])
    c.outline()
    return c


def it_hierbas():
    c = Cv(32, 32)
    for dx, h in ((-8, 22), (-4, 25), (0, 27), (4, 25), (8, 22)):
        c.paint(c.line((16, 27), (16 + dx, 27 - h), 3), T['fol'], k=1)
    c.paint(c.ell(8, 20, 23, 25), (P['ocre_c'], P['ocre_m'], P['tierra']), k=1)   # atadura
    c.set(10, 6, P['crema']); c.set(22, 7, P['crema'])
    c.outline()
    return c


def it_hongos():
    c = Cv(32, 32)
    for x, y, r in ((9, 17, 7), (21, 14, 8)):
        c.paint(c.rect(x - 2, y, x + 2, 28), (P['crema'], P['crema'], P['piedra_c']), k=1)
        c.paint(c.ell(x - r, y - r + 2, x + r, y + 4), (P['ocre_m'], P['teja'], P['tierra_o']), k=1)
        c.set(x - 2, y - 3, P['crema']); c.set(x + 2, y - 1, P['crema'])
    c.outline()
    return c


def it_cuerda():
    c = Cv(32, 32)
    for i, r in enumerate((13, 9, 5)):
        c.paint(c.ell(16 - r - 2, 16 - r + 1, 16 + r + 2, 16 + r + 1) if False else c.ell(16 - r, 16 - r, 16 + r, 16 + r), T['ocre'], k=1) if i == 0 else None
    c.paint(c.ell(3, 3, 28, 28), (P['ocre_c'], P['ocre_m'], P['tierra']), k=1)
    c.fill(c.ell(8, 8, 23, 23), P['ocre_m'])
    c.fill(c.ell(12, 12, 19, 19), 0 if False else P['tierra'])
    c.fill(c.ell(14, 14, 17, 17), P['tierra_o'])
    for k in range(8):
        a = k * math.pi / 4
        c.set(int(16 + 10 * math.cos(a)), int(16 + 10 * math.sin(a)), P['tierra'])
    c.fill(c.line((22, 24), (30, 30), 2), P['ocre_m'])
    c.outline()
    return c


def it_infusion():
    c = Cv(32, 32)
    c.paint(c.poly([(6, 12), (23, 12), (21, 28), (8, 28)]), (P['crema'], P['crema'], P['piedra_c']), k=1)
    c.fill(c.rect(8, 14, 21, 18), P['fol_c']); c.fill(c.rect(8, 14, 21, 14), P['fol_m'])
    c.paint(c.ell(21, 14, 29, 24), (P['crema'], P['piedra_c'], P['piedra_m']), k=1) if False else None
    c.fill(c.ring(23, 19, 4) if hasattr(c, 'ring') else c.rect(24, 15, 27, 22), P['piedra_c'])
    c.fill(c.rect(25, 17, 26, 20), 0 if False else P['piedra_m'])
    for x in (11, 15, 19): c.set(x, 8, P['niebla']); c.set(x + 1, 6, P['niebla']); c.set(x, 4, P['niebla'])
    c.outline()
    return c


ITEMS = [('semilla_trigo', lambda: sack(P['trigo'], 0), 'IT-01'), ('semilla_nabo', lambda: sack(P['violeta'], 1), 'IT-02'),
         ('semilla_calabaza', lambda: sack(P['teja'], 2), 'IT-03'), ('trigo', it_trigo, 'IT-04'), ('nabo', it_nabo, 'IT-05'),
         ('calabaza', it_calabaza, 'IT-06'), ('lena', it_lena, 'IT-07'), ('hierbas', it_hierbas, 'IT-08'),
         ('hongos', it_hongos, 'IT-09'), ('cuerda', it_cuerda, 'IT-10'), ('infusion', it_infusion, 'IT-11')]


# ======================================================== ICONOS UI 64x64
def ico(fn):
    c = Cv(64, 64)
    fn(c)
    c.outline()
    return c


def i_coin(c):
    c.paint(c.ell(8, 8, 55, 55), (P['oro'], P['trigo'], P['ocre_m']), k=2)
    c.fill(c.ell(15, 15, 48, 48), P['trigo']); c.fill(c.ell(16, 16, 47, 47) & ~c.ell(18, 18, 45, 45), P['oro'])
    c.fill(c.rect(29, 22, 34, 41), P['ocre_m']); c.fill(c.rect(25, 22, 38, 24), P['ocre_m']); c.fill(c.rect(25, 39, 38, 41), P['ocre_m'])


def i_leaf(c):
    m = c.poly([(10, 54), (14, 30), (28, 12), (52, 8), (54, 30), (42, 50), (22, 54)])
    c.paint(m, T['fol'], k=2)
    c.fill(c.line((12, 52), (46, 14), 2), P['fol_o'])
    for i in range(4): c.fill(c.line((20 + i * 6, 44 - i * 7), (28 + i * 6, 44 - i * 5), 1), P['fol_o'])


def i_heart(c):
    c.paint(c.ell(6, 8, 33, 36), (P['vida'], P['vida'], P['integ']), k=2)
    c.paint(c.ell(30, 8, 57, 36), (P['vida'], P['vida'], P['integ']), k=2)
    c.paint(c.poly([(8, 28), (55, 28), (32, 57)]), (P['vida'], P['vida'], P['integ']), k=2)
    c.fill(c.rect(14, 14, 18, 18), P['crema']); c.fill(c.rect(14, 19, 15, 21), P['crema'])


def i_shield(c):
    m = c.poly([(8, 8), (32, 4), (56, 8), (56, 34), (32, 60), (8, 34)])
    c.paint(m, (P['integ'], P['integ'], P['teja']), k=2)
    c.fill(c.poly([(32, 12), (48, 14), (48, 32), (32, 50), (16, 32), (16, 14)]), P['teja'])
    c.fill(c.poly([(32, 16), (44, 18), (44, 31), (32, 44), (20, 31), (20, 18)]), P['integ'])
    c.fill(c.poly([(32, 20), (42, 30), (32, 40), (22, 30)]), P['crema'])
    c.fill(c.poly([(32, 25), (37, 30), (32, 35), (27, 30)]), P['integ'])


def i_sun(c):
    for k in range(8):
        a = k * math.pi / 4
        c.paint(c.line((32 + 20 * math.cos(a), 32 + 20 * math.sin(a)), (32 + 28 * math.cos(a), 32 + 28 * math.sin(a)), 4), (P['trigo'], P['trigo'], P['ocre_m']), k=1)
    c.paint(c.ell(14, 14, 49, 49), (P['oro'], P['trigo'], P['ocre_m']), k=2)


def i_moon(c):
    m = c.ell(10, 8, 54, 56) & ~c.ell(26, 4, 66, 48)
    c.paint(m, (P['niebla'], P['lila'], P['violeta']), k=2)
    c.set(46, 14, P['niebla']); c.set(50, 30, P['niebla'])


def i_torch(c):
    c.paint(c.line((20, 58), (38, 28), 7), WOOD, k=1)
    c.paint(c.ell(22, 6, 46, 34), (P['trigo'], P['fuego'], P['teja']), k=2)
    c.fill(c.ell(29, 14, 39, 30), P['trigo']); c.fill(c.ell(32, 20, 36, 28), P['crema'])


def i_leaf_small(c):
    m = c.poly([(16, 48), (18, 32), (28, 20), (46, 16), (48, 32), (40, 44), (26, 48)])
    c.paint(m, T['fol'], k=1)
    c.fill(c.line((18, 46), (40, 22), 1), P['fol_o'])


def i_lock(c):
    c.paint(c.rect(14, 28, 49, 56), (P['trigo'], P['ocre_m'], P['tierra']), k=2)
    c.paint(c.ell(20, 8, 43, 40) & ~c.ell(27, 16, 36, 40), T['piedra'], k=1)
    c.fill(c.rect(30, 38, 33, 48), P['tierra_o']); c.fill(c.ell(28, 36, 35, 42), P['tierra_o'])


def i_check(c):
    c.paint(c.line((12, 34), (26, 50), 8), (P['fol_c'], P['fol_m'], P['fol_o']), k=1)
    c.paint(c.line((26, 50), (54, 14), 8), (P['fol_c'], P['fol_m'], P['fol_o']), k=1)


def i_circle(c):
    c.paint(c.ell(8, 8, 55, 55) & ~c.ell(16, 16, 47, 47), T['piedra'], k=1)


def i_arrow(c):
    c.paint(c.poly([(10, 24), (34, 24), (34, 10), (56, 32), (34, 54), (34, 40), (10, 40)]), (P['crema'], P['crema'], P['piedra_c']), k=1)


def i_close(c):
    c.paint(c.line((14, 14), (50, 50), 8), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)
    c.paint(c.line((50, 14), (14, 50), 8), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)


def i_gear(c):
    for k in range(8):
        a = k * math.pi / 4
        c.paint(c.line((32 + 18 * math.cos(a), 32 + 18 * math.sin(a)), (32 + 27 * math.cos(a), 32 + 27 * math.sin(a)), 8), T['piedra'], k=1)
    c.paint(c.ell(10, 10, 53, 53), T['piedra'], k=2)
    c.fill(c.ell(23, 23, 40, 40), P['K'])
    c.fill(c.ell(25, 25, 38, 38), P['azul_m'])


def i_speaker(c, on=True):
    c.paint(c.poly([(8, 24), (20, 24), (34, 10), (34, 54), (20, 40), (8, 40)]), T['piedra'], k=1)
    if on:
        for r in (10, 18):
            ring = c.ell(32 - r, 32 - r, 32 + r + 4, 32 + r) if False else c.ell(34 - r // 2, 32 - r, 34 + r + 6, 32 + r)
            ring &= ~c.ell(34 - r // 2 + 4, 32 - r + 4, 34 + r + 2, 32 + r - 4)
            ring &= c.rect(40, 0, 63, 63)
            c.paint(ring, (P['crema'], P['crema'], P['piedra_c']), k=1)
    else:
        c.paint(c.line((42, 22), (58, 42), 5), (P['vida'], P['vida'], P['integ']), k=1)
        c.paint(c.line((58, 22), (42, 42), 5), (P['vida'], P['vida'], P['integ']), k=1)


def i_screen(c):
    c.paint(c.rect(6, 12, 57, 46), T['piedra'], k=2)
    c.fill(c.rect(11, 17, 52, 41), P['azul_m'])
    c.fill(c.rect(11, 17, 24, 22), P['niebla'])
    c.paint(c.rect(26, 46, 37, 52), T['piedra'], k=1); c.paint(c.rect(18, 52, 45, 56), T['piedra'], k=1)
    for (x, y) in ((14, 20), (47, 20), (14, 36), (47, 36)): c.fill(c.rect(x, y, x + 3, y + 3), P['crema'])


def i_contrast(c):
    c.fill(c.ell(8, 8, 55, 55), P['crema'])
    c.fill(c.ell(8, 8, 55, 55) & c.rect(32, 0, 63, 63), P['noche'])
    c.paint(c.ell(8, 8, 55, 55), (P['piedra_c'], P['piedra_c'], P['piedra_m']), k=1, light=False) if False else None


UI_ICONS = [('moneda_oro', i_coin, 'UI-01'), ('hoja', i_leaf, 'UI-02'), ('corazon', i_heart, 'UI-03'), ('escudo', i_shield, 'UI-04'),
            ('sol', i_sun, 'UI-05'), ('luna', i_moon, 'UI-06'), ('antorcha', i_torch, 'UI-07'), ('hoja_pequena', i_leaf_small, 'UI-08'),
            ('candado', i_lock, 'UI-09'), ('palomita', i_check, 'UI-10'), ('circulo_vacio', i_circle, 'UI-11'), ('flecha', i_arrow, 'UI-12'),
            ('cruz_cerrar', i_close, 'UI-13'), ('engrane', i_gear, 'UI-14'), ('altavoz_activo', lambda c: i_speaker(c, True), 'UI-15'),
            ('altavoz_silenciado', lambda c: i_speaker(c, False), 'UI-16'), ('pantalla', i_screen, 'UI-17'), ('contraste', i_contrast, 'UI-18')]


# ======================================================== ELEMENTOS UI
def panel(w, h, fill=None, frame=WOOD, bw=8, studs=True, dither=True):
    c = Cv(w, h)
    fill = fill or P['noche']
    c.fill(c.rect(0, 0, w - 1, h - 1), P['K'])
    c.paint(c.rect(1, 1, w - 2, h - 2), frame, k=2)
    c.fill(c.rect(bw, bw, w - 1 - bw, h - 1 - bw), P['K'])
    inner = c.rect(bw + 1, bw + 1, w - 2 - bw, h - 2 - bw)
    c.fill(inner, fill)
    if dither:
        ys, xs = np.nonzero(inner)
        for y, x in zip(ys, xs):
            if (x + y) % 4 == 0 and (x // 4 + y // 4) % 2 == 0:
                c.set(x, y, P['azul_m'] if fill == P['noche'] else P['piedra_c'])
    c.fill(c.rect(bw + 1, bw + 1, w - 2 - bw, bw + 1), P['azul_m'] if fill == P['noche'] else P['crema'])
    if studs:
        for (x, y) in ((bw // 2, bw // 2), (w - 1 - bw // 2, bw // 2), (bw // 2, h - 1 - bw // 2), (w - 1 - bw // 2, h - 1 - bw // 2)):
            c.fill(c.rect(x - 1, y - 1, x + 1, y + 1), P['trigo'])
            c.set(x - 1, y - 1, P['crema'])
    return c


def button(state):
    tones = {0: (P['ocre_m'], P['madera'], P['tierra_o']), 1: (P['trigo'], P['ocre_m'], P['tierra']), 2: (P['tierra'], P['tierra_o'], P['K'])}[state]
    c = Cv(160, 48)
    off = 2 if state == 2 else 0
    c.fill(c.rect(0, 0, 159, 47), P['K'])
    c.paint(c.rect(1, 1 + off, 158, 46), tones, k=3, light=state != 2)
    c.fill(c.rect(4, 4 + off, 155, 43), tones[1])
    if state == 1:
        c.fill(c.rect(4, 4, 155, 5), P['crema'])
    for x in (3, 156):
        c.fill(c.rect(x, 3 + off, x + 0, 4 + off), P['trigo'])
    c.fill(c.rect(0, 0, 1, 1), 0 if False else P['K'])
    # esquinas cortadas
    for (x, y) in ((0, 0), (159, 0), (0, 47), (159, 47)):
        c.a[y, x] = 0
    return c


def slot(selected):
    c = Cv(48, 48)
    col = P['trigo'] if selected else P['piedra_m']
    c.fill(c.rect(0, 0, 47, 47), P['K'])
    c.paint(c.rect(1, 1, 46, 46), (col, col, P['piedra_o']) if not selected else (P['crema'], P['trigo'], P['ocre_m']), k=2 if selected else 1)
    c.fill(c.rect(4 if selected else 3, 4 if selected else 3, 43 if selected else 44, 43 if selected else 44), P['K'])
    c.fill(c.rect(5, 5, 42, 42), P['noche'])
    c.fill(c.rect(5, 5, 42, 5), P['azul_m']); c.fill(c.rect(5, 5, 5, 42), P['azul_m'])
    return c


def bar_back(w=192, h=24):
    c = Cv(w, h)
    c.fill(c.rect(0, 0, w - 1, h - 1), P['K'])
    c.paint(c.rect(1, 1, w - 2, h - 2), (P['piedra_m'], P['piedra_o'], P['piedra_o']), k=1)
    c.fill(c.rect(3, 3, w - 4, h - 4), P['noche'])
    for a in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)): c.a[a[1], a[0]] = 0
    return c


def bar_fill(col, light, dark, w=192, h=24):
    c = Cv(w, h)
    m = c.rect(3, 3, w - 4, h - 4)
    c.fill(m, col)
    c.fill(c.rect(3, 3, w - 4, 5), light)
    c.fill(c.rect(3, h - 6, w - 4, h - 4), dark)
    return c


def clock_back():
    c = bar_back(256, 32)
    # marcas de hora
    for i in range(1, 12):
        x = 3 + int((256 - 7) * i / 12)
        c.fill(c.rect(x, 24, x, 27), P['piedra_m'])
    return c


def dialog_box():
    c = panel(896, 192, bw=8)
    # hueco de 128 px para el retrato (izquierda)
    c.fill(c.rect(24, 32, 24 + 127, 32 + 127), P['K'])
    c.fill(c.rect(26, 34, 24 + 125, 32 + 125), P['azul_m'])
    c.fill(c.rect(26, 34, 24 + 125, 34), P['lila'])
    return c


def notif():
    return panel(320, 64, bw=6)


def trade_panel():
    c = panel(768, 512, bw=10)
    c.fill(c.rect(20, 56, 747, 57), P['azul_m'])            # linea bajo las pestanas
    c.fill(c.rect(20, 58, 747, 58), P['K'])
    c.fill(c.rect(380, 70, 381, 490), P['azul_m'])           # separador de columnas
    return c


def tab(active):
    c = Cv(160, 40)
    tones = (P['trigo'], P['ocre_m'], P['tierra_o']) if active else (P['madera'], P['tierra_o'], P['K'])
    c.fill(c.rect(0, 0, 159, 39), P['K'])
    c.paint(c.rect(1, 1, 158, 39), tones, k=2)
    c.fill(c.rect(4, 4, 155, 39), tones[1])
    for (x, y) in ((0, 0), (159, 0)): c.a[y, x] = 0
    return c


def slider_track():
    c = Cv(256, 32)
    c.fill(c.rect(0, 12, 255, 19), P['K'])
    c.fill(c.rect(1, 13, 254, 18), P['piedra_o'])
    c.fill(c.rect(1, 13, 254, 14), P['piedra_m'])
    return c


def knob(w, h):
    c = Cv(w, h)
    c.fill(c.rect(0, 0, w - 1, h - 1), P['K'])
    c.paint(c.rect(1, 1, w - 2, h - 2), (P['crema'], P['trigo'], P['ocre_m']), k=2)
    for a in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)): c.a[a[1], a[0]] = 0
    return c


def toggle(on):
    c = Cv(64, 32)
    c.fill(c.rect(0, 0, 63, 31), P['K'])
    c.paint(c.rect(1, 1, 62, 30), (P['fol_c'], P['fol_m'], P['fol_o']) if on else (P['piedra_m'], P['piedra_o'], P['K']), k=2)
    kx = 36 if on else 4
    c.fill(c.rect(kx, 4, kx + 23, 27), P['K'])
    c.paint(c.rect(kx + 1, 5, kx + 22, 26), (P['crema'], P['crema'], P['piedra_c']), k=1)
    for a in ((0, 0), (63, 0), (0, 31), (63, 31)): c.a[a[1], a[0]] = 0
    return c


def scroll_track():
    c = Cv(24, 256)
    c.fill(c.rect(0, 0, 23, 255), P['K'])
    c.fill(c.rect(1, 1, 22, 254), P['piedra_o'])
    c.fill(c.rect(1, 1, 2, 254), P['piedra_m'])
    return c


# ======================================================== VFX
def fx_mota():
    c = Cv(32, 32)
    for r, a, col in ((14, 40, P['lila']), (11, 80, P['lila']), (8, 130, P['niebla']), (5, 200, P['niebla']), (2, 255, P['crema'])):
        c.fill(c.ell(16 - r, 16 - r, 16 + r, 16 + r), col, a)
    return c


def fx_polvo():
    c = Cv(32, 32)
    for (x, y, w, h, col) in ((6, 20, 5, 2, P['ocre_c']), (14, 10, 2, 5, P['ocre_m']), (22, 18, 6, 2, P['crema']), (11, 24, 3, 3, P['madera']),
                              (20, 7, 3, 3, P['ocre_c']), (4, 8, 2, 2, P['crema']), (26, 26, 2, 2, P['ocre_m'])):
        c.fill(c.rect(x, y, x + w - 1, y + h - 1), col)
    return c


def fx_hojas():
    out = []
    for v in range(3):
        c = Cv(32, 32)
        if v == 0: m = c.ell(9, 8, 22, 23)
        elif v == 1: m = c.poly([(16, 4), (24, 14), (20, 26), (12, 26), (8, 14)])
        else: m = c.poly([(6, 18), (16, 6), (26, 16), (18, 26)])
        c.paint(m, T['fol'] if v != 2 else (P['ocre_c'], P['ocre_m'], P['tierra']), k=1)
        c.fill(c.line((16, 7), (16, 24), 1) if v < 2 else c.line((8, 19), (24, 15), 1), P['fol_o'] if v != 2 else P['tierra'])
        c.outline()
        out.append(c)
    return hstack(out)


def fx_impacto():
    out = []
    for i, r in enumerate((4, 9, 13, 8)):
        c = Cv(32, 32)
        col = P['crema'] if i != 1 else P['crema']
        c.fill(c.ell(16 - r // 2, 16 - r // 2, 16 + r // 2, 16 + r // 2), col)
        for k in range(8):
            a = k * math.pi / 4
            c.fill(c.line((16 + r * 0.6 * math.cos(a), 16 + r * 0.6 * math.sin(a)), (16 + r * 1.1 * math.cos(a), 16 + r * 1.1 * math.sin(a)), 1), P['niebla'] if i < 3 else P['piedra_c'])
        out.append(c)
    return hstack(out)


def fx_brillo():
    out = []
    for i in range(4):
        c = Cv(32, 32)
        a = i * math.pi / 8
        for k in range(2):
            ang = a + k * math.pi / 2
            c.fill(c.line((16 - 12 * math.cos(ang), 16 - 12 * math.sin(ang)), (16 + 12 * math.cos(ang), 16 + 12 * math.sin(ang)), 1), P['trigo'])
        c.fill(c.ell(13, 13, 18, 18), P['oro']); c.fill(c.rect(15, 15, 16, 16), P['crema'])
        out.append(c)
    return hstack(out)


def fx_chispa():
    c = Cv(32, 32)
    c.fill(c.rect(14, 14, 17, 17), P['fuego']); c.fill(c.rect(15, 15, 16, 16), P['trigo'])
    return c


def fx_niebla():
    c = Cv(128, 128)
    r = np.random.RandomState(2)
    Y, X = np.mgrid[0:128, 0:128]
    n = np.zeros((128, 128))
    for s, w in ((4, 0.5), (8, 0.3), (16, 0.2)):
        small = r.rand(128 // s + 2, 128 // s + 2)
        big = np.kron(small, np.ones((s, s)))[:128, :128]
        n += big * w
    d = np.sqrt(((X - 64) / 64.0) ** 2 + ((Y - 64) / 64.0) ** 2)
    a = np.clip((1 - d) * 1.4 * n * 1.6, 0, 1)
    levels = np.floor(a * 6) / 6.0 * 150           # bandas de alfa (sin degradado continuo)
    c.a[:, :, :3] = P['niebla']
    c.a[:, :, 3] = levels.astype(np.uint8)
    return c


# ======================================================== BUILD
def build():
    # items
    cells = []
    for name, fn, iid in ITEMS:
        ic = fn()
        save(ic, f'Items/singles/spr_item_{name}.png', iid)
        cells.append(ic)
    sh = sheet_grid(cells, 32, 8, 8)
    save(sh, 'Items/spr_item_hoja.png', 'IT-01..11')
    write_piskel(cells, 'items', 'Items/items.piskel', fps=1)
    # iconos UI
    cells = []
    for name, fn, uid in UI_ICONS:
        ic = ico(fn)
        save(ic, f'UI/Icons/singles/spr_ui_icono_{name}.png', uid)
        cells.append(ic)
    save(sheet_grid(cells, 64, 8, 8), 'UI/Icons/spr_ui_iconos.png', 'UI-01..18')
    write_piskel(cells, 'iconos_ui', 'UI/Icons/iconos_ui.piskel', fps=1)
    # elementos
    E = 'UI/Elements/'
    save(panel(96, 96, bw=8), E + 'spr_ui_marco_ventana.png', 'UI-19')
    for i, n in enumerate(('normal', 'sobre', 'pulsado')): save(button(i), E + f'spr_ui_boton_{n}.png', 'UI-20')
    save(slot(0), E + 'spr_ui_ranura_rapida_normal.png', 'UI-21'); save(slot(1), E + 'spr_ui_ranura_rapida_sel.png', 'UI-21')
    save(slot(0), E + 'spr_ui_ranura_inventario_normal.png', 'UI-22'); save(slot(1), E + 'spr_ui_ranura_inventario_sel.png', 'UI-22')
    save(bar_back(), E + 'spr_ui_barra_vida_fondo.png', 'UI-23')
    save(bar_fill(P['vida'], P['crema'], P['integ']), E + 'spr_ui_barra_vida_relleno.png', 'UI-23')
    save(bar_back(), E + 'spr_ui_barra_integridad_fondo.png', 'UI-24')
    save(bar_fill(P['integ'], P['fuego'], P['teja']), E + 'spr_ui_barra_integridad_relleno.png', 'UI-24')
    save(clock_back(), E + 'spr_ui_reloj_fondo.png', 'UI-25')
    save(bar_fill(P['trigo'], P['crema'], P['ocre_m'], 256, 32), E + 'spr_ui_reloj_relleno.png', 'UI-25')
    save(dialog_box(), E + 'spr_ui_caja_dialogo.png', 'UI-26')
    save(notif(), E + 'spr_ui_notificacion.png', 'UI-27')
    save(trade_panel(), E + 'spr_ui_ventana_comercio.png', 'UI-28')
    save(tab(True), E + 'spr_ui_pestana_activa.png', 'UI-29'); save(tab(False), E + 'spr_ui_pestana_inactiva.png', 'UI-29')
    save(slider_track(), E + 'spr_ui_deslizador_riel.png', 'UI-30'); save(knob(32, 32), E + 'spr_ui_deslizador_manija.png', 'UI-30')
    save(toggle(False), E + 'spr_ui_interruptor_off.png', 'UI-31'); save(toggle(True), E + 'spr_ui_interruptor_on.png', 'UI-31')
    save(scroll_track(), E + 'spr_ui_desplazamiento_riel.png', 'UI-32'); save(knob(24, 48), E + 'spr_ui_desplazamiento_manija.png', 'UI-32')
    pixfont.build_ttf(os.path.join(ART, 'UI', 'Elements', 'fnt_ui_tipografia.ttf'))
    MANIFEST.append({'id': 'UI-33', 'file': 'Assets/Art/UI/Elements/fnt_ui_tipografia.ttf', 'w': 0, 'h': 0})
    # vfx
    V = 'VFX/'
    save(fx_mota(), V + 'spr_vfx_desvanecimiento_anima.png', 'FX-01'); save(fx_polvo(), V + 'spr_vfx_polvo_tala.png', 'FX-02')
    save(fx_hojas(), V + 'spr_vfx_hoja_cae.png', 'FX-03'); save(fx_impacto(), V + 'spr_vfx_impacto_golpe.png', 'FX-04')
    save(fx_brillo(), V + 'spr_vfx_brillo_collectible.png', 'FX-05'); save(fx_chispa(), V + 'spr_vfx_chispa_fuego.png', 'FX-06')
    save(fx_niebla(), V + 'spr_vfx_niebla_nocturna.png', 'FX-07')


if __name__ == '__main__':
    build()
