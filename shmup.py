#Shmup game

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
font_name = pygame.font.match_font('tahoma')
score = 0

WIDTH = 480
HEIGHT = 600
FPS = 60

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_C = (255, 255, 204)
FONT_C = (96, 19, 0)

# --------------------------------------------------------------
pygame.init() #initializes pygame
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates window
pygame.display.set_caption("Shmup zuzogame")
clock = pygame.time.Clock()

#-----------------------------------------------------
#Load all game graphics
#background = pygame.image.load(path.join(img_dir, "background.png")).convert()
 #background_rect = backgrounf.get_rect()

player_img = pygame.image.load(path.join(img_dir, "Cat.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
player_dead_img = pygame.image.load(path.join(img_dir, "Cat_dead.png")).convert()
#---------------------------------------

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size) #font object that can create text
    text_surface = font.render(text, True, FONT_C)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    
#---------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 60))
        self.transColor = player_img.get_at((0,0))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.radius = (int)(self.rect.width * .85 / 2)
       # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (int)(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0 

    def update(self):
        self.speedx = 0 
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.top < (int)(HEIGHT/3) * 2:
            self.rect.top = (int)(HEIGHT/3) * 2 
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT 

    def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    
    def is_dead(self):
        self.image = pygame.transform.scale(player_dead_img, (70, 60))
        self.transColor = player_dead_img.get_at((0,0))
        self.image.set_colorkey(self.transColor)
        

#----------------------------------------------

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(enemy_img, (40, 50))
        self.image = self.image_original.copy() #copy of original one
        self.transColor = enemy_img.get_at((0,0))
        self.image_original.set_colorkey(self.transColor)
        #self.radius = 20
        self.rect = self.image_original.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 6)
        self.speedx = random.randrange(-2,2)
        self.rotation = 0
        self.rotation_speed = random.randrange(-4, 4)
        self.last_update = pygame.time.get_ticks() #how many ticks its been since the clock started

    def rotate(self):
        now = pygame.time.get_ticks()        

        if now  - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360 #we don't want to have bigger number than 360
            new_image= pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)

#----------------------------------------------------
       
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (35, 35))
        self.transColor = bullet_img.get_at((0,0))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy

        #kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() #command that deletes sprites

#-------------------------------------------------

#Adding sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(7):
    enemy = Mob()
    all_sprites.add(enemy)
    mobs.add(enemy)

#------------------------------------------------------------
#Game loop
running = True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #Update
    all_sprites.update()

    #check if bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #checks if one group collides with another one

    #print(hits)
    for hit in hits:
        score = score + 1
        enemy = Mob()
        all_sprites.add(enemy)
        mobs.add(enemy)
    
    #check if a mob hit a player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) #this is a list
    if hits:
        running = False
        player.is_dead()

    #Draw / render
    screen.fill(BACKGROUND_C)
    #screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    pygame.display.flip() # *after* drawing everything flip the display *)

pygame.quit()