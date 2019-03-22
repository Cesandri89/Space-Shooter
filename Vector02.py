
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/feuerwerk/blob/master/vectortemplate2d.py
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
#import math
import random
import os
import time
#import operator
import math
pygame.mixer.init()
#import vectorclass2d as v
#import textscroller_vertical as ts
#import subprocess

"""Best game: 10 waves by Ines"""

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp


def randomize_color(color, delta=50):
    d=random.randint(-delta, delta)
    color = color + d
    color = min(255,color)
    color = max(0, color)
    return color






class Game:
    menuitems = []
    mainmenu = ["play", "options", "credits", "upgrade player1", "upgrade player2", "quit"]
    optionsmenu = ["audio", "video", "language", "back"]
    upgrademenu = ["spaceship","speed", "health", "shots", "damage", "back"]
    languagemenu = ["english","italian","german","back"]
    spaceshipmenu = ["spaceship1","spaceship2"]
    #languageitalianmenu = ["inglese","italiano","tedesco","indietro"]
    italiano = {"play":"gioca", "options":"opzioni", "credits":"crediti", "upgrade player1":"potenzia player1",
                "upgrade player2":"potenzia player2","quit":"esci", "audio":"audio", "video":"video",
                 "language":"lingua","back":"indietro","speed":"velocita","health":"vita",
                 "shots":"proiettili","damage":"danno","german":"tedesco","english":"inglese",
                 "italian":"italiano" }
    deutsch = {"play":"Spiel starten", "options":"Optionen", "credits":"Mitwirkende",
                "upgrade player1":  "Upgrade player1", "upgrade player2":"Upgrade player2","quit":"Ende",
                "audio":"Ton","video":"Grafik","language":"Sprache","back":"Zurück",
                "speed":"Geschwindigkeit","health":"Leben","shots":"Kugeln","damage":"Schaden",
                "german":"Deutsch","english":"English","italian":"Italienisch"}

class WaveScreen(pygame.sprite.Sprite):

    #def _overwrite_parameters(self):
    def __init__(self):
        #super(self)
        pygame.sprite.Sprite.__init__(self)#self.groups)
        #self.active_wave = 0
        self.image = pygame.Surface((20,20))
        #while 1:
        self.image.fill((0,0,0))

        #pygame.draw.circle(self.image,(255,255,0),(30,30),10)
        self.rect = self.image.get_rect()
        self.rect.x = Zviewer.width
        self.rect.y = Zviewer.height

        print("fghjklkjhghjkjhghjkjhjk")

    def update(self):
        print("ciao")
        #self.rect.fill((254,254,254))


class Mouse(pygame.sprite.Sprite):
    def __init__(self, radius = 50, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse", ):
        """create a (black) surface and paint a blue Mouse on it"""
        self._layer=10
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = radius
        self.color = color
        self.startx=startx
        self.starty=starty
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.delta = -10
        self.age = 0
        self.pos = pygame.mouse.get_pos()
        self.move = 0
        self.tail=[]
        self.create_image()
        self.rect = self.image.get_rect()
        self.control = control # "mouse" "keyboard1" "keyboard2"
        self.pushed = False

    def create_image(self):

        self.image = pygame.surface.Surface((self.radius*0.5, self.radius*0.5))
        delta1 = 12.5
        delta2 = 25
        w = self.radius*0.5 / 100.0
        h = self.radius*0.5 / 100.0
        # pointing down / up
        for y in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)

            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left
        for x in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)

            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self, seconds):
        if self.control == "mouse":
            self.x, self.y = pygame.mouse.get_pos()
        elif self.control == "keyboard1":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_w]:
                self.y -= delta
            if pressed[pygame.K_s]:
                self.y += delta
            if pressed[pygame.K_a]:
                self.x -= delta
            if pressed[pygame.K_d]:
                self.x += delta
        elif self.control == "keyboard2":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_UP]:
                self.y -= delta
            if pressed[pygame.K_DOWN]:
                self.y += delta
            if pressed[pygame.K_LEFT]:
                self.x -= delta
            if pressed[pygame.K_RIGHT]:
                self.x += delta
        elif self.control == "joystick1":
            pass
        elif self.control == "joystick2":
            pass
        if self.x < 0:
            self.x = 0
        elif self.x > Zviewer.width:
            self.x = Zviewer.width
        if self.y < 0:
            self.y = 0
        elif self.y > Zviewer.height:
            self.y = Zviewer.height
        self.tail.insert(0,(self.x,self.y))
        self.tail = self.tail[:128]
        self.rect.center = self.x, self.y
        self.r += self.delta   # self.r can take the values from 255 to 101
        if self.r < 151:
            self.r = 151
            self.delta = 10
        if self.r > 255:
            self.r = 255
            self.delta = -10
        self.create_image()

class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called"""
        pass

    def _default_parameters(self, **kwargs):
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Zviewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 10
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 100
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                #self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        self.pos += self.move * seconds
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        #self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Zviewer.width
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Zviewer.height
        # -------- right edge -----
        if self.pos.x  > Zviewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Zviewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -Zviewer.height:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Zviewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0



class Flytext(VectorSprite):
    
    def _overwrite_parameters(self):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
    
        #pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        # max_age
      
        #self.x, self.y = x, y
        
        #self.duration = duration  # duration of flight in seconds
        #self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        #self.age = 0 - delay

        
    def create_image(self):
        self.image = make_text(self.text, self.color, self.fontsize)  # font 22
        self.rect = self.image.get_rect()
        #self.rect.center = (self.x, self.y)
        
   

class Cloud(VectorSprite):
    
    def _overwrite_parameters(self):
        self.speed = 100
        self.damage = 1
        self.hitpoints = 100
        self.shots = 1
        self.points = 0
        self._layer = -5
        self.active_weapon = "default"
        self.weapons = ["default","superbullet"]
        self.switch_number = 0
        self.ammotime = 0
        self.pos.x = random.randint(0, Zviewer.world_width)
        self.pos.y = -random.randint(0, Zviewer.world_heigth)
        print("Wolke", self.pos)

    def create_image(self):
        
        self.image = pygame.Surface((180,80))
        self.image.set_colorkey((0,0,0))
        pygame.draw.ellipse(self.image,(202,198,190),[22,22,138,58],0)
        pygame.draw.ellipse(self.image,(202,198,190),[30,16,64,50],0)
        pygame.draw.ellipse(self.image,(202,198,190),[78,16,98,64],0)
        
        
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
       


class Explosion():

    def __init__(self, pos, maxspeed=150, minspeed=20, color=(255,255,0),maxduration=2.5,gravityy=3.7,sparksmin=5,sparksmax=20, a1=0,a2=360):

        for s in range(random.randint(sparksmin,sparksmax)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.triangular(a1,a2)
            v.rotate_ip(a)
            g = pygame.math.Vector2(0, - gravityy)
            speed = random.randint(minspeed, maxspeed)     #150
            duration = random.random() * maxduration
            Spark(pos=pygame.math.Vector2(pos.x, pos.y), angle=a, move=v*speed,
                  max_age = duration, color=color, gravity = g)


class Spark(VectorSprite):

    def __init__(self, **kwargs):
        VectorSprite.__init__(self, **kwargs)
        if "gravity" not in kwargs:
            self.gravity = pygame.math.Vector2(0, -3.7)

    def _overwrite_parameters(self):
        self._layer = 2
        self.kill_on_edge = True

    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,75)    #50
        g = randomize_color(g,75)
        b = randomize_color(b,75)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b),
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.move += self.gravity




class Player(VectorSprite):

    def _overwrite_parameters(self):
        self.speed = 100
        self.damage = 1
        self.hitpoints = 100
        self.shots = 1
        self.points = 0
        self.active_weapon = "default"
        self.weapons = ["default","superbullet"]
        self.switch_number = 0
        self.ammotime = 0



    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
                self.pos.x = 0
                self.move = pygame.math.Vector2(0,0)
                #self.move.x *= -1
            # -------- upper edge -----
        if self.pos.y  > 0:
                self.pos.y = 0
                #self.move.y *= -1
                self.move = pygame.math.Vector2(0,0)
            # -------- right edge -----
        if self.pos.x  > Zviewer.world_width:
                self.pos.x = Zviewer.world_width
                self.move = pygame.math.Vector2(0,0)
               
            # --------- lower edge ------------
        if self.pos.y   < -Zviewer.world_heigth:
                self.pos.y = -Zviewer.world_heigth
                self.move = pygame.math.Vector2(0,0)
    


    def create_image(self):
        #self.image = pygame.Surface((100,100))
        #pygame.draw.polygon(self.image,(255,0,0),((80,20),(95,35),(80,45),(70,27)))
        #pygame.draw.polygon(self.image,(255,0,0),((80,80),(95,65),(80,55),(70,73)))
      #  pygame.draw.polygon(self.image,(55,247,244),((25,35),(70,35),(70,40),(25,40)))
        #pygame.draw.polygon(self.image,(255,0,0),((60,40),(70,60),(60,50),(60,40),(60,40)))
        #pygame.draw.circle(self.image,(0,0,255),(50,50),30)

        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        if self.number == 0:
            self.image = Zviewer.images["player1"]
        elif self.number == 1:
            self.image = Zviewer.images["player2"]

        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.mass = 200

    def switch(self):
        self.switch_number += 1
        if self.switch_number == len(self.weapons ):
            self.switch_number = 0
        self.active_weapon = self.weapons[self.switch_number]
        print(self.active_weapon)

    def shoot(self):
        #Flytext(x=600, y=300, text="ciao Cesare",dx = 20,dy = 0)
        Zviewer.shot.play()
        # create a new vector (a copy, but not the same, as the pos vector of spaceship)
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        a = self.angle
        # launch rocktet not from middle of spaceship, but from it's nose (rightmost point)
        # we know that from middle of spaceship to right edge ("nose") is 25 pixel
        t = pygame.math.Vector2(-25,25)
        t.rotate_ip(self.angle)
        # player1 has a second cannon
        t1 = pygame.math.Vector2(-25,-25)
        t1.rotate_ip(self.angle)
        if self.ammotime > self.age:
            delta_angle = [-3,-2,-1,0,1,4,6]
        else:
            delta_angle = [0]
        for da in delta_angle:
            v = pygame.math.Vector2(500,0)
            v.rotate_ip(self.angle+da)
            v += self.move # adding speed of spaceship to rocket

            if self.active_weapon == "default":
                for x in range(self.shots):
                    #pygame.mixer.music.play(shot)
                    Rocket(pos=p+t, move=v, angle=a+da,bossnumber = self.number)
                    #if self.number == 0:
                    Rocket(pos=p+t1, move=v, angle=a,bossnumber = self.number)

            if self.active_weapon == "superbullet":
                for x in range(self.shots):
                    #pygame.mixer.music.play(shot)
                    SuperRocket(pos=p+t, move=v, angle=a,bossnumber = self.number)
                    #if self.number == 0:
                    SuperRocket(pos=p+t1, move=v, angle=a,bossnumber = self.number)




class Smoke(VectorSprite):

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25),
                           int(self.age*3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        if self.gravity is not None:
            self.move += self.gravity * seconds
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, self.pos.y)
        c = int(self.age * 100)
        c = min(255,c)
        self.color=(c,c,c)

class Zombie(VectorSprite):
    """generic zombie.
       goes to middle of screen"""

    def _overwrite_parameters(self):
        # --- pos ----
        a = random.randint(1,4)
        if a==1:
            # --- oben ---
            y = -20
            x = random.randint(0, Zviewer.width)
        elif a == 2:
            # ---- rechts ----
            x = Zviewer.width - 20
            y = random.randint(-Zviewer.height, 0)
        elif a == 3:
            #  --- unten ---
            y = -Zviewer.height + 20
            x = random.randint(0,Zviewer.width)
        else:
            # --- links ---
            y = random.randint(-Zviewer.height, 0)
            x = 20
        self.pos=pygame.math.Vector2(x,y)
        # ---- move ---
        # vector von self.pos zur mitte
        mitte = pygame.math.Vector2(Zviewer.width / 2, - Zviewer.height / 2)
        rechts = pygame.math.Vector2(1,0)
        speed = random.randint(15, 30)
        diff = mitte - self.pos
        a = rechts.angle_to(diff)
        rechts *= speed
        #print("Recgts", rechts)
        rechts.rotate_ip(a)
        self.move = rechts
        #self.kill_on_edge = True
        self.bounce_on_edge = True
        self.max_age = random.randint(30,90)
        self.radius = random.randint(10, 25)
        self.hitpoints = self.radius / 2
        self.mass = self.radius * 50


    def kill(self):
        Explosion(self.pos, maxspeed=300,minspeed=200, color=(200,0,0))
        VectorSprite.kill(self)


    def create_image(self):
        self.image = Zviewer.images["zombiedefault"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

        # look into direction of moving
        angle = pygame.math.Vector2(1,0).angle_to(self.move)
        self.set_angle(angle)




class Zombie_Berserker(Zombie):
    """shoots around randomly without aiming.
       runs around randomly"""


    def _overwrite_parameters(self):
        Zombie._overwrite_parameters(self)
        self.p_shooting = 0.07

    def kill(self):
        Explosion(self.pos, color=(200,200,200))
        VectorSprite.kill(self)


    def create_image(self):
        self.image = Zviewer.images["zombieberserker"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        # look into direction of moving
        #angle = pygame.math.Vector2(1,0).angle_to(self.move)
        #self.set_angle(angle)



    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #casual = random.randint(1,2)
        # richtungswechsel
  #      print(self.time_wait)

        #pygame.transform.rotate(self.image,3)

        if random.random() < 0.02:
                self.move.rotate_ip(random.randint(0,360))
        # ballern
        if random.random() < self.p_shooting:
            v = pygame.math.Vector2(100,0)
            a = random.randint(0,360)
            #pygame.transform.rotate(self.image,3)

            v.rotate_ip(a)
            v += self.move # adding speed of spaceship to rocket
            # create a new vector (a copy, but not the same, as the pos vector of spaceship)
            p = pygame.math.Vector2(self.pos.x, self.pos.y)
            # launch rocktet not from middle of spaceship, but from it's nose (rightmost point)
            # we know that from middle of spaceship to right edge ("nose") is 25 pixel
            #t = pygame.math.Vector2(-25,25)
            #t.rotate_ip(self.player1.angle)
            #t1 = pygame.math.Vector2(-25,-25)
            #t1.rotate_ip(self.player1.angle)
            #Rocket(pos=p+t, move=v, angle=a,bossnumber = self.player1.number)
            Rocket_Enemy(pos=p, move=v, angle=a, bossnumber = self.number, max_distance=150)
            #Rocket_Enemy(pos=p, move=v, angle=a, bossnumber = z.number)
        if random.random() < 0.01:
         #   print("alt", self.p_shooting)
            self.p_shooting *= 1.1
          #  print("neu",self.p_shooting)
        #self.time_wait += 0.1
        # look into direction of moving
        angle = pygame.math.Vector2(1,0).angle_to(self.move)
        self.set_angle(angle)


        #if self.time_wait > 0.3:
        #    self.time_wait = 0.01


        #else:
        #    self.x += 100
#class :


class Zombie_Warrior(Zombie):

    """ hunting player """

    def create_image(self):
        #c = random.choice( (64,64,64), (128,128,128),        )
       # self.image = pygame.Surface((self.radius*2,self.radius*2))
        #pygame.draw.circle(self.image, (255,0,0),(self.radius,self.radius),self.radius )
        #self.image.set_colorkey((0,0,0))
        #self.image.convert_alpha()
        self.image = Zviewer.images["zombiewarrior"]
        self.image0 = self.image.copy()
        #non usare# self.image = pygame.image.load("enemy1.png")
        self.rect = self.image.get_rect()

    def kill(self):
        Explosion(self.pos, maxspeed=400,minspeed=100,color=(180,220,230),sparksmin=100,sparksmax=200)
        VectorSprite.kill(self)


    def update(self, seconds):
        VectorSprite.update(self, seconds)
        # --- einen zufälligen Player verfolgen ----
        players = []
        for nr in [0,1]:
            if nr in VectorSprite.numbers:
                 players.append(VectorSprite.numbers[nr])

        if len(players) > 0 and random.random() < 0.01:
            target = random.choice(players)
            diffvector =  target.pos - self.pos
            print("new move:", diffvector, self.pos, target.pos)
            diffvector.normalize_ip()
            self.move = diffvector * 100

        # look into direction of moving
        angle = pygame.math.Vector2(1,0).angle_to(self.move)
        self.set_angle(angle)


class Zombie_Boss(Zombie):

    """  shoots randomly and spawn random spaceships( Zombie,Zombie_Berserker) """

    def create_image(self):
        self.image = Zviewer.images["zombieboss"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def kill(self):
        Explosion(self.pos, maxspeed=400,minspeed=100,color=(180,220,230),sparksmin=100,sparksmax=200)
        VectorSprite.kill(self)


    def update(self, seconds):
        VectorSprite.update(self, seconds)
        # --- einen zufälligen Player verfolgen ----
        players = []
        for nr in [0,1]:
            if nr in VectorSprite.numbers:
                 players.append(VectorSprite.numbers[nr])

        if len(players) > 0 and random.random() < 0.01:
            target = random.choice(players)
            diffvector =  target.pos - self.pos
            print("new move:", diffvector, self.pos, target.pos)
            diffvector.normalize_ip()
            self.move = diffvector * 10

        # look into direction of moving
        angle = pygame.math.Vector2(1,0).angle_to(self.move)
        self.set_angle(angle)

        #spawn random zombies
        if random.random() < 0.2:
            Zombie_Berserker()

        if random.random() < 0.5:
            Zombie()








class Rocket_Enemy(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1
        self.kill_on_edge = True
        self.damage = 1

    def create_image(self):
        #self.image = Zviewer.images["bullet"]
        self.image = pygame.Surface((10,5))
        #pygame.draw.rect(self.image, (255,255,0), (0,2, 8,3),0)
        #pygame.draw.line(self.image, (220,220,0), (0,3),(10,3),2)
        pygame.draw.polygon(self.image, (255,1,1),
                            [(0,0), (7,0), (9,2), (9,3), (7, 4), (0,4)]
                           )
        #self.image.fill((255,255,0))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Rocket(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1
        self.kill_on_edge = True
        self.damage = 200

    def create_image(self):
        #self.image = Zviewer.images["bullet"]
        self.image = pygame.Surface((10,5))
        #pygame.draw.rect(self.image, (255,255,0), (0,2, 8,3),0)
        #pygame.draw.line(self.image, (220,220,0), (0,3),(10,3),2)
        pygame.draw.polygon(self.image, (255,255,0),
                            [(0,0), (7,0), (9,2), (9,3), (7, 4), (0,4)]
                           )
        #self.image.fill((255,255,0))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()


class SuperRocket(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1
        self.kill_on_edge = True
        self.damage = 10

    def create_image(self):

        #self.image = Zviewer.images["bullet"]
        self.image = pygame.Surface((20,8))
        #pygame.draw.rect(self.image, (255,255,0), (0,2, 8,3),0)
        #pygame.draw.line(self.image, (220,220,0), (0,3),(10,3),2)
        pygame.draw.polygon(self.image, (25,25,25),
                            [(0,0), (15,0), (20,4), (15,8), (0, 8), (0,0)]
                           )
        #self.image.fill((255,255,0))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

class Ammo(Zombie):


    def create_image(self):
        self.image = Zviewer.images["ammo"]
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def kill(self):
        VectorSprite.kill(self)

    #def power(self):
      #  pass
     #  self.timer = time.time()
        #self.time = (self.timer()) - time.time()) / -1
#       if self.time < 10:
#           p.

class Money(Zombie):

    def create_image(self):
        self.image = Zviewer.images["money"]
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    def kill(self):
        VectorSprite.kill(self)

class Zviewer(object):
    width = 0
    height = 0
    world_width = 10000
    world_heigth = 10000

    def __init__(self, width=640, height=400, fps=120):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        global screen
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        Zviewer.width = width    # make global readable
        Zviewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.image.load("back.png")#pygame.Surface(self.screen.get_size()).convert()
        #self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.wave = 0
        # ------ background images ------
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                        self.backgroundfilenames.append(file)
            random.shuffle(self.backgroundfilenames) # remix sort order
        except:
            print("no folder 'data' or no jpg files in it")
        #if len(self.backgroundfilenames) == 0:
        #    print("Error: no .jpg files found")
        #    pygame.quit
        #    sys.exit()
        Zviewer.bombchance = 0.015
        Zviewer.rocketchance = 0.001
       # Zviewer.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        Zviewer.images = {}
        self.load_images()
        self.paint()
        self.loadbackground()
        self.prepare_sounds()
        Game.menuitems = Game.mainmenu[:]
        Game.cursor = 0
        Game.language = "english"

    def load_images(self):
        Zviewer.images["player1"] = pygame.image.load("player1.png").convert_alpha()
        Zviewer.images["player2"] = pygame.image.load("player2.png").convert_alpha()
        
        Zviewer.images["zombiewarrior"] = pygame.image.load("enemy1.png").convert_alpha()
        Zviewer.images["zombieberserker"] = pygame.image.load("spaceship1-Black.png").convert_alpha()
        Zviewer.images["zombiedefault"] = pygame.image.load("spaceship1-orange.png").convert_alpha()
        Zviewer.images["zombieboss"] = pygame.image.load("redboss.png").convert_alpha()
        Zviewer.images["ammo"] = pygame.image.load("ammo.png").convert_alpha()
        Zviewer.images["money"] = pygame.image.load("money.png").convert_alpha()


        ## resize all to 100,100
        for i in Zviewer.images.keys():
            if "player" in i:
                Zviewer.images[i] = pygame.transform.scale(Zviewer.images[i], (100,100))

    def loadbackground(self):

        try:
            self.background = pygame.image.load("back.png")
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white

        self.background = pygame.transform.scale(self.background,
                          (Zviewer.width,Zviewer.height))
        self.background.convert()


    def prepare_sounds(self):
        # music
        Zviewer.shot = pygame.mixer.Sound(os.path.join("data","novashot.wav"))


    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.tracergroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()
        self.enemygroup  = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.rocketenemygroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.wavescreengroup = pygame.sprite.Group()
        self.flytextgroup = pygame.sprite.Group()
        self.cloudgroup = pygame.sprite.Group()
        self.powerupsgroup = pygame.sprite.Group()
        Player.groups = self.allgroup, self.playergroup
        Mouse.groups = self.allgroup, self.mousegroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Rocket_Enemy.groups = self.allgroup, self.rocketenemygroup
        SuperRocket.groups = self.allgroup, self.rocketgroup
        Cloud.groups = self.allgroup, self.cloudgroup
        Ammo.groups  = self.allgroup, self.powerupsgroup
        Money.groups = self.allgroup, self.powerupsgroup
        VectorSprite.groups = self.allgroup
        WaveScreen.groups = self.allgroup , self.wavescreengroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Zombie_Warrior.groups = self.allgroup, self.enemygroup
        Zombie.groups = self.allgroup, self.enemygroup
        Zombie_Berserker.group = self.allgroup , self.enemygroup




        # ------ player1,2,3: mouse, keyboard, joystick ---
        #self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        #self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        #self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        #self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        #self.mouse5 = Mouse(control="joystick2", color=(255,255,255))

        self.player1 =  Player(warp_on_edge=True, pos=pygame.math.Vector2(Zviewer.width/2,-Zviewer.height/2))
        #self.player2 =  Player(warp_on_edge=True, pos=pygame.math.Vector2(Zviewer.width/2+100,-Zviewer.height/2))
        for _ in range(3000):
            Cloud()



    def superschuss(self, player):
        self.supertime = 0
        v = pygame.math.Vector2(100,0)
        v.rotate_ip(player.angle)
        v += player.move # adding speed of spaceship to rocket
        # create a new vector (a copy, but not the same, as the pos vector of spaceship)
        p = pygame.math.Vector2(player.pos.x, player.pos.y)
        a = player.angle
        # launch rocktet not from middle of spaceship, but from it's nose (rightmost point)
        # we know that from middle of spaceship to right edge ("nose") is 25 pixel
        t = pygame.math.Vector2(50,0)
        t.rotate_ip(player.angle)
        SuperRocket(pos=p+t, move=10, angle=a, bossnumber = player.number, damage = self.supertime * 2)


    def new_wave(self):
        self.wave += 1
        Flytext(pos=pygame.math.Vector2(Zviewer.width//2, Zviewer.height // 2),
                move=pygame.math.Vector2(0, -10),
                text="Approaching wave {}".format(self.wave), 
                color=(200,0,0),
                fontsize = 15
                )
        if self.wave > 2:
            for b in range(1, self.wave - 1 ):
                Zombie_Boss()


    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        self.supertime = 0
        self.points = 0
        self.activeplayer = self.player1
        self.new_wave()
        self.money = 0
        while running:

            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            pygame.display.set_caption("player1 hp: {}  MONEY $: {} ".format(self.player1.hitpoints ,self.money))
            if gameOver:
                if self.playtime > exittime:
                    break
            #Game over?
            #if not gameOver:
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # ------ menu -----
                    if event.key == pygame.K_m:
                        self.menurun()
                    # ---- shooting rockets for player1 ----
                    if event.key == pygame.K_TAB:
                        self.player1.shoot()

                    # ---- shooting superrockets for player1 ----
                    # press and hold 3 seconds
                    if event.key == pygame.K_LSHIFT:
                        self.supertime = 0
                        self.supertime += seconds
                        if self.supertime > 3:
                            self.superschuss(self.player1)
                    else:
                        if self.supertime > 0:
                            self.superschuss(self.player1)
                            self.supertime = 0

                    # ---- shooting rockets for player2 ----
                    #if event.key == pygame.K_SPACE:
                    #   self.player2.shoot()

                    # ---- switching weapon for player1
                    if event.key == pygame.K_c:
                        self.player1.switch()

                    # ---- switching weapon for player2
                    #if event.key == pygame.K_x:
                    #   self.player2.switch()

                    if event.key == pygame.K_z:
                        Zombie()
                        Cloud()



                    # ---- stop movement for self.player1 -----
                    if event.key == pygame.K_r:
                        self.player1.move *= 0.1 # remove 90% of movement

            # ---- new bullets for enemies ----
            #for z in self.enemygroup:






            #---- new zombies -----
            if random.random() < 0.025:
                Zombie()

            if random.random() < 0.020:
                Zombie_Berserker()

            if random.random() < 0.01:
                Zombie_Warrior()

            #---- new power up ----
            if random.random() < 0.008:
                Ammo()

            if random.random() < 0.05:
                Money()


            pointsboth = self.player1.points #+ self.player2.points)
            if pointsboth > 0 and pointsboth % 15 == 0:
                self.new_wave()
                self.player1.points += 1
                #self.player2.points += 1



            # delete everything on screen
            self.screen.blit(self.background, (0, 0))

            # ------ move indicator for self.player1 -----
            pygame.draw.circle(self.screen, (0,255,0), (100,100), 100,1)
            glitter = (0, random.randint(128, 255), 0)
            pygame.draw.line(self.screen, glitter, (100,100),
                            (100 + self.player1.move.x, 100 - self.player1.move.y))


            # --- line from eck to mouse ---
            #pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.player1.pos.x, -self.player1.pos.y), (self.mouse1.x, self.mouse1.y))

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()


            # if pressed_keys[pygame.K_LSHIFT]:
            # ---- movement for player1 ----
            moving = False
            vel1 = 5
            if pressed_keys[pygame.K_a]:
                self.player1.rotate(vel1)
                moving = True
            if pressed_keys[pygame.K_d]:
                self.player1.rotate(-vel1)
                moving = True
            if pressed_keys[pygame.K_w]:
                # forward
                v = pygame.math.Vector2(vel1,0)
                v.rotate_ip(self.player1.angle)
                #self.player1.move += v
                for sprite in self.allgroup:
                    if sprite.number == 0:
                        continue # not for player
                    sprite.move += -v
                    
            if pressed_keys[pygame.K_s]:
                v = pygame.math.Vector2(vel1,0)
                v.rotate_ip(self.player1.angle)
                #self.player1.move += v
                for sprite in self.allgroup:
                    if sprite.number == 0:
                        continue # not for player
                    sprite.move += v
                    
                    
                    
            if not moving:
                self.player1.move = pygame.math.Vector2(0,0)

            # if pressed_keys[pygame.K_LSHIFT]:
            # ---- movement for player2 ----
            #moving2 = False
            #vel2 = 5
            #if pressed_keys[pygame.K_LEFT]:
            #    self.player2.rotate(vel2)
            #   moving2 = True
            #if pressed_keys[pygame.K_RIGHT]:
            #    self.player2.rotate(-vel2)
            #    moving2 = True
            #if pressed_keys[pygame.K_UP]:
            #    v = pygame.math.Vector2(vel2,0)
            #   v.rotate_ip(self.player2.angle)
            #    self.player2.move += v
            #    moving2 = True
            #if pressed_keys[pygame.K_DOWN]:
            #    v = pygame.math.Vector2(vel2,0)
            #   v.rotate_ip(self.player2.angle)
            #    self.player2.move += -v
            #    moving2 = True

            #if not moving2:
            #    self.player2.move = pygame.math.Vector2(0,0)


            # ------ mouse handler ------
           # left,middle,right = pygame.mouse.get_pressed()
            #if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
            #if right:
            #    self.launchRocket(pygame.mouse.get_pos())
            #oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            #mouses = [self.mouse4, self.mouse5]
            #for number, j in enumerate(self.joysticks):
            #    if number == 0:
            #       x = j.get_axis(0)
            #       y = j.get_axis(1)
            #       mouses[number].x += x * 20 # *2
            #       mouses[number].y += y * 20 # *2
            #       buttons = j.get_numbuttons()
            #       for b in range(buttons):
            #           pushed = j.get_button( b )
                       #if b == 0 and pushed:
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #elif b == 1 and pushed:
                       #    if not self.mouse4.pushed:
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #        mouses[number] = True
                       #elif b == 1 and not pushed:
                       #    mouses[number] = False
            #pos1 = pygame.math.Vector2(pygame.mouse.get_pos())
            #pos2 = self.mouse2.rect.center
            #pos3 = self.mouse3.rect.center

            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)
            self.allgroup.update(seconds)

            # --------- collision detection between player and rocket -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
                             False, pygame.sprite.collide_rect)
                for r in crashgroup:
                    if r.bossnumber != p.number:
                        p.hitpoints -= r.damage
                        r.kill()

            # --------- collision detection between player and power up ammo/Money ------
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.powerupsgroup,
                             False, pygame.sprite.collide_mask)
                for u in crashgroup:
                    print("crashgroup", u)
                    what = u.__class__.__name__ 
                    if what == "Ammo":
                        p.ammotime = p.age + 10
                    elif what == "Money":
                        self.money += 10
                    u.kill()



            # --------- collision detection between player and enemy_rocket -----
            for r in self.rocketenemygroup:
                crashgroup = pygame.sprite.spritecollide(r, self.playergroup,
                             False, pygame.sprite.collide_mask)

                for p in crashgroup:
                    p.hitpoints -= 0.5

            # --------- collision detection between enemies and rocket -----
            for e in self.enemygroup:
                crashgroup = pygame.sprite.spritecollide(e, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                #print("collided!")
                for r in crashgroup:
                #   if r.__class__.__name__ == "Rocket":
                    e.hitpoints -= r.damage
                    Explosion(e.pos, color=(255,0,0), sparksmin=2, sparksmax=3)
                    elastic_collision(r, e)

                    if e.hitpoints <= 0:
                        #print("coll:", r.bossnumber, self.player1.number, self.player2.number)
                        if r.bossnumber == self.player1.number:
                            self.player1.points += 1

                        elif r.bossnumber == self.player2.number:
                            self.player2.points += 1

                    self.money += 1

                    r.kill()
                    #e.kill()


            # --------- collision detection between enemy and other enemy -----
            for e in self.enemygroup:
                crashgroup = pygame.sprite.spritecollide(e, self.enemygroup,
                             False, pygame.sprite.collide_circle)
                for e_other in crashgroup:
                    elastic_collision(e,e_other)

            # --------- collision detection between player and enemy -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.enemygroup,
                             False, pygame.sprite.collide_mask)
                #print("collided!")
                for e in crashgroup:
                    p.hitpoints -= 1
                    e.hitpoints -= random.randint(5,10)
                  #  elastic_collision(p,e)
                    p.points += 1
                    print(p.points)
                    #e.kill()
                    #p.kill()

            # --------- collision detection player1 and player2  -----
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.playergroup,
                             False, pygame.sprite.collide_mask)
                #print("collided!")
                for r in crashgroup:
                    if p.number < r.number:
                        #e.hitpoints -= r.damage
                        elastic_collision(r, p)
                        # r.kill()



            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            # self.wavescreengroup.draw(self.screen)
            #self.wavescreengroup.draw(self.screen)
            # ---- move vectors for caesare ---

        #    for s in self.allgroup:
         #       print(s.pos)
          #      x1, y1 = s.pos.x, -s.pos.y
           #     ab = s.pos + s.move
            #    x2, y2 = ab.x, -ab.y
             #   pygame.draw.line(self.screen, (0,0,64), (x1,y1), (x2, y2))

            # --- Martins verbesserter Mousetail -----
            #for mouse in self.mousegroup:
            #    if len(mouse.tail)>2:
            #        for a in range(1,len(mouse.tail)):
            #            r,g,b = mouse.color
            #            pygame.draw.line(self.screen,(r-a,g,b),
            #                         mouse.tail[a-1],
            #                         mouse.tail[a],10-a*10//10)

            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)
        pygame.quit()

    def startmenu(self):
        pass

    def menurun(self):
        """The mainloop only for the menu"""
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            #self.playtime += seconds
            pygame.display.set_caption("player1 hp: {} player2 hp: {}" .format(self.player1.hitpoints, self.player2.hitpoints))
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_DOWN:
                        Game.cursor += 1
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_UP:
                        Game.cursor -= 1
                    if event.key == pygame.K_RETURN:
                        # ----- menü auswertung -----
                        command = Game.menuitems[Game.cursor]
                        if command == "quit":
                            running = False
                        if command == "back":
                            #if Game.menuitems == Game.optionsmenu:
                            Game.menuitems = Game.mainmenu[:]
                            #elif Game.menuitems == Game.languagemenu:
                            #
                            #Game.menuitems = Game.optionsmenu[:]
                        if command == "options":
                            Game.menuitems = Game.optionsmenu[:]
                        if command == "upgrade player1":
                            Game.menuitems = Game.upgrademenu[:]
                            self.activeplayer = self.player1
                            Flytext(x=600, y=300, text="ciao Cesare",dx = 20,dy = 0)
                        if command == "upgrade player2":

                            Game.menuitems = Game.upgrademenu[:]
                            self.activeplayer = self.player2
                        if command == "language":
                            Game.menuitems = Game.languagemenu[:]
                        if command == "italian":
                            Game.language = "italian"
                        if command == "english":
                            #Flytext(200,200,text="you´re already in english",color=(255,0,0))
                            Game.language = "english"
                        if command == "german":
                            Game.language = "german"
                        # --- upgrade player ----
                        if command == "shots":
                            if self.activeplayer.shots <= 5:
                               self.activeplayer.shots += 1
                               print(self.activeplayer.shots)
                            else:
                                Flytext(500,300, "maximal number of shots already bought")
                        if command == "health":
                            self.activeplayer.hitpoints += 10
                            print(self.activeplayer.hitpoints)
                        if command == "damage":
                            self.activeplayer.damage += 2

                        if command == "speed":
                            self.activeplayer.speed += 1
                            print(self.activeplayer.speed)
                        
                        #improving player1 spaceship 
                        if command == "spaceship":
                            Game.menuitems = Game.spaceshipmenu[:]
                           
                        if command == "spaceship1":
                            pass
                            #self.activeplayer.image = 


                    #   if command == "



            # --- limit cursor ---
            if Game.cursor < 0:
                Game.cursor = 0
            if Game.cursor >= len(Game.menuitems):
                Game.cursor = len(Game.menuitems) - 1

            # delete everything on screen
            self.screen.blit(self.background, (0, 0))

            # ---- background for menu -----
            pygame.draw.rect(self.screen, (144,238,144), (0, 0, self.width, self.height))

            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)
            write(self.screen, "Menu", x= 600, y=20, fontsize=50)


            # --- write menuitems ----
            for nr, item in enumerate(Game.menuitems):
                if Game.language == "english":
                    i = item
                elif Game.language == "german":
                    i = Game.deutsch[item]
                elif Game.language == "italian":
                    i = Game.italiano[item]
                write(self.screen, i, x=400, y=200+50*nr, fontsize=75,color=(70,144,255))
            # --- write cursor ----
            write(self.screen, "-->", x= 300, y=205+50*Game.cursor, fontsize=50,color=(0,0,255))
            # --------- upgrade -----
            #self.allgroup.update(seconds)
            self.flytextgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            #self.allgroup.draw(self.screen)
            self.flytextgroup.draw(self.screen)

            self.wavescreengroup.draw(self.screen)

            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        #pygame.mouse.set_visible(True)
        #pygame.quit()



if __name__ == '__main__':
    Zviewer(1430,800).run() # try Zviewer(800,600).run()
