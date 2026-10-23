"""
=============================================================================
08 - VIDEOJUEGO COMPLETO: "Cosmic Defender - Retro Space Arcade"
=============================================================================
Un videojuego arcade espacial completo desarrollado enteramente con Pygame,
integrando todas las técnicas, patrones y módulos aprendidos:
  - Máquina de Estados de Juego (Menú Principal, Gameplay, Pausa y Game Over).
  - Fondo espacial tridimensional simulado con múltiples capas de estrellas (Parallax).
  - Arquitectura orientada a objetos basada en pygame.sprite.Sprite y Group.
  - Cuatro tipos de enemigos: Drones de asalto, Cruceros con disparos, Asteroides
    rotatorios que se dividen al ser impactados y Jefes de oleada.
  - Cuatro power-ups coleccionables: Triple Blaster, Escudo de Invulnerabilidad,
    Kit de Reparación y Bomba Nova destructora.
  - Sistema de partículas para propulsores, chispas y explosiones expansivas.
  - Efectos de sonido procedurales chiptune generados matemáticamente en memoria.
  - Interfaz de usuario HUD completa con barra de escudo, oleadas y puntuación récord.

Controles:
  - [WASD] o [FLECHAS]: Mover la nave espacial.
  - [ESPACIO] o [CLIC IZQUIERDO]: Disparar láseres.
  - [P]: Pausar / reanudar la partida.
  - [R]: Reiniciar partida tras Game Over.
  - [M]: Volver al Menú Principal.
  - [ESC]: Salir del juego.
=============================================================================
"""

import sys
import math
import struct
import random
import pygame

# -----------------------------------------------------------------------------
# CONSTANTES GLOBALES
# -----------------------------------------------------------------------------
ANCHO, ALTO = 900, 700
FPS = 60

# Estados del juego
ESTADO_MENU = 1
ESTADO_JUGANDO = 2
ESTADO_PAUSA = 3
ESTADO_GAMEOVER = 4

# Colores del tema Arcade Neón
COLOR_FONDO = (10, 12, 22)
COLOR_TEXTO = (245, 248, 255)
COLOR_AMARILLO = (255, 215, 0)
COLOR_CIAN = (0, 230, 255)
COLOR_ROJO = (255, 75, 95)
COLOR_VERDE = (70, 240, 150)
COLOR_PURPURA = (180, 80, 255)

# -----------------------------------------------------------------------------
# GENERACIÓN DE AUDIO PROCEDIMENTAL EN RAM
# -----------------------------------------------------------------------------
class GestorAudio:
    """Sintetiza y reproduce efectos de sonido sin depender de archivos en disco."""
    def __init__(self):
        self.disponible = False
        self.sonidos = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.disponible = True
            self.sonidos["laser"] = self._sintetizar_laser()
            self.sonidos["laser_enemigo"] = self._sintetizar_laser_enemigo()
            self.sonidos["explosion_chica"] = self._sintetizar_explosion(0.25, 0.6)
            self.sonidos["explosion_grande"] = self._sintetizar_explosion(0.55, 0.9)
            self.sonidos["powerup"] = self._sintetizar_powerup()
            self.sonidos["dano"] = self._sintetizar_dano()
            self.sonidos["bomba"] = self._sintetizar_bomba()
        except Exception:
            self.disponible = False

    def reproducir(self, nombre, volumen=0.6):
        if self.disponible and nombre in self.sonidos:
            try:
                snd = self.sonidos[nombre]
                snd.set_volume(volumen)
                snd.play()
            except Exception:
                pass

    def _sintetizar_laser(self, tasa=22050):
        muestras = int(tasa * 0.12)
        buf = bytearray()
        fase = 0.0
        for i in range(muestras):
            t = i / float(muestras)
            freq = 950.0 * (1.0 - t * 0.8)
            fase += (2.0 * math.pi * freq) / tasa
            val = int(32767.0 * 0.5 * (1.0 - t) * math.sin(fase))
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

    def _sintetizar_laser_enemigo(self, tasa=22050):
        muestras = int(tasa * 0.15)
        buf = bytearray()
        fase = 0.0
        for i in range(muestras):
            t = i / float(muestras)
            freq = 350.0 + 150.0 * math.sin(t * 15.0)
            fase += (2.0 * math.pi * freq) / tasa
            val = int(32767.0 * 0.4 * (1.0 - t) * (1.0 if math.sin(fase) > 0 else -1.0))
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

    def _sintetizar_explosion(self, duracion, volumen, tasa=22050):
        muestras = int(tasa * duracion)
        buf = bytearray()
        for i in range(muestras):
            t = i / float(muestras)
            amp = volumen * math.exp(-t * 6.0)
            ruido = random.uniform(-1.0, 1.0)
            val = int(32767.0 * amp * ruido)
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

    def _sintetizar_powerup(self, tasa=22050):
        muestras = int(tasa * 0.28)
        mitad = muestras // 2
        buf = bytearray()
        fase = 0.0
        for i in range(muestras):
            freq = 880.0 if i < mitad else 1320.0
            t_loc = (i if i < mitad else (i - mitad)) / float(mitad)
            fase += (2.0 * math.pi * freq) / tasa
            val = int(32767.0 * 0.5 * (1.0 - t_loc * 0.5) * math.sin(fase))
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

    def _sintetizar_dano(self, tasa=22050):
        muestras = int(tasa * 0.18)
        buf = bytearray()
        fase = 0.0
        for i in range(muestras):
            t = i / float(muestras)
            freq = 220.0 - 100.0 * t
            fase += (2.0 * math.pi * freq) / tasa
            val = int(32767.0 * 0.6 * (1.0 - t) * (1.0 if math.sin(fase) > 0 else -1.0))
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

    def _sintetizar_bomba(self, tasa=22050):
        muestras = int(tasa * 0.7)
        buf = bytearray()
        fase = 0.0
        for i in range(muestras):
            t = i / float(muestras)
            freq = 140.0 * (1.0 - t * 0.6)
            fase += (2.0 * math.pi * freq) / tasa
            onda = math.sin(fase) + random.uniform(-0.5, 0.5)
            val = int(32767.0 * 0.8 * math.exp(-t * 3.5) * onda * 0.5)
            val = max(-32768, min(32767, val))
            buf.extend(struct.pack('<hh', val, val))
        return pygame.mixer.Sound(buffer=buf)

# -----------------------------------------------------------------------------
# FONDO PARALLAX MULTICAPA
# -----------------------------------------------------------------------------
class CampoEstelar:
    """Genera 3 capas de estrellas a diferentes velocidades para efecto 3D."""
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.estrellas = []
        # Capa 1: Lejana (pequeña y lenta)
        for _ in range(70):
            self.estrellas.append([random.randint(0, ancho), random.randint(0, alto), 1, 40.0, (140, 160, 200)])
        # Capa 2: Media
        for _ in range(45):
            self.estrellas.append([random.randint(0, ancho), random.randint(0, alto), 2, 85.0, (200, 220, 255)])
        # Capa 3: Cercana (brillante y rápida)
        for _ in range(25):
            self.estrellas.append([random.randint(0, ancho), random.randint(0, alto), 3, 160.0, (255, 255, 255)])

    def actualizar(self, dt):
        for e in self.estrellas:
            e[1] += e[3] * dt
            if e[1] > self.alto:
                e[1] = 0
                e[0] = random.randint(0, self.ancho)

    def dibujar(self, pantalla):
        for e in self.estrellas:
            pygame.draw.circle(pantalla, e[4], (int(e[0]), int(e[1])), e[2])

# -----------------------------------------------------------------------------
# SISTEMA DE PARTÍCULAS
# -----------------------------------------------------------------------------
class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y, color, radio=4, vel_max=180.0, vida_max=0.5):
        super().__init__()
        self.x, self.y = float(x), float(y)
        self.radio_inicial = radio
        self.color = color
        angulo = random.uniform(0, math.pi * 2)
        vel = random.uniform(20.0, vel_max)
        self.vx = math.cos(angulo) * vel
        self.vy = math.sin(angulo) * vel
        self.vida = vida_max
        self.vida_total = vida_max

        self.image = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        self.rect = self.image.get_rect(center=(int(x), int(y)))

    def update(self, dt):
        self.vida -= dt
        if self.vida <= 0:
            self.kill()
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))
        # Reducción de tamaño y opacidad
        progreso = self.vida / self.vida_total
        r = max(1, int(self.radio_inicial * progreso))
        alfa = int(255 * progreso)
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        col_con_alfa = (*self.color[:3], alfa)
        pygame.draw.circle(self.image, col_con_alfa, (r, r), r)

# -----------------------------------------------------------------------------
# CLASE NAVE DEL JUGADOR
# -----------------------------------------------------------------------------
class NaveJugador(pygame.sprite.Sprite):
    def __init__(self, audio):
        super().__init__()
        self.audio = audio
        self.ancho, self.alto = 66, 56
        self.image_base = self._crear_grafico_nave()
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 90))

        # Física de movimiento suave
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.aceleracion = 1800.0
        self.friccion = 8.5

        # Atributos de juego
        self.salud_max = 100
        self.salud = 100
        self.cadencia_disparo = 0.16
        self.temporizador_disparo = 0.0

        # Power-ups activos
        self.tiempo_triple_blaster = 0.0
        self.tiempo_escudo = 0.0
        self.invulnerable_dano = 0.0

    def _crear_grafico_nave(self):
        surf = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        cx, cy = self.ancho // 2, self.alto // 2
        # Alas y toberas
        alas = [(cx, cy - 24), (cx + 31, cy + 20), (cx + 18, cy + 15), (cx, cy + 6),
                (cx - 18, cy + 15), (cx - 31, cy + 20)]
        pygame.draw.polygon(surf, (30, 90, 200), alas)
        pygame.draw.polygon(surf, (0, 220, 255), alas, width=2)
        # Fuselaje central
        fuselaje = [(cx, cy - 27), (cx + 12, cy + 12), (cx, cy + 20), (cx - 12, cy + 12)]
        pygame.draw.polygon(surf, (235, 245, 255), fuselaje)
        pygame.draw.polygon(surf, (100, 160, 240), fuselaje, width=2)
        # Cabina
        pygame.draw.circle(surf, (0, 240, 255), (cx, cy - 8), 5)
        return surf

    def recibir_dano(self, cantidad):
        if self.tiempo_escudo > 0 or self.invulnerable_dano > 0:
            return False  # Bloqueado por escudo
        self.salud = max(0, self.salud - cantidad)
        self.invulnerable_dano = 0.8  # Parpadeo de invulnerabilidad post-daño
        self.audio.reproducir("dano", 0.7)
        return True

    def curar(self, cantidad):
        self.salud = min(self.salud_max, self.salud + cantidad)

    def activar_escudo(self, duracion=8.0):
        self.tiempo_escudo = duracion

    def activar_triple_blaster(self, duracion=10.0):
        self.tiempo_triple_blaster = duracion

    def update(self, dt, grupo_particulas):
        # Reducir temporizadores
        if self.temporizador_disparo > 0:
            self.temporizador_disparo -= dt
        if self.tiempo_triple_blaster > 0:
            self.tiempo_triple_blaster -= dt
        if self.tiempo_escudo > 0:
            self.tiempo_escudo -= dt
        if self.invulnerable_dano > 0:
            self.invulnerable_dano -= dt

        # Entrada por teclado
        teclas = pygame.key.get_pressed()
        ax, ay = 0.0, 0.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            ax -= self.aceleracion
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            ax += self.aceleracion
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            ay -= self.aceleracion
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            ay += self.aceleracion

        # Integrar física
        self.vel_x += ax * dt
        self.vel_y += ay * dt
        self.vel_x -= self.vel_x * self.friccion * dt
        self.vel_y -= self.vel_y * self.friccion * dt

        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

        # Confinar dentro de los bordes de la pantalla
        self.pos_x = max(self.ancho // 2, min(ANCHO - self.ancho // 2, self.pos_x))
        self.pos_y = max(self.alto // 2 + 60, min(ALTO - self.alto // 2 - 10, self.pos_y))
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        # Partículas de propulsión del motor
        if random.random() < 0.75:
            offset_y = self.rect.bottom - 4
            grupo_particulas.add(Particula(self.rect.centerx + random.randint(-4, 4), offset_y,
                                           (255, random.randint(120, 240), 40), radio=3, vel_max=80.0, vida_max=0.3))

        # Actualizar imagen con efectos visuales (Escudo o Parpadeo)
        self.image = self.image_base.copy()
        if self.tiempo_escudo > 0:
            # Dibujar burbuja de fuerza
            pygame.draw.circle(self.image, (0, 220, 255), (self.ancho // 2, self.alto // 2), self.ancho // 2 - 1, width=2)
            pygame.draw.circle(self.image, (180, 255, 255), (self.ancho // 2, self.alto // 2), self.ancho // 2 - 4, width=1)
        elif self.invulnerable_dano > 0 and int(self.invulnerable_dano * 18) % 2 == 0:
            self.image.set_alpha(80)

    def disparar(self, grupo_proyectiles):
        if self.temporizador_disparo > 0:
            return
        self.temporizador_disparo = self.cadencia_disparo
        self.audio.reproducir("laser", 0.5)

        if self.tiempo_triple_blaster > 0:
            # Ráfaga triple: centro, izquierda angulada, derecha angulada
            grupo_proyectiles.add(ProyectilLaser(self.rect.centerx, self.rect.top, 0.0, -700.0, True))
            grupo_proyectiles.add(ProyectilLaser(self.rect.centerx - 14, self.rect.top + 6, -140.0, -680.0, True))
            grupo_proyectiles.add(ProyectilLaser(self.rect.centerx + 14, self.rect.top + 6, 140.0, -680.0, True))
        else:
            # Doble láser estándar
            grupo_proyectiles.add(ProyectilLaser(self.rect.centerx - 16, self.rect.top + 4, 0.0, -700.0, True))
            grupo_proyectiles.add(ProyectilLaser(self.rect.centerx + 16, self.rect.top + 4, 0.0, -700.0, True))

# -----------------------------------------------------------------------------
# PROYECTIL LÁSER (JUGADOR Y ENEMIGO)
# -----------------------------------------------------------------------------
class ProyectilLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, es_jugador=True):
        super().__init__()
        self.es_jugador = es_jugador
        self.vx = vx
        self.vy = vy
        self.x = float(x)
        self.y = float(y)

        ancho, alto = (8, 22) if es_jugador else (10, 18)
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        color_ext = (0, 220, 255, 140) if es_jugador else (255, 60, 90, 160)
        color_int = (255, 255, 255) if es_jugador else (255, 220, 140)
        pygame.draw.rect(self.image, color_ext, (0, 0, ancho, alto), border_radius=4)
        pygame.draw.rect(self.image, color_int, (2, 2, ancho - 4, alto - 4), border_radius=2)
        self.rect = self.image.get_rect(center=(int(x), int(y)))

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))
        if self.rect.bottom < 40 or self.rect.top > ALTO + 20:
            self.kill()

# -----------------------------------------------------------------------------
# CLASES DE ENEMIGOS Y ASTEROIDES
# -----------------------------------------------------------------------------
class DronExplorador(pygame.sprite.Sprite):
    """Enemigo veloz con movimiento en zigzag."""
    def __init__(self, x, y, nivel_oleada=1):
        super().__init__()
        self.ancho, self.alto = 46, 38
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._dibujar()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_y = random.uniform(130.0, 190.0) + nivel_oleada * 10
        self.amplitud = random.uniform(40.0, 80.0)
        self.frecuencia = random.uniform(2.5, 4.0)
        self.tiempo = random.uniform(0.0, math.pi * 2)
        self.salud = 1
        self.puntos = 100

    def _dibujar(self):
        cx, cy = self.ancho // 2, self.alto // 2
        puntos = [(cx, cy + 16), (cx + 20, cy - 8), (cx + 8, cy - 16), (cx - 8, cy - 16), (cx - 20, cy - 8)]
        pygame.draw.polygon(self.image, (255, 60, 90), puntos)
        pygame.draw.polygon(self.image, (255, 200, 220), puntos, width=2)
        pygame.draw.circle(self.image, (255, 230, 50), (cx, cy - 2), 5)

    def update(self, dt, *args):
        self.tiempo += dt
        self.pos_y += self.vel_y * dt
        self.rect.y = int(self.pos_y)
        self.rect.centerx = int(self.pos_x + math.sin(self.tiempo * self.frecuencia) * self.amplitud)
        if self.rect.top > ALTO + 20:
            self.kill()

class CruceroPesado(pygame.sprite.Sprite):
    """Nave enemiga pesada que dispara proyectiles hacia el jugador."""
    def __init__(self, x, y, audio, nivel_oleada=1):
        super().__init__()
        self.audio = audio
        self.ancho, self.alto = 64, 52
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self._dibujar()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_y = random.uniform(55.0, 85.0)
        self.salud = 3 + (nivel_oleada // 3)
        self.puntos = 250
        self.cadencia_disparo = random.uniform(1.6, 2.4)
        self.tiempo_disparo = random.uniform(0.5, 1.5)

    def _dibujar(self):
        cx, cy = self.ancho // 2, self.alto // 2
        fuselaje = [(cx, cy + 22), (cx + 28, cy - 6), (cx + 18, cy - 22), (cx - 18, cy - 22), (cx - 28, cy - 6)]
        pygame.draw.polygon(self.image, (160, 50, 230), fuselaje)
        pygame.draw.polygon(self.image, (230, 160, 255), fuselaje, width=2)
        # Cañones dobles
        pygame.draw.rect(self.image, (255, 120, 50), (cx - 18, cy + 4, 6, 14))
        pygame.draw.rect(self.image, (255, 120, 50), (cx + 12, cy + 4, 6, 14))

    def update(self, dt, grupo_balas_enemigas, pos_jugador):
        self.pos_y += self.vel_y * dt
        self.rect.y = int(self.pos_y)

        # Disparar proyectiles dirigidos
        self.tiempo_disparo -= dt
        if self.tiempo_disparo <= 0:
            self.tiempo_disparo = self.cadencia_disparo
            self.audio.reproducir("laser_enemigo", 0.45)
            # Calcular vector hacia la posición del jugador
            dx = pos_jugador[0] - self.rect.centerx
            dy = pos_jugador[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                vel = 320.0
                vx = (dx / dist) * vel
                vy = (dy / dist) * vel
                grupo_balas_enemigas.add(ProyectilLaser(self.rect.centerx, self.rect.bottom, vx, vy, False))

        if self.rect.top > ALTO + 20:
            self.kill()

class Asteroide(pygame.sprite.Sprite):
    """Roca espacial giratoria que se fragmenta en pedazos al ser destruida."""
    def __init__(self, x, y, tamano=2):  # tamano 2: grande, 1: chico
        super().__init__()
        self.tamano = tamano
        self.radio = 38 if tamano == 2 else 20
        self.salud = 2 if tamano == 2 else 1
        self.puntos = 150 if tamano == 2 else 75

        self.image_base = self._generar_forma_asteroide()
        self.image = self.image_base.copy()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_y = random.uniform(90.0, 160.0)
        self.vel_x = random.uniform(-40.0, 40.0)
        self.angulo = 0.0
        self.vel_rotacion = random.uniform(-90.0, 90.0)

    def _generar_forma_asteroide(self):
        diametro = self.radio * 2 + 10
        surf = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
        cx, cy = diametro // 2, diametro // 2
        puntos = []
        num_vertices = 9
        for i in range(num_vertices):
            ang = i * (2 * math.pi / num_vertices)
            r = self.radio + random.uniform(-5, 5)
            puntos.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
        pygame.draw.polygon(surf, (120, 115, 130), puntos)
        pygame.draw.polygon(surf, (190, 185, 205), puntos, width=2)
        # Cráteres
        pygame.draw.circle(surf, (90, 85, 100), (cx - 6, cy - 6), max(2, self.radio // 4))
        return surf

    def update(self, dt, *args):
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.angulo = (self.angulo + self.vel_rotacion * dt) % 360

        # Rotar sobre su centro
        self.image = pygame.transform.rotate(self.image_base, self.angulo)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))

        if self.rect.top > ALTO + 30:
            self.kill()

# -----------------------------------------------------------------------------
# POWER-UPS
# -----------------------------------------------------------------------------
class PowerUp(pygame.sprite.Sprite):
    """Ítems coleccionables que mejoran la nave del jugador."""
    # Tipos: 'triple', 'escudo', 'vida', 'bomba'
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.radio = 18
        self.image = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        self._dibujar()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_y = 110.0
        self.tiempo = 0.0

    def _dibujar(self):
        cx, cy = self.radio, self.radio
        colores = {
            "triple": ((255, 215, 0), "3x"),
            "escudo": ((0, 220, 255), "SH"),
            "vida":   ((70, 240, 150), "+HP"),
            "bomba":  ((255, 75, 95), "BOM"),
        }
        color, etiqueta = colores.get(self.tipo, ((255, 255, 255), "?"))
        # Cápsula brillante
        pygame.draw.circle(self.image, color, (cx, cy), self.radio)
        pygame.draw.circle(self.image, (255, 255, 255), (cx, cy), self.radio, width=2)
        # Símbolo
        fnt = pygame.font.SysFont("Segoe UI", 11, bold=True)
        txt = fnt.render(etiqueta, True, (15, 20, 30))
        self.image.blit(txt, txt.get_rect(center=(cx, cy)))

    def update(self, dt):
        self.tiempo += dt
        self.pos_y += self.vel_y * dt
        # Ligera oscilación horizontal
        x_osc = self.pos_x + math.sin(self.tiempo * 5.0) * 15.0
        self.rect.center = (int(x_osc), int(self.pos_y))
        if self.rect.top > ALTO + 20:
            self.kill()

# -----------------------------------------------------------------------------
# CLASE PRINCIPAL DEL JUEGO
# -----------------------------------------------------------------------------
class VideojuegoCosmicDefender:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Cosmic Defender: Retro Space Arcade")
        self.reloj = pygame.time.Clock()

        self.audio = GestorAudio()
        self.campo_estrellas = CampoEstelar(ANCHO, ALTO)

        # Fuentes
        self.fuente_logo = pygame.font.SysFont("Arial Black", 44)
        self.fuente_tit = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.fuente_sub = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.fuente_mono = pygame.font.SysFont("Consolas", 14)

        # Estado global
        self.estado = ESTADO_MENU
        self.puntuacion_maxima = 0
        self.reiniciar_partida()

    def reiniciar_partida(self):
        """Inicializa todas las entidades para comenzar una nueva partida."""
        self.jugador = NaveJugador(self.audio)
        self.grupo_jugador = pygame.sprite.GroupSingle(self.jugador)

        self.grupo_lasers_jugador = pygame.sprite.Group()
        self.grupo_lasers_enemigos = pygame.sprite.Group()
        self.grupo_enemigos = pygame.sprite.Group()
        self.grupo_asteroides = pygame.sprite.Group()
        self.grupo_powerups = pygame.sprite.Group()
        self.grupo_particulas = pygame.sprite.Group()

        # Métricas de la partida
        self.puntuacion = 0
        self.oleada = 1
        self.enemigos_restantes_oleada = 12
        self.enemigos_totales_destruidos = 0
        self.temporizador_aparicion = 0.0
        self.intervalo_aparicion = 1.3
        self.mensaje_oleada_tiempo = 2.5

    def crear_explosion(self, x, y, color=(255, 140, 50), cantidad=20, radio=5):
        for _ in range(cantidad):
            self.grupo_particulas.add(Particula(x, y, color, radio=radio, vel_max=220.0, vida_max=0.55))

    def activar_bomba_nova(self):
        """Detona a todos los enemigos y asteroides presentes en pantalla."""
        self.audio.reproducir("bomba", 0.9)
        # Destruir enemigos
        for enemigo in list(self.grupo_enemigos):
            self.puntuacion += enemigo.puntos
            self.enemigos_totales_destruidos += 1
            self.crear_explosion(enemigo.rect.centerx, enemigo.rect.centery, (255, 100, 220), cantidad=18)
            enemigo.kill()
        # Destruir asteroides
        for asteroide in list(self.grupo_asteroides):
            self.puntuacion += asteroide.puntos
            self.crear_explosion(asteroide.rect.centerx, asteroide.rect.centery, (180, 180, 190), cantidad=15)
            asteroide.kill()
        self.grupo_lasers_enemigos.empty()

    def procesar_logica_oleada(self, dt):
        """Gestiona el ritmo de aparición de enemigos y transición de oleadas."""
        if self.mensaje_oleada_tiempo > 0:
            self.mensaje_oleada_tiempo -= dt

        self.temporizador_aparicion += dt
        if self.temporizador_aparicion >= self.intervalo_aparicion:
            self.temporizador_aparicion = 0.0

            if self.enemigos_restantes_oleada > 0:
                self.enemigos_restantes_oleada -= 1
                rx = random.randint(60, ANCHO - 60)

                # Probabilidades de tipo de enemigo
                r = random.random()
                if r < 0.45:
                    self.grupo_enemigos.add(DronExplorador(rx, -30, self.oleada))
                elif r < 0.75:
                    self.grupo_asteroides.add(Asteroide(rx, -40, tamano=2))
                else:
                    self.grupo_enemigos.add(CruceroPesado(rx, -40, self.audio, self.oleada))

            # Si ya se generaron todos y no quedan enemigos vivos, avanzar oleada
            elif len(self.grupo_enemigos) == 0 and len(self.grupo_asteroides) == 0:
                self.oleada += 1
                self.enemigos_restantes_oleada = 10 + self.oleada * 4
                self.intervalo_aparicion = max(0.45, 1.3 - (self.oleada * 0.08))
                self.mensaje_oleada_tiempo = 2.5
                self.audio.reproducir("powerup", 0.8)
                # Bonificación de reparación entre oleadas
                self.jugador.curar(20)

    def soltar_powerup_aleatorio(self, x, y):
        """Genera un power-up con probabilidad del 22% al destruir una amenaza."""
        if random.random() < 0.22:
            tipo = random.choices(["triple", "escudo", "vida", "bomba"], weights=[35, 30, 25, 10])[0]
            self.grupo_powerups.add(PowerUp(x, y, tipo))

    # -------------------------------------------------------------------------
    # BUCLE DE EVENTOS Y ACTUALIZACIÓN
    # -------------------------------------------------------------------------
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            dt = self.reloj.tick(FPS) / 1000.0
            pos_raton = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == ESTADO_JUGANDO:
                            self.estado = ESTADO_PAUSA
                        elif self.estado == ESTADO_PAUSA:
                            self.estado = ESTADO_JUGANDO
                        else:
                            ejecutando = False

                    elif evento.key == pygame.K_p:
                        if self.estado == ESTADO_JUGANDO:
                            self.estado = ESTADO_PAUSA
                        elif self.estado == ESTADO_PAUSA:
                            self.estado = ESTADO_JUGANDO

                    elif evento.key == pygame.K_r:
                        if self.estado in (ESTADO_GAMEOVER, ESTADO_PAUSA):
                            self.reiniciar_partida()
                            self.estado = ESTADO_JUGANDO

                    elif evento.key == pygame.K_m:
                        if self.estado in (ESTADO_GAMEOVER, ESTADO_PAUSA):
                            self.estado = ESTADO_MENU

                    elif evento.key == pygame.K_SPACE:
                        if self.estado == ESTADO_MENU:
                            self.reiniciar_partida()
                            self.estado = ESTADO_JUGANDO
                        elif self.estado == ESTADO_GAMEOVER:
                            self.reiniciar_partida()
                            self.estado = ESTADO_JUGANDO

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.estado == ESTADO_MENU:
                        self.reiniciar_partida()
                        self.estado = ESTADO_JUGANDO
                    elif self.estado == ESTADO_GAMEOVER:
                        self.reiniciar_partida()
                        self.estado = ESTADO_JUGANDO

            # Actualizar fondo parallax
            self.campo_estrellas.actualizar(dt)

            # -----------------------------------------------------------------
            # LÓGICA DE JUEGO ACTIVO
            # -----------------------------------------------------------------
            if self.estado == ESTADO_JUGANDO:
                # Disparo continuo con barra espaciadora o clic sostenido
                teclas = pygame.key.get_pressed()
                if teclas[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                    self.jugador.disparar(self.grupo_lasers_jugador)

                # Generador de oleadas
                self.procesar_logica_oleada(dt)

                # Actualizaciones de entidades
                self.grupo_jugador.update(dt, self.grupo_particulas)
                self.grupo_lasers_jugador.update(dt)
                self.grupo_lasers_enemigos.update(dt)
                self.grupo_enemigos.update(dt, self.grupo_lasers_enemigos, self.jugador.rect.center)
                self.grupo_asteroides.update(dt)
                self.grupo_powerups.update(dt)
                self.grupo_particulas.update(dt)

                # --- 1. COLISIÓN: LÁSERES DEL JUGADOR vs ENEMIGOS ---
                impactos_enemigos = pygame.sprite.groupcollide(self.grupo_lasers_jugador, self.grupo_enemigos, True, False)
                for laser, lista_enemigos in impactos_enemigos.items():
                    for enemigo in lista_enemigos:
                        enemigo.salud -= 1
                        if enemigo.salud <= 0:
                            enemigo.kill()
                            self.puntuacion += enemigo.puntos
                            self.enemigos_totales_destruidos += 1
                            self.audio.reproducir("explosion_chica", 0.6)
                            self.crear_explosion(enemigo.rect.centerx, enemigo.rect.centery, (255, 90, 110), cantidad=16)
                            self.soltar_powerup_aleatorio(enemigo.rect.centerx, enemigo.rect.centery)
                        else:
                            self.crear_explosion(laser.rect.centerx, laser.rect.top, (255, 230, 100), cantidad=6)

                # --- 2. COLISIÓN: LÁSERES DEL JUGADOR vs ASTEROIDES ---
                impactos_asteroides = pygame.sprite.groupcollide(self.grupo_lasers_jugador, self.grupo_asteroides, True, False)
                for laser, lista_asteroides in impactos_asteroides.items():
                    for ast in lista_asteroides:
                        ast.salud -= 1
                        if ast.salud <= 0:
                            ast.kill()
                            self.puntuacion += ast.puntos
                            self.audio.reproducir("explosion_grande", 0.65)
                            self.crear_explosion(ast.rect.centerx, ast.rect.centery, (160, 155, 175), cantidad=18, radio=4)
                            self.soltar_powerup_aleatorio(ast.rect.centerx, ast.rect.centery)
                            # Fragmentar en 2 asteroides pequeños si era grande
                            if ast.tamano == 2:
                                for desv in (-25, 25):
                                    nuevo_ast = Asteroide(ast.rect.centerx + desv, ast.rect.centery, tamano=1)
                                    nuevo_ast.vel_x = desv * 2.5
                                    self.grupo_asteroides.add(nuevo_ast)
                        else:
                            self.crear_explosion(laser.rect.centerx, laser.rect.top, (200, 200, 220), cantidad=5)

                # --- 3. COLISIÓN: JUGADOR vs LÁSERES ENEMIGOS ---
                balas_impactan_jugador = pygame.sprite.spritecollide(self.jugador, self.grupo_lasers_enemigos, True)
                for bala in balas_impactan_jugador:
                    self.crear_explosion(bala.rect.centerx, bala.rect.centery, (255, 70, 70), cantidad=10)
                    self.jugador.recibir_dano(18)

                # --- 4. COLISIÓN: JUGADOR vs ENEMIGOS FÍSICOS ---
                choques_enemigos = pygame.sprite.spritecollide(self.jugador, self.grupo_enemigos, True)
                for enemigo in choques_enemigos:
                    self.crear_explosion(enemigo.rect.centerx, enemigo.rect.centery, (255, 120, 50), cantidad=24)
                    self.jugador.recibir_dano(28)

                # --- 5. COLISIÓN: JUGADOR vs ASTEROIDES ---
                choques_asteroides = pygame.sprite.spritecollide(self.jugador, self.grupo_asteroides, True)
                for ast in choques_asteroides:
                    self.crear_explosion(ast.rect.centerx, ast.rect.centery, (180, 170, 190), cantidad=22)
                    self.jugador.recibir_dano(34)

                # --- 6. COLISIÓN: JUGADOR vs POWER-UPS ---
                powerups_recogidos = pygame.sprite.spritecollide(self.jugador, self.grupo_powerups, True)
                for p in powerups_recogidos:
                    self.audio.reproducir("powerup", 0.75)
                    self.crear_explosion(p.rect.centerx, p.rect.centery, (100, 255, 220), cantidad=14)
                    if p.tipo == "triple":
                        self.jugador.activar_triple_blaster(10.0)
                    elif p.tipo == "escudo":
                        self.jugador.activar_escudo(8.0)
                    elif p.tipo == "vida":
                        self.jugador.curar(35)
                    elif p.tipo == "bomba":
                        self.activar_bomba_nova()

                # Comprobar derrota
                if self.jugador.salud <= 0:
                    self.audio.reproducir("explosion_grande", 1.0)
                    self.crear_explosion(self.jugador.rect.centerx, self.jugador.rect.centery, (255, 180, 50), cantidad=40, radio=6)
                    self.estado = ESTADO_GAMEOVER
                    if self.puntuacion > self.puntuacion_maxima:
                        self.puntuacion_maxima = self.puntuacion

            # -----------------------------------------------------------------
            # RENDERIZADO VISUAL SEGÚN ESTADO
            # -----------------------------------------------------------------
            self.pantalla.fill(COLOR_FONDO)
            self.campo_estrellas.dibujar(self.pantalla)

            if self.estado == ESTADO_JUGANDO:
                self.dibujar_juego_activo()
            elif self.estado == ESTADO_MENU:
                self.dibujar_menu_principal()
            elif self.estado == ESTADO_PAUSA:
                self.dibujar_juego_activo()
                self.dibujar_overlay_pausa()
            elif self.estado == ESTADO_GAMEOVER:
                self.dibujar_pantalla_gameover()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # -------------------------------------------------------------------------
    # PANTALLAS Y MÓDULOS DE RENDERIZADO
    # -------------------------------------------------------------------------
    def dibujar_juego_activo(self):
        # Dibujar entidades del juego
        self.grupo_particulas.draw(self.pantalla)
        self.grupo_powerups.draw(self.pantalla)
        self.grupo_asteroides.draw(self.pantalla)
        self.grupo_enemigos.draw(self.pantalla)
        self.grupo_lasers_enemigos.draw(self.pantalla)
        self.grupo_lasers_jugador.draw(self.pantalla)
        self.grupo_jugador.draw(self.pantalla)

        # ---------------------------------------------------------------------
        # HUD SUPERIOR (CABECERA DE INFORMACIÓN)
        # ---------------------------------------------------------------------
        # Fondo translúcido superior
        pygame.draw.rect(self.pantalla, (18, 22, 36), (0, 0, ANCHO, 56))
        pygame.draw.line(self.pantalla, (45, 60, 95), (0, 56), (ANCHO, 56), 2)

        # Barra de Salud / Escudo del Jugador
        salud_pct = max(0.0, self.jugador.salud / float(self.jugador.salud_max))
        ancho_barra = 180
        color_salud = COLOR_VERDE if salud_pct > 0.5 else (COLOR_AMARILLO if salud_pct > 0.25 else COLOR_ROJO)
        pygame.draw.rect(self.pantalla, (35, 42, 60), (25, 16, ancho_barra, 22), border_radius=5)
        pygame.draw.rect(self.pantalla, color_salud, (25, 16, int(ancho_barra * salud_pct), 22), border_radius=5)
        pygame.draw.rect(self.pantalla, (255, 255, 255), (25, 16, ancho_barra, 22), width=1, border_radius=5)

        txt_salud = self.fuente_mono.render(f"CASCO: {self.jugador.salud}%", True, (255, 255, 255))
        self.pantalla.blit(txt_salud, (40, 19))

        # Indicador de Power-up Activo
        if self.jugador.tiempo_escudo > 0:
            txt_pw = self.fuente_mono.render(f"🛡️ ESCUDO: {self.jugador.tiempo_escudo:.1f}s", True, COLOR_CIAN)
            self.pantalla.blit(txt_pw, (225, 19))
        elif self.jugador.tiempo_triple_blaster > 0:
            txt_pw = self.fuente_mono.render(f"⚡ TRIPLE: {self.jugador.tiempo_triple_blaster:.1f}s", True, COLOR_AMARILLO)
            self.pantalla.blit(txt_pw, (225, 19))

        # Puntuación actual y Oleada
        txt_oleada = self.fuente_sub.render(f"OLEADA {self.oleada}", True, COLOR_PURPURA)
        self.pantalla.blit(txt_oleada, (ANCHO // 2 - 45, 16))

        txt_puntos = self.fuente_sub.render(f"SCORE: {self.puntuacion:06d}", True, COLOR_AMARILLO)
        self.pantalla.blit(txt_puntos, (ANCHO - 220, 16))

        # Cartel de nueva oleada flotante
        if self.mensaje_oleada_tiempo > 0:
            alfa_msg = int(min(1.0, self.mensaje_oleada_tiempo) * 255)
            surf_ol = self.fuente_tit.render(f"¡OLEADA {self.oleada} EN CURSO!", True, (255, 240, 100))
            surf_ol.set_alpha(alfa_msg)
            r_ol = surf_ol.get_rect(center=(ANCHO // 2, 140))
            self.pantalla.blit(surf_ol, r_ol)

    def dibujar_menu_principal(self):
        # Título estilo Neón Arcade
        surf_tit = self.fuente_logo.render("COSMIC DEFENDER", True, COLOR_CIAN)
        surf_som = self.fuente_logo.render("COSMIC DEFENDER", True, (20, 50, 90))
        r_tit = surf_tit.get_rect(center=(ANCHO // 2, 160))
        self.pantalla.blit(surf_som, (r_tit.x + 4, r_tit.y + 4))
        self.pantalla.blit(surf_tit, r_tit)

        surf_sub = self.fuente_sub.render("Retro Space Arcade Experience en Python y Pygame", True, (200, 220, 255))
        self.pantalla.blit(surf_sub, surf_sub.get_rect(center=(ANCHO // 2, 220)))

        # Tarjeta de Instrucciones
        caja = pygame.Rect(ANCHO // 2 - 270, 270, 540, 250)
        pygame.draw.rect(self.pantalla, (22, 28, 44), caja, border_radius=12)
        pygame.draw.rect(self.pantalla, (55, 75, 120), caja, width=2, border_radius=12)

        tit_inst = self.fuente_sub.render("Instrucciones de Vuelo:", True, COLOR_AMARILLO)
        self.pantalla.blit(tit_inst, (caja.x + 25, caja.y + 20))

        guia = [
            "• [WASD] o [Flechas]: Pilotar la nave espacial",
            "• [ESPACIO] o [Clic Izquierdo]: Disparar láseres de plasma",
            "• [P]: Pausar o reanudar el combate",
            "• Derriba Drones, Cruceros y Asteroides para puntuar",
            "• Recoge Power-ups: ⚡Triple, 🛡️Escudo, 💚Salud, 💣Bomba",
        ]
        for i, g in enumerate(guia):
            s_g = self.fuente_mono.render(g, True, (210, 225, 245))
            self.pantalla.blit(s_g, (caja.x + 25, caja.y + 60 + i * 28))

        # Botón / Llamado a la acción parpadeante
        pulso = (math.sin(pygame.time.get_ticks() * 0.006) + 1.0) / 2.0
        col_cta = (int(100 + 155 * pulso), int(220 + 35 * pulso), 255)
        surf_cta = self.fuente_tit.render(">>> PRESIONA ESPACIO O CLIC PARA JUGAR <<<", True, col_cta)
        self.pantalla.blit(surf_cta, surf_cta.get_rect(center=(ANCHO // 2, 575)))

        if self.puntuacion_maxima > 0:
            txt_rec = self.fuente_mono.render(f"RÉCORD ACTUAL: {self.puntuacion_maxima:06d} PUNTOS", True, COLOR_AMARILLO)
            self.pantalla.blit(txt_rec, txt_rec.get_rect(center=(ANCHO // 2, 630)))

    def dibujar_overlay_pausa(self):
        # Cortina oscura translúcida
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((10, 14, 25, 180))
        self.pantalla.blit(overlay, (0, 0))

        # Cuadro de pausa
        caja = pygame.Rect(ANCHO // 2 - 200, ALTO // 2 - 120, 400, 240)
        pygame.draw.rect(self.pantalla, (24, 30, 48), caja, border_radius=12)
        pygame.draw.rect(self.pantalla, COLOR_CIAN, caja, width=2, border_radius=12)

        txt_p = self.fuente_logo.render("PAUSA", True, (255, 255, 255))
        self.pantalla.blit(txt_p, txt_p.get_rect(center=(ANCHO // 2, ALTO // 2 - 60)))

        opciones = [
            "[P] o [ESC]: Continuar batalla",
            "[R]: Reiniciar partida desde cero",
            "[M]: Salir al Menú Principal",
        ]
        for i, op in enumerate(opciones):
            s_op = self.fuente_sub.render(op, True, (200, 220, 245))
            self.pantalla.blit(s_op, s_op.get_rect(center=(ANCHO // 2, ALTO // 2 + 15 + i * 32)))

    def dibujar_pantalla_gameover(self):
        # Partículas de la explosión final continúan dibujándose
        self.grupo_particulas.draw(self.pantalla)

        # Cortina
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((20, 10, 15, 200))
        self.pantalla.blit(overlay, (0, 0))

        # Letrero Game Over
        surf_go = self.fuente_logo.render("GAME OVER", True, COLOR_ROJO)
        self.pantalla.blit(surf_go, surf_go.get_rect(center=(ANCHO // 2, 170)))

        # Tarjeta de Estadísticas
        caja = pygame.Rect(ANCHO // 2 - 220, 240, 440, 240)
        pygame.draw.rect(self.pantalla, (26, 22, 34), caja, border_radius=12)
        pygame.draw.rect(self.pantalla, (90, 40, 60), caja, width=2, border_radius=12)

        stats = [
            f"Puntuación Obtenida:    {self.puntuacion:06d}",
            f"Puntuación Máxima:      {self.puntuacion_maxima:06d}",
            f"Oleada Alcanzada:       Nivel {self.oleada}",
            f"Enemigos Eliminados:    {self.enemigos_totales_destruidos}",
        ]
        for i, st in enumerate(stats):
            col = COLOR_AMARILLO if "Máxima" in st else (235, 235, 245)
            s_st = self.fuente_sub.render(st, True, col)
            self.pantalla.blit(s_st, (caja.x + 35, caja.y + 35 + i * 44))

        # Botones de reinicio
        surf_btn = self.fuente_tit.render("[R] o [ESPACIO]: JUGAR DE NUEVO", True, COLOR_VERDE)
        self.pantalla.blit(surf_btn, surf_btn.get_rect(center=(ANCHO // 2, 530)))

        surf_menu = self.fuente_sub.render("[M]: Volver al Menú Principal   |   [ESC]: Salir", True, (170, 185, 210))
        self.pantalla.blit(surf_menu, surf_menu.get_rect(center=(ANCHO // 2, 580)))

# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    juego = VideojuegoCosmicDefender()
    juego.ejecutar()
