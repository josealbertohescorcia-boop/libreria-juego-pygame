"""
=============================================================================
04 - Superficies (Surface), Canal Alfa y Transformaciones en Pygame
=============================================================================
En Pygame, casi todo elemento visual es una 'Surface' (superficie).
Este módulo explica en profundidad:
  1. Creación de superficies en memoria con pygame.Surface((w, h)).
  2. Transparencias:
     - Superficies con canal alfa por píxel (pygame.SRCALPHA).
     - Opacidad global de superficie con surface.set_alpha(0-255).
     - Máscara de color transparente con surface.set_colorkey().
  3. Módulo pygame.transform:
     - Rotación (pygame.transform.rotate) manteniendo el centro fijo (sin temblor).
     - Escalado rápido (scale) vs suavizado de alta calidad (smoothscale).
     - Inversión de imagen horizontal y vertical (pygame.transform.flip).
     - Transformación combinada (rotozoom).
  4. Generación procedimental de sprites estilizados en código (100% autónomos).

Controles interactivos:
  - [1, 2, 3, 4]: Seleccionar el Sprite activo (Nave, Gema, Moneda, Orbe Neón).
  - [Q / E]: Rotar manualmente en sentido antihorario u horario.
  - [ESPACIO]: Activar / desactivar rotación automática continua.
  - [W / S]: Aumentar o reducir el factor de escala (zoom).
  - [A / D]: Aumentar o disminuir la transparencia (canal alfa global).
  - [H]: Voltear horizontalmente (Flip X).
  - [V]: Voltear verticalmente (Flip Y).
  - [R]: Restablecer valores de transformación por defecto.
  - [ESC]: Salir.
=============================================================================
"""

import sys
import math
import pygame

# -----------------------------------------------------------------------------
# Generadores de Sprites Procedimentales en memoria (Superficies con SRCALPHA)
# -----------------------------------------------------------------------------

def crear_sprite_nave():
    """Genera una superficie transparente con una nave espacial vectorizada."""
    w, h = 120, 120
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # Alas traseras
    alas = [(cx, cy - 45), (cx + 48, cy + 35), (cx + 25, cy + 30), (cx, cy + 15),
            (cx - 25, cy + 30), (cx - 48, cy + 35)]
    pygame.draw.polygon(surf, (45, 80, 140), alas)
    pygame.draw.polygon(surf, (100, 170, 255), alas, width=2)

    # Fuselaje principal
    fuselaje = [(cx, cy - 50), (cx + 20, cy + 25), (cx, cy + 38), (cx - 20, cy + 25)]
    pygame.draw.polygon(surf, (220, 230, 245), fuselaje)
    pygame.draw.polygon(surf, (70, 110, 180), fuselaje, width=2)

    # Cabina de cristal con brillo
    cabina = [(cx, cy - 25), (cx + 10, cy + 5), (cx - 10, cy + 5)]
    pygame.draw.polygon(surf, (0, 220, 255), cabina)
    pygame.draw.circle(surf, (255, 255, 255), (cx, cy - 10), 3)

    # Propulsores y fuego
    fuego = [(cx - 10, cy + 38), (cx, cy + 55), (cx + 10, cy + 38)]
    pygame.draw.polygon(surf, (255, 120, 30), fuego)
    pygame.draw.polygon(surf, (255, 240, 80), [(cx - 5, cy + 38), (cx, cy + 48), (cx + 5, cy + 38)])

    return surf

def crear_sprite_gema():
    """Genera una superficie con una gema esmeralda facetada."""
    w, h = 120, 120
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # Facetas de la gema
    p_arriba = (cx, cy - 45)
    p_abajo = (cx, cy + 45)
    p_der = (cx + 40, cy - 10)
    p_izq = (cx - 40, cy - 10)
    p_centro = (cx, cy - 5)

    # Polígonos de facetas con diferente iluminación
    pygame.draw.polygon(surf, (60, 220, 130), [p_arriba, p_der, p_centro])
    pygame.draw.polygon(surf, (30, 170, 90),  [p_arriba, p_izq, p_centro])
    pygame.draw.polygon(surf, (20, 130, 70),  [p_izq, p_abajo, p_centro])
    pygame.draw.polygon(surf, (40, 190, 100), [p_der, p_abajo, p_centro])

    # Bordes de las aristas
    for faceta in [[p_arriba, p_der, p_centro], [p_arriba, p_izq, p_centro],
                   [p_izq, p_abajo, p_centro], [p_der, p_abajo, p_centro]]:
        pygame.draw.polygon(surf, (200, 255, 220), faceta, width=2)

    # Destello de luz especular
    pygame.draw.circle(surf, (255, 255, 255), (cx - 15, cy - 20), 4)
    return surf

def crear_sprite_moneda():
    """Genera una moneda de oro con relieve circular."""
    w, h = 120, 120
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # Borde dorado exterior
    pygame.draw.circle(surf, (215, 155, 20), (cx, cy), 46)
    # Cuerpo brillante
    pygame.draw.circle(surf, (255, 205, 40), (cx, cy), 41)
    # Borde interior
    pygame.draw.circle(surf, (230, 175, 25), (cx, cy), 34, width=3)
    # Estrella o símbolo central
    puntos_estrella = []
    for i in range(10):
        r = 20 if (i % 2 == 0) else 10
        ang = i * (math.pi / 5) - math.pi / 2
        puntos_estrella.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    pygame.draw.polygon(surf, (255, 240, 130), puntos_estrella)
    return surf

def crear_sprite_orbe_resplandor():
    """Genera un orbe de energía neón con gradiente de transparencia alfa."""
    w, h = 140, 140
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # Círculos concéntricos con alfa decreciente para efecto de resplandor (bloom)
    for radio in range(60, 5, -3):
        factor = 1.0 - (radio / 60.0)
        alfa = int(factor * factor * 180)
        color = (180, 50, 255, alfa)
        pygame.draw.circle(surf, color, (cx, cy), radio)

    pygame.draw.circle(surf, (240, 180, 255), (cx, cy), 16)
    pygame.draw.circle(surf, (255, 255, 255), (cx, cy), 9)
    return surf

def rotar_sobre_centro(superficie, angulo, centro):
    """
    Rota una superficie alrededor de su centro sin producir desplazamiento o temblor.
    Retorna la nueva superficie y su nuevo rectángulo centrado en la posición original.
    """
    nueva_surf = pygame.transform.rotate(superficie, angulo)
    nuevo_rect = nueva_surf.get_rect(center=centro)
    return nueva_surf, nuevo_rect

def main():
    pygame.init()
    ANCHO, ALTO = 940, 640
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("04 - Superficies, Canal Alfa y Transformaciones")

    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Segoe UI", 21, bold=True)
    fuente_sub = pygame.font.SysFont("Segoe UI", 16, bold=True)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    # Catálogo de sprites creados en memoria
    sprites = [
        {"nombre": "Nave Estelar Vectorial", "surf": crear_sprite_nave()},
        {"nombre": "Gema Esmeralda Facetada", "surf": crear_sprite_gema()},
        {"nombre": "Moneda Dorada Mágica",   "surf": crear_sprite_moneda()},
        {"nombre": "Orbe Neón con Resplandor", "surf": crear_sprite_orbe_resplandor()},
    ]
    idx_sprite = 0

    # Variables de transformación
    angulo = 0.0
    escala = 1.0
    opacidad = 255
    volteo_x = False
    volteo_y = False
    auto_rotar = True
    velocidad_rotacion = 60.0  # Grados por segundo

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_1:
                    idx_sprite = 0
                elif evento.key == pygame.K_2:
                    idx_sprite = 1
                elif evento.key == pygame.K_3:
                    idx_sprite = 2
                elif evento.key == pygame.K_4:
                    idx_sprite = 3
                elif evento.key == pygame.K_SPACE:
                    auto_rotar = not auto_rotar
                elif evento.key == pygame.K_h:
                    volteo_x = not volteo_x
                elif evento.key == pygame.K_v:
                    volteo_y = not volteo_y
                elif evento.key == pygame.K_r:
                    # Restablecer valores
                    angulo = 0.0
                    escala = 1.0
                    opacidad = 255
                    volteo_x = False
                    volteo_y = False

        # Entrada continua para rotación manual, zoom y opacidad
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_q]:
            angulo = (angulo + 120.0 * dt) % 360
        if teclas[pygame.K_e]:
            angulo = (angulo - 120.0 * dt) % 360
        if teclas[pygame.K_w]:
            escala = min(2.8, escala + 0.8 * dt)
        if teclas[pygame.K_s]:
            escala = max(0.3, escala - 0.8 * dt)
        if teclas[pygame.K_a]:
            opacidad = max(20, opacidad - int(180 * dt))
        if teclas[pygame.K_d]:
            opacidad = min(255, opacidad + int(180 * dt))

        if auto_rotar:
            angulo = (angulo + velocidad_rotacion * dt) % 360

        # ---------------------------------------------------------------------
        # PROCESO DE TRANSFORMACIÓN EN CADENA
        # ---------------------------------------------------------------------
        # 1. Obtener la superficie base inalterada
        surf_base = sprites[idx_sprite]["surf"].copy()

        # 2. Aplicar transparencia global (canal alfa)
        surf_base.set_alpha(opacidad)

        # 3. Aplicar volteo (flip horizontal / vertical)
        if volteo_x or volteo_y:
            surf_base = pygame.transform.flip(surf_base, volteo_x, volteo_y)

        # 4. Aplicar escalado suave (smoothscale)
        ancho_orig, alto_orig = surf_base.get_size()
        nuevo_w = max(10, int(ancho_orig * escala))
        nuevo_h = max(10, int(alto_orig * escala))
        surf_escalada = pygame.transform.smoothscale(surf_base, (nuevo_w, nuevo_h))

        # 5. Aplicar rotación preservando el centro geométrico
        centro_escena = (ANCHO // 2 - 90, ALTO // 2 + 15)
        surf_final, rect_final = rotar_sobre_centro(surf_escalada, angulo, centro_escena)

        # ---------------------------------------------------------------------
        # RENDERIZADO VISUAL
        # ---------------------------------------------------------------------
        pantalla.fill((16, 20, 30))

        # Cuadrícula de transparencia estilo ajedrez (para apreciar el canal alfa)
        tam_cuad = 24
        area_lienzo_ancho = ANCHO - 300
        for gx in range(0, area_lienzo_ancho, tam_cuad):
            for gy in range(70, ALTO, tam_cuad):
                if ((gx // tam_cuad) + (gy // tam_cuad)) % 2 == 0:
                    pygame.draw.rect(pantalla, (23, 29, 44), (gx, gy, tam_cuad, tam_cuad))

        # Ejes guías y círculo de órbita
        pygame.draw.circle(pantalla, (45, 60, 90), centro_escena, 130, width=1)
        pygame.draw.line(pantalla, (40, 55, 80), (centro_escena[0] - 160, centro_escena[1]), (centro_escena[0] + 160, centro_escena[1]), 1)
        pygame.draw.line(pantalla, (40, 55, 80), (centro_escena[0], centro_escena[1] - 160), (centro_escena[0], centro_escena[1] + 160), 1)

        # Dibujar la superficie transformada final
        pantalla.blit(surf_final, rect_final)

        # Dibujar la caja delimitadora (Bounding Box del rect resultante)
        pygame.draw.rect(pantalla, (255, 200, 50), rect_final, width=1)

        # Punto del centro
        pygame.draw.circle(pantalla, (255, 60, 60), centro_escena, 4)

        # ---------------------------------------------------------------------
        # CABECERA Y PANEL LATERAL
        # ---------------------------------------------------------------------
        # Barra superior
        pygame.draw.rect(pantalla, (24, 30, 45), (0, 0, ANCHO, 65))
        pygame.draw.line(pantalla, (50, 65, 95), (0, 65), (ANCHO, 65), 2)
        tit = fuente_titulo.render("04: Superficies, Canal Alfa y Transformaciones 2D", True, (245, 245, 255))
        pantalla.blit(tit, (25, 10))

        tabs = "[1] Nave Estelar   [2] Gema   [3] Moneda   [4] Orbe Neón (Elige con 1-4)"
        surf_tabs = fuente_mono.render(tabs, True, (130, 200, 255))
        pantalla.blit(surf_tabs, (25, 38))

        # Panel lateral de propiedades
        px_panel = ANCHO - 300
        pygame.draw.rect(pantalla, (22, 28, 42), (px_panel, 65, 300, ALTO - 65))
        pygame.draw.line(pantalla, (50, 65, 95), (px_panel, 65), (px_panel, ALTO), 2)

        tit_prop = fuente_sub.render("Propiedades Activas", True, (255, 215, 0))
        pantalla.blit(tit_prop, (px_panel + 20, 80))

        props = [
            f"Sprite:      {sprites[idx_sprite]['nombre'][:18]}",
            f"Ángulo:      {angulo:5.1f}° {'(Giro ON)' if auto_rotar else '(Pausa)'}",
            f"Escala:      {escala:4.2f}x ({nuevo_w}x{nuevo_h} px)",
            f"Opacidad:    {opacidad}/255 ({int(opacidad/255*100)}%)",
            f"Volteo X:    {'SÍ' if volteo_x else 'NO'}",
            f"Volteo Y:    {'SÍ' if volteo_y else 'NO'}",
            f"BoundingBox: {rect_final.width}x{rect_final.height} px",
        ]
        pygame.draw.rect(pantalla, (16, 21, 32), (px_panel + 15, 110, 270, 185), border_radius=6)
        for i, pr in enumerate(props):
            col_p = (120, 240, 180) if "Ángulo" in pr else (200, 220, 240)
            surf_pr = fuente_mono.render(pr, True, col_p)
            pantalla.blit(surf_pr, (px_panel + 25, 122 + i * 23))

        # Panel de instrucciones
        tit_inst = fuente_sub.render("Controles de Teclado", True, (255, 160, 100))
        pantalla.blit(tit_inst, (px_panel + 20, 315))

        comandos = [
            "[1..4]: Cambiar de sprite",
            "[ESPACIO]: Pausar/Reanudar giro",
            "[Q / E]: Rotar manualmente",
            "[W / S]: Aumentar / Reducir zoom",
            "[A / D]: Modificar opacidad alfa",
            "[H / V]: Invertir en eje X / Y",
            "[R]: Resetear transformaciones",
            "[ESC]: Salir",
        ]
        pygame.draw.rect(pantalla, (16, 21, 32), (px_panel + 15, 345, 270, 250), border_radius=6)
        for i, cmd in enumerate(comandos):
            surf_c = fuente_mono.render(cmd, True, (170, 190, 215))
            pantalla.blit(surf_c, (px_panel + 25, 357 + i * 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
