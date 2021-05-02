import math
import random
from math import sin, cos, pi
import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BULLET_MAX = 4096
MYSPEED = 1
pal = [0xF8F5E5, 0xE1DECC, 0x291B17, 0x754D42, 0x1D4F7A, 0x3080C7, 0x2A7C9B, 0x46B3C2, 0x9678b6, 0x907fbe, 0x7e90ce, 0x66a6d9, 0x5dbada, 0x6dcbd4, 0x83d5ce, 0x8dd9cc]

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Pullette", palette = pal)
        pyxel.mouse(True)
        pyxel.image(0).load(0, 0, "assets/me.png")
        pyxel.image(1).load(0, 0, "assets/mom.png")

        self.start = True
        self.wait = False
        self.view = False
        self.mother = Mother()
        self.me = Me()
        self.randvar = Randvar()
        self.bullets = []
        self.spells = {0:'POLYGON ROTATION',
                        1:'POLYGON ROTATION+BULLET CURVE&ACCELERATION',
                        2:'TROCHOID',
                        3:'LISSAJOUS CURVE',
                        4:'ROSE CURVE',
                        5:'N-WAY+BULLET CURVE',
                        6:'N-WAY SIN WAVE',
                        7:'BROKEN ROSE',
                        8:'INNER POLIGON ROTATION',
                        9:'DEBUG'}
        self.miss = 0

        pyxel.run(self.update, self.draw)

    def mymove(self): #keyboard
#      move_x = pyxel.mouse_x
#      move_y = pyxel.mouse_y
        if not (self.wait or self.start):
            if pyxel.btn(pyxel.KEY_SPACE):
                self.me.me_v = 1
            if not pyxel.btn(pyxel.KEY_SPACE):
                self.me.me_v = 2
            if (pyxel.KEY_RIGHT or pyxel.KEY_LEFT) and (pyxel.KEY_DOWN or pyxel.KEY_UP):
                self.me.me_v = self.me.me_v/math.sqrt(2)
            if pyxel.btn(pyxel.KEY_RIGHT):
                if self.me.me_x < SCREEN_WIDTH:
                    self.me.update(self.me.me_x+self.me.me_v, self.me.me_y, self.me.me_v)
            if pyxel.btn(pyxel.KEY_LEFT):
                if self.me.me_x > 0:
                    self.me.update(self.me.me_x-self.me.me_v, self.me.me_y, self.me.me_v)
            if pyxel.btn(pyxel.KEY_DOWN):
                if self.me.me_y < SCREEN_HEIGHT:
                    self.me.update(self.me.me_x, self.me.me_y+self.me.me_v, self.me.me_v)
            if pyxel.btn(pyxel.KEY_UP):
                if self.me.me_y > 0:
                    self.me.update(self.me.me_x, self.me.me_y-self.me.me_v, self.me.me_v)

    def spiral(self, x, y, n, l, col):
        t = pi*l/n
        newb = Bullet(x, y, 1, t, 2, col)
        self.bullets.append(newb)

    def gswirl(self, x, y, n, m, l):
        t = [pi*((l/n)+(f/m))*2 for f in range(m)]
        if self.randvar.c%3 == 0:
            newbs = [Bullet(x, y, 1, angle, 1, (l%8)+8) for angle in t]
        elif self.randvar.c%3 == 1:
            newbs = [Bullet(x, y, 1, angle, 1, round(11.5+3.5*sin(pyxel.frame_count/60*2*pi))) for angle in t]
        else:
            newbs = [Bullet(x, y, 1, angle, 1, 1+(l%2)) for angle in t]
        for i in newbs:
                self.bullets.append(i)

    def nway(self, x, y, f, v, col):
        t = [pi*(g/f)*2 for g in range(f)]
        newbs = [Bullet(x, y, v, angle, 2, col) for angle in t]
        for i in newbs:
                self.bullets.append(i)

    def swirl(self, x, y, n, m, l, col):
        t = [pi*((l/n)+(f/m))*2 for f in range(m)]
        newbs = [Bullet(x, y, 1, angle, 3, col) for angle in t]
        for i in newbs:
                self.bullets.append(i)
    
    def circle(self, x, y, f, col, s):
        newbs = [Bullet(x, y, 1, pi/f*n*2, s, col) for n in range(f)]
        for i in newbs:
            self.bullets.append(i)

    def surround(self, x, y, f, l, dt):
        angle = 2*pi/f
        newbs = [Bullet(x+l*cos(angle*n+dt), y+l*sin(angle*n+dt), 0, angle*n+dt, 1, 1) for n in range(f)]
        for i in newbs:
            self.bullets.append(i)
    
    def troch(self, a, b, e, col):
        d = 512
        p = pi*12
        if self.randvar.c%2 == 0:
            newbs = [Bullet(self.mother.mom_x+24*((a-b)*sin(p/d*n)+e*cos((a-b)/b*p/d*n)), 
                    self.mother.mom_y+24*((a-b)*cos(p/d*n)-e*sin((a-b)/b*p/d*n)),
                    1, p/d*n*2, 0, round(n/24)%8+8) for n in range(d)]
        else:
            newbs = [Bullet(self.mother.mom_x+24*((a-b)*sin(p/d*n)+e*cos((a-b)/b*p/d*n)), 
                    self.mother.mom_y+24*((a-b)*cos(p/d*n)-e*sin((a-b)/b*p/d*n)),
                    1, p/d*n*2, 0, col) for n in range(d)]
        for i in newbs:
            self.bullets.append(i)

    def troch_d(self, a, b, e, col, l):
        p = pi*24*l
        newb = Bullet(self.mother.mom_x+24*((a-b)*sin(p)+e*cos((a-b)/b*p)), 
                self.mother.mom_y+24*((a-b)*cos(p)-e*sin((a-b)/b*p)),
                1, p*2, 0, col)
        self.bullets.append(newb)

    def epitroch(self, a, b, e, col):
        d = 512
        p = pi*12
        if self.randvar.c%2 == 0:
            newbs = [Bullet(self.mother.mom_x+24*((a+b)*sin(p/d*n)-e*cos((a+b)/b*p/d*n)), 
                    self.mother.mom_y+24*((a+b)*cos(p/d*n)-e*sin((a+b)/b*p/d*n)),
                    1, p/d*n*2, 0, round(n/24)%8+8) for n in range(d)]
        else:
            newbs = [Bullet(self.mother.mom_x+24*((a+b)*sin(p/d*n)-e*cos((a+b)/b*p/d*n)), 
                    self.mother.mom_y+24*((a+b)*cos(p/d*n)-e*sin((a+b)/b*p/d*n)),
                    1, p/d*n*2, 0, col) for n in range(d)]
        for i in newbs:
            self.bullets.append(i)

    def epitroch_d(self, a, b, e, col, l):
        p = pi*24*l
        newb = Bullet(self.mother.mom_x+24*((a+b)*sin(p)-e*cos((a+b)/b*p)), 
                self.mother.mom_y+24*((a+b)*cos(p)-e*sin((a+b)/b*p)),
                1, p*2, 0, col)
        self.bullets.append(newb)

    def lissa(self, a, b, c, d, col):
        f = 256
        p = pi*8
        if self.randvar.e%2 == 0:
            newbs = [Bullet(self.mother.mom_x+a*sin(p/f*n*c), 
                    self.mother.mom_y+b*cos(p/f*n*d),
                    1, p/f*n*2, 1, n%8+8) for n in range(f)]
        else:
            newbs = [Bullet(self.mother.mom_x+a*sin(p/f*n*c), 
                    self.mother.mom_y+b*cos(p/f*n*d),
                    1, p/f*n*2, 1, col) for n in range(f)]
        for i in newbs:
            self.bullets.append(i)

    def lissa_d(self, a, b, c, d, col, l):
        p = pi*8*l
        newb = Bullet(self.mother.mom_x+a*sin(p*c*l), 
                self.mother.mom_y+b*cos(p*d*l),
                0, p*2*l, 0, col)
        self.bullets.append(newb)

    def rose(self, a, b, col):
        c = 512
        p = pi*16
        if self.randvar.e%2 == 0:
            newbs = [Bullet(self.mother.mom_x+36*(sin(a/b*p/c*n)*cos(p/c*n)), 
                    self.mother.mom_y-36*(sin(a/b*p/c*n)*sin(p/c*n)),
                    1, p/c*n*2, 0, col) for n in range(c)]
        else:
            newbs = [Bullet(self.mother.mom_x+36*(sin(a/b*p/c*n)*cos(p/c*n)), 
                    self.mother.mom_y-36*(sin(a/b*p/c*n)*sin(p/c*n)),
                    1, p/c*n*2, 0, round(n/2)%8+8) for n in range(c)]
        for i in newbs:
            self.bullets.append(i)

    def broken_rose(self, a, b, col, dt):
        c = 512
        p = pi*dt
        if a == b:
            c = 128
        if self.randvar.e%2 == 0:
            newbs = [Bullet(self.mother.mom_x+36*(sin(a/b*p/c*n)*cos(a/b*p/c*n)), 
                    self.mother.mom_y-18+36*(sin(a/b*p/c*n)*sin(a/b*p/c*n)),
                    1, p/c*n*2, 0, round(n/dt)%8+8) for n in range(c)]
        else:
            newbs = [Bullet(self.mother.mom_x+36*(sin(a/b*p/c*n)*cos(a/b*p/c*n)), 
                    self.mother.mom_y-18+36*(sin(a/b*p/c*n)*sin(a/b*p/c*n)),
                    1, p/c*n*2, 0, col) for n in range(c)]
        for i in newbs:
            self.bullets.append(i)

    def rose_d(self, a, b, col, l):
        p = pi*8*l
        newb = Bullet(self.mother.mom_x+48*(sin(a/b*p)*cos(p)), 
                self.mother.mom_y+48*(sin(a/b*p)*sin(p)),
                1, p*2, 0, col)
        self.bullets.append(newb)

    def curve(self, bullet, count, dt):
        t = bullet.t+dt
        if bullet.count >= count:
            bullet.anglectr(t)
    
    def accel(self, bullet, count, dv):
        v = bullet.v+dv
        if bullet.count >= count:
            bullet.anglectr(v)        
    
    def mom_move(self):
        if self.mother.count % 600 == 0:
            self.mother.update()
            self.randvar.update()
            self.miss = 0
        if 1 <= self.mother.count % 600 < 540:
            if self.mother.spell == 0:
                if self.mother.count % self.randvar.itv == 0:
                    l = self.mother.loop
                    n = self.randvar.drand
                    m = self.randvar.frand
                    self.gswirl(self.mother.mom_x, self.mother.mom_y, n, m, l)
                    self.mother.loop += 1
            if self.mother.spell == 1:
                if self.mother.count % self.randvar.itv == 0:
                    l = self.mother.loop
                    n = self.randvar.drand
                    m = self.randvar.c
                    if self.randvar.d % 2 == 0:
                        self.swirl(self.mother.mom_x, self.mother.mom_y, n, m, l, round(11.5+3.5*sin(self.mother.loop/60*2*pi)))
                    else:
                        self.swirl(self.mother.mom_x, self.mother.mom_y, n, m, l, round(1.5+0.5*sin(self.mother.loop/60*2*pi)))
                    for i in self.bullets:
                        if i.new and i.count < 150:
                            i.v = 0.8+(i.count/self.randvar.itv)*self.randvar.dv
                            i.t = i.t+self.randvar.dt
#                            i.anglectr(i.t+self.randvar.dt)
#                            i.speedctr(i.v+self.randvar.dv)
                    self.mother.loop += 1
            if self.mother.spell == 2:
                eh = self.randvar.c
                a = self.randvar.a/10
                b = self.randvar.b/10
                e = self.randvar.e/10
                col = self.randvar.color
                if self.randvar.g % 2 == 0:
                    if self.mother.count % 90 == 30:
                        if eh % 2 == 0:
                            self.troch(a, b, e, col)
                        else:
                            self.epitroch(a, b, e, col)
                else:
                    l = self.mother.loop/512
                    r = -l
                    if eh % 2 == 0:
                        self.troch_d(a, b, e, col, l)
                        self.troch_d(a, b, e, col, r)
                        self.troch_d(a, b, e, col, l+1/2)
                        self.troch_d(a, b, e, col, r-1/2)
                    else:
                        self.epitroch_d(a, b, e, col, l)
                        self.epitroch_d(a, b, e, col, r)
                        self.epitroch_d(a, b, e, col, l+1/2)
                        self.epitroch_d(a, b, e, col, r-1/2)
                    for i in self.bullets:
                        if i.new:
                            if i.count == 0:
                                i.no = self.mother.loop
                                i.col = round(i.no/6)%8+8
                                i.size = 1
                            else:
                                i.size = 0
                        if i.count < 160 and i.new:
                            i.v = 0
                        else:
                            i.v = 1
                    self.mother.loop += 1 
            if self.mother.spell == 3:
                a = self.randvar.a
                b = self.randvar.b
                c = self.randvar.c
                d = self.randvar.d
                col = self.randvar.color
                if self.randvar.g % 2 == 0:
                    if self.mother.count % 60 == 50:
                        self.lissa(a, b, c, d, col)
                else:
                    a = a*4
                    b = b*4
                    l = self.mother.loop/512
                    self.lissa_d(a, b, c, d, col, l)
                    for i in self.bullets:
                        if i.new:
                            if i.count == 0:
                                i.no = self.mother.loop
                                i.col = i.no%8+8
                                i.size = 2
                            else:
                                i.size = 0
                        if i.count < 120:
                            i.v = 0
                        else:
                            i.v = 1
                    self.mother.loop += 1
            if self.mother.spell == 4:
                a = self.randvar.a
                b = self.randvar.b
                col = self.randvar.color
                if self.randvar.g % 2 == 0:
                    if self.mother.count % 90 == 60:
                        self.rose(a, b, col)
                else:
                    l = self.mother.loop/512
                    r = -l
                    self.rose_d(a, b, col, l)
                    self.rose_d(a, b, col, r)
                    self.rose_d(a, b, col, l+1/2)
                    self.rose_d(a, b, col, r-1/2)
                    for i in self.bullets:
                        if i.new:
                            if i.count == 0:
                                i.no = self.mother.loop
                                i.col = i.no%8+8
                                i.size = 1
                            else:
                                i.size = 0
                        if i.count < 240 and i.new:
                            i.v = 0
                        else:
                            i.v = 1
                    self.mother.loop += 1 
            if self.mother.spell == 5:
                itv = math.ceil(self.randvar.itv/2)
                if self.mother.count % itv == 0:
                    if self.randvar.d % 3 == 0:
                        col = round(11.5+3.5*sin(self.mother.loop/60*2*pi))
                    elif self.randvar.d % 3 == 1:
                        col = round(math.ceil(self.randvar.c/2)*2+0.5+0.5*sin((self.mother.loop+1)/60*2*pi))
                    else:
                        col = self.randvar.color
                    m = self.randvar.frand
                    l = self.mother.loop
                    v = math.floor(self.randvar.c/3)
                    if v == 0:
                        v = 1 
                    self.nway(self.mother.mom_x, self.mother.mom_y, m, v, col)
                    remb = []
                    for i in self.bullets:
                        if i.count == 0:
                            i.no = self.mother.loop
                        if i.new and i.count < 100:
                            i.anglectr(i.t+self.randvar.dt*l/200)
                        if i.new and i.count > m*5:
                            if i.no % 2 != 0:
                                remb.append(i)
                            else:
                                i.size = 1
                        if i.new and i.count > m*10 and i.no % 4 != 0:
                            remb.append(i)
                        if (not i.new) and i.no % 8 != 0:
                            remb.append(i)
                    for i in remb:
                        if i in self.bullets:
                            self.bullets.remove(i)
                    self.mother.loop += 1
            if self.mother.spell == 6:
                if self.mother.count % self.randvar.itv == 0:
                    col = self.mother.loop%8+8
                    m = self.randvar.frand
                    dt = 2*pi*(self.randvar.a/self.randvar.b)*sin(self.mother.loop*self.randvar.dt)
                    self.nway(self.mother.mom_x, self.mother.mom_y, m, 1, col)
                    for i in self.bullets:
                        if i.count == 0:
                            i.size = 1
                            i.anglectr(i.t+dt)
                    self.mother.loop += 1
            if self.mother.spell == 7:
                a = self.randvar.a
                b = self.randvar.b
                col = self.randvar.color
                if self.mother.count % 90 == 60:
                    dt = self.randvar.drand
                    self.broken_rose(a, b, col, dt)
            if self.mother.spell == 8:
                x = self.mother.mom_x
                y = self.mother.mom_y
                f = self.randvar.frand
                l = self.randvar.c*24
                itv = self.randvar.itv+1
                d = 2*pi/math.ceil(2*pi/self.randvar.dt)
                dt = d*self.mother.loop
                remb = []
                if self.randvar.g < 12:
                    g = 0
                else:
                    g = 2*pi/self.randvar.g
                waittime = math.ceil((2*pi/f)/d)*itv
                if self.mother.count % itv == 0:
                    self.surround(x, y, f, l, dt)
                    self.surround(x, y, f, l, -dt)
                    for i in self.bullets:
                        if i.count == 0:
                            i.no = self.mother.loop
                            i.t = i.t+pi+g
                        if i.count > waittime:
                            i.v = 1
                            i.col = 6
                        if i.count - waittime > l*cos(g):
                            i.col = 7
                    self.bullets.reverse()
                    self.mother.loop += 1
        if self.mother.spell == 9:
            pass
        self.mother.count += 1
        if self.mother.count % 600 == 540:
            for i in self.bullets:
                i.abandon()

    def hit(self, b):
        if math.sqrt((self.me.me_x-b.x)**2+(self.me.me_y-b.y)**2) < (b.size+1)/2 + self.me.body:
            self.miss += 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            self.start = not self.start
        if pyxel.btnp(pyxel.KEY_W):
            self.wait = not self.wait
        if pyxel.btnp(pyxel.KEY_A):
            self.start = False
            self.view = False
        if pyxel.btnp(pyxel.KEY_V):
            self.start = False
            self.view = True

        if not pyxel.btn(pyxel.KEY_ALT):
            if pyxel.btnp(pyxel.KEY_0):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 0
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_1):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 1
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_2):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 2
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_3):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 3
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_4):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 4
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_5):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 5
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_6):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 6
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_7):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 7
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_8):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 8
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

            if pyxel.btnp(pyxel.KEY_9):
                self.mother.update()
                self.randvar.update()
                self.mother.spell = 9
                self.mother.count = 1
                self.bullets = []
                self.miss = 0

        if not self.start:
            self.mymove()
            if not self.wait:
                remb = []
                self.mom_move()
                if BULLET_MAX < len(self.bullets):
                    self.bullets = [self.bullets[n-1] for n in range(BULLET_MAX)]
                for i in self.bullets:
                    i.update()
                    if i.count > 480 or ((not i.new) and (i.v == 0) and i.count > 60):
                        remb.append(i)
                    if not self.wait:
                        self.hit(i)
                for i in remb:
                    self.bullets.remove(i)

        else:
            self.start = True
            self.wait = False
            self.view = False
            self.mother = Mother()
            self.me = Me()
            self.randvar = Randvar()
            self.bullets = []
            
    def draw(self):
        pyxel.cls(0)
        if self.start:
            c = round(11.5+3.5*sin(pyxel.frame_count/120*2*pi))
            pyxel.text(113, 65, "Pullette", 1)
            pyxel.text(112, 64, "Pullette", c)
            pyxel.text(82, 72, "-bullet hell simulator-", 1)
            pyxel.text(100, 96, "A : ACTIVE MODE", 3)
            pyxel.text(100, 104, "V : VIEW MODE", 3)
            pyxel.text(100, 112, "W : WAIT", 3)
            pyxel.text(100, 120, "Q : QUIT", 3)            

        else:
            self.draw_caption()
            if not self.view:
                pyxel.blt(self.me.me_x-8, self.me.me_y-8, 0, 0, 0, 16, 16, 0)
            for i in self.bullets:
                pyxel.circ(i.x, i.y, i.size, i.col)
            if not self.view:
                pyxel.blt(self.mother.mom_x-8, 
                self.mother.mom_y-8+round(4*sin(pyxel.frame_count/120*2*pi)), 
                1, 0, 0, 16, 16, 0)
            if self.wait:
                self.draw_caption()
                if math.floor(pyxel.frame_count/16)%8 < 2:
                    pyxel.text(100, 96, "A : ACTIVE MODE", 3)
                    pyxel.text(100, 104, "V : VIEW MODE", 3)
                    pyxel.text(100, 112, "W : RETURN", 3)
                    pyxel.text(100, 120, "S : RESTART", 3)
                    pyxel.text(100, 128, "Q : QUIT", 3)

    def draw_caption(self):
        if self.wait:
            mainc = 2
            subc = 3
        else:
            mainc = 1
            subc = 1
        pyxel.text(4, 4, "{}".format(self.spells[self.mother.spell]), mainc)
        pyxel.text(212, 4, "count: {}".format(self.mother.count), mainc)
        if not self.view:
            pyxel.text(212, 12, "miss:{}".format(self.miss), mainc)
        if self.mother.spell == 0:
            pyxel.text(4, 12, "source angle:{}".format(self.randvar.frand), subc)
            pyxel.text(4, 20, "source angle diff:1/{}*2pi".format(self.randvar.drand), subc)
            pyxel.text(4, 28, "shooting interval:{}f".format(self.randvar.itv), subc)
        if self.mother.spell == 1:
            pyxel.text(4, 12, "source angle:{}".format(self.randvar.c), subc)
            pyxel.text(4, 20, "source angle diff:1/{}*2pi".format(self.randvar.drand), subc)
            pyxel.text(4, 28, "bullet angle diff:1/{:.0f}*2pi".format((2*pi)/self.randvar.dt), subc)
            pyxel.text(4, 36, "bullet velocity diff:1/{:.0f}".format(1/self.randvar.dv), subc)
            pyxel.text(4, 44, "update interval:{}f".format(self.randvar.itv), subc)
            pyxel.text(4, 52, "stop update:150f", subc)
        if self.mother.spell == 2:
            pyxel.text(4, 20, "a:{}".format(self.randvar.a/10), subc)
            pyxel.text(4, 28, "b:{}".format(self.randvar.b/10), subc)
            pyxel.text(4, 36, "c:{}".format(self.randvar.e/10), subc)
            if self.randvar.c % 2 == 0:
                pyxel.text(4, 12, "HYPOTROCHOID", subc)
                pyxel.text(4, 44, "x=({0}-{1})cos(t)+{2}cos((({0}-{1})/{1})t)".format(self.randvar.a/10, self.randvar.b/10, self.randvar.e/10), subc)        
                pyxel.text(4, 52, "y=({0}-{1})sin(t)-{2}sin((({0}-{1})/{1})t)".format(self.randvar.a/10, self.randvar.b/10, self.randvar.e/10), subc)
            else:
                pyxel.text(4, 12, "EPITROCHOID", subc)
                pyxel.text(4, 44, "x=({0}+{1})cos(T)-{2}cos((({0}+{1})/{1})T)".format(self.randvar.a/10, self.randvar.b/10, self.randvar.e/10), subc)        
                pyxel.text(4, 52, "y=({0}+{1})sin(T)-{2}sin((({0}+{1})/{1})T)".format(self.randvar.a/10, self.randvar.b/10, self.randvar.e/10), subc)
        if self.mother.spell == 3:
            pyxel.text(4, 12, "a:{}".format(self.randvar.a), subc)
            pyxel.text(4, 20, "b:{}".format(self.randvar.b), subc)
            pyxel.text(4, 28, "c:{}".format(self.randvar.c), subc)
            pyxel.text(4, 36, "d:{}".format(self.randvar.d), subc)
            pyxel.text(4, 44, "x={}cos({}t)".format(self.randvar.a, self.randvar.c), subc)        
            pyxel.text(4, 52, "y={}sin({}t)".format(self.randvar.b, self.randvar.d), subc)
        if self.mother.spell == 4:
            pyxel.text(4, 12, "a:{}".format(self.randvar.a), subc)
            pyxel.text(4, 20, "b:{}".format(self.randvar.b), subc)
            pyxel.text(4, 28, "x=sin(({}/{})t)cos(t)".format(self.randvar.a, self.randvar.b), subc)        
            pyxel.text(4, 36, "y=sin(({}/{})t)sin(t)".format(self.randvar.a, self.randvar.b), subc)
        if self.mother.spell == 5:
            v = math.floor(self.randvar.c/3)
            if v == 0:
                v = 1 
            pyxel.text(4, 12, "n:{}".format(self.randvar.frand), subc)
            pyxel.text(4, 20, "bullet velocity:{:.0f}".format(v), subc)
            pyxel.text(4, 28, "bullet angle diff:1/{:.0f}*2pi".format((2*pi)/self.randvar.dt*200), subc)
            pyxel.text(4, 36, "update interval:{}f".format(math.ceil(self.randvar.itv/2)), subc)
            pyxel.text(4, 44, "stop update:100f", subc)
        if self.mother.spell == 6:
            pyxel.text(4, 12, "n:{}".format(self.randvar.frand), subc)
            pyxel.text(4, 20, "a:{0}/{1}".format(self.randvar.a, self.randvar.b), subc)
            pyxel.text(4, 28, "b:1/{}".format(round(2*pi/self.randvar.dt)), subc)
            pyxel.text(4, 36, "bullet angle:({0}/{1})*2pi*sin(t/{2}*2pi)".format(self.randvar.a, self.randvar.b, round(2*pi/self.randvar.dt)), subc)
        if self.mother.spell == 7:
            pyxel.text(4, 12, "a:{}".format(self.randvar.a), subc)
            pyxel.text(4, 20, "b:{}".format(self.randvar.b), subc)
            pyxel.text(4, 28, "x=sin(({0}/{1})t)cos(({0}/{1})t)".format(self.randvar.a, self.randvar.b), subc)        
            pyxel.text(4, 36, "y=sin(({0}/{1})t)sin(({0}/{1})t)".format(self.randvar.a, self.randvar.b), subc)
            pyxel.text(4, 44, "dt={}/512*2pi".format(self.randvar.drand), subc)
        if self.mother.spell == 8:
            pyxel.text(4, 12, "corner:{}".format(self.randvar.frand), subc)
            pyxel.text(4, 20, "radius:{}".format(self.randvar.c*24), subc)
            pyxel.text(4, 28, "angle diff to center:2pi*1/{}".format(self.randvar.g), subc)        
            pyxel.text(4, 36, "angle diff of rotation:2pi*1/{}".format(math.ceil(2*pi/self.randvar.dt)), subc)
            pyxel.text(4, 44, "shooting interval:{}f".format(self.randvar.itv+1), subc)    

class Mother:
    def __init__(self):
        self.mom_x = SCREEN_WIDTH/2
        self.mom_y = SCREEN_HEIGHT/4
        self.count = 0
        self.loop = 0
        self.spell = 0
        self.spellno = 0
    def update(self):
        self.count = 0
        self.spell = random.randint(0, 8)
        self.spellno += 1
        self.loop = 0

class Randvar:
    def __init__(self):
        self.drand = random.randint(12, 60)
        self.frand = random.randint(3, 12)
        self.itv = random.randint(1, 6)
        self.a = random.randint(1, 24)
        self.b = random.randint(1, 24)
        self.c = random.randint(1, 6)
        self.d = random.randint(1, 6)
        self.e = random.randint(1, 16)
        self.g = random.randint(1, 36)
        self.color = random.randint(2, 15)
        self.dt = 2*pi/random.randint(24, 72)
        self.dv = 1/random.randint(60, 180)
    def update(self):
        self.drand = random.randint(12, 60)
        self.frand = random.randint(3, 12)
        self.itv = random.randint(1, 6)
        self.a = random.randint(1, 24)
        self.b = random.randint(1, 24)
        self.c = random.randint(1, 6)
        self.d = random.randint(1, 6)
        self.e = random.randint(1, 16)
        self.g = random.randint(1, 36)
        self.color = random.randint(2, 15)
        self.dt = 2*pi/random.randint(24, 72)
        self.dv = 1/random.randint(60, 180)

class Me:
    def __init__(self):
        self.me_x = SCREEN_WIDTH/2
        self.me_y = 3*SCREEN_HEIGHT/4
        self.me_v = 2
        self.body = 1.0
    def update(self, x, y, v):
        self.me_x = x
        self.me_y = y
        self.me_v = v

class Bullet:
    def __init__(self, x, y, v, t, size, col):
        self.x = x
        self.y = y
        self.v = v
        self.t = t
        self.size = size
        self.col = col
        self.count = 0
        self.new = True
        self.no = 0
    def update(self):
        self.x += self.v*cos(self.t)
        self.y += self.v*sin(self.t)
        self.count += 1
    def speedctr(self, v):
        self.v = v
    def anglectr(self, t):
        self.t = t
    def abandon(self):
        self.new = False

App()
