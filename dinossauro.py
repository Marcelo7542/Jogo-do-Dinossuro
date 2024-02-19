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

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons,'death_sound.wav'))
colidiu = False

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))

escolha_obstaculo = random.choice([0, 1])

pontos = 0

velocidade = 10


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Consolas', tamanho, True, True)
    mensagem = f'{msg}'
    texto = fonte.render(mensagem, True, cor)
    return texto

def reiniciar_jogo():
    global pontos, velocidade, colidiu, escolha_obstaculo
    pontos = 0 
    velocidade = 10
    colidiu = False
    dino.rect.y = altura - 64 - 96//2
    dino.pulo = False
    dino_voador.rect.x = largura
    cactus.rect.x = largura
    escolha_obstaculo = random.choice([0,1])

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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.rect.x -= velocidade

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
        self.rect.x -= velocidade
        
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0),(32,32))
        self.image = pygame.transform.scale(self.image, (32 *2, 32*2))
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura, altura - 64)
        self.rect.x = largura
        
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0 :
                self.rect.x = largura
            self.rect.x -= velocidade  
        
class Dino_voador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32,0), (32,32))   
            img = pygame.transform.scale(img, (32 *3, 32 *3))
            self.imagens.append(img)
            
        self.index = 0
        self.image = self.imagens[int(self.index)]
        self.escolha = escolha_obstaculo
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (largura, 300)
        self.rect.x = largura
        
        
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0 :
                self.rect.x = largura
            self.rect.x -= velocidade
        if self.index > 1:
            self.index = 0
        self.index += 0.25
        self.image = self.imagens[int(self.index)]
todas_as_sprites = pygame.sprite.Group()
dino = Dinossauro()
todas_as_sprites.add(dino)

for i in range(5):
    nuvem = Nuvem()
    todas_as_sprites.add(nuvem)
    
for i in range(100): 
    chao = Chao(i)
    todas_as_sprites.add(chao)

cactus = Cactus()
todas_as_sprites.add(cactus)
  
dino_voador = Dino_voador()
todas_as_sprites.add(dino_voador)
    
obstaculos = pygame.sprite.Group()
obstaculos.add(cactus)   
obstaculos.add(dino_voador)



relogio = pygame.time.Clock()
while True:
    relogio.tick(40)
    window.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP and colidiu == False:
                if dino.rect.y != dino.pos_y:
                    pass
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()
        
    colisoes = pygame.sprite.spritecollide(dino, obstaculos, False, pygame.sprite.collide_mask)

        
        
    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True
        
    if colidiu == True:
        game_over = exibe_mensagem("GAME OVER", 40, (0,0,0))
        window.blit(game_over, (largura/2,altura/2))
        reiniciar = exibe_mensagem('Pressione R para reiniciar', 20, (0,0,0))
        window.blit(reiniciar, (largura//2,(altura//2) + 60))
    else:
        pontos += 1
        todas_as_sprites.update()
        text_pontos = exibe_mensagem(pontos, 40, (0,0,0))
    todas_as_sprites.draw(window)
    
    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 23:
            velocidade += 0
        else:
            velocidade += 1
    window.blit(text_pontos, (480,30))
    
    if cactus.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = random.choice([0, 1])
        cactus.rect.x = largura
        dino_voador.rect.x = largura
        cactus.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo 
        
    pygame.display.flip()