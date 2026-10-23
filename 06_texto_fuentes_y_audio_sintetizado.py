"""
=============================================================================
06 - Texto, Fuentes Tipográficas y Audio Sintetizado en Pygame
=============================================================================
Este módulo cubre la comunicación audiovisual en Pygame:
  1. Módulo pygame.font:
     - Carga de fuentes del sistema (pygame.font.SysFont) y por defecto.
     - Renderizado de texto antialiased (suavizado) vs no suavizado.
     - Efectos tipográficos profesionales: sombras paralelas (drop shadow),
       contornos neón (outline) y pulsación dinámica de escala.
  2. Módulo pygame.mixer:
     - Inicialización robusta con manejo de excepciones (por si no hay hardware).
     - Síntesis de sonido procedural en memoria (¡sin depender de archivos WAV/MP3!).
     - Generación matemática de ondas (seno, rampa, ruido blanco) para efectos retro:
       Láser, Salto, Moneda, Explosión y Alarma de Daño.
     - Control de volumen y canales de reproducción.

Controles interactivos:
  - [1]: Sonido de Láser / Disparo (barrido descendente).
  - [2]: Sonido de Salto (barrido ascendente rápido).
  - [3]: Sonido de Moneda / Power-Up (doble campanilla brillante).
  - [4]: Sonido de Explosión (ruido blanco estocástico).
  - [5]: Sonido de Alarma / Daño (arpegio de alerta).
  - [TAB]: Alternar estilo tipográfico del letrero central.
  - [+ / -]: Subir o bajar el volumen maestro.
  - [ESC]: Salir.
=============================================================================
"""

import sys
import math
import struct
import random
import pygame

# -----------------------------------------------------------------------------
# Generadores Matemáticos de Audio Retro Chiptune (Bytes a pygame.mixer.Sound)
# -----------------------------------------------------------------------------

def generar_sonido_laser(tasa=22050):
    """Genera un sonido de disparo láser con barrido de frecuencia descendente."""
    duracion = 0.18
    num_muestras = int(tasa * duracion)
    buffer = bytearray()
    fase = 0.0

    for i in range(num_muestras):
        t = i / float(num_muestras)
        # Frecuencia cae de 900 Hz a 150 Hz
        freq = 900.0 * (1.0 - t * 0.85)
        fase += (2.0 * math.pi * freq) / tasa
        # Envolvente de decaimiento
        amplitud = 0.7 * (1.0 - t)
        muestra = int(32767.0 * amplitud * math.sin(fase))
        buffer.extend(struct.pack('<h', max(-32768, min(32767, muestra))))

    return pygame.mixer.Sound(buffer=buffer)

def generar_sonido_salto(tasa=22050):
    """Genera un sonido de salto arcade con barrido de frecuencia ascendente."""
    duracion = 0.22
    num_muestras = int(tasa * duracion)
    buffer = bytearray()
    fase = 0.0

    for i in range(num_muestras):
        t = i / float(num_muestras)
        # Frecuencia sube de 200 Hz a 650 Hz
        freq = 200.0 + 450.0 * (t ** 0.7)
        fase += (2.0 * math.pi * freq) / tasa
        # Onda cuadrada suave
        onda = 1.0 if math.sin(fase) > 0 else -1.0
        amplitud = 0.5 * (1.0 - t * 0.7)
        muestra = int(32767.0 * amplitud * onda)
        buffer.extend(struct.pack('<h', max(-32768, min(32767, muestra))))

    return pygame.mixer.Sound(buffer=buffer)

def generar_sonido_moneda(tasa=22050):
    """Genera una campanilla de moneda retro en dos notas ascendentes (B5 -> E6)."""
    duracion = 0.32
    num_muestras = int(tasa * duracion)
    mitad = num_muestras // 2
    buffer = bytearray()
    fase = 0.0

    for i in range(num_muestras):
        # Primera nota: 987 Hz (Si), Segunda nota: 1318 Hz (Mi)
        freq = 987.0 if i < mitad else 1318.0
        t_nota = (i if i < mitad else (i - mitad)) / float(mitad)
        fase += (2.0 * math.pi * freq) / tasa
        amplitud = 0.6 * (1.0 - t_nota * 0.6)
        muestra = int(32767.0 * amplitud * math.sin(fase))
        buffer.extend(struct.pack('<h', max(-32768, min(32767, muestra))))

    return pygame.mixer.Sound(buffer=buffer)

def generar_sonido_explosion(tasa=22050):
    """Genera una detonación usando ruido blanco con envolvente exponencial."""
    duracion = 0.45
    num_muestras = int(tasa * duracion)
    buffer = bytearray()

    for i in range(num_muestras):
        t = i / float(num_muestras)
        # Envolvente exponencial de decaimiento
        amplitud = 0.8 * math.exp(-t * 5.0)
        ruido = random.uniform(-1.0, 1.0)
        muestra = int(32767.0 * amplitud * ruido)
        buffer.extend(struct.pack('<h', max(-32768, min(32767, muestra))))

    return pygame.mixer.Sound(buffer=buffer)

def generar_sonido_alarma(tasa=22050):
    """Genera un tono de advertencia / impacto con modulación rápida."""
    duracion = 0.25
    num_muestras = int(tasa * duracion)
    buffer = bytearray()
    fase = 0.0

    for i in range(num_muestras):
        t = i / float(num_muestras)
        # Frecuencia oscila rápidamente entre 300 y 500 Hz
        freq = 400.0 + 100.0 * math.sin(2.0 * math.pi * 30.0 * (i / tasa))
        fase += (2.0 * math.pi * freq) / tasa
        amplitud = 0.5 * (1.0 - t)
        muestra = int(32767.0 * amplitud * math.sin(fase))
        buffer.extend(struct.pack('<h', max(-32768, min(32767, muestra))))

    return pygame.mixer.Sound(buffer=buffer)

def renderizar_texto_con_sombra(fuente, texto, color_frente, color_sombra, offset=(3, 3)):
    """Genera una superficie combinada con sombra paralela elegante."""
    surf_frente = fuente.render(texto, True, color_frente)
    surf_sombra = fuente.render(texto, True, color_sombra)

    w = surf_frente.get_width() + abs(offset[0])
    h = surf_frente.get_height() + abs(offset[1])
    surf_final = pygame.Surface((w, h), pygame.SRCALPHA)

    surf_final.blit(surf_sombra, (max(0, offset[0]), max(0, offset[1])))
    surf_final.blit(surf_frente, (max(0, -offset[0]), max(0, -offset[1])))
    return surf_final

def renderizar_texto_con_contorno(fuente, texto, color_frente, color_borde, grosor=2):
    """Genera una superficie con contorno perimetral (outline)."""
    surf_frente = fuente.render(texto, True, color_frente)
    surf_borde = fuente.render(texto, True, color_borde)

    w = surf_frente.get_width() + grosor * 2
    h = surf_frente.get_height() + grosor * 2
    surf_final = pygame.Surface((w, h), pygame.SRCALPHA)

    # Dibujar borde en 8 direcciones
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx != 0 or dy != 0:
                surf_final.blit(surf_borde, (dx + grosor, dy + grosor))

    surf_final.blit(surf_frente, (grosor, grosor))
    return surf_final

def main():
    pygame.init()

    # Inicialización segura del sistema de audio
    audio_disponible = False
    sonidos = {}
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        sonidos = {
            1: {"nombre": "Disparo Láser",  "sound": generar_sonido_laser(),     "color": (80, 220, 255)},
            2: {"nombre": "Salto Arcade",    "sound": generar_sonido_salto(),     "color": (120, 255, 140)},
            3: {"nombre": "Moneda / Premio", "sound": generar_sonido_moneda(),    "color": (255, 220, 70)},
            4: {"nombre": "Gran Explosión",  "sound": generar_sonido_explosion(), "color": (255, 100, 70)},
            5: {"nombre": "Alerta / Daño",   "sound": generar_sonido_alarma(),    "color": (240, 90, 220)},
        }
        audio_disponible = True
    except Exception as e:
        print(f"Aviso: No se pudo inicializar pygame.mixer ({e}). El programa correrá en modo silencioso.")

    ANCHO, ALTO = 940, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("06 - Tipografía, Fuentes y Audio Sintetizado")

    reloj = pygame.time.Clock()
    fuente_tit = pygame.font.SysFont("Segoe UI", 21, bold=True)
    fuente_banner = pygame.font.SysFont("Arial Black", 34)
    fuente_sub = pygame.font.SysFont("Segoe UI", 16, bold=True)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    volumen = 0.8
    ultimo_sonido_reproducido = "Ninguno (Pulsa 1..5 para escuchar)"
    color_destello = (50, 70, 100)
    tiempo_destello = 0.0

    # Barras de ecualizador gráfico animado
    num_barras = 18
    alturas_barras = [10.0] * num_barras

    estilo_texto = 1  # 1: Sombra, 2: Contorno Neón, 3: Pulso Dinámico
    tiempo_anim = 0.0

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0
        tiempo_anim += dt
        if tiempo_destello > 0:
            tiempo_destello -= dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_TAB:
                    estilo_texto = (estilo_texto % 3) + 1
                elif evento.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    volumen = min(1.0, volumen + 0.1)
                elif evento.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    volumen = max(0.0, volumen - 0.1)
                elif evento.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    idx = evento.key - pygame.K_0
                    if audio_disponible and idx in sonidos:
                        snd_info = sonidos[idx]
                        snd_info["sound"].set_volume(volumen)
                        snd_info["sound"].play()
                        ultimo_sonido_reproducido = f"Efecto #{idx}: {snd_info['nombre']}"
                        color_destello = snd_info["color"]
                        tiempo_destello = 0.4
                        # Excitar ecualizador
                        for b in range(num_barras):
                            alturas_barras[b] = random.uniform(40.0, 120.0)

        # Decaimiento del ecualizador
        for b in range(num_barras):
            alturas_barras[b] = max(8.0, alturas_barras[b] - 140.0 * dt)

        # ---------------------------------------------------------------------
        # RENDERIZADO VISUAL
        # ---------------------------------------------------------------------
        pantalla.fill((18, 22, 34))

        # Encabezado
        pygame.draw.rect(pantalla, (25, 32, 48), (0, 0, ANCHO, 65))
        pygame.draw.line(pantalla, (45, 60, 95), (0, 65), (ANCHO, 65), 2)
        tit = fuente_tit.render("06: Sistema de Fuentes (pygame.font) y Síntesis de Audio (pygame.mixer)", True, (245, 245, 255))
        pantalla.blit(tit, (25, 12))
        sub_hdr = fuente_mono.render("[1..5] Sonidos   [TAB] Alternar Estilo Texto   [+/-] Volumen   [ESC] Salir", True, (140, 180, 230))
        pantalla.blit(sub_hdr, (25, 38))

        # ---------------------------------------------------------------------
        # SECCIÓN 1: DEMOSTRACIÓN DE EFECTOS TIPOGRÁFICOS
        # ---------------------------------------------------------------------
        caja_texto = pygame.Rect(30, 85, ANCHO - 340, 200)
        pygame.draw.rect(pantalla, (24, 30, 46), caja_texto, border_radius=10)
        pygame.draw.rect(pantalla, (50, 65, 100), caja_texto, width=2, border_radius=10)

        tit_secc1 = fuente_sub.render(f"Efecto de Texto Activo (Pulsa TAB): Modo #{estilo_texto}", True, (255, 215, 0))
        pantalla.blit(tit_secc1, (45, 95))

        texto_lema = "PYGAME ARCADE 2026"
        centro_caja = (caja_texto.centerx, caja_texto.centery + 15)

        if estilo_texto == 1:
            # Texto con sombra paralela profunda
            surf_banner = renderizar_texto_con_sombra(fuente_banner, texto_lema, (255, 235, 90), (40, 20, 60), offset=(5, 5))
            r_banner = surf_banner.get_rect(center=centro_caja)
            pantalla.blit(surf_banner, r_banner)
            desc_modo = "Técnica: Dos llamadas a font.render() con desplazamiento (offset X/Y) para crear profundidad."

        elif estilo_texto == 2:
            # Texto con contorno brillante estilo neón
            surf_banner = renderizar_texto_con_contorno(fuente_banner, texto_lema, (255, 255, 255), (0, 180, 255), grosor=3)
            r_banner = surf_banner.get_rect(center=centro_caja)
            pantalla.blit(surf_banner, r_banner)
            desc_modo = "Técnica: Renderizado del color de contorno en las 8 direcciones perimetrales antes de estampar el frente."

        else:
            # Texto con pulso dinámico de escala
            factor_escala = 1.0 + math.sin(tiempo_anim * 4) * 0.12
            surf_base = fuente_banner.render(texto_lema, True, (255, 100, 180))
            w_esc = int(surf_base.get_width() * factor_escala)
            h_esc = int(surf_base.get_height() * factor_escala)
            surf_banner = pygame.transform.smoothscale(surf_base, (w_esc, h_esc))
            r_banner = surf_banner.get_rect(center=centro_caja)
            pantalla.blit(surf_banner, r_banner)
            desc_modo = "Técnica: font.render() combinado con transformación suave de escala en tiempo real."

        surf_desc = fuente_mono.render(desc_modo, True, (160, 180, 210))
        pantalla.blit(surf_desc, (45, caja_texto.bottom - 26))

        # ---------------------------------------------------------------------
        # SECCIÓN 2: VISUALIZADOR DE AUDIO Y EFECTOS SINTETIZADOS
        # ---------------------------------------------------------------------
        caja_audio = pygame.Rect(30, 305, ANCHO - 340, ALTO - 335)
        pygame.draw.rect(pantalla, (22, 28, 42), caja_audio, border_radius=10)
        pygame.draw.rect(pantalla, (50, 65, 100), caja_audio, width=2, border_radius=10)

        tit_secc2 = fuente_sub.render("Estudio de Efectos de Sonido Sintéticos (Muestras Procedurales en RAM)", True, (130, 220, 255))
        pantalla.blit(tit_secc2, (45, 318))

        # Indicador del último sonido
        color_ind = color_destello if tiempo_destello > 0 else (120, 140, 170)
        surf_ind = fuente_sub.render(ultimo_sonido_reproducido, True, color_ind)
        pantalla.blit(surf_ind, (45, 348))

        # Ecualizador de barras interactivo
        ancho_barra = 20
        espacio = 8
        inicio_eq_x = caja_audio.centerx - ((num_barras * (ancho_barra + espacio)) // 2)
        base_eq_y = caja_audio.bottom - 50

        for b in range(num_barras):
            bx = inicio_eq_x + b * (ancho_barra + espacio)
            by = base_eq_y - alturas_barras[b]
            # Gradiente de color según altura
            frac = alturas_barras[b] / 120.0
            r_col = int(50 + 205 * frac)
            g_col = int(220 - 120 * frac)
            b_col = int(120 + 130 * (1.0 - frac))
            pygame.draw.rect(pantalla, (r_col, g_col, b_col), (bx, by, ancho_barra, alturas_barras[b]), border_radius=4)
            pygame.draw.rect(pantalla, (255, 255, 255), (bx, by, ancho_barra, 3))

        linea_base = fuente_mono.render("Ecualizador de audio reactivo a eventos sonoros procedimentales", True, (130, 150, 180))
        pantalla.blit(linea_base, (caja_audio.centerx - 220, base_eq_y + 12))

        # ---------------------------------------------------------------------
        # PANEL LATERAL: CATÁLOGO DE SONIDOS Y VOLUMEN (DERECHA)
        # ---------------------------------------------------------------------
        px_panel = ANCHO - 290
        tit_cat = fuente_sub.render("Catálogo de Sonidos [1..5]", True, (255, 215, 0))
        pantalla.blit(tit_cat, (px_panel, 85))

        for i in range(1, 6):
            by = 115 + (i - 1) * 65
            if audio_disponible:
                info_s = sonidos[i]
                c_caja = (32, 40, 60)
                pygame.draw.rect(pantalla, c_caja, (px_panel, by, 260, 55), border_radius=8)
                pygame.draw.rect(pantalla, info_s["color"], (px_panel, by, 260, 55), width=2, border_radius=8)

                num_txt = fuente_sub.render(f"[{i}] {info_s['nombre']}", True, (255, 255, 255))
                pantalla.blit(num_txt, (px_panel + 12, by + 8))

                sub_t = fuente_mono.render("Presiona para reproducir", True, (160, 180, 210))
                pantalla.blit(sub_t, (px_panel + 12, by + 30))

        # Control de Volumen Maestro
        by_vol = 460
        tit_vol = fuente_sub.render("Volumen Maestro (+ / -)", True, (255, 180, 100))
        pantalla.blit(tit_vol, (px_panel, by_vol))

        # Barra medidora de volumen
        pygame.draw.rect(pantalla, (25, 30, 45), (px_panel, by_vol + 25, 260, 24), border_radius=6)
        ancho_vol = int(260 * volumen)
        pygame.draw.rect(pantalla, (80, 220, 140), (px_panel, by_vol + 25, ancho_vol, 24), border_radius=6)
        pygame.draw.rect(pantalla, (255, 255, 255), (px_panel, by_vol + 25, 260, 24), width=1, border_radius=6)

        txt_pct = fuente_mono.render(f"{int(volumen * 100)}%", True, (20, 25, 35))
        pantalla.blit(txt_pct, (px_panel + 115, by_vol + 28))

        # Estado del módulo de audio
        estado_audio_txt = "Estado Mixer: ACTIVO (22.05 kHz)" if audio_disponible else "Estado Mixer: NO DISPONIBLE"
        col_est = (100, 240, 160) if audio_disponible else (255, 100, 100)
        surf_est = fuente_mono.render(estado_audio_txt, True, col_est)
        pantalla.blit(surf_est, (px_panel, by_vol + 65))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
