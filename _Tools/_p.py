s=open('validate.py',encoding='utf-8').read()
s=s.replace("def expect_size(rel, w, h):\n    b = os.path.basename(rel)","def expect_size(rel, w, h):\n    \"\"\"Tamanos del estandar de 64 px (tabla 3.1 de la guia v1.1).\"\"\"\n    b = os.path.basename(rel)")
s=s.replace("""        if 'glotglot' in b: return h == 128 and w % 128 == 0
        if 'candil' in b: return h == 32 and w % 32 == 0
        return h == 64 and w % 64 == 0
    if rel.startswith('Tilesets/'): return w == h and w in (256, 512)
    if rel.startswith('Objects/'): return h in (32, 64) and w % h == 0
    if rel.startswith('Items/'): return (w, h) in ((256, 256), (32, 32))
    if rel.startswith('UI/Icons/'): return (w, h) in ((512, 512), (64, 64))""","""        if 'glotglot' in b: return h == 256 and w % 256 == 0
        if 'candil' in b: return h == 64 and w % 64 == 0
        return h == 128 and w % 128 == 0
    if rel.startswith('Tilesets/'): return w == h and w in (512, 1024)
    if rel.startswith('Objects/'): return h in (64, 128) and w % h == 0
    if rel.startswith('Items/'): return (w, h) in ((512, 512), (64, 64))
    if rel.startswith('UI/Icons/'): return (w, h) in ((1024, 1024), (128, 128))""")
s=s.replace("return h in (32, 128) and w % h == 0","return h in (64, 256) and w % h == 0")
s=s.replace("""        t = {'marco_ventana': (96, 96), 'boton': (160, 48), 'ranura': (48, 48), 'barra_vida': (192, 24), 'barra_integridad': (192, 24),
             'reloj': (256, 32), 'caja_dialogo': (896, 192), 'notificacion': (320, 64), 'ventana_comercio': (768, 512),
             'pestana': (160, 40), 'deslizador_riel': (256, 32), 'deslizador_manija': (32, 32), 'interruptor': (64, 32),
             'desplazamiento_riel': (24, 256), 'desplazamiento_manija': (24, 48)}""","""        t = {'marco_ventana': (192, 192), 'boton': (320, 96), 'ranura': (96, 96), 'barra_vida': (384, 48), 'barra_integridad': (384, 48),
             'reloj': (512, 64), 'caja_dialogo': (1792, 384), 'notificacion': (640, 128), 'ventana_comercio': (1536, 1024),
             'pestana': (320, 80), 'deslizador_riel': (512, 64), 'deslizador_manija': (64, 64), 'interruptor': (128, 64),
             'desplazamiento_riel': (48, 512), 'desplazamiento_manija': (48, 96)}""")
s=s.replace("""        a = np.array(im.convert('RGBA'))
        if not expect_size(rel, im.width, im.height): err(f, 1, f'tamano {im.width}x{im.height} no valido')""","""        a = np.array(im.convert('RGBA'))
        if not expect_size(rel, im.width, im.height): err(f, 1, f'tamano {im.width}x{im.height} no valido')
        k = scale_for(rel)
        if k > 1:
            # el estandar exige que cada pixel logico sea un bloque kxk uniforme (sin medios pixeles)
            if im.width % k or im.height % k: err(f, 1, f'tamano no multiplo de {k}')
            else:
                sub = a[::k, ::k]
                if not np.array_equal(np.repeat(np.repeat(sub, k, 0), k, 1), a): err(f, 1, f'hay pixeles que no forman bloques {k}x{k}')
                a = sub""")
open('validate.py','w',encoding='utf-8').write(s)
