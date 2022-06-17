#Создай собственный Шутер!

from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png',player.rect.centerx,player.rect.top,20,20,3)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 450:
            randX = randint(5,610)
            self.rect.y = 0
            self.rect.x = randX
            self.speed = randint(1,2)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Hearts(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 450:
            randX = randint(5,610)
            self.rect.y = 0
            self.rect.x = randX



randNum = randint(1,2)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,60)

player = Player('rocket.png', 5, win_height - 100,65,65, 3)
enemy1 = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))
enemy2 = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))
enemy3 = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))
enemy4 = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))
enemy5 = Enemy('ufo.png',randint(5,610),0,65,65,randint(1,2))
enemy6 = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))

bullets = sprite.Group()
hearts = sprite.Group()
lost = 0
score = 0
kills = 0
countlife = 1

monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
monsters.add(enemy6)

lose = font2.render('Вы проиграли((',1,(255,0,0))

game = True 
clock = time.Clock()
FPS = 60
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if finish != True:
        window.blit(background,(0, 0)) 
        text = font1.render('Счет:'+ str(score),1,(255,255,255))
        window.blit(text,(10,20))

        lifes = font1.render('Жизни:'+ str(countlife),1,(255,255,255))
        window.blit(lifes,(10,60))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        hearts.draw(window)
        hearts.update()

        if sprite.spritecollide(player,monsters, False):
            finish = True 

        
        colides = sprite.groupcollide(monsters,bullets,True,True)
        for colide in colides:
            enemy = Enemy('ufo.png',randint(5,610),0,65,65 ,randint(1,2))
            monsters.add(enemy)
            score += 1
            kills += 1

        if kills == 5:
            heart = Hearts('heart.png',randint(5,610),0,65,65 ,1)
            hearts.add(heart)
            kills = 0
        if sprite.spritecollide(player,hearts,True):
            countlife += 1

        if countlife == 0:
            finish = True
            window.blit(lose,(200,250))

        
    display.update()
    clock.tick(FPS)