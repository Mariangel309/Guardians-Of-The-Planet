import os
import sys
import math
import random
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark


class Button:
    def __init__(self, x, y, width, height):
        # Crea un rectángulo que representa el botón
        self.rect = pygame.Rect(x, y, width, height)

    def is_clicked(self, event):
        # Verifica si el evento es un clic del mouse y si el clic está dentro del rectángulo del botón
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        pass # Aquí puedes dibujar el botón si lo deseas, pero en este caso no es necesario

# Clase principal del juego
class Game:
    def __init__(self):
        pygame.init() # Inicializa Pygame

        self.enemigos_derrotados = 0
        self.total_enemigos = 0

        self.pixel_font = pygame.font.Font('data/Fonts/pixel_font.ttf', 12)

        # Carga de música y efectos de sonido
        self.sonido_boton = pygame.mixer.Sound('data/sfx/boton.mp3')  # Ruta a el archivo de música

        self.volume = 0.5  # volumen inicial (50%)
        pygame.mixer.init() # Inicializa el mezclador de Pygame
        pygame.mixer.music.set_volume(self.volume) # Establece el volumen  de la música

        # Inicializa la pantalla
        pygame.display.set_caption('Guardians Of The Planet') # Título de la ventana
        self.screen = pygame.display.set_mode((640, 480)) # Tamaño de la ventana
        self.display = pygame.Surface((320, 240)) # Pantalla de juego

        self.clock = pygame.time.Clock() # Reloj para controlar la velocidad de fotogramas

        self.font = pygame.font.Font('data/Fonts/static/Oswald-Medium.ttf', 40) # Carga la fuente
        
        self.movement = [False, False] # Inicializa el movimiento del jugador (izquierda y derecha)

        # Carga de imágenes y animaciones

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'enemy/hurt': Animation(load_images('entities/enemy/hurt'), img_dur=4, loop=False),
            'enemy1/idle': Animation(load_images('entities/enemy1/idle'), img_dur=6),
            'enemy1/run': Animation(load_images('entities/enemy1/run'), img_dur=4),
            'enemy1/hurt': Animation(load_images('entities/enemy1/hurt'), img_dur=4, loop=False),
            'enemy2/idle': Animation(load_images('entities/enemy2/idle'), img_dur=6),
            'enemy2/run': Animation(load_images('entities/enemy2/run'), img_dur=4),
            'enemy2/hurt': Animation(load_images('entities/enemy2/hurt'), img_dur=4, loop=False),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'player/idle':  Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump':  Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide':  Animation(load_images('entities/player/wall_slide')),
            'skin1/idle':   Animation(load_images('entities/skin/skin1/idle'), img_dur=6),
            'skin1/run': Animation(load_images('entities/skin/skin1/run'), img_dur=4),
            'skin1/jump': Animation(load_images('entities/skin/skin1/jump')),
            'skin1/slide': Animation(load_images('entities/skin/skin1/slide')),
            'skin1/wall_slide': Animation(load_images('entities/skin/skin1/wall_slide')),
            'skin2/idle':Animation(load_images('entities/skin/skin2/idle'), img_dur=6),
            'skin2/run':  Animation(load_images('entities/skin/skin2/run'), img_dur=4),
            'skin2/jump': Animation(load_images('entities/skin/skin2/jump')),
            'skin2/slide': Animation(load_images('entities/skin/skin2/slide')),
            'skin2/wall_slide': Animation(load_images('entities/skin/skin2/wall_slide')),

            
        }

        self.level = 0

        self.backgrounds = {
            0: pygame.image.load('data/images/backgrounds/background_0.png').convert(),
            1: pygame.image.load('data/images/backgrounds/background_1.png').convert(),
            2: pygame.image.load('data/images/backgrounds/background_2.png').convert(),
        }

        for key in self.backgrounds:
            self.backgrounds[key] = pygame.transform.scale(self.backgrounds[key], self.display.get_size())
        self.current_background = self.backgrounds[self.level]
        self.prev_background = self.current_background
        self.background_alpha = 255

        # Carga de imágenes del menú
        self.menu_assets = {
            'background': pygame.image.load('data/images/menu_backgrounds/primero.png'),
            'titulo': pygame.image.load('data/images/menu_backgrounds/titulo.png'),
            'boton_jugar': pygame.image.load('data/images/menu_backgrounds/jugar.png'),
            'boton_tienda': pygame.image.load('data/images/menu_backgrounds/tienda.png'),
            'boton_creditos': pygame.image.load('data/images/menu_backgrounds/creditos.png'),
            'boton_salir': pygame.image.load('data/images/menu_backgrounds/salir.png'),
            'icono_config': pygame.image.load('data/images/menu_backgrounds/configuracion.png'),
            'signo_mas': pygame.transform.scale(pygame.image.load('data/images/menu_backgrounds/mas.png'), (70, 70)),
            'volumen_titulo': pygame.transform.scale(pygame.image.load('data/images/menu_backgrounds/volumen.png'), (420, 370)),
            'signo_menos': pygame.transform.scale(pygame.image.load('data/images/menu_backgrounds/menos.png'), (70, 70)),
            'tienda_titulo': pygame.transform.scale(pygame.image.load('data/images/menu_backgrounds/Tienda_titulo.png'), (420, 370)),
            'game_over': pygame.transform.scale(pygame.image.load('data/images/menu_backgrounds/gameover1.png'), (520, 460))
        }

        # Escalamos las imágenes del menú
        self.menu_assets['background'] = pygame.transform.smoothscale(self.menu_assets['background'], (640, 480))
        self.menu_assets['titulo'] = pygame.transform.scale(self.menu_assets['titulo'], (600, 430))
        self.menu_assets['boton_jugar'] = pygame.transform.scale(self.menu_assets['boton_jugar'], (132, 70))
        self.menu_assets['boton_tienda'] = pygame.transform.scale(self.menu_assets['boton_tienda'], (132, 70))
        self.menu_assets['boton_creditos'] = pygame.transform.scale(self.menu_assets['boton_creditos'], (132, 70))
        self.menu_assets['boton_salir'] = pygame.transform.scale(self.menu_assets['boton_salir'], (120, 70))
        self.menu_assets['icono_config'] = pygame.transform.scale(self.menu_assets['icono_config'], (80, 70))

        self.heart_img = pygame.image.load('data/images/souls/corazon.png').convert_alpha()# Carga la imagen del corazón
        self.heart_img = pygame.transform.scale(self.heart_img, (24, 24))# Escala la imagen del corazón

        # Crea las nubes decorativas del fondo
        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.enemy_icon = pygame.image.load('data/images/ui/enemy_icon.png').convert_alpha()

        # Crea el jugador
        self.player = Player(self, (50,50), (8, 15))
        
        # Carga el mapa
        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 0
        self.load_level(self.level)

        self.screenshake = 0

        self.sonido_dash = pygame.mixer.Sound('data/sfx/dash.wav')
        self.sonido_dash.set_volume(0.1)

        self.sonido_saltar = pygame.mixer.Sound('data/sfx/jump.wav')
        self.sonido_saltar.set_volume(0.42)

        self.sonido_golpe_enemigo = pygame.mixer.Sound('data/sfx/hit.wav')
        self.sonido_golpe_enemigo.set_volume(0.32)

        self.musicadefondo = pygame.mixer.Sound('data/sfx/musicadefondo.ogg')
        self.musicadefondo.set_volume(0.32)        

        self.sonidodemuerte = pygame.mixer.Sound('data/sfx/death.wav')
        self.sonidodemuerte.set_volume(1)     

        self.corriendo = pygame.mixer.Sound('data/sfx/corriendo.mp3')
        self.corriendo.set_volume(0.62)     

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        enemy_spawners = [s for s in self.tilemap.extract([('spawners', 1)])]
        if self.level == 2:
            if len(enemy_spawners) >= 15:
                step = len(enemy_spawners) // 15
                enemy_spawners = [enemy_spawners[i] for i in range(0, len(enemy_spawners), step)][:15]
            else:
                enemy_spawners = enemy_spawners
        enemy_type = 'enemy'
        if self.level == 1:
            enemy_type = 'enemy1'
        elif self.level == 2:
            enemy_type = 'enemy2'
        for spawner in enemy_spawners:
            self.enemies.append(Enemy(self, spawner['pos'], (8, 15), e_type=enemy_type))
        
        for spawner in self.tilemap.extract([('spawners', 0)]):
            self.player.pos = spawner['pos']

        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

        self.prev_background = self.current_background
        self.current_background = self.backgrounds.get(self.level, self.current_background)
        self.background_alpha = 0


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
                    self.sonido_boton.play()
                    fdas = 3
                    self.reset_game()
                    self.npc_intro_dialogue()
                    self.run()
                    return
                if store_button.is_clicked(event):
                    self.sonido_boton.play()
                    self.tienda_menu()
                if credits_button.is_clicked(event):
                    print("Mostrar créditos")
                    self.sonido_boton.play()
                if quit_button.is_clicked(event):
                    self.sonido_boton.play()
                    pygame.quit()
                    sys.exit()
                if icono_configuracion.is_clicked(event):
                    self.sonido_boton.play()
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
                    self.sonido_boton.play()
                    self.volume = min(1.0, self.volume + 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                if disminuir.is_clicked(event):
                    self.sonido_boton.play()
                    self.volume = max(0.0, self.volume - 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                if volver.is_clicked(event):
                    self.sonido_boton.play()
                    return

            pygame.display.update()
            self.clock.tick(60)

    def npc_intro_dialogue(self):
        pygame.event.clear()  

        messages = [
            "¡Hola, guardián!",
            "Este mundo está lleno de peligros… estás preparado?",
            "Derrota a los enemigos y salva el planeta",
            "¡Buena suerte!"
        ]

        
        try:
            nnnn_image = pygame.image.load("data/images/imnpc/nnnn.png").convert_alpha()
            next_image = pygame.image.load("data/images/imnpc/next.png").convert_alpha()
        except Exception as e:
            print("Error cargando imágenes del NPC o botón next:", e)
            return
        
        altura_caja = 450  # Altura fija de la caja
        nnnn_image = pygame.transform.scale(nnnn_image, (self.screen.get_width(), altura_caja))
    


        nnnn_rect = nnnn_image.get_rect()
        nnnn_rect.bottom = self.screen.get_height()  # Parte inferior de la pantalla
        nnnn_rect.left = 0  # Alineado al borde izquierdo

        text_area = pygame.Rect(nnnn_rect.left + 200, nnnn_rect.top + altura_caja - 100, nnnn_rect.width - 260, 200)
        # Posicionar el botón 'next'
        next_image = pygame.transform.scale(next_image, (200, 90))  # También puedes escalarlo como en tu ejemplo
        next_rect = next_image.get_rect()
        next_rect.bottomright = (nnnn_rect.right - 30, nnnn_rect.bottom - 30)

        font = pygame.font.Font(None, 28)
        clock = pygame.time.Clock()
        message_index = 0

        def draw_text_wrapped(surface, text, font, color, rect):
            words = text.split(' ')
            lines = []
            line = ''
            for word in words:
                test_line = line + word + ' '
                if font.size(test_line)[0] <= rect.width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)

            y = rect.top
            line_height = font.get_linesize()
            for line in lines:
                rendered = font.render(line.strip(), True, color)
                surface.blit(rendered, (rect.left, y))
                y += line_height

        running = True
        while running and message_index < len(messages):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_rect.collidepoint(event.pos):
                        message_index += 1
                        if message_index >= len(messages):
                            running = False

            self.screen.blit(self.menu_assets['background'], (0, 0))  # Usa el fondo del menú

            self.screen.blit(nnnn_image, nnnn_rect)
            if message_index < len(messages):
                draw_text_wrapped(self.screen, messages[message_index], font, (0,0,0), text_area)

            # Botón next
            self.screen.blit(next_image, next_rect)
           
            pygame.display.update()
            clock.tick(60)



    def run(self):
        self.musicadefondo.play(-1) 
        pygame.mixer.music.load('data/sfx/ambience.wav') 
        pygame.mixer.music.set_volume(0.3)  # volumen entre 0.0 y 1.0
        pygame.mixer.music.play(-1)  # -1 para que se repita en loop

        pixel_font = pygame.font.Font('data/Fonts/pixel_font.ttf', 9)
        while True:

            if self.player.vidas <= 0:
                self.sonidodemuerte.play()
                self.reset_game()
                self.game_over()
                return           
            self.display.blit(self.prev_background, (0, 0))

            if self.background_alpha < 255:
                bg_copy = self.current_background.copy()
                bg_copy.set_alpha(self.background_alpha)
                self.display.blit(bg_copy, (0, 0))
                self.background_alpha = min(255, self.background_alpha + 5)
            else:
                self.display.blit(self.current_background, (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.sonidodemuerte.play()
                    self.player.vidas = 0    # forzá la muerte
                    continue
            # Movimiento de la cámara directamente al jugador

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.sonido_golpe_enemigo.play()
                    self.enemies.remove(enemy)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
                for i in range(self.player.vidas): # Corazones
                    self.display.blit(self.heart_img, (5 + i * 25, 5)) # Posición del corazón
                self.display.blit(self.enemy_icon, (5, 35))
                enemy_count_text = self.pixel_font.render(f'x {len(self.enemies)}', True, (255, 255, 255))
                self.display.blit(enemy_count_text, (30, 35))
                if self.player.vidas <= 0:
                    self.musicadefondo.stop()
                    self.game_over()
                    return
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.player.take_damage()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                        
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.corriendo.play(-1)  # Reproduce el sonido de correr
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.corriendo.play(-1) 
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                        self.sonido_saltar.play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                        self.sonido_dash.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.corriendo.stop()
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.corriendo.stop()
                        self.movement[1] = False
            
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)                       
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), 
                (int(screenshake_offset[0]), int(screenshake_offset[1]))
            )
            pygame.display.update()
            self.clock.tick(60)

    def tienda_menu(self):
            volver_img = pygame.transform.scale(pygame.image.load("data/images/menu_backgrounds/volveralmenu.png"), (300, 200))
            volver = Button(195, 360, 200, 80)

            
            self.screen.blit(self.menu_assets['background'], (0, 0))
            self.screen.blit(self.menu_assets['tienda_titulo'], (110, -110))

            boton_skin_verde = Button(100, 185, 180, 35)
            boton_skin_rosado = Button(370, 185, 200, 35)
            boton_skin_original = Button(220, 267, 211, 35)

            # Texto skins
            skins = [
                {"nombre": "Ninja Verde", "pos": (100, 170)},
                {"nombre": "Ninja Rosado", "pos": (370, 170)},
                {"nombre": "Ninja Original", "pos": (220, 250)},
            ]

            while True:
                
                # Mostrar nombre skins
                for producto in skins:
                    texto = self.font.render(producto["nombre"], True, (240, 180, 35))
                    self.screen.blit(texto, producto["pos"])
                
                self.screen.blit(volver_img, (170, 300))  # Imagen del botón volver

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if volver.is_clicked(event):
                        self.sonido_boton.play()
                        return
                    if boton_skin_verde.is_clicked(event):
                        self.sonido_boton.play()
                        skin_seleccionada = 'skin1'
                    if boton_skin_rosado.is_clicked(event):
                        self.sonido_boton.play()
                        skin_seleccionada = 'skin2'
                    if boton_skin_original.is_clicked(event):
                        self.sonido_boton.play()
                        skin_seleccionada = 'player'


                pygame.display.update()
                self.clock.tick(60)

    def game_over(self):
        self.corriendo.stop()
        self.musicadefondo.stop()  # Detiene la música de fondo
        pygame.mixer.music.load('data/music.wav')  # Ruta a el archivo de música
        pygame.mixer.music.play(-1)  # -1 significa que se reproduce en bucle infinito
        volver_img = pygame.transform.scale(pygame.image.load("data/images/menu_backgrounds/volveralmenu.png"), (300, 200))
        volver = Button(195, 360, 200, 80)
        self.screen.blit(self.menu_assets['background'], (0, 0))
        self.screen.blit(self.menu_assets['game_over'], (60, -20)) 
        self.screen.blit(volver_img, (170, 300))  # Imagen del botón volver

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if volver.is_clicked(event):
                    self.sonido_boton.play()
                    self.main_menu()
                    return

            pygame.display.update()
            self.clock.tick(60)

    def reset_game(self):
        self.level = 0
        self.load_level(self.level)
        self.player.vidas = 3
        self.player.air_time = 0
        self.player.jumps = 1
        self.player.dashing = 0
        self.dead = 0
        self.transition = 0
        self.scroll = [0, 0]
        self.movement = [False, False]

if __name__ == '__main__':
    game = Game()
    game.main_menu()  # Mostrar menú antes de iniciar el juego
    game.run()