"""TS-01..TS-06: tilesets de 32x32 (sin contorno, regla 4)."""
import numpy as np
from common import *

S = 32


def rng_of(seed): return np.random.RandomState(seed)


def noise(base, hi, lo, p_hi=0.10, p_lo=0.10, seed=0):
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), base)
    r = rng_of(seed)
    for y in range(S):
        for x in range(S):
            v = r.rand()
            if v < p_hi: c.set(x, y, hi)
            elif v < p_hi + p_lo: c.set(x, y, lo)
    return c


def tufts(c, col, n, seed, light=None):
    r = rng_of(seed + 77)
    for _ in range(n):
        x, y = r.randint(2, S - 3), r.randint(3, S - 2)
        c.set(x, y, col); c.set(x - 1, y - 1, col); c.set(x + 1, y - 1, col)
        if light: c.set(x, y - 1, light)


GRASS = {0: (P['fol_m'], P['fol_c'], P['fol_o']), 1: (P['fol_m'], P['trigo'], P['ocre_m']), 2: (P['ocre_m'], P['ocre_c'], P['tierra'])}
LEAF = {0: (P['tierra'], P['ocre_m'], P['tierra_o']), 1: (P['ocre_m'], P['ocre_c'], P['tierra']), 2: (P['tierra_o'], P['tierra'], P['K'])}
DIRT = {0: (P['ocre_m'], P['ocre_c'], P['tierra']), 1: (P['ocre_m'], P['ocre_c'], P['tierra']), 2: (P['tierra'], P['ocre_m'], P['tierra_o'])}


def grass(seed, st=0):
    b, h, l = GRASS[st]
    c = noise(b, h, l, 0.07, 0.08, seed)
    tufts(c, l, 4 if st < 2 else 2, seed, h if st < 2 else None)
    return c


def tall_grass(seed, st=0):
    b, h, l = GRASS[st]
    c = noise(l, b, h, 0.15, 0.04, seed)
    r = rng_of(seed + 5)
    for _ in range(14 - st * 4):
        x, y = r.randint(1, S - 2), r.randint(6, S - 1)
        for k in range(r.randint(4, 7)):
            c.set(x + (k // 3), y - k, b if k % 2 else h)
    return c


def leaf_litter(seed, st=0):
    b, h, l = LEAF[st]
    c = noise(b, h, l, 0.12, 0.10, seed)
    r = rng_of(seed + 9)
    for _ in range(9 - st * 2):
        x, y = r.randint(1, S - 3), r.randint(1, S - 3)
        c.set(x, y, h); c.set(x + 1, y, h); c.set(x + 1, y + 1, l)
    return c


def dirt(seed, st=0):
    b, h, l = DIRT[st]
    c = noise(b, h, l, 0.08, 0.09, seed)
    r = rng_of(seed)
    for _ in range(3):
        x, y = r.randint(2, S - 4), r.randint(2, S - 4)
        c.set(x, y, P['piedra_m']); c.set(x + 1, y, P['piedra_c'])
    return c


def cobble(seed, tones=None):
    pc, pm, po = tones or (P['piedra_c'], P['piedra_m'], P['piedra_o'])
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), po)
    r = rng_of(seed)
    y = 0
    while y < S:
        h = 8 if (y // 8) % 2 == 0 else 8
        x = -r.randint(0, 6)
        while x < S:
            w = r.randint(8, 12)
            m = c.rect(max(x, 0), y, min(x + w - 2, S - 1), y + h - 2)
            c.paint(m, (pc, pm, po), k=1)
            x += w
        y += h
    return c


def water(frame, seed=3):
    c = noise(P['azul_m'], P['niebla'], P['noche'], 0.0, 0.10, seed)
    r = rng_of(seed + 1)
    for i in range(7):
        x, y = (r.randint(2, 24) + frame * 4) % 28, r.randint(2, 28)
        c.set(x, y, P['niebla']); c.set(x + 1, y, P['niebla']); c.set(x + 2, y, P['lila'])
    return c


def planks(seed, tones=None):
    l, b, s = tones or (P['ocre_m'], P['madera'], P['tierra_o'])
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), b)
    for y in (0, 8, 16, 24):
        c.fill(c.rect(0, y, S - 1, y), s)
        c.fill(c.rect(0, y + 1, S - 1, y + 1), l)
    r = rng_of(seed)
    for row in range(4):
        x = r.randint(4, 26)
        c.fill(c.rect(x, row * 8, x, row * 8 + 7), s)
        for _ in range(3):
            c.set(r.randint(0, 31), row * 8 + r.randint(2, 6), s)
    return c


def brick_wall(tones=None, seed=1, mortar=None):
    l, b, s = tones or (P['piedra_c'], P['piedra_m'], P['piedra_o'])
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), mortar or s)
    for row in range(4):
        off = 0 if row % 2 == 0 else 8
        for bx in range(-8, S, 16):
            x0 = bx + off
            c.paint(c.rect(max(x0, 0), row * 8, min(x0 + 14, S - 1), row * 8 + 6), (l, b, s), k=1)
    return c


def plaster_wall(seed=2):
    c = noise(P['crema'], P['crema'], P['piedra_c'], 0.0, 0.06, seed)
    # entramado de madera
    c.fill(c.rect(0, 0, S - 1, 1), P['madera']); c.fill(c.rect(0, 30, S - 1, 31), P['madera'])
    c.fill(c.rect(0, 0, 1, S - 1), P['madera']); c.fill(c.rect(30, 0, 31, S - 1), P['madera'])
    return c


def roof(variant=0, seed=1):
    l, b, s = (P['ocre_m'], P['teja'], P['tierra_o'])
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), b)
    for row in range(4):
        y = row * 8
        c.fill(c.rect(0, y + 6, S - 1, y + 7), s)
        c.fill(c.rect(0, y, S - 1, y), l)
        off = 0 if row % 2 == 0 else 4
        for x in range(off, S, 8):
            c.fill(c.rect(x, y + 1, x, y + 5), s)
    if variant == 1:   # cumbrera
        c.fill(c.rect(0, 0, S - 1, 5), P['tierra_o']); c.fill(c.rect(0, 0, S - 1, 1), P['madera'])
    if variant == 2:   # alero
        c.fill(c.rect(0, 26, S - 1, 31), P['tierra_o']); c.fill(c.rect(0, 26, S - 1, 26), P['madera'])
    return c


def door_tile(part='bot'):
    c = Cv(S, S)
    c.fill(c.rect(0, 0, S - 1, S - 1), P['piedra_c'])
    m = c.rect(4, 0 if part == 'bot' else 6, 27, 31 if part == 'bot' else 31)
    c.paint(m, (P['madera'], P['tierra'], P['tierra_o']), k=2)
    for x in (10, 16, 22): c.fill(c.rect(x, 0, x, 31), P['tierra_o'])
    if part == 'bot': c.set(23, 16, P['trigo']); c.set(23, 17, P['ocre_m'])
    return c


def window_tile():
    c = brick_wall()
    c.paint(c.rect(7, 6, 24, 25), (P['madera'], P['tierra_o'], P['K']), k=2)
    c.fill(c.rect(10, 9, 21, 22), P['azul_m'])
    c.fill(c.rect(10, 9, 14, 12), P['niebla'])
    c.fill(c.rect(15, 9, 16, 22), P['tierra_o']); c.fill(c.rect(10, 15, 21, 16), P['tierra_o'])
    return c


def barrel(tint=0):
    c = grass_under = Cv(S, S)
    c.paint(c.ell(6, 3, 25, 29), (P['ocre_m'], P['madera'], P['tierra_o']), k=2)
    for y in (9, 21): c.fill(c.rect(7, y, 24, y), P['piedra_o'])
    c.fill(c.ell(8, 4, 23, 11), P['ocre_m'])
    c.outline()
    return c


def crate():
    c = Cv(S, S)
    c.paint(c.rect(5, 6, 26, 28), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
    c.fill(c.rect(5, 6, 26, 8), P['ocre_m'])
    c.fill(c.line((6, 9), (25, 27), 1), P['tierra_o']); c.fill(c.line((25, 9), (6, 27), 1), P['tierra_o'])
    c.outline()
    return c


def signpost():
    c = Cv(S, S)
    c.paint(c.rect(15, 14, 17, 30), T['maderat'], k=1)
    c.paint(c.rect(5, 5, 26, 15), (P['ocre_m'], P['madera'], P['tierra_o']), k=1)
    c.fill(c.rect(9, 9, 21, 9), P['tierra_o']); c.fill(c.rect(9, 12, 18, 12), P['tierra_o'])
    c.outline()
    return c


def puddle():
    c = Cv(S, S)
    m = c.ell(4, 12, 27, 24)
    c.paint(m, (P['niebla'], P['azul_m'], P['noche']), k=1)
    c.fill(c.rect(9, 15, 13, 15), P['niebla'])
    return c


def roots(seed):
    c = leaf_litter(seed)
    r = rng_of(seed)
    x, y = 0, r.randint(10, 22)
    while x < S:
        for d in range(2): c.set(x, y + d, P['tierra_o'])
        c.set(x, y - 1, P['madera'])
        x += 1
        if r.rand() < 0.4: y += r.choice([-1, 1])
    return c


def log_tile(part):
    c = leaf_litter(4)
    if part == 'l': m = c.ell(6, 8, 40, 26)
    elif part == 'r': m = c.ell(-8, 8, 26, 26)
    else: m = c.rect(0, 8, 31, 26)
    c.paint(m & c.rect(0, 8, 31, 26), (P['ocre_m'], P['madera'], P['tierra_o']), k=2)
    for x in (8, 17, 25): c.set(x, 14, P['tierra_o']); c.set(x + 1, 18, P['tierra_o'])
    if part == 'l': c.fill(c.ell(5, 9, 11, 25), P['ocre_c']); c.fill(c.ell(7, 12, 9, 22), P['ocre_m'])
    return c


def undergrowth(seed, st=0):
    c = leaf_litter(seed, st)
    b, h, l = GRASS[st]
    r = rng_of(seed + 3)
    for _ in range(3):
        x, y = r.randint(6, 24), r.randint(8, 24)
        m = c.ell(x - 5, y - 4, x + 5, y + 3)
        c.paint(m, (h, b, l), k=1)
    return c


def stepping_stone(seed):
    c = water(0, seed)
    r = rng_of(seed)
    x, y = r.randint(8, 14), r.randint(8, 14)
    c.paint(c.ell(x, y, x + 12, y + 9), T['piedra'], k=1)
    return c


def hoja_floor(tones, seed): return planks(seed, tones)


def plowed(wet=False, seed=0):
    base = (P['tierra'], P['tierra_o']) if not wet else (P['tierra_o'], P['K'])
    c = Cv(S, S); c.fill(c.rect(0, 0, S - 1, S - 1), base[0])
    for y in range(2, S, 6):
        c.fill(c.rect(0, y, S - 1, y + 2), base[1])
        c.fill(c.rect(0, y + 3, S - 1, y + 3), P['ocre_m'] if not wet else P['tierra'])
    if wet:
        r = rng_of(seed + 3)
        for _ in range(7): c.set(r.randint(0, 31), r.randint(0, 31), P['azul_m'])
    return c


def fence(part):
    c = Cv(S, S)
    wood = (P['ocre_m'], P['madera'], P['tierra_o'])
    if part in ('h', 'hl', 'hr'):
        c.paint(c.rect(0, 12, 31, 14), wood, k=1); c.paint(c.rect(0, 20, 31, 22), wood, k=1)
        xs = {'h': (14,), 'hl': (3,), 'hr': (28,)}[part]
        for x in xs: c.paint(c.rect(x - 1, 6, x + 1, 28), wood, k=1)
    elif part == 'v':
        c.paint(c.rect(13, 0, 15, 31), wood, k=1); c.paint(c.rect(18, 0, 20, 31), wood, k=1)
        c.paint(c.rect(11, 14, 22, 16), wood, k=1)
    c.outline()
    return c


def furrow_border(edge):
    c = grass(5)
    d = plowed()
    m = {'n': c.rect(0, 0, 31, 7), 's': c.rect(0, 24, 31, 31), 'w': c.rect(0, 0, 7, 31), 'e': c.rect(24, 0, 31, 31)}[edge]
    out = d.copy(); out.a[m] = c.a[m]
    return out


def rug(part):
    c = planks(1)
    cols = (P['teja'], P['integ'] if False else P['teja'], P['tierra_o'])
    m = {'c': c.rect(0, 0, 31, 31), 'n': c.rect(0, 6, 31, 31), 's': c.rect(0, 0, 31, 25), 'w': c.rect(6, 0, 31, 31), 'e': c.rect(0, 0, 25, 31),
         'nw': c.rect(6, 6, 31, 31), 'ne': c.rect(0, 6, 25, 31), 'sw': c.rect(6, 0, 31, 25), 'se': c.rect(0, 0, 25, 25)}[part]
    c.fill(m, P['teja'])
    if part == 'c':
        for i in range(0, 32, 8): c.fill(c.rect(i, 0, i + 1, 31), P['ocre_m'])
    return c


def shelf_back(variant):
    c = planks(2, (P['madera'], P['tierra_o'], P['K']))
    c.fill(c.rect(0, 0, 31, 31), P['tierra_o'])
    for y in (10, 22):
        c.paint(c.rect(0, y, 31, y + 3), T['madera'], k=1)
    if variant:
        for x in (3, 12, 21):
            c.paint(c.rect(x, 3, x + 6, 9), (P['ocre_c'], P['ocre_m'], P['tierra']), k=1)
            c.paint(c.rect(x + 1, 15, x + 7, 21), (P['fol_c'], P['fol_m'], P['fol_o']), k=1)
    return c


def column(part):
    c = Cv(S, S); c.fill(c.rect(0, 0, 31, 31), P['piedra_o'])
    m = c.rect(8, 0, 23, 31)
    c.paint(m, T['piedra'], k=2)
    if part == 'top': c.paint(c.rect(4, 0, 27, 8), T['piedra'], k=1)
    if part == 'base': c.paint(c.rect(4, 24, 27, 31), T['piedra'], k=1)
    return c


def iron_gate(part):
    c = Cv(S, S); c.fill(c.rect(0, 0, 31, 31), P['piedra_o'])
    for x in range(3, 32, 6):
        c.paint(c.rect(x, 0, x + 1, 31), (P['piedra_c'], P['piedra_m'], P['K']), k=1)
        c.set(x, 0, P['crema']) if False else None
    c.fill(c.rect(0, 8, 31, 9), P['K']); c.fill(c.rect(0, 22, 31, 23), P['K'])
    if part == 'top':
        for x in range(3, 32, 6): c.set(x, 0, P['piedra_c']); c.set(x + 1, 1, P['piedra_c'])
    return c


def steps(i):
    c = Cv(S, S); c.fill(c.rect(0, 0, 31, 31), P['piedra_m'])
    for k in range(4):
        y = k * 8
        c.fill(c.rect(0, y, 31, y + 1), P['piedra_c']); c.fill(c.rect(0, y + 6, 31, y + 7), P['piedra_o'])
    return c


def stained_glass(v):
    c = brick_wall(T['piedra'])
    cols = [(P['teja'], P['trigo'], P['azul_m']), (P['azul_m'], P['violeta'], P['teja']), (P['trigo'], P['fol_m'], P['violeta']), (P['violeta'], P['teja'], P['azul_m'])][v]
    m = c.poly([(8, 31), (8, 10), (16, 2), (24, 10), (24, 31)])
    c.paint(m, (P['piedra_c'], P['piedra_m'], P['piedra_o']), k=1)
    m2 = c.poly([(11, 29), (11, 11), (16, 5), (21, 11), (21, 29)])
    c.fill(m2, cols[0])
    c.fill(m2 & c.rect(0, 0, 31, 14), cols[1]); c.fill(m2 & c.rect(0, 20, 31, 31), cols[2])
    c.fill(c.rect(15, 5, 16, 31), P['K'])
    return c


def turned_earth(seed):
    c = dirt(seed, 2)
    r = rng_of(seed)
    for _ in range(4):
        x, y = r.randint(2, 24), r.randint(4, 26)
        c.paint(c.ell(x, y, x + 7, y + 4), (P['ocre_m'], P['tierra'], P['tierra_o']), k=1)
    return c


# -------------------------------------------------------------- Rule tiles (16 variantes)
def rule16(inner, outer, band=3, seed=0, style='soft'):
    """16 variantes por mascara N=1,E=2,S=4,W=8 (bit=1: hay vecino del mismo tipo)."""
    out = []
    r = rng_of(seed)
    jit = [r.randint(-1, 1) for _ in range(S)]
    for m in range(16):
        t = inner.copy()
        for bit, side in ((1, 'n'), (2, 'e'), (4, 's'), (8, 'w')):
            if m & bit: continue
            for i in range(S):
                d = band + jit[i]
                for k in range(max(1, d)):
                    if side == 'n': x, y = i, k
                    elif side == 's': x, y = i, S - 1 - k
                    elif side == 'w': x, y = k, i
                    else: x, y = S - 1 - k, i
                    t.a[y, x] = outer.a[y, x]
        # esquinas redondeadas donde faltan dos lados contiguos
        for (b1, b2, cx, cy) in ((1, 8, 0, 0), (1, 2, S - 1, 0), (4, 8, 0, S - 1), (4, 2, S - 1, S - 1)):
            if not (m & b1) and not (m & b2):
                for dy in range(4):
                    for dx in range(4):
                        if dx + dy < 4:
                            x = dx if cx == 0 else S - 1 - dx
                            y = dy if cy == 0 else S - 1 - dy
                            t.a[y, x] = outer.a[y, x]
        out.append(t)
    return out


def wall16(base):
    """Muro de piedra: bordes con remate oscuro (sin vecino) para armar muros de cualquier forma."""
    out = []
    for m in range(16):
        t = base.copy()
        cap = P['piedra_c']
        if not (m & 1): t.fill(t.rect(0, 0, 31, 4), P['piedra_c']); t.fill(t.rect(0, 5, 31, 5), P['piedra_o'])
        if not (m & 4): t.fill(t.rect(0, 28, 31, 31), P['piedra_o'])
        if not (m & 8): t.fill(t.rect(0, 0, 2, 31), P['piedra_o'])
        if not (m & 2): t.fill(t.rect(29, 0, 31, 31), P['piedra_o'])
        out.append(t)
    return out


class Sheet:
    def __init__(self, size):
        self.n = size // S
        self.c = Cv(size, size)
        self.count = 0

    def put(self, col, row, tile):
        assert col < self.n and row < self.n
        self.c.blit(tile, col * S, row * S)
        self.count += 1

    def block(self, col, row, tiles, cols=4):
        for i, t in enumerate(tiles):
            self.put(col + i % cols, row + i // cols, t)

    def row(self, col, row, tiles):
        for i, t in enumerate(tiles):
            self.put(col + i, row, t)


def ts01():
    s = Sheet(512)
    g = [grass(i) for i in range(4)]; d = [dirt(i) for i in range(3)]; cb = [cobble(i) for i in range(3)]
    s.block(0, 0, rule16(dirt(9), grass(9), 3, 1), 4)            # camino de tierra sobre pasto
    s.block(4, 0, rule16(grass(8), dirt(8), 3, 2), 4)            # borde de pasto sobre tierra
    s.block(8, 0, rule16(cobble(5), dirt(7), 3, 3), 4)           # empedrado de plaza con bordes
    s.row(0, 4, g); s.row(4, 4, d); s.row(7, 4, cb)
    s.row(0, 5, [brick_wall(seed=1), plaster_wall(), window_tile(), door_tile('top'), door_tile('bot'), brick_wall(T['tierra'], mortar=P['tierra_o'])])
    s.row(0, 6, [roof(0), roof(1), roof(2), roof(0, 2), puddle(), signpost(), barrel(), crate()])
    # variantes de pasto con flores/tierra, pasto alto de borde
    extra = []
    for i in range(6):
        t = grass(20 + i); r = rng_of(i)
        for _ in range(3): t.set(r.randint(2, 29), r.randint(2, 29), P['trigo'] if i % 2 else P['crema'])
        extra.append(t)
    s.row(0, 7, extra)
    s.row(0, 8, [tall_grass(i) for i in range(4)] + [dirt(30), dirt(31), cobble(12), cobble(13)])
    # rellenos (para llegar a ~90 piezas utiles)
    s.row(0, 9, [roof(1, 2), roof(2, 3), brick_wall(seed=4), plaster_wall(), planks(3), planks(4)])
    return s


def ts02(st=0, bank=None):
    s = Sheet(512)
    s.block(0, 0, rule16(water(0), dirt(4, 0), 3, 5), 4)         # arroyo cuadro 1
    s.block(4, 0, rule16(water(1), dirt(4, 0), 3, 5), 4)         # arroyo cuadro 2 (animacion)
    s.block(8, 0, rule16(leaf_litter(2), dirt(4), 3, 6), 4)      # hojarasca con borde a tierra
    s.row(0, 4, [leaf_litter(i) for i in range(4)] + [tall_grass(i) for i in range(4)])
    s.row(0, 5, [dirt(i) for i in range(3)] + [stepping_stone(i) for i in range(3)] + [roots(i) for i in range(3)])
    s.row(0, 6, [undergrowth(i) for i in range(4)] + [log_tile('l'), log_tile('m'), log_tile('r')])
    s.row(0, 7, [grass(i) for i in range(4)])
    return s


def ts03():
    s = Sheet(256)
    s.row(0, 0, [planks(i) for i in range(4)])
    s.block(0, 1, [rug(p) for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se')], 3)
    s.row(4, 1, [brick_wall(T['tierra'], mortar=P['tierra_o']), plaster_wall(), window_tile(), brick_wall(seed=3)])
    s.row(0, 4, [shelf_back(0), shelf_back(1), shelf_back(1), window_tile()])
    s.row(4, 4, [planks(5), plaster_wall()])
    return s


def ts04():
    s = Sheet(256)
    s.row(0, 0, [plowed(False, 0), plowed(False, 1), plowed(True, 0), plowed(True, 1)])
    s.row(0, 1, [furrow_border(e) for e in 'nsew'])
    s.row(0, 2, [fence(p) for p in ('h', 'hl', 'hr', 'v')])
    s.row(0, 3, [grass(i) for i in range(4)])
    return s


def ts05():
    s = Sheet(512)
    s.block(0, 0, wall16(brick_wall()), 4)                       # muro de piedra del atrio
    s.block(4, 0, rule16(cobble(5), dirt(7, 2), 3, 7), 4)        # piso de piedra con borde a tierra
    s.row(0, 4, [cobble(i, (P['piedra_m'], P['piedra_o'], P['K'])) for i in range(4)] + [turned_earth(i) for i in range(3)])
    s.row(0, 5, [column('top'), column('mid'), column('base'), iron_gate('top'), iron_gate('mid'), steps(0), steps(1), steps(2)])
    s.row(0, 6, [planks(i, (P['piedra_m'], P['piedra_o'], P['K'])) for i in range(3)] + [stained_glass(i) for i in range(4)])
    s.row(0, 7, [dirt(i, 2) for i in range(3)] + [leaf_litter(i, 2) for i in range(3)])
    return s


def ts06():
    s = Sheet(512)
    row = 0
    for st in (1, 2):
        s.row(0, row, [leaf_litter(i, st) for i in range(4)] + [tall_grass(i, st) for i in range(4)])
        s.row(0, row + 1, [dirt(i, st) for i in range(3)] + [undergrowth(i, st) for i in range(4)] + [grass(i, st) for i in range(3)])
        row += 3
    return s


def build():
    mapping = {'TS-01': ('spr_tile_pueblo.png', ts01), 'TS-02': ('spr_tile_bosque.png', ts02), 'TS-03': ('spr_tile_tienda.png', ts03),
               'TS-04': ('spr_tile_huerto.png', ts04), 'TS-05': ('spr_tile_cementerio.png', ts05), 'TS-06': ('spr_tile_bosque_estados.png', ts06)}
    for tid, (fn, f) in mapping.items():
        sh = f()
        save(sh.c, 'Tilesets/' + fn, tid)
        write_piskel([sh.c], fn[:-4], 'Tilesets/' + fn[:-4] + '.piskel', fps=1)
        print(tid, sh.count, 'tiles')


if __name__ == '__main__':
    build()
