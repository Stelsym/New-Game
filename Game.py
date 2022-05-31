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
    def __init__(self,player_image,player_x,player_y,size_x,size_y,speed_x,speed_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
        self.speed_y = speed_y
        self.speed_x = speed_x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def image_reset(self,new_image,size_x,size_y): 
        self.image = transform.scale(image.load(new_image),(size_x,size_y))
        self.reset()

class Player_ALFA(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed_x
        if keys[K_s] and self.rect.y < win_y-200:
            self.rect.y += self.speed_x

class Player_BETA(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed_x
        if keys[K_DOWN] and self.rect.y < win_y-200:
            self.rect.y += self.speed_x

class Ball(GameSprite):
    def update(self):
        global Flag
        if Flag == False:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        
        if Flag != False:
            self.rect.x -= self.speed_x
            self.rect.y -= self.speed_y

        if self.rect.y < 0 or self.rect.y > win_y - 101:
            self.speed_y *= -1
        #if self.rect.x < 0 or self.rect.x > win_x - 101:
            #self.speed_x *= -1
        
        


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

Player1 = Player_ALFA('fanta.png',50,100,75,200,15,15)
Player2 = Player_BETA('sprite.png',win_x-150,100,125,200,15,15)
Asteroid = Ball('asteroid.png',win_x/2,win_y/2,100,100,12,12)

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

            if sprite.collide_rect(Player1,Asteroid):
                Asteroid.speed_x *= -1
                rand = randint(12,18)
                Asteroid.speed_y = rand

            if sprite.collide_rect(Player2,Asteroid):
                Asteroid.speed_x *= -1
                rand = randint(12,18)
                Asteroid.speed_y = rand
            
            if Asteroid.rect.x >= win_x - 101:
                window.blit(text_win_fanta,(win_x/2-250,win_y/2-100))
                Asteroid.speed_y = 0
                Asteroid.speed_x = 0


        text_not_start = font1.render('НАЖМИТЕ ПРОБЕЛ ЧТОБЫ НАЧАТЬ ИГРУ',1,(150,0,0))
        text_win_fanta = font1.render('ФАНТА ЗАБИЛА ГОЛ!!!',1,(150,0,0))

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