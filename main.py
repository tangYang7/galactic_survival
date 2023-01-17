import pygame
import random
import os

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

MUSIC, SOUND = True, True
FPS = 60
BACKGROUND = (128, 128, 128)
WIDTH, HEIGHT = 500, 600

# game init and create viewport
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("First Game")

# load pictures
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "lovepik-red-bullet.png")).convert()
ship_img = pygame.image.load(os.path.join("img", "ship.jpg")).convert()
ship_lives_img = pygame.transform.scale(ship_img, (24, 32))
ship_lives_img.set_colorkey(BLACK)
pygame.display.set_icon(ship_lives_img)

rock_imgs = []
for i in range(3):
    rock_imgs.append( pygame.image.load(os.path.join("img", f"rock{i}.jpg")).convert()
    )

expl_animate = {} # dict
expl_animate['lg'] = []
expl_animate['sm'] = []
expl_animate['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_animate['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_animate['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_animate['player'].append(pygame.transform.scale(player_expl_img, (180, 180)))

# load music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
death_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))

expls = []
for i in range(2):
    expls.append(pygame.mixer.Sound(os.path.join("sound", f"expl{i}.wav"))) 
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.2)

# word
# font_name = pygame.font.match_font('arial')
font_name = os.path.join("font.ttf")

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)    # current hp
    pygame.draw.rect(surf, WHITE, outline_rect, 2)    # hp's border

def draw_lives(surf, live_count, img, x, y):
    for i in range(live_count):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(pygame.transform.scale(background_img, (500, 600)), (0, 0)) 
    draw_text(screen, '太空生存戰', 60, WIDTH/2, HEIGHT/4)
    draw_text(screen, ' ←跟→移動飛船，space鍵可以發射子彈', 24, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲', 30, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYUP:  # when stop holding the keyboard button
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True
                waiting = False
    return False

def one_more_time():
    button_clicked = False
    font = pygame.font.SysFont("arial", 32)
    text = font.render("  Again  ", True, WHITE)
    text_rect = text.get_rect(center = (WIDTH/2, HEIGHT/2))
    pygame.draw.rect(screen, (110, 120, 204), text_rect)
    draw_text(screen, '或者按space鍵可重新開始', 24, WIDTH/2, HEIGHT*2.5/4)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = True if text_rect.collidepoint(event.pos) else False
    
        if button_clicked:
            waiting = False
        else:
            screen.blit(text, text_rect)
        pygame.display.update()
    return True

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
        self.rect.center = (WIDTH/2, HEIGHT-20)
        self.health = 100
        self.lives = 2
        self.hidden = False
        self.hide_time = 0
  
    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.center = (WIDTH/2, HEIGHT-20)
    
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
        if not self.hidden:
            bullet = Bullet(self.rect.centerx, self.rect.y)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if SOUND:
                shoot_sound.set_volume(0.3)
                shoot_sound.play()
        
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

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
        self.rect.x = x
        self.rect.y = y
        self.speedY = -10
        
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < 0 :
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_animate[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_animate[self.size]):
                self.kill()
            else:
                self.image = expl_animate[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

def add_new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

score = 0
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
rocks = pygame.sprite.Group()
for i in range(8):
    add_new_rock()


# game 
pygame.mixer.music.play(-1)
show_init = True
running = True
while running:
    if MUSIC:   pygame.mixer.music.set_volume(0.2)
    else:       pygame.mixer.music.set_volume(0)
    
    if show_init:
        if draw_init():
            break
        show_init = False
    clock.tick(FPS)      # 一秒內最多只能被執行n次loop (FPS)
    # get userInput
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
            hit_music.set_volume(0.15) 
            hit_music.play()
        score += int(hit.radius)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        add_new_rock()
    # hits = pygame.sprite.spritecollide(player, rocks, False)
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        if SOUND:
            death_sound.set_volume(0.07) 
            death_sound.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        add_new_rock()
        if player.health < 0:
            death_expl = Explosion(player.rect.center, 'player')
            if SOUND:
                death_sound.set_volume(0.15) 
                death_sound.play()
            all_sprites.add(death_expl)
            player.lives -= 1
            player.health = 100
            player.hide()

    if player.lives == 0 and not death_expl.alive():
        if one_more_time():
            break
        player = Player()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        bullets = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        for i in range(8):
            add_new_rock()
        score = 0

    # show screen
    screen.fill( BACKGROUND ) #RGB
    screen.blit(
        pygame.transform.scale(background_img, (500, 600)), 
        (0, 0)) 
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, ship_lives_img, WIDTH-100, 15)
    pygame.display.update()

# end game
pygame.quit()