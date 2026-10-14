# Mercadieval — assets generados

Todo se generó por código siguiendo `Mercadieval_GuiaAssets_v1.1.md` (estándar de 64 px; la v1.0 de 32 px queda como referencia histórica). Copia la carpeta `Assets/` dentro del proyecto Unity 2D (6.3 LTS).

## Qué hay

| Carpeta | Contenido | IDs |
|---|---|---|
| `Assets/Art/Characters` | 332 cuadros (hojas por animación y orientación sur / nor / lat) | PJ-01…13, EN-01…04 |
| `Assets/Art/Tilesets` | 6 tilesets con Rule Tiles de 16 variantes (camino, arroyo con 2 cuadros de animación, borde de pasto, muro, empedrado) | TS-01…06 |
| `Assets/Art/Objects` | 30 objetos (tiras con variantes o estados) | OB-01…30 |
| `Assets/Art/Items` | 11 íconos (`singles/`) + hoja `spr_item_hoja.png` 512×512 | IT-01…11 |
| `Assets/Art/UI` | 18 íconos (hoja 1024×1024 + `singles/`), 15 elementos, fuente `fnt_ui_tipografia.ttf` (con á é í ó ú ñ Ñ ü ¿ ¡) | UI-01…33 |
| `Assets/Art/Portraits` | 7 retratos 256×256 | RT-01…07 |
| `Assets/Art/Cinematics`, `Screens` | 19 paneles + 5 pantallas a 1920×1080 (dibujados a 480×270 y escalados ×4 con vecino más cercano) | CN-01…19, BG-01…05 |
| `Assets/Art/VFX` | 7 texturas de partícula | FX-01…07 |
| `Assets/Audio/Music` | 7 pistas `.ogg` (44,1 kHz estéreo, loop sin corte; 90 s o 120 s) | MU-01…07 |
| `Assets/Audio/SFX` | 31 `.wav` (los pasos tienen 3 variantes cada uno; 16 bits, mono, pico −3 dBFS) | SX-01…27 |
| `Assets/_Source` | `.piskel` espejo de cada asset gráfico + paleta (`.gpl`, `.pal` y `.png`) | — |
| `Assets/Editor` | `MercadievalAssetPostprocessor.cs` | — |
| `Assets/manifest_assets.json` | Lista de todos los archivos con su ID y tamaño | — |
| `_Tools/` | Generador en Python (`python _Tools/build_all.py`) y validador (`python _Tools/validate.py`) | — |

## Estándar de 64 px (v1.1)

Casilla y PPU = 64. Personajes 128×128 (88 px de alto), Candil 64, Glotglot 256, objetos 64/128, ítems 64, íconos de interfaz 128, partículas 64 (niebla 256), elementos de interfaz ×2 y mayúscula de la fuente de 16 px (usa tamaño 20 en Unity). Retratos, cinemáticas, pantallas y audio no cambian. Cada píxel lógico es un bloque de 2×2 px reales: el generador dibuja en la rejilla lógica y `common.save()` escala ×2 al guardar (`SCALE = 2`). La referencia de cámara pasa a 1920×1080 (salida ×1).

## Cómo importarlo

1. Copia `Assets/` a tu proyecto. El script de `Assets/Editor` aplica solo la configuración del apartado 3.3: Sprite, PPU 64 (128 en íconos de interfaz), Point, sin compresión (Normal en los paneles de 1920×1080), Full Rect, sin mipmaps, Clamp.
2. Corta las hojas por celda: personajes 128 (Candil 64, Glotglot 256), tilesets 64, íconos de inventario 64, íconos de interfaz 128. Los pivotes son Bottom en personajes y objetos, y Center en el resto.
3. Los marcos y botones llevan borde 9-slice configurado.
4. Si algo no se corta, usa **Mercadieval ▸ Reimportar assets de arte**.
5. Los sprites cortados se llaman `<archivo>_<n>` con n desde 0. Las animaciones van a 12 fps, excepto Idle (2 fps) y Flotar de Candil, ánimas y Glotglot (5 fps, 4 cuadros en 0,8 s). Las duraciones están en el apartado 1.2.

## Verificación

`python _Tools/validate.py` comprueba por archivo los puntos 1–6 del apartado 5.4: tamaño, paleta de 26 colores (más el blanco puro de la capa de luz de Candil), sin semitransparencias fuera de las autorizadas, contorno de 1 píxel lógico (2 px reales) `#15121C`, y bloques de 2×2 uniformes, nombre y PNG con alfa. Resultado actual: **216 PNG, 0 incidencias**. El punto 7 (fuente en `_Source`) se cumple con los `.piskel` generados.

Los 332 cuadros de personaje coinciden con el total de la guía. Los tamaños de hoja del Mercader coinciden con el Anexo B.

## Decisiones que conviene revisar

- **Es arte procedural**: respeta reglas, paleta y tamaños, pero es una base para pulir en Piskel, no arte de ilustrador. Los 7 audios de música y los 27 efectos están sintetizados; conviene escucharlos. No se pudieron escuchar durante la generación.
- **Piskel**: los `.piskel` siguen el formato de Piskel pero no pude abrirlos en Piskel para comprobarlo. El `.aup3` de Audacity no se genera; en su lugar están los scripts.
- **Paneles de dato (CN-07, 08, 12, 13)**: el Documento de Proyecto v2.0 (apartado 1.4.6) no estaba disponible. Dejé las composiciones y la fuente «Fuente: CONAFOR», con una placa vacía donde va la cifra, sin inventar datos. Las alturas de las barras de CN-12 son ilustrativas. Los textos de las 4 causas de CN-13 deben añadirse (se puede escribir con `pixfont.draw_text`).
- **Orientaciones únicas** (NPC, Desmayo, Robar, Atender, Martillar): se dibujaron en `sur`. Excepciones: **Huir** del ladrón en `lat` y los fantasmas con 3 orientaciones.
- **Retratos**: dibujados a 128×128 y escalados ×2, así que los píxeles son de 2×2.
- **Tilesets TS-03 y TS-04**: hojas de 512×512 (en el estándar de 64 px; antes 256×256).
- **Candil**: el cuerpo (`spr_pj_candil_*`) deja la cavidad del abdomen apagada. La luz es el archivo aparte `spr_pj_candil_luz_flotar.png` en blanco puro, alineado píxel a píxel, para teñirla por código.
- **Insignias**: el Inquisidor y las lápidas usan un rombo, no una cruz, por el apartado 8.5. El escudo de interfaz también lleva rombo.
- **Fantasmas** (EN-02/03/04, `Desvanecer`): usan alfa parcial (permitido en el contorno exterior). El contorno es `#15121C` con alfa ~66 %.
