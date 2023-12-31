from Scripts.Entities import *
from Scripts.Weapons import Wep_Ene
from Scripts.Particles import Earth_Cols, Laser_line
from Scripts.Projectile import FireBall
import pygame, random

pygame.mixer.init()
pygame.mixer.set_num_channels(8)

class Skeleton(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 250, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.game = game
        self.attacking = False
        self.delay = 900
        self.timer = pygame.time.get_ticks()

        self.sound_att = pygame.mixer.Sound('Data/sfx/skeleton.mp3')
        self.sound_timer = pygame.time.get_ticks()
        self.sound_delay = 1000
        self.sound_att.set_volume(0.3)

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = ( -1 if self.flip else 1)
    
    def attack(self):
        self.walking = 0
        self.attacking = True
        self.Earth()
        self.set_action('attack')
    
    def Earth(self):
        if self.attacking:
            current = pygame.time.get_ticks()
            if self.action != 'attack':
                self.timer = pygame.time.get_ticks()
            if current - self.timer >= self.delay:
                self.game.Particles.append(Earth_Cols(self.game, (30, 75), self.rect(), -1 if self.flip else 1, 5))
                self.timer = pygame.time.get_ticks()

    def update(self, tilemap, player):
        super().update(tilemap)
        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        # self.dbg = tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            if self.Air_time < 1:
                self.walk(tilemap)

        if abs(player.rect().x - self.rect().x) < 150:
            if random.randint(0, 100) < 20:
                if pygame.time.get_ticks() - self.sound_timer >= self.sound_delay:
                    self.sound_att.play()
                    self.sound_timer = pygame.time.get_ticks()

            if self.rect().bottom - player.rect().bottom  < 64 and self.rect().bottom - player.rect().bottom >= 0:
                if self.rect().x - player.rect().x > 0:
                    self.flip = True
                if self.rect().x - player.rect().x < 0:
                    self.flip = False
                self.attack()

        self.Earth()
        if self.action == 'idle' and self.Air_time < 1:
                chance = random.randint(0, 100)
                if chance < 10:
                    self.walk(tilemap)      

        if self.action == 'attack':
            if self.animation.done:
                self.attacking = False

        if self.attacking:
            pass
        elif self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset = (0,0)):
        #HITBOX DEBUG
        # ac = pygame.Surface(self.size)
        # pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        # surf.blit(ac, pos)
        # if self.dbg:
        #     rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
        #     ac2 = pygame.Surface((32, 32))
        #     surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale , self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False), (self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Thug(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.game = game
        self.Air_time = 0
        self.attacking = False

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)

    def attack(self):
        self.walking = 0
        self.set_action('attack')
        self.game.Particles.append(Laser_line(self.game, 10, self.rect(), -1 if self.flip else 1, 10, offset=(0, -11)))
        self.attacking = True

    def update(self, tilemap, player):

        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        # self.dbg = tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            if self.Air_time < 1:
                self.walk(tilemap)

        if self.action != 'attack':
            if abs(player.rect().x - self.rect().x) < 324:
                if self.rect().bottom - player.rect().bottom  < 64 and self.rect().bottom - player.rect().bottom >= 0:
                    if self.rect().x - player.rect().x > 0:
                        self.flip = True
                    if self.rect().x - player.rect().x < 0:
                        self.flip = False
                    self.attack()

        if self.action == 'idle' and self.Air_time < 1:
            chance = random.randint(0, 100)
            if chance < 10:
                self.walk(tilemap)

        super().update(tilemap)

        if self.action == 'attack':
            if self.animation.done:
                self.attacking = False

        if self.attacking:
            pass
        elif self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        #HITBOX DEBUG
        # ac = pygame.Surface(self.size)
        # pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        # surf.blit(ac, pos)
        # if self.dbg:
        #     rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
        #     ac2 = pygame.Surface((32, 32))
        #     surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Wizard(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 100, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.game = game
        self.delay = 1000
        self.timer = pygame.time.get_ticks()
        self.attacking = False
        self.att_sound = pygame.mixer.Sound('Data/sfx/magic_spell.mp3')
        self.att_sound.set_volume(0.25)

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)

    def attack(self):
        self.walking = 0
        self.attacking = True
        self.fireball()
        self.att_sound.play(maxtime=800)
        self.set_action('attack')
    
    def fireball(self):
        if self.attacking:
            current = pygame.time.get_ticks()
            if self.action != 'attack':
                self.timer = pygame.time.get_ticks()
            if current - self.timer >= self.delay:
                self.game.Projectile.append(FireBall(self.game, self.rect().center, -1 if self.flip else 1, 8, (20,15), 0, scale= 1.5, showtime=80, offset=(-75, -75), dame=25))
                self.timer = pygame.time.get_ticks()

    def update(self, tilemap, player):
        super().update(tilemap)
        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        # self.dbg = tilemap.solid_check(
        #     (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            if self.Air_time < 1:
                self.walk(tilemap)

        if self.action != 'attack':
            if abs(player.rect().x - self.rect().x) < 200:
                if self.rect().bottom - player.rect().bottom  < 64 and self.rect().bottom - player.rect().bottom >= 0:
                    if self.rect().x - player.rect().x > 0:
                        self.flip = True
                    if self.rect().x - player.rect().x < 0:
                        self.flip = False
                    self.attack()
        self.fireball()

        if  self.action == 'idle' and self.Air_time < 1:
            chance = random.randint(0, 100)
            if chance < 10:
                self.walk(tilemap)

        if self.action == 'attack':
            if self.animation.done:
                self.attacking = False

        if self.attacking:
            pass
        elif self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        #HITBOX DEBUG
        # ac = pygame.Surface(self.size)
        # pos = (self.rect().x - offset[0] , self.rect().y - offset[1])
        # surf.blit(ac, pos)
        # if self.dbg:
        #     rect = pygame.Rect(self.dbg['pos'][0] * 32 -offset[0], self.dbg['pos'][1] *32 - offset[1], 32, 32)
        #     ac2 = pygame.Surface((32, 32))
        #     surf.blit(ac2, rect)

        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))

class Zombie(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, assets, Health = 200, speed=1.5, scale = 1, animations_offset=(0, 0)):
        super().__init__(e_type, pos, size, assets, Health, speed)
        self.scale = scale
        self.animations_offset = animations_offset
        self.walking = 0
        self.Air_time = 0
        self.game = game
        self.weapon = Wep_Ene('rifle', Loffset=(100, 10), Roffset=(15, 10), scale=1, dame=20)
        self.sound_att = pygame.mixer.Sound('Data/sfx/zombie_growl.mp3')
        self.sound_timer = pygame.time.get_ticks()
        self.sound_delay = 3000
        self.sound_att.set_volume(0.1)

    def walk(self, tilemap):
        if not self.walking:
            self.walking = random.randint(30, 120)
        if tilemap.solid_check((self.pos[0], self.pos[1]), self.size, self.flip):
            if self.Coll['left'] or self.Coll['right']:
                self.flip = not self.flip
        else:
            self.flip = not self.flip
        self.Dir.x = (-1 if self.flip else 1)
    
    def attack(self):
        self.weapon.attack(self.game, self)
        self.walking = 0

    def update(self, tilemap, player):
        super().update(tilemap)
        self.Air_time += 1
        if self.Coll['bottom']:
            self.Air_time = 0

        # self.dbg = tilemap.solid_check(
        #     (self.pos[0], self.pos[1]), self.size, self.flip)

        self.walking = max(0, self.walking - 1)
        if self.walking == 0:
            self.Dir.x = 0
        else:
            if self.Air_time < 1:
                self.walk(tilemap)

        if abs(player.rect().x - self.rect().x) <= 224:
            if random.randint(0, 100) < 20:
                if pygame.time.get_ticks() - self.sound_timer >= self.sound_delay:
                    self.sound_timer = pygame.time.get_ticks()
                    self.sound_att.play()
            if self.rect().bottom - player.rect().bottom  < 64 and self.rect().bottom - player.rect().bottom >= 0:
                if self.rect().x - player.rect().x > 0:
                    self.flip = True
                if self.rect().x - player.rect().x < 0:
                    self.flip = False
                self.attack()
        self.weapon.update(self.rect(), self.flip)

        if self.action == 'idle' and self.Air_time < 1 and self.weapon.action == 'idle':
            chance = random.randint(0, 100)
            if chance < 10:
                self.walk(tilemap)

        if self.Dir.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.scale(self.animation.IMG(), (self.animation.IMG().get_width() * self.scale, self.animation.IMG().get_height() * self.scale))
        surf.blit(pygame.transform.flip(img, self.flip, False),(self.pos[0] - offset[0] + self.animations_offset[0], self.pos[1] - offset[1] + self.animations_offset[1]))
        self.weapon.render(surf, self.flip, offset)


