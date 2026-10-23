"""
=============================================================================
05 - Detección de Colisiones y la Clase pygame.Rect
=============================================================================
El corazón de la lógica espacial y física en Pygame es la clase `pygame.Rect`.
Este módulo cubre:
  1. Atributos de posicionamiento de Rect (center, topleft, midbottom, etc.).
  2. Colisión AABB entre rectángulos (rect.colliderect).
  3. Detección de punto dentro de rectángulo (rect.collidepoint) para botones e interfaces.
  4. Colisión circular mediante distancia euclidiana (math.hypot).
  5. Resolución de colisiones y rebotes en paredes con rect.clamp e inversión de velocidad.
  6. Uso de rect.collidelist para verificar múltiples obstáculos de manera eficiente.

Controles interactivos:
  - [RATÓN (Arrastre)]: Haz clic y arrastra el Bloque Jugador o pulsa [WASD / Flechas].
  - [ESPACIO]: Generar un nuevo obstáculo en una posición aleatoria.
  - [B]: Alternar movimiento de las esferas rebotadoras automáticas.
  - [C]: Limpiar obstáculos adicionales.
  - [ESC]: Salir.
=============================================================================
"""

import sys
import math
import random
import pygame

class BotonUI:
    """Implementación de un botón interactivo usando rect.collidepoint."""
    def __init__(self, rect, texto, color_base=(45, 60, 90), color_hover=(70, 100, 150), color_click=(100, 180, 255)):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_click = color_click
        self.hover = False
        self.presionado = False

    def actualizar(self, pos_raton, clic_presionado):
        self.hover = self.rect.collidepoint(pos_raton)
        self.presionado = self.hover and clic_presionado

    def dibujar(self, pantalla, fuente):
        color = self.color_click if self.presionado else (self.color_hover if self.hover else self.color_base)
        pygame.draw.rect(pantalla, color, self.rect, border_radius=8)
        borde_color = (130, 190, 255) if self.hover else (70, 90, 130)
        pygame.draw.rect(pantalla, borde_color, self.rect, width=2, border_radius=8)

        surf_txt = fuente.render(self.texto, True, (255, 255, 255))
        r_txt = surf_txt.get_rect(center=self.rect.center)
        pantalla.blit(surf_txt, r_txt)

def main():
    pygame.init()
    ANCHO, ALTO = 940, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("05 - Detección de Colisiones y Sistema Rect")

    reloj = pygame.time.Clock()
    fuente_tit = pygame.font.SysFont("Segoe UI", 20, bold=True)
    fuente_sub = pygame.font.SysFont("Segoe UI", 15, bold=True)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    # Bloque principal manipulable por el usuario
    jugador_w, jugador_h = 90, 90
    rect_jugador = pygame.Rect(180, 250, jugador_w, jugador_h)
    arrastrando = False
    offset_x, offset_y = 0, 0

    # Obstáculos rectangulares fijos
    obstaculos = [
        pygame.Rect(380, 120, 110, 80),
        pygame.Rect(530, 260, 90, 120),
        pygame.Rect(360, 410, 130, 70),
    ]

    # Círculo interactivo (detección radial)
    circulo_pos = [200, 460]
    circulo_radio = 55

    # Esferas rebotadoras dinámicas
    bolas_activas = True
    bolas = [
        {"x": 100.0, "y": 140.0, "vx": 180.0, "vy": 140.0, "r": 20, "col": (255, 140, 60)},
        {"x": 600.0, "y": 120.0, "vx": -160.0, "vy": 190.0, "r": 25, "col": (230, 80, 140)},
    ]

    # Botones de UI usando collidepoint
    boton_limpiar = BotonUI((680, 480, 230, 40), "Limpiar Obstáculos (C)")
    boton_agregar = BotonUI((680, 530, 230, 40), "+ Añadir Obstáculo (Espacio)")

    limite_area = pygame.Rect(20, 70, 640, ALTO - 90)

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0
        pos_raton = pygame.mouse.get_pos()
        clic_izq = pygame.mouse.get_pressed()[0]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    # Crear obstáculo aleatorio
                    rx = random.randint(limite_area.left + 20, limite_area.right - 100)
                    ry = random.randint(limite_area.top + 20, limite_area.bottom - 80)
                    obstaculos.append(pygame.Rect(rx, ry, random.randint(50, 100), random.randint(50, 90)))
                elif evento.key == pygame.K_b:
                    bolas_activas = not bolas_activas
                elif evento.key == pygame.K_c:
                    obstaculos.clear()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Comprobar si se hizo clic en el bloque del jugador para arrastrar
                    if rect_jugador.collidepoint(evento.pos):
                        arrastrando = True
                        offset_x = rect_jugador.x - evento.pos[0]
                        offset_y = rect_jugador.y - evento.pos[1]
                    # Comprobar clics en botones UI
                    if boton_limpiar.rect.collidepoint(evento.pos):
                        obstaculos.clear()
                    elif boton_agregar.rect.collidepoint(evento.pos):
                        rx = random.randint(limite_area.left + 20, limite_area.right - 100)
                        ry = random.randint(limite_area.top + 20, limite_area.bottom - 80)
                        obstaculos.append(pygame.Rect(rx, ry, random.randint(50, 100), random.randint(50, 90)))

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastrando = False

        # Actualizar botones UI
        boton_limpiar.actualizar(pos_raton, clic_izq)
        boton_agregar.actualizar(pos_raton, clic_izq)

        # Mover bloque del jugador con arrastre de ratón o teclado
        if arrastrando:
            rect_jugador.x = pos_raton[0] + offset_x
            rect_jugador.y = pos_raton[1] + offset_y
        else:
            # Control por teclado si no se arrastra
            teclas = pygame.key.get_pressed()
            vel_k = 300 * dt
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                rect_jugador.x -= vel_k
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                rect_jugador.x += vel_k
            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                rect_jugador.y -= vel_k
            if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                rect_jugador.y += vel_k

        # Confinar al jugador dentro del área de simulación (rect.clamp)
        rect_jugador.clamp_ip(limite_area)

        # Movimiento y rebote de las esferas dinámicas
        if bolas_activas:
            for b in bolas:
                b["x"] += b["vx"] * dt
                b["y"] += b["vy"] * dt

                # Rebote en límites del área de juego
                if b["x"] - b["r"] <= limite_area.left:
                    b["x"] = limite_area.left + b["r"]
                    b["vx"] *= -1
                elif b["x"] + b["r"] >= limite_area.right:
                    b["x"] = limite_area.right - b["r"]
                    b["vx"] *= -1

                if b["y"] - b["r"] <= limite_area.top:
                    b["y"] = limite_area.top + b["r"]
                    b["vy"] *= -1
                elif b["y"] + b["r"] >= limite_area.bottom:
                    b["y"] = limite_area.bottom - b["r"]
                    b["vy"] *= -1

        # =====================================================================
        # DETECCIÓN DE COLISIONES
        # =====================================================================
        # 1. Colisión de rectángulos: rect.collidelist(obstaculos)
        indice_colision = rect_jugador.collidelist(obstaculos)
        hay_colision_rect = (indice_colision != -1)

        # 2. Colisión circular con el orbe fijo: distancia euclidiana contra rect
        # Punto más cercano del rectángulo al centro del círculo
        mas_cercano_x = max(rect_jugador.left, min(circulo_pos[0], rect_jugador.right))
        mas_cercano_y = max(rect_jugador.top, min(circulo_pos[1], rect_jugador.bottom))
        distancia_al_circulo = math.hypot(circulo_pos[0] - mas_cercano_x, circulo_pos[1] - mas_cercano_y)
        hay_colision_circulo = (distancia_al_circulo <= circulo_radio)

        # 3. Colisión con esferas rebotadoras dinámicas
        colision_bola = False
        for b in bolas:
            bx_cercano = max(rect_jugador.left, min(b["x"], rect_jugador.right))
            by_cercano = max(rect_jugador.top, min(b["y"], rect_jugador.bottom))
            if math.hypot(b["x"] - bx_cercano, b["y"] - by_cercano) <= b["r"]:
                colision_bola = True
                break

        # ---------------------------------------------------------------------
        # RENDERIZADO VISUAL
        # ---------------------------------------------------------------------
        pantalla.fill((18, 22, 32))

        # Encabezado
        pygame.draw.rect(pantalla, (25, 32, 48), (0, 0, ANCHO, 60))
        pygame.draw.line(pantalla, (45, 60, 90), (0, 60), (ANCHO, 60), 2)
        tit = fuente_tit.render("05: Detección de Colisiones (AABB, Círculos y Collidepoint)", True, (245, 245, 255))
        pantalla.blit(tit, (25, 15))

        # Área de simulación
        pygame.draw.rect(pantalla, (24, 30, 44), limite_area, border_radius=8)
        pygame.draw.rect(pantalla, (55, 70, 100), limite_area, width=2, border_radius=8)

        # Dibujar obstáculos rectangulares
        for i, obst in enumerate(obstaculos):
            choca = (i == indice_colision)
            col_obst = (235, 75, 90) if choca else (60, 80, 115)
            pygame.draw.rect(pantalla, col_obst, obst, border_radius=6)
            pygame.draw.rect(pantalla, (255, 255, 255) if choca else (100, 130, 175), obst, width=2, border_radius=6)

            # Etiqueta de coordenadas
            etq = fuente_mono.render(f"Obs #{i+1}", True, (255, 255, 255))
            pantalla.blit(etq, (obst.centerx - 22, obst.centery - 8))

        # Dibujar círculo fijo interactivo
        col_circ = (255, 80, 180) if hay_colision_circulo else (50, 160, 120)
        pygame.draw.circle(pantalla, col_circ, (int(circulo_pos[0]), int(circulo_pos[1])), circulo_radio)
        pygame.draw.circle(pantalla, (255, 255, 255), (int(circulo_pos[0]), int(circulo_pos[1])), circulo_radio, width=2)
        surf_c_txt = fuente_mono.render("Círculo", True, (255, 255, 255))
        pantalla.blit(surf_c_txt, (circulo_pos[0] - 24, circulo_pos[1] - 8))

        # Dibujar esferas móviles rebotadoras
        for b in bolas:
            pygame.draw.circle(pantalla, b["col"], (int(b["x"]), int(b["y"])), b["r"])
            pygame.draw.circle(pantalla, (255, 255, 255), (int(b["x"]), int(b["y"])), b["r"], width=2)

        # Dibujar Bloque del Jugador
        algun_choque = (hay_colision_rect or hay_colision_circulo or colision_bola)
        col_jugador = (255, 80, 80) if algun_choque else (50, 140, 245)
        pygame.draw.rect(pantalla, col_jugador, rect_jugador, border_radius=10)
        pygame.draw.rect(pantalla, (255, 255, 255), rect_jugador, width=3, border_radius=10)

        # Puntos de anclaje visuales de la clase Rect
        pygame.draw.circle(pantalla, (255, 255, 0), rect_jugador.center, 4)       # center
        pygame.draw.circle(pantalla, (0, 255, 255), rect_jugador.topleft, 4)      # topleft
        pygame.draw.circle(pantalla, (0, 255, 255), rect_jugador.bottomright, 4)  # bottomright

        texto_jugador = "¡COLISIÓN!" if algun_choque else "JUGADOR"
        surf_j = fuente_sub.render(texto_jugador, True, (255, 255, 255))
        pantalla.blit(surf_j, surf_j.get_rect(center=rect_jugador.center))

        # ---------------------------------------------------------------------
        # PANEL LATERAL DE TELEMETRÍA Y CONTROLES (DERECHA)
        # ---------------------------------------------------------------------
        px_panel = 680
        tit_tel = fuente_tit.render("Estado de Colisiones", True, (255, 215, 0))
        pantalla.blit(tit_tel, (px_panel, 75))

        estados = [
            f"Rect vs Rects:   {'IMPACTO ACTIVO' if hay_colision_rect else 'LIBRE'}",
            f"Rect vs Círculo: {'IMPACTO ACTIVO' if hay_colision_circulo else 'LIBRE'}",
            f"Rect vs Esferas: {'IMPACTO ACTIVO' if colision_bola else 'LIBRE'}",
            f"Posición Centro: ({rect_jugador.centerx}, {rect_jugador.centery})",
            f"TopLeft Rect:    ({rect_jugador.left}, {rect_jugador.top})",
            f"Obstáculos:      {len(obstaculos)} cajas",
            f"Esferas Móviles: {'ACTIVAS' if bolas_activas else 'PAUSADAS'}",
        ]

        pygame.draw.rect(pantalla, (24, 30, 44), (px_panel, 110, 230, 180), border_radius=6)
        for i, est in enumerate(estados):
            c_est = (255, 90, 90) if "IMPACTO" in est else ((120, 240, 160) if "LIBRE" in est else (200, 215, 235))
            surf_est = fuente_mono.render(est, True, c_est)
            pantalla.blit(surf_est, (px_panel + 12, 120 + i * 23))

        # Explicación pedagógica de los métodos Rect
        tit_exp = fuente_sub.render("Métodos Rect Explicados:", True, (130, 200, 255))
        pantalla.blit(tit_exp, (px_panel, 310))

        explicaciones = [
            "colliderect(): Chequeo AABB",
            "  Rápido entre dos rectángulos.",
            "collidepoint(): Punto en área",
            "  Perfecto para clics en botones.",
            "collidelist(): Busca en lista",
            "  Devuelve el índice del impacto.",
            "clamp_ip(): Confinamiento",
            "  Impide que salga del área.",
        ]
        pygame.draw.rect(pantalla, (20, 25, 38), (px_panel, 335, 230, 130), border_radius=6)
        for i, exp in enumerate(explicaciones):
            col_exp = (255, 220, 130) if ":" in exp else (170, 185, 205)
            surf_exp = fuente_mono.render(exp, True, col_exp)
            pantalla.blit(surf_exp, (px_panel + 10, 345 + i * 15))

        # Dibujar botones UI (collidepoint)
        boton_limpiar.dibujar(pantalla, fuente_sub)
        boton_agregar.dibujar(pantalla, fuente_sub)

        # Instrucciones de teclado al pie
        info_pie = fuente_mono.render("Arrastra con ratón | [WASD] Teclado | [ESPACIO] Nueva caja | [B] Esferas | [ESC] Salir", True, (150, 170, 195))
        pantalla.blit(info_pie, (25, ALTO - 18))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
