import pygame
import sys
import subprocess

pygame.init()
ANCHO = 800
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal")

font = pygame.font.SysFont(None, 50)
opciones = ["Jugar", "Instrucciones", "Seleccionar personaje", "Opciones", "Usuario", "Ver puntajes", "Salir"]
seleccion = 0

logo = pygame.image.load("src/Imagenes/logo.png")
logo = pygame.transform.scale(logo, (ANCHO, ALTO))  
def dibujar_menu():
    pantalla.blit(logo, (0, 0)) 

    for i, texto in enumerate(opciones):
        color =  (255, 165, 0) if i == seleccion else (0, 0, 0) 
        render = font.render(texto, True, color)
        rect = render.get_rect(center=(ANCHO // 2, 350 + i * 50))
        pantalla.blit(render, rect)
    pygame.display.flip()

def comojugar():   

    fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(160) 
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))

    font_info = pygame.font.SysFont(None, 40)
    instrucciones = [
        "Instrucciones:",
        "1. Usa las flechas para moverte.",
        "2. Recoge llaves y evita las paredes.",
        "3. Llega al objetivo para ganar.",
        "4. Presiona ESC para volver al menú.",
        "5. Puedes jugar como agente presionando 'A'",
    ]
    for i, linea in enumerate(instrucciones):
        render = font_info.render(linea, True, (255, 255, 255))
        pantalla.blit(render, (50, 300 + i * 40))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    esperando = False

def seleccionar_personaje():
    personajes = [
        "src/Imagenes/jugador1.png",
        "src/Imagenes/jugador2.png",
        "src/Imagenes/jugador3.png"
    ]
    nombres = ["Personaje 1", "Personaje 2", "Personaje 3"]
    seleccion = 0
    font = pygame.font.SysFont(None, 48)
    eligiendo = True
    espacio_x = 220
    x_inicial = 60
    y_img = 120
    y_texto = y_img + 170

    while eligiendo:
        # Fondo con logo y overlay oscuro
        fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))

        for i, ruta in enumerate(personajes):
            img = pygame.image.load(ruta)
            img = pygame.transform.scale(img, (140, 140))
            x = x_inicial + i * espacio_x
            pantalla.blit(img, (x, y_img))
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto = font.render(nombres[i], True, color)
            texto_rect = texto.get_rect(center=(x + 70, y_texto))
            pantalla.blit(texto, texto_rect)
        texto_info = font.render("Presiona enter para elegir", True, (200, 200, 200))
        pantalla.blit(texto_info, (ANCHO // 2 - texto_info.get_width() // 2, 400))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    seleccion = (seleccion - 1) % len(personajes)
                elif evento.key == pygame.K_RIGHT:
                    seleccion = (seleccion + 1) % len(personajes)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    with open("src/personaje_seleccionado.txt", "w") as f:
                        f.write(personajes[seleccion])
                    eligiendo = False
                elif evento.key == pygame.K_ESCAPE:
                    eligiendo = False

def configurar_opciones():
    # Intenta leer valores previos
    global TIEMPO_LIMITE, NUM_Llaves
    try:
        with open("src/opciones_config.txt") as f:
            lineas = f.readlines()
            TIEMPO_LIMITE = int(lineas[0].strip())
            NUM_Llaves = int(lineas[1].strip())
    except:
        TIEMPO_LIMITE = 60
        NUM_Llaves = 3

    seleccion = 0
    opciones_conf = ["Tiempo límite", "Número de llaves", "Volver"]
    font = pygame.font.SysFont(None, 48)
    configurando = True
    while configurando:
        # Fondo con logo y overlay oscuro
        fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))

        for i, texto in enumerate(opciones_conf):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            if i == 0:
                txt = f"{texto}: {TIEMPO_LIMITE} s"
            elif i == 1:
                txt = f"{texto}: {NUM_Llaves}"
            else:
                txt = texto
            render = font.render(txt, True, color)
            pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, 200 + i * 60))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_conf)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_conf)
                elif evento.key == pygame.K_LEFT:
                    if seleccion == 0 and TIEMPO_LIMITE > 10:
                        TIEMPO_LIMITE -= 5
                    elif seleccion == 1 and NUM_Llaves > 1:
                        NUM_Llaves -= 1
                elif evento.key == pygame.K_RIGHT:
                    if seleccion == 0:
                        TIEMPO_LIMITE += 5
                    elif seleccion == 1:
                        NUM_Llaves += 1
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if seleccion == 2:
                        # Guarda las opciones en un archivo para usarlas en juego.py
                        with open("src/opciones_config.txt", "w") as f:
                            f.write(f"{TIEMPO_LIMITE}\n{NUM_Llaves}\n")
                        configurando = False
                elif evento.key == pygame.K_ESCAPE:
                    configurando = False

def ingresar_usuario():
    global usuario_actual
    usuario_actual = ""
    font = pygame.font.SysFont(None, 48)
    escribiendo = True
    while escribiendo:
        # Fondo con logo y overlay oscuro
        fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))

        texto = font.render("Ingresa tu nombre de usuario:", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200))
        texto_usuario = font.render(usuario_actual + "|", True, (255, 255, 0))
        pantalla.blit(texto_usuario, (ANCHO // 2 - texto_usuario.get_width() // 2, 300))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if usuario_actual.strip() != "":
                        with open("src/usuario_actual.txt", "w") as f:
                            f.write(usuario_actual.strip())
                        escribiendo = False
                elif evento.key == pygame.K_ESCAPE:
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    usuario_actual = usuario_actual[:-1]
                else:
                    if len(usuario_actual) < 16 and evento.unicode.isprintable():
                        usuario_actual += evento.unicode

def ver_puntajes():
    font = pygame.font.SysFont(None, 36)
    try:
        with open("src/puntajes.txt") as f:
            lineas = f.readlines()
    except:
        lineas = []
    viendo = True
    while viendo:
        fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))

        encabezado = font.render("USUARIO    TIEMPO    PUNTAJE    ESTADO    LLAVES", True, (255, 255, 0))
        pantalla.blit(encabezado, (40, 60))

        for i, linea in enumerate(lineas[-10:]):
            render = font.render(linea.strip(), True, (255, 255, 255))
            pantalla.blit(render, (40, 100 + i * 35))
        texto_info = font.render("Presiona ESC para volver", True, (200, 200, 200))
        pantalla.blit(texto_info, (ANCHO // 2 - texto_info.get_width() // 2, ALTO - 50))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    viendo = False

corriendo = True
while corriendo:
    dibujar_menu()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(opciones)
            elif evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(opciones)
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                if seleccion == 0:
                    pygame.quit()
                    subprocess.call([sys.executable, "src/juego.py"])
                    sys.exit()
                elif seleccion == 1:
                    comojugar()
                elif seleccion == 2:    
                    seleccionar_personaje()
                elif seleccion == 3:
                    configurar_opciones()
                elif seleccion == 4:
                    ingresar_usuario()
                elif seleccion == 5:
                    ver_puntajes()
                elif seleccion == 6:
                    corriendo = False
pygame.quit()
sys.exit()