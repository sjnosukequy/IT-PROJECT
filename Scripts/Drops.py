import pygame, random, copy
from Scripts.Weapons import *

pygame.mixer.init()
class Drop:
    def __init__(self, game, pos, type, size, scale = 1):
        self.game = game
        self.pos = copy.deepcopy(pos)
        self.type = type
        self.action = ''
        self.size = size
        self.scale = scale
        self.speed = -5
        self.set_action(self.type)
    
    def update(self):
        self.animation.update()
        self.pos[1] += self.speed
        self.speed = min(self.speed + 1, 3)
        entity_rect = self.rect()
        for rect in self.game.tilemap.physic_rects_around(self.pos, self.size):
            if entity_rect.colliderect(rect):
                entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y

    def function(self):
        pass

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets['Drops' + '/' + self.action].copy()

    def render(self, surf, offset):
        img = self.animation.IMG()
        img2 = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        surf.blit(img2, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
def DropHandler(game, pos):
        chance = random.randint(0, 100)
        if chance < 5:
            game.Drops.append(Rocket(game, pos, (30, 20)))
        elif chance < 10:
            game.Drops.append(Drop_Health(game, pos, (30, 30)))
        elif chance < 20:
            game.Drops.append(Ammo_Pistol(game, pos, (30, 23)))
        elif chance < 40:
            game.Drops.append(Ammo_Rifle(game, pos, (30, 26)))
        
        

def BossDropHandler(game, pos):
    chance = random.randint(0, 100)
    if chance < 5:
        choice2 = random.choice(['health', 'ammo_pistol', 'rocket'])
        if choice2 == 'rocket':
            game.Drops.append(Rocket(game, pos, (30, 20)))
        if choice2 == 'health':
            game.Drops.append(Drop_Health(game, pos, (30, 30)))

    elif chance < 10:
        game.Drops.append(Ammo_Pistol(game, pos, (30, 23)))
class Drop_Health(Drop):
    def __init__(self, game, pos, size, scale=1):
        super().__init__(game, pos, 'health', size, scale)
        self.amount = random.choice([100, 200, 400])
        self.healsfx = pygame.mixer.Sound('Data/sfx/heal.wav')
        self.healsfx.set_volume(0.1)
    
    def function(self):
        self.healsfx.play()
        self.game.Player.Heal(self.amount)

class Ammo_Pistol(Drop):
    def __init__(self, game, pos,  size, scale=1, amount = 25):
        super().__init__(game, pos, 'ammo_pistol', size, scale)
        self.amount = amount
        self.pickupsfx = pygame.mixer.Sound('Data/sfx/pickup.wav')
        self.pickupsfx.set_volume(0.1)

    def function(self):
        self.pickupsfx.play()
        len1 = len(self.game.hands)
        for i in range (len1): 
            if self.game.hands[i].type == "pistol":
                self.game.hands[i].addBullets(self.amount)

class Rocket(Drop):
    def __init__(self, game, pos,  size, scale=1):
        super().__init__(game, pos, 'rocket', size, scale)
        self.amount = random.randint(1, 10)
        self.pickupsfx = pygame.mixer.Sound('Data/sfx/pickup.wav')
        self.pickupsfx.set_volume(0.1)

    def function(self):
        self.pickupsfx.play()
        len1 = len(self.game.hands)
        for i in range (len1): 
            if self.game.hands[i].type == "launcher":
                self.game.hands[i].addBullets(self.amount)

class Ammo_Rifle(Drop):
    def __init__(self, game, pos,  size, scale=1, amount = 25):
        super().__init__(game, pos, 'ammo_rifle', size, scale)
        self.amount = amount
        self.pickupsfx = pygame.mixer.Sound('Data/sfx/pickup.wav')
        self.pickupsfx.set_volume(0.1)

    def function(self):
        self.pickupsfx.play()
        len1 = len(self.game.hands)
        for i in range (len1): 
            if self.game.hands[i].type == "rifle":
                self.game.hands[i].addBullets(self.amount)