"""RT-01..RT-07 retratos 256x256 (dibujados a 128x128 y escalados x2 con vecino mas cercano)."""
from common import *
from spirits import ghost, candil_body

LINO = (P['crema'], P['crema'], P['piedra_c'])
PELO = (P['tierra'], P['madera'], P['tierra_o'])


def head(c, skin, w=26, top=18, bottom=88):
    m = c.ell(64 - w - 2, top, 64 + w + 2, bottom)
    c.paint(m, skin, k=2)
    return m


def face(c, skin, eye=P['K'], brow=P['tierra_o'], worry=0, tired=False, y=58, mouth_w=10):
    for sx in (-1, 1):
        ex = 64 + sx * 14
        c.fill(c.rect(ex - 5, y - 3, ex + 5, y + 3), P['crema'])
        c.fill(c.rect(ex - 2, y - 3, ex + 2, y + 3), eye)
        c.set(ex - 1, y - 2, P['crema'])
        inner = ex - sx * 6
        outer = ex + sx * 6
        c.fill(c.line((inner, y - 10 - worry), (outer, y - 10 + worry), 2), brow)
        if tired:
            c.fill(c.rect(ex - 4, y + 5, ex + 4, y + 6), P['ocre_m'])
    c.fill(c.rect(62, y + 2, 66, y + 12), skin[2])
    c.fill(c.rect(61, y + 12, 67, y + 13), skin[2])
    c.fill(c.rect(64 - mouth_w // 2, y + 22, 64 + mouth_w // 2, y + 23), P['tierra'])


def shoulders(c, tones, w=44, top=92):
    m = c.poly([(64 - w - 16, 127), (64 - w, top + 6), (64 - 24, top), (64 + 24, top), (64 + w, top + 6), (64 + w + 16, 127)])
    c.paint(m, tones, k=2)
    return m


def ears(c, skin):
    for sx in (-1, 1):
        c.paint(c.ell(64 + sx * 29 - 3, 52, 64 + sx * 29 + 3, 66), skin, k=1)


def portrait(kind):
    c = Cv(128, 128)
    if kind == 'mercader':
        shoulders(c, LINO)
        c.paint(c.poly([(24, 127), (30, 100), (50, 94), (58, 110), (58, 127)]), T['ocre'], k=2)
        c.paint(c.poly([(104, 127), (98, 100), (78, 94), (70, 110), (70, 127)]), T['ocre'], k=2)
        c.fill(c.rect(54, 78, 74, 96), P['ocre_c'])
        ears(c, T['piel'])
        m = head(c, T['piel'])
        hair = (c.ell(34, 12, 94, 54) & c.rect(0, 0, 127, 46)) | ((c.rect(35, 30, 41, 62) | c.rect(87, 30, 93, 62)) & m)
        c.paint(hair, PELO, k=2)
        for x in (44, 56, 70, 82):
            c.fill(c.poly([(x, 20), (x + 4, 10), (x + 8, 20)]), P['madera'])
        face(c, T['piel'], tired=True, worry=1)
        for xx in range(44, 86, 2):
            for yy in (72, 76, 80):
                if m[yy, xx] and (xx + yy) % 4 == 0: c.set(xx, yy, P['tierra'])
    elif kind == 'bruno':
        gris = (P['piedra_c'], P['piedra_m'], P['piedra_o'])
        shoulders(c, LINO, w=52)
        c.paint(c.rect(30, 100, 40, 127), T['tierra'], k=1)
        c.paint(c.rect(88, 100, 98, 127), T['tierra'], k=1)
        c.fill(c.rect(52, 78, 76, 96), P['ocre_c'])
        ears(c, T['piel'])
        m = head(c, T['piel'], w=30)
        c.paint(c.ell(34, 12, 94, 48) & c.rect(0, 0, 127, 44), gris, k=2)
        face(c, T['piel'], brow=P['piedra_o'], y=58)
        beard = c.poly([(36, 66), (92, 66), (88, 96), (64, 104), (40, 96)]) & (m | c.rect(34, 84, 94, 104))
        c.paint(beard, gris, k=2)
        c.fill(c.rect(54, 82, 74, 84), P['tierra_o'])
    elif kind == 'elvira':
        verde = (P['fol_m'], P['fol_o'], P['K'])
        pelo = (P['tierra_o'], P['tierra_o'], P['K'])
        c.paint(c.ell(26, 10, 102, 126), pelo, k=2)
        shoulders(c, verde, w=40, top=96)
        c.paint(c.poly([(50, 94), (78, 94), (64, 118)]), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)
        c.fill(c.rect(56, 80, 72, 96), P['ocre_c'])
        m = head(c, T['piel'], w=24, top=22, bottom=90)
        c.paint((c.ell(38, 16, 90, 46) & c.rect(0, 0, 127, 42)) | (c.rect(36, 30, 44, 70) & m) | (c.rect(84, 30, 92, 70) & m), pelo, k=2)
        face(c, T['piel'], worry=2, y=60, mouth_w=7)
    elif kind == 'inquisidor':
        robe = (P['piedra_m'], P['piedra_o'], P['K'])
        shoulders(c, robe, w=40)
        c.paint(c.poly([(46, 94), (82, 94), (64, 127)]), (P['crema'], P['piedra_c'], P['piedra_m']), k=1)
        c.fill(c.poly([(64, 106), (70, 114), (64, 122), (58, 114)]), P['trigo'])
        c.fill(c.rect(55, 80, 73, 96), P['crema'])
        pale = (P['crema'], P['crema'], P['ocre_c'])
        head(c, pale, w=22, top=26, bottom=92)
        face(c, pale, brow=P['piedra_o'], y=62, mouth_w=12)
        c.fill(c.line((50, 82), (54, 90), 1), P['ocre_c'])
        c.fill(c.line((78, 82), (74, 90), 1), P['ocre_c'])
        c.paint(c.ell(14, 26, 114, 44), robe, k=2)
        c.paint(c.poly([(40, 30), (42, 4), (86, 4), (88, 30)]), robe, k=2)
        c.fill(c.rect(42, 22, 86, 26), P['piedra_c'])
    elif kind == 'tomas':
        shoulders(c, T['ocre'], w=44)
        c.fill(c.rect(54, 78, 74, 96), P['ocre_c'])
        ears(c, T['piel'])
        m = head(c, T['piel'], w=26, top=26)
        face(c, T['piel'], y=62)
        c.paint(c.ell(10, 24, 118, 46), T['paja'], k=2)
        c.paint(c.poly([(36, 30), (38, 4), (90, 4), (92, 30)]), T['paja'], k=2)
        c.fill(c.rect(38, 24, 90, 28), P['tierra'])
        for xx in range(44, 86, 2):
            if m[88, xx] and xx % 4 == 0: c.set(xx, 82, P['tierra'])
    elif kind == 'candil':
        body = candil_body(0)
        big = Cv.from_image(body.image().resize((96, 96), Image.NEAREST))
        c.blit(big, 16, 8)
        c.fill(c.ell(50, 82, 78, 112), P['crema'])
        c.fill(c.ell(54, 86, 74, 108), P['c_verde'])
        c.outline()
        return scale_nn(c, 2)
    elif kind == 'glotglot':
        g = ghost('sur', 0.2, 'errante', scale=3.1, size=128, alpha=215, bob=-6)
        c.blit(g)
        for (x, y) in ((22, 40), (100, 44), (28, 94), (98, 96)):
            c.fill(c.ell(x - 7, y - 9, x + 7, y + 9), P['violeta'], 150)
            c.fill(c.ell(x - 3, y - 4, x + 3, y + 3), P['noche'], 200)
        return scale_nn(c, 2)
    c.outline()
    return scale_nn(c, 2)


def build():
    names = [('mercader', 'RT-01'), ('bruno', 'RT-02'), ('elvira', 'RT-03'), ('inquisidor', 'RT-04'), ('candil', 'RT-05'),
             ('glotglot', 'RT-06'), ('tomas', 'RT-07')]
    for n, rid in names:
        save(portrait(n), f'Portraits/spr_ret_{n}.png', rid)


if __name__ == '__main__':
    build()
