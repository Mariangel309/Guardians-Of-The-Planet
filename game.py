import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pass

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Ninja Game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]


        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds')
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)


        #Camara para el videojuego
        self.scroll = [0, 0]

    def main_menu(self):
        background = pygame.image.load('data/images/background main menu/background1.png').convert()
        background = pygame.transform.scale(background, (640, 480))

        play_button = Button(48, 420, 132, 30)
        store_button = Button(194, 420, 132, 30)
        credits_button = Button(340, 420, 132, 30)
        quit_button = Button(486, 420, 120, 30)

        while True:
            self.screen.blit(background, (0, 0))

            play_button.draw(self.screen)
            store_button.draw(self.screen)
            credits_button.draw(self.screen)
            quit_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if play_button.is_clicked(event):
                    return  # Salir del menú e iniciar el juego
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
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            #Movimiento de la cámara directamente al jugador

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.main_menu()  # Mostrar menú antes de iniciar el juego
    game.run()

