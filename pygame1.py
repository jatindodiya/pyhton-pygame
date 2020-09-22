import pygame
import random
pygame.init()
pygame.display.set_caption("Goblin Hunter game")

font = pygame.font.SysFont('comicsans', 30, True)

walkRight = [pygame.image.load('photos/R1.png'), pygame.image.load('photos/R2.png'), pygame.image.load('photos/R3.png'), pygame.image.load('photos/R4.png'), pygame.image.load('photos/R5.png'), pygame.image.load('photos/R6.png'), pygame.image.load('photos/R7.png'), pygame.image.load('photos/R8.png'), pygame.image.load('photos/R9.png')]
walkLeft = [pygame.image.load('photos/L1.png'), pygame.image.load('photos/L2.png'), pygame.image.load('photos/L3.png'), pygame.image.load('photos/L4.png'), pygame.image.load('photos/L5.png'), pygame.image.load('photos/L6.png'), pygame.image.load('photos/L7.png'), pygame.image.load('photos/L8.png'), pygame.image.load('photos/L9.png')]
bg = pygame.image.load('photos/bg.jpg')
char = pygame.image.load('photos/standing.png')

screen_height = 480
screen_width = 800
win = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('photos/punch.wav')
hitSound = pygame.mixer.Sound('photos/knifeHit.wav')
jumpSound = pygame.mixer.Sound('photos/jump.wav')

music = pygame.mixer.music.load('photos/music.mp3')
pygame.mixer.music.play(-1)

level = 1
levelChange = True
score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.WalkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitval = False
        self.health = 10
        self.playerVisible = True
        
        
    def draw(self):
        if self.playerVisible:
            if self.walkCount + 1 >= 9:
                self.walkCount = 0
            if not(self.standing):   
                if self.left:  
                    win.blit(walkLeft[self.walkCount], (self.x,self.y))
                    self.walkCount += 1                          
                elif self.right:
                    win.blit(walkRight[self.walkCount], (self.x,self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x,self.y))
                else:
                    win.blit(walkLeft[0], (self.x,self.y))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,110,0), (self.hitbox[0]+1, self.hitbox[1] - 19, 48 - int(48/10*(10-self.health)), 8))
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.health -= 2
        if self.health <= 0:
            self.playerVisible = False
            displayMessage("Game Over",100,200)
            pygame.time.delay(2000)
            redrawGameWindow()
            displayMessage("your score is = " + str(score),100,200)
            pygame.time.delay(2000)
            exit(0)
            
        self.x = 0
        self.y = 350
        self.walkCount = 0
        displayMessage("-5",100,200)
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        

class enemy(object):
    walkRight = [pygame.image.load('photos/R1E.png'), pygame.image.load('photos/R2E.png'), pygame.image.load('photos/R3E.png'), pygame.image.load('photos/R4E.png'), pygame.image.load('photos/R5E.png'), pygame.image.load('photos/R6E.png'), pygame.image.load('photos/R7E.png'), pygame.image.load('photos/R8E.png'), pygame.image.load('photos/R9E.png'), pygame.image.load('photos/R10E.png'), pygame.image.load('photos/R11E.png')]
    walkLeft = [pygame.image.load('photos/L1E.png'), pygame.image.load('photos/L2E.png'), pygame.image.load('photos/L3E.png'), pygame.image.load('photos/L4E.png'), pygame.image.load('photos/L5E.png'), pygame.image.load('photos/L6E.png'), pygame.image.load('photos/L7E.png'), pygame.image.load('photos/L8E.png'), pygame.image.load('photos/L9E.png'), pygame.image.load('photos/L10E.png'), pygame.image.load('photos/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 2 + (level)
        self.health = 8 + (2*level)
        self.visible = True 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        
    def draw(self):
        self.move()
        if self.walkCount+1 >= 33:
            self.walkCount = 0
            
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1 
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1

        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0,110,0), (self.hitbox[0]+1, self.hitbox[1] - 19, 48 - int(48/(8+(2*level))*(8+(2*level)-self.health)), 8))
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,e
            
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.path[1] = random.randint(100,screen_width-50)
                print(self.path[1])
                
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.path[0] = random.randint(0,screen_width-200)
                print(self.path[0])

    def hit(self):
        hitSound.play()
        self.health -= 1
        print('hit')
        
class projectile():
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.colour = colour
        self.vel = 8 
    def draw(self):
        pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)

        
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (650, 10))
    
    man.draw()
    for goblin in goblins:
        goblin.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()


def displayMessage(message,fontSize, height):
    font = pygame.font.SysFont('comicsans', fontSize)
    text = font.render(message, 1, (255,0,0))
    win.blit(text,(screen_width//2 - int(text.get_width()/2),height))
    pygame.display.update()

def gameStart():
    win.blit(bg,(0,0))
    stay = True
    while stay:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stay = False
        keys = pygame.key.get_pressed()
        pygame.display.update()
        displayMessage("let's start hunting",50,100)
        displayMessage("press spacebar to start the game",50,200)
        if keys[pygame.K_SPACE]:
            win.blit(bg,(0,0))
            break
          
           
#main loop
man = player(50,350,64,64)
bullets = []
goblins = []
level = 0
respon = True
shootLoop = 0
run = True
gameStart()
while run:
    clock.tick(27)

    

                
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for goblin in goblins:    
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
                man.hitJump = False
                man.jumpCount = 10
              
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if len(goblins) == 0:
        respon = True
        level += 1
        
        displayMessage("level "+ str(level),100,200)
        pygame.time.delay(2000)
        
    for goblin in goblins:
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    if goblin.health <= 0:
                        goblins.pop(goblins.index(goblin)) 
                        
                    
                                              
    if len(goblins) < level and respon:
        respon = False
        for i in range(level):
            goblins.append(enemy(random.randint(100,800),355,64,64,random.randint(100,700)))

    for bullet in bullets:
        if bullet.x < screen_width and bullet.x > 0:
            bullet.x += bullet.vel * bullet.facing  
        else:
            bullets.pop(bullets.index(bullet))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(man.x+man.width//2, man.y+man.height//2, 6 , (255,0,0), facing))
            bulletSound.play()
        shootLoop = 1
    
    if keys[pygame.K_LEFT] and man.x > man.vel:
        #print("left")
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.vel - man.width:
        #print("right")
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
        
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            jumpSound.play()
            man.isJump = True
            man.walkCount = 0
                
    else: 
        if man.jumpCount >= -10:
            man.y -= int((man.jumpCount * abs(man.jumpCount)) * 0.5)
            man.jumpCount -= 1
        else: 
            man.jumpCount = 10
            man.isJump = False

    redrawGameWindow() 
    
    
pygame.quit()
