from pico2d import *
import math
import random
import game_constant
import game_world
import game_framework
import stage
import effect


PIXEL_PER_METER = 20.0
BULLET_SPEED_KMPH = 250.0
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


class Bullet:
    image = None
    image_w, image_h = None, None
    fire_sound = None
    def __init__(self, x, y, rad, damage):
        self.x, self.y = x + 50 * math.cos(rad), y + 50 * math.sin(rad)
        self.x += (damage - 10) * math.cos(rad)
        self.y += (damage - 10) * math.sin(rad)
        self.dx, self.dy = self.x, self.y
        self.rad = rad
        self.damage = damage
        self.fir = True
        if Bullet.image is None:
            Bullet.image = load_image('image/weapon/bullet.png')
            Bullet.image_w, Bullet.image_h = Bullet.image.w, Bullet.image.h
        if Bullet.fire_sound is None:
            Bullet.fire_sound = load_wav('sound/gun_shot.wav')
            Bullet.fire_sound.set_volume(32)
        Bullet.fire_sound.play()

    def update(self):
        if self.fir:
            self.fir = False
        else:
            self.dx, self.dy = self.x, self.y
            self.x += BULLET_SPEED_PPS * game_framework.frame_time * math.cos(self.rad)
            self.y += BULLET_SPEED_PPS * game_framework.frame_time * math.sin(self.rad)
            if self.x < 0 - 25 or self.x > stage.STAGE_WIDTH + 25:
                game_world.remove_object(self)
            elif self.y < 0 - 25 or self.y > stage.STAGE_HEIGHT + 25:
                game_world.remove_object(self)

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image_w, self.image_h, self.rad, '0',
                                       self.x, self.y, self.damage * 2, self.image_h)

    def get_pos(self):
        ds, dc = self.damage * math.sin(self.rad), self.damage * math.cos(self.rad)
        return game_constant.Point(self.dx - dc, self.dy - ds)

    def get_line(self):
        ds, dc = self.damage * math.sin(self.rad), self.damage * math.cos(self.rad)
        return game_constant.Line(game_constant.Point(self.dx - dc, self.dy - ds), game_constant.Point(self.x + dc, self.y + ds))

    def handle_collide(self, point):
        game_world.remove_object(self)
        game_world.add_object(effect.BulletEffect(point.x, point.y), game_world.BULLET_EFFECT_LAYER)


class Grenade_1:
    sound = None
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y, rad, damage, speed):
        self.x, self.y = x + 50 * math.cos(rad), y + 50 * math.sin(rad)
        self.dx, self.dy = self.x, self.y
        self.speed = speed * 1000.0 / 360.0 * 20.0
        self.rad = rad
        self.timer = 6.0
        self.damage = damage
        self.fir = True
        if Grenade_1.image is None:
            Grenade_1.image = load_image('image/weapon/grenade_1.png')
            Grenade_1.image_w, Grenade_1.image_h = Grenade_1.image.w, Grenade_1.image.h
        if Grenade_1.sound is None:
            Grenade_1.sound = load_wav('sound/grenade.wav')
            Grenade_1.sound.set_volume(16)

    def update(self):
        if self.fir:
            self.fir = False
        else:
            self.dx, self.dy = self.x, self.y
            self.x += self.speed * game_framework.frame_time * math.cos(self.rad)
            self.y += self.speed * game_framework.frame_time * math.sin(self.rad)
            if self.x < 0 or self.x > stage.STAGE_WIDTH:
                self.x = clamp(0, self.x, stage.STAGE_WIDTH)
                self.rad += math.pi - self.rad * 2
            if self.y < 80 or self.y > stage.STAGE_HEIGHT:
                self.rad = -self.rad
                self.y = clamp(0, self.y, stage.STAGE_HEIGHT)

            self.timer -= game_framework.frame_time
            if self.timer < 0:
                self.explosion()

            self.speed -= 5
            if self.speed < 0:
                self.speed = 0

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image_w, self.image_h, self.rad, '0',
                                       self.x, self.y, 10, 10)

    def explosion(self):
        game_world.remove_object(self)
        d_rad = math.pi / 4
        bullets = [Bullet(self.x, self.y, self.rad + d_rad * i, self.damage) for i in range(8)]
        game_world.add_objects(bullets, game_world.BULLET_LAYER)
        Grenade_1.sound.play()

    def get_pos(self):
        dis = self.speed * game_framework.frame_time
        ds, dc = dis * math.sin(self.rad), dis * math.cos(self.rad)
        return game_constant.Point(self.dx - dc, self.dy - ds)

    def get_line(self):
        dis = self.speed * game_framework.frame_time
        ds, dc = dis * math.sin(self.rad), dis * math.cos(self.rad)
        return game_constant.Line(game_constant.Point(self.dx - dc, self.dy - ds),
                                  game_constant.Point(self.x + dc, self.y + ds))

    def handle_collide(self, p, rad):
        self.rad += 2 * (rad - self.rad)
        dis = self.speed * game_framework.frame_time
        ds, dc = dis * math.sin(self.rad), dis * math.cos(self.rad)
        self.x, self.y = p.x + dc, p.y + ds
        deg = math.degrees(rad)
        if deg < 0:
            deg += 180.0


class Grenade_2(Grenade_1):
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y, rad, damage, speed):
        self.x, self.y = x + 50 * math.cos(rad), y + 50 * math.sin(rad)
        self.dx, self.dy = self.x, self.y
        self.speed = speed * 1000.0 / 360.0 * 20.0
        self.rad = rad
        self.timer = 6.0
        self.damage = damage
        self.fir = True
        if Grenade_2.image is None:
            Grenade_2.image = load_image('image/weapon/grenade_2.png')
            Grenade_2.image_w, Grenade_2.image_h = Grenade_2.image.w, Grenade_2.image.h

    def explosion(self):
        game_world.remove_object(self)
        d_rad = math.pi / 8
        bullets = [Bullet(self.x, self.y, self.rad + d_rad * i, self.damage) for i in range(16)]
        game_world.add_objects(bullets, game_world.BULLET_LAYER)


class IDLE:
    @staticmethod
    def enter(self):
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        pass


class SHOOT:
    @staticmethod
    def enter(self):
        if self.magazine_capacity <= 0: return
        self.magazine_capacity -= 1

        self.timer = 0.1

        rad_d = random.uniform(-self.recoil, self.recoil)
        bullet = Bullet(self.x, self.y, self.rad + rad_d, self.damage)
        game_world.add_object(bullet, game_world.BULLET_LAYER)

        self.recoil = (self.recoil + self.add_recoil) * self.mul_recoil
        if self.recoil > self.max_recoil:
            self.recoil = self.max_recoil

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.timer -= game_framework.frame_time

class THROW:
    @staticmethod
    def enter(self):
        if self.magazine_capacity <= 0:
            self.cur_state = IDLE
            return
        self.magazine_capacity -= 1
        self.timer = 1.0

    @staticmethod
    def exit(self):
        grenade = None
        if type(self).__name__ == 'Grenades_1':
            grenade = Grenade_1(self.x, self.y, self.rad, self.damage, 10)
        if type(self).__name__ == 'Grenades_2':
            grenade = Grenade_2(self.x, self.y, self.rad, self.damage, 10)
        game_world.add_object(grenade, game_world.GRENADE_LAYER)
        if self.ammo_max >= self.magazine_max_capacity:
            self.magazine_capacity = self.magazine_max_capacity
            self.ammo_max -= self.magazine_max_capacity
        else:
            self.magazine_capacity = self.ammo_max
            self.ammo_max = 0

    @staticmethod
    def do(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.state_update(IDLE)


class RELOAD:
    @staticmethod
    def enter(self):
        self.timer = 2
        pass

    @staticmethod
    def exit(self):
        if self.ammo_max >= self.magazine_max_capacity:
            self.magazine_capacity = self.magazine_max_capacity
            self.ammo_max -= self.magazine_max_capacity
        else:
            self.magazine_capacity = self.ammo_max
            self.ammo_max = 0

    @staticmethod
    def do(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.state_update(IDLE)


class Gun:
    def __init__(self, activate):
        # ??????
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # ??????
        self.recoil, self.max_recoil = 0, 0.3  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # ??????
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 45
        self.shake = 0

        self.cur_state = IDLE
        self.cur_state.enter(self)

    def setPos(self, x, y, rad):
        self.x, self.y = x + 10 * math.sin(rad), y - 10 * math.cos(rad)
        self.rad = rad

    def update(self):
        self.recoil = (self.recoil - 0.7 * game_framework.frame_time)
        if self.shake == 2:
            if self.recoil < self.mul_recoil / 3:
                self.recoil = self.mul_recoil / 3
        if self.shake == 1:
            if self.recoil < self.mul_recoil / 6:
                self.recoil = self.mul_recoil / 6
        elif self.shake == 0:
            if self.recoil < 0:
                self.recoil = 0

        self.cur_state.do(self)

    def state_update(self, state):
        self.cur_state.exit(self)
        self.cur_state = state
        self.cur_state.enter(self)


class Rifle_1(Gun):  # like a
    def __init__(self, activate):
        # ??????
        # super().__init__(activate)
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # ??????
        self.recoil, self.max_recoil = 0, 0.3  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # ??????
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 45
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)


class Rifle_2(Gun):  # like m
    def __init__(self, activate):
        # ??????
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # ??????
        self.recoil, self.max_recoil = 0, 0.27  # rad
        self.add_recoil, self.mul_recoil = 0.09, 1.15

        # ??????
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 40
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)


class Rifle_3(Gun):  # like a
    def __init__(self, activate):
        # ??????
        # super().__init__(activate)
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 1800000

        # ??????
        self.recoil, self.max_recoil = 0, 0.3  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # ??????
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 45
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)


class Handgun(Gun):
    def __init__(self, activate):
        # ??????
        self.magazine_capacity = 8
        self.magazine_max_capacity = 8
        self.ammo_max = 40

        # ??????
        self.recoil, self.max_recoil = 0, 0.1  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.1

        # ??????
        self.activate = activate
        self.timer, self.rof = 0, 10
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 25
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)


class Grenades_1(Gun):
    def __init__(self):
        # ??????
        self.magazine_capacity = 1
        self.magazine_max_capacity = 1
        self.ammo_max = 6

        # ??????
        self.timer, self.rof = 0, 10
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 80
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)


class Grenades_2(Grenades_1):
    def __init__(self):
        # ??????
        self.magazine_capacity = 1
        self.magazine_max_capacity = 1
        self.ammo_max = 2

        # ??????
        self.timer, self.rof = 0, 10
        self.x, self.y = 0, 0
        self.rad = 0
        # ??????
        self.damage = 100
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self)


class Knife:
    pass
