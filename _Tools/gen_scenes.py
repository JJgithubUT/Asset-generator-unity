"""CN-01..CN-19 paneles de cinematica y BG-01..BG-05 pantallas. Se dibujan a 480x270 y se escalan x4 (Nearest)."""
import math
import numpy as np
from common import *
import gen_objects as O
import gen_tiles as TL
import pixfont
from spirits import candil_body

W, H = 480, 270


def new(): return Cv(W, H)


def sky(c, cols, y0=0, y1=None, blend=14):
    """Bandas de color con transicion tramada (Bayer). cols: lista de colores de arriba a abajo."""
    y1 = y1 or H
    n = len(cols)
    seg = (y1 - y0) / n
    for y in range(y0, y1):
        t = (y - y0) / seg
        i = min(int(t), n - 1)
        frac = (t - i) * seg
        col = cols[i]
        if i + 1 < n and frac > seg - blend:
            p = (frac - (seg - blend)) / blend
            for x in range(W):
                c.set(x, y, cols[i + 1] if bayer(x, y) < p else col)
        else:
            c.a[y, :, :3] = col
            c.a[y, :, 3] = 255


def put(c, spr, x, y, k=1, flip=False):
    """Coloca un sprite escalado k con su base centrada en (x, y)."""
    s = scale_nn(spr, k) if k != 1 else spr
    c.blit(s, int(x - s.w // 2), int(y - s.h), flip=flip)


def hills(c, y, amp, col_tones, seed=1, period=60):
    r = np.random.RandomState(seed)
    ph = r.rand(3) * 6
    for x in range(W):
        yy = y + amp * (math.sin(x / period + ph[0]) * 0.6 + math.sin(x / (period * 0.37) + ph[1]) * 0.4)
        c.fill(c.rect(x, int(yy), x, H - 1), col_tones[1])
        c.set(x, int(yy), col_tones[0])


def ground(c, y, cols, seed=1, density=0.05):
    c.fill(c.rect(0, y, W - 1, H - 1), cols[0])
    r = np.random.RandomState(seed)
    for _ in range(int((H - y) * W * density)):
        c.set(r.randint(0, W), r.randint(y, H), cols[1] if r.rand() < 0.5 else cols[2])


def stars(c, n, seed=3, ymax=120):
    r = np.random.RandomState(seed)
    for _ in range(n):
        c.set(r.randint(0, W), r.randint(0, ymax), P['niebla'] if r.rand() < 0.5 else P['lila'])


def disc(c, x, y, r, tones):
    c.paint(c.ell(x - r, y - r, x + r, y + r), tones, k=2)


def nightify(c, x0=0, x1=None, keep=()):
    """Convierte la region a la paleta de noche por luminancia (para la iluminacion nocturna)."""
    x1 = x1 or W
    ramp = [P['K'], P['noche'], P['azul_m'], P['violeta'], P['lila'], P['niebla']]
    reg = c.a[:, x0:x1]
    lum = (reg[:, :, 0] * 0.3 + reg[:, :, 1] * 0.55 + reg[:, :, 2] * 0.15) / 255.0
    idx = np.clip((lum ** 0.9 * len(ramp)).astype(int), 0, len(ramp) - 1)
    idx = np.where(lum > 0.82, 4, np.minimum(idx, 3))
    for i, col in enumerate(ramp):
        m = (idx == i) & (reg[:, :, 3] > 0)
        for kc in keep:
            m &= ~((reg[:, :, 0] == kc[0]) & (reg[:, :, 1] == kc[1]) & (reg[:, :, 2] == kc[2]))
        reg[m, :3] = col


def shop(c, cx, yb, k=3, lit=False, burned=False, closed=True):
    """Fachada de la tienda (se compone con tiles y objetos escalados)."""
    wall_w, wall_h = 11 * 32 * k // 3 * 1, 4 * 32 * k // 3
    x0 = cx - wall_w // 2
    ytop = yb - wall_h
    tile = TL.plaster_wall() if not burned else TL.brick_wall(T['piedra_d'], mortar=P['K'])
    for ty in range(0, wall_h, 32 * k // 3 if False else 32):
        pass
    big = scale_nn(tile, max(1, k * 2 // 3))
    ts = big.w
    for xx in range(x0, x0 + wall_w, ts):
        for yy in range(ytop, yb, ts):
            c.blit(big, xx, yy)
    # techo
    rf = scale_nn(TL.roof(0) if not burned else TL.roof(2), max(1, k * 2 // 3))
    roof_h = rf.h
    pts = [(x0 - 14, ytop + 6), (x0 + 8, ytop - roof_h + 6), (x0 + wall_w - 8, ytop - roof_h + 6), (x0 + wall_w + 14, ytop + 6)]
    tones = (P['ocre_m'], P['teja'], P['tierra_o']) if not burned else (P['piedra_m'], P['piedra_o'], P['K'])
    c.paint(c.poly(pts), tones, k=2)
    for yy in range(ytop - roof_h + 10, ytop + 4, 8):
        c.fill(c.rect(x0 - 10, yy, x0 + wall_w + 10, yy) & c.poly(pts), P['tierra_o'] if not burned else P['K'])
    if burned:  # techo hundido: hueco
        c.fill(c.poly([(cx - 30, ytop - roof_h + 10), (cx + 6, ytop - roof_h + 6), (cx + 16, ytop + 2), (cx - 20, ytop + 4)]), P['K'])
    # puerta
    d = scale_nn(O.door(0), max(1, k * 2 // 3)) if not burned else None
    dw = 64 * max(1, k * 2 // 3)
    if d is not None:
        c.blit(d, cx - dw // 2, yb - d.h)
    else:
        c.fill(c.rect(cx - 30, yb - 90, cx + 30, yb), P['K'])
        c.fill(c.rect(cx - 30, yb - 90, cx - 24, yb), P['madera'])
    # ventanas
    for sx in (-1, 1):
        wx = cx + sx * wall_w // 3
        wm = c.rect(wx - 22, ytop + 30, wx + 22, ytop + 74)
        c.paint(wm, (P['madera'], P['tierra_o'], P['K']), k=2)
        c.fill(c.rect(wx - 17, ytop + 35, wx + 17, ytop + 69), P['noche'] if (lit or True) else P['azul_m'])
        if lit and not burned:
            c.fill(c.rect(wx - 17, ytop + 35, wx + 17, ytop + 69), P['trigo'])
            c.fill(c.rect(wx - 17, ytop + 35, wx + 17, ytop + 40), P['crema'])
        c.fill(c.rect(wx, ytop + 35, wx, ytop + 69), P['tierra_o']); c.fill(c.rect(wx - 17, ytop + 52, wx + 17, ytop + 52), P['tierra_o'])
        if burned:
            c.fill(c.line((wx - 17, ytop + 35), (wx + 17, ytop + 69), 2), P['K'])
    # faroles de fachada
    for sx in (-1, 1):
        put(c, O.lamp(1 if lit else 0), cx + sx * (dw // 2 + 28), yb - 40, max(1, k * 2 // 3))
    # letrero
    if not burned:
        c.paint(c.rect(cx - 40, ytop + 6, cx + 40, ytop + 22), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
        for i in range(5):
            c.fill(c.rect(cx - 30 + i * 13, ytop + 12, cx - 24 + i * 13, ytop + 16), P['trigo'] if lit else P['ocre_c'])
    # escalon
    c.paint(c.rect(cx - dw // 2 - 8, yb - 4, cx + dw // 2 + 8, yb + 3), T['piedra'], k=1)


# ----------------------------------------------------------------------- escenas
OAKS = [O.oak(i) for i in range(3)]


def forest_row(c, y, n, k, x0=0, x1=W, seed=1, tint=None):
    r = np.random.RandomState(seed)
    xs = np.linspace(x0, x1, n)
    for x in xs:
        put(c, OAKS[r.randint(0, 3)], x + r.randint(-8, 8), y + r.randint(-4, 4), k, flip=bool(r.randint(0, 2)))


def road(c, y0):
    c.fill(c.poly([(W // 2 - 30, y0), (W // 2 + 30, y0), (W + 40, H), (-40, H)]), P['ocre_c'])
    r = np.random.RandomState(4)
    for _ in range(400):
        x, y = r.randint(0, W), r.randint(y0, H)
        if c.a[y, x, 3] and tuple(c.a[y, x, :3]) == P['ocre_c']:
            c.set(x, y, P['ocre_m'])


def scene_cn01():
    c = new()
    sky(c, [P['trigo'], P['ocre_c'], P['crema']], 0, 150)
    hills(c, 140, 10, T['fol'][::1], 2)
    ground(c, 150, (P['fol_m'], P['fol_c'], P['fol_o']), 5)
    for row, (yy, kk, nn) in enumerate(((150, 2, 9), (160, 3, 6))):
        forest_row(c, yy, nn, kk, -10, W + 10, 10 + row)
    road(c, 156)
    # carruaje
    cx, yb = 250, 235
    c.paint(c.rect(cx - 50, yb - 60, cx + 50, yb - 20), (P['ocre_m'], P['madera'], P['tierra_o']), k=2)
    c.paint(c.poly([(cx - 56, yb - 60), (cx - 40, yb - 80), (cx + 40, yb - 80), (cx + 56, yb - 60)]), (P['ocre_m'], P['teja'], P['tierra_o']), k=2)
    c.fill(c.rect(cx - 36, yb - 52, cx - 10, yb - 32), P['noche']); c.fill(c.rect(cx + 10, yb - 52, cx + 36, yb - 32), P['noche'])
    for x in (cx - 34, cx + 34):
        c.paint(c.ell(x - 18, yb - 36, x + 18, yb), (P['ocre_m'], P['madera'], P['tierra_o']), k=2)
        c.fill(c.ell(x - 12, yb - 30, x + 12, yb - 6), P['tierra_o'])
        for a in range(4):
            ang = a * math.pi / 4
            c.fill(c.line((x - 13 * math.cos(ang), yb - 18 - 13 * math.sin(ang)), (x + 13 * math.cos(ang), yb - 18 + 13 * math.sin(ang)), 1), P['ocre_c'])
    c.fill(c.rect(cx - 52, yb - 62, cx + 52, yb - 60), P['K'])
    c.fill(c.line((cx + 50, yb - 40), (cx + 90, yb - 30), 2), P['madera'])
    return c


def scene_cn02():
    c = new()
    sky(c, [P['noche'], P['azul_m'], P['violeta']], 0, 190)
    stars(c, 50)
    ground(c, 220, (P['azul_m'], P['noche'], P['violeta']), 3)
    shop(c, 240, 232, 3, lit=False)
    nightify(c)
    return c


def scene_cn03():
    c = new()
    c.fill(c.rect(0, 0, W - 1, H - 1), P['tierra_o'])
    big = scale_nn(TL.planks(1, (P['madera'], P['tierra_o'], P['K'])), 2)
    for x in range(0, W, 64):
        for y in range(150, H, 64): c.blit(big, x, y)
    for x in range(0, W, 64):
        for y in range(0, 150, 64): c.blit(scale_nn(TL.plaster_wall(), 2) if False else scale_nn(TL.brick_wall(T['tierra'], mortar=P['tierra_o']), 2), x, y)
    put(c, O.shelf(1), 90, 160, 3); put(c, O.shelf(0), 390, 160, 3)
    put(c, O.counter(), 240, 250, 4)
    cd = candil_body(0)
    put(c, cd, 240, 114, 4)
    # ventana nocturna
    c.paint(c.rect(210, 20, 270, 90), (P['madera'], P['tierra_o'], P['K']), k=2); c.fill(c.rect(216, 26, 264, 84), P['noche'])
    c.fill(c.rect(239, 26, 241, 84), P['tierra_o'])
    nightify(c, 0, W) if False else None
    return c


def scene_cn04():
    c = new()
    sky(c, [P['trigo'], P['ocre_c'], P['crema']], 0, 120)
    hills(c, 110, 8, T['fol'], 3)
    ground(c, 120, (P['fol_m'], P['fol_c'], P['fol_o']), 7)
    r = np.random.RandomState(8)
    n = 12
    pos = []
    for row, (yy, kk, cnt) in enumerate(((150, 2, 5), (200, 3, 4), (258, 3, 3))):
        for i in range(cnt):
            pos.append((60 + i * (360 / max(cnt - 1, 1)) + r.randint(-14, 14), yy, kk))
    for (x, y, k) in pos[:n]:
        put(c, OAKS[r.randint(0, 3)], x, y, k)
    return c


def counter_scene(c, who='inq'):
    c.fill(c.rect(0, 0, W - 1, H - 1), P['tierra_o'])
    big = scale_nn(TL.brick_wall(T['tierra'], mortar=P['tierra_o']), 2)
    for x in range(0, W, 64):
        for y in range(0, 170, 64): c.blit(big, x, y)
    fl = scale_nn(TL.planks(1, (P['madera'], P['tierra_o'], P['K'])), 2)
    for x in range(0, W, 64):
        for y in range(170, H, 64): c.blit(fl, x, y)
    put(c, O.shelf(1), 60, 170, 3)
    put(c, O.counter(), 280, 262, 4)


def scene_cn05():
    c = new()
    counter_scene(c)
    # recaudador: figura envuelta en capa oscura con sombrero, mano extendida
    x, yb = 130, 262
    robe = (P['piedra_m'], P['piedra_o'], P['K'])
    c.paint(c.poly([(x - 36, yb), (x - 26, yb - 110), (x + 26, yb - 110), (x + 36, yb)]), robe, k=2)
    c.paint(c.ell(x - 18, yb - 160, x + 18, yb - 118), (P['crema'], P['crema'], P['ocre_c']), k=2)
    c.paint(c.ell(x - 40, yb - 142, x + 40, yb - 128), robe, k=2); c.paint(c.rect(x - 22, yb - 172, x + 22, yb - 140), robe, k=2)
    c.fill(c.rect(x - 10, yb - 148, x - 6, yb - 146), P['K']); c.fill(c.rect(x + 6, yb - 148, x + 10, yb - 146), P['K'])
    c.paint(c.line((x + 20, yb - 100), (x + 70, yb - 86), 12), robe, k=1)
    c.paint(c.ell(x + 66, yb - 96, x + 82, yb - 80), (P['madera'], P['tierra_o'], P['K']), k=1)
    for i in range(5):
        c.paint(c.ell(210 + i * 14, 196 - (i % 2) * 6, 222 + i * 14, 206 - (i % 2) * 6), (P['oro'], P['trigo'], P['ocre_m']), k=1)
    return c


def scene_cn06():
    c = new()
    sky(c, [P['crema'], P['ocre_c'], P['trigo']], 0, 140)
    hills(c, 130, 10, T['fol'], 4)
    ground(c, 140, (P['fol_m'], P['fol_c'], P['fol_o']), 4)
    # casas de fondo
    for x in (60, 170, 400):
        c.paint(c.rect(x - 34, 110, x + 34, 150), (P['crema'], P['crema'], P['piedra_c']), k=1)
        c.paint(c.poly([(x - 42, 112), (x - 24, 86), (x + 24, 86), (x + 42, 112)]), (P['ocre_m'], P['teja'], P['tierra_o']), k=2)
        c.fill(c.rect(x - 6, 124, x + 6, 150), P['madera'])
    road(c, 150)
    put(c, O.cart(), 300, 250, 4)
    put(c, O.stump(), 60, 258, 3); put(c, O.stump(), 430, 240, 2)
    return c


def mexico_poly(c, ox, oy, s, col):
    """Silueta esquematica de Mexico (poligono simplificado)."""
    pts = [(0, 6), (14, 4), (26, 10), (34, 18), (36, 24), (30, 28), (26, 34), (22, 40), (24, 46), (18, 44), (12, 36), (8, 28), (4, 20), (-2, 14),
           (-6, 6), (-8, 0), (-14, -10), (-20, -22), (-24, -34), (-32, -40), (-40, -36), (-38, -26), (-30, -20), (-26, -10), (-14, -4)]
    pts = [(ox + x * s, oy + y * s) for x, y in pts]
    m = c.poly(pts)
    c.paint(m, col, k=2)
    # peninsula de Yucatan y Baja California
    c.paint(c.poly([(ox + 26 * s, oy + 30 * s), (ox + 40 * s, oy + 28 * s), (ox + 44 * s, oy + 38 * s), (ox + 34 * s, oy + 36 * s)]), col, k=1)
    c.paint(c.poly([(ox - 40 * s, oy - 36 * s), (ox - 46 * s, oy - 22 * s), (ox - 38 * s, oy - 4 * s), (ox - 36 * s, oy - 24 * s)]), col, k=1)
    return m


def data_plate(c, x0, y0, x1, y1):
    """Placa para la cifra dominante (el valor exacto lo aporta el Documento de Proyecto 1.4.6)."""
    c.fill(c.rect(x0, y0, x1, y1), P['K'])
    c.paint(c.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2), (P['azul_m'], P['noche'], P['noche']), k=1)
    c.fill(c.rect(x0 + 6, y0 + 6, x1 - 6, y1 - 6), P['noche'])
    c.fill(c.rect(x0 + 6, y0 + 6, x1 - 6, y0 + 6), P['lila'])


def source_tag(c):
    pixfont.draw_text(c, 14, H - 22, 'Fuente: CONAFOR', P['piedra_c'])


def dark_bg(c):
    c.fill(c.rect(0, 0, W - 1, H - 1), P['noche'])
    for y in range(H):
        for x in range(W):
            if (x + y) % 6 == 0 and (x // 3 + y // 3) % 3 == 0: c.set(x, y, P['azul_m'])


def scene_cn07():
    c = new(); dark_bg(c)
    mexico_poly(c, 190, 140, 2.7, (P['fol_m'], P['fol_o'], P['K']))
    mexico_poly(c, 190, 140, 2.7, (P['fol_c'], P['fol_m'], P['fol_o']))
    data_plate(c, 270, 90, 460, 190)
    source_tag(c)
    return c


def scene_cn08():
    c = new(); dark_bg(c)
    for i, k in enumerate((3, 2, 1)):
        put(c, OAKS[i % 3], 90 + i * 100, 200, k)
    for x in (320, 380):
        put(c, O.stump(), x - 30, 215, 1)
    c.fill(c.rect(24, 205, 300, 207), P['piedra_m'])
    data_plate(c, 290, 70, 465, 160)
    source_tag(c)
    return c


def scene_cn09():
    c = new()
    sky(c, [P['crema'], P['ocre_c'], P['trigo']], 0, 110)
    hills(c, 105, 8, T['fol'], 5)
    ground(c, 115, (P['fol_m'], P['fol_c'], P['fol_o']), 7)
    r = np.random.RandomState(9)
    for (x, y, k) in ((50, 170, 2), (440, 170, 2), (90, 240, 3), (400, 245, 3)):
        put(c, OAKS[r.randint(0, 3)], x, y, k)
    for (x, y) in ((140, 185), (340, 190), (170, 250), (300, 255), (20, 255), (460, 215)):
        put(c, O.stump(), x, y, 2)
    c.fill(c.rect(160, 90, 320, 150), P['noche'])         # zona neutra: Unity escribe el numero encima
    c.fill(c.rect(162, 92, 318, 148), P['azul_m'])
    return c


def scene_cn10():
    c = new()
    snow = (P['crema'], P['niebla'], P['piedra_c'])
    sky(c, [P['niebla'], P['crema'], P['piedra_c']], 0, 130)
    ground(c, 130, snow, 2, 0.03)
    put(c, O.stall((P['piedra_o'], P['piedra_m']), O.ex_inq), 340, 175, 3)
    from gen_characters import draw_human
    from char_styles import cliente_style
    for i, kind in enumerate(('campesino', 'artesano', 'dama', 'base', 'campesino')):
        spr = draw_human('lat', {}, cliente_style(kind))
        put(c, spr, 60 + i * 44, 240 - i * 6, 2)
    r = np.random.RandomState(1)
    for _ in range(140):
        c.set(r.randint(0, W), r.randint(0, H), P['crema'])
    return c


def scene_cn11():
    c = new()
    sky(c, [P['niebla'], P['crema'], P['piedra_c']], 0, 130)
    ground(c, 130, (P['crema'], P['niebla'], P['piedra_c']), 3, 0.03)
    put(c, O.stall((P['piedra_o'], P['piedra_m']), O.ex_inq), 330, 170, 3)
    put(c, O.woodpile(), 110, 262, 3); put(c, O.woodpile(), 200, 240, 2); put(c, O.woodpile(), 40, 215, 2)
    put(c, O.woodpile(), 160, 205, 1)
    return c


def bar_axes(c):
    c.fill(c.rect(70, 50, 72, 226), P['piedra_c']); c.fill(c.rect(70, 226, 420, 228), P['piedra_c'])
    for y in range(66, 226, 32): c.fill(c.rect(66, y, 70, y), P['piedra_m'])


def scene_cn12():
    c = new(); dark_bg(c)
    bar_axes(c)
    for (x, h, col, yr) in ((120, 100, (P['fol_c'], P['fol_m'], P['fol_o']), '2001'), (270, 170, (P['fuego'], P['teja'], P['tierra_o']), '2018')):
        c.paint(c.rect(x, 226 - h, x + 90, 225), col, k=2)
        pixfont.draw_text(c, x + 14, 236, yr, P['crema'], 2)
        data_plate(c, x - 4, 226 - h - 38, x + 94, 226 - h - 6)
    source_tag(c)
    return c


def scene_cn13():
    c = new(); dark_bg(c)
    icons = [lambda x, y: (c.paint(c.ell(x, y, x + 24, y + 24), T['fol'], k=1)),
             lambda x, y: (c.paint(c.rect(x + 8, y, x + 16, y + 24), T['tierra'], k=1), c.paint(c.ell(x, y - 6, x + 24, y + 8), T['fol'], k=1)),
             lambda x, y: c.paint(c.poly([(x + 12, y - 4), (x + 24, y + 26), (x, y + 26)]), (P['trigo'], P['fuego'], P['teja']), k=1),
             lambda x, y: c.paint(c.rect(x, y, x + 24, y + 22), T['piedra'], k=1)]
    for i in range(4):
        y = 40 + i * 52
        c.paint(c.ell(26, y, 62, y + 36), (P['trigo'], P['ocre_m'], P['tierra']), k=2)
        pixfont.draw_text(c, 38, y + 9, str(i + 1), P['K'], 2)
        icons[i](84, y + 6)
        data_plate(c, 128, y - 2, 452, y + 40)
    source_tag(c)
    return c


def hand_acorn(c):
    skin = T['piel']
    c.paint(c.ell(110, 150, 380, 330), skin, k=3)                         # palma
    for i, (x0, x1, y0) in enumerate(((120, 160, 120), (170, 214, 100), (224, 268, 104), (278, 318, 124))):
        c.paint(c.rect(x0, y0, x1, 190), skin, k=2)
        c.paint(c.ell(x0, y0 - 6, x1, y0 + 20), skin, k=2)
    c.paint(c.poly([(330, 200), (385, 150), (410, 176), (356, 236)]), skin, k=2)   # pulgar
    ac = O.acorn(None, True)
    put(c, ac, 245, 200, 6)


def scene_cn14():
    c = new()
    c.fill(c.rect(0, 0, W - 1, H - 1), P['tierra_o'])
    sky(c, [P['azul_m'], P['violeta'], P['tierra']], 0, 270, 30)
    # puño con manga de lino al fondo
    c.paint(c.poly([(60, 270), (100, 190), (380, 190), (430, 270)]), (P['crema'], P['crema'], P['piedra_c']), k=2)
    hand_acorn(c)
    return c


def scene_cn15():
    c = new()
    sky(c, [P['crema'], P['ocre_c'], P['trigo']], 0, 110)
    hills(c, 105, 8, T['fol'], 6)
    ground(c, 115, (P['ocre_m'], P['ocre_c'], P['tierra']), 8)
    r = np.random.RandomState(12)
    for (x, y, k) in ((50, 170, 2), (440, 175, 2), (260, 130, 1)):
        put(c, OAKS[r.randint(0, 3)], x, y, k)
    for (x, y) in ((110, 190), (200, 230), (320, 200), (390, 250), (60, 250), (450, 235), (240, 165), (150, 150), (360, 145)):
        put(c, O.stump(), x, y, 2)
    c.fill(c.rect(160, 205, 320, 262), P['noche']); c.fill(c.rect(162, 207, 318, 260), P['azul_m'])
    return c


def scene_cn16():
    c = new()
    sky(c, [P['crema'], P['trigo'], P['ocre_c'], P['crema']], 0, 150, 18)
    disc(c, 240, 120, 30, (P['crema'], P['oro'], P['trigo']))
    hills(c, 140, 8, T['fol'], 1)
    ground(c, 150, (P['fol_m'], P['fol_c'], P['fol_o']), 3)
    r = np.random.RandomState(15)
    for i in range(5):
        put(c, O.sapling(2), 60 + i * 90, 200 + (i % 2) * 22, 3)
    for i in range(3):
        put(c, O.sapling(1), 110 + i * 130, 255, 3)
    for i in range(6):
        put(c, O.sapling(0), 40 + i * 80, 160, 2)
    return c


def scene_cn17():
    c = new()
    sky(c, [P['crema'], P['ocre_c'], P['piedra_c']], 0, 120)
    ground(c, 120, (P['piedra_m'], P['piedra_c'], P['piedra_o']), 5, 0.05)
    cb = scale_nn(TL.cobble(3), 2)
    for x in range(0, W, 64):
        for y in range(130, H, 64): c.blit(cb, x, y)
    put(c, O.stall((P['trigo'], P['crema']), O.ex_tomas), 110, 175, 3)
    put(c, O.stall((P['piedra_o'], P['piedra_m']), O.ex_inq), 370, 175, 3)
    put(c, O.stall((P['fol_m'], P['fol_c']), O.ex_elvira), 240, 160, 2)
    put(c, O.lamp(1), 240, 255, 4)
    nightify(c, 240, W)
    c.fill(c.rect(239, 0, 240, H - 1), P['K'])
    return c


def scene_cn18():
    c = new()
    sky(c, [P['K'], P['noche'], P['azul_m']], 0, 200)
    stars(c, 90, 5)
    disc(c, 400, 50, 16, (P['niebla'], P['lila'], P['violeta']))
    ground(c, 225, (P['noche'], P['azul_m'], P['K']), 2)
    shop(c, 240, 238, 3, lit=True)
    nightify(c, 0, W, keep=(P['trigo'], P['fuego'], P['oro']))
    # ventanas encendidas se mantienen; resto en paleta de noche
    for (x, y) in ((60, 245), (130, 255), (350, 252), (420, 244), (30, 262), (460, 262)):
        put(c, O.stump(), x, y, 2)
    return c


def scene_cn19():
    c = new()
    sky(c, [P['violeta'], P['lila'], P['ocre_c'], P['trigo']], 0, 220, 20)
    ground(c, 225, (P['piedra_o'], P['piedra_m'], P['K']), 6)
    shop(c, 240, 238, 3, burned=True)
    r = np.random.RandomState(6)
    for _ in range(160):
        x, y = r.randint(0, W), r.randint(225, H)
        c.set(x, y, P['piedra_m'] if r.rand() < 0.5 else P['K'])
    for (x, y, k) in ((90, 250, 2), (380, 255, 2)):
        put(c, O.stump(), x, y, k)
    return c


SCENES = {f'CN-{i:02d}': f for i, f in enumerate(
    [scene_cn01, scene_cn02, scene_cn03, scene_cn04, scene_cn05, scene_cn06, scene_cn07, scene_cn08, scene_cn09, scene_cn10, scene_cn11,
     scene_cn12, scene_cn13, scene_cn14, scene_cn15, scene_cn16, scene_cn17, scene_cn18, scene_cn19], 1)}
CN_NAMES = {1: ('cin01', 1), 2: ('cin01', 2), 3: ('cin01', 3), 4: ('cin01', 4), 5: ('cin02', 1), 6: ('cin02', 2), 7: ('cin02', 3), 8: ('cin02', 4),
            9: ('cin02', 5), 10: ('cin03', 1), 11: ('cin03', 2), 12: ('cin03', 3), 13: ('cin03', 4), 14: ('cin03', 5), 15: ('cin03', 6),
            16: ('cin04', 'a'), 17: ('cin04', 'b'), 18: ('cin04', 'c'), 19: ('cin04', 'd')}


# ----------------------------------------------------------------------- pantallas
def bg01():
    c = new()
    sky(c, [P['K'], P['noche'], P['azul_m']], 0, 200)
    stars(c, 80, 9)
    ground(c, 230, (P['noche'], P['azul_m'], P['K']), 4)
    s = new()
    shop(s, 380, 240, 3, lit=False)
    nightify(s)
    c.blit(s)
    # Candil encendida en verde cerca de la puerta
    cd = scale_nn(candil_body(1), 4)
    px, py = 262, 176
    c.blit(cd, px - 64, py - 64)
    for r_, col in ((26, P['azul_m']), (20, P['violeta'])):
        pass
    c.fill(c.ell(px - 14, py + 4, px + 14, py + 32), P['c_verde'])
    c.fill(c.ell(px - 8, py + 10, px + 8, py + 26), P['crema'])
    return c


def bg02():
    c = new()
    for y in range(0, H, 2): c.fill(c.rect(0, y, W - 1, y + 1), P['madera'] if (y // 2) % 2 == 0 else P['tierra_o'])
    for y in range(0, H, 24): c.fill(c.rect(0, y, W - 1, y), P['K'])
    c.paint(c.rect(30, 14, W - 31, H - 15), (P['crema'], P['crema'], P['ocre_c']), k=2)
    r = np.random.RandomState(3)
    for _ in range(300): c.set(r.randint(32, W - 32), r.randint(16, H - 16), P['ocre_c'])
    c.fill(c.rect(40, 24, W - 41, 24), P['ocre_m']); c.fill(c.rect(40, H - 25, W - 41, H - 25), P['ocre_m'])
    return c


def bg03():
    c = new(); dark_bg(c)
    c.fill(c.rect(24, 24, W - 25, 24), P['azul_m']); c.fill(c.rect(24, H - 25, W - 25, H - 25), P['azul_m'])
    return c


def bg04():
    c = new()
    sky(c, [P['K'], P['noche'], P['azul_m']], 0, 220)
    ground(c, 232, (P['noche'], P['azul_m'], P['K']), 4)
    s = new(); shop(s, 240, 244, 3, lit=False); nightify(s); c.blit(s)
    r = np.random.RandomState(5)
    for _ in range(260):
        x, y = r.randint(0, W), r.randint(0, H)
        c.fill(c.line((x, y), (x - 3, y + 9), 1), P['niebla'] if r.rand() < 0.6 else P['lila'])
    for (x, y) in ((120, 255), (330, 258), (420, 250)):
        c.fill(c.ell(x - 14, y, x + 14, y + 5), P['azul_m'])
    return c


def bg05():
    c = new()
    sky(c, [P['crema'], P['trigo'], P['ocre_c'], P['crema']], 0, 150, 18)
    disc(c, 380, 118, 26, (P['crema'], P['oro'], P['trigo']))
    hills(c, 140, 8, T['fol'], 2)
    ground(c, 150, (P['fol_m'], P['fol_c'], P['fol_o']), 6)
    forest_row(c, 190, 8, 2, 20, 460, 21)
    forest_row(c, 255, 6, 3, 40, 440, 22)
    return c


def build():
    for i, (cn, (grp, pn)) in enumerate(CN_NAMES.items(), 1):
        c = SCENES[f'CN-{cn:02d}']()
        fn = f'spr_cin_{grp}_panel{pn:02d}.png' if isinstance(pn, int) else f'spr_cin_{grp}_final{pn}.png'
        c.a[c.a[:, :, 3] == 0] = (*P['K'], 255)
        big = scale_nn(c, 4)
        save(big, 'Cinematics/' + fn, f'CN-{cn:02d}')
        write_piskel([c], fn[:-4], 'Cinematics/' + fn[:-4] + '.piskel', fps=1)
    for fn, f, bid in (('spr_bg_menu_principal', bg01, 'BG-01'), ('spr_bg_puntuacion', bg02, 'BG-02'), ('spr_bg_cierre_educativo', bg03, 'BG-03'),
                       ('spr_bg_fin_partida', bg04, 'BG-04'), ('spr_bg_creditos', bg05, 'BG-05')):
        c = f()
        c.a[c.a[:, :, 3] == 0] = (*P['K'], 255)
        save(scale_nn(c, 4), f'Screens/{fn}.png', bid)
        write_piskel([c], fn, f'Screens/{fn}.piskel', fps=1)


if __name__ == '__main__':
    build()
