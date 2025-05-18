import sys
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)


class Game:
    def __init__(self):
        pygame.init()


        self.volume = 0.5  # volumen inicial (50%)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)


        pygame.display.set_caption('Guardians Of The Planet')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('data/Fonts/static/Oswald-Medium.ttf', 40)

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        self.menu_assets = {
            'background': pygame.image.load('data/images/menu_backgrounds/primero.png'),
            'titulo': pygame.image.load('data/images/menu_backgrounds/titulo.png'),
            'boton_jugar': pygame.image.load('data/images/menu_backgrounds/jugar.png'),
            'boton_tienda': pygame.image.load('data/images/menu_backgrounds/tienda.png'),
            'boton_creditos': pygame.image.load('data/images/menu_backgrounds/creditos.png'),
            'boton_salir': pygame.image.load('data/images/menu_backgrounds/salir.png'),
            'icono_config': pygame.image.load('data/images/menu_backgrounds/configuracion.png'),
            'signo_mas': pygame.transform.scale(
                pygame.image.load('data/images/menu_backgrounds/mas.png'), (70, 70)),
            'volumen_titulo': pygame.transform.scale(
                pygame.image.load('data/images/menu_backgrounds/volumen.png'), (420, 370)),
            'signo_menos': pygame.transform.scale(
                pygame.image.load('data/images/menu_backgrounds/menos.png'), (70, 70))
        }

        # Escalamos las imágenes del menú
        self.menu_assets['background'] = pygame.transform.smoothscale(
            self.menu_assets['background'], (640, 480))
        self.menu_assets['titulo'] = pygame.transform.scale(
            self.menu_assets['titulo'], (600, 430))
        self.menu_assets['boton_jugar'] = pygame.transform.scale(
            self.menu_assets['boton_jugar'], (132, 70))
        self.menu_assets['boton_tienda'] = pygame.transform.scale(
            self.menu_assets['boton_tienda'], (132, 70))
        self.menu_assets['boton_creditos'] = pygame.transform.scale(
            self.menu_assets['boton_creditos'], (132, 70))
        self.menu_assets['boton_salir'] = pygame.transform.scale(
            self.menu_assets['boton_salir'], (120, 70))
        self.menu_assets['icono_config'] = pygame.transform.scale(
            self.menu_assets['icono_config'], (80, 70))

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        # Camara para el videojuego
        self.scroll = [0, 0]

    def main_menu(self):

        pygame.mixer.music.load('data/music.wav')  # Ruta a el archivo de música
        pygame.mixer.music.play(-1)  # -1 significa que se reproduce en bucle infinito

        background = self.menu_assets['background'] 
        ancho = 640

        # Botones con su propio rectángulo (posición + tamaño independiente de la imagen)
        play_button = Button(73, 402, 110, 27)
        store_button = Button(220, 402, 110, 27)
        credits_button = Button(367, 402, 119, 27)
        quit_button = Button(525, 403, 90, 27)
        icono_configuracion = Button(568, 32, 47, 47)

        i = 0  # Variable para el movimiento del fondo

        while True:
            i -= 1  # mueve el fondo 1 píxel hacia la izquierda cada frame
            if i <= -ancho:
                i = 0  # reinicia el loop

            # Dibuja dos fondos seguidos para loop continuo
            self.screen.blit(background, (i, 0))
            self.screen.blit(background, (i + ancho, 0))

            self.screen.blit(self.menu_assets['titulo'], (20, 10))  # Se pone el título en la posición correcta

            # Se ponen las imagenes de los botones en la posición correcta
            self.screen.blit(self.menu_assets['boton_jugar'], (60, 380))
            self.screen.blit(self.menu_assets['boton_tienda'], (210, 380))
            self.screen.blit(self.menu_assets['boton_creditos'], (360, 380))
            self.screen.blit(self.menu_assets['boton_salir'], (510, 380))
            self.screen.blit(self.menu_assets['icono_config'], (550, 20))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if play_button.is_clicked(event):
                    pygame.mixer.music.stop()
                    return
                if store_button.is_clicked(event):
                    self.tienda_menu()
                if credits_button.is_clicked(event):
                    print("Mostrar créditos")
                if quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()
                if icono_configuracion.is_clicked(event):
                    self.configuracion_menu()

            pygame.display.update()
            self.clock.tick(60)

    def configuracion_menu(self):

        volver_img = pygame.transform.scale(pygame.image.load("data/images/menu_backgrounds/volveralmenu.png"), (300, 200))
        aumentar = Button(390, 205, 52, 60)
        disminuir = Button(190, 220, 52, 30)
        volver = Button(195, 310, 250, 80)

        while True:
            self.screen.blit(self.menu_assets['background'], (0, 0))

            self.screen.blit(self.menu_assets['volumen_titulo'], (110, -100))  # Posición del título de volumen
            
            # Dibujar imagen de volver al menú
            self.screen.blit(volver_img, (170, 250)) 

            self.screen.blit(self.menu_assets['signo_mas'], (380, 200))
            self.screen.blit(self.menu_assets['signo_menos'], (180, 200))
            
            # Mostrar el volumen como porcentaje
            volumen_texto = self.font.render(f'{int(self.volume * 100)}%', True, (240, 180, 35))
            self.screen.blit(volumen_texto, (282, 210))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if aumentar.is_clicked(event):
                    self.volume = min(1.0, self.volume + 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                if disminuir.is_clicked(event):
                    self.volume = max(0.0, self.volume - 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                if volver.is_clicked(event):
                    return

            pygame.display.update()
            self.clock.tick(60)
    def run(self):

        while True:
            self.display.blit(self.assets['background'], (0, 0))

            # Movimiento de la cámara directamente al jugador

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
    def tienda_menu(self):
            volver_img = pygame.transform.scale(
                pygame.image.load("data/images/menu_backgrounds/volveralmenu.png"), (300, 200))
            volver = Button(195, 310, 250, 80)

            # Texto de ejemplo para los productos
            skins = [
                {"nombre": "Ninja Verde", "pos": (100, 100)},
                {"nombre": "Ninja Azul", "pos": (400, 100)},
                {"nombre": "Ninja Naranja", "pos": (100, 220)},
                {"nombre": "Ninja Original", "pos": (400, 220)},
            ]

            while True:
                self.screen.blit(self.menu_assets['background'], (0, 0))

                titulo = self.font.render("TIENDA", True, (255, 255, 255))
                self.screen.blit(titulo, (240, 30))

                # Dibujar skins (nombre solamente por ahora faltan las skins)
                for producto in skins:
                    texto = self.font.render(producto["nombre"], True, (240, 180, 35))
                    self.screen.blit(texto, producto["pos"])

                self.screen.blit(volver_img, (170, 250))  # Imagen del botón volver

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if volver.is_clicked(event):
                        return

                pygame.display.update()
                self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.main_menu()  # Mostrar menú antes de iniciar el juego
    game.run()