"""Verificacion automatica de la lista del apartado 5.4 (puntos 1-7) sobre todos los assets."""
import os, re, sys, glob
import numpy as np
from PIL import Image
from common import *

ALPHA_OK = ('glotglot', 'anima_', 'candil_luz', 'obj_sombra', 'niebla_nocturna', 'desvanecimiento_anima')
NO_OUTLINE = ('Tilesets', 'Cinematics', 'Screens', 'Portraits', 'VFX', 'UI/Elements', 'candil_luz', 'spr_item_hoja', 'spr_ui_iconos', 'glotglot', 'anima_', 'obj_sombra', 'obj_marcador', 'obj_bellota')
errors = []


def err(f, n, msg): errors.append((os.path.relpath(f, ROOT).replace(os.sep, '/'), n, msg))


def expect_size(rel, w, h):
    b = os.path.basename(rel)
    if rel.startswith('Characters/'):
        if 'glotglot' in b: return h == 128 and w % 128 == 0
        if 'candil' in b: return h == 32 and w % 32 == 0
        return h == 64 and w % 64 == 0
    if rel.startswith('Tilesets/'): return w == h and w in (256, 512)
    if rel.startswith('Objects/'): return h in (32, 64) and w % h == 0
    if rel.startswith('Items/'): return (w, h) in ((256, 256), (32, 32))
    if rel.startswith('UI/Icons/'): return (w, h) in ((512, 512), (64, 64))
    if rel.startswith('Portraits/'): return (w, h) == (256, 256)
    if rel.startswith(('Cinematics/', 'Screens/')): return (w, h) == (1920, 1080)
    if rel.startswith('VFX/'): return h in (32, 128) and w % h == 0
    if rel.startswith('UI/Elements/'):
        t = {'marco_ventana': (96, 96), 'boton': (160, 48), 'ranura': (48, 48), 'barra_vida': (192, 24), 'barra_integridad': (192, 24),
             'reloj': (256, 32), 'caja_dialogo': (896, 192), 'notificacion': (320, 64), 'ventana_comercio': (768, 512),
             'pestana': (160, 40), 'deslizador_riel': (256, 32), 'deslizador_manija': (32, 32), 'interruptor': (64, 32),
             'desplazamiento_riel': (24, 256), 'desplazamiento_manija': (24, 48)}
        for k, v in t.items():
            if k in b: return (w, h) == v
    return True


def main():
    files = sorted(glob.glob(os.path.join(ART, '**', '*.png'), recursive=True))
    pal = set(P.values()) | {WHITE}
    n = 0
    for f in files:
        rel = os.path.relpath(f, ART).replace(os.sep, '/')
        b = os.path.basename(f)
        n += 1
        if not re.fullmatch(r'(spr)_[a-z0-9_]+\.png', b): err(f, 5, 'nombre fuera de convencion')
        im = Image.open(f)
        if im.mode != 'RGBA': err(f, 6, f'modo {im.mode} (se espera PNG-24 con alfa)')
        a = np.array(im.convert('RGBA'))
        if not expect_size(rel, im.width, im.height): err(f, 1, f'tamano {im.width}x{im.height} no valido')
        al = a[:, :, 3]
        semi = (al > 0) & (al < 255)
        if semi.any() and not any(k in b for k in ALPHA_OK): err(f, 3, f'{int(semi.sum())} px semitransparentes')
        op = a[al > 0][:, :3]
        cols = set(map(tuple, np.unique(op, axis=0)))
        bad = cols - pal
        if bad: err(f, 2, f'colores fuera de paleta: {sorted(bad)[:3]}')
        # contorno
        if not any(k in rel or k in b for k in NO_OUTLINE):
            solid = al > 0
            pad = np.pad(solid, 1)
            nb = ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
            edge = solid & nb
            col = a[:, :, :3]
            notk = edge & ~np.all(col == np.array(K), axis=2)
            if notk.any(): err(f, 4, f'{int(notk.sum())} px de borde que no son #15121C')
        # fuente
        base = os.path.splitext(rel)[0]
        grp = rel.split('/')[0]
    for f in glob.glob(os.path.join(AUDIO, '**', '*.*'), recursive=True):
        b = os.path.basename(f)
        if not re.fullmatch(r'(sfx|mus)_[a-z0-9_]+\.(wav|ogg)', b): err(f, 5, 'nombre fuera de convencion')
    print(f'{n} PNG revisados;', len(errors), 'incidencias')
    for e in errors[:80]: print(e)
    return errors


if __name__ == '__main__':
    main()
