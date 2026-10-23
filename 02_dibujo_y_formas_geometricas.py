"""
=============================================================================
02 - Dibujo y Formas Geométricas con el módulo pygame.draw
=============================================================================
Este módulo profundiza en las capacidades de renderizado 2D que ofrece Pygame:
  1. Rectángulos (pygame.draw.rect), esquinas redondeadas y grosor de bordes.
  2. Círculos (pygame.draw.circle) concéntricos y anillos.
  3. Elipses (pygame.draw.ellipse) acotadas por rectángulos.
  4. Líneas simples y continuas (pygame.draw.line, lines, aaline con antialiasing).
  5. Polígonos y estrellas complejas (pygame.draw.polygon).
  6. Arcos de circunferencia (pygame.draw.arc) basados en radianes.

Controles interactivos:
  - [1]: Modo "Galería de Formas Primitivas" (muestra cada función con sus parámetros).
  - [2]: Modo "Paisaje Geométrico Compuesto" (ilustración vectorial animada).
  - [ESPACIO]: Activa o congela la rotación y pulsación de las formas.
  - [+] / [-]: Aumenta o disminuye el grosor de línea de las figuras con borde.
  - [ESC]: Salir del programa.
=============================================================================
"""

import sys
import math
import pygame

def calcular_vertices_estrella(centro_x, centro_y, puntas=5, radio_externo=50, radio_interno=22, angulo_offset=0):
    """Calcula los puntos (x, y) de una estrella de 'puntas' lados con rotación."""
    puntos = []
    paso_angular = math.pi / puntas
    for i in range(puntas * 2):
        radio = radio_externo if (i % 2 == 0) else radio_interno
        angulo = angulo_offset + i * paso_angular - math.pi / 2
        px = centro_x + math.cos(angulo) * radio
        py = centro_y + math.sin(angulo) * radio
        puntos.append((px, py))
    return puntos

def main():
    pygame.init()
    ANCHO, ALTO = 900, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("02 - Dibujo de Primitivas y Formas con pygame.draw")

    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Segoe UI", 22, bold=True)
    fuente_sub = pygame.font.SysFont("Segoe UI", 16, bold=True)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    # Estado interactivo
    modo_actual = 1  # 1 = Galería de primitivas, 2 = Paisaje compuesto
    animado = True
    tiempo = 0.0
    grosor_base = 3

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0
        if animado:
            tiempo += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_1:
                    modo_actual = 1
                elif evento.key == pygame.K_2:
                    modo_actual = 2
                elif evento.key == pygame.K_SPACE:
                    animado = not animado
                elif evento.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    grosor_base = min(grosor_base + 1, 10)
                elif evento.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    grosor_base = max(grosor_base - 1, 1)

        # ---------------------------------------------------------------------
        # RENDERIZADO
        # ---------------------------------------------------------------------
        pantalla.fill((18, 22, 34))

        # Barra superior con selector de modos
        pygame.draw.rect(pantalla, (28, 35, 52), (0, 0, ANCHO, 65))
        pygame.draw.line(pantalla, (55, 70, 105), (0, 65), (ANCHO, 65), 2)

        titulo = "02: Galería de Primitivas Geométricas" if modo_actual == 1 else "02: Composición Artística Vectorial"
        surf_tit = fuente_titulo.render(titulo, True, (245, 245, 255))
        pantalla.blit(surf_tit, (25, 12))

        texto_modos = "[1] Galería Primitivas   [2] Paisaje Compuesto   [ESPACIO] Animar/Pausar   [+/-] Grosor bordes"
        surf_modos = fuente_mono.render(texto_modos, True, (160, 185, 225))
        pantalla.blit(surf_modos, (25, 38))

        if modo_actual == 1:
            # =================================================================
            # MODO 1: GALERÍA DE PRIMITIVAS GEOMÉTRICAS (Cuadrícula 3x2)
            # =================================================================
            cajas = [
                # (col, fila, nombre, funcion)
                (0, 0, "1. pygame.draw.rect"),
                (1, 0, "2. pygame.draw.circle"),
                (2, 0, "3. pygame.draw.ellipse"),
                (0, 1, "4. pygame.draw.polygon"),
                (1, 1, "5. pygame.draw.line / lines"),
                (2, 1, "6. pygame.draw.arc"),
            ]

            margen_x, margen_y = 30, 85
            ancho_tarjeta = (ANCHO - margen_x * 4) // 3
            alto_tarjeta = 230

            for col in range(3):
                for fila in range(2):
                    idx = fila * 3 + col
                    bx = margen_x + col * (ancho_tarjeta + margen_x)
                    by = margen_y + fila * (alto_tarjeta + 18)

                    # Fondo de tarjeta
                    pygame.draw.rect(pantalla, (25, 30, 44), (bx, by, ancho_tarjeta, alto_tarjeta), border_radius=10)
                    pygame.draw.rect(pantalla, (45, 55, 80), (bx, by, ancho_tarjeta, alto_tarjeta), width=1, border_radius=10)

                    # Etiqueta
                    lbl = fuente_sub.render(cajas[idx][2], True, (220, 230, 250))
                    pantalla.blit(lbl, (bx + 12, by + 10))

                    cx = bx + ancho_tarjeta // 2
                    cy = by + alto_tarjeta // 2 + 10

                    # 1. RECTÁNGULOS
                    if idx == 0:
                        # Relleno con bordes redondeados
                        ancho_r = int(100 + math.sin(tiempo * 3) * 15)
                        alto_r = 70
                        rect_fill = pygame.Rect(cx - ancho_r // 2, cy - alto_r // 2, ancho_r, alto_r)
                        pygame.draw.rect(pantalla, (65, 135, 245), rect_fill, border_radius=12)
                        # Rectángulo de borde superpuesto
                        pygame.draw.rect(pantalla, (255, 255, 255), rect_fill, width=grosor_base, border_radius=12)

                    # 2. CÍRCULOS
                    elif idx == 1:
                        # Círculo relleno central
                        pulso = (math.sin(tiempo * 4) + 1.0) / 2.0
                        radio_c = int(35 + pulso * 12)
                        pygame.draw.circle(pantalla, (245, 100, 110), (cx, cy), radio_c)
                        # Anillos concéntricos con grosor configurable
                        pygame.draw.circle(pantalla, (255, 210, 120), (cx, cy), 55, width=grosor_base)
                        pygame.draw.circle(pantalla, (100, 230, 180), (cx, cy), 12)

                    # 3. ELIPSES
                    elif idx == 2:
                        w_elipse = int(130 + math.cos(tiempo * 2) * 20)
                        h_elipse = int(70 + math.sin(tiempo * 2) * 15)
                        rect_elipse = pygame.Rect(cx - w_elipse // 2, cy - h_elipse // 2, w_elipse, h_elipse)
                        # Elipse de fondo
                        pygame.draw.ellipse(pantalla, (140, 75, 230), rect_elipse)
                        # Elipse de contorno
                        pygame.draw.ellipse(pantalla, (255, 255, 150), rect_elipse, width=grosor_base)

                    # 4. POLÍGONOS (ESTRELLA DE 5 PUNTAS)
                    elif idx == 3:
                        ang = tiempo * 1.5
                        puntos_estrella = calcular_vertices_estrella(cx, cy, puntas=5, radio_externo=55, radio_interno=24, angulo_offset=ang)
                        # Relleno del polígono
                        pygame.draw.polygon(pantalla, (255, 185, 30), puntos_estrella)
                        # Contorno
                        pygame.draw.polygon(pantalla, (255, 255, 255), puntos_estrella, width=grosor_base)

                    # 5. LÍNEAS (LINE, LINES, AALINE)
                    elif idx == 4:
                        # Línea con antialiasing
                        ox = math.cos(tiempo * 2) * 50
                        oy = math.sin(tiempo * 2) * 35
                        pygame.draw.aaline(pantalla, (255, 80, 80), (cx - 60, cy - 35), (cx + 60, cy + 35))
                        # Polilínea conectada formando una onda
                        puntos_onda = []
                        for px in range(-55, 56, 12):
                            py = int(math.sin((px + tiempo * 80) * 0.08) * 25)
                            puntos_onda.append((cx + px, cy + py))
                        pygame.draw.lines(pantalla, (80, 220, 255), False, puntos_onda, width=grosor_base)

                    # 6. ARCOS DE CIRCUNFERENCIA
                    elif idx == 5:
                        rect_arco = pygame.Rect(cx - 50, cy - 50, 100, 100)
                        ang_ini = (tiempo * 2) % (math.pi * 2)
                        ang_fin = ang_ini + math.pi * 1.25
                        pygame.draw.arc(pantalla, (255, 105, 180), rect_arco, ang_ini, ang_fin, width=grosor_base + 2)
                        # Círculo guía tenue
                        pygame.draw.ellipse(pantalla, (60, 70, 95), rect_arco, width=1)

            # Pie con parámetros
            pie_texto = f"Parámetros activos: Grosor de bordes = {grosor_base} px | Estado de animación = {'ACTIVA' if animado else 'PAUSADA'}"
            surf_pie = fuente_mono.render(pie_texto, True, (140, 160, 190))
            pantalla.blit(surf_pie, (35, ALTO - 30))

        else:
            # =================================================================
            # MODO 2: PAISAJE GEOMÉTRICO ARTÍSTICO COMPUESTO
            # Demuestra cómo combinar formas para crear arte procedimental
            # =================================================================
            # 1. Cielo crepuscular con franjas degradadas
            franjas = [
                ((15, 20, 45), 0, 140),
                ((30, 28, 65), 140, 120),
                ((65, 35, 75), 260, 100),
                ((120, 50, 75), 360, 100),
            ]
            for col, y_pos, alto_f in franjas:
                pygame.draw.rect(pantalla, col, (0, y_pos + 65, ANCHO, alto_f))

            # 2. Estrellas titilantes en el cielo
            for i in range(25):
                sx = (i * 37 + 15) % ANCHO
                sy = 75 + (i * 23) % 230
                brillo = int(180 + math.sin(tiempo * 5 + i) * 75)
                pygame.draw.circle(pantalla, (brillo, brillo, brillo), (sx, sy), 2)

            # 3. Sol poniente con rayos giratorios
            sol_x, sol_y = ANCHO - 160, 220
            # Rayos del sol con líneas
            num_rayos = 12
            for r in range(num_rayos):
                a = tiempo * 0.5 + (r * 2 * math.pi / num_rayos)
                rx1 = sol_x + math.cos(a) * 55
                ry1 = sol_y + math.sin(a) * 55
                rx2 = sol_x + math.cos(a) * 78
                ry2 = sol_y + math.sin(a) * 78
                pygame.draw.line(pantalla, (255, 215, 90), (rx1, ry1), (rx2, ry2), width=3)
            # Disco solar principal
            pygame.draw.circle(pantalla, (255, 140, 40), (sol_x, sol_y), 45)
            pygame.draw.circle(pantalla, (255, 220, 80), (sol_x, sol_y), 38)

            # 4. Montañas del fondo (Polígonos superpuestos)
            montana_lejana = [(50, 460), (220, 260), (410, 460)]
            pygame.draw.polygon(pantalla, (45, 30, 65), montana_lejana)

            montana_lejana2 = [(300, 460), (510, 240), (740, 460)]
            pygame.draw.polygon(pantalla, (55, 38, 75), montana_lejana2)

            montana_cercana = [(-20, 480), (160, 310), (370, 480)]
            pygame.draw.polygon(pantalla, (35, 45, 60), montana_cercana)

            montana_cercana2 = [(450, 480), (680, 290), (920, 480)]
            pygame.draw.polygon(pantalla, (35, 45, 60), montana_cercana2)

            # 5. Suelo y colina de primer plano
            pygame.draw.rect(pantalla, (25, 55, 40), (0, 470, ANCHO, ALTO - 470))
            # Colina curva usando elipse
            pygame.draw.ellipse(pantalla, (32, 70, 50), (-100, 440, ANCHO + 200, 300))

            # 6. Cabaña acogedora
            casa_x, casa_y = 210, 420
            # Cuerpo de la casa (rectángulo)
            pygame.draw.rect(pantalla, (120, 75, 45), (casa_x, casa_y, 110, 80))
            # Tejado (polígono triangular)
            tejado = [(casa_x - 15, casa_y), (casa_x + 55, casa_y - 45), (casa_x + 125, casa_y)]
            pygame.draw.polygon(pantalla, (160, 50, 45), tejado)
            # Puerta (rectángulo con borde superior redondeado)
            pygame.draw.rect(pantalla, (70, 40, 25), (casa_x + 15, casa_y + 35, 30, 45), border_top_left_radius=6, border_top_right_radius=6)
            # Pomo de la puerta
            pygame.draw.circle(pantalla, (255, 215, 0), (casa_x + 40, casa_y + 60), 3)
            # Ventana iluminada con marco
            pygame.draw.rect(pantalla, (255, 230, 130), (casa_x + 60, casa_y + 20, 35, 35))
            pygame.draw.line(pantalla, (80, 50, 30), (casa_x + 77, casa_y + 20), (casa_x + 77, casa_y + 55), 2)
            pygame.draw.line(pantalla, (80, 50, 30), (casa_x + 60, casa_y + 37), (casa_x + 95, casa_y + 37), 2)

            # 7. Árboles estilizados (Troncos y círculos/triángulos)
            for ax, ay, escala in [(100, 450, 1.0), (370, 470, 0.85), (780, 455, 1.1)]:
                # Tronco
                tw, th = int(14 * escala), int(40 * escala)
                pygame.draw.rect(pantalla, (85, 50, 30), (ax - tw // 2, ay, tw, th))
                # Copa del árbol (círculos concéntricos escalonados)
                r_copa = int(32 * escala)
                pygame.draw.circle(pantalla, (20, 95, 45), (ax, ay - int(12 * escala)), r_copa)
                pygame.draw.circle(pantalla, (25, 120, 55), (ax, ay - int(30 * escala)), int(r_copa * 0.8))

            # Resumen inferior
            info = fuente_mono.render("Composición 100% vectorial creada exclusivamente combinando primitivas de pygame.draw", True, (240, 240, 255))
            pantalla.blit(info, (30, ALTO - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
