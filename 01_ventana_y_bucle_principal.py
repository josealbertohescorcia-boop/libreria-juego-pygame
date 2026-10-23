"""
=============================================================================
01 - Ventana, Bucle Principal (Game Loop) y Control de Tiempo en Pygame
=============================================================================
Este módulo introduce los fundamentos esenciales para cualquier aplicación
o videojuego en Pygame:
  1. Inicialización de la librería (pygame.init()).
  2. Creación y configuración de la ventana (pygame.display.set_mode).
  3. El Bucle Principal del Juego (Game Loop): Procesar Eventos -> Actualizar -> Dibujar.
  4. Control de fotogramas por segundo (FPS) con pygame.time.Clock.
  5. Cálculo del tiempo delta (delta_time) para movimientos independientes de la tasa de refresco.
  6. Finalización limpia del entorno (pygame.quit()).

Controles interactivos:
  - [ESPACIO]: Cambia la paleta de colores de fondo.
  - [FLECHA ARRIBA] / [FLECHA ABAJO]: Aumenta o disminuye el límite de FPS.
  - [P]: Pausar / reanudar la animación del reloj de delta time.
  - [ESC] o cerrar ventana: Salir del programa de forma segura.
=============================================================================
"""

import sys
import math
import pygame

def main():
    # -------------------------------------------------------------------------
    # 1. Inicialización de Pygame
    # -------------------------------------------------------------------------
    # pygame.init() inicializa todos los submódulos integrados (video, audio, etc.)
    pygame.init()

    # Dimensiones de la ventana
    ANCHO = 800
    ALTO = 600

    # pygame.display.set_mode crea la superficie principal sobre la que se dibuja
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("01 - Fundamentos de Pygame: Ventana y Game Loop")

    # -------------------------------------------------------------------------
    # 2. Reloj y control de tiempo
    # -------------------------------------------------------------------------
    # pygame.time.Clock ayuda a mantener una tasa de fotogramas constante y
    # calcular el tiempo transcurrido entre fotogramas sucesivos.
    reloj = pygame.time.Clock()
    fps_objetivo = 60
    pausado = False

    # Fuentes para mostrar información en pantalla
    fuente_titulo = pygame.font.SysFont("Segoe UI", 26, bold=True)
    fuente_texto = pygame.font.SysFont("Segoe UI", 18)
    fuente_mono = pygame.font.SysFont("Consolas", 16)

    # Paletas de color de fondo alternables
    paletas = [
        {"nombre": "Azul Profundo", "color": (15, 23, 42)},
        {"nombre": "Verde Bosque",   "color": (10, 40, 30)},
        {"nombre": "Púrpura Neón",   "color": (35, 10, 45)},
        {"nombre": "Gris Carbón",    "color": (28, 30, 38)},
    ]
    indice_paleta = 0

    # Variables de animación para demostrar delta_time
    angulo_giro = 0.0          # En radianes
    velocidad_angular = 2.0    # Radianes por segundo

    # -------------------------------------------------------------------------
    # 3. Bucle Principal (Game Loop)
    # -------------------------------------------------------------------------
    ejecutando = True
    while ejecutando:
        # clock.tick(fps) pausa el bucle para no superar el límite de FPS y
        # devuelve los milisegundos transcurridos desde el último fotograma.
        dt_ms = reloj.tick(fps_objetivo)
        # Convertimos milisegundos a segundos para usar física o animaciones basadas en tiempo
        delta_time = dt_ms / 1000.0

        # --- A. Fase de Procesamiento de Eventos ---
        for evento in pygame.event.get():
            # Evento para cerrar la ventana (clic en la X superior)
            if evento.type == pygame.QUIT:
                ejecutando = False

            # Eventos de pulsación de teclado
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    # Cambiar paleta de fondo cíclicamente
                    indice_paleta = (indice_paleta + 1) % len(paletas)
                elif evento.key == pygame.K_UP:
                    fps_objetivo = min(fps_objetivo + 15, 240)
                elif evento.key == pygame.K_DOWN:
                    fps_objetivo = max(fps_objetivo - 15, 15)
                elif evento.key == pygame.K_p:
                    pausado = not pausado

        # --- B. Fase de Actualización de Estado (Lógica) ---
        if not pausado:
            # Multiplicar por delta_time garantiza que la velocidad sea idéntica
            # sin importar si el juego corre a 30, 60 o 144 FPS.
            angulo_giro += velocidad_angular * delta_time

        # --- C. Fase de Dibujado (Render) ---
        # 1. Limpiar pantalla rellenándola con el color de fondo elegido
        color_fondo = paletas[indice_paleta]["color"]
        pantalla.fill(color_fondo)

        # 2. Dibujar panel superior con título
        pygame.draw.rect(pantalla, (255, 255, 255, 20), (30, 20, ANCHO - 60, 60), border_radius=8)
        texto_titulo = fuente_titulo.render("Fundamentos de Pygame: Bucle y Control de FPS", True, (240, 240, 255))
        pantalla.blit(texto_titulo, (45, 32))

        # 3. Demostración gráfica: Orbe orbital gobernado por delta_time
        centro_x, centro_y = ANCHO // 2, ALTO // 2 + 30
        radio_orbita = 120

        # Dibujar órbita guía (círculo tenue)
        pygame.draw.circle(pantalla, (80, 100, 130), (centro_x, centro_y), radio_orbita, width=2)
        # Dibujar núcleo central
        pygame.draw.circle(pantalla, (255, 200, 80), (centro_x, centro_y), 24)
        pygame.draw.circle(pantalla, (255, 255, 255), (centro_x, centro_y), 12)

        # Calcular posición del satélite orbital
        satelite_x = int(centro_x + math.cos(angulo_giro) * radio_orbita)
        satelite_y = int(centro_y + math.sin(angulo_giro) * radio_orbita)

        # Dibujar línea conectora y satélite
        pygame.draw.line(pantalla, (100, 180, 255), (centro_x, centro_y), (satelite_x, satelite_y), 2)
        pygame.draw.circle(pantalla, (60, 220, 255), (satelite_x, satelite_y), 16)
        pygame.draw.circle(pantalla, (255, 255, 255), (satelite_x, satelite_y), 6)

        # 4. Mostrar panel de métricas de rendimiento y controles
        fps_reales = reloj.get_fps()
        metricas = [
            f"FPS Actuales:      {fps_reales:6.1f}",
            f"FPS Objetivo:      {fps_objetivo} FPS",
            f"Delta Time:        {delta_time * 1000:6.2f} ms ({delta_time:.4f} s)",
            f"Paleta de Fondo:   {paletas[indice_paleta]['nombre']}",
            f"Estado:            {'PAUSADO' if pausado else 'EN EJECUCIÓN'}",
        ]

        # Caja de telemetría (esquina superior izquierda)
        pygame.draw.rect(pantalla, (20, 25, 35), (40, 100, 320, 145), border_radius=8)
        pygame.draw.rect(pantalla, (60, 120, 200), (40, 100, 320, 145), width=2, border_radius=8)

        for i, linea in enumerate(metricas):
            color = (120, 255, 180) if i == 0 else (220, 225, 235)
            surf_linea = fuente_mono.render(linea, True, color)
            pantalla.blit(surf_linea, (55, 115 + i * 24))

        # Caja de instrucciones y controles (esquina inferior)
        instrucciones = [
            "[ESPACIO] Cambiar paleta de color de fondo",
            "[ARRIBA / ABAJO] Subir o bajar el límite de FPS",
            "[P] Pausar / reanudar el satélite orbital",
            "[ESC] Salir de la aplicación",
        ]
        pygame.draw.rect(pantalla, (20, 25, 35), (40, ALTO - 130, ANCHO - 80, 105), border_radius=8)
        pygame.draw.rect(pantalla, (100, 110, 130), (40, ALTO - 130, ANCHO - 80, 105), width=1, border_radius=8)

        titulo_instr = fuente_texto.render("Controles Interactivos Disponibles:", True, (255, 215, 0))
        pantalla.blit(titulo_instr, (55, ALTO - 125))

        for i, texto in enumerate(instrucciones):
            surf_instr = fuente_mono.render(texto, True, (200, 210, 220))
            pantalla.blit(surf_instr, (55, ALTO - 100 + i * 20))

        # 5. Actualizar la pantalla completa (doble búfer)
        # pygame.display.flip() vuelca todo lo dibujado en la memoria gráfica a la pantalla visible
        pygame.display.flip()

    # -------------------------------------------------------------------------
    # 4. Finalización limpia
    # -------------------------------------------------------------------------
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
