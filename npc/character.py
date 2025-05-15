import pygame
import constantes 
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(constantes.RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, constantes.SCREEN_WIDTH), random.randint(0, constantes.SCREEN_HEIGHT))

        
        