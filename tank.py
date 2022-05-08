import math
import time

import pygame.sprite

from config import CONFIG


class Tank(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.images = pygame.image.load('assets/img/tanks.png').convert_alpha()
        self.image = self.images.subsurface(pygame.Rect(0, 0, 32, 32))
        self.image = pygame.transform.scale(self.image, CONFIG.TANK_SIZE)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = CONFIG.TANK_POSITION

        self.x, self.y = float(self.rect.x), float(self.rect.y)

        self.max_speed = CONFIG.MAX_SPEED
        self.speed = 0
        self.accelerate = CONFIG.ACCELERATE
        self.friction = self.accelerate / 100 * 80
        self.angle = 0
        self.max_gun_angle = 60
        self.gun_angle = 0
        self.max_shot_power = CONFIG.MAX_SHOT_POWER
        self.shot_power = self.max_speed

    def update(self):
        keys = pygame.key.get_pressed()

        # speed accelerate
        if (self.speed ** 2) ** 0.5 < self.max_speed:
            if keys[pygame.K_d]:
                self.speed += self.accelerate
            if keys[pygame.K_a]:
                self.speed -= self.accelerate

        # increase shot power
        if keys[pygame.K_SPACE]:
            self.shot_power += 0.1 if self.shot_power < self.max_shot_power else 0

        # exit from border
        if self.rect.right > self.screen_rect.right:
            self.speed = -self.accelerate * 5
        elif self.rect.left < 0:
            self.speed = self.accelerate * 5

        # friction
        if (self.speed ** 2) ** 0.5 < self.friction:
            self.speed = 0
        elif self.speed < 0:
            self.speed += self.friction
        elif self.speed > 0:
            self.speed -= self.friction

        # change gun angle
        if keys[pygame.K_w]:
            if self.gun_angle < self.max_gun_angle:
                self.gun_angle += 1
        elif keys[pygame.K_s]:
            if self.gun_angle > -self.max_gun_angle:
                self.gun_angle -= 1

        if self.gun_angle < -45:
            self.image = self.images.subsurface(pygame.Rect(0,0,32,32))
        elif self.gun_angle > -15 and self.gun_angle <15:
            self.image = self.images.subsurface(pygame.Rect(32,0,32,32))
        elif self.gun_angle > 15 and self.gun_angle <45:
            self.image = self.images.subsurface(pygame.Rect(64,0,32,32))
        elif self.gun_angle > 45:
            self.image = self.images.subsurface(pygame.Rect(96,0,32,32))

        self.image = pygame.transform.scale(self.image, CONFIG.TANK_SIZE)

        # moving
        self.x += self.speed
        self.rect.x = int(self.x)

    def shot_direction(self):
        pass

    def shot(self):
        bullet = Bullet(self)
        self.speed -= self.shot_power / 10
        self.shot_power = self.max_speed
        return bullet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('assets/img/bullet.png')
        self.image = pygame.transform.scale(self.image, CONFIG.BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.speed = tank.shot_power
        self.rect.centerx = tank.rect.right
        self.rect.centery = tank.rect.centery - tank.gun_angle/3 + 10
        self.time_to_live = CONFIG.BULLET_TTL
        self.start_time = time.time()
        self.bullet_live = True

        self.angle = tank.angle + tank.gun_angle
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_x = self.speed*math.cos(math.radians(self.angle))
        self.speed_y = self.speed*math.sin(math.radians(self.angle))

    def update(self):
        if time.time() - self.start_time > self.time_to_live or self.y > CONFIG.TANK_POSITION[1]:
            self.kill()
        self.x += self.speed_x
        self.y -= self.speed_y
        self.speed_y -= CONFIG.GRAVITATION
        # self.angle = math.asin(self.speed_x/self.speed_y)
            # self.rect.x -= 1
            # self.rect.y = self.rect.y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class Map(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/img/map.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, CONFIG.WINDOW_SIZE)
        self.rect = self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.rect.x -= self.speed