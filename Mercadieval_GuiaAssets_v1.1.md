# MERCADIEVAL

## Guía de producción de assets gráficos y sonoros

| Campo | Dato |
|---|---|
| Proyecto | Mercadieval — videojuego 2D en Unity 6.3 LTS |
| Empresa de desarrollo | SXPnosa |
| Documento | Guía de producción de assets, v1.1 (estándar de 64 px) |
| Fecha | 13 de octubre de 2026 |
| Documento de referencia | Documento de Proyecto v2.0, apartados 1.6 y 1.7 |
| Dirigido a | Diseñador o artista encargado de la producción gráfica y sonora |
| Contacto técnico | Juan Javier Castillo Bretón (integración en Unity) |

## Cambio de estándar en la v1.1: de 32 px a 64 px

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

Este documento es el encargo completo de arte y audio del proyecto. Contiene las reglas de estilo, las especificaciones técnicas, la paleta obligatoria, la nomenclatura y la lista maestra de todo lo que hay que producir, con prioridad y semana de entrega.

**Orden de lectura recomendado:** primero los apartados 1 a 5 (reglas, paleta y especificaciones), una sola vez, porque aplican a todo. Después la lista maestra del apartado 6, que es la lista de trabajo.

**Lo que NO se negocia:** la paleta de 26 colores, la cuadrícula de 64 px, el filtro Point sin suavizado, la nomenclatura de archivos y los tamaños por tipo de asset. Todo lo demás —composición, silueta, personalidad de cada personaje— es criterio del diseñador.

**Cómo se entrega:** cada asset terminado se sube a la carpeta correspondiente del repositorio, con su archivo fuente de Piskel al lado. En el mensaje del commit se escribe el ID del asset, por ejemplo `PJ-01: idle y correr del Mercader`.

**Criterio de aceptación:** un asset se da por terminado cuando cumple la lista de verificación del apartado 5.4. Si falla alguno de esos siete puntos, se devuelve para corrección.

## Glosario breve

| Término | Significado |
|---|---|
| Sprite | Imagen 2D que Unity dibuja en pantalla |
| Tile | Casilla cuadrada de 64 × 64 px con la que se "pinta" el escenario |
| Tileset | Hoja con muchos tiles ordenados en cuadrícula |
| Hoja de sprites | Imagen con todos los cuadros de una animación en fila |
| Cuadro (frame) | Cada dibujo individual de una animación |
| PPU | Píxeles por unidad. Cuántos píxeles del dibujo equivalen a 1 unidad de Unity. Aquí siempre 64 |
| 9-slice | Imagen que Unity estira por los bordes sin deformar las esquinas; se usa en marcos y botones |
| Pivote | Punto de anclaje del sprite. Aquí casi siempre la base (Bottom) |
| Diegético | Elemento que existe dentro del mundo del juego, no en la interfaz |

# 1. Reglas generales de estilo

Estas ocho reglas aplican a **todo** asset gráfico del proyecto, sin excepción, incluida la interfaz.

| # | Regla | Por qué |
|---|---|---|
| 1 | **Pixel art de densidad media (estética 16-bit).** Nada de arte vectorial, fotografía, degradados suaves ni texturas escaneadas, ni siquiera en menús o íconos | El juego debe leerse como una sola pieza. Mezclar estilos es el error más visible |
| 2 | **Todo se dibuja sobre cuadrícula múltiplo de 64 px** y en los tamaños exactos de la tabla del apartado 3.1 | Unity escala por múltiplos enteros; un tamaño fuera de la cuadrícula produce píxeles borrosos |
| 3 | **Sin suavizado (anti-aliasing).** Cada píxel es un color plano de la paleta. No usar pinceles suaves, desenfoque ni opacidad parcial, salvo en las capas de luz y niebla indicadas | El filtro de Unity está en Point: cualquier píxel semitransparente se ve sucio |
| 4 | **Contorno de 1 píxel lógico (2 px reales) en negro de contorno `#15121C`** en todo sprite que se dibuje sobre el escenario (personajes, objetos, enemigos). Los tiles del suelo no llevan contorno | Separa las figuras del fondo y mantiene la legibilidad en la noche |
| 5 | **Máximo 3 tonos por superficie:** luz, base y sombra. No más | Es lo que da la lectura limpia del pixel art y acelera la producción |
| 6 | **Solo los 26 colores de la paleta del apartado 2.** Ningún color fuera de esa lista, en ningún asset | Garantiza la cohesión visual y permite recolorear por código |
| 7 | **Fuente de luz siempre desde arriba y ligeramente a la izquierda.** Las sombras caen abajo a la derecha | Coherencia entre assets dibujados por personas distintas |
| 8 | **Perspectiva cenital (top-down) con ligera inclinación frontal.** Los personajes se ven de tres cuartos desde arriba: se les ve la cara y la parte superior de los hombros, no la coronilla | Es la vista del juego; dibujar un asset en perspectiva lateral lo inutiliza |

## 1.1 La regla de las tres orientaciones

Los personajes se mueven en 4 direcciones, pero **solo se dibujan 3**: sur (de frente), norte (de espaldas) y lateral (mirando a la derecha). La dirección izquierda la genera Unity volteando la lateral por código (`flipX`).

**Consecuencia para el diseñador:** nunca dibujes la vista izquierda. Dibuja siempre la derecha. Esto ahorra el 25 % del trabajo de animación y está ya descontado de los totales de este documento.

**Excepción:** si un personaje tiene un elemento asimétrico que se vería mal al voltearse —un parche en el ojo, una bolsa en un solo hombro, una cicatriz— avísalo antes de dibujarlo y se resuelve centrando el elemento o dibujando la cuarta vista.

## 1.2 Ritmo de animación

Todas las animaciones corren a **12 cuadros por segundo**, salvo donde se indique otra cosa.

| Animación | Cuadros | Duración | Notas de ritmo |
|---|---|---|---|
| Idle | 2 | 1 s (0.5 s por cuadro) | Respiración muy sutil: 1 o 2 px de desplazamiento vertical. No exagerar |
| Correr / Caminar | 6 | 0.5 s | Ciclo completo: contacto, paso bajo, paso alto, contacto opuesto, paso bajo, paso alto |
| Atacar | 4 | 0.33 s | Cuadro 1 anticipación (farol atrás), cuadro 2 impacto (el daño se aplica aquí), cuadros 3-4 recuperación |
| Saltar | 5 | 0.6 s | Cuadro 1 flexión, 2 despegue, 3 punto alto, 4 caída, 5 aterrizaje |
| Flotar (Candil y ánimas) | 4 | 0.8 s | Movimiento de 2 px arriba y abajo, suave y continuo |
| Desvanecer | 6 a 8 | 0.5 s | La figura se disuelve desde abajo; el último cuadro es casi transparente |
| Desmayo | 6 | 1 s, sin repetición | Termina en el suelo y se queda ahí |

## 1.3 Lo que se rechaza

| Error | Qué pasa si se entrega así |
|---|---|
| Píxeles semitransparentes por usar pincel suave | Se ve un halo sucio alrededor del sprite |
| Tamaño que no es múltiplo de 64 | Unity no puede cortar la hoja y el sprite queda desalineado |
| Color fuera de la paleta | Rompe la cohesión; se detecta con el muestreo de color de la revisión |
| Vista izquierda dibujada a mano | Trabajo desperdiciado y riesgo de que no coincida con la derecha volteada |
| Pivote mal puesto | El personaje "flota" o se hunde en el suelo |
| Píxeles de medio tamaño (bloques de 2 × 2 con dos colores) | La imagen deja de ser pixel art uniforme y el contorno se ve irregular |
| Archivo con nombre distinto al de la convención | No se encuentra en el repositorio y se duplica el trabajo |
| Exportado en JPG | El JPG no tiene transparencia y comprime con pérdida: destruye el pixel art |

# 2. Paleta de colores obligatoria

26 colores. **Ningún asset puede introducir un color fuera de esta lista.** Se entrega al diseñador como archivo `.pal` de Piskel junto con este documento.

## 2.1 Paleta de día (cálidos y terrosos)

| # | Nombre | HEX | RGB | Dónde se usa |
|---|---|---|---|---|
| 01 | Ocre claro | `#E8C07D` | 232, 192, 125 | Luz de otoño, caminos de tierra, paja |
| 02 | Ocre medio | `#C9924B` | 201, 146, 75 | Tejados, cestas, sombra de caminos |
| 03 | Tierra | `#8B5A2B` | 139, 90, 43 | Parcelas del huerto, mandiles, troncos |
| 04 | Tierra oscura | `#5A3821` | 90, 56, 33 | Sombra de troncos y tocones |
| 05 | Madera | `#6B4226` | 107, 66, 38 | Estantes, mostrador, puestos del mercado |
| 06 | Piedra clara | `#B8AFA0` | 184, 175, 160 | Muros, luz de invierno |
| 07 | Piedra media | `#8A8071` | 138, 128, 113 | Empedrado de la plaza |
| 08 | Piedra oscura | `#4F4A42` | 79, 74, 66 | Túnica del Inquisidor, lápidas |
| 09 | Follaje claro | `#7FA650` | 127, 166, 80 | Copas de roble, luz de primavera |
| 10 | Follaje medio | `#4E7B35` | 78, 123, 53 | Pasto, hierbas |
| 11 | Follaje oscuro | `#2E4F22` | 46, 79, 34 | Sombra de follaje, chal de Elvira |
| 12 | Trigo | `#E3B23C` | 227, 178, 60 | Cultivo maduro, paja, oro en el mundo |
| 13 | Rojo teja | `#A8412E` | 168, 65, 46 | Tejados, detalles de ropa |
| 14 | Crema | `#F2E3C6` | 242, 227, 198 | Texto de interfaz, lino, camisas |

## 2.2 Paleta de noche (fríos)

| # | Nombre | HEX | RGB | Dónde se usa |
|---|---|---|---|---|
| 15 | Azul noche | `#1B2340` | 27, 35, 64 | Luz nocturna, fondo de menús |
| 16 | Azul medio | `#2E3C63` | 46, 60, 99 | Sombras nocturnas |
| 17 | Violeta | `#4A3B6B` | 74, 59, 107 | Cuerpo de Candil, niebla |
| 18 | Lila espectral | `#8E7BB5` | 142, 123, 181 | Ánimas y Glotglot |
| 19 | Niebla | `#C3C9E0` | 195, 201, 224 | Alas de Candil, bruma, texto nocturno |

## 2.3 Acentos funcionales

Estos siete colores **tienen significado en el juego**. No se usan como decoración: si aparecen en un asset que no es el suyo, el jugador los lee mal.

| # | Nombre | HEX | RGB | Significado exclusivo |
|---|---|---|---|---|
| 20 | Candil verde | `#3FD16A` | 63, 209, 106 | "Sin peligro". Solo en la luz de Candil |
| 21 | Candil amarillo | `#F2C13D` | 242, 193, 61 | "Peligro". Solo en la luz de Candil y el aviso de anochecer |
| 22 | Fuego | `#E2622B` | 226, 98, 43 | Hoguera, farol encendido, alertas |
| 23 | Integridad | `#C0392B` | 192, 57, 43 | Barra de integridad de la tienda |
| 24 | Vida | `#D64550` | 214, 69, 80 | Barra de vida del jugador |
| 25 | Oro | `#FFD35C` | 255, 211, 92 | Contador de oro, contador de Puntos, monedas |
| 26 | Negro de contorno | `#15121C` | 21, 18, 28 | Contorno de 1 px de todos los sprites |

## 2.4 Reglas de uso de la paleta

1. **Un asset diurno usa la paleta de día más el negro de contorno.** No mezcles azules de noche en un sprite de día: la noche la produce la iluminación de Unity, no el dibujo.
2. **Las ánimas y Glotglot son la excepción:** se dibujan con la paleta de noche porque solo existen de noche.
3. **Los acentos funcionales no decoran.** No pongas rojo de vida en una manzana ni amarillo de Candil en una flor.
4. **Candil se dibuja en dos archivos separados:** el cuerpo con la paleta normal, y la luz (abdomen y halo) en blanco puro `#FFFFFF` en un archivo aparte. El código la tiñe de verde o amarillo. Si dibujas la luz ya coloreada, no se podrá cambiar.
5. **Para una superficie usa tres tonos consecutivos de la misma familia.** Ejemplo para madera: Ocre medio (luz), Madera (base), Tierra oscura (sombra).

# 3. Especificaciones técnicas

## 3.1 Resolución y formato por tipo de asset

| Tipo de asset | Tamaño por cuadro | Formato | Hoja | Pivote |
|---|---|---|---|---|
| Tile de escenario | 64 × 64 px | PNG-24 con alfa | 1024 × 1024 px (16 × 16 tiles) | — |
| Personaje, NPC, enemigo | 128 × 128 px | PNG-24 con alfa | Una fila por animación | Bottom (centro inferior) |
| Candil | 64 × 64 px | PNG-24 con alfa | Fila de 4 cuadros | Center |
| Glotglot (jefe) | 256 × 256 px | PNG-24 con alfa | Una fila por animación | Bottom |
| Objeto del mundo pequeño | 64 × 64 px | PNG-24 con alfa | Single o Multiple | Bottom |
| Objeto del mundo grande | 128 × 128 px | PNG-24 con alfa | Single o Multiple | Bottom |
| Ícono de inventario | 64 × 64 px | PNG-24 con alfa | Hoja de 512 × 512 px | Center |
| Ícono de interfaz | 128 × 128 px | PNG-24 con alfa | Hoja de 1024 × 1024 px | Center |
| Elemento de interfaz (marco, botón, barra) | Variable, múltiplo de 32 px | PNG-24 con alfa | Single | Center |
| Retrato de diálogo | 256 × 256 px | PNG-24 con alfa | Single | Center |
| Panel de cinemática | 1920 × 1080 px | PNG-24 | Single | Center |
| Fondo de pantalla completa | 1920 × 1080 px | PNG-24 | Single | Center |
| Textura de partícula | 64 × 64 px (niebla 256 × 256) | PNG-24 con alfa | Single | Center |

**Sobre los paneles de 1920 × 1080:** se dibujan a 480 × 270 px y se escalan ×4 con interpolación "vecino más cercano" (Nearest Neighbor) al exportar. **Nunca se dibujan directamente a 1920 × 1080**, porque el resultado no sería pixel art.

## 3.2 Escala y cámara

| Parámetro | Valor |
|---|---|
| Píxeles por unidad (PPU) | **64** — 1 casilla de 64 px = 1 unidad de Unity |
| PPU de íconos de interfaz | 128 |
| Resolución de referencia de la cámara | 1920 × 1080 px |
| Resolución de salida | 1920 × 1080 px (escalado entero ×1) |
| Campo de visión en pantalla | 30 × 16.875 casillas |

**Qué significa en la práctica:** un personaje de 128 × 128 px ocupa 2 × 2 casillas en pantalla. Un tile de 64 px es una casilla. Si dibujas un personaje que ocupa más de 2 casillas de ancho, no cabrá bien en los pasillos del pueblo.

**Altura de referencia del personaje:** dentro del lienzo de 128 × 128 px, el Mercader mide **88 px de alto** y se apoya en el borde inferior. Los 40 px restantes de la parte superior son aire para sombreros, saltos y accesorios. Todos los NPC humanos usan la misma altura para que se vean coherentes entre sí.

## 3.3 Configuración de importación en Unity

Esto lo aplica el programador, pero conviene conocerlo porque explica varias de las reglas anteriores.

| Propiedad | Valor |
|---|---|
| Texture Type | Sprite (2D and UI) |
| Pixels Per Unit | 64 (128 en íconos de interfaz) |
| Filter Mode | **Point (no filter)** |
| Compression | **None** en sprites de juego; Normal Quality en paneles de 1920 × 1080 |
| Mesh Type | Full Rect |
| Generate Mip Maps | Desactivado |
| Wrap Mode | Clamp |
| Alpha Is Transparency | Activado |
| Max Size | 2048 |
| Slice | Grid By Cell Size: 64 × 64, 128 × 128 o 256 × 256 según el tipo |

## 3.4 Capas de ordenamiento

El escenario se dibuja en este orden, de atrás hacia adelante. Conviene saberlo al diseñar los tiles.

`Fondo` → `Suelo` → `Decorado` → `Objetos` → `Personajes` → `Clima` → `Efectos` → `UI`

Dentro de la capa `Personajes`, Unity ordena por la posición vertical: lo que está más abajo en pantalla se dibuja encima. Por eso el pivote va en la base del sprite.

# 4. Nomenclatura y organización

## 4.1 Formato del nombre de archivo

```
<tipo>_<categoria>_<nombre>_<variante>_<NN>.<ext>
```

Todo en **minúsculas**, **sin acentos**, **sin espacios**, con guion bajo como separador.

**Ejemplos correctos:**

| Archivo | Qué es |
|---|---|
| `spr_pj_mercader_correr_sur.png` | Hoja de 6 cuadros del Mercader corriendo hacia el sur |
| `spr_pj_mercader_atacar_lat.png` | Hoja del Mercader atacando de lado |
| `spr_enm_anima_errante_flotar_nor.png` | Ánima errante flotando de espaldas |
| `spr_tile_bosque.png` | Tileset del bosque |
| `spr_obj_roble_01.png` | Primera variante del roble en pie |
| `spr_item_lena.png` | Ícono de inventario de la leña |
| `spr_ui_icono_oro.png` | Ícono de oro de la interfaz |
| `spr_ret_bruno.png` | Retrato de diálogo de Bruno |
| `spr_cin_cin02_panel03.png` | Tercer panel de la cinemática CIN-02 |
| `sfx_talar.wav` | Efecto de sonido de talar |
| `mus_pueblo_dia_otono.ogg` | Música del pueblo, de día, en otoño |

**Ejemplos incorrectos:** `Mercader Correr.png` (espacios y mayúsculas), `spr_pj_mercader_correr_izquierda.png` (la izquierda no se dibuja), `leña.png` (acento y sin prefijo), `final_v2_bueno_DEFINITIVO.png`.

## 4.2 Prefijos

| Prefijo | Significado |
|---|---|
| `spr_` | Cualquier sprite |
| `tile_` | Tileset de escenario |
| `pj_` | Personaje jugable o NPC con historia |
| `enm_` | Enemigo |
| `obj_` | Objeto del mundo |
| `item_` | Artículo de inventario |
| `ui_` | Elemento de interfaz |
| `ret_` | Retrato de diálogo |
| `cin_` | Panel de cinemática |
| `bg_` | Fondo de pantalla completa |
| `vfx_` | Textura de partícula |
| `mus_` | Pista musical |
| `sfx_` | Efecto de sonido |

## 4.3 Sufijos de orientación

| Sufijo | Orientación |
|---|---|
| `_sur` | De frente, mirando hacia el jugador |
| `_nor` | De espaldas |
| `_lat` | De lado, mirando a la **derecha** |

## 4.4 Estructura de carpetas del repositorio

```
Assets/
  Art/
    Characters/      PJ-01 a PJ-13, EN-01 a EN-04
    Tilesets/        TS-01 a TS-06
    Objects/         OB-01 a OB-32
    Items/           IT-01 a IT-11
    UI/
      Icons/         UI-01 a UI-18
      Elements/      UI-19 a UI-33
    Portraits/       RT-01 a RT-07
    Cinematics/      CN-01 a CN-19
    Screens/         BG-01 a BG-05
    VFX/             FX-01 a FX-07
  Audio/
    Music/           MU-01 a MU-07
    SFX/             SX-01 a SX-26
  _Source/           Archivos .piskel y .aup3 originales, misma estructura
```

## 4.5 Entrega y control de versiones

- Cada asset terminado va a su carpeta, con el archivo fuente en la carpeta espejo de `_Source/`.
- Mensaje de commit: `<ID>: <qué se entregó>`. Ejemplo: `PJ-05: idle y martillar de Bruno`.
- **No se versiona en el nombre del archivo.** Nada de `_v2`, `_final`, `_bueno`. Para eso está Git.
- Si un asset se corrige, se sobrescribe el archivo y se hace un commit nuevo.

# 5. Proceso de trabajo

## 5.1 Prioridades

| Código | Significado | Qué pasa si falta |
|---|---|---|
| **M** | Imprescindible | El juego no se puede entregar sin esto |
| **S** | Importante | Se entrega si el calendario lo permite; hay un sustituto temporal |
| **C** | Deseable | Se recorta sin consecuencias si falta tiempo |

## 5.2 Calendario de entrega

El juego se programa en paralelo sobre **formas grises** (rectángulos de color plano) que se sustituyen por el arte final conforme llega. Esto significa que **un retraso en el arte no bloquea la programación**, pero sí la build de presentación.

| Sprint | Fechas | Qué se entrega |
|---|---|---|
| S4 | 19 – 25 oct | Tileset del pueblo y del bosque, el Mercader completo, Candil |
| S5 | 26 oct – 1 nov | Comerciantes, clientes, ladrón, objetos del mundo, íconos de inventario |
| S6 | 2 – 8 nov | Ánimas, guardias, Inquisidor, tileset del cementerio, interfaz completa |
| S7 | 9 – 15 nov | Glotglot, retratos, paneles de cinemática, pantallas, partículas |
| S8 | 16 – 22 nov | Correcciones derivadas de la beta y pulido |

## 5.3 Flujo de un asset

1. **Boceto rápido** a baja resolución o a lápiz, para validar silueta y lectura. Se comparte antes de dibujar los píxeles finales.
2. **Visto bueno del equipo** sobre el boceto. Es el momento barato para cambiar algo.
3. **Dibujo final** en Piskel, con la paleta cargada.
4. **Exportación** en PNG según el apartado 3.1.
5. **Entrega** al repositorio con el archivo fuente.
6. **Revisión** contra la lista de verificación.
7. **Integración** en Unity por el programador.

Los bocetos del paso 1 **se conservan**: son evidencia requerida del informe técnico del proyecto.

## 5.4 Lista de verificación antes de entregar

Siete puntos. Si falla uno, el asset se devuelve.

| # | Verificación |
|---|---|
| 1 | El tamaño en píxeles es exactamente el que indica la tabla del apartado 3.1 |
| 2 | Todos los colores pertenecen a la paleta de 26 colores |
| 3 | No hay píxeles semitransparentes, salvo en capas de luz o niebla autorizadas |
| 4 | El contorno es de 1 px en `#15121C` (excepto tiles de suelo) |
| 5 | El nombre del archivo sigue la convención del apartado 4.1 |
| 6 | Está exportado en PNG-24 con canal alfa, nunca en JPG |
| 7 | El archivo fuente de Piskel está en la carpeta `_Source/` correspondiente |

# 6. Lista maestra de assets

Esta es la lista de trabajo. Cada fila es un entregable con su identificador, su tamaño, su prioridad y la semana en que se necesita.

## 6.1 Personajes, NPC y enemigos

**Recordatorio:** solo se dibujan 3 orientaciones (sur, norte y lateral derecha). La izquierda la genera el código. La columna "Animaciones" se lee como `Nombre orientaciones x cuadros`.

| ID | Personaje | Tamano por cuadro | Animaciones (orientaciones x cuadros) | Cuadros | Pr. | Sprint |
|---|---|---|---|---|---|---|
| PJ-01 | El Mercader (jugador) | 128 x 128 | Idle 3x2, Correr 3x6, Atacar 3x4, Saltar 3x5, Desmayo 1x6 | **57** | M | S4 |
| PJ-02 | Candil - cuerpo | 128 x 128 | Flotar 1x4, Alerta 1x2 | **6** | M | S4 |
| PJ-03 | Candil - capa de luz (se tine por codigo) | 128 x 128 | Flotar 1x4 | **4** | M | S4 |
| PJ-04 | Tomas el granjero | 128 x 128 | Idle 1x2, Atender 1x4 | **6** | M | S5 |
| PJ-05 | Bruno el herrero | 128 x 128 | Idle 1x2, Martillar 1x4 | **6** | M | S5 |
| PJ-06 | Elvira la herbolaria | 128 x 128 | Idle 1x2, Atender 1x4 | **6** | M | S5 |
| PJ-07 | El Inquisidor | 128 x 128 | Idle 1x2, Atender 1x4 | **6** | M | S6 |
| PJ-08 | Guardia del templo (decorativo) | 128 x 128 | Idle 1x2 | **2** | C | S6 |
| PJ-09 | Cliente - sprite base | 128 x 128 | Idle 3x2, Caminar 3x6 | **24** | M | S5 |
| PJ-10 | Cliente - variante Campesino (recoloreo + sombrero) | 128 x 128 | Idle 3x2, Caminar 3x6 | **24** | M | S5 |
| PJ-11 | Cliente - variante Artesano (recoloreo + delantal) | 128 x 128 | Idle 3x2, Caminar 3x6 | **24** | M | S5 |
| PJ-12 | Cliente - variante Dama del pueblo (recoloreo + falda) | 128 x 128 | Idle 3x2, Caminar 3x6 | **24** | M | S5 |
| PJ-13 | Guardia a sueldo | 128 x 128 | Idle 3x2, Caminar 3x6, Atacar 3x4 | **36** | S | S6 |
| EN-01 | Ladron | 128 x 128 | Idle 3x2, Correr 3x6, Robar 1x4, Huir 1x4 | **32** | M | S5 |
| EN-02 | Anima errante | 128 x 128 | Flotar 3x4, Atacar 3x3, Desvanecer 1x6 | **27** | M | S6 |
| EN-03 | Anima veloz (silueta propia, paleta mas clara) | 128 x 128 | Flotar 3x4, Atacar 3x3, Desvanecer 1x6 | **27** | M | S6 |
| EN-04 | Glotglot (jefe final) | 256 x 256 | Idle 1x4, Avanzar 1x4, Golpear 1x5, Desvanecer 1x8 | **21** | M | S7 |

**Total de cuadros de personaje: 332**

### Notas por personaje

| ID | Indicaciones de diseño |
|---|---|
| PJ-01 | Mercader, 24 años, delgado, estatura media, hombros estrechos. Cabello castaño corto despeinado, barba de pocos días, ojeras marcadas. Camisa de lino crudo, chaleco de lana ocre, delantal de cuero gastado, botas de media caña. **Lleva un farol de mano colgado al cinto**: en la animación de atacar, el farol es el arma y debe leerse claramente. Altura 88 px dentro del lienzo |
| PJ-02 | Candil: mezcla de polilla y luciérnaga del tamaño de un gato. Cuerpo redondo violeta `#4A3B6B`, ojos grandes, antenas cortas, alas pálidas `#C3C9E0`. **No dibujar el abdomen luminoso aquí**: va en PJ-03 |
| PJ-03 | Solo el abdomen y el halo de luz de Candil, **en blanco puro `#FFFFFF`**, en archivo separado y alineado píxel a píxel con PJ-02. El código lo tiñe de verde o amarillo |
| PJ-04 | Tomás el granjero: aspecto rústico, sombrero de paja, ropa de trabajo en tonos ocres. Está siempre detrás de su puesto |
| PJ-05 | Bruno el herrero: 55 años, robusto, ancho de espalda, barba gris, camisa arremangada, mandil de herrero `#8B5A2B`, muñequeras de cuero. Es el personaje más cálido del reparto |
| PJ-06 | Elvira la herbolaria: 40 años, complexión media, **postura encogida** (se esconde). Chal verde oscuro `#2E4F22`, falda larga parda, canasta de hierbas al brazo |
| PJ-07 | El Inquisidor: 50 años, alto, enjuto, **espalda muy recta**. Túnica oscura `#4F4A42` con insignias religiosas, guantes, sombrero de ala ancha. Debe leerse como autoridad, no como monstruo |
| PJ-08 | Guardia del templo: decorativo, nunca interactúa. Puede ser una silueta simple con lanza |
| PJ-09 | Cliente base: figura neutra sin rasgos marcados, pensada para recolorear. Es la plantilla de PJ-10, PJ-11 y PJ-12 |
| PJ-10 a PJ-12 | Variantes del cliente base: **mismo esqueleto y mismos cuadros**, solo cambian paleta de ropa y un accesorio distintivo (sombrero, delantal, falda larga). No redibujar la animación |
| PJ-13 | Guardia a sueldo: armadura ligera, lanza. Debe distinguirse a simple vista del guardia del templo y del ladrón, porque de noche aparecen juntos |
| EN-01 | Ladrón: encapuchado, encorvado, silueta humana clara. **No debe parecer un fantasma**: su amenaza es distinta a la de las ánimas |
| EN-02 | Ánima errante: figura translúcida envuelta en telas quemadas, lila espectral `#8E7BB5`. Sin rostro definido. Bordes irregulares y alfa parcial permitido en el contorno exterior |
| EN-03 | Ánima veloz: misma familia visual que EN-02 pero **silueta más estrecha y alargada**, paleta más clara. El jugador debe distinguirlas en medio segundo |
| EN-04 | Glotglot: 256 × 256 px. Figura translúcida envuelta en cenizas y telas quemadas, **sin origen único ni rostro**. Es la suma de muchas ánimas: la silueta puede sugerir varias figuras superpuestas. Es el asset más visible del juego |

## 6.2 Tilesets de escenario

Un tileset es una hoja de 1024 × 1024 px con 256 casillas de 64 × 64 px (o de 512 × 512 px con 64 casillas, en TS-03 y TS-04). No hace falta llenar las 256: la columna "Tiles útiles" indica cuántos se necesitan de verdad.

| ID | Tileset | Hoja | Tiles | Contenido obligatorio | Pr. | Sprint |
|------|-----------|--------|-----|--------------------------------------------|------|--------|
| TS-01 | Pueblo — exterior | 1024 × 1024 | ~90 | Empedrado de la plaza (con bordes), tierra de camino, pasto, muros de casa, tejados, puertas y ventanas de fondo, bordes entre superficies, decorado (barriles, cajas, carteles, charcos) | M | S4 |
| TS-02 | Bosque | 1024 × 1024 | ~70 | Suelo de hojarasca, pasto alto, tierra, agua del arroyo (con bordes y 2 cuadros de animación), piedras de paso, raíces, maleza de borde, troncos caídos | M | S4 |
| TS-03 | Interior de la tienda | 512 × 512 | ~30 | Piso de madera, alfombra, muros interiores, repisas de fondo, ventana | M | S5 |
| TS-04 | Huerto | 512 × 512 | ~20 | Tierra arada, tierra regada, borde de parcela, cerca de madera | M | S5 |
| TS-05 | Cementerio e iglesia | 1024 × 1024 | ~70 | Piso de piedra, tierra removida, muro de piedra del atrio, columnas, reja, escalones, nave de la iglesia, vitral de fondo | M | S6 |
| TS-06 | Estados del bosque — variantes de paleta | 1024 × 1024 | ~40 | Variantes Degradado y Devastado de TS-02: follaje reducido, suelo seco, tonos más crudos | M | S6 |

**Sobre TS-06:** no se redibuja el bosque entero. Son las casillas que cambian visiblemente entre los tres estados —suelo, maleza y hojarasca— en sus dos variantes degradadas. El resto se reutiliza de TS-02.

**Rule Tiles requeridos** (el programador los configura, el diseñador entrega las piezas): caminos de tierra, agua del arroyo, borde de pasto y muro de piedra. Cada uno necesita 16 variantes de borde dentro de su tileset.

## 6.3 Objetos del mundo

| ID | Objeto | Tamaño | Variantes o estados | Pr. | Sprint |
|----|------------------------------|---------|--------------------------------|----|--------|
| OB-01 | Roble en pie | 128 × 128 | 3 variantes de silueta | M | S4 |
| OB-02 | Tocón | 64 × 64 | 1 | M | S4 |
| OB-03 | Roble joven plantado | 64 × 64 | 3 fases de crecimiento | M | S6 |
| OB-04 | Mata de hierbas | 64 × 64 | 2 (llena, recolectada) | M | S4 |
| OB-05 | Grupo de hongos | 64 × 64 | 2 (lleno, recolectado) | M | S4 |
| OB-06 | Parcela de huerto | 64 × 64 | 2 (vacía, sembrada) | M | S5 |
| OB-07 | Cultivo de trigo | 64 × 64 | 3 fases | M | S5 |
| OB-08 | Cultivo de nabo | 64 × 64 | 3 fases | M | S5 |
| OB-09 | Cultivo de calabaza | 64 × 64 | 3 fases | M | S5 |
| OB-10 | Estante de la tienda | 128 × 128 | 2 (vacío, con mercancía) | M | S5 |
| OB-11 | Mostrador | 128 × 128 | 1 | M | S5 |
| OB-12 | Cama | 128 × 128 | 1 | M | S5 |
| OB-13 | Puesto de Tomás | 128 × 128 | 1 | M | S5 |
| OB-14 | Puesto de Bruno (forja) | 128 × 128 | 1 | M | S5 |
| OB-15 | Puesto de Elvira | 128 × 128 | 1 | M | S5 |
| OB-16 | Puesto del Inquisidor | 128 × 128 | 1 | M | S6 |
| OB-17 | Puesto de guardias | 128 × 128 | 1 | S | S6 |
| OB-18 | Puerta de la tienda | 128 × 128 | 2 (normal, reforzada) | S | S6 |
| OB-19 | Farol de fachada | 64 × 64 | 2 (encendido, apagado) | M | S5 |
| OB-20 | Pila de leña de la hoguera | 128 × 128 | 1, **apagada siempre** | M | S6 |
| OB-21 | Lápida | 64 × 64 | 3 variantes | M | S6 |
| OB-22 | Portón del cementerio | 128 × 128 | 2 (con cadena, abierto) | M | S6 |
| OB-23 | Bellota | 64 × 64 | 1 + brillo de 4 cuadros | M | S6 |
| OB-24 | Bellota de roble antiguo | 64 × 64 | 1 + brillo de 4 cuadros | M | S7 |
| OB-25 | Moneda perdida | 64 × 64 | 4 cuadros de giro | M | S5 |
| OB-26 | Letrero del sendero al bosque | 64 × 64 | 1 | C | S6 |
| OB-27 | Carro de leña (decorativo) | 128 × 128 | 1 | C | S6 |
| OB-28 | Barril y cajas | 64 × 64 | 3 variantes | C | S5 |
| OB-29 | Sombra de personaje | 64 × 64 | 1, elipse semitransparente | M | S4 |
| OB-30 | Marcador de interacción "[E]" | 64 × 64 | 1 | M | S4 |

## 6.4 Íconos de inventario

Todos de 64 × 64 px, sobre una sola hoja de 512 × 512 px. Deben distinguirse entre sí **a simple vista y en miniatura**: es lo que el jugador mira cien veces por partida.

| ID | Artículo | Pr. | Sprint |
|---|---|---|---|
| IT-01 | Semilla de trigo | M | S5 |
| IT-02 | Semilla de nabo | M | S5 |
| IT-03 | Semilla de calabaza | M | S5 |
| IT-04 | Trigo | M | S5 |
| IT-05 | Nabo | M | S5 |
| IT-06 | Calabaza | M | S5 |
| IT-07 | Leña | M | S5 |
| IT-08 | Hierbas | M | S5 |
| IT-09 | Hongos | M | S5 |
| IT-10 | Cuerda | M | S5 |
| IT-11 | Infusión de hierbas | M | S6 |

**Advertencia:** las tres semillas tienden a verse iguales. Diferéncialas por la forma del saquito y por un color de etiqueta distinto, no solo por el tamaño.

## 6.5 Íconos de interfaz

Todos de 128 × 128 px, sobre una hoja de 1024 × 1024 px.

| ID | Ícono | Uso | Pr. | Sprint |
|---|---|---|---|---|
| UI-01 | Moneda de oro | Contador de oro | M | S6 |
| UI-02 | Hoja | Contador de Puntos | M | S6 |
| UI-03 | Corazón | Barra de vida | M | S6 |
| UI-04 | Escudo o casa | Barra de integridad | M | S6 |
| UI-05 | Sol | Reloj, fase de día | M | S6 |
| UI-06 | Luna | Reloj, fase de noche | M | S6 |
| UI-07 | Antorcha | Marca los artículos que interesan a la Inquisición | M | S6 |
| UI-08 | Hoja pequeña | Marca los artículos que suman Puntos | M | S6 |
| UI-09 | Candado | Contenido bloqueado | S | S7 |
| UI-10 | Palomita | Prueba completada | M | S7 |
| UI-11 | Círculo vacío | Prueba pendiente | M | S7 |
| UI-12 | Flecha | Navegación y avance de diálogo | M | S6 |
| UI-13 | Cruz de cerrar | Cerrar ventana | M | S6 |
| UI-14 | Engrane | Opciones | M | S7 |
| UI-15 | Altavoz activo | Volumen | M | S7 |
| UI-16 | Altavoz silenciado | Volumen en cero | M | S7 |
| UI-17 | Pantalla | Pantalla completa | M | S7 |
| UI-18 | Medio círculo claro-oscuro | Contraste | M | S7 |

## 6.6 Elementos de interfaz

| ID | Elemento | Tamaño | Detalle | Pr. | Sprint |
|---|---|---|---|---|---|
| UI-19 | Marco de ventana (9-slice) | 192 × 192 px | Esquinas de 64 px; se estira sin deformar | M | S6 |
| UI-20 | Botón | 320 × 96 px | 3 estados: normal, sobre, pulsado | M | S6 |
| UI-21 | Ranura de barra rápida | 96 × 96 px | 2 estados: normal, seleccionada | M | S6 |
| UI-22 | Ranura de inventario | 96 × 96 px | 2 estados | M | S6 |
| UI-23 | Barra de vida | 384 × 48 px | Fondo y relleno, archivos separados | M | S6 |
| UI-24 | Barra de integridad | 384 × 48 px | Fondo y relleno, archivos separados | M | S6 |
| UI-25 | Reloj con barra día/noche | 512 × 64 px | Fondo y relleno | M | S6 |
| UI-26 | Caja de diálogo | 1792 × 384 px | Con hueco de 256 px para el retrato | M | S7 |
| UI-27 | Panel de notificación | 640 × 128 px | Mensajes de 3 s | M | S6 |
| UI-28 | Panel de ventana de comercio | 1536 × 1024 px | Con dos pestañas | M | S6 |
| UI-29 | Pestaña | 320 × 80 px | 2 estados: activa, inactiva | M | S6 |
| UI-30 | Deslizador (slider) | 512 × 64 px | Riel y manija | M | S7 |
| UI-31 | Interruptor (toggle) | 128 × 64 px | 2 estados | M | S7 |
| UI-32 | Barra de desplazamiento | 48 × 512 px | Riel y manija | S | S7 |
| UI-33 | Tipografía bitmap | Altura de mayúscula 16 px (8 px lógicos; tamaño 20 en Unity) | `.ttf`, con acentos y signos de apertura del español | M | S5 |

**Sobre UI-33:** es el asset más fácil de olvidar y bloquea toda la interfaz. Debe incluir **á é í ó ú ñ Ñ ü ¿ ¡**. Si no se produce a medida, se elige una fuente pixel con licencia libre que los tenga y se acredita en los créditos.

## 6.7 Retratos de diálogo

256 × 256 px. Busto del personaje de frente, con expresión neutra, sobre fondo transparente.

| ID | Retrato | Pr. | Sprint |
|---|---|---|---|
| RT-01 | El Mercader | M | S7 |
| RT-02 | Bruno | M | S7 |
| RT-03 | Elvira | M | S7 |
| RT-04 | El Inquisidor | M | S7 |
| RT-05 | Candil | M | S7 |
| RT-06 | Glotglot | M | S7 |
| RT-07 | Tomás | S | S7 |

## 6.8 Paneles de cinemática

1920 × 1080 px, **dibujados a 480 × 270 px y escalados ×4 con vecino más cercano**. Imagen fija, sin animación. El texto lo pone Unity encima: **no escribas texto dentro de la imagen**, salvo en los paneles de dato, donde la cifra forma parte de la composición.

| ID | Cinemática | Panel | Qué se ve | Pr. | Sprint |
|---|---|---|---|---|---|
| CN-01 | CIN-01 Apertura | 1 | Carruaje en el camino, bosque frondoso al fondo | M | S7 |
| CN-02 | CIN-01 Apertura | 2 | Fachada de la tienda cerrada, faroles apagados | M | S7 |
| CN-03 | CIN-01 Apertura | 3 | Interior de la tienda, Candil apagada sobre el mostrador | M | S7 |
| CN-04 | CIN-01 Apertura | 4 | El bosque completo, los 12 robles en pie | M | S7 |
| CN-05 | CIN-02 Cierre nivel 1 | 1 | El recaudador cobrando en el mostrador | M | S7 |
| CN-06 | CIN-02 Cierre nivel 1 | 2 | Carro cargado de leña saliendo del pueblo | M | S7 |
| CN-07 | CIN-02 Cierre nivel 1 | 3 | **Panel de dato:** mapa de México sobre fondo oscuro, con la cifra en grande | M | S7 |
| CN-08 | CIN-02 Cierre nivel 1 | 4 | **Panel de dato:** silueta de árboles que se reduce, con la cifra | M | S7 |
| CN-09 | CIN-02 Cierre nivel 1 | 5 | El bosque del juego con los tocones. **Fondo neutro: Unity escribe el número encima** | M | S7 |
| CN-10 | CIN-03 Cierre nivel 2 | 1 | La plaza en invierno, puesto del Inquisidor con fila de gente | M | S7 |
| CN-11 | CIN-03 Cierre nivel 2 | 2 | Pila de leña creciendo junto al puesto del Inquisidor | M | S7 |
| CN-12 | CIN-03 Cierre nivel 2 | 3 | **Panel de dato:** gráfica de dos barras, 2001 contra 2018 | M | S7 |
| CN-13 | CIN-03 Cierre nivel 2 | 4 | **Panel de dato:** lista de las cuatro causas de deforestación | M | S7 |
| CN-14 | CIN-03 Cierre nivel 2 | 5 | Una bellota en la mano del Mercader, primer plano | M | S7 |
| CN-15 | CIN-03 Cierre nivel 2 | 6 | El bosque del juego en su estado actual, fondo neutro | M | S7 |
| CN-16 | CIN-04 Final | A | **"El bosque renace":** robles jóvenes creciendo, amanecer despejado | M | S7 |
| CN-17 | CIN-04 Final | B | **"Entre dos fuegos":** el pueblo dividido, media plaza en sombra | M | S7 |
| CN-18 | CIN-04 Final | C | **"El precio de la hoguera":** tienda próspera rodeada de tocones, noche cerrada | M | S7 |
| CN-19 | CIN-04 Derrota | D | **"La tienda en cenizas":** la tienda quemada al amanecer | M | S7 |

**Sobre los paneles de dato (CN-07, CN-08, CN-12, CN-13):** son los que cumplen el criterio de la rúbrica sobre datos del problema ambiental. La cifra debe ser el elemento dominante de la composición, legible desde lejos, con la fuente ("Fuente: CONAFOR") en tamaño pequeño al pie. Los textos exactos están en el apartado 1.4.6 del Documento de Proyecto v2.0.

**Sobre el contenido:** ninguna cinemática muestra ejecuciones, hogueras encendidas, sangre ni violencia explícita. La pila de leña aparece siempre apagada. Esto sostiene la clasificación B15 / PEGI 12 y es un requerimiento verificable (RNF-14).

## 6.9 Pantallas completas

1920 × 1080 px, mismo método que las cinemáticas.

| ID | Pantalla | Contenido | Pr. | Sprint |
|---|---|---|---|---|
| BG-01 | Menú principal | Fachada de la tienda de noche, con Candil en verde. Espacio libre a la izquierda para el título y los botones | M | S7 |
| BG-02 | Pantalla de puntuación | Fondo sobrio, pergamino o tabla de madera, con mucho espacio para el desglose de cifras | M | S7 |
| BG-03 | Pantalla de cierre educativa | Fondo neutro oscuro, con espacio para tres bloques de texto | M | S7 |
| BG-04 | Fin de partida | La tienda cerrada bajo la lluvia | M | S7 |
| BG-05 | Créditos | Repetición sencilla del bosque al amanecer, con espacio para texto en desplazamiento | S | S7 |

## 6.10 Texturas de partícula

Imágenes pequeñas que Unity multiplica y anima. Formas simples, sin detalle fino.

| ID | Efecto | Tamaño | Descripción | Pr. | Sprint |
|---|---|---|---|---|---|
| FX-01 | Desvanecimiento de ánima | 64 × 64 | Mota de luz lila que se difumina | M | S6 |
| FX-02 | Polvo de tala | 64 × 64 | Astilla y serrín | M | S5 |
| FX-03 | Hoja que cae | 64 × 64 | 3 variantes de hoja | S | S6 |
| FX-04 | Impacto de golpe | 64 × 64 | Destello corto, 4 cuadros | M | S6 |
| FX-05 | Brillo de collectible | 64 × 64 | Chispa que gira | M | S6 |
| FX-06 | Chispa de fuego | 64 × 64 | Punto naranja | S | S7 |
| FX-07 | Niebla nocturna | 256 × 256 | Mancha difusa, **alfa parcial permitido** | M | S6 |

## 6.11 Música

Pistas en `.ogg` Vorbis a 44.1 kHz, estéreo, cerca de 128 kbps. Todas deben repetirse sin corte audible (loop limpio).

| ID | Pista | Duración objetivo | Carácter | Pr. | Sprint |
|---|---|---|---|---|---|
| MU-01 | Menú principal | 1:30 | Lenta, melancólica, instrumento solo | M | S7 |
| MU-02 | Pueblo de día — otoño | 2:00 | Cálida, laboriosa, ritmo tranquilo | M | S6 |
| MU-03 | Pueblo de día — invierno | 2:00 | Variación más sobria de MU-02 | S | S7 |
| MU-04 | Pueblo de día — primavera | 2:00 | Variación más tensa de MU-02 | S | S7 |
| MU-05 | Noche | 1:30 | Tensa, percusión baja, sin melodía clara | M | S6 |
| MU-06 | Jefe final | 2:00 | La más intensa del juego; coral si es posible | M | S7 |
| MU-07 | Finales y créditos | 2:00 | Resolutiva, sin triunfalismo | M | S7 |

Si no se componen a medida, se usan pistas con licencia **CC0 o CC-BY** y se acreditan en los créditos con autor, título y enlace. Esa acreditación es obligatoria.

## 6.12 Efectos de sonido

`.wav` PCM de 16 bits a 44.1 kHz, mono, normalizados a −3 dBFS de pico. Cortos y secos: casi todos duran menos de medio segundo.

| ID | Efecto | Duración | Nota | Pr. | Sprint |
|---|---|---|---|---|---|
| SX-01 | Paso sobre tierra | 0.2 s | 3 variantes, se alternan | M | S5 |
| SX-02 | Paso sobre piedra | 0.2 s | 3 variantes | S | S6 |
| SX-03 | Salto | 0.3 s | | M | S5 |
| SX-04 | Aterrizaje | 0.2 s | | M | S5 |
| SX-05 | Golpe con el farol | 0.3 s | | M | S6 |
| SX-06 | Impacto en enemigo | 0.2 s | | M | S6 |
| SX-07 | Jugador recibe daño | 0.3 s | | M | S6 |
| SX-08 | Ánima desvaneciéndose | 0.6 s | | M | S6 |
| SX-09 | Recolectar hierbas u hongos | 0.4 s | | M | S5 |
| SX-10 | Talar árbol | 1.2 s | Hacha repetida y caída | M | S5 |
| SX-11 | Plantar bellota | 0.5 s | Tierra removida | M | S6 |
| SX-12 | Plantar semilla | 0.4 s | | M | S5 |
| SX-13 | Cosechar | 0.4 s | | M | S5 |
| SX-14 | Moneda al vender | 0.4 s | El sonido más repetido del juego: que no canse | M | S5 |
| SX-15 | Compra rechazada | 0.3 s | Tono negativo breve | M | S5 |
| SX-16 | Abrir ventana de interfaz | 0.2 s | | M | S6 |
| SX-17 | Cerrar ventana | 0.2 s | | M | S6 |
| SX-18 | Navegar en menú | 0.1 s | | M | S6 |
| SX-19 | Confirmar | 0.2 s | | M | S6 |
| SX-20 | **Candil cambia a amarillo** | 0.4 s | Requerimiento explícito (RNF-15). Debe oírse por encima de la música | M | S5 |
| SX-21 | Campana de anochecer | 1.5 s | A las 19:00 | M | S6 |
| SX-22 | Prueba completada | 0.8 s | Positivo, breve | M | S7 |
| SX-23 | Impuesto cobrado | 0.6 s | | M | S6 |
| SX-24 | Mejora comprada | 0.8 s | | S | S7 |
| SX-25 | Robo en la tienda | 0.5 s | Cristal o madera rota | M | S6 |
| SX-26 | Rugido de Glotglot | 2.0 s | Voces superpuestas | M | S7 |
| SX-27 | Avance de cuadro de diálogo | 0.1 s | Muy discreto | S | S7 |

# 7. Resumen de carga de trabajo

## 7.1 Totales por categoría

| Categoría | Apartado | Entregables | M | S | C |
|---|---|---|---|---|---|
| Personajes y NPC | 6.1 | 13 | 11 | 1 | 1 |
| Enemigos | 6.1 | 4 | 4 | 0 | 0 |
| Tilesets de escenario | 6.2 | 6 | 6 | 0 | 0 |
| Objetos del mundo | 6.3 | 30 | 25 | 2 | 3 |
| Íconos de inventario | 6.4 | 11 | 11 | 0 | 0 |
| Interfaz: iconos y elementos | 6.5 y 6.6 | 33 | 31 | 2 | 0 |
| Retratos de diálogo | 6.7 | 7 | 6 | 1 | 0 |
| Paneles de cinemática | 6.8 | 19 | 19 | 0 | 0 |
| Pantallas completas | 6.9 | 5 | 4 | 1 | 0 |
| Texturas de partícula | 6.10 | 7 | 5 | 2 | 0 |
| Música | 6.11 | 7 | 5 | 2 | 0 |
| Efectos de sonido | 6.12 | 27 | 24 | 3 | 0 |
| **Total** | | **169** | **151** | **14** | **4** |

**169 entregables en total**, de los cuales **151 son imprescindibles**. Los 14 marcados como S y los 4 marcados como C son el margen de recorte si el calendario aprieta; se recortan en ese orden.

## 7.2 Carga de animación

| Concepto | Cantidad |
|---|---|
| Cuadros de animación de personaje, NPC y enemigo | **332** |
| Tiles útiles estimados en los 6 tilesets | ~320 |
| Imágenes de 1920 × 1080 (cinemáticas y pantallas) | 24 |
| Pistas de música | 7 |
| Efectos de sonido | 27 |

Los 332 cuadros ya tienen descontado el ahorro de la regla de las tres orientaciones (apartado 1.1). Sin esa regla serían cerca de 440.

## 7.3 Reparto por sprint

| Sprint | Fechas | Entregables | Lo más pesado |
|---|---|---|---|
| S4 | 19 – 25 oct | 11 | Pocos entregables pero el más caro de todos: el Mercader completo son 57 cuadros, más dos tilesets completos |
| S5 | 26 oct – 1 nov | 45 | Muchos entregables pequeños: comerciantes, clientes, objetos del huerto e íconos de inventario |
| S6 | 2 – 8 nov | 58 | El sprint más cargado: ánimas, tileset del cementerio y la interfaz entera |
| S7 | 9 – 15 nov | 55 | Glotglot, 19 paneles de cinemática, 5 pantallas y los retratos |
| S8 | 16 – 22 nov | — | Solo correcciones derivadas de la beta |

**Advertencia honesta sobre el calendario.** S6 y S7 concentran 113 de los 169 entregables en dos semanas. Es una carga alta para una sola persona. Tres formas de aliviarla, en orden de preferencia:

1. **Adelantar la interfaz a S5.** Los íconos y elementos de UI (UI-01 a UI-33) no dependen de ninguna decisión pendiente y pueden producirse desde ya.
2. **Adelantar los retratos y los paneles de cinemática a S6.** Los textos de las cinemáticas ya están cerrados en el Documento de Proyecto v2.0, apartado 1.4.6.
3. **Recortar los 18 assets de prioridad S y C.** El juego funciona sin ellos, con sustitutos simples.

## 7.4 Lo que bloquea la programación si se retrasa

El equipo programa sobre formas grises, así que casi nada del arte es bloqueante. Las tres excepciones:

| Asset | Por qué bloquea |
|---|---|
| **UI-33 — Tipografía bitmap** | Sin fuente con acentos y signos de apertura no se puede montar ninguna pantalla de texto. **Es el primer asset que debe entregarse** |
| **PJ-02 y PJ-03 — Candil en dos capas** | Si la luz no viene en archivo separado, el indicador verde/amarillo no se puede programar, y es una mecánica central |
| **TS-02 — Tileset del bosque** | El arroyo necesita sus bordes para probar el salto, que es un requerimiento de la rúbrica |

# 8. Anexos

## 8.1 Anexo A — Plantilla de hoja de sprites

Una hoja de animación se organiza así: **una fila por animación**, cuadros de izquierda a derecha, sin espacio entre ellos, sin márgenes y sin texto.

```
Archivo: spr_pj_mercader_correr_sur.png   (768 x 128 px = 6 cuadros de 128 x 128)

+--------+--------+--------+--------+--------+--------+
| cuadro | cuadro | cuadro | cuadro | cuadro | cuadro |
|   1    |   2    |   3    |   4    |   5    |   6    |
+--------+--------+--------+--------+--------+--------+
 64 px    64 px    64 px    64 px    64 px    64 px
```

Dentro de cada cuadro (de 128 px), el personaje se apoya en el **borde inferior**, centrado horizontalmente. Si el personaje "salta" de posición entre cuadros, la animación tiembla en el juego.

## 8.2 Anexo B — Ejemplo resuelto: el Mercader

Para que quede claro qué se espera, este es el desglose completo de PJ-01, el personaje más grande del encargo.

| Archivo | Tamaño | Cuadros | Contenido |
|---|---|---|---|
| `spr_pj_mercader_idle_sur.png` | 256 × 128 | 2 | De frente, respiración sutil |
| `spr_pj_mercader_idle_nor.png` | 256 × 128 | 2 | De espaldas |
| `spr_pj_mercader_idle_lat.png` | 256 × 128 | 2 | De lado, mirando a la derecha |
| `spr_pj_mercader_correr_sur.png` | 768 × 128 | 6 | Ciclo de carrera de frente |
| `spr_pj_mercader_correr_nor.png` | 768 × 128 | 6 | Ciclo de espaldas |
| `spr_pj_mercader_correr_lat.png` | 768 × 128 | 6 | Ciclo de lado |
| `spr_pj_mercader_atacar_sur.png` | 512 × 128 | 4 | Golpe con el farol, de frente |
| `spr_pj_mercader_atacar_nor.png` | 512 × 128 | 4 | De espaldas |
| `spr_pj_mercader_atacar_lat.png` | 512 × 128 | 4 | De lado |
| `spr_pj_mercader_saltar_sur.png` | 640 × 128 | 5 | Salto de frente |
| `spr_pj_mercader_saltar_nor.png` | 640 × 128 | 5 | Salto de espaldas |
| `spr_pj_mercader_saltar_lat.png` | 640 × 128 | 5 | Salto de lado |
| `spr_pj_mercader_desmayo_sur.png` | 768 × 128 | 6 | Cae y se queda en el suelo |
| | | **57** | |

Más el archivo fuente `mercader.piskel` en `_Source/Characters/`.

## 8.3 Anexo C — Qué hace cada asset en el juego

Contexto rápido para entender el encargo. El juego: heredas una tienda en un pueblo medieval. De día recolectas en el bosque, talas robles, cultivas, surtes tu tienda y comercias en la plaza. De noche, ladrones y espíritus atacan la tienda y decides si la defiendes o te duermes.

**La tensión del juego:** el Inquisidor paga un 50 % más por la leña y la cuerda, pero cada venta alimenta a los espíritus que atacan de noche y te obliga a talar más robles, **que no vuelven a crecer solos**. El bosque cambia de aspecto según cuántos quedan en pie. Por eso TS-06, las variantes degradadas del bosque, no es decoración: es el mensaje del juego hecho imagen.

**Candil** es la mascota que te acompaña siempre y cambia de verde a amarillo cuando hay peligro. Sustituye a cualquier medidor en pantalla, así que su legibilidad es crítica.

**Glotglot** es la suma de los espíritus de las acusadas. Cuanto más le vendiste al Inquisidor, más resistente es.

## 8.4 Anexo D — Preguntas frecuentes

| Pregunta | Respuesta |
|---|---|
| ¿Puedo usar un color que no está en la paleta? | No. Si falta un tono que de verdad hace falta, se propone al equipo y se decide si se amplía la paleta para todo el juego |
| ¿Dibujo la vista izquierda? | No. Solo la derecha. El código la voltea |
| ¿Puedo usar degradados? | No, salvo en FX-07 (niebla) y en la capa de luz de Candil |
| ¿Los paneles de cinemática son pixel art? | Sí. Se dibujan a 480 × 270 y se escalan ×4 con vecino más cercano |
| ¿Puedo poner el texto dentro de la imagen de cinemática? | No, salvo en los cuatro paneles de dato, donde la cifra es parte de la composición |
| ¿Qué pasa si un asset no cabe en su tamaño? | Se avisa antes de dibujarlo. Cambiar el tamaño después obliga a rehacer la configuración en Unity |
| ¿Puedo usar assets de bibliotecas gratuitas? | Solo con licencia CC0 o CC-BY, acreditados en los créditos, y solo si encajan con la paleta y la densidad de píxel. Para los personajes principales no: deben ser inéditos |
| ¿Dónde están los textos exactos de los diálogos y cinemáticas? | Documento de Proyecto v2.0, apartados 1.4.3 a 1.4.6 |
| ¿Dónde está la distribución de cada escena? | Documento de Proyecto v2.0, apartados 1.6.1 y 1.6.3 (storyboards) |

## 8.5 Anexo E — Contenido prohibido

El juego está clasificado **B15** en el sistema mexicano y **PEGI 12** en el europeo. Estas restricciones son requerimiento verificable (RNF-14) y ningún asset puede incumplirlas.

| No se dibuja | Qué se hace en su lugar |
|---|---|
| Sangre, heridas o partículas rojas de impacto | Destello blanco corto (FX-04) |
| Cadáveres o cuerpos en el suelo | Los enemigos se desvanecen con partículas (FX-01) |
| Ejecuciones, quemas o personas en la hoguera | La pila de leña aparece siempre **apagada y vacía** (OB-20) |
| Símbolos religiosos reales identificables | Insignias inventadas, geométricas |
| Desnudez o contenido sexual | — |
| Imágenes de apuestas, dados, cartas o ruleta | — |
