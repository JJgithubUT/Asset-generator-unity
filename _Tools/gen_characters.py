"""Genera PJ-01..PJ-13 y EN-01..EN-04 (hojas de sprites + fuentes .piskel)."""
import math
from common import *
from humans import *
from char_styles import *
from spirits import *

DIRS = ('sur', 'nor', 'lat')
OUT = {}   # id -> lista de archivos


def sheet(frames):
    return hstack(frames)


def emit(asset_id, folder, prefix, name, anim, d, frames, piskel_frames):
    fn = f'{prefix}_{name}_{anim}' + (f'_{d}' if d else '') + '.png'
    save(sheet(frames), f'Characters/{folder}/{fn}', asset_id)
    piskel_frames.extend(frames)


def build_human(asset_id, folder, prefix, name, style, anims, pisk_name=None):
    """anims: lista (anim, dirs, poses_por_dir)"""
    allf = []
    for anim, dirs, poses in anims:
        for d in dirs:
            frames = [draw_human(d, po, style) for po in poses[d]]
            emit(asset_id, folder, prefix, name, anim, d, frames, allf)
    write_piskel(allf, pisk_name or name, f'Characters/{folder}/{name}.piskel')
    return allf


def per_dir(fn):
    return {d: fn(d) for d in DIRS}


def only_sur(poses):
    return {'sur': poses}


# ---------------- poses de las animaciones sueltas ----------------
def idle2(): return [{'dy': 0}, {'dy': 1}]
def idle2_all(): return per_dir(lambda d: idle2())


def atender(hand='rh', n=4):
    ys = [(2, -7), (3, -10), (2, -7), (1, -4)]
    return [{hand: ys[i], 'dy': 1 if i == 2 else 0} for i in range(n)]


def martillar():
    return [dict(rh=(1, -10), hammer=(0, -1)), dict(rh=(1, -14), hammer=(0, -1)),
            dict(rh=(-1, -3), hammer=(0, 1), dy=1), dict(rh=(0, -6), hammer=(0, -1))]


def robar():
    return [dict(lh=(-1, -5), rh=(1, -5)), dict(lh=(-3, -10), rh=(3, -10), dy=1),
            dict(lh=(0, -7), rh=(0, -7), bolsa=1), dict(lh=(0, -3), rh=(0, -3), bolsa=1)]


def huir():
    ps = walk_poses('lat', 4, lift=4, swing=3, run=True)
    for p in ps: p['bolsa'] = 1
    return ps


def guardia_atacar(d):
    if d == 'sur':
        return [dict(rh=(2, -4), spear=(0, 8, 0, -30)), dict(rh=(-1, 6), spear=(0, -20, 0, 8), dy=1),
                dict(rh=(0, 3), spear=(0, -12, 0, 6)), dict(rh=(0, 0))]
    if d == 'nor':
        return [dict(rh=(2, 4), spear=(0, -8, 0, 12)), dict(rh=(1, -10), spear=(0, 12, 0, -24), dy=1),
                dict(rh=(1, -5), spear=(0, 8, 0, -22)), dict(rh=(0, 0))]
    return [dict(lh=(-6, 0), spear=(-14, 2, 12, -6)), dict(lh=(12, 1), spear=(-18, 0, 16, 0), dy=1),
            dict(lh=(8, 1), spear=(-14, 0, 14, -2)), dict(lh=(0, 0))]


def build_all():
    # ---- PJ-01 Mercader
    st = mercader_style()
    mp = mercader_poses()
    allf = []
    anim_list = [('idle', 2), ('correr', 6), ('atacar', 4), ('saltar', 5)]
    for anim, n in anim_list:
        for d in DIRS:
            frames = [draw_human(d, po, st) for po in mp[d][anim]]
            assert len(frames) == n
            emit('PJ-01', 'Mercader', 'spr_pj', 'mercader', anim, d, frames, allf)
    # desmayo (sur, 6 cuadros): se cae y queda en el suelo
    faint = []
    base = draw_human('sur', {'dy': 0, 'no_outline': 1}, st)
    angles = [0, 12, 30, 55, 78, 90]
    for i, a in enumerate(angles):
        faint.append(rotate_fall(base, a, i))
    emit('PJ-01', 'Mercader', 'spr_pj', 'mercader', 'desmayo', 'sur', faint, allf)
    write_piskel(allf, 'mercader', 'Characters/Mercader/mercader.piskel')

    # ---- PJ-02 / PJ-03 Candil
    fl = [candil_body(i) for i in range(4)]
    al = [candil_body(i, 'alerta') for i in range(2)]
    luz = [candil_luz(i) for i in range(4)]
    save(hstack(fl), 'Characters/Candil/spr_pj_candil_flotar.png', 'PJ-02')
    save(hstack(al), 'Characters/Candil/spr_pj_candil_alerta.png', 'PJ-02')
    save(hstack(luz), 'Characters/Candil/spr_pj_candil_luz_flotar.png', 'PJ-03')
    write_piskel(fl + al, 'candil', 'Characters/Candil/candil.piskel')
    write_piskel(luz, 'candil_luz', 'Characters/Candil/candil_luz.piskel')

    # ---- NPC con una sola orientacion (sur)
    build_human('PJ-04', 'Tomas', 'spr_pj', 'tomas', tomas_style(),
                [('idle', ('sur',), only_sur(idle2())), ('atender', ('sur',), only_sur(atender('rh')))])
    build_human('PJ-05', 'Bruno', 'spr_pj', 'bruno', bruno_style(),
                [('idle', ('sur',), only_sur(idle2())), ('martillar', ('sur',), only_sur(martillar()))])
    build_human('PJ-06', 'Elvira', 'spr_pj', 'elvira', elvira_style(),
                [('idle', ('sur',), only_sur(idle2())), ('atender', ('sur',), only_sur(atender('rh')))])
    build_human('PJ-07', 'Inquisidor', 'spr_pj', 'inquisidor', inquisidor_style(),
                [('idle', ('sur',), only_sur(idle2())), ('atender', ('sur',), only_sur(atender('lh')))])
    build_human('PJ-08', 'GuardiaTemplo', 'spr_pj', 'guardia_templo', guardia_templo_style(),
                [('idle', ('sur',), only_sur(idle2()))])
    # ---- clientes
    for pid, kind in (('PJ-09', 'base'), ('PJ-10', 'campesino'), ('PJ-11', 'artesano'), ('PJ-12', 'dama')):
        sw = lambda d, kind=kind: [dict(p, sway=((1 if i in (1, 2) else -1) if kind == 'dama' else 0))
                                   for i, p in enumerate(walk_poses(d, 6, lift=2, swing=2))]
        build_human(pid, f'Cliente_{kind}', 'spr_pj', f'cliente_{kind}', cliente_style(kind),
                    [('idle', DIRS, idle2_all()), ('caminar', DIRS, per_dir(sw))])
    # ---- PJ-13 guardia a sueldo
    build_human('PJ-13', 'GuardiaSueldo', 'spr_pj', 'guardia_sueldo', guardia_sueldo_style(),
                [('idle', DIRS, idle2_all()),
                 ('caminar', DIRS, per_dir(lambda d: walk_poses(d, 6, lift=3, swing=2))),
                 ('atacar', DIRS, per_dir(guardia_atacar))])
    # ---- EN-01 ladron
    build_human('EN-01', 'Ladron', 'spr_enm', 'ladron', ladron_style(),
                [('idle', DIRS, idle2_all()),
                 ('correr', DIRS, per_dir(lambda d: walk_poses(d, 6, lift=4, swing=3, run=True))),
                 ('robar', ('sur',), only_sur(robar())),
                 ('huir', ('lat',), {'lat': huir()})])

    # ---- EN-02 / EN-03 animas
    for aid, kind, nm in (('EN-02', 'errante', 'anima_errante'), ('EN-03', 'veloz', 'anima_veloz')):
        allf = []
        for anim in ('flotar', 'atacar'):
            for d in DIRS:
                fr = ghost_frames(kind, d, anim)
                emit(aid, 'Anima_' + kind, 'spr_enm', nm, anim, d, fr, allf)
        fr = ghost_fade(kind)
        emit(aid, 'Anima_' + kind, 'spr_enm', nm, 'desvanecer', 'sur', fr, allf)
        write_piskel(allf, nm, f'Characters/Anima_{kind}/{nm}.piskel')

    # ---- EN-04 Glotglot
    allf = []
    for anim, n in (('idle', 4), ('avanzar', 4), ('golpear', 5)):
        fr = [glotglot_frame(anim, i, n) for i in range(n)]
        emit('EN-04', 'Glotglot', 'spr_enm', 'glotglot', anim, None, fr, allf)
    fr = glotglot_fade(8)
    emit('EN-04', 'Glotglot', 'spr_enm', 'glotglot', 'desvanecer', None, fr, allf)
    write_piskel(allf, 'glotglot', 'Characters/Glotglot/glotglot.piskel')


def rotate_fall(base, angle, i):
    """Desmayo: el cuerpo (sin contorno) rota sobre los pies y queda tumbado; luego se contornea."""
    if angle == 0:
        c = base.copy()
        c.outline()
        return c
    im = base.image()
    if angle == 90:
        rot = im.rotate(-90, resample=Image.NEAREST, expand=False, center=(32, 62))
    else:
        rot = im.rotate(-angle, resample=Image.NEAREST, expand=False, center=(32, 62))
    out = Cv.from_image(rot)
    # asentar en el suelo: la mayor y debe quedar en 62
    ys = np.nonzero(out.a[:, :, 3] > 0)[0]
    if len(ys):
        d = 62 - ys.max()
        out.a = np.roll(out.a, d, axis=0)
    xs = np.nonzero(out.a[:, :, 3] > 0)[1]
    if len(xs):
        cx = (xs.min() + xs.max()) // 2
        out.a = np.roll(out.a, 32 - cx, axis=1)
    out.outline()
    return out


if __name__ == '__main__':
    build_all()
    print(len(MANIFEST), 'archivos')
