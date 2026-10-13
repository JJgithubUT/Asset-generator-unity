"""Mercadieval - utilidades comunes del generador de assets (pixel art, paleta de 26 colores)."""
import os, json, base64, io
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ART = os.path.join(ROOT, 'Assets', 'Art')
AUDIO = os.path.join(ROOT, 'Assets', 'Audio')
SRC = os.path.join(ROOT, 'Assets', '_Source')


def hexrgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---- Paleta obligatoria (apartado 2) ----------------------------------------------------
PALETTE_LIST = [
    (1, 'Ocre claro', 'E8C07D', 'ocre_c'), (2, 'Ocre medio', 'C9924B', 'ocre_m'),
    (3, 'Tierra', '8B5A2B', 'tierra'), (4, 'Tierra oscura', '5A3821', 'tierra_o'),
    (5, 'Madera', '6B4226', 'madera'), (6, 'Piedra clara', 'B8AFA0', 'piedra_c'),
    (7, 'Piedra media', '8A8071', 'piedra_m'), (8, 'Piedra oscura', '4F4A42', 'piedra_o'),
    (9, 'Follaje claro', '7FA650', 'fol_c'), (10, 'Follaje medio', '4E7B35', 'fol_m'),
    (11, 'Follaje oscuro', '2E4F22', 'fol_o'), (12, 'Trigo', 'E3B23C', 'trigo'),
    (13, 'Rojo teja', 'A8412E', 'teja'), (14, 'Crema', 'F2E3C6', 'crema'),
    (15, 'Azul noche', '1B2340', 'noche'), (16, 'Azul medio', '2E3C63', 'azul_m'),
    (17, 'Violeta', '4A3B6B', 'violeta'), (18, 'Lila espectral', '8E7BB5', 'lila'),
    (19, 'Niebla', 'C3C9E0', 'niebla'),
    (20, 'Candil verde', '3FD16A', 'c_verde'), (21, 'Candil amarillo', 'F2C13D', 'c_amar'),
    (22, 'Fuego', 'E2622B', 'fuego'), (23, 'Integridad', 'C0392B', 'integ'),
    (24, 'Vida', 'D64550', 'vida'), (25, 'Oro', 'FFD35C', 'oro'),
    (26, 'Negro de contorno', '15121C', 'K'),
]
P = {k: hexrgb(h) for (_, _, h, k) in PALETTE_LIST}
WHITE = (255, 255, 255)
PAL_SET = set(P.values())

# familias de tres tonos (luz, base, sombra) -> regla 5
T = {
    'piel': (P['crema'], P['ocre_c'], P['ocre_m']),
    'madera': (P['ocre_m'], P['madera'], P['tierra_o']),
    'maderat': (P['tierra'], P['madera'], P['tierra_o']),
    'tierra': (P['ocre_m'], P['tierra'], P['tierra_o']),
    'ocre': (P['ocre_c'], P['ocre_m'], P['tierra']),
    'paja': (P['crema'], P['trigo'], P['ocre_m']),
    'piedra': (P['piedra_c'], P['piedra_m'], P['piedra_o']),
    'piedra_d': (P['piedra_m'], P['piedra_o'], P['K']),
    'fol': (P['fol_c'], P['fol_m'], P['fol_o']),
    'teja': (P['ocre_m'], P['teja'], P['tierra_o']),
    'tela': (P['crema'], P['piedra_c'], P['piedra_m']),
    'noche': (P['azul_m'], P['noche'], P['K']),
    'espectro': (P['niebla'], P['lila'], P['violeta']),
    'espectro_c': (P['crema'], P['niebla'], P['lila']),
    'candil': (P['lila'], P['violeta'], P['azul_m']),
    'alas': (P['crema'], P['niebla'], P['lila']),
}
K = P['K']


def shade_of(t, n):
    """Variante de tono: n=0 luz, 1 base, 2 sombra"""
    return t[n]


# ---- Mascaras ------------------------------------------------------------------------------
def _img(w, h):
    return Image.new('L', (w, h), 0)


def m_rect(w, h, x0, y0, x1, y1):
    im = _img(w, h)
    if x1 >= x0 and y1 >= y0:
        ImageDraw.Draw(im).rectangle([x0, y0, x1, y1], fill=255)
    return np.array(im) > 0


def m_ell(w, h, x0, y0, x1, y1):
    im = _img(w, h)
    if x1 >= x0 and y1 >= y0:
        ImageDraw.Draw(im).ellipse([x0, y0, x1, y1], fill=255)
    return np.array(im) > 0


def m_poly(w, h, pts):
    im = _img(w, h)
    ImageDraw.Draw(im).polygon([(int(round(x)), int(round(y))) for x, y in pts], fill=255)
    return np.array(im) > 0


def m_line(w, h, p0, p1, width=1):
    im = _img(w, h)
    d = ImageDraw.Draw(im)
    p0 = (int(round(p0[0])), int(round(p0[1])))
    p1 = (int(round(p1[0])), int(round(p1[1])))
    d.line([p0, p1], fill=255, width=width)
    if width >= 3:  # tapas redondeadas para que no queden extremos en pico
        r = width // 2
        for (x, y) in (p0, p1):
            d.ellipse([x - r + 1, y - r + 1, x + r - 1, y + r - 1], fill=255)
    return np.array(im) > 0


def shift(m, dx, dy):
    """desplaza una mascara booleana (rellena con False)"""
    out = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    if xs1 > xs0 and ys1 > ys0:
        out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return out


class Cv:
    """Lienzo RGBA de pixel art (sin antialiasing)."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)

    # -- mascaras ligadas al tamano del lienzo
    def rect(self, x0, y0, x1, y1): return m_rect(self.w, self.h, x0, y0, x1, y1)
    def ell(self, x0, y0, x1, y1): return m_ell(self.w, self.h, x0, y0, x1, y1)
    def poly(self, pts): return m_poly(self.w, self.h, pts)
    def line(self, p0, p1, width=1): return m_line(self.w, self.h, p0, p1, width)

    # -- escritura
    def set(self, x, y, col, alpha=255):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x, :3] = col
            self.a[y, x, 3] = alpha

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return tuple(self.a[y, x])
        return (0, 0, 0, 0)

    def fill(self, mask, col, alpha=255):
        self.a[mask, :3] = col
        self.a[mask, 3] = alpha

    def paint(self, mask, tones, k=1, alpha=255, light=True, shadow=True):
        """Rellena la mascara con 3 tonos (luz arriba-izquierda, sombra abajo-derecha)."""
        L, B, S = tones
        lit = np.zeros_like(mask)
        sh = np.zeros_like(mask)
        for d in range(1, k + 1):
            lit |= ~shift(mask, 0, d) | ~shift(mask, d, 0)   # vecino arriba/izquierda fuera
            sh |= ~shift(mask, 0, -d) | ~shift(mask, -d, 0)  # vecino abajo/derecha fuera
        if not light: lit &= False
        if not shadow: sh &= False
        both = lit & sh
        lit &= ~both
        sh &= ~both
        self.fill(mask, B, alpha)
        self.fill(mask & lit, L, alpha)
        self.fill(mask & sh, S, alpha)

    def outline(self, col=K, diag=False, alpha=255, fix_edges=True):
        if fix_edges:
            # el contorno de 1 px necesita sitio: si el dibujo toca el borde del lienzo se sube 1 px (base) o se recorta
            if (self.a[-1, :, 3] > 0).any() and not (self.a[0, :, 3] > 0).any():
                self.a = np.roll(self.a, -1, axis=0); self.a[-1, :, 3] = 0
            self.a[0, :, 3] = np.where(self.a[0, :, 3] > 0, 0, 0)
            self.a[-1, :, 3] = 0
            self.a[:, 0, 3] = 0
            self.a[:, -1, 3] = 0
        solid = self.a[:, :, 3] > 0
        n = np.zeros_like(solid)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (-1, 1), (1, -1), (-1, -1)) if diag else ()):
            n |= shift(solid, dx, dy)
        edge = n & ~solid
        self.fill(edge, col, alpha)

    def blit(self, src, x=0, y=0, flip=False):
        s = src.a[:, ::-1] if flip else src.a
        h, w = s.shape[:2]
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        part = s[y0 - y:y1 - y, x0 - x:x1 - x]
        m = part[:, :, 3] > 0
        reg = self.a[y0:y1, x0:x1]
        reg[m] = part[m]

    def copy(self):
        c = Cv(self.w, self.h)
        c.a = self.a.copy()
        return c

    def flipx(self):
        c = Cv(self.w, self.h)
        c.a = self.a[:, ::-1].copy()
        return c

    def solid_mask(self):
        return self.a[:, :, 3] > 0

    def image(self):
        return Image.fromarray(self.a, 'RGBA')

    @staticmethod
    def from_image(im):
        im = im.convert('RGBA')
        c = Cv(im.width, im.height)
        c.a = np.array(im)
        return c


def hstack(frames):
    w = sum(f.w for f in frames)
    h = max(f.h for f in frames)
    out = Cv(w, h)
    x = 0
    for f in frames:
        out.blit(f, x, 0)
        x += f.w
    return out


def scale_nn(c, k):
    return Cv.from_image(c.image().resize((c.w * k, c.h * k), Image.NEAREST))


def bayer(x, y, n=4):
    m4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    return m4[y % 4][x % 4] / 16.0


# ---- Salida ----------------------------------------------------------------------------
MANIFEST = []


def _ensure(p):
    os.makedirs(os.path.dirname(p), exist_ok=True)


def save(c, rel, asset_id=None, folder='Art', src_group=None):
    """Guarda un PNG-24 RGBA en Assets/<folder>/<rel> y lo registra en el manifiesto."""
    base = ART if folder == 'Art' else AUDIO
    p = os.path.join(base, rel)
    _ensure(p)
    c.image().save(p, 'PNG')
    MANIFEST.append({'id': asset_id, 'file': os.path.relpath(p, ROOT).replace('\\', '/'), 'w': c.w, 'h': c.h})
    return p


def png_b64(c):
    b = io.BytesIO()
    c.image().save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def write_piskel(frames, name, rel, fps=12, rows=None):
    """Escribe un .piskel (archivo fuente) en Assets/_Source/<rel>. frames: lista de Cv iguales."""
    p = os.path.join(SRC, rel)
    _ensure(p)
    w, h = frames[0].w, frames[0].h
    strip = hstack(frames)
    layer = {'name': 'Layer 1', 'opacity': 1, 'frameCount': len(frames),
             'chunks': [{'layout': [[i] for i in range(len(frames))], 'base64PNG': png_b64(strip)}]}
    doc = {'modelVersion': 2, 'piskel': {'name': name, 'description': '', 'fps': fps,
                                         'height': h, 'width': w, 'layers': [json.dumps(layer)]}}
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(doc, f)
    return p


def sheet_grid(cells, cell, cols, rows, order=None):
    out = Cv(cell * cols, cell * rows)
    for i, c in enumerate(cells):
        out.blit(c, (i % cols) * cell, (i // cols) * cell)
    return out
