"""
=============================================================================
03 - Manejo Integral de Eventos, Teclado y Ratón en Pygame
=============================================================================
Este módulo enseña los dos paradigmas esenciales de entrada de usuario en Pygame:
  1. Eventos Discretos (pygame.event.get()):
     - Cruciales para acciones instantáneas que deben ocurrir exactamente una vez
       por pulsación (abrir menús, disparar proyectiles, pausar, clic de ratón).
     - pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL.
  2. Muestreo de Estado Continuo (Polling):
     - pygame.key.get_pressed(): Devuelve el estado booleano de todas las teclas.
       Ideal para movimientos continuos y fluidos en tiempo real (WASD / Flechas).
     - pygame.mouse.get_pos() y pygame.mouse.get_pressed().

Controles interactivos:
  - [W, A, S, D] o [FLECHAS]: Mover el avatar de forma suave con aceleración.
  - [SHIFT]: Activar acelerador (turbo).
  - [RATÓN (Movimiento)]: El avatar orienta su cañón apuntando hacia el cursor.
  - [CLIC IZQUIERDO]: Disparar pulsos de energía hacia el ratón.
  - [CLIC DERECHO]: Crear onda expansiva en el punto del cursor.
  - [RUEDA DEL RATÓN]: Cambiar el radio / escala del avatar.
  - [C]: Limpiar las partículas del lienzo.
  - [ESC]: Salir.
=============================================================================
"""

import sys
import math
import pygame

def main():
    pygame.init()
    ANCHO, ALTO = 920, 640
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("03 - Manejo de Entrada: Eventos, Teclado y Ratón")

    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Segoe UI", 20, bold=True)
    fuente_texto = pygame.font.SysFont("Segoe UI", 15)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    # Estado del jugador / avatar
    px, py = ANCHO // 2 - 100, ALTO // 2
    vel_x, vel_y = 0.0, 0.0
    radio_jugador = 22
    color_jugador = (70, 160, 255)

    # Listas de entidades interactivas creadas por eventos
    proyectiles = []    # Lista de dicts {x, y, vx, vy, vida}
    ondas = []          # Lista de dicts {x, y, radio, radio_max, color}
    registro_eventos = ["Sistema de entrada iniciado. Esperando eventos..."]

    def registrar_evento(mensaje):
        registro_eventos.append(mensaje)
        if len(registro_eventos) > 9:
            registro_eventos.pop(0)

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        # =====================================================================
        # 1. PROCESAMIENTO DE EVENTOS DISCRETOS
        # =====================================================================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                nombre_tecla = pygame.key.name(evento.key).upper()
                registrar_evento(f"KEYDOWN: Tecla [{nombre_tecla}] (Código: {evento.key})")

                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_c:
                    proyectiles.clear()
                    ondas.clear()
                    registrar_evento("ACCIÓN: Lienzo limpiado.")

            elif evento.type == pygame.KEYUP:
                nombre_tecla = pygame.key.name(evento.key).upper()
                registrar_evento(f"KEYUP: Tecla soltada [{nombre_tecla}]")

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                boton = evento.button
                registrar_evento(f"MOUSEBUTTONDOWN: Botón {boton} en ({mx}, {my})")

                if boton == 1:  # Clic Izquierdo -> Disparar proyectil desde el avatar
                    angulo = math.atan2(my - py, mx - px)
                    vel_bala = 500.0
                    proyectiles.append({
                        "x": px,
                        "y": py,
                        "vx": math.cos(angulo) * vel_bala,
                        "vy": math.sin(angulo) * vel_bala,
                        "vida": 2.5
                    })
                elif boton == 3:  # Clic Derecho -> Onda expansiva
                    ondas.append({
                        "x": mx,
                        "y": my,
                        "radio": 5.0,
                        "radio_max": 70.0,
                        "color": (255, 120, 80)
                    })

            elif evento.type == pygame.MOUSEWHEEL:
                # Modificar tamaño del avatar con la rueda
                radio_jugador = max(12, min(50, radio_jugador + evento.y * 3))
                registrar_evento(f"MOUSEWHEEL: Desplazamiento Y = {evento.y} -> Radio: {radio_jugador}")

        # =====================================================================
        # 2. MUESTREO CONTINUO (POLLING) PARA MOVIMIENTO FLUIDO
        # =====================================================================
        teclas = pygame.key.get_pressed()
        mods = pygame.key.get_mods()

        fuerza_aceleracion = 1400.0
        if mods & pygame.KMOD_SHIFT:
            fuerza_aceleracion = 2400.0  # Modo turbo

        ax, ay = 0.0, 0.0
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            ay -= fuerza_aceleracion
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            ay += fuerza_aceleracion
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            ax -= fuerza_aceleracion
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            ax += fuerza_aceleracion

        # Integrar aceleración a la velocidad con fricción
        vel_x += ax * dt
        vel_y += ay * dt
        friccion = 8.0
        vel_x -= vel_x * friccion * dt
        vel_y -= vel_y * friccion * dt

        # Actualizar posición
        px += vel_x * dt
        py += vel_y * dt

        # Limitar dentro del área de juego interactiva
        limite_der = ANCHO - 330
        px = max(radio_jugador + 15, min(limite_der - radio_jugador - 15, px))
        py = max(radio_jugador + 15, min(ALTO - radio_jugador - 15, py))

        # =====================================================================
        # 3. ACTUALIZACIÓN DE PROYECTILES Y ONDAS
        # =====================================================================
        for p in proyectiles[:]:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vida"] -= dt
            if p["vida"] <= 0 or p["x"] < 0 or p["x"] > limite_der or p["y"] < 0 or p["y"] > ALTO:
                proyectiles.remove(p)

        for o in ondas[:]:
            o["radio"] += 140.0 * dt
            if o["radio"] >= o["radio_max"]:
                ondas.remove(o)

        # =====================================================================
        # 4. RENDERIZADO VISUAL
        # =====================================================================
        pantalla.fill((20, 24, 33))

        # Área de juego (rejilla de fondo sutil)
        for rx in range(0, limite_der, 40):
            pygame.draw.line(pantalla, (27, 33, 46), (rx, 0), (rx, ALTO))
        for ry in range(0, ALTO, 40):
            pygame.draw.line(pantalla, (27, 33, 46), (0, ry), (limite_der, ry))

        # Dibujar ondas expansivas (clic derecho)
        for o in ondas:
            progreso = o["radio"] / o["radio_max"]
            alfa_color = tuple(int(c * (1.0 - progreso)) for c in o["color"])
            grosor = max(1, int(4 * (1.0 - progreso)))
            pygame.draw.circle(pantalla, alfa_color, (int(o["x"]), int(o["y"])), int(o["radio"]), width=grosor)

        # Dibujar proyectiles (clic izquierdo)
        for p in proyectiles:
            pygame.draw.circle(pantalla, (255, 230, 80), (int(p["x"]), int(p["y"])), 6)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(p["x"]), int(p["y"])), 3)

        # Obtener posición actual del ratón para apuntar
        mx, my = pygame.mouse.get_pos()
        angulo_apuntado = math.atan2(my - py, mx - px)

        # Dibujar línea guía de apuntado punteada/fina
        if mx < limite_der:
            pygame.draw.line(pantalla, (60, 80, 110), (px, py), (mx, my), 1)
            pygame.draw.circle(pantalla, (255, 90, 90), (mx, my), 8, width=2)
            pygame.draw.circle(pantalla, (255, 90, 90), (mx, my), 2)

        # Dibujar Avatar (cuerpo y cañón apuntador)
        longitud_canon = radio_jugador + 14
        canon_fin_x = px + math.cos(angulo_apuntado) * longitud_canon
        canon_fin_y = py + math.sin(angulo_apuntado) * longitud_canon
        pygame.draw.line(pantalla, (240, 240, 250), (px, py), (canon_fin_x, canon_fin_y), 5)

        # Cuerpo del avatar
        pygame.draw.circle(pantalla, color_jugador, (int(px), int(py)), radio_jugador)
        pygame.draw.circle(pantalla, (255, 255, 255), (int(px), int(py)), radio_jugador, width=2)
        pygame.draw.circle(pantalla, (20, 30, 50), (int(px), int(py)), max(3, radio_jugador // 3))

        # ---------------------------------------------------------------------
        # PANEL LATERAL DE TELEMETRÍA Y REGISTRO DE EVENTOS (DERECHA)
        # ---------------------------------------------------------------------
        pygame.draw.rect(pantalla, (28, 34, 48), (limite_der, 0, ANCHO - limite_der, ALTO))
        pygame.draw.line(pantalla, (55, 68, 95), (limite_der, 0), (limite_der, ALTO), 2)

        # Título del panel
        tit_panel = fuente_titulo.render("Inspector de Entradas", True, (255, 215, 0))
        pantalla.blit(tit_panel, (limite_der + 20, 20))

        # Estado del ratón y jugador en vivo
        botones_raton = pygame.mouse.get_pressed()
        datos_telemetria = [
            f"Ratón X, Y:   ({mx:3d}, {my:3d})",
            f"Clics [I,C,D]: [{int(botones_raton[0])}, {int(botones_raton[1])}, {int(botones_raton[2])}]",
            f"Jugador X, Y: ({int(px):3d}, {int(py):3d})",
            f"Velocidad:    {math.hypot(vel_x, vel_y):5.1f} px/s",
            f"Radio Avatar: {radio_jugador} px",
            f"Turbo (SHIFT):{'ACTIVO' if (mods & pygame.KMOD_SHIFT) else 'INACTIVO'}",
            f"Proyectiles:  {len(proyectiles)}",
        ]

        pygame.draw.rect(pantalla, (20, 24, 35), (limite_der + 15, 55, ANCHO - limite_der - 30, 155), border_radius=6)
        for i, dato in enumerate(datos_telemetria):
            surf_dato = fuente_mono.render(dato, True, (190, 210, 235))
            pantalla.blit(surf_dato, (limite_der + 25, 65 + i * 20))

        # Registro de Eventos (Event Log en vivo)
        sub_log = fuente_texto.render("Registro de Eventos (FIFO):", True, (130, 220, 170))
        pantalla.blit(sub_log, (limite_der + 20, 225))

        pygame.draw.rect(pantalla, (16, 20, 28), (limite_der + 15, 250, ANCHO - limite_der - 30, 240), border_radius=6)
        for i, ev_str in enumerate(registro_eventos):
            color_ev = (255, 230, 140) if "MOUSEBUTTON" in ev_str else (180, 220, 255)
            surf_ev = fuente_mono.render(ev_str[:34], True, color_ev)
            pantalla.blit(surf_ev, (limite_der + 22, 260 + i * 23))

        # Guía de controles al fondo del panel
        sub_ctrl = fuente_texto.render("Guía de Controles:", True, (255, 180, 120))
        pantalla.blit(sub_ctrl, (limite_der + 20, 505))

        guia = [
            "WASD / Flechas: Mover avatar",
            "SHIFT: Correr con aceleración",
            "Clic Izq: Disparar proyectil",
            "Clic Der: Onda de impacto",
            "Rueda Ratón: Cambiar tamaño",
            "C: Limpiar proyectiles / ondas",
        ]
        for i, g in enumerate(guia):
            surf_g = fuente_mono.render(g, True, (160, 175, 195))
            pantalla.blit(surf_g, (limite_der + 20, 530 + i * 16))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
