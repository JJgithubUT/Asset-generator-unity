"""Candil (PJ-02/03), animas (EN-02/03) y Glotglot (EN-04): figuras fantasmales."""
import math
import numpy as np
from common import *

# ---------------------------------------------------------------- Candil
def candil_body(frame, mode='flotar'):
    """32x32, centro. Cuerpo sin abdomen luminoso (en su sitio queda la cavidad apagada)."""
    c = Cv(32, 32)
    if mode == 'flotar':
        dy = [0, -1, -2, -1][frame]
        wing = [-2, 0, 2, 0][frame]          # aleteo: alas arriba / abajo
        jit = 0
    else:
        dy = [-1, -2][frame]
        wing = [-5, -4][frame]
        jit = [-1, 1][frame]
    cx = 16 + jit
    # alas (detras del cuerpo)
    for sgn in (-1, 1):
        xc = cx + sgn * 9
        w0, w1 = (xc - 5, xc + 5)
        top = 6 + dy + wing
        wm = c.ell(w0, top, w1, top + 11)
        # recorte para que el ala sea una cuna que sale del cuerpo
        c.paint(wm, T['alas'], k=1)
        vein = c.line((cx + sgn * 5, 14 + dy), (xc + sgn * 2, top + 4), 1) & wm
        c.fill(vein, P['lila'])
    # abdomen apagado (cavidad donde va la capa de luz)
    c.paint(c.ell(cx - 4, 19 + dy, cx + 4, 28 + dy), (P['azul_m'], P['noche'], P['K']), k=1)
    # cuerpo
    c.paint(c.ell(cx - 7, 7 + dy, cx + 7, 21 + dy), T['candil'], k=2)
    # antenas
    for sgn in (-1, 1):
        c.fill(c.line((cx + sgn * 3, 8 + dy), (cx + sgn * 6, 3 + dy + (1 if mode == 'alerta' else 0)), 1), P['violeta'])
        c.set(cx + sgn * 6, 2 + dy + (1 if mode == 'alerta' else 0), P['niebla'])
    # ojos grandes
    for sgn in (-1, 1):
        ex = cx + sgn * 3
        r = 2 if mode == 'flotar' else 3
        c.fill(c.ell(ex - r + (0 if sgn < 0 else 1), 10 + dy, ex + r - 1 + (0 if sgn < 0 else 1), 10 + dy + 2 * r - 1), P['niebla'])
        c.set(ex + (0 if sgn < 0 else 1), 11 + dy + (r - 1), P['K'])
        if r == 3: c.set(ex + (0 if sgn < 0 else 1), 12 + dy + (r - 1), P['K'])
    c.outline()
    return c


def candil_luz(frame):
    """Capa de luz: abdomen + halo en BLANCO PURO #FFFFFF. Alineada con el cuerpo (mismo dy)."""
    c = Cv(32, 32)
    dy = [0, -1, -2, -1][frame]
    cx = 16
    halo = c.ell(cx - 8, 19 + dy - 2, cx + 8, 28 + dy + 3)
    c.fill(halo, WHITE, 70)
    halo2 = c.ell(cx - 6, 19 + dy - 1, cx + 6, 28 + dy + 2)
    c.fill(halo2, WHITE, 130)
    c.fill(c.ell(cx - 4, 19 + dy, cx + 4, 28 + dy), WHITE, 255)
    return c


# ---------------------------------------------------------------- Animas
def _ghost_masks(shape, cx, top, s, kind, phase, d, lunge=0.0, arms=(0, 0), lean=0.0):
    H, W = shape
    Y, X = np.mgrid[0:H, 0:W]
    u = (X - cx) / s
    v = (Y - top) / s
    if d == 'lat':
        u = -u if False else u
    if kind == 'veloz':
        hr, hw0, hw1, hem0 = 6.2, 3.8, 6.6, 47
    else:
        hr, hw0, hw1, hem0 = 8.5, 6.6, 12.5, 35
    # inclinacion (lean): desplaza columnas segun la altura
    ul = u - lean * (v / 30.0)
    hy = 8.0
    head = ((ul / hr) ** 2 + ((v - hy) / hr) ** 2) <= 1.0
    if kind == 'veloz':
        # capucha apuntada hacia arriba
        head |= (np.abs(ul) <= (hr * (1 - np.clip((hy - 3 - v) / 9.0, 0, 1)) * 0.0 + np.clip((v + 4) / 9.0, 0, 1) * hr * 0.6)) & (v >= -4) & (v < hy - 3)
    t = np.clip((v - (hy + 3)) / (hem0 - hy - 3), 0, 1)
    hw = hw0 + (hw1 - hw0) * t ** 0.9
    wave = 2.4 * np.sin(0.8 * ul + phase) + (np.floor(ul) % 3 == 0) * 1.6 + (np.floor(ul) % 5 == 0) * 1.0
    hem = hem0 + wave
    body = (v >= hy + 2) & (np.abs(ul) <= hw) & (v <= hem)
    if d == 'lat':
        # figura de perfil: cola larga que se arrastra hacia atras (izquierda)
        trail = (ul < 0) & (v >= hy + 4) & (v <= hem0 - 4 + wave) & (np.abs(ul) <= hw + (-ul) * 0.35)
        body = (v >= hy + 2) & (ul <= hw * 0.65) & (ul >= -hw - 6) & (v <= hem + (ul < 0) * 3 * 0)
        body &= (v <= hem0 + wave + np.clip(-ul, 0, 99) * 0.18)
    # brazos: mangas rotas colgando (se pintan con lineas)
    ax_l, ay_l = arms[0] if isinstance(arms[0], (tuple, list)) else (0, arms[0])
    ax_r, ay_r = arms[1] if isinstance(arms[1], (tuple, list)) else (0, arms[1])
    return u, v, head, body, (ax_l, ay_l, ax_r, ay_r)


def ghost(d, frame_t, kind='errante', lunge=0.0, arms=((0, 0), (0, 0)), bob=0, scale=1.0, size=64,
          tones=None, alpha=205, phase_off=0.0, fade=None, lean=0.0, hollow=True):
    """Dibuja una anima. frame_t: fase (0..1) del ciclo."""
    c = Cv(size, size)
    tones = tones or (T['espectro_c'] if kind == 'veloz' else T['espectro'])
    s = scale
    cx = size / 2 + (lunge * 6 if d == 'lat' else 0)
    top = (size * 0.30 if kind == 'errante' else size * 0.20) + bob
    if d == 'sur': top += lunge * 4 * s
    if d == 'nor': top -= lunge * 4 * s
    phase = 2 * math.pi * frame_t + phase_off
    u, v, head, body, (alx, aly, arx, ary) = _ghost_masks((size, size), cx, top, s, kind, phase, d, lunge, arms, lean)
    mask = head | body
    # brazos como mangas colgantes (poligonos)
    def sleeve(sx, sy, hx, hy_):
        p0 = (cx + sx * s, top + sy * s)
        p1 = (cx + hx * s, top + hy_ * s)
        return c.line(p0, p1, max(3, int(4 * s)))
    if kind == 'veloz':
        shoulders = ((-4, 16), (4, 16)); hands = ((-7 + alx, 30 + aly), (7 + arx, 30 + ary))
    else:
        shoulders = ((-9, 17), (9, 17)); hands = ((-14 + alx, 31 + aly), (14 + arx, 31 + ary))
    if lunge > 0.4 and d == 'sur':
        hands = ((-13, 25), (13, 25))
    if d == 'lat':
        sl = sleeve(2, 17, 8 + alx + lunge * 8, 25 + aly)
        mask |= sl
    else:
        mask |= sleeve(shoulders[0][0], shoulders[0][1], hands[0][0], hands[0][1])
        mask |= sleeve(shoulders[1][0], shoulders[1][1], hands[1][0], hands[1][1])
    # estela de cenizas sueltas (isleos) bajo el dobladillo
    rng = np.random.RandomState(int(frame_t * 100) + (7 if kind == 'veloz' else 3))
    hem_y = top + (47 if kind == 'veloz' else 35) * s
    for _ in range(6 if kind == 'errante' else 9):
        px = int(cx + rng.randint(-12, 13) * s * (0.5 if kind == 'veloz' else 1))
        py = int(hem_y + rng.randint(1, 8))
        if 0 <= px < size - 1 and 0 <= py < size - 1 and rng.rand() < 0.7:
            mask[py, px] = True
    if fade is not None:  # desvanecer: se disuelve desde abajo
        ys = np.arange(size)[:, None]
        cut = top + (fade['cut']) * s
        rng2 = np.random.RandomState(11 + int(fade['k']))
        noise = rng2.rand(size, size)
        keep = (ys < cut + (noise - 0.5) * 12)
        keep &= noise > fade['gap']
        mask &= keep
    k = 2 if s >= 1.0 else 1
    c.paint(mask, tones, k=k, alpha=alpha)
    # hueco de la capucha (sin rostro definido): vacio oscuro con punteado
    if hollow and d != 'nor':
        hx0 = -3.2 if d == 'sur' else 1.0
        hx1 = 3.2 if d == 'sur' else 7.6
        if kind == 'veloz': hx0, hx1 = (-2.2, 2.2) if d == 'sur' else (0.6, 6.0)
        void = (u >= hx0) & (u <= hx1) & (np.abs(v - 9.0) <= 3.6 + (0 if kind == 'errante' else -0.6)) & head & mask
        void &= ((u - (0 if d == 'sur' else 4.3)) / ((hx1 - hx0) / 2)) ** 2 + ((v - 9.0) / 3.8) ** 2 <= 1.0
        c.fill(void, P['noche'], 240)
        if d == 'sur':
            yy, xx = np.nonzero(void)
            for y_, x_ in zip(yy, xx):
                if (x_ + y_) % 2 == 0 and v[y_, x_] > 10.5: c.set(x_, y_, P['violeta'], 240)
    # contorno: 1px negro con alfa parcial en el borde exterior
    solid = c.a[:, :, 3] > 0
    n = np.zeros_like(solid)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n |= shift(solid, dx, dy)
    edge = n & ~solid
    c.fill(edge, P['K'], 170)
    return c


def ghost_frames(kind, d, anim):
    out = []
    if anim == 'flotar':
        for i in range(4):
            t = i / 4
            bob = [0, -1, -2, -1][i]
            sway = ((math.sin(2 * math.pi * t) * 2), 0)
            arms = ((int(round(sway[0])), 0), (int(round(-sway[0])), 0))
            out.append(ghost(d, t, kind, bob=bob, arms=arms, lean=0.8 * math.sin(2 * math.pi * t) * (1 if d != 'lat' else 0)))
    elif anim == 'atacar':
        for i, lg in enumerate([-0.3, 1.0, 0.5]):
            arms = [((2, -6), (-2, -6)), ((-3, -2), (3, -2)), ((0, 3), (0, 3))][i]
            if kind == 'veloz':
                lg = [-0.5, 1.2, 0.6][i]
            out.append(ghost(d, i / 3 + 0.1, kind, lunge=max(lg, 0), arms=arms, bob=-1 if i == 0 else 0,
                             scale=1.0 + (0.12 if i == 1 else 0), lean=(-1.5 if (i == 0) else (2.5 if i == 1 else 0.5))))
    return out


def ghost_fade(kind, d='sur'):
    out = []
    for i in range(6):
        fade = {'cut': 50 - i * 9, 'gap': 0.04 + i * 0.1, 'k': i}
        a = max(40, 205 - i * 25)
        out.append(ghost(d, 0.2, kind, fade=fade, alpha=a, bob=-i % 2))
    return out


# ---------------------------------------------------------------- Glotglot 128x128
def glotglot_frame(anim, i, n):
    size = 128
    c = Cv(size, size)
    t = i / n
    ph = 2 * math.pi * t
    if anim == 'idle':
        bob = [0, -2, -3, -1][i % 4]; sway = math.sin(ph) * 2; lunge = 0; arm_up = 0
    elif anim == 'avanzar':
        bob = [0, -2, 0, -2][i % 4]; sway = math.sin(ph) * 3; lunge = [0.2, 0.5, 0.8, 0.4][i % 4]; arm_up = 0
    else:  # golpear
        bob = [0, -3, -5, 2, 0][i % 5]; sway = 0; lunge = [0, 0.1, 0.2, 1.0, 0.4][i % 5]; arm_up = [0.3, 0.8, 1.0, -0.3, 0][i % 5]
    layers = [
        # (cx offset, top, scale, tonos, alpha, phase)
        (-38, 36, 1.5, (P['violeta'], P['azul_m'], P['noche']), 150, 1.0),
        (40, 38, 1.45, (P['violeta'], P['azul_m'], P['noche']), 150, 2.1),
        (-22, 30, 1.9, (P['lila'], P['violeta'], P['azul_m']), 175, 3.0),
        (24, 30, 1.85, (P['lila'], P['violeta'], P['azul_m']), 175, 4.0),
    ]
    for (dx, top, sc, tones, a, pho) in layers:
        g = ghost('sur', t, 'errante', scale=sc, size=size, tones=tones, alpha=a, phase_off=pho + ph,
                  bob=bob * 0.5 + 2 * math.sin(ph + pho), hollow=True, lean=sway * 0.3)
        # recolocar la figura: ghost() siempre centra en size/2, la desplazamos
        gg = Cv(size, size)
        gg.a = np.roll(g.a, int(dx + sway * 0.5), axis=1)
        # recorte vertical (top) por desplazamiento
        gg.a = np.roll(gg.a, int(top - 38) - 14, axis=0)
        c.blit(gg)
    # figura principal gigante
    main = ghost('sur', t, 'errante', scale=2.5, size=size, tones=T['espectro'], alpha=205, phase_off=ph,
                 bob=bob + 4, lean=sway * 0.5, hollow=True, lunge=lunge * 0.8)
    mm = Cv(size, size)
    mm.a = np.roll(main.a, -12 - int(10 * lunge) + (0 if anim != 'golpear' else int(arm_up * -6)), axis=0)
    c.blit(mm)
    # brazos enormes de tela: rematan en cenizas
    cx = 64 + sway
    topy = 56 + bob
    for sgn in (-1, 1):
        sx, sy = cx + sgn * 26, topy + 8
        if anim == 'golpear':
            hx, hy = cx + sgn * (30 - 12 * lunge), topy - 22 * arm_up + 40 * (1 - arm_up) * (lunge > 0.9) + 26 * (1 - arm_up) * 0.0 + 10
            if lunge > 0.9: hy = topy + 46
        else:
            hx, hy = cx + sgn * 36 + sway * 0.5, topy + 38 + (bob % 3)
        sl = c.line((sx, sy), (hx, hy), 9)
        c.paint(sl, T['espectro'], k=2, alpha=205)
        # manos: cenizas dispersas
        for k in range(5):
            px, py = int(hx + sgn * k * 2 - 2), int(hy + 4 + k)
            c.set(px, py, P['niebla'], 180)
    # cenizas flotantes
    rng = np.random.RandomState(5 + i + len(anim))
    for _ in range(40):
        x, y = rng.randint(4, 124), rng.randint(6, 124)
        if c.a[y, x, 3] == 0 and rng.rand() < 0.5:
            c.set(x, y, P['piedra_m'] if rng.rand() < 0.5 else P['piedra_c'], 255)
    # contorno semitransparente exterior (aplicado sobre el conjunto)
    solid = c.a[:, :, 3] > 0
    n = np.zeros_like(solid)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n |= shift(solid, dx, dy)
    c.fill(n & ~solid, P['K'], 170)
    return c


def glotglot_fade(n=8):
    out = []
    base = glotglot_frame('idle', 0, 4)
    rng = np.random.RandomState(99)
    noise = rng.rand(128, 128)
    ys = np.arange(128)[:, None]
    for i in range(n):
        f = base.copy()
        cut = 120 - i * (130 / n)
        keep = (ys < cut + (noise - 0.5) * 22) & (noise > 0.03 + i * 0.1)
        f.a[~keep, 3] = 0
        f.a[:, :, 3] = np.where(f.a[:, :, 3] > 0, np.maximum(40, f.a[:, :, 3].astype(int) - i * 20), 0).astype(np.uint8)
        out.append(f)
    return out
