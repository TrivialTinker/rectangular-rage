import pygame
import random
pygame.init()

#colour definitions
red =       (255,0,0)
green =     (0,255,0)
blue =      (0,0,255)
black =     (0,0,0)
white =     (255,255,255)
gray =      (125,125,125)
yellow =    (255,255,0)

enemy = pygame.image.load('enemy.png')

font = pygame.font.SysFont('arial',50)

width = 600
height = 600
display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
screen = pygame.Rect(0,0,width,height)
def Quit():
    pygame.quit()
    quit()
class player():
    def __init__(self):
        self.rect = pygame.Rect(width/2-10,height/2+30,20,60)
    def move(self,x,y,w,h):
        self.rect.x = x
        self.rect.y = y
        self.rect.w = w
        self.rect.h = h
        self.rect.normalize()
        pygame.draw.rect(display,green,self.rect)
def restart():
    global lives
    lives = 0
    main()
def life(x,y,l):
    display.blit(font.render(str(l),1,green),(width/2-30,30))

def scr(score):
    display.blit(font.render(str(score),1,red),(20,20))

class Bullet(object):
    def __init__(self, pos, size, d):
        global bullets
        self.d = d
        bullets.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.rect.center = pos
        if self.d[0]<0: self.rect.right = player.rect.left
        elif self.d[0]>0: self.rect.left = player.rect.right
        if self.d[1]<0: self.rect.bottom = player.rect.top
        elif self.d[1]>0: self.rect.top = player.rect.bottom
        
    def shoot(self):
        self.rect.x += self.d[0]
        self.rect.y += self.d[1]
        pygame.draw.rect(display,blue,self.rect)
        
class Enemy():
    def __init__(self, pos):
        global enemies
        enemies.append(self)
        self.rect = pygame.Rect(pos[0],pos[1],20,20)
    def move(self,x,y,speed):
        if self.rect.x > x: self.rect.x -= speed
        elif self.rect.x < x: self.rect.x += speed
        if self.rect.y > y: self.rect.y -= speed
        elif self.rect.y < y: self.rect.y += speed
        pygame.draw.rect(display,red,self.rect)

player = player()
def main():
    global enemies
    global bullets
    global lives
    x = 200
    y = 100
    w = 20
    h = 60
    xchange = 0
    ychange = 0
    bullets = []
    speed = 2
    bltspd = 4
    d = [0,-bltspd]
    enemies = []
    lives = 10
    score = 0
    size = 10
    spawnrate = 110
    can_shoot = True
    enmyspd = 1
    while lives > 0:
        

        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit()
                
        #controls>        
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]: Quit()
        if key[pygame.K_SPACE] and can_shoot:
            Bullet(player.rect.center,size,d)
            can_shoot = False
            enmyspd = 0
        if key[pygame.K_a]: w,h,xchange,d = -60,20,-speed,[-bltspd,0]
        if key[pygame.K_d]: w,h,xchange,d = 60,20,speed,[bltspd,0]
        if key[pygame.K_s]: w,h,ychange,d = 20,60,speed,[0,bltspd]
        if key[pygame.K_w]: w,h,ychange,d = 20,-60,-speed,[0,-bltspd]
        if key[pygame.K_UP] and spawnrate > 1: spawnrate -= 1
        if key[pygame.K_DOWN]: spawnrate += 1
        if key[pygame.K_r]: restart()
        if not key[pygame.K_a] and not key[pygame.K_d]: xchange = 0
        if not key[pygame.K_w] and not key[pygame.K_s]: ychange = 0
        if not key[pygame.K_SPACE]: can_shoot,enmyspd = True,1
        #<controls

        #logic>
        x += xchange
        y += ychange
        if random.randint(1,spawnrate) == 1:
            if random.choice([True,False]):
                Enemy([random.choice([-20,width]),random.randint(0,height-20)])
            else:
                Enemy([random.randint(0,width-20),random.choice([-20,height])])
        if score > 100:
            size = 100
        #<logic
            
        #drawing>
        display.fill(white)
        
        for b in bullets:
            b.shoot()
            if not b.rect.colliderect(screen):
                bullets.remove(b)
            for e in enemies:
                if b.rect.colliderect(e.rect):
                    enemies.remove(e)
                    score += lives
        
        for e in enemies:
            e.move(x,y,enmyspd)
            if e.rect.colliderect(player.rect):
                enemies.remove(e)
                lives -= 1
        
        player.move(x,y,w,h)
        life(width/2,20,lives)
        scr(score)
        pygame.display.update()
        #<drawing
    restart()
main()
