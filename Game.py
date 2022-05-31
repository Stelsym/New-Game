from pygame import *
from random import randint
from time import time as timer #импортировать под названием таймер
import ctypes

user32 = ctypes.windll.user32
win_x = user32.GetSystemMetrics(0)
win_y = user32.GetSystemMetrics(1)

window = display.set_mode((win_x,win_y),flags=FULLSCREEN)
display.set_caption('')
background = transform.scale(image.load('space.jpg'),(win_x,win_y))

#Классы
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def image_reset(self,new_image,size_x,size_y): 
        self.image = transform.scale(image.load(new_image),(size_x,size_y))
        self.reset()

class Player_ALFA(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_y-200:
            self.rect.y += self.speed

class Player_BETA(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_y-200:
            self.rect.y += self.speed

class Ball(GameSprite):
    def update(self):
        global Flag
        if Flag == False:
            if self.rect.x < win_x-101:
                self.rect.x += self.speed
            else:
                Flag = True
        
        if Flag != False:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                Flag = False

        




#Настройки
font.init()
font1 = font.SysFont('Verdana',26)

Game = True
Start = False
Finish = False

FPS = 60
clock = time.Clock()

random = randint(1,2)
if random == 1:
    Flag = False
else:
    Flag = True

Player1 = Player_ALFA('fanta.png',50,100,75,200,10)
Player2 = Player_BETA('sprite.png',win_x-150,100,125,200,10)
Asteroid = Ball('asteroid.png',win_x/2,win_y/2,100,100,10)

#Цикл
while Game:
    if not Finish:
        window.blit(background,(0,0))
        Player1.reset()
        Player1.update()
        Player2.reset()
        Player2.update()
        Asteroid.reset()
        if Start != False:
            Asteroid.update()
        
        text_not_start = font1.render('НАЖМИТЕ ПРОБЕЛ ЧТОБЫ НАЧАТЬ ИГРУ',1,(150,0,0))
        if Start != True:
            window.blit(text_not_start,(win_x/2-250,win_y/2-100))

        display.update()

    for e in event.get():
        if e.type == QUIT:
            Game = False
        
        if e.type == KEYDOWN:
            if e.key == K_1:
                window = display.set_mode((win_x,win_y),flags=FULLSCREEN) #ПОЛНОЭКРАННЫЙ
            if e.key == K_ESCAPE:
                window = display.set_mode((win_x,win_y),flags=RESIZABLE) #ОКОННЫЙ

            if e.key == K_SPACE:
                Start = True
            
                
    clock.tick(FPS)
    #time.delay(10) 