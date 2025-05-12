import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity

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

    def run(self):
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