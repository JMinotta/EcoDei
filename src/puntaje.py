import pygame
import sys
import subprocess

logo = pygame.image.load("src/Imagenes/fondo.png")
pygame.display.set_caption("Puntaje")

def mostrar_puntaje(tiempo, puntaje, gano):
    pygame.init()
    info = pygame.display.Info()
    ANCHO, ALTO = info.current_w, info.current_h
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Resultado")

    # Fondo con logo y overlay oscuro
    fondo = pygame.transform.scale(logo, (ANCHO, ALTO))
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))

    font_titulo = pygame.font.SysFont(None, 80)
    font_info = pygame.font.SysFont(None, 56)
    font_opcion = pygame.font.SysFont(None, 48)

    if gano:
        titulo = font_titulo.render("¡Ganaste!", True, (0, 255, 0))
    else:
        titulo = font_titulo.render("Perdiste", True, (255, 0, 0))

    texto_tiempo = font_info.render(f"Tiempo: {tiempo} s", True, (255, 255, 255))
    texto_puntaje = font_info.render(f"Puntaje: {puntaje}", True, (255, 255, 0))

    opciones = ["Volver al menú", "Volver a jugar", 'Salir del juego']
    seleccion = 0

    corriendo = True
    while corriendo:
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(overlay, (0, 0))

        centro_x = ANCHO // 2
        centro_y = ALTO // 2

        pantalla.blit(titulo, titulo.get_rect(center=(centro_x, centro_y - 120)))
        pantalla.blit(texto_tiempo, texto_tiempo.get_rect(center=(centro_x, centro_y - 50)))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=(centro_x, centro_y)))

        # Opciones de menú centradas
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            render = font_opcion.render(opcion, True, color)
            pantalla.blit(render, render.get_rect(center=(centro_x, centro_y + 120 + i*55)))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if seleccion == 0:
                        pygame.quit()
                        subprocess.call([sys.executable, "src/menu.py"])
                        sys.exit()
                    elif seleccion == 1:
                        pygame.quit()
                        subprocess.call([sys.executable, "src/juego.py"])
                        sys.exit()
                    elif seleccion == 2:
                        pygame.quit()
                        sys.exit()