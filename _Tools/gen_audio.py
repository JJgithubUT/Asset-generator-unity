"""MU-01..07 (.ogg Vorbis 44.1 kHz estereo, loop limpio) y SX-01..27 (.wav PCM16 44.1 kHz mono, pico -3 dBFS)."""
import os, math
import numpy as np
import soundfile as sf
from common import AUDIO, MANIFEST, ROOT

SR = 44100
RNG = np.random.RandomState(1234)


def t_(d): return np.arange(int(SR * d)) / SR


def env(n, a=0.005, d=0.1, curve=4.0, sustain=0.0):
    t = np.arange(n) / SR
    e = np.exp(-curve * t / max(d, 1e-4))
    e = np.maximum(e, sustain)
    att = np.minimum(1.0, t / max(a, 1e-4))
    return e * att


def lp(x, fc):
    a = 1 - math.exp(-2 * math.pi * fc / SR)
    y = np.empty_like(x)
    s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s)
        y[i] = s
    return y


def hp(x, fc): return x - lp(x, fc)


def bp(x, f0, f1): return hp(lp(x, f1), f0)


def noise(d): return RNG.uniform(-1, 1, int(SR * d))


def sine(f, d, phase=0): return np.sin(2 * math.pi * f * t_(d) + phase)


def sweep(f0, f1, d, wave='sine', expo=True):
    t = t_(d)
    f = f0 * (f1 / f0) ** (t / d) if expo else f0 + (f1 - f0) * t / d
    ph = 2 * math.pi * np.cumsum(f) / SR
    if wave == 'sine': return np.sin(ph)
    if wave == 'tri': return 2 / math.pi * np.arcsin(np.sin(ph))
    if wave == 'sq': return np.sign(np.sin(ph)) * 0.6
    if wave == 'saw': return 2 * ((ph / (2 * math.pi)) % 1) - 1


def fit(x, d):
    n = int(SR * d)
    return np.pad(x, (0, max(0, n - len(x))))[:n]


def mixl(*parts, d=None):
    n = max(len(p) for p in parts) if d is None else int(SR * d)
    out = np.zeros(n)
    for p in parts: out[:len(p)] += p[:n]
    return out


def at(x, off, total):
    out = np.zeros(int(SR * total)); i = int(SR * off)
    seg = x[:len(out) - i]
    out[i:i + len(seg)] = seg
    return out


def bell(f, d, parts=((1, 1.0), (2.76, 0.6), (5.4, 0.35), (8.9, 0.2)), curve=5.0):
    n = int(SR * d)
    out = np.zeros(n)
    for r, a in parts: out += a * sine(f * r, d) * env(n, 0.002, d / (1 + r * 0.25), curve)
    return out


def thud(f0, f1, d, curve=7): return sweep(f0, f1, d) * env(int(SR * d), 0.002, d, curve)


def save_sfx(name, x, sid):
    x = np.asarray(x, dtype=np.float64)
    x = x - np.mean(x[:50]) * 0
    # fundido de 3 ms al inicio y final para evitar clics
    f = int(SR * 0.003)
    if len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    pk = np.max(np.abs(x)) or 1.0
    x = x / pk * (10 ** (-3 / 20))
    p = os.path.join(AUDIO, 'SFX', name + '.wav')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    sf.write(p, x, SR, subtype='PCM_16')
    MANIFEST.append({'id': sid, 'file': os.path.relpath(p, ROOT).replace('\\', '/'), 'w': 0, 'h': 0})


# ------------------------------------------------------------------------- SFX
def sfx_paso_tierra(i):
    d = 0.2
    n = noise(d)
    return mixl(lp(n, 500 + i * 120) * env(len(n), 0.002, 0.05, 5), thud(110 - i * 8, 60, d) * 0.6)


def sfx_paso_piedra(i):
    d = 0.2
    n = bp(noise(d), 800, 3200 + i * 400)
    return mixl(n * env(len(n), 0.001, 0.035, 6), sine(1300 + i * 140, d) * env(int(SR * d), 0.001, 0.03, 8) * 0.3)


def sfx_salto():
    d = 0.3
    return mixl(sweep(220, 560, d, 'tri') * env(int(SR * d), 0.01, 0.25, 3) * 0.7, bp(noise(d), 600, 2200) * env(int(SR * d), 0.02, 0.2, 4) * 0.3)


def sfx_aterrizaje():
    d = 0.2
    return mixl(thud(120, 50, d, 9), lp(noise(d), 700) * env(int(SR * d), 0.001, 0.06, 6) * 0.7)


def sfx_golpe_farol():
    d = 0.3
    wh = bp(noise(d), 500, 2500) * np.sin(np.linspace(0, math.pi, int(SR * d))) ** 2 * 0.5
    return mixl(wh, at(bell(920, 0.2, ((1, 1), (1.5, 0.5), (2.4, 0.3)), 7), 0.1, d) * 0.9)


def sfx_impacto():
    d = 0.2
    return mixl(thud(170, 70, d, 10), bp(noise(d), 300, 2500) * env(int(SR * d), 0.001, 0.05, 7) * 0.8)


def sfx_dano():
    d = 0.3
    return mixl(sweep(420, 140, d, 'saw') * env(int(SR * d), 0.003, 0.25, 4) * 0.55, lp(noise(d), 1800) * env(int(SR * d), 0.001, 0.08, 6) * 0.5)


def sfx_anima():
    d = 0.6
    t = t_(d)
    vib = 1 + 0.02 * np.sin(2 * math.pi * 7 * t)
    f = 520 * (0.45) ** (t / d) * vib
    ph = 2 * math.pi * np.cumsum(f) / SR
    tone = (np.sin(ph) + 0.4 * np.sin(2 * ph)) * (1 - t / d) ** 1.5
    sh = hp(noise(d), 3000) * (1 - t / d) ** 2 * 0.15
    return (tone * 0.7 + sh) * np.minimum(1, t / 0.03)


def sfx_recolectar():
    d = 0.4
    out = np.zeros(int(SR * d))
    for k in range(4):
        out += at(bp(noise(0.08), 1500, 5000) * env(int(SR * 0.08), 0.003, 0.05, 6) * (0.5 + 0.1 * k), 0.03 + k * 0.07, d)
    out += at(sweep(500, 800, 0.1, 'sine') * env(int(SR * 0.1), 0.005, 0.1, 5) * 0.4, 0.28, d)
    return out


def sfx_talar():
    d = 1.2
    out = np.zeros(int(SR * d))
    for k, off in enumerate((0.0, 0.22, 0.44)):
        hit = mixl(lp(noise(0.12), 1800) * env(int(SR * 0.12), 0.001, 0.04, 7), thud(190, 90, 0.12, 12) * 0.9, sine(320, 0.12) * env(int(SR * 0.12), 0.001, 0.05, 9) * 0.3)
        out += at(hit * (0.9 + 0.05 * k), off, d)
    # crujido y caida del arbol
    cr = lp(noise(0.5), 900) * (np.linspace(0.2, 1, int(SR * 0.5)) ** 2) * (0.6 + 0.4 * np.sign(np.sin(2 * math.pi * 40 * t_(0.5))))
    out += at(cr * 0.5, 0.62, d)
    out += at(mixl(thud(80, 35, 0.35, 5), lp(noise(0.35), 400) * env(int(SR * 0.35), 0.002, 0.2, 5)) * 1.1, 0.95, d)
    return out


def sfx_plantar_bellota():
    d = 0.5
    return mixl(lp(noise(0.3), 600) * env(int(SR * 0.3), 0.01, 0.15, 5), at(thud(95, 55, 0.2, 8) * 0.8, 0.12, d), at(bp(noise(0.2), 400, 1500) * env(int(SR * 0.2), 0.005, 0.1, 6) * 0.4, 0.25, d))


def sfx_plantar_semilla():
    d = 0.4
    out = np.zeros(int(SR * d))
    for k in range(5):
        out += at(bp(noise(0.05), 800, 3000) * env(int(SR * 0.05), 0.001, 0.025, 7) * 0.6, k * 0.06, d)
    return out + at(thud(110, 70, 0.15, 9) * 0.5, 0.25, d)


def sfx_cosechar():
    d = 0.4
    return mixl(hp(noise(0.06), 2500) * env(int(SR * 0.06), 0.001, 0.03, 7), at(sweep(400, 760, 0.18, 'tri') * env(int(SR * 0.18), 0.005, 0.15, 5) * 0.6, 0.06, d), at(bp(noise(0.15), 700, 2500) * env(int(SR * 0.15), 0.01, 0.08, 5) * 0.4, 0.2, d))


def sfx_moneda():
    d = 0.4
    return mixl(bell(1760, 0.25, ((1, 1), (2.01, 0.3)), 9) * 0.9, at(bell(2349, 0.3, ((1, 1), (2.01, 0.25)), 8) * 0.8, 0.07, d))


def sfx_rechazada():
    d = 0.3
    a = sweep(230, 215, 0.13, 'sq') * env(int(SR * 0.13), 0.002, 0.13, 3) * 0.5
    b = sweep(170, 150, 0.15, 'sq') * env(int(SR * 0.15), 0.002, 0.15, 3) * 0.5
    return lp(mixl(a, at(b, 0.13, d)), 1800)


def sfx_abrir():
    d = 0.2
    return mixl(sweep(420, 900, d, 'tri') * env(int(SR * d), 0.005, 0.15, 5) * 0.6, bp(noise(d), 1000, 4000) * env(int(SR * d), 0.01, 0.12, 5) * 0.2)


def sfx_cerrar():
    d = 0.2
    return mixl(sweep(800, 380, d, 'tri') * env(int(SR * d), 0.005, 0.15, 5) * 0.6, bp(noise(d), 800, 3000) * env(int(SR * d), 0.003, 0.08, 6) * 0.2)


def sfx_navegar():
    d = 0.1
    return sweep(700, 760, d, 'tri') * env(int(SR * d), 0.002, 0.07, 6)


def sfx_confirmar():
    d = 0.2
    return mixl(sine(600, 0.1) * env(int(SR * 0.1), 0.003, 0.08, 5) * 0.7, at(sine(900, 0.12) * env(int(SR * 0.12), 0.003, 0.1, 5) * 0.7, 0.07, d))


def sfx_candil_amarillo():
    d = 0.4
    out = np.zeros(int(SR * d))
    for k, f in enumerate((1180, 1580, 1180)):
        x = (sweep(f, f * 1.02, 0.1, 'sq') + 0.5 * sine(f * 2, 0.1)) * env(int(SR * 0.1), 0.002, 0.09, 3)
        out += at(x * 0.7, k * 0.12, d)
    return out


def sfx_campana():
    d = 1.5
    return bell(440, d, ((1, 1), (2.0, 0.55), (2.76, 0.5), (4.1, 0.3), (5.4, 0.25)), 3.5) + 0.2 * at(bell(220, 1.2, ((1, 1), (1.5, 0.3)), 3), 0.0, d)[:int(SR * d)]


def arp(notes, step, d, dur=0.4, curve=6):
    out = np.zeros(int(SR * d))
    for k, f in enumerate(notes):
        n = int(SR * dur)
        x = (sine(f, dur) + 0.3 * sine(f * 2, dur)) * env(n, 0.004, dur, curve)
        out += at(x * 0.6, k * step, d)
    return out


def sfx_completada():
    return arp([523.25, 659.25, 783.99, 1046.5], 0.12, 0.8, 0.45, 4)


def sfx_impuesto():
    d = 0.6
    return mixl(bell(1320, 0.3, ((1, 1), (2.01, 0.3)), 8) * 0.8, at(bell(990, 0.35, ((1, 1), (2.01, 0.3)), 7) * 0.8, 0.08, d), at(thud(160, 80, 0.2, 9) * 0.7, 0.25, d), at(sweep(500, 260, 0.25, 'tri') * env(int(SR * 0.25), 0.003, 0.2, 4) * 0.5, 0.3, d))


def sfx_mejora():
    d = 0.8
    a = arp([392, 523.25, 659.25, 783.99, 1046.5], 0.1, d, 0.45, 4)
    sp = hp(noise(0.4), 5000) * env(int(SR * 0.4), 0.05, 0.3, 4) * 0.15
    return mixl(a, at(sp, 0.35, d))


def sfx_robo():
    d = 0.5
    out = np.zeros(int(SR * d))
    out += at(hp(noise(0.12), 2500) * env(int(SR * 0.12), 0.001, 0.05, 6), 0.0, d)
    for k in range(7):
        out += at(bp(noise(0.06), 1500, 7000) * env(int(SR * 0.06), 0.001, 0.025, 6) * RNG.uniform(0.2, 0.6), 0.1 + k * RNG.uniform(0.03, 0.06), d)
    out += at(thud(240, 100, 0.2, 9) * 0.5, 0.05, d)
    return out


def sfx_rugido():
    d = 2.0
    t = t_(d)
    n = len(t)
    out = np.zeros(n)
    for k in range(6):
        f0 = RNG.uniform(70, 150)
        cont = f0 * (1 + 0.5 * np.sin(math.pi * t / d) ** 1.0) * (1 + 0.03 * np.sin(2 * math.pi * RNG.uniform(4, 7) * t))
        ph = 2 * math.pi * np.cumsum(cont) / SR
        v = np.zeros(n)
        for h in range(1, 14):
            fr = cont * h
            form = np.exp(-((fr - (500 + 400 * np.sin(math.pi * t / d))) / 350) ** 2) + 0.6 * np.exp(-((fr - 1500) / 500) ** 2)
            v += np.sin(h * ph + k) * form / h ** 0.5
        out += v
    out += lp(noise(d), 1200) * 0.8 * np.sin(math.pi * t / d) ** 1.2
    out *= np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.4)
    return out


def sfx_dialogo():
    d = 0.1
    return sine(520, d) * env(int(SR * d), 0.002, 0.06, 6) * 0.6


def build_sfx():
    for i in range(3): save_sfx(f'sfx_paso_tierra_{i + 1:02d}', sfx_paso_tierra(i), 'SX-01')
    for i in range(3): save_sfx(f'sfx_paso_piedra_{i + 1:02d}', sfx_paso_piedra(i), 'SX-02')
    items = [('saltar', sfx_salto, 'SX-03'), ('aterrizar', sfx_aterrizaje, 'SX-04'), ('golpe_farol', sfx_golpe_farol, 'SX-05'),
             ('impacto_enemigo', sfx_impacto, 'SX-06'), ('jugador_dano', sfx_dano, 'SX-07'), ('anima_desvanece', sfx_anima, 'SX-08'),
             ('recolectar', sfx_recolectar, 'SX-09'), ('talar', sfx_talar, 'SX-10'), ('plantar_bellota', sfx_plantar_bellota, 'SX-11'),
             ('plantar_semilla', sfx_plantar_semilla, 'SX-12'), ('cosechar', sfx_cosechar, 'SX-13'), ('moneda', sfx_moneda, 'SX-14'),
             ('compra_rechazada', sfx_rechazada, 'SX-15'), ('ventana_abrir', sfx_abrir, 'SX-16'), ('ventana_cerrar', sfx_cerrar, 'SX-17'),
             ('menu_navegar', sfx_navegar, 'SX-18'), ('confirmar', sfx_confirmar, 'SX-19'), ('candil_amarillo', sfx_candil_amarillo, 'SX-20'),
             ('campana_anochecer', sfx_campana, 'SX-21'), ('prueba_completada', sfx_completada, 'SX-22'), ('impuesto_cobrado', sfx_impuesto, 'SX-23'),
             ('mejora_comprada', sfx_mejora, 'SX-24'), ('robo_tienda', sfx_robo, 'SX-25'), ('rugido_glotglot', sfx_rugido, 'SX-26'),
             ('dialogo_avance', sfx_dialogo, 'SX-27')]
    for name, fn, sid in items: save_sfx('sfx_' + name, fn(), sid)


# ------------------------------------------------------------------------- MUSICA
def mhz(m): return 440.0 * 2 ** ((m - 69) / 12)


class Song:
    def __init__(self, bpm, bars):
        self.bpm, self.bars = bpm, bars
        self.beat = 60.0 / bpm
        self.dur = bars * 4 * self.beat
        self.N = int(round(self.dur * SR))
        self.L = np.zeros(self.N + SR * 4)
        self.R = np.zeros(self.N + SR * 4)

    def add(self, x, t, amp=1.0, pan=0.0):
        i = int(t * SR)
        if i >= self.N: return
        gl, gr = amp * math.cos((pan + 1) * math.pi / 4), amp * math.sin((pan + 1) * math.pi / 4)
        self.L[i:i + len(x)] += x * gl if i + len(x) <= len(self.L) else (x * gl)[:len(self.L) - i]
        self.R[i:i + len(x)] += x * gr if i + len(x) <= len(self.R) else (x * gr)[:len(self.R) - i]

    def finish(self, echo=((0.19, 0.28), (0.33, 0.2), (0.51, 0.13)), peak=0.89):
        N = self.N
        L = self.L[:N].copy(); R = self.R[:N].copy()
        L[:len(self.L) - N] += self.L[N:][:N]; R[:len(self.R) - N] += self.R[N:][:N]     # cola que envuelve al inicio (loop limpio)
        l0, r0 = L.copy(), R.copy()
        for dl, g in echo:
            k = int(dl * SR)
            L += g * np.roll(r0, k); R += g * np.roll(l0, k + 37)
        pk = max(np.max(np.abs(L)), np.max(np.abs(R)))
        return np.stack([L, R], axis=1) / pk * peak


def v_pluck(f, d, bright=1.0):
    n = int(SR * d)
    t = np.arange(n) / SR
    x = np.sin(2 * math.pi * f * t) + 0.45 * bright * np.sin(4 * math.pi * f * t) * np.exp(-6 * t) + 0.2 * np.sin(6 * math.pi * f * t) * np.exp(-9 * t)
    return x * np.exp(-3.2 * t / d) * np.minimum(1, t / 0.004)


def v_pad(f, d, att=0.6, rel=0.8, detune=0.004):
    n = int(SR * (d + rel))
    t = np.arange(n) / SR
    x = np.zeros(n)
    for h, a in ((1, 1.0), (2, 0.5), (3, 0.3), (4, 0.18), (5, 0.1)):
        for dt in (-detune, detune):
            x += a * np.sin(2 * math.pi * f * h * (1 + dt) * t + h)
    e = np.minimum(1, t / att) * np.where(t < d, 1.0, np.exp(-(t - d) * 5 / rel))
    return x * e * 0.25


def v_bass(f, d):
    n = int(SR * d)
    t = np.arange(n) / SR
    x = np.sin(2 * math.pi * f * t) + 0.35 * np.sin(4 * math.pi * f * t) + 0.12 * np.sin(6 * math.pi * f * t)
    return x * np.exp(-2.2 * t / d) * np.minimum(1, t / 0.006)


def v_choir(f, d, att=0.5, rel=0.7):
    n = int(SR * (d + rel))
    t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * math.pi * 5.2 * t + f)
    ph = 2 * math.pi * f * np.cumsum(vib) / SR
    x = np.zeros(n)
    for h in range(1, 14):
        fr = f * h
        w = np.exp(-((fr - 650) / 300) ** 2) + 0.7 * np.exp(-((fr - 1100) / 350) ** 2) + 0.3 * np.exp(-((fr - 2500) / 500) ** 2)
        x += np.sin(h * ph + h * 0.7) * w / h ** 0.4
    e = np.minimum(1, t / att) * np.where(t < d, 1.0, np.exp(-(t - d) * 5 / rel))
    return x * e * 0.3


def v_kick(d=0.35):
    n = int(SR * d)
    return sweep(110, 42, d) * np.exp(-9 * np.arange(n) / SR / d * 1.0) * 1.2


def v_tom(f=90, d=0.4):
    n = int(SR * d)
    return sweep(f * 1.6, f, d) * np.exp(-6 * np.arange(n) / SR / d) + 0.1 * lp(noise(d), 800) * np.exp(-12 * np.arange(n) / SR / d)


def v_shaker(d=0.08):
    n = int(SR * d)
    return hp(noise(d), 6000) * np.exp(-8 * np.arange(n) / SR / d) * 0.5


def v_wood(d=0.08, f=900):
    n = int(SR * d)
    return (sine(f, d) + 0.5 * sine(f * 1.6, d)) * np.exp(-14 * np.arange(n) / SR / d)


MINOR = [0, 2, 3, 5, 7, 8, 10]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
PHRYG = [0, 1, 3, 5, 7, 8, 10]
DORIAN = [0, 2, 3, 5, 7, 9, 10]


def chord(root, kind):
    return {'M': [0, 4, 7], 'm': [0, 3, 7], 'sus': [0, 5, 7], 'dim': [0, 3, 6], 'm7': [0, 3, 7, 10], 'M7': [0, 4, 7, 11], 'pw': [0, 7, 12]}[kind]


def melody_notes(scale, root, rng, bars, density, rng_range=(0, 9), start=5):
    """Genera frases de 8 compases que se repiten (A A B A) con paseo aleatorio por la escala."""
    def phrase():
        notes = []
        deg = start
        for b in range(8):
            t = 0.0
            while t < 4:
                if rng.rand() < density:
                    step = rng.choice([-2, -1, -1, 0, 1, 1, 2])
                    deg = int(np.clip(deg + step, rng_range[0], rng_range[1]))
                    ln = float(rng.choice([0.5, 1.0, 1.0, 1.5, 2.0]))
                    ln = min(ln, 4 - t)
                    notes.append((b * 4 + t, ln, deg))
                    t += ln
                else:
                    t += float(rng.choice([0.5, 1.0]))
        return notes
    A, B = phrase(), phrase()
    out = []
    order = ['A', 'A', 'B', 'A']
    for blk in range(bars // 8 + 1):
        ph = A if order[blk % 4] == 'A' else B
        for (t, ln, deg) in ph:
            if blk * 8 * 4 + t < bars * 4:
                out.append((blk * 32 + t, ln, deg))
    return out


def deg_to_midi(root, scale, deg):
    o, i = divmod(deg, len(scale))
    return root + scale[i] + 12 * o


def compose(cfg):
    rng = np.random.RandomState(cfg['seed'])
    S = Song(cfg['bpm'], cfg['bars'])
    root, scale, prog = cfg['root'], cfg['scale'], cfg['prog']
    layers = cfg['layers']
    b = S.beat
    mel = melody_notes(scale, root + 12, rng, cfg['bars'], cfg.get('mel_density', 0.6), cfg.get('mel_range', (0, 9)), cfg.get('mel_start', 4)) if 'melody' in layers else []
    for bar in range(cfg['bars']):
        sec = bar // 8
        active = cfg['sections'][sec % len(cfg['sections'])]
        t0 = bar * 4 * b
        rt, kind = prog[bar % len(prog)]
        cm = chord(rt, kind)
        base = root + rt
        if 'pad' in layers and 'pad' in active:
            for k, iv in enumerate(cm):
                S.add(v_pad(mhz(base + 12 + iv), 4 * b * 0.98, cfg.get('pad_att', 0.7)), t0, cfg.get('pad_amp', 0.8), pan=(k - 1) * 0.4)
        if 'drone' in layers and 'drone' in active and bar % 2 == 0:
            S.add(v_pad(mhz(root - 12), 8 * b, 1.5, 1.5), t0, 0.9, 0)
            S.add(v_pad(mhz(root - 5), 8 * b, 2.0, 1.5), t0, 0.5, -0.3)
        if 'bass' in layers and 'bass' in active:
            pat = cfg.get('bass_pat', [(0, 2), (2, 1), (3, 1)])
            for (bt, ln) in pat:
                iv = cm[0] if bt != 3 else cm[2 % len(cm)]
                S.add(v_bass(mhz(base - 12 + (iv if bt == 3 else 0)), ln * b * 0.95), t0 + bt * b, cfg.get('bass_amp', 0.9), 0)
        if 'arp' in layers and 'arp' in active:
            order = cfg.get('arp_order', [0, 1, 2, 1])
            step = cfg.get('arp_step', 0.5)
            n = int(4 / step)
            for k in range(n):
                iv = cm[order[k % len(order)] % len(cm)]
                S.add(v_pluck(mhz(base + 12 + iv + (12 if k % 8 == 7 else 0)), 1.0, 1.0), t0 + k * step * b, cfg.get('arp_amp', 0.45), pan=0.5 if k % 2 else -0.5)
        if 'kick' in layers and 'kick' in active:
            for bt in cfg.get('kick_beats', [0, 2]):
                S.add(v_kick(), t0 + bt * b, cfg.get('kick_amp', 0.9), 0)
        if 'tom' in layers and 'tom' in active:
            for bt in cfg.get('tom_beats', [1.5, 3.5]):
                S.add(v_tom(cfg.get('tom_f', 80) * (1 if bt % 2 else 1.2)), t0 + bt * b, 0.7, pan=-0.2)
        if 'shaker' in layers and 'shaker' in active:
            for k in range(8):
                S.add(v_shaker(), t0 + k * 0.5 * b, 0.35 if k % 2 else 0.5, pan=0.3)
        if 'wood' in layers and 'wood' in active:
            for bt in (1, 3):
                S.add(v_wood(), t0 + bt * b, 0.3, pan=-0.3)
        if 'choir' in layers and 'choir' in active:
            for k, iv in enumerate(cm):
                S.add(v_choir(mhz(base + 12 + iv + (12 if k == 2 else 0)), 4 * b * 0.98), t0, 0.7, pan=(k - 1) * 0.5)
        if 'ping' in layers and 'ping' in active and bar % cfg.get('ping_every', 2) == 0:
            for _ in range(2):
                S.add(v_pluck(mhz(root + 24 + int(rng.choice(scale))), 2.5, 1.5), t0 + float(rng.uniform(0, 3.5)) * b, 0.3, pan=float(rng.uniform(-0.8, 0.8)))
    for (t, ln, deg) in mel:
        sec = int(t // 32)
        if 'melody' not in cfg['sections'][sec % len(cfg['sections'])]: continue
        m = deg_to_midi(root + 12, scale, deg)
        voice = v_pluck(mhz(m), max(ln * b, 0.6) * 1.2, cfg.get('mel_bright', 1.0))
        S.add(voice, t * b, cfg.get('mel_amp', 0.8), pan=0.15)
    return S


SONGS = {
    'MU-01': ('mus_menu_principal', dict(seed=1, bpm=64, bars=24, root=57, scale=MINOR, mel_density=0.4, mel_amp=0.9,
              prog=[(0, 'm'), (0, 'm'), (8, 'M'), (8, 'M'), (5, 'M'), (5, 'M'), (7, 'M'), (7, 'm')], layers=['pad', 'melody', 'arp'],
              sections=[['pad', 'melody'], ['pad', 'melody', 'arp'], ['pad', 'melody']], arp_step=1.0, arp_amp=0.3, arp_order=[0, 2, 1, 2], pad_att=1.2, pad_amp=0.6)),
    'MU-02': ('mus_pueblo_dia_otono', dict(seed=2, bpm=96, bars=48, root=50, scale=MAJOR, mel_density=0.65, mel_amp=0.8,
              prog=[(0, 'M'), (7, 'M'), (9, 'm'), (5, 'M'), (0, 'M'), (7, 'M'), (5, 'M'), (7, 'sus')],
              layers=['pad', 'bass', 'arp', 'melody', 'shaker', 'wood'],
              sections=[['pad', 'bass', 'arp'], ['pad', 'bass', 'arp', 'melody', 'shaker'], ['pad', 'bass', 'arp', 'melody', 'wood', 'shaker'], ['pad', 'bass', 'melody', 'shaker'], ['pad', 'bass', 'arp', 'melody', 'wood']],
              arp_step=0.5, bass_pat=[(0, 1.5), (2, 1), (3, 1)])),
    'MU-03': ('mus_pueblo_dia_invierno', dict(seed=3, bpm=80, bars=40, root=50, scale=DORIAN, mel_density=0.4, mel_amp=0.7,
              prog=[(0, 'm'), (5, 'M'), (7, 'm'), (5, 'M'), (0, 'm'), (10, 'M'), (5, 'M'), (7, 'sus')], layers=['pad', 'bass', 'arp', 'melody', 'wood'],
              sections=[['pad', 'bass'], ['pad', 'bass', 'melody'], ['pad', 'bass', 'arp', 'melody'], ['pad', 'melody', 'wood'], ['pad', 'bass', 'melody']],
              arp_step=1.0, arp_amp=0.35, pad_amp=0.7, bass_pat=[(0, 3)])),
    'MU-04': ('mus_pueblo_dia_primavera', dict(seed=4, bpm=112, bars=56, root=52, scale=MINOR, mel_density=0.75, mel_amp=0.8, mel_bright=1.4,
              prog=[(0, 'm'), (0, 'm'), (8, 'M'), (7, 'M'), (0, 'm'), (5, 'm'), (8, 'M'), (7, 'M')], layers=['pad', 'bass', 'arp', 'melody', 'shaker', 'tom'],
              sections=[['pad', 'bass', 'arp'], ['pad', 'bass', 'arp', 'melody', 'shaker'], ['pad', 'bass', 'arp', 'melody', 'shaker', 'tom'], ['pad', 'bass', 'arp', 'shaker', 'tom']],
              arp_step=0.5, arp_order=[0, 2, 1, 2, 0, 2, 1, 2], arp_amp=0.5, tom_beats=[3, 3.5], bass_pat=[(0, 1), (1, 1), (2, 1), (3, 1)])),
    'MU-05': ('mus_noche', dict(seed=5, bpm=72, bars=27, root=45, scale=PHRYG, mel_density=0.0, mel_amp=0,
              prog=[(0, 'm'), (1, 'sus'), (0, 'dim'), (6, 'm')], layers=['drone', 'pad', 'kick', 'tom', 'ping'],
              sections=[['drone', 'kick'], ['drone', 'pad', 'kick', 'tom'], ['drone', 'pad', 'kick', 'tom', 'ping']], kick_beats=[0, 2.75], tom_beats=[1.5, 3.25], tom_f=70, pad_amp=0.55, ping_every=1)),
    'MU-06': ('mus_jefe_final', dict(seed=6, bpm=120, bars=60, root=45, scale=PHRYG, mel_density=0.6, mel_amp=0.5, mel_bright=1.6,
              prog=[(0, 'm'), (0, 'm'), (1, 'M'), (0, 'm'), (0, 'm'), (8, 'M'), (7, 'M'), (6, 'dim')], layers=['choir', 'bass', 'kick', 'tom', 'arp', 'melody', 'drone'],
              sections=[['choir', 'bass', 'kick', 'drone'], ['choir', 'bass', 'kick', 'tom', 'arp'], ['choir', 'bass', 'kick', 'tom', 'arp', 'melody'], ['choir', 'bass', 'kick', 'tom', 'melody', 'drone']],
              kick_beats=[0, 1, 2, 3], kick_amp=0.8, tom_beats=[1.5, 3.5, 3.75], tom_f=65, arp_step=0.25, arp_order=[0, 0, 1, 0], arp_amp=0.35,
              bass_pat=[(0, 0.5), (0.5, 0.5), (1, 0.5), (1.5, 0.5), (2, 0.5), (2.5, 0.5), (3, 0.5), (3.5, 0.5)], bass_amp=0.8)),
    'MU-07': ('mus_finales_creditos', dict(seed=7, bpm=80, bars=40, root=48, scale=MAJOR, mel_density=0.5, mel_amp=0.8,
              prog=[(0, 'M'), (9, 'm'), (5, 'M'), (7, 'M'), (0, 'M'), (5, 'M'), (2, 'm'), (7, 'sus')], layers=['pad', 'bass', 'arp', 'melody'],
              sections=[['pad', 'melody'], ['pad', 'bass', 'melody', 'arp'], ['pad', 'bass', 'melody'], ['pad', 'melody', 'arp'], ['pad', 'bass', 'melody']],
              arp_step=1.0, arp_amp=0.35, pad_amp=0.9, bass_pat=[(0, 3)])),
}


def build_music(only=None):
    for mid, (name, cfg) in SONGS.items():
        if only and mid not in only: continue
        song = compose(cfg)
        data = song.finish()
        p = os.path.join(AUDIO, 'Music', name + '.ogg')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        d32 = data.astype(np.float32)
        with sf.SoundFile(p, 'w', SR, 2, format='OGG', subtype='VORBIS') as f:
            for i in range(0, len(d32), 4096): f.write(d32[i:i + 4096])
        MANIFEST.append({'id': mid, 'file': os.path.relpath(p, ROOT).replace('\\', '/'), 'w': 0, 'h': 0})
        print(mid, name, round(len(data) / SR, 2), 's')


if __name__ == '__main__':
    import sys
    if 'sfx' in sys.argv or len(sys.argv) == 1: build_sfx()
    if 'music' in sys.argv or len(sys.argv) == 1: build_music()
