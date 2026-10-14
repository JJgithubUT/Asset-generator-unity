"""Regenera TODOS los assets de Mercadieval. Uso: python build_all.py"""
import os, json, shutil
import common
from common import *


def palettes():
    d = os.path.join(SRC, 'Palette')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'mercadieval_26.gpl'), 'w', encoding='utf-8') as f:
        f.write('GIMP Palette\nName: Mercadieval 26\nColumns: 13\n#\n')
        for n, name, hx, k in PALETTE_LIST:
            r, g, b = hexrgb(hx)
            f.write(f'{r:3d} {g:3d} {b:3d}\t{n:02d} {name} #{hx}\n')
    with open(os.path.join(d, 'mercadieval_26.pal'), 'w', encoding='ascii') as f:
        f.write('JASC-PAL\r\n0100\r\n26\r\n')
        for n, name, hx, k in PALETTE_LIST:
            r, g, b = hexrgb(hx)
            f.write(f'{r} {g} {b}\r\n')
    # PNG de muestra (26 casillas) para importar en Piskel como paleta desde imagen
    c = Cv(26, 1)
    for i, (_, _, hx, _) in enumerate(PALETTE_LIST): c.set(i, 0, hexrgb(hx))
    c.image().save(os.path.join(d, 'mercadieval_26.png'))


def sources_for_rest():
    """Cada PNG sin .piskel propio recibe su archivo fuente espejo en _Source/."""
    n = 0
    for e in common.MANIFEST:
        f = e['file']
        if not f.startswith('Assets/Art/') or not f.endswith('.png'): continue
        rel = f[len('Assets/Art/'):]
        pk = os.path.join(SRC, os.path.splitext(rel)[0] + '.piskel')
        # los personajes ya traen su .piskel agrupado
        folder = os.path.dirname(os.path.join(SRC, rel))
        if os.path.exists(pk): continue
        if rel.startswith('Characters/') and any(x.endswith('.piskel') for x in os.listdir(folder) if os.path.isdir(folder)) if os.path.isdir(folder) else False: continue
        if rel.startswith(('Tilesets/', 'Cinematics/', 'Screens/', 'Items/', 'UI/Icons/')) and not rel.startswith(('Items/singles', 'UI/Icons/singles')):
            continue
        if '/singles/' in rel: continue
        im = Image.open(os.path.join(ROOT, f))
        c = Cv.from_image(im)
        if c.w > 1000: c = scale_nn(c, 1)
        write_piskel([c], os.path.basename(pk)[:-7], os.path.relpath(pk, SRC), fps=1, scale=1)
        n += 1
    return n


def main():
    import gen_characters, gen_tiles, gen_objects, gen_ui, gen_portraits, gen_scenes, gen_audio
    gen_characters.build_all(); gen_tiles.build(); gen_objects.build(); gen_ui.build(); gen_portraits.build()
    gen_scenes.build(); gen_audio.build_sfx(); gen_audio.build_music()
    palettes()
    n = sources_for_rest()
    with open(os.path.join(ROOT, 'Assets', 'manifest_assets.json'), 'w', encoding='utf-8') as f:
        json.dump(common.MANIFEST, f, indent=1, ensure_ascii=False)
    print('archivos generados:', len(common.MANIFEST), '| fuentes extra:', n)


if __name__ == '__main__':
    main()
