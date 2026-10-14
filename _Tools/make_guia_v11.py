"""Genera Mercadieval_GuiaAssets_v1.1.md (estandar de 64 px) a partir de la v1.0."""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src = open(os.path.join(ROOT, 'Mercadieval_GuiaAssets_v1.0.md'), encoding='utf-8').read()

# (viejo, nuevo, veces esperadas)
R = [
    ('| Documento | Guía de producción de assets, v1.0 |', '| Documento | Guía de producción de assets, v1.1 (estándar de 64 px) |', 1),
    ('## Cómo usar este documento\n', '''## Cambio de estándar en la v1.1: de 32 px a 64 px

Esta versión sustituye a la v1.0. **La cuadrícula, el tile y los píxeles por unidad pasan de 32 a 64.** Los personajes se duplican para conservar su tamaño en pantalla (siguen ocupando 2 × 2 casillas). El arte se escala ×2 con vecino más cercano.

| Concepto | v1.0 | v1.1 |
|---|---|---|
| Casilla (tile) y PPU del mundo | 32 | **64** |
| Personaje, NPC, enemigo | 64 × 64 | **128 × 128** |
| Candil / Glotglot | 32 × 32 / 128 × 128 | **64 × 64 / 256 × 256** |
| Objetos pequeños / grandes | 32 / 64 | **64 / 128** |
| Íconos de inventario / de interfaz | 32 / 64 | **64 / 128** |
| Texturas de partícula | 32 (niebla 128) | **64 (niebla 256)** |
| Elementos de interfaz | múltiplos de 16 | **múltiplos de 32** |
| Referencia de cámara | 960 × 540 (salida ×2) | **1920 × 1080 (salida ×1)** |
| Contorno | 1 px | **1 píxel lógico = 2 px reales** |

**Píxel lógico:** cada píxel del dibujo es un bloque de 2 × 2 px reales. Se dibuja y se verifica en la cuadrícula lógica; la entrega es siempre la versión ×2. Sin medios píxeles: ningún bloque de 2 × 2 puede tener dos colores.

No cambian: retratos (256 × 256), paneles de cinemática y pantallas (1920 × 1080, dibujados a 480 × 270 y escalados ×4), la paleta de 26 colores, la nomenclatura y todo el audio.

## Cómo usar este documento
''', 1),
    ('la cuadrícula de 32 px', 'la cuadrícula de 64 px', 1),
    ('| Tile | Casilla cuadrada de 32 × 32 px', '| Tile | Casilla cuadrada de 64 × 64 px', 1),
    ('Aquí siempre 32 |', 'Aquí siempre 64 |', 1),
    ('| 2 | **Todo se dibuja sobre cuadrícula múltiplo de 32 px**', '| 2 | **Todo se dibuja sobre cuadrícula múltiplo de 64 px**', 1),
    ('| 4 | **Contorno de 1 px en negro de contorno `#15121C`**', '| 4 | **Contorno de 1 píxel lógico (2 px reales) en negro de contorno `#15121C`**', 1),
    ('| Tamaño que no es múltiplo de 32 |', '| Tamaño que no es múltiplo de 64 |', 1),
    ('| Archivo con nombre distinto', '| Píxeles de medio tamaño (bloques de 2 × 2 con dos colores) | La imagen deja de ser pixel art uniforme y el contorno se ve irregular |\n| Archivo con nombre distinto', 1),
    # 3.1
    ('| Tile de escenario | 32 × 32 px | PNG-24 con alfa | 512 × 512 px (16 × 16 tiles) | — |', '| Tile de escenario | 64 × 64 px | PNG-24 con alfa | 1024 × 1024 px (16 × 16 tiles) | — |', 1),
    ('| Personaje, NPC, enemigo | 64 × 64 px |', '| Personaje, NPC, enemigo | 128 × 128 px |', 1),
    ('| Candil | 32 × 32 px | PNG-24 con alfa | Fila de 4 cuadros | Center |', '| Candil | 64 × 64 px | PNG-24 con alfa | Fila de 4 cuadros | Center |', 1),
    ('| Glotglot (jefe) | 128 × 128 px |', '| Glotglot (jefe) | 256 × 256 px |', 1),
    ('| Objeto del mundo pequeño | 32 × 32 px |', '| Objeto del mundo pequeño | 64 × 64 px |', 1),
    ('| Objeto del mundo grande | 64 × 64 px |', '| Objeto del mundo grande | 128 × 128 px |', 1),
    ('| Ícono de inventario | 32 × 32 px | PNG-24 con alfa | Hoja de 256 × 256 px |', '| Ícono de inventario | 64 × 64 px | PNG-24 con alfa | Hoja de 512 × 512 px |', 1),
    ('| Ícono de interfaz | 64 × 64 px | PNG-24 con alfa | Hoja de 512 × 512 px |', '| Ícono de interfaz | 128 × 128 px | PNG-24 con alfa | Hoja de 1024 × 1024 px |', 1),
    ('Variable, múltiplo de 16 px', 'Variable, múltiplo de 32 px', 1),
    ('| Textura de partícula | 32 × 32 px (niebla 128 × 128) |', '| Textura de partícula | 64 × 64 px (niebla 256 × 256) |', 1),
    # 3.2
    ('| Píxeles por unidad (PPU) | **32** — 1 casilla de 32 px = 1 unidad de Unity |', '| Píxeles por unidad (PPU) | **64** — 1 casilla de 64 px = 1 unidad de Unity |', 1),
    ('| PPU de íconos de interfaz | 64 |', '| PPU de íconos de interfaz | 128 |', 1),
    ('| Resolución de referencia de la cámara | 960 × 540 px |', '| Resolución de referencia de la cámara | 1920 × 1080 px |', 1),
    ('| Resolución de salida | 1920 × 1080 px (escalado entero ×2) |', '| Resolución de salida | 1920 × 1080 px (escalado entero ×1) |', 1),
    ('un personaje de 64 × 64 px ocupa 2 × 2 casillas en pantalla. Un tile de 32 px es una casilla.', 'un personaje de 128 × 128 px ocupa 2 × 2 casillas en pantalla. Un tile de 64 px es una casilla.', 1),
    ('dentro del lienzo de 64 × 64 px, el Mercader mide **44 px de alto** y se apoya en el borde inferior. Los 20 px restantes', 'dentro del lienzo de 128 × 128 px, el Mercader mide **88 px de alto** y se apoya en el borde inferior. Los 40 px restantes', 1),
    # 3.3
    ('| Pixels Per Unit | 32 (64 en íconos de interfaz) |', '| Pixels Per Unit | 64 (128 en íconos de interfaz) |', 1),
    ('| Slice | Grid By Cell Size: 32 × 32 o 64 × 64 según el tipo |', '| Slice | Grid By Cell Size: 64 × 64, 128 × 128 o 256 × 256 según el tipo |', 1),
    # 6.1
    ('| Candil - cuerpo | 32 x 32 |', '| Candil - cuerpo | 64 x 64 |', 1),
    ('| Candil - capa de luz (se tine por codigo) | 32 x 32 |', '| Candil - capa de luz (se tine por codigo) | 64 x 64 |', 1),
    ('Altura 44 px dentro del lienzo', 'Altura 88 px dentro del lienzo', 1),
    ('Glotglot: 128 × 128 px.', 'Glotglot: 256 × 256 px.', 1),
    ('| EN-04 | Glotglot (jefe final) | 128 x 128 |', '| EN-04 | Glotglot (jefe final) | 256 x 256 |', 1),
    # 6.2
    ('Un tileset es una hoja de 512 × 512 px con 256 casillas de 32 × 32 px.', 'Un tileset es una hoja de 1024 × 1024 px con 256 casillas de 64 × 64 px (o de 512 × 512 px con 64 casillas, en TS-03 y TS-04).', 1),
    ('| TS-03 | Interior de la tienda | 256 × 256 |', '| TS-03 | Interior de la tienda | 512 × 512 |', 1),
    ('| TS-04 | Huerto | 256 × 256 |', '| TS-04 | Huerto | 512 × 512 |', 1),
    # 6.4 / 6.5
    ('Todos de 32 × 32 px, sobre una sola hoja de 256 × 256 px.', 'Todos de 64 × 64 px, sobre una sola hoja de 512 × 512 px.', 1),
    ('Todos de 64 × 64 px, sobre una hoja de 512 × 512 px.', 'Todos de 128 × 128 px, sobre una hoja de 1024 × 1024 px.', 1),
    # 6.6
    ('| 96 × 96 px | Esquinas de 32 px;', '| 192 × 192 px | Esquinas de 64 px;', 1),
    ('| 160 × 48 px | 3 estados', '| 320 × 96 px | 3 estados', 1),
    ('| Ranura de barra rápida | 48 × 48 px |', '| Ranura de barra rápida | 96 × 96 px |', 1),
    ('| Ranura de inventario | 48 × 48 px |', '| Ranura de inventario | 96 × 96 px |', 1),
    ('| Barra de vida | 192 × 24 px |', '| Barra de vida | 384 × 48 px |', 1),
    ('| Barra de integridad | 192 × 24 px |', '| Barra de integridad | 384 × 48 px |', 1),
    ('| Reloj con barra día/noche | 256 × 32 px |', '| Reloj con barra día/noche | 512 × 64 px |', 1),
    ('| Caja de diálogo | 896 × 192 px | Con hueco de 128 px para el retrato |', '| Caja de diálogo | 1792 × 384 px | Con hueco de 256 px para el retrato |', 1),
    ('| Panel de notificación | 320 × 64 px |', '| Panel de notificación | 640 × 128 px |', 1),
    ('| Panel de ventana de comercio | 768 × 512 px |', '| Panel de ventana de comercio | 1536 × 1024 px |', 1),
    ('| Pestaña | 160 × 40 px |', '| Pestaña | 320 × 80 px |', 1),
    ('| Deslizador (slider) | 256 × 32 px |', '| Deslizador (slider) | 512 × 64 px |', 1),
    ('| Interruptor (toggle) | 64 × 32 px |', '| Interruptor (toggle) | 128 × 64 px |', 1),
    ('| Barra de desplazamiento | 24 × 256 px |', '| Barra de desplazamiento | 48 × 512 px |', 1),
    ('| Tipografía bitmap | Altura de mayúscula 8 px |', '| Tipografía bitmap | Altura de mayúscula 16 px (8 px lógicos; tamaño 20 en Unity) |', 1),
    # 6.10
    ('| FX-01 | Desvanecimiento de ánima | 32 × 32 |', '| FX-01 | Desvanecimiento de ánima | 64 × 64 |', 1),
    ('| FX-02 | Polvo de tala | 32 × 32 |', '| FX-02 | Polvo de tala | 64 × 64 |', 1),
    ('| FX-03 | Hoja que cae | 32 × 32 |', '| FX-03 | Hoja que cae | 64 × 64 |', 1),
    ('| FX-04 | Impacto de golpe | 32 × 32 |', '| FX-04 | Impacto de golpe | 64 × 64 |', 1),
    ('| FX-05 | Brillo de collectible | 32 × 32 |', '| FX-05 | Brillo de collectible | 64 × 64 |', 1),
    ('| FX-06 | Chispa de fuego | 32 × 32 |', '| FX-06 | Chispa de fuego | 64 × 64 |', 1),
    ('| FX-07 | Niebla nocturna | 128 × 128 |', '| FX-07 | Niebla nocturna | 256 × 256 |', 1),
    # anexo A
    ('(384 x 64 px = 6 cuadros de 64 x 64)', '(768 x 128 px = 6 cuadros de 128 x 128)', 1),
    ('Dentro de cada cuadro, el personaje se apoya', 'Dentro de cada cuadro (de 128 px), el personaje se apoya', 1),
    # anexo B
    ('| 128 × 64 |', '| 256 × 128 |', 3),
    ('| 384 × 64 |', '| 768 × 128 |', 4),
    ('| 256 × 64 |', '| 512 × 128 |', 3),
    ('| 320 × 64 |', '| 640 × 128 |', 3),
]

out = src
for old, new, n in R:
    c = out.count(old)
    assert c >= 1, ('no encontrado', old)
    if n and c != n:
        print('AVISO: cuenta', c, '!=', n, 'para', old[:60])
    out = out.replace(old, new)

# tabla 6.1: tamanos por cuadro 64 x 64 -> 128 x 128 (solo filas PJ/EN con 64 x 64)
out = re.sub(r'^(\| (?:PJ|EN)-\d\d \|[^|]*\| )64 x 64( \|)', r'\g<1>128 x 128\2', out, flags=re.M)
# tabla 6.3: tamanos de objetos (32 -> 64, 64 -> 128) en filas OB-xx
def ob(m):
    return m.group(1) + {'32': '64 × 64', '64': '128 × 128'}[m.group(2)] + m.group(3)
out = re.sub(r'^(\| OB-\d\d \|[^|]*\| )(32|64) × \2( \|)', ob, out, flags=re.M)
# tabla 6.2: hojas de 512 x 512 -> 1024 x 1024 (TS-01,02,05,06)
out = re.sub(r'^(\| TS-0[1256] \|[^|]*\| )512 × 512( \|)', r'\g<1>1024 × 1024\2', out, flags=re.M)

open(os.path.join(ROOT, 'Mercadieval_GuiaAssets_v1.1.md'), 'w', encoding='utf-8').write(out)
print('ok', len(out))
