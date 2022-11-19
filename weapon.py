from pico2d import *
import math
import random
import game_constant
import game_world
import game_framework
import stage
import efecte


PIXEL_PER_METER = 20.0
BULLET_SPEED_KMPH = 250.0
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


class Bullet:
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y, rad, damage):
        self.x, self.y = x + 50 * math.cos(rad), y + 50 * math.sin(rad)
        self.x += (damage - 10) * math.cos(rad)
        self.y += (damage - 10) * math.sin(rad)
        self.dx, self.dy = self.x, self.y
        self.rad = rad
        self.damage = damage
        self.fir = True
        if Bullet.image is None:
            Bullet.image = load_image('image/bullet.png')
            Bullet.image_w, Bullet.image_h = Bullet.image.w, Bullet.image.h

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

    def getPos(self):
        ds, dc = self.damage * math.sin(self.rad), self.damage * math.cos(self.rad)
        return game_constant.Point(self.dx - dc, self.dy - ds)

    def getLine(self):
        ds, dc = self.damage * math.sin(self.rad), self.damage * math.cos(self.rad)
        return game_constant.Line(game_constant.Point(self.dx - dc, self.dy - ds), game_constant.Point(self.x + dc, self.y + ds))

    def collide_handle(self, other, point):
        game_world.remove_object(self)
        game_world.add_object(efecte.BulletEffect(point.x, point.y), game_world.BULLET_EFFECT_LAYER)


LMD, LMU, RD, TIMER, IGNORE = range(5)
event_name = ['MOUSE_DOWN', 'MOUSE_UP', 'RD', 'TIMER', 'IGNORE']
key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None): LMD,
    (SDL_MOUSEBUTTONUP, None): LMU,
    (SDL_KEYDOWN, SDLK_r): RD
}


class IDLE:
    @staticmethod
    def enter(self, event):
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        pass


class SHOOT:
    @staticmethod
    def enter(self, event):
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
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.add_event(TIMER)


class RELOAD:
    @staticmethod
    def enter(self, event):
        self.timer = 2
        pass

    @staticmethod
    def exit(self, event):
        if self.ammo_max >= self.magazine_max_capacity:
            self.magazine_capacity = self.magazine_max_capacity
            self.ammo_max -= self.magazine_max_capacity
        else:
            self.magazine_capacity = self.ammo_max
            self.ammo_max = 0
        pass

    @staticmethod
    def do(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.add_event(TIMER)


next_state = {
    IDLE: {LMD: SHOOT, LMU: IDLE, RD: RELOAD, TIMER: IGNORE},
    SHOOT: {LMD: IGNORE, LMU: IDLE, RD: RELOAD, TIMER: SHOOT},
    RELOAD: {LMD: IGNORE, LMU: IGNORE, RD: IGNORE, TIMER: IDLE}
}

next_state_handgun = {
    IDLE: {LMD: SHOOT, LMU: IDLE, RD: RELOAD, TIMER: IGNORE},
    SHOOT: {LMD: IGNORE, LMU: IDLE, RD: RELOAD, TIMER: IDLE},
    RELOAD: {LMD: IGNORE, LMU: IGNORE, RD: IGNORE, TIMER: IDLE}
}

class Gun:
    def __init__(self, activate):
        # 탄약
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # 반동
        self.recoil, self.max_recoil = 0, 0.3  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # 상태
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # 총알
        self.damage = 45
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

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

        if self.event_que:
            event = self.event_que.pop()
            if next_state[self.cur_state][event] != IGNORE:
                self.cur_state.exit(self, event)
                try:
                    self.cur_state = next_state[self.cur_state][event]
                except KeyError:
                    print(f'ERROR: State {self.cur_state.__name__} Event {event_name[event]}')
                # self.cur_state = next_state[self.cur_state][event]
                self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


class Rifle_1(Gun):  # like a
    def __init__(self, activate):
        # 탄약
        # super().__init__(activate)
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # 반동
        self.recoil, self.max_recoil = 0, 0.3  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.2

        # 상태
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # 총알
        self.damage = 45
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)


class Rifle_2(Gun):  # like m
    def __init__(self, activate):
        # 탄약
        self.magazine_capacity = 30
        self.magazine_max_capacity = 30
        self.ammo_max = 180

        # 반동
        self.recoil, self.max_recoil = 0, 0.27  # rad
        self.add_recoil, self.mul_recoil = 0.09, 1.15

        # 상태
        self.activate = activate
        self.timer = 0
        self.x, self.y = 0, 0
        self.rad = 0
        # 총알
        self.damage = 40
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)


class Handgun(Gun):
    def __init__(self, activate):
        # 탄약
        self.magazine_capacity = 8
        self.magazine_max_capacity = 8
        self.ammo_max = 40

        # 반동
        self.recoil, self.max_recoil = 0, 0.1  # rad
        self.add_recoil, self.mul_recoil = 0.1, 1.1

        # 상태
        self.activate = activate
        self.timer, self.rof = 0, 10
        self.x, self.y = 0, 0
        self.rad = 0
        # 총알
        self.damage = 25
        self.shake = 0

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

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

        if self.event_que:
            event = self.event_que.pop()
            if next_state_handgun[self.cur_state][event] != IGNORE:
                self.cur_state.exit(self, event)
                try:
                    self.cur_state = next_state_handgun[self.cur_state][event]
                except KeyError:
                    print(f'ERROR: State {self.cur_state.__name__} Event {event_name[event]}')
                # self.cur_state = next_state[self.cur_state][event]
                self.cur_state.enter(self, event)


class Grenade:
    
    pass


class Knife:
    pass
