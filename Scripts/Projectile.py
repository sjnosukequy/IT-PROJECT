import pygame, math
from Scripts.Assets import Assets

class Projectile:
    def __init__(self, game, type, pos, vel, speed, size, angle, owner = 'player', dame = 10, showtime = 250, scale = 1):
        self.type = type
        self.game = game
        self.pos = list(pos)
        self.vel = vel
        self.speed = speed
        self.angle = angle
        self.dame = dame
        self.img = Assets['bullet' + '/' + self.type]
        self.owner = owner
        self.size = size
        self.alive_time = 2000
        self.timer = pygame.time.get_ticks()
        self.kill = False
        self.showtime = showtime
        self.flip = False
        self.scale = scale
    
    def update(self):
        self.current_time = pygame.time.get_ticks()
        rad = math.radians(self.angle)
        dy = - math.tan(rad) * self.vel
        dir = pygame.Vector2(self.vel, dy)
        if dir.magnitude():
            dir = pygame.Vector2.normalize(dir)
        dir *= self.speed
        self.pos[0] += dir[0]
        self.pos[1] += dir[1]
        self.flip = False
        if self.vel < 0:
            self.flip = True
        self.destroy()
    
    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def destroy(self):
        if self.current_time - self.timer >= self.alive_time:
            self.kill = True

    def render(self, surf, offset = (0,0)):
        if self.current_time - self.timer >= self.showtime:
            # black = pygame.Surface(self.size)
            # rect = pygame.Rect((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size)
            # surf.blit(black, rect)
            img_1 = pygame.transform.scale(self.img, (self.img.get_width() * self.scale,self.img.get_height() * self.scale))
            img = pygame.transform.rotate(img_1, self.angle)
            img.set_colorkey('black')
            surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Rocket_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='player', dame=10, showtime=250, scale=1):
        super().__init__(game, 'rocket' , pos, vel, speed, size, angle, owner, dame, showtime, scale)

class Small_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='player', dame=10, showtime=250, scale=1):
        super().__init__(game, 'small', pos, vel, speed, size, angle, owner, dame, showtime, scale)

class Small_Ene_ammo(Projectile):
    def __init__(self, game, pos, vel, speed, size, angle, owner='Ene', dame=10, showtime=250, scale=1):
        super().__init__(game, 'small', pos, vel, speed, size, angle, owner, dame, showtime, scale)