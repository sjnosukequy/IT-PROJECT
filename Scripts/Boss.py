import pygame
import random
import math, copy
from Scripts.Drops import BossDropHandler
from Scripts.Projectile import Soul_bullet
# from Scripts.Particles import Particles

# hit_sound = pygame.mixer.Sound('data/sfx/hit.wav')
# hit_sound.set_volume(0.2)

# Dash_sound = pygame.mixer.Sound('data/sfx/dash.wav')
# Dash_sound.set_volume(0.1)

# Fire_sound = pygame.mixer.Sound('data/sfx/fire.mp3')
# Fire_sound.set_volume(0.3)

class Boss:
    def __init__(self, game, pos, type, name, size, Health = 10000, dmg = 50, scale = 1, anim_offset=(0,0)):
        self.name = name
        self.game = game
        self.type = type
        self.health = Health
        self.health_max = Health
        self.size = list(size)
        self.anim_offset = anim_offset
        self.pos = list(pos)
        self.bound = [0,0,0,0]
        self.bound[0] = self.pos[0] + 250
        self.bound[1] = self.pos[0] - 250
        self.bound[2] = self.pos[1] + 250
        self.bound[3] = self.pos[1] - 250
        self.flip = False

        self.action = ''
        self.set_action('idle')

        self.Dir = pygame.math.Vector2()
        self.Dead = False
        self.Dead_2 = False
        self.attack_frame = 0
        self.dmg = dmg

        self.Dest = self.pos.copy()

        self.invs = 1000
        self.hurt_frame = 0

        self.cool_down = 2000
        self.cool_frame = 0

        self.Recover_cooldown = 400
        self.Recover_frame = 0

        self.Death_delay = 2500
        self.Death_frame = 0

        self.now = 0
        self.scale = scale
        self.Player_invs = 1000
    
    def DMG(self, health):
        self.health -= health
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.rect().colliderect(self.game.Player.rect()):
            if self.game.Player.is_dash:
                if self.action != 'death':
                    if self.now - self.hurt_frame >= self.invs:

                        # if random.randint(0, 100) <= 5:
                        #     self.game.Health.append(Health(self.game.assets, self.game.Player.rect().center, random.choice([100, 150, 50])))
                        BossDropHandler(self.game, list(self.rect().center))
                        self.game.target = self

                        self.set_action('hit')
                        self.DMG(100)
                        self.hurt_frame = pygame.time.get_ticks()
                        self.Recover_frame = pygame.time.get_ticks()
                        # for i in range(100):
                        #     angle = random.random() * math.pi * 2
                        #     Pvel = [ math.cos(angle) * 1, math.sin(angle) * 1]
                        #     self.game.Particles.append(Particles(self.game.assets, 'blood', self.rect().center, velocity= Pvel, frame= random.randint(0, 30)))

        self.pos[0] += self.Dir.x
        self.pos[1] += self.Dir.y

        if self.health <= 0:
            self.Dead_2 = True
            if self.Death_frame == 0:
                self.Death_frame = pygame.time.get_ticks()
            self.set_action('death')
            if self.now - self.Death_frame >= self.Death_delay:
                self.Dead = True

        if self.action == 'hit':
            if self.now - self.Recover_frame >= self.Recover_cooldown:
                self.set_action('idle')

        if abs(int(self.pos[0] - self.Dest[0])) <= 5:
            self.Dir.x = 0
        else:
            self.Dir.x = (self.Dest[0] - self.pos[0]) / 10

        if abs(int(self.pos[1] - self.Dest[1])) <= 5:
            self.Dir.y = 0
        else:
            self.Dir.y = (self.Dest[1] - self.pos[1]) / 10
        
        if self.Dir.x > 0:
            self.flip = False
        elif self.Dir.x < 0:
            self.flip = True
        
        if self.action != 'hit' and self.action != 'death':
            if "attack" not in self.action:
                if self.Dir.x == 0 and self.Dir.y == 0:
                    self.set_action('idle')

        # if self.Dir.x > 0:
        #     self.flip = False
        #     self.Dir.x = max(self.Dir.x - 1, 0)
        # if self.Dir.x < 0:
        #     self.flip = True
        #     self.Dir.x = min(self.Dir.x + 1, 0 )
        # if self.Dir.x == 0:
        #     self.set_action('idle')

        self.animation.update()
    
    def render(self, surf, offset = (0,0)):
        # rect = self.rect()
        # surf_rect = pygame.Surface((rect.width, rect.height))
        # surf.blit(surf_rect, (rect.x - offset[0], rect[1] - offset[1]) )

        img1 = self.animation.IMG()
        img2 = pygame.transform.scale(img1, (img1.get_width() * self.scale, img1.get_height() * self.scale))
        surf.blit(pygame.transform.flip(img2, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
    
    def rect(self):
        return pygame.Rect(self.pos, self.size)

class Evil_wizard(Boss):
    def __init__(self, game, pos, name, size, Health = 10000, scale = 3, anim_offset = (0, 0)):
        super().__init__(game, pos, 'Evil', name, size, Health, scale=scale, anim_offset=anim_offset)
        self.attack_delay = 2000
        self.attack_frame = 0

        self.Burn_delay = 100
        self.Burn_frame = 0

        self.size_bck = self.size[0]
    def rect(self):
        if self.action == 'attack1':
            if self.flip:
                return pygame.Rect(self.pos[0] - self.size[0] + 80, self.pos[1], self.size[0], self.size[1])
            else:
                return pygame.Rect(self.pos, self.size)
        else:
            return pygame.Rect(self.pos, self.size)
    
    def update(self):
        if self.action == 'attack1':
            self.size[0] = self.size_bck + 120
        else:
            self.size[0] = self.size_bck
        super().update()
        self.Move()
        if self.rect().colliderect(self.game.Player.rect()):
            if self.action == 'attack1':
                if self.now - self.Burn_frame >= self.Burn_delay:
                    # hit_sound.play()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(3)
                    self.Burn_frame = pygame.time.get_ticks()
            elif self.action == 'hit' or self.action == 'death':
                pass
            else:
                if self.now -self.attack_frame >= self.Player_invs:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
        
        if self.action != 'hit' and self.action != 'death':
            if self.action == 'attack1':
                if self.Dir.x == 0 and self.Dir.y == 0:
                    if self.now - self.attack_frame >= self.attack_delay:
                        self.set_action('idle')
        
    def Move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 50:
                    self.attack_frame = pygame.time.get_ticks()
                    self.set_action('attack1')
                    # Dash_sound.play()
                    # Fire_sound.play()
                    #X AXIS
                    self.Dest[0] = self.game.Player.pos[0]
                    #Y AXIS
                    self.Dest[1] = self.game.Player.pos[1] - 20
                elif chance <= 85:
                    self.set_action('move')
                    # Dash_sound.play()
                    #X AXIS
                    if self.pos[0] + 200 >= self.bound[0]:
                        self.Dest[0] = self.pos[0] + random.randrange(-200, -50, 10)
                    elif self.pos[0] - 200 <= self.bound[1]:
                        self.Dest[0] = self.pos[0] + random.randrange(50, 200, 10)
                    else:
                        step = random.randrange(-200, 200, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -50:
                            step = -50
                        self.Dest[0] = self.pos[0] + step

                    #Y AXIS
                    if self.pos[1] + 100 >= self.bound[2]:
                        self.Dest[1] = self.pos[1] + random.randrange(-100, -50, 10)
                    elif self.pos[1] - 100 <= self.bound[3]:
                        self.Dest[1] = self.pos[1] + random.randrange(50, 100, 10)
                    else:
                        step = random.randrange(-100, 100, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -70:
                            step = -70
                        self.Dest[1] = self.pos[1] + step

class Ghost(Boss):
    def __init__(self, game, pos, name, size, Health = 10000, scale = 3, anim_offset = (0, 0)):
        super().__init__(game, pos, 'Ghost', name, size, Health, scale=scale, anim_offset=anim_offset)
        self.attack_delay = 2000
        self.attack_frame = 0

        self.Soul_ball_delay = 1000
        self.Soul_ball_frame = 0
        self.bound[0] = self.pos[0] + 500
        self.bound[1] = self.pos[0] - 500
        self.bound[2] = self.pos[1] + 350
        self.bound[3] = self.pos[1] - 350

        self.charging = False
    
    def update(self):
        super().update()
        self.Move()
        if self.action == 'hit':
            if self.charging:
                self.charging = False
                self.game.Projectile.append(Soul_bullet(self.game, (self.rect().centerx, self.rect().centery -10 ), -1 if self.flip else 1, 8, (40, 30), 0, scale=2, offset= (-60, -80) if not self.flip else (-80, -80), showtime=100))
        
        if self.rect().colliderect(self.game.Player.rect()):
            if self.action == 'hit' or self.action == 'death':
                pass
            else:
                if self.now -self.attack_frame >= self.Player_invs:
                    # hit_sound.play()
                    self.attack_frame = pygame.time.get_ticks()
                    if not self.game.Player.is_dash:
                        self.game.Player.DMG(self.dmg)
        
        if self.action != 'hit' and self.action != 'death':
            if self.action == 'attack1':
                if self.charging:
                    if self.now - self.Soul_ball_frame >= self.Soul_ball_delay:
                        self.game.Projectile.append(Soul_bullet(self.game, (self.rect().centerx, self.rect().centery -30 ), -1 if self.flip else 1, 8, (70, 60), 0, scale=4, offset=(-140, -160) if not self.flip else (-160, -160), showtime=100))
                        self.Soul_ball_frame = pygame.time.get_ticks()
                        self.charging = False
                if self.Dir.x == 0 and self.Dir.y == 0:
                    if self.now - self.attack_frame >= self.attack_delay:
                        self.set_action('idle')
        
    def Move(self):
        now = pygame.time.get_ticks()
        if self.action == 'idle':
            if now - self.cool_frame >= self.cool_down:
                self.cool_frame = pygame.time.get_ticks()
                chance = random.randint(0, 100)
                if chance <= 50:
                    self.attack_frame = pygame.time.get_ticks()
                    self.set_action('attack1')
                    self.charging = True
                    # Dash_sound.play()
                    # Fire_sound.play()
                    self.Soul_ball_frame = pygame.time.get_ticks()
                    if self.rect().centery != self.game.Player.rect().centery:
                        self.Dest[1] = self.game.Player.rect().centery - 100
                    
                    flip = self.rect().centerx - self.game.Player.rect().centerx
                    if flip > 0:
                        self.flip = True
                    elif flip < 0:
                        self.flip = False

                elif chance <= 85:
                    self.set_action('move')
                    # Dash_sound.play()
                    #X AXIS
                    if self.pos[0] + 200 >= self.bound[0]:
                        self.Dest[0] = self.pos[0] + random.randrange(-400, -50, 10)
                    elif self.pos[0] - 200 <= self.bound[1]:
                        self.Dest[0] = self.pos[0] + random.randrange(50, 400, 10)
                    else:
                        step = random.randrange(-200, 200, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -50:
                            step = -50
                        self.Dest[0] = self.pos[0] + step

                    #Y AXIS
                    if self.pos[1] + 100 >= self.bound[2]:
                        self.Dest[1] = self.pos[1] + random.randrange(-200, -50, 10)
                    elif self.pos[1] - 100 <= self.bound[3]:
                        self.Dest[1] = self.pos[1] + random.randrange(50, 200, 10)
                    else:
                        step = random.randrange(-100, 100, 10)
                        if step >= 0 and step < 50:
                            step = 50
                        elif step < 0 and step > -70:
                            step = -70
                        self.Dest[1] = self.pos[1] + step