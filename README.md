# 🎮 Dominio de Pygame: De Cero a un Videojuego Completo

Repositorio educativo profesional con tutoriales paso a paso y un videojuego arcade espacial completo desarrollado en **Python** utilizando la librería **Pygame** (compatible con `pygame-ce`).

---

## 📋 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Requisitos e Instalación](#-requisitos-e-instalación)
3. [Estructura del Proyecto y Archivos](#-estructura-del-proyecto-y-archivos)
4. [Detalle de Cada Archivo Educativo](#-detalle-de-cada-archivo-educativo)
   - [01 - Ventana y Bucle Principal](#01---01_ventana_y_bucle_principalpy)
   - [02 - Dibujo y Formas Geométricas](#02---02_dibujo_y_formas_geometricaspy)
   - [03 - Manejo de Eventos, Teclado y Ratón](#03---03_manejo_eventos_y_teclado_ratonpy)
   - [04 - Superficies, Canal Alfa y Transformaciones](#04---04_imagenes_superficies_y_transformacionespy)
   - [05 - Detección de Colisiones y Sistema Rect](#05---05_colisiones_y_sistema_rectpy)
   - [06 - Texto, Fuentes y Audio Sintetizado](#06---06_texto_fuentes_y_audio_sintetizadopy)
   - [07 - Arquitectura Orientada a Objetos: Sprite y Groups](#07---07_sprites_y_grupos_arquitecturapy)
5. [Videojuego Completo: Cosmic Defender](#-videojuego-completo-cosmic-defender)
6. [Buenas Prácticas en el Desarrollo con Pygame](#-buenas-prácticas-en-el-desarrollo-con-pygame)
7. [Licencia y Créditos](#-licencia-y-créditos)

---

## 🌟 Descripción General

Este repositorio está diseñado como una guía progresiva y exhaustiva para aprender programación de gráficos 2D y desarrollo de videojuegos con **Pygame**. 

Cada archivo aborda un pilar fundamental de la librería de forma independiente, práctica e interactiva. Todo el proyecto es **100% autónomo y autosuficiente**: los gráficos, naves espaciales, gemas y efectos de sonido se generan de manera algorítmica y procedural en código, por lo que **no depende de archivos de imagen externos (PNG) ni pistas de audio (WAV/MP3)** que puedan extraviarse o causar errores de ruta.

---

## ⚙️ Requisitos e Instalación

### Requisitos Previos
- **Python 3.10 o superior** (probado y compatible hasta Python 3.14).
- Sistema Operativo: Windows, macOS o Linux.

### Instalación Rápida

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/josealbertohescorcia-boop/libreria-juego-pygame.git
   cd libreria-juego-pygame
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   - En Windows:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - En macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   > *Nota:* Se utiliza `pygame-ce` (Pygame Community Edition), la versión moderna, activa y optimizada de Pygame que provee total compatibilidad con las versiones más recientes de Python.

---

## 📂 Estructura del Proyecto y Archivos

| Archivo | Módulo / Tema Principal | Nivel | Descripción Resumida |
| :--- | :--- | :---: | :--- |
| `01_ventana_y_bucle_principal.py` | Fundamentos y Tiempo | Básico | Creación de ventana, Game Loop, control de FPS y delta time. |
| `02_dibujo_y_formas_geometricas.py` | Gráficos 2D Vectoriales | Básico | Uso de `pygame.draw` (rect, circle, polygon, arc, lines) y paisaje vectorial. |
| `03_manejo_eventos_y_teclado_raton.py` | Entradas de Usuario | Intermedio | Eventos discretos vs muestreo continuo, apuntado con ratón y telemetría. |
| `04_imagenes_superficies_y_transformaciones.py` | Superficies y Render | Intermedio | Canal alfa, transparencias `SRCALPHA`, rotación centrada, escala y volteo. |
| `05_colisiones_y_sistema_rect.py` | Física Espacial | Intermedio | Métodos de `pygame.Rect` (`colliderect`, `collidepoint`, colisión circular y clamp). |
| `06_texto_fuentes_y_audio_sintetizado.py` | Audio y Tipografía | Avanzado | `pygame.font`, sombras/neón, y síntesis de audio retro en RAM con `pygame.mixer`. |
| `07_sprites_y_grupos_arquitectura.py` | Arquitectura POO | Avanzado | Clases `Sprite`, contenedores `Group`/`GroupSingle`, ciclo `kill()` y `groupcollide()`. |
| `08_videojuego_space_defender.py` | **Videojuego Completo** | Master | **Cosmic Defender**: Arcade espacial con estados, oleadas, power-ups y sonido retro. |

---

## 📖 Detalle de Cada Archivo Educativo

---

### 01 - `01_ventana_y_bucle_principal.py`
**Objetivo de Aprendizaje:** Comprender la anatomía básica e indispensable de cualquier aplicación gráfica con Pygame.

#### Conceptos Clave Explicados:
- **`pygame.init()` y `pygame.quit()`:** Inicialización y limpieza formal de los subsistemas.
- **`pygame.display.set_mode((ANCHO, ALTO))`:** Creación de la superficie principal (ventana de visualización).
- **El Bucle de Juego (Game Loop):** Ciclo continuo en 3 etapas:
  1. *Fase de Eventos*: Leer entradas del sistema operativo (`pygame.event.get()`).
  2. *Fase de Actualización (Update)*: Aplicar reglas del juego, física y temporizadores.
  3. *Fase de Renderizado (Draw)*: Limpiar con `fill()`, dibujar elementos y refrescar con `pygame.display.flip()`.
- **Control de Fotogramas y `delta_time`:** Uso de `pygame.time.Clock()` para fijar tasas estables de fotogramas (ej. 60 FPS) y calcular el paso exacto del tiempo en segundos para garantizar que el movimiento sea independiente del hardware del usuario.

#### Controles Interactivos:
- `[ESPACIO]`: Alternar entre 4 paletas cromáticas de fondo.
- `[FLECHA ARRIBA] / [FLECHA ABAJO]`: Aumentar o reducir el límite de FPS en tiempo real (15 a 240 FPS).
- `[P]`: Pausar / reanudar la animación del orbe orbital.
- `[ESC]`: Cerrar la aplicación.

```bash
python 01_ventana_y_bucle_principal.py
```

---

### 02 - `02_dibujo_y_formas_geometricas.py`
**Objetivo de Aprendizaje:** Dominar el módulo `pygame.draw` para renderizar gráficos vectoriales 2D nativos sin necesidad de cargar imágenes externas.

#### Conceptos Clave Explicados:
- **Rectángulos (`pygame.draw.rect`):** Relleno, contornos, y esquinas redondeadas con `border_radius`.
- **Círculos y Elipses (`circle`, `ellipse`):** Centros, radios, bounding boxes y anillos concéntricos.
- **Polígonos y Estrellas (`polygon`):** Renderizado de figuras complejas a partir de listas de vértices calculados matemáticamente con funciones trigonométricas (`cos` y `sin`).
- **Líneas y Polilíneas (`line`, `lines`, `aaline`):** Trazado de segmentos continuos y líneas suavizadas con antialiasing.
- **Arcos (`arc`):** Curvas delimitadas por ángulos en radianes.

#### Dos Modos de Visualización:
1. **Galería de Primitivas:** Una cuadrícula explicativa con cada figura aislada y sus parámetros en pantalla.
2. **Paisaje Vectorial Artístico:** Una composición escénica completa (cielo degradado, estrellas titilantes, sol con rayos rotatorios, cordillera montañosa, árboles y una cabaña con ventanas iluminadas).

#### Controles Interactivos:
- `[1]`: Modo Galería de Primitivas.
- `[2]`: Modo Paisaje Artístico Compuesto.
- `[ESPACIO]`: Pausar / activar animaciones geométricas.
- `[+] / [-]`: Modificar dinámicamente el grosor de las líneas y contornos.
- `[ESC]`: Salir.

```bash
python 02_dibujo_y_formas_geometricas.py
```

---

### 03 - `03_manejo_eventos_y_teclado_raton.py`
**Objetivo de Aprendizaje:** Comprender la diferencia fundamental entre la gestión de eventos discretos y el sondeo continuo (polling) de estados del teclado y ratón.

#### Conceptos Clave Explicados:
- **Eventos Discretos (`pygame.event.get()`):** Ideal para disparadores únicos (pulsar una sola vez para abrir un menú, presionar escape para pausar, clics instantáneos).
- **Muestreo Continuo (`pygame.key.get_pressed()`):** Esencial para traslaciones suaves de personajes, cálculo de aceleración, inercia y fricción física.
- **Interacción con el Ratón:** Obtención de coordenadas (`pygame.mouse.get_pos()`), eventos de botones (`MOUSEBUTTONDOWN`/`UP`), cálculo del ángulo de apuntado mediante `math.atan2()`, y captura de la rueda de desplazamiento (`MOUSEWHEEL`).
- **Inspector de Telemetría en Vivo:** Un panel lateral con registro FIFO en tiempo real que imprime cada evento capturado por Pygame.

#### Controles Interactivos:
- `[W, A, S, D]` o `[FLECHAS]`: Mover al avatar con aceleración física e inercia.
- `[SHIFT]`: Activar modo Turbo (impulso de aceleración).
- `[RATÓN]`: Orientar el cañón del avatar hacia la posición del puntero.
- `[CLIC IZQUIERDO]`: Disparar orbes de energía dirigidos.
- `[CLIC DERECHO]`: Emitir ondas de choque expansivas en el punto del clic.
- `[RUEDA RATÓN]`: Modificar dinámicamente el tamaño/escala del avatar.
- `[C]`: Limpiar proyectiles y ondas en pantalla.

```bash
python 03_manejo_eventos_y_teclado_raton.py
```

---

### 04 - `04_imagenes_superficies_y_transformaciones.py`
**Objetivo de Aprendizaje:** Dominar el objeto primordial de Pygame: la clase `pygame.Surface`, el manejo de canales de transparencia (Alpha) y el módulo `pygame.transform`.

#### Conceptos Clave Explicados:
- **Superficies con Canal Alfa (`pygame.SRCALPHA`):** Creación de gráficos transparentes con translucidez por píxel y efectos de resplandor neón (bloom).
- **Opacidad Global (`surface.set_alpha(0-255)`):** Regulación del nivel de desvanecimiento general de un sprite.
- **Rotación Centrada Perfecta:** Cómo rotar superficies usando `pygame.transform.rotate()` recalculando el rectángulo resultante (`new_rect = new_surf.get_rect(center=old_rect.center)`) para eliminar el temblor o desvío de pivote.
- **Escalado Rápido vs Suave:** Diferencia visual y de rendimiento entre `scale()` y `smoothscale()`.
- **Inversión de Ejes (`pygame.transform.flip`):** Volteo horizontal y vertical.

#### Galería de Sprites Procedimentales:
Incluye 4 generadores de sprites creados 100% en código:
1. *Nave Estelar Vectorial* (con alerones, toberas y cabina luminosa).
2. *Gema Esmeralda Facetada* (con caras poligonales sombreadas e iluminación especular).
3. *Moneda Dorada Mágica* (con bordes en relieve y estrella grabada).
4. *Orbe Neón con Resplandor* (gradiente esférico translúcido de canal alfa).

#### Controles Interactivos:
- `[1, 2, 3, 4]`: Cambiar el sprite activo seleccionado.
- `[ESPACIO]`: Activar / pausar la rotación continua automática.
- `[Q / E]`: Rotar manualmente en sentido horario / antihorario.
- `[W / S]`: Aumentar o reducir el factor de escala (zoom).
- `[A / D]`: Aumentar o disminuir la opacidad alfa del sprite.
- `[H] / [V]`: Invertir horizontalmente (Flip X) o verticalmente (Flip Y).
- `[R]`: Restablecer todos los valores de transformación.

```bash
python 04_imagenes_superficies_y_transformaciones.py
```

---

### 05 - `05_colisiones_y_sistema_rect.py`
**Objetivo de Aprendizaje:** Comprender la geometría espacial en 2D a través de `pygame.Rect` y los diferentes métodos de detección y respuesta a colisiones.

#### Conceptos Clave Explicados:
- **Puntos de Anclaje de `pygame.Rect`:** Propiedades útiles como `center`, `topleft`, `bottomright`, `midtop`, etc.
- **Colisión Caja-Caja AABB (`rect.colliderect`):** Algoritmo ultrarrápido para rectángulos alineados a los ejes.
- **Colisión Punto-Caja (`rect.collidepoint`):** Base fundamental para implementar botones, paneles interactivos e interfaces gráficas (UI).
- **Colisión Circular Radial:** Uso de la distancia euclidiana (`math.hypot`) contra radio conjunto para esferas y orbes.
- **Confinamiento de Pantalla (`rect.clamp_ip`):** Restringir automáticamente un objeto para que nunca escape del marco delimitador.
- **Búsqueda en Listas (`rect.collidelist`):** Detección eficiente contra múltiples obstáculos en un solo paso.

#### Controles Interactivos:
- `[RATÓN (Arrastre)]` o `[WASD / Flechas]`: Mover y arrastrar el bloque del jugador.
- `[ESPACIO]`: Crear una nueva caja obstáculo en posición aleatoria.
- `[B]`: Pausar / reanudar las esferas móviles rebotadoras con física elástica.
- `[C]`: Limpiar todos los obstáculos adicionales.
- Botones de interfaz interactivos en pantalla con estados Normal, Hover y Clic.

```bash
python 05_colisiones_y_sistema_rect.py
```

---

### 06 - `06_texto_fuentes_y_audio_sintetizado.py`
**Objetivo de Aprendizaje:** Implementar tipografía avanzada con `pygame.font` y sintetizar efectos de sonido de audio arcade procedurales directamente en la memoria RAM con `pygame.mixer`.

#### Conceptos Clave Explicados:
- **Renderizado Tipográfico Avanzado:**
  - Creación de textos con **sombra paralela profunda** (Drop Shadow).
  - Creación de textos con **contorno neón perimetral** (Outline en 8 direcciones).
  - Animación de **pulso y escala oscilante** con funciones senoidales.
- **Síntesis de Audio Chiptune Procedimental:**
  - Sin necesidad de cargar archivos externos, el código calcula muestras PCM de audio de 16 bits en buffers en memoria utilizando la librería estándar `struct` y fórmulas matemáticas.
  - Generador de *Láser* (barrido descendente de frecuencia).
  - Generador de *Salto* (barrido ascendente tipo plataforma).
  - Generador de *Moneda / Power-up* (arpegio armónico brillante en dos notas).
  - Generador de *Gran Explosión* (ruido blanco estocástico con caída exponencial).
  - Generador de *Alarma / Daño* (modulación FM periódica).
- **Ecualizador Espectral Reactivo:**
  - Visualizador gráfico animado de barras de frecuencias que reacciona a los eventos sonoros en tiempo real.

#### Controles Interactivos:
- `[1]`: Disparar sonido de Láser.
- `[2]`: Disparar sonido de Salto Arcade.
- `[3]`: Disparar sonido de Moneda / Power-Up.
- `[4]`: Disparar sonido de Explosión.
- `[5]`: Disparar sonido de Alarma de Impacto.
- `[TAB]`: Alternar el estilo tipográfico del letrero central (Sombra / Contorno Neón / Pulso).
- `[+] / [-]`: Modificar el volumen maestro de salida.

```bash
python 06_texto_fuentes_y_audio_sintetizado.py
```

---

### 07 - `07_sprites_y_grupos_arquitectura.py`
**Objetivo de Aprendizaje:** Adoptar la arquitectura profesional estándar orientada a objetos de Pygame mediante `pygame.sprite.Sprite` y contenedores `Group`.

#### Conceptos Clave Explicados:
- **El Contrato `pygame.sprite.Sprite`:**
  - Cada subclase debe inicializarse con `super().__init__()` y exponer obligatoriamente `self.image` (superficie) y `self.rect` (rectángulo delimitador).
  - Encapsulación de toda la lógica de movimiento, animación y temporizadores dentro del método `update(dt)`.
- **El Método `self.kill()`:**
  - Desvincula instantáneamente el sprite de todos los grupos a los que pertenece. Permite la recolección automática de basura sin dejar referencias huérfanas ni causar fugas de memoria (memory leaks).
- **Contenedores de Sprites:**
  - `pygame.sprite.Group`: Colección eficiente que ejecuta `update()` y `draw()` en una sola llamada por lotes.
  - `pygame.sprite.GroupSingle`: Contenedor especializado de 1 sola entidad para el jugador principal.
- **Colisiones Masivas Declarativas (`pygame.sprite.groupcollide`):**
  - Chequea colisiones entre dos grupos completos (ej. Proyectiles vs Drones Enemigos) en una sola operación optimizada con eliminación automática configurable (`dokillA`, `dokillB`).

#### Demostración Interactiva:
- Nave defensora que dispara ráfagas dobles contra drones enemigos con oscilación matemática.
- Sistema de partículas que nacen de las explosiones y mueren de forma autónoma con su propio ciclo de vida.
- Panel lateral con conteo exacto de instancias vivas de cada grupo en la memoria RAM.

#### Controles Interactivos:
- `[RATÓN]`: Desplazar la nave sobre el eje horizontal.
- `[ESPACIO]` o `[CLIC IZQUIERDO]`: Disparo láser manual.
- `[E]`: Alternar modo de disparo continuo automático.
- `[G]`: Generar manualmente una nueva oleada de drones.
- `[ESC]`: Salir.

```bash
python 07_sprites_y_grupos_arquitectura.py
```

---

## 🚀 Videojuego Completo: Cosmic Defender

**Archivo:** `08_videojuego_space_defender.py`

Un videojuego arcade espacial retro terminado, rejugable y pulido que reúne todos los conceptos de los módulos anteriores en una experiencia de juego completa.

```
       ▲  [Nave Defensora]
      /█\ 
     /███\        ⚡ [Power-up Triple]
    /__▲__\             💥 [Explosión de Asteroides]
      ▼ ▼
  ══════════════════════════════════════════════════════
  CASCO: 100%  |  OLEADA: 3  |  SCORE: 014,850 PUNTOS
```

### Características Principales del Videojuego:

1. **Máquina de Estados de Juego:**
   - **Menú Principal (`ESTADO_MENU`):** Portada arcade con títulos neón, mejores puntuaciones de la sesión e instrucciones.
   - **Modo Combate (`ESTADO_JUGANDO`):** Acción espacial continua a 60 FPS.
   - **Pausa Táctica (`ESTADO_PAUSA`):** Cortina translúcida para pausar y reanudar con `[P]` o `[ESC]`.
   - **Pantalla de Fin de Juego (`ESTADO_GAMEOVER`):** Resumen detallado con puntuación final, récord, oleada alcanzada y enemigos eliminados, con reinicio instantáneo con `[R]` o `[ESPACIO]`.

2. **Fondo Parallax Multicapa:**
   - 3 capas independientes de estrellas a diferentes profundidades, densidades y velocidades que generan una sensación inmersiva de movimiento a través del cosmos en 3D.

3. **Física del Jugador:**
   - Nave espacial con respuesta suave de aceleración e inercia gobernada por ecuaciones de fricción física.
   - Sistema de propulsión con estela de partículas de plasma y fuego.
   - Parpadeo de invulnerabilidad temporal tras recibir impactos.

4. **Variedad de Enemigos con Comportamientos Únicos:**
   - **Drones Exploradores:** Rápidos, descienden trazando trayectorias sinusoidales en zigzag.
   - **Cruceros Pesados:** Mayor resistencia, calculan el ángulo vectorial hacia la nave del jugador y le disparan proyectiles de plasma dirigidos.
   - **Asteroides Espaciales:** Rocas con rotación sobre su propio eje. Al ser destruidas por los disparos, **se fracturan en dos asteroides más pequeños**, demandando puntería adicional.

5. **Sistema de Power-ups Coleccionables:**
   - ⚡ **Triple Blaster:** Convierte los cañones dobles en una ráfaga triple en abanico durante 10 segundos.
   - 🛡️ **Escudo de Fuerza:** Genera una cúpula de energía que absorbe el 100% del daño durante 8 segundos.
   - 💚 **Kit de Reparación:** Repara de emergencia 35 puntos de salud del casco de la nave.
   - 💣 **Bomba Nova:** Detona una onda expansiva en toda la pantalla destruyendo inmediatamente a todos los enemigos y asteroides visibles.

6. **Audio Retro Procedural Chiptune en Memoria:**
   - Todos los efectos sonoros (disparos láser, impactos de daño, recolección de premios, detonaciones y bombas) son sintetizados en tiempo de ejecución en RAM, sin fallos de códecs ni dependencias de ficheros externos.

7. **Progresión de Dificultad Dinámica por Oleadas:**
   - Al derrotar a los enemigos de una oleada, se incrementa la cantidad de agresores, su velocidad y su frecuencia de aparición, premiando al jugador con una bonificación de reparación de casco entre oleadas.

### Controles de Cosmic Defender:
| Tecla / Acción | Función |
| :--- | :--- |
| `[W, A, S, D]` / `[Flechas]` | Mover la nave espacial en todas direcciones |
| `[ESPACIO]` / `[Clic Izquierdo]` | Disparar láseres de plasma (mantén presionado para ráfaga continua) |
| `[P]` / `[ESC]` | Pausar / Reanudar la partida |
| `[R]` / `[ESPACIO]` | Reiniciar partida inmediatamente en Game Over |
| `[M]` | Regresar al Menú Principal |

Para iniciar el videojuego:
```bash
python 08_videojuego_space_defender.py
```

---

## 💡 Buenas Prácticas en el Desarrollo con Pygame

Al estudiar este repositorio encontrarás aplicadas las mejores prácticas recomendadas por la comunidad de desarrolladores de videojuegos en Python:

1. **Uso riguroso de `delta_time`:**  
   Nunca sumes cantidades fijas de píxeles a las coordenadas; multiplica siempre las velocidades por `dt` (`pos += vel * dt`). Esto asegura que la velocidad sea idéntica a 30, 60 o 144 FPS.
2. **Separación de Lógica y Render:**  
   Procesa primero las entradas (`pygame.event.get()`), luego actualiza el estado del mundo y finalmente dibuja los elementos. Nunca mezcles lógica de colisión dentro de la fase de renderizado.
3. **Manejo de Transparencias:**  
   Usa superficies dedicadas con `pygame.SRCALPHA` cuando necesites transparencias por píxel, y evita recrear superficies en cada fotograma dentro del bucle principal para mantener un rendimiento óptimo.
4. **Ciclo de Vida de Sprites (`kill()`):**  
   Siempre invoca `sprite.kill()` en entidades que salen de pantalla o son destruidas para que Pygame libere la memoria de inmediato.
5. **Robustez de Audio:**  
   Envuelve siempre la inicialización de `pygame.mixer` en bloques `try/except` para que tu juego funcione perfectamente incluso en sistemas headless, contenedores o equipos sin dispositivo de audio activo.

---

## 📄 Licencia y Créditos

Este proyecto se distribuye bajo la licencia **MIT**, lo que significa que tienes total libertad para utilizarlo, modificarlo, redistribuirlo y emplearlo como base para tus propios videojuegos comerciales o proyectos educativos.

Desarrollado con dedicación para dominar la programación de videojuegos en Python con **Pygame**. ¡Que disfrutes la aventura espacial! 🚀
