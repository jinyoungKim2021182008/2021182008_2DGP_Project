from pico2d import *
import math
import random
from game_constant import *


class Bullet:
    def __init__(self, damage):
        self.x, self.y = 0, 0
        self.rad = 0
        self.damage = damage
        self.bullet_image = load_image('image/character/bullet.png')
        self.bullet_image_width = self.bullet_image.w   # 50
        self.bullet_image_height = self.bullet_image.h  # 2

    def setBullet(self, x, y, rad):
        self.x, self.y = x + 50 * math.cos(rad), y + 50 * math.sin(rad)
        self.rad = rad

    def update(self):
        self.x += 10 * math.cos(self.rad)
        self.y += 10 * math.sin(self.rad)

    def render(self):
        self.bullet_image.clip_composite_draw(0, 0, self.bullet_image_width, self.bullet_image_height, self.rad, '0',
                                              self.x, self.y, self.bullet_image_width, self.bullet_image_height)


    def check_delete(self):
        if self.x < -100 or self.x > SCENE_WIDTH + 100:
            return True
        if self.y < -100 or self.y > SCENE_HEIGHT + 100:
            return True

        return False


class Rifle_1:  # like ak47
    def __init__(self, state):
        # 탄약
        self.magazine_capacity = 30
        self.ammo_max = 180

        # 반동
        self.recoil, self.max_recoil = 0, 0.5  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # 상태
        self.state = state  # false = dropped, true = on character

        # 총알
        self.damage = 45
        self.bullets = [Bullet(self.damage) for i in range(30)]
        self.check_bullets = [False for i in range(30)]
        self.next_bullet_index = 0

    def shoot(self, x, y, rad):
        if self.magazine_capacity <= 0: return
        # 탄약 감소
        self.magazine_capacity -= 1

        # 총알 나감
        self.check_bullets[self.next_bullet_index] = True
        rad_d = random.uniform(-self.recoil, self.recoil)
        self.bullets[self.next_bullet_index].setBullet(x + 10 * math.sin(rad), y - 10 * math.cos(rad), rad + rad_d)
        self.next_bullet_index = (self.next_bullet_index + 1) % 30

        # 반동 증가
        self.recoil = (self.recoil + self.add_recoil) * self.mul_recoil
        if self.recoil > self.max_recoil:
            self.recoil = self.max_recoil
        pass

    def update(self):
        self.recoil = (self.recoil - 0.02) * 0.95
        if self.recoil < 0:
            self.recoil = 0

        for i in range(0, 30):
            if self.check_bullets[i]:
                if self.bullets[i].check_delete():
                    print(1)
                    self.check_bullets[i] = False
                else:
                    self.bullets[i].update()

    def reload(self):
        if self.ammo_max <= 0: return

        self.ammo_max -= 30
        self.magazine_capacity = 30

    def render(self):
        for i in range(0, 30):
            if self.check_bullets[i]:
                self.bullets[i].render()


class Rifle_2:  # like m16
    pass


class Handgun:
    pass


class Grenade:
    pass


class Knife:
    pass
