import pygame
from pygame.locals import *
import os
from sys import *
import random


pygame.init()
pygame.mixer.init()


diretorio = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio, 'imagens')
diretorio_sons = os.path.join(diretorio, 'sons')

largura = 640
altura = 500


window = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Dinossauro")

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

class Dinossauro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dinossauro = []
        self.som = pygame.mixer.Sound(os.path.join(diretorio_sons, "jump_sound.wav"))
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dinossauro.append(img)

        self.index = 0
        self.image = self.dinossauro[int(self.index)]
        self.rect = self.image.get_rect()
        self.pos_y = altura - 64 - 96//2
        self.rect.center = (100,436)
        self.pulo = False
        
    def pular(self):
        self.pulo = True
        self.som.play()
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y
            
        if self.index > 2:
            self.index = 0
        self.index += 0.25
        self.image = self.dinossauro[int(self.index)]
        
class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((224, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(50,200,50)
        self.rect.x = random.randrange(0,500,40)
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10

class Chao(pygame.sprite.Sprite):
    def __init__(self, i):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = i * 64
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10
        
        
todas_as_sprites = pygame.sprite.Group()
dino = Dinossauro()
todas_as_sprites.add(dino)

for i in range(5):
    nuvem = Nuvem()
    todas_as_sprites.add(nuvem)
    
for i in range(100): 
    chao = Chao(i)
    todas_as_sprites.add(chao)
    
    
relogio = pygame.time.Clock()
while True:
    relogio.tick(40)
    window.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or K_SPACE:
                if dino.rect.y != dino.pos_y:
                    pass
                else:
                    dino.pular()
                    
    todas_as_sprites.draw(window)
    todas_as_sprites.update()
    
    pygame.display.flip()