import pygame
import random
import os
FPS = 60
BACKGROUND = (128, 128, 128)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
MUSIC = True
SOUND = True

WIDTH, HEIGHT = 500, 600
# game init and create viewport
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

# load pictures
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "lovepik-red-bullet.png")).convert()
ship_img = pygame.image.load(os.path.join("img", "ship.jpg")).convert()
rock_imgs = []
for i in range(3):
    rock_imgs.append( pygame.image.load(os.path.join("img", f"rrock{i}.jpg")).convert()
    )

# load music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expls = []
for i in range(2):
    expls.append(pygame.mixer.Sound(os.path.join("sound", f"expl{i}.wav"))) 
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.3)

# word
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ship_img, (60, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ########circle object set#######
        self.radius = self.rect.width * 0.9 /2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        ################################
        self.speedX = 8
        # self.rect.x = 200
        # self.rect.y = 200
        self.rect.center = (WIDTH/2, HEIGHT-20)

        
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedX
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedX

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        if SOUND:
            shoot_sound.set_volume(0.5)
            shoot_sound.play()
        
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rock_imgs)
        size = random.choice( [(35, 35), (50, 50), (70, 70), (80, 80)])
        self.image = pygame.transform.scale(self.image, size)
        self.image.set_colorkey(BLACK)
        self.image_new = self.image

        self.rect = self.image.get_rect()
        ########circle object set#######
        self.radius = self.rect.width * 0.85 /2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        ################################
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedX = random.randrange(-3, 3)
        self.speedY = random.randrange(3, 7)
        self.rot_degree = random.randrange(-3, 3)
        self.total_degree = 0

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_new, self.total_degree)
        # rotate fix center
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.speedX = random.randrange(-3, 3)
            self.speedY = random.randrange(3, 7)
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (30, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.speedY = -10
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < 0 :
            self.kill()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
rocks = pygame.sprite.Group()
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

score = 0
pygame.mixer.music.play(-1)

# game time set
running = True
while running:
    clock.tick(FPS)      # 一秒內最多只能被執行n次loop (FPS)
    # get userInput
    if MUSIC:
        pygame.mixer.music.set_volume(0.3)
    else:
        pygame.mixer.music.set_volume(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:    #ESC: end the game
                running = False
            if event.key == pygame.K_8:
                MUSIC = not MUSIC
            if event.key == pygame.K_7:
                SOUND = not SOUND

    # update game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        hit_music = random.choice(expls)
        if SOUND:
            hit_music.set_volume(0.5)
            hit_music.play()
        score += int(hit.radius)
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    # hits = pygame.sprite.spritecollide(player, rocks, False)
    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # show screen
    screen.fill( BACKGROUND ) #RGB
    screen.blit(
        pygame.transform.scale(background_img, (500, 600)), 
        (0, 0)) 
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    pygame.display.update()

# end game
pygame.quit()