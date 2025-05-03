from pygame import *
from random import randint
def init_game():
    global killed, lost, FPS
    killed = 0
    lost = 0
    bullets = sprite.Group()
    monsters = sprite.Group()
    monster = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
    monster1 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
    monster2 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
    monster3 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
    monster4 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
    monsters.add(monster)
    monsters.add(monster1)
    monsters.add(monster2)
    monsters.add(monster3)
    monsters.add(monster4)
    btn1 = GameSprite('button.png', 250, 65, 0, 200, 325)
    button = GameSprite('Play.png', 250, 65, 0, 200, 250)
    player = Player('V3.png', 65, 65, 10, 50, 435)
    clock = time.Clock()
    FPS = 60
    finish = False
    menu = True
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)
mixer.init()
mixer.music.load('ULTRAKILL.mp3')
mixer.music.play()
killed = 0
lost = 0
window = display.set_mode((700, 500))
background = transform.scale(image.load('z.png'), (700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.status = False
        self.parry_duration = 60
        self.parry_timer = 0
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if self.status:
            current_time = time.get_ticks()
            if current_time - self.start_time >= 1:
                self.parry_timer -= 1
                self.start_time = current_time
            if self.parry_timer <= 0:
                self.status = False
    def parry(self):
        if not self.status:
            self.status = True
            self.parry_timer = self.parry_duration  
    def fire(self):
        bullet = Bullet('bullet.png', 10, 20, 10, self.rect.centerx, self.rect.centery)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 465:
            self.rect.y = -100
            self.rect.x = randint(0, 635)
            self.speed = randint(1, 3)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -10:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
monster = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
monster1 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
monster2 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
monster3 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
monster4 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
monsters.add(monster)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
btn1 = GameSprite('button.png', 250, 65, 0, 200, 325)
button = GameSprite('Play.png', 250, 65, 0, 200, 250)
player = Player('V3.png', 65, 65, 10, 50, 435)
game = True
clock = time.Clock()
FPS = 60
finish = False
menu = True
while game:
    if menu:
        window.blit(background, (0,0))
        btn1.reset()
        button.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if button.rect.collidepoint(x, y):
                    menu = False
    if finish == False and menu == False:
        victory = font2.render('ПОБЕДА!!!111!!!!!1!', 1, (255, 215, 0))
        text_win = font1.render('Убито:' +str(killed), 1, (255, 0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 0, 0))
        lose = font2.render('Инопланетяне вас скушали(', 1, (255, 215, 0))
        window.blit(background, (0,0))
        window.blit(text_lose, (5, 10))
        window.blit(text_win, (5, 40))
        sprites_list1 = sprite.spritecollide(player, monsters, True)
        for monster in sprites_list1:
            if not player.status:
                window.blit(lose, (10, 250))
                finish = True
            killed += 1
            enemy1 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
            monsters.add(enemy1)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for monster in sprites_list: 
            killed += 1
            enemy1 = Enemy('ufo.png', 65, 35, randint(1, 3), randint(0, 635), -100)
            monsters.add(enemy1)
        player.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        player.reset()
        if lost > 2:
            window.blit(lose, (10, 250))
            finish = True
        if killed > 9:
            window.blit(victory, (200, 250))
            finish = True
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN and e.button == 1:        
                    player.fire()
            keys_pressed = key.get_pressed()
            if keys_pressed[K_f]:
                print('f')
                if not player.status:
                    player.start_time = time.get_ticks()
                player.parry()
    if finish == True and menu == False:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_r:
                    init_game()
            if e.type == QUIT:
                    game = False
    clock.tick(FPS)
    display.update()