import pygame
import sys
import constantes
import character

#inicializar Pygame
pygame.init()

#config de la pantalla
screen_width = constantes.SCREEN_HEIGHT
screen_width = constantes.SCREEN_WIDTH

screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption('NPCCC')

#npc
npc = character.NPC()
all_sprites = pygame.sprite.Group()
all_sprites.add(npc)

#bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(constantes.BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    pygame.quit()
    sys.exit()

