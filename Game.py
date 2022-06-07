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
            sound_rand = randint(1,2)
            if sound_rand == 1:
                sound_ball_pryg_pryg1.play()
            if sound_rand == 2:
                sound_ball_pryg_pryg2.play()
            self.speed_y *= -1
        


#Настройки
font.init()
font1 = font.SysFont('Verdana',26)
font2 = font.SysFont('Verdana',31)

mixer.init()
mixer.music.load('fon.mp3')
mixer.music.play()
sound_ball_pryg_pryg1 = mixer.Sound('ball_ogg.ogg')
sound_ball_pryg_pryg2 = mixer.Sound('ball_ogg2.ogg')
sound_fanta_win = mixer.Sound('fanta_win.ogg')
sound_sprite_win = mixer.Sound('win.ogg')

Game = True
Start = False
Finish = False
Stop_a = False #Fanta
Plus_a = True
Stop_b = False #Sprite
Plus_b = True
Go_Dalshe = False

a = 0 #Fanta
b = 0 #Sprite

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
                Stop_a = True
                Start = False

            if Asteroid.rect.x <= 0 or Asteroid.rect.x == 0:
                Stop_b = True
                Start = False
        
        text_win_fanta = font1.render('ФАНТА ЗАБИЛА ГОЛ!!!',1,(150,0,0))
        text_win_sprite = font1.render('СПРАЙТ ЗАБИЛ ГОЛ!!!',1,(150,0,0))

        text_not_start = font1.render('НАЖМИТЕ ПРОБЕЛ ЧТОБЫ НАЧАТЬ ИГРУ',1,(150,0,0))
        text_go_dalshe = font1.render('НАЖМИТЕ ПРОБЕЛ ЧТОБЫ ПРОДОЛЖИТЬ ИГРУ',1,(150,0,0))

        text_fanta_scet = font1.render(str(a),1,(150,0,0))
        text_sprite_scet = font1.render(str(b),1,(150,0,0))

        if Start != True:
            if Stop_a == False and Stop_b == False:
                window.blit(text_not_start,(win_x/2-250,win_y/2-100))
            if Stop_a == True:
                if Stop_a == True and Plus_a == True:
                    sound_fanta_win.play()
                    a += 1
                    Plus_a = False

                window.blit(text_win_fanta,(win_x/2-250,win_y/2-100))
                window.blit(text_go_dalshe,(win_x/2-250,win_y/2))
                window.blit(text_fanta_scet,(win_x/2+75,win_y/2-100))
                window.blit(text_sprite_scet,(win_x/2+135,win_y/2-100))

                Asteroid.speed_y = 0
                Asteroid.speed_x = 0

                Asteroid.rect.x = win_x/2
                Asteroid.rect.y = win_y/2

            if Stop_b == True:
                if Stop_b == True and Plus_b == True:
                    sound_sprite_win.play()
                    b += 1
                    Plus_b = False

                window.blit(text_win_sprite,(win_x/2-250,win_y/2-100))
                window.blit(text_go_dalshe,(win_x/2-250,win_y/2))
                window.blit(text_fanta_scet,(win_x/2+75,win_y/2-100))
                window.blit(text_sprite_scet,(win_x/2+135,win_y/2-100))

                Asteroid.speed_y = 0
                Asteroid.speed_x = 0

                Asteroid.rect.x = win_x/2
                Asteroid.rect.y = win_y/2

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
                if Player1.speed_x == 0 and Player1.speed_y == 0:
                    Player1.speed_x = 15
                    Player1.speed_y = 15
                if Player2.speed_x == 0 and Player2.speed_y == 0:
                    Player2.speed_x = 15
                    Player2.speed_y = 15
                if Asteroid.speed_x == 0 and Asteroid.speed_y == 0:
                    Asteroid.speed_x = 12
                    Asteroid.speed_y = 12   
                if Stop_a == True:
                    Stop_a = False
                if Stop_b == True:
                    Stop_b = False
                if Plus_a == False:
                    Plus_a = True
                if Plus_b == False:
                    Plus_b = True

            if e.key == K_0:
                mixer.music.play()
            if e.key == K_9:
                mixer.music.set_volume(0.5)
            if e.key == K_8:
                mixer.music.set_volume(1)
            if e.key == K_7:
                mixer.music.pause()
            if e.key == K_p:
                Start = False
                
    clock.tick(FPS)
    #time.delay(10) 