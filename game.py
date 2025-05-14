import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity

class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pass # no dibuja nada
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game:
    def __init__(self):
        pygame.init() #Función que inicializa todos los módulos de Pygame que necesitan ser activados antes de usarlos

        pygame.display.set_caption('Ninja Game')
        #pygame.display es el módulo que controla la pantalla o ventana principal del juego

        self.screen = pygame.display.set_mode((640, 480)) #Creación de la ventana del juego con dimensiones (ancho, alto)

        self.clock = pygame.time.Clock() #Esta es una herramienta que se usa para controlar la velocidad del juego, i.e. cuantas veces por segundo se actualiza la pantalla (frames per second FPS)
        
        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'), 
            'decor': load_images('tiles/decor'),
            'decor': load_images('tiles/decor'),
            'decor': load_images('tiles/decor'),
            'player': load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (16, 26))

    def main_menu(self):
        background = pygame.image.load('data/images/background main menu/background1.png').convert()
        background = pygame.transform.scale(background, (640, 480))  # Ajustar al tamaño de la ventana

        # Crear botones con texto más pequeño
        play_button = Button(48, 420, 132, 30)
        store_button = Button(194, 420, 132, 30)
        credits_button = Button(340, 420, 132, 30)
        quit_button = Button(486, 420, 120, 30)

        while True:
            self.screen.blit(background, (0, 0))  # Fondo del menú


            # Dibujar botones
            play_button.draw(self.screen)
            store_button.draw(self.screen)
            credits_button.draw(self.screen)
            quit_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if play_button.is_clicked(event):
                    return  # Iniciar juego
                if store_button.is_clicked(event):
                    print("Abrir tienda")
                if credits_button.is_clicked(event):
                    print("Mostrar créditos")
                if quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.main_menu()  # Llamamos al menú principal antes de iniciar el juego
        while True: #Este es un bucle infinito que se repite una y otra vez, esto para actualizar y dibujar todo
            self.screen.fill((14, 219, 248))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.screen)


            for event in pygame.event.get(): #Detecta las entradas del usuario
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #Cierra la app cuando el usuario presione la X de cerrar
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            pygame.display.update()
            self.clock.tick(60)  #60 repeticiones por segundo

Game().run()