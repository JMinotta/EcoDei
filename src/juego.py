import pygame
import sys
import random
import numpy as np
from puntaje import mostrar_puntaje
import os
import subprocess

pygame.init()

# Música de fondo
pygame.mixer.init()
pygame.mixer.music.load("src/sonido/musica_fondo.mp3")  # Cambia la ruta y nombre según tu archivo
pygame.mixer.music.set_volume(0.5)  # Volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 para que se repita indefinidamente

# Tamaño de cada bloque
TAM_BLOQUE = 32
FILAS = 21
COLUMNAS = 31
FRANJA_SUPERIOR = 60

ANCHO_PANTALLA = COLUMNAS * TAM_BLOQUE
ALTO_PANTALLA = FILAS * TAM_BLOQUE + FRANJA_SUPERIOR
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego del Laberinto")

# Cargar imágenes
def cargar_imagen(ruta, ancho=TAM_BLOQUE, alto=TAM_BLOQUE):
    img = pygame.image.load(ruta)
    return pygame.transform.scale(img, (ancho, alto))

img_pared = cargar_imagen("src/Imagenes/muro.png")
img_camino = cargar_imagen("src/Imagenes/suelo.png")
ruta_personaje = "src/Imagenes/jugador.png"
if os.path.exists("src/personaje_seleccionado.txt"):
    with open("src/personaje_seleccionado.txt") as f:
        ruta_personaje = f.read().strip()
img_jugador = cargar_imagen(ruta_personaje, TAM_BLOQUE+8, TAM_BLOQUE+8)
img_objetivo = cargar_imagen("src/Imagenes/objetivo.png")
img_llave = cargar_imagen("src/Imagenes/llave.png")

# Generar laberinto
def generar_laberinto(filas, columnas):
    lab = [[1 for _ in range(columnas)] for _ in range(filas)]
    def en_rango(x, y): return 0 <= x < columnas and 0 <= y < filas
    def dfs(x, y):
        lab[y][x] = 0
        dirs = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if en_rango(nx, ny) and lab[ny][nx] == 1:
                lab[y + dy // 2][x + dx // 2] = 0
                dfs(nx, ny)
    inicio_x = random.randrange(1, columnas, 2)
    inicio_y = random.randrange(1, filas, 2)
    dfs(inicio_x, inicio_y)
    return lab

laberinto = generar_laberinto(FILAS, COLUMNAS)

def estado_valido(x, y):
    return 0 <= x < COLUMNAS and 0 <= y < FILAS and laberinto[y][x] == 0

def posicion_aleatoria_valida():
    while True:
        x = random.randint(1, COLUMNAS - 2)
        y = random.randint(1, FILAS - 2)
        if laberinto[y][x] == 0:
            return x, y

objetivo_x, objetivo_y = posicion_aleatoria_valida()

EPISODIOS = 10000
epsilon = 0.3
alpha = 0.1
gamma = 0.9
ACTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
Q = np.zeros((FILAS, COLUMNAS, len(ACTIONS)))

# Mostrar "Cargando..."
pantalla.fill((0, 0, 0))
font_cargando = pygame.font.SysFont(None, 72)
texto_cargando = font_cargando.render("Entrenando agente... Por favor espera", True, (255, 255, 255))
rect_texto = texto_cargando.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
pantalla.blit(texto_cargando, rect_texto)
pygame.display.flip()

def entrenar_agente():
    for episodio in range(EPISODIOS):
        x, y = posicion_aleatoria_valida()
        while (x, y) == (objetivo_x, objetivo_y):
            x, y = posicion_aleatoria_valida()
        for paso in range(300):
            if np.random.rand() < epsilon:
                a = np.random.randint(0, len(ACTIONS))
            else:
                a = np.argmax(Q[y, x])
            dx, dy = ACTIONS[a]
            nx, ny = x + dx, y + dy
            if not estado_valido(nx, ny):
                recompensa = -10
                nx, ny = x, y
            elif (nx, ny) == (objetivo_x, objetivo_y):
                recompensa = 100
            else:
                recompensa = -1
            Q[y, x, a] += alpha * (recompensa + gamma * np.max(Q[ny, nx]) - Q[y, x, a])
            x, y = nx, ny
            if (x, y) == (objetivo_x, objetivo_y):
                break

entrenar_agente()

jugador_x, jugador_y = posicion_aleatoria_valida()
jugando = True
clock = pygame.time.Clock()
modo_agente = False

# Leer configuración de opciones
TIEMPO_LIMITE = 60
NUM_Llaves = 3
try:
    with open("src/opciones_config.txt") as f:
        lineas = f.readlines()
        TIEMPO_LIMITE = int(lineas[0].strip())
        NUM_Llaves = int(lineas[1].strip())
except:
    print("Error leyendo opciones_config.txt, usando valores por defecto.")

def posiciones_llaves(n=3):
    llaves = set()
    while len(llaves) < n:
        x, y = posicion_aleatoria_valida()
        if (x, y) != (objetivo_x, objetivo_y):
            llaves.add((x, y))
    return list(llaves)

llaves_pos = posiciones_llaves(NUM_Llaves)
llaves_recogidas = set()

def guardar_puntaje(usuario, tiempo, puntaje, gano, llaves, total_llaves):
    with open("src/puntajes.txt", "a") as f:
        f.write(f"{usuario}            {tiempo}            {puntaje}            {'GANADOR' if gano else 'PERDEDOR'}            {llaves}/{total_llaves}\n")

# Antes de mostrar el puntaje, lee el usuario:
usuario = "Anonimo"
try:
    with open("src/usuario_actual.txt") as f:
        usuario = f.read().strip()
except:
    pass

while jugando:
    pantalla.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                subprocess.call([sys.executable, "src/menu.py"])
                sys.exit()
            elif evento.key == pygame.K_a:
                modo_agente = not modo_agente
            if not modo_agente:
                if evento.key == pygame.K_UP and estado_valido(jugador_x, jugador_y - 1):
                    jugador_y -= 1
                elif evento.key == pygame.K_DOWN and estado_valido(jugador_x, jugador_y + 1):
                    jugador_y += 1
                elif evento.key == pygame.K_LEFT and estado_valido(jugador_x - 1, jugador_y):
                    jugador_x -= 1
                elif evento.key == pygame.K_RIGHT and estado_valido(jugador_x + 1, jugador_y):
                    jugador_x += 1

    if modo_agente and (jugador_x, jugador_y) != (objetivo_x, objetivo_y):
        a = np.argmax(Q[jugador_y, jugador_x])
        dx, dy = ACTIONS[a]
        nx, ny = jugador_x + dx, jugador_y + dy
        if estado_valido(nx, ny):
            jugador_x, jugador_y = nx, ny

    if (jugador_x, jugador_y) in llaves_pos and (jugador_x, jugador_y) not in llaves_recogidas:
        llaves_recogidas.add((jugador_x, jugador_y))

    if 'tiempo_inicio' not in locals():
        tiempo_inicio = pygame.time.get_ticks()
    tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000

    puntuacion = max(0, TIEMPO_LIMITE - tiempo_actual)
    puntuacion += len(llaves_recogidas) * 10

    font = pygame.font.SysFont(None, 48)
    texto_tiempo = font.render(f"Tiempo: {tiempo_actual}s", True, (255, 255, 255))
    texto_puntos = font.render(f"Puntos: {puntuacion}", True, (255, 255, 0))
    texto_llaves = font.render(f"Llaves: {len(llaves_recogidas)}/{NUM_Llaves}", True, (0, 255, 255))

    pantalla.blit(texto_tiempo, (20, 10))
    pantalla.blit(texto_puntos, (ANCHO_PANTALLA // 2 - texto_puntos.get_width() // 2, 10))
    pantalla.blit(texto_llaves, (ANCHO_PANTALLA - texto_llaves.get_width() - 20, 10))

    for y in range(FILAS):
        for x in range(COLUMNAS):
            pos_y = y * TAM_BLOQUE + FRANJA_SUPERIOR
            if laberinto[y][x] == 1:
                pantalla.blit(img_pared, (x*TAM_BLOQUE, pos_y))
            else:
                pantalla.blit(img_camino, (x*TAM_BLOQUE, pos_y))

    for (lx, ly) in llaves_pos:
        if (lx, ly) not in llaves_recogidas:
            pantalla.blit(img_llave, (lx*TAM_BLOQUE, ly*TAM_BLOQUE + FRANJA_SUPERIOR))

    pantalla.blit(img_objetivo, (objetivo_x*TAM_BLOQUE, objetivo_y*TAM_BLOQUE + FRANJA_SUPERIOR))
    pantalla.blit(img_jugador, (jugador_x*TAM_BLOQUE, jugador_y*TAM_BLOQUE + FRANJA_SUPERIOR))

    if tiempo_actual >= TIEMPO_LIMITE:
        guardar_puntaje(usuario, tiempo_actual, puntuacion, False, len(llaves_recogidas), NUM_Llaves)
        mostrar_puntaje(tiempo_actual, puntuacion, gano=False)
        jugando = False
    if (jugador_x, jugador_y) == (objetivo_x, objetivo_y):
        if len(llaves_recogidas) == NUM_Llaves:
            guardar_puntaje(usuario, tiempo_actual, puntuacion, True, len(llaves_recogidas), NUM_Llaves)
            mostrar_puntaje(tiempo_actual, puntuacion, gano=True)
            jugando = False
        else:
            font_alerta = pygame.font.SysFont(None, 36)
            pantalla.blit(font_alerta.render(f"¡Necesitas las {NUM_Llaves} llaves!", True, (255, 0, 0)), (ANCHO_PANTALLA//2 - 120, 40))

    pygame.display.flip()
    clock.tick(15)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
