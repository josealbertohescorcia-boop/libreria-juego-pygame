"""
=============================================================================
07 - Arquitectura Orientada a Objetos: pygame.sprite.Sprite y Groups
=============================================================================
El módulo `pygame.sprite` proporciona la arquitectura estándar de la industria
para diseñar videojuegos organizados, limpios y escalables en Pygame:
  1. La clase pygame.sprite.Sprite:
     - El contrato fundamental: cada Sprite DEBE tener `self.image` y `self.rect`.
     - Encapsulación de lógica en el método `update()`.
     - El método `self.kill()`, que desvincula la entidad de todos sus grupos
       para una recolección de basura inmediata y limpia sin fugas de memoria.
  2. Contenedores de Sprites (pygame.sprite.Group y GroupSingle):
     - group.update(): actualiza todos los sprites del grupo en una sola llamada.
     - group.draw(superficie): dibuja todos los sprites por lotes optimizados.
  3. Colisiones masivas entre grupos:
     - pygame.sprite.groupcollide(): detecta impactos entre proyectiles y enemigos
       eliminando o dañando entidades de forma automática y declarativa.

Controles interactivos:
  - [RATÓN (Movimiento)]: Mover la nave defensora a lo largo del eje inferior.
  - [CLIC IZQ / ESPACIO]: Disparar láseres.
  - [AUTO (E)]: Activar o desactivar disparo automático continuo.
  - [G]: Forzar generación de una oleada de drones enemigos.
  - [ESC]: Salir.
=============================================================================
"""

import sys
import math
import random
import pygame

# -----------------------------------------------------------------------------
# Clases de Entidades basadas en pygame.sprite.Sprite
# -----------------------------------------------------------------------------

class Jugador(pygame.sprite.Sprite):
    """Nave defensora del jugador gestionada como Sprite."""
    def __init__(self, x_inicial, y_inicial):
        super().__init__()
        self.ancho, self.alto = 64, 50
        # Crear superficie con canal alfa
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._dibujar_nave()
        self.rect = self.image.get_rect(center=(x_inicial, y_inicial))
        self.cadencia_disparo = 0.15  # Segundos entre disparos
        self.temporizador_disparo = 0.0

    def _dibujar_nave(self):
        cx, cy = self.ancho // 2, self.alto // 2
        # Alas
        alas = [(cx, cy - 20), (cx + 30, cy + 18), (cx + 15, cy + 12), (cx, cy + 4),
                (cx - 15, cy + 12), (cx - 30, cy + 18)]
        pygame.draw.polygon(self.image, (40, 110, 220), alas)
        pygame.draw.polygon(self.image, (120, 190, 255), alas, width=2)
        # Cabina
        pygame.draw.polygon(self.image, (230, 240, 255), [(cx, cy - 24), (cx + 10, cy + 4), (cx - 10, cy + 4)])
        pygame.draw.circle(self.image, (0, 240, 255), (cx, cy - 8), 4)

    def update(self, dt, limite_x):
        # Seguir suavemente la posición X del ratón
        pos_raton_x = pygame.mouse.get_pos()[0]
        self.rect.centerx += (pos_raton_x - self.rect.centerx) * 14.0 * dt
        # Limitar dentro de los bordes asignados
        self.rect.left = max(20, self.rect.left)
        self.rect.right = min(limite_x - 20, self.rect.right)

        if self.temporizador_disparo > 0:
            self.temporizador_disparo -= dt

    def puede_disparar(self):
        return self.temporizador_disparo <= 0

    def reiniciar_cadencia(self):
        self.temporizador_disparo = self.cadencia_disparo

class Proyectil(pygame.sprite.Sprite):
    """Láser disparado por el jugador que viaja hacia arriba."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 22), pygame.SRCALPHA)
        # Resplandor exterior
        pygame.draw.rect(self.image, (0, 200, 255, 120), (0, 0, 8, 22), border_radius=4)
        # Núcleo brillante
        pygame.draw.rect(self.image, (255, 255, 255), (2, 2, 4, 18), border_radius=2)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = -620.0  # Pixeles por segundo

    def update(self, dt):
        self.rect.y += self.velocidad_y * dt
        # Si sale de la pantalla por arriba, se destruye de todos los grupos
        if self.rect.bottom < 50:
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    """Dron alienígena que desciende con oscilación senoidal."""
    def __init__(self, x, y, tipo=1):
        super().__init__()
        self.tipo = tipo
        self.ancho, self.alto = 52, 44
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._dibujar_dron()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x_base = float(x)
        self.pos_y = float(y)
        self.velocidad_y = random.uniform(85.0, 160.0)
        self.amplitud_oscilacion = random.uniform(30.0, 70.0)
        self.frecuencia_oscilacion = random.uniform(2.0, 4.0)
        self.tiempo_vivo = random.uniform(0.0, math.pi * 2)
        self.vida = 2 if tipo == 2 else 1

    def _dibujar_dron(self):
        cx, cy = self.ancho // 2, self.alto // 2
        color_cuerpo = (235, 60, 90) if self.tipo == 1 else (170, 60, 240)
        # Forma alienígena
        puntos = [(cx, cy + 18), (cx + 24, cy - 8), (cx + 12, cy - 18),
                  (cx - 12, cy - 18), (cx - 24, cy - 8)]
        pygame.draw.polygon(self.image, color_cuerpo, puntos)
        pygame.draw.polygon(self.image, (255, 255, 255), puntos, width=2)
        # Ojo cíclope luminoso
        pygame.draw.circle(self.image, (255, 220, 50), (cx, cy - 2), 6)
        pygame.draw.circle(self.image, (20, 20, 20), (cx, cy - 2), 3)

    def recibir_impacto(self):
        self.vida -= 1
        return self.vida <= 0

    def update(self, dt):
        self.tiempo_vivo += dt
        self.pos_y += self.velocidad_y * dt
        # Movimiento ondulante
        self.rect.y = int(self.pos_y)
        self.rect.centerx = int(self.pos_x_base + math.sin(self.tiempo_vivo * self.frecuencia_oscilacion) * self.amplitud_oscilacion)

        # Si supera el fondo de la pantalla, se destruye
        if self.rect.top > 650:
            self.kill()

class ParticulaExplosion(pygame.sprite.Sprite):
    """Partícula visual generada al destruir una entidad."""
    def __init__(self, x, y, color):
        super().__init__()
        self.radio = random.randint(3, 7)
        self.image = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radio, self.radio), self.radio)
        self.rect = self.image.get_rect(center=(x, y))

        angulo = random.uniform(0, math.pi * 2)
        velocidad = random.uniform(60.0, 220.0)
        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad
        self.vida = random.uniform(0.3, 0.6)
        self.vida_max = self.vida

    def update(self, dt):
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        self.vida -= dt
        if self.vida <= 0:
            self.kill()
        else:
            # Desvanecimiento progresivo
            alfa = int((self.vida / self.vida_max) * 255)
            self.image.set_alpha(alfa)

def main():
    pygame.init()
    ANCHO, ALTO = 940, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("07 - Arquitectura Orientada a Objetos: pygame.sprite")

    reloj = pygame.time.Clock()
    fuente_tit = pygame.font.SysFont("Segoe UI", 21, bold=True)
    fuente_sub = pygame.font.SysFont("Segoe UI", 16, bold=True)
    fuente_mono = pygame.font.SysFont("Consolas", 13)

    limite_area_juego = 650  # El resto es panel lateral

    # -------------------------------------------------------------------------
    # Grupos de Sprites (pygame.sprite.Group)
    # -------------------------------------------------------------------------
    # GroupSingle: optimizado para 1 solo sprite exclusivo (el jugador)
    grupo_jugador = pygame.sprite.GroupSingle()
    jugador = Jugador(limite_area_juego // 2, ALTO - 70)
    grupo_jugador.add(jugador)

    # Groups regulares: colecciones de entidades múltiples
    grupo_proyectiles = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_particulas = pygame.sprite.Group()

    # Variables de control
    temporizador_spawn_enemigo = 0.0
    intervalo_spawn = 1.0
    auto_disparo = False
    enemigos_destruidos = 0

    def crear_explosion(x, y, color=(255, 140, 50), cantidad=14):
        for _ in range(cantidad):
            grupo_particulas.add(ParticulaExplosion(x, y, color))

    # Generar oleada inicial
    for i in range(4):
        ex = random.randint(60, limite_area_juego - 60)
        ey = random.randint(80, 220)
        grupo_enemigos.add(Enemigo(ex, ey, tipo=random.choice([1, 2])))

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0
        temporizador_spawn_enemigo += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_e:
                    auto_disparo = not auto_disparo
                elif evento.key == pygame.K_g:
                    # Generar oleada manual
                    for _ in range(3):
                        ex = random.randint(60, limite_area_juego - 60)
                        ey = random.randint(70, 160)
                        grupo_enemigos.add(Enemigo(ex, ey, tipo=random.choice([1, 2])))
                elif evento.key == pygame.K_SPACE:
                    if jugador.puede_disparar():
                        # Disparo doble
                        grupo_proyectiles.add(Proyectil(jugador.rect.centerx - 14, jugador.rect.top))
                        grupo_proyectiles.add(Proyectil(jugador.rect.centerx + 14, jugador.rect.top))
                        jugador.reiniciar_cadencia()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and jugador.puede_disparar():
                    grupo_proyectiles.add(Proyectil(jugador.rect.centerx - 14, jugador.rect.top))
                    grupo_proyectiles.add(Proyectil(jugador.rect.centerx + 14, jugador.rect.top))
                    jugador.reiniciar_cadencia()

        # Disparo continuo si está en modo automático o si se mantiene presionado el ratón
        if (auto_disparo or pygame.mouse.get_pressed()[0]) and jugador.puede_disparar():
            grupo_proyectiles.add(Proyectil(jugador.rect.centerx - 14, jugador.rect.top))
            grupo_proyectiles.add(Proyectil(jugador.rect.centerx + 14, jugador.rect.top))
            jugador.reiniciar_cadencia()

        # Generación periódica automática de drones enemigos
        if temporizador_spawn_enemigo >= intervalo_spawn:
            temporizador_spawn_enemigo = 0.0
            if len(grupo_enemigos) < 12:
                ex = random.randint(60, limite_area_juego - 60)
                grupo_enemigos.add(Enemigo(ex, 70, tipo=random.choice([1, 2])))

        # =====================================================================
        # 1. ACTUALIZACIÓN POLIMÓRFICA DE GRUPOS (group.update())
        # =====================================================================
        grupo_jugador.update(dt, limite_area_juego)
        grupo_proyectiles.update(dt)
        grupo_enemigos.update(dt)
        grupo_particulas.update(dt)

        # =====================================================================
        # 2. COLISIÓN MASIVA DECLARATIVA: pygame.sprite.groupcollide()
        # =====================================================================
        # groupcollide(grupoA, grupoB, dokillA, dokillB):
        # Devuelve un diccionario donde cada clave es un proyectil y el valor
        # es la lista de enemigos impactados.
        impactos = pygame.sprite.groupcollide(grupo_proyectiles, grupo_enemigos, True, False)
        for proyectil, lista_enemigos in impactos.items():
            for enemigo in lista_enemigos:
                if enemigo.recibir_impacto():
                    enemigo.kill()  # Se desvincula de grupo_enemigos automáticamente
                    enemigos_destruidos += 1
                    col_exp = (255, 90, 110) if enemigo.tipo == 1 else (210, 90, 255)
                    crear_explosion(enemigo.rect.centerx, enemigo.rect.centery, color=col_exp)
                else:
                    crear_explosion(proyectil.rect.centerx, proyectil.rect.top, color=(100, 220, 255), cantidad=5)

        # ---------------------------------------------------------------------
        # RENDERIZADO VISUAL
        # ---------------------------------------------------------------------
        pantalla.fill((16, 20, 32))

        # Cuadrícula sutil del campo de juego
        for rx in range(0, limite_area_juego, 40):
            pygame.draw.line(pantalla, (23, 29, 44), (rx, 65), (rx, ALTO))
        for ry in range(65, ALTO, 40):
            pygame.draw.line(pantalla, (23, 29, 44), (0, ry), (limite_area_juego, ry))

        # Encabezado
        pygame.draw.rect(pantalla, (25, 32, 48), (0, 0, ANCHO, 65))
        pygame.draw.line(pantalla, (45, 60, 95), (0, 65), (ANCHO, 65), 2)
        tit = fuente_tit.render("07: Arquitectura pygame.sprite.Sprite, Group y groupcollide()", True, (245, 245, 255))
        pantalla.blit(tit, (25, 12))
        sub_hdr = fuente_mono.render("[Ratón] Mover nave   [Clic/Espacio] Disparar   [E] Auto-fuego   [G] Oleada   [ESC] Salir", True, (140, 180, 230))
        pantalla.blit(sub_hdr, (25, 38))

        # =====================================================================
        # 3. DIBUJADO OPTIMIZADO POR LOTES: group.draw(pantalla)
        # =====================================================================
        grupo_particulas.draw(pantalla)
        grupo_proyectiles.draw(pantalla)
        grupo_enemigos.draw(pantalla)
        grupo_jugador.draw(pantalla)

        # ---------------------------------------------------------------------
        # PANEL LATERAL DERECHO: INSPECTOR DE GRUPOS DE SPRITES
        # ---------------------------------------------------------------------
        px_panel = limite_area_juego
        pygame.draw.rect(pantalla, (22, 28, 42), (px_panel, 65, ANCHO - px_panel, ALTO - 65))
        pygame.draw.line(pantalla, (50, 65, 95), (px_panel, 65), (px_panel, ALTO), 2)

        tit_panel = fuente_sub.render("Monitor de Grupos Activos", True, (255, 215, 0))
        pantalla.blit(tit_panel, (px_panel + 20, 80))

        # Conteo exacto de instancias en memoria de cada grupo
        total_sprites = len(grupo_jugador) + len(grupo_proyectiles) + len(grupo_enemigos) + len(grupo_particulas)
        grupos_info = [
            ("grupo_jugador (GroupSingle):", f"{len(grupo_jugador)} entidad", (100, 190, 255)),
            ("grupo_proyectiles (Group):",   f"{len(grupo_proyectiles)} activos", (80, 230, 255)),
            ("grupo_enemigos (Group):",      f"{len(grupo_enemigos)} drones", (255, 110, 130)),
            ("grupo_particulas (Group):",    f"{len(grupo_particulas)} chispas", (255, 190, 90)),
            ("Total Sprites en memoria:",    f"{total_sprites} objetos", (130, 255, 170)),
            ("Enemigos destruidos:",         f"{enemigos_destruidos} bajas", (255, 235, 120)),
            ("Auto-disparo [E]:",            "ACTIVADO" if auto_disparo else "DESACTIVADO", (255, 255, 255)),
        ]

        pygame.draw.rect(pantalla, (16, 21, 32), (px_panel + 15, 110, ANCHO - px_panel - 30, 220), border_radius=8)
        for i, (nombre, valor, color) in enumerate(grupos_info):
            s_nom = fuente_mono.render(nombre, True, (170, 185, 210))
            s_val = fuente_mono.render(valor, True, color)
            pantalla.blit(s_nom, (px_panel + 25, 122 + i * 29))
            pantalla.blit(s_val, (px_panel + 25, 137 + i * 29))

        # Resumen de Conceptos Clave
        tit_conc = fuente_sub.render("Beneficios Arquitectónicos:", True, (130, 210, 255))
        pantalla.blit(tit_conc, (px_panel + 20, 350))

        conceptos = [
            "• Contrato self.image y self.rect:",
            "  Estandariza todas las entidades.",
            "• group.update():",
            "  Polimorfismo en 1 sola línea.",
            "• group.draw():",
            "  Renderizado por lotes veloz.",
            "• self.kill():",
            "  Elimina la entidad de TODOS",
            "  los grupos sin fugas de memoria.",
            "• groupcollide():",
            "  Colisiones N contra M en O(k).",
        ]
        pygame.draw.rect(pantalla, (16, 21, 32), (px_panel + 15, 375, ANCHO - px_panel - 30, 245), border_radius=8)
        for i, c in enumerate(conceptos):
            c_color = (255, 215, 130) if c.startswith("•") else (160, 175, 195)
            s_c = fuente_mono.render(c, True, c_color)
            pantalla.blit(s_c, (px_panel + 25, 385 + i * 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
