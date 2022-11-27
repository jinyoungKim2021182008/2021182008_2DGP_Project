from pico2d import *
import math

import random

import game_constant
import game_world
import play_state
from game_constant import Point, Circle, Rect
from effect import BloodEffect, DeadEffect
import game_framework
import weapon
from ui import Cursor

WD, SD, AD, DD, WU, SU, AU, DU, LSHD, LSHU, LMD, LMU, RD, D1, D2, D3, TIMER, IGNORE = range(18)
event_name = ['WD', 'SD', 'AD', 'DD', 'WU', 'SU', 'AU', 'DU', 'LSHD', 'LSHU',
              'LEFT_MOUSE_DOWN', 'LEFT_MOUSE_UP', 'RD', 'D1', 'D2', 'D3', 'TIMER', 'IGNORE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_w): WD,
    (SDL_KEYDOWN, SDLK_s): SD,
    (SDL_KEYDOWN, SDLK_a): AD,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_w): WU,
    (SDL_KEYUP, SDLK_s): SU,
    (SDL_KEYUP, SDLK_a): AU,
    (SDL_KEYUP, SDLK_d): DU,
    (SDL_KEYDOWN, SDLK_LSHIFT): LSHD,
    (SDL_KEYUP, SDLK_LSHIFT): LSHU,
    (SDL_MOUSEBUTTONDOWN, None): LMD,
    (SDL_MOUSEBUTTONUP, None): LMU,
    (SDL_KEYDOWN, SDLK_r): RD,
    (SDL_KEYDOWN, SDLK_1): D1,
    (SDL_KEYDOWN, SDLK_2): D2,
    (SDL_KEYDOWN, SDLK_3): D3
}


class IDLE:
    ACTION_PER_TIME = 20
    FRAMES_PER_ACTION = 20

    @staticmethod
    def enter(self, event):
        self.feet_frame = 0
        self.fs = 0

        self.weapons[self.select_weapon].shake = 0

        if self.action_state == IDLE:
            self.bs = 0
            self.body_frame = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        if self.action_state == IDLE:
            self.body_frame = (self.body_frame + IDLE.ACTION_PER_TIME * game_framework.frame_time) % IDLE.FRAMES_PER_ACTION


PIXEL_PER_METER = 15.0
WALK_SPEED_KMPH = 15.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)


class WALK:
    ACTION_PER_TIME = 20
    FRAMES_PER_ACTION = 20

    @staticmethod
    def enter(self, event):
        self.feet_frame = 0
        self.fs = 1
        if event == WD or event == SU:
            self.feet_dir_y += 1
        if event == SD or event == WU:
            self.feet_dir_y -= 1
        if event == AD or event == DU:
            self.feet_dir_x -= 1
        if event == DD or event == AU:
            self.feet_dir_x += 1

        self.weapons[self.select_weapon].shake = 1

        if self.action_state == IDLE:
            self.bs = 1
            self.body_frame = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        if self.feet_dir_x == 0 and self.feet_dir_y == 0:
            self.change_state(self.move_state, IDLE)
        elif self.feet_dir_x != 0 and self.feet_dir_y != 0:
            self.x += self.feet_dir_x * WALK_SPEED_PPS * game_framework.frame_time / 1.4
            self.y += self.feet_dir_y * WALK_SPEED_PPS * game_framework.frame_time / 1.4
        else:
            self.x += self.feet_dir_x * WALK_SPEED_PPS * game_framework.frame_time
            self.y += self.feet_dir_y * WALK_SPEED_PPS * game_framework.frame_time
        self.feet_frame = (self.feet_frame + 1) % 20
        self.set_feet_dir()

        if self.action_state == IDLE:
            self.body_frame = (self.body_frame + IDLE.ACTION_PER_TIME * game_framework.frame_time) % IDLE.FRAMES_PER_ACTION


RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class RUN:
    ACTION_PER_TIME = 30
    FRAMES_PER_ACTION = 20

    @staticmethod
    def enter(self, event):
        self.feet_frame = 0
        self.fs = 2
        if event == WD or event == SU:
            self.feet_dir_y += 1
        if event == SD or event == WU:
            self.feet_dir_y -= 1
        if event == AD or event == DU:
            self.feet_dir_x -= 1
        if event == DD or event == AU:
            self.feet_dir_x += 1

        self.weapons[self.select_weapon].shake = 2

        if self.action_state == IDLE:
            self.bs = 1
            self.body_frame = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        if self.feet_dir_x == 0 and self.feet_dir_y == 0:
            self.change_state(self.move_state, IDLE)
        elif self.feet_dir_x != 0 and self.feet_dir_y != 0:
            self.x += self.feet_dir_x * RUN_SPEED_PPS * game_framework.frame_time / 1.4
            self.y += self.feet_dir_y * RUN_SPEED_PPS * game_framework.frame_time / 1.4
        else:
            self.x += self.feet_dir_x * RUN_SPEED_PPS * game_framework.frame_time
            self.y += self.feet_dir_y * RUN_SPEED_PPS * game_framework.frame_time
        self.feet_frame = (self.feet_frame + RUN.ACTION_PER_TIME * game_framework.frame_time) % RUN.FRAMES_PER_ACTION
        self.set_feet_dir()

        if self.action_state == IDLE:
            self.body_frame = (self.body_frame + RUN.ACTION_PER_TIME * game_framework.frame_time) % RUN.FRAMES_PER_ACTION


class SHOOT:
    ACTION_PER_TIME = 30
    FRAMES_PER_ACTION = 3

    @staticmethod
    def enter(self, event):
        self.bs = 3
        self.body_frame = 0

        self.timer = 0.1
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.body_frame = (self.body_frame + SHOOT.ACTION_PER_TIME * game_framework.frame_time) % SHOOT.FRAMES_PER_ACTION
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            if self.weapons[self.select_weapon].magazine_capacity == 0 or type(self.weapons[self.select_weapon]).__name__ == 'Handgun':
                self.add_event(LMU)
            else:
                self.add_event(TIMER)


class THROW:
    ACTION_PER_TIME = 10
    FRAMES_PER_ACTION = 15

    @staticmethod
    def enter(self, event):
        self.bs = 3
        self.body_frame = 0

        self.timer = 2.0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.body_frame = (self.body_frame + THROW.ACTION_PER_TIME * game_framework.frame_time) % THROW.FRAMES_PER_ACTION
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.add_event(TIMER)


class RELOAD:
    ACTION_PER_TIME = 10
    FRAMES_PER_ACTION = 20

    @staticmethod
    def enter(self, event):
        if self.returnNowWeapon() == 2:
            self.timer = 1.5
        else:
            self.timer = 2.0
        self.bs = 2
        self.body_frame = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.body_frame = (self.body_frame + RELOAD.ACTION_PER_TIME * game_framework.frame_time) % RELOAD.FRAMES_PER_ACTION
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.add_event(TIMER)


class CHANGE_WEAPON:
    ACTION_PER_TIME = 20
    FRAMES_PER_ACTION = 15
    next_weapon = 0
    @staticmethod
    def enter(self, event):
        if event == D1:
            if self.select_weapon == 0:
                self.add_event(TIMER)
            CHANGE_WEAPON.next_weapon = 0
        if event == D2:
            if self.select_weapon == 1:
                self.add_event(TIMER)
            CHANGE_WEAPON.next_weapon = 1
        if event == D3:
            if self.select_weapon == 2:
                self.add_event(TIMER)
            CHANGE_WEAPON.next_weapon = 2
        self.bs = 2
        self.body_frame = 0
        self.timer = 1.5

    @staticmethod
    def exit(self, event):
        self.select_weapon = CHANGE_WEAPON.next_weapon
        pass

    @staticmethod
    def do(self):
        self.body_frame = (self.body_frame + RELOAD.ACTION_PER_TIME * game_framework.frame_time) % RELOAD.FRAMES_PER_ACTION
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.add_event(TIMER)

next_move_state = {
    IDLE: {WD: WALK, SD: WALK, AD: WALK, DD: WALK, WU: WALK, SU: WALK, AU: WALK, DU: WALK, LSHD: RUN, LSHU: IGNORE},
    WALK: {WD: WALK, SD: WALK, AD: WALK, DD: WALK, WU: WALK, SU: WALK, AU: WALK, DU: WALK, LSHD: RUN, LSHU: IGNORE},
    RUN: {WD: RUN, SD: RUN, AD: RUN, DD: RUN, WU: RUN, SU: RUN, AU: RUN, DU: RUN, LSHD: RUN, LSHU: WALK}
}

next_action_state = {
    IDLE: {LMD: SHOOT, LMU: IGNORE, RD: RELOAD, TIMER: IGNORE, D1: CHANGE_WEAPON, D2: CHANGE_WEAPON, D3: CHANGE_WEAPON},
    SHOOT: {LMD: IGNORE, LMU: IDLE, RD: RELOAD, TIMER: SHOOT, D1: IGNORE, D2: IGNORE, D3: IGNORE},
    THROW: {LMD: IGNORE, LMU: IGNORE, RD: IGNORE, TIMER: IDLE, D1: IGNORE, D2: IGNORE, D3: IGNORE},
    RELOAD: {LMD: IGNORE, LMU: IGNORE, RD: IGNORE, TIMER: IDLE, D1: IGNORE, D2: IGNORE, D3: IGNORE},
    CHANGE_WEAPON: {LMD: IGNORE, LMU: IGNORE, RD: IGNORE, TIMER: IDLE, D1: IGNORE, D2: IGNORE, D3: IGNORE}
}


class Character:
    feet_image = None
    feet_image_w = []
    feet_image_h = []
    body_image = None
    body_image_w = []
    body_image_h = []

    def __init__(self, x, y, hp, armor):
        """
        캐릭터 위치 및 정보
        """
        self.x, self.y = x, y
        self.speed = 0
        self.hp = hp
        self.armor = armor
        """
        캐릭터 발  
        """
        # 0 = idle, 1 = walk, 2 = run
        if Character.feet_image is None:
            pass

        self.feet_direction = 0
        self.feet_dir_x, self.feet_dir_y = 0, 0
        self.feet_frame = 0
        self.fs = 0
        """
        캐릭터 몸  
        """
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        if Character.body_image is None:
            pass

        self.body_frame = 0
        self.body_reload_frame = 0
        self.body_rad = 0
        self.bs = 0

        """
        무기
        """
        self.weapons = [weapon.Rifle_1(True)]
        self.select_weapon = 0

        self.event_que = []
        self.move_state = IDLE
        self.action_state = IDLE
        self.move_state.enter(self, None)

    def update(self):
        self.move_state.do(self)
        if self.action_state != IDLE:
            self.action_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            if WD <= event <= LSHU:
                if next_move_state[self.move_state][event] != IGNORE:
                    self.move_state.exit(self, event)
                    try:
                        self.move_state = next_move_state[self.move_state][event]
                    except KeyError:
                        print(f'ERROR: State {self.move_state.__name__} Event {event_name[event]}')
                    self.move_state.enter(self, event)
            else:
                if next_action_state[self.action_state][event] != IGNORE:
                    self.action_state.exit(self, event)
                    try:
                        self.action_state = next_action_state[self.action_state][event]
                    except KeyError:
                        print(f'ERROR: State {self.action_state.__name__} Event {event_name[event]}')
                    self.action_state.enter(self, event)

        self.weapons[self.select_weapon].setPos(self.x, self.y, self.body_rad)
        self.weapons[self.select_weapon].update()

    def change_state(self, state, nextstate):
        state = nextstate
        state.enter(self, None)

    def set_feet_dir(self):
        direction = [[3, 2, 1],
                     [4, 0, 0],
                     [5, 6, 7]]
        self.feet_direction = direction[1 - self.feet_dir_y][1 + self.feet_dir_x]

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
            self.weapons[self.select_weapon].handle_event(event)
        else:
            if event.type == SDL_MOUSEMOTION:
                self.cursor.set_pos(event.x, 800 - 1 - event.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def get_ps(self):
        return [Point(self.x + 10, self.y + 10), Point(self.x + 10, self.y - 10),
                Point(self.x - 10, self.y - 10), Point(self.x - 10, self.y + 10)]

    def draw(self):
        self.feet_image[self.fs].clip_composite_draw(int(self.feet_frame) * self.feet_image_w[self.fs], 0,
                                                     self.feet_image_w[self.fs], self.feet_image_h[self.fs],
                                                     (math.pi / 4) * self.feet_direction, '0', self.x, self.y,
                                                     self.feet_image_w[self.fs] // 5, self.feet_image_h[self.fs] // 5)

        self.body_image[self.bs].clip_composite_draw(int(self.body_frame) * self.body_image_w[self.bs], 0,
                                                     self.body_image_w[self.bs], self.body_image_h[self.bs],
                                                     self.body_rad, '0', self.x, self.y,
                                                     self.body_image_w[self.bs] // 5, self.body_image_h[self.bs] // 5)
        draw_rectangle(*self.get_bb())

    def get_circle(self):
        return Circle(Point(self.x, self.y), 10)

    def get_rect(self):
        return Rect(self.x, self.y, 20, 20, 0)

    def handle_collide(self, other):
        if type(other).__name__ == 'Bullet':
            self.armor -= other.damage
            if self.armor < 0:
                self.hp += self.armor
                self.armor = 0
                game_world.add_object(BloodEffect(self.x, self.y, other.rad + random.uniform(-0.5, 0.5)),
                                      game_world.CHARACTER_EFFECT_LAYER)

            if self.hp <= 0:
                game_world.add_object(DeadEffect(self.x, self.y), game_world.CHARACTER_EFFECT_LAYER)
                game_world.remove_object(self)

        if type(other).__name__ == 'Target':
            pass

        if type(other).__name__ == 'SandBarricade':
            speed = 0.0
            if self.fs == 1:
                speed = WALK_SPEED_PPS
            if self.fs == 2:
                speed = RUN_SPEED_PPS
            if self.feet_dir_x != 0 and self.feet_dir_y != 0:
                self.x -= self.feet_dir_x * speed * game_framework.frame_time / 1.4 + self.feet_dir_x
                self.y -= self.feet_dir_y * speed * game_framework.frame_time / 1.4 + self.feet_dir_y
            elif self.feet_dir_x != 0 or self.feet_dir_y != 0:
                self.x -= self.feet_dir_x * speed * game_framework.frame_time + self.feet_dir_x
                self.y -= self.feet_dir_y * speed * game_framework.frame_time + self.feet_dir_y

            self.x += self.feet_dir_x * speed * game_framework.frame_time
            if game_constant.Rect2Rect(self.get_ps(), other.get_ps()):
                self.x -= self.feet_dir_x * speed * game_framework.frame_time

            self.y += self.feet_dir_y * speed * game_framework.frame_time
            if game_constant.Rect2Rect(self.get_ps(), other.get_ps()):
                self.y -= self.feet_dir_y * speed * game_framework.frame_time


class Player(Character):
    feet_image = None
    feet_image_w = []
    feet_image_h = []
    body_image = None
    body_image_w = []
    body_image_h = []

    def __init__(self, x, y, hp, armor, main_weapon_num, sub_weapon_num, grenade_num):
        """
        캐릭터 위치 및 정보
        """
        self.x, self.y = x, y
        self.speed = 0
        self.hp = hp
        self.armor = armor
        """
        캐릭터 발  
        """
        # 0 = idle, 1 = walk, 2 = run
        if Player.feet_image is None:
            Player.feet_image = [load_image('image/character/player/feet/idle.png'),  # cnt = 1
                                 load_image('image/character/player/feet/walk.png'),  # cnt = 20
                                 load_image('image/character/player/feet/run.png')]  # cnt = 20
            Player.feet_image_w = [self.feet_image[0].w, self.feet_image[1].w // 20, self.feet_image[2].w // 20]
            Player.feet_image_h = [self.feet_image[0].h, self.feet_image[1].h, self.feet_image[2].h]

        self.feet_direction = 0
        self.feet_dir_x, self.feet_dir_y = 0, 0
        self.feet_frame = 0
        self.fs = 0
        """
        캐릭터 몸  
        """
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        if Player.body_image is None:
            Player.body_image = [[load_image('image/character/player/body/rifle1/idle.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle1/move.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle1/reload.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle1/shoot.png')],
                                 [load_image('image/character/player/body/rifle2/idle.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle2/move.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle2/reload.png'),  # cnt = 20
                                  load_image('image/character/player/body/rifle2/shoot.png')],
                                 [load_image('image/character/player/body/handgun/idle.png'),  # cnt = 20
                                  load_image('image/character/player/body/handgun/move.png'),  # cnt = 20
                                  load_image('image/character/player/body/handgun/reload.png'),  # cnt = 15
                                  load_image('image/character/player/body/handgun/shoot.png')], # cnt = 3
                                 [load_image('image/character/player/body/grenade/idle.png'),   # cnt = 20
                                  load_image('image/character/player/body/grenade/move.png'),   # cnt = 20
                                  load_image('image/character/player/body/grenade/shoot.png'),  # cnt = 15
                                  load_image('image/character/player/body/grenade/shoot.png')]]  # cnt = 15
            Player.body_image_w = [[self.body_image[0][0].w // 20, self.body_image[0][1].w // 20,
                                   self.body_image[0][2].w // 20, self.body_image[0][3].w // 3],
                                   [self.body_image[1][0].w // 20, self.body_image[1][1].w // 20,
                                   self.body_image[1][2].w // 20, self.body_image[1][3].w // 3],
                                   [self.body_image[2][0].w // 20, self.body_image[2][1].w // 20,
                                   self.body_image[2][2].w // 15, self.body_image[2][3].w // 3],
                                   [self.body_image[3][0].w // 20, self.body_image[3][1].w // 20,
                                    self.body_image[3][2].w // 15, self.body_image[3][3].w // 15]]
            Player.body_image_h = [[self.body_image[0][0].h, self.body_image[0][1].h,
                                   self.body_image[0][2].h, self.body_image[0][3].h],
                                   [self.body_image[1][0].h, self.body_image[1][1].h,
                                   self.body_image[1][2].h, self.body_image[1][3].h],
                                   [self.body_image[2][0].h, self.body_image[2][1].h,
                                   self.body_image[2][2].h, self.body_image[2][3].h],
                                   [self.body_image[3][0].h, self.body_image[3][1].h,
                                    self.body_image[3][2].h, self.body_image[3][3].h]]

        self.body_frame = 0
        self.body_reload_frame = 0
        self.body_rad = 0
        self.bs = 0
        """
        무기
        """
        self.weapons = []
        if main_weapon_num == 0:
            self.weapons.append(weapon.Rifle_1(True))
        if main_weapon_num == 1:
            self.weapons.append(weapon.Rifle_2(True))
        if sub_weapon_num == 0:
            self.weapons.append(weapon.Handgun(True))
        if grenade_num == 0:
            self.weapons.append(weapon.Grenades_1())
        if grenade_num == 1:
            self.weapons.append(weapon.Grenades_2())
        self.select_weapon = 0

        self.event_que = []
        self.move_state = IDLE
        self.action_state = IDLE
        self.move_state.enter(self, None)

    def update(self):
        self.move_state.do(self)
        if self.action_state != IDLE:
            self.action_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            if WD <= event <= LSHU:
                if next_move_state[self.move_state][event] != IGNORE:
                    self.move_state.exit(self, event)
                    try:
                        self.move_state = next_move_state[self.move_state][event]
                    except KeyError:
                        print(f'ERROR: State {self.move_state.__name__} Event {event_name[event]}')
                    self.move_state.enter(self, event)
            else:
                if next_action_state[self.action_state][event] != IGNORE:
                    self.action_state.exit(self, event)
                    try:
                        if self.returnNowWeapon() >= 3 and next_action_state[self.action_state][event] == SHOOT:
                            self.action_state = THROW
                        elif self.returnNowWeapon() >= 3 and next_action_state[self.action_state][event] == RELOAD:
                            self.action_state = IDLE
                        else:
                            self.action_state = next_action_state[self.action_state][event]
                    except KeyError:
                        print(f'ERROR: State {self.action_state.__name__} Event {event_name[event]}')
                    self.action_state.enter(self, event)

        self.setBodyRad()

        if self.x < 15:
            self.x = 15
        if self.x > 785:
            self.x = 785
        if self.y < 95:
            self.y = 95
        if self.y > 785:
            self.y = 785

        self.weapons[self.select_weapon].setPos(self.x, self.y, self.body_rad)
        self.weapons[self.select_weapon].update()

    def setBodyRad(self):
        cx, cy = play_state.cursor.get_pos()
        self.body_rad = math.atan2(self.y - cy, self.x - cx) - math.pi / 2
        point_distance = math.sqrt(math.pow(self.x - cx, 2) + math.pow(self.y - cy, 2))
        self.body_rad -= math.atan2(point_distance, 10)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
            self.weapons[self.select_weapon].handle_event(event)

    def getInfo(self):
        return self.hp, self.armor, self.weapons[self.select_weapon].magazine_capacity, self.weapons[self.select_weapon].ammo_max

    def returnNowWeapon(self):
        if type(self.weapons[self.select_weapon]).__name__ == 'Rifle_1':
            return 0
        elif type(self.weapons[self.select_weapon]).__name__ == 'Rifle_2':
            return 1
        elif type(self.weapons[self.select_weapon]).__name__ == 'Handgun':
            return 2
        elif type(self.weapons[self.select_weapon]).__name__ == 'Grenades_1' or type(self.weapons[self.select_weapon]).__name__ == 'Grenades_2':
            return 3
        else:
            return -1

    def draw(self):
        self.feet_image[self.fs].clip_composite_draw(int(self.feet_frame) * self.feet_image_w[self.fs], 0,
                                                     self.feet_image_w[self.fs], self.feet_image_h[self.fs],
                                                     (math.pi / 4) * self.feet_direction, '0', self.x, self.y,
                                                     self.feet_image_w[self.fs] // 5, self.feet_image_h[self.fs] // 5)

        nw = self.returnNowWeapon()
        self.body_image[nw][self.bs].clip_composite_draw(int(self.body_frame) * self.body_image_w[nw][self.bs], 0,
                                                         self.body_image_w[nw][self.bs], self.body_image_h[nw][self.bs],
                                                         self.body_rad, '0', self.x, self.y,
                                                         self.body_image_w[nw][self.bs] // 5,
                                                         self.body_image_h[nw][self.bs] // 5)

        draw_rectangle(*self.get_bb())


class Enemy(Character):
    feet_image = None
    feet_image_w = []
    feet_image_h = []
    body_image = None
    body_image_w = []
    body_image_h = []

    def __init__(self, x, y, hp, armor):
        """
        캐릭터 위치 및 정보
        """
        self.x, self.y = x, y
        self.speed = 0
        self.hp = hp
        self.armor = armor
        """
        캐릭터 발  
        """
        # 0 = idle, 1 = walk, 2 = run
        if Enemy.feet_image is None:
            Enemy.feet_image = [load_image('image/character/enemy/feet/idle.png'),  # cnt = 1
                                load_image('image/character/enemy/feet/walk.png'),  # cnt = 20
                                load_image('image/character/enemy/feet/run.png')]  # cnt = 20
            Enemy.feet_image_w = [self.feet_image[0].w, self.feet_image[1].w // 20, self.feet_image[2].w // 20]
            Enemy.feet_image_h = [self.feet_image[0].h, self.feet_image[1].h, self.feet_image[2].h]

        self.feet_direction = 0
        self.feet_dir_x, self.feet_dir_y = 0, 0
        self.feet_frame = 0
        self.fs = 0
        """
        캐릭터 몸  
        """
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        if Enemy.body_image is None:
            Enemy.body_image = [load_image('image/character/enemy/body/idle.png'),  # cnt = 20
                                load_image('image/character/enemy/body/move.png'),  # cnt = 20
                                load_image('image/character/enemy/body/reload.png'),  # cnt = 20
                                load_image('image/character/enemy/body/shoot.png')]  # cnt = 3
            Enemy.body_image_w = [self.body_image[0].w // 20, self.body_image[1].w // 20,
                                  self.body_image[2].w // 20, self.body_image[3].w // 3]
            Enemy.body_image_h = [self.body_image[0].h, self.body_image[1].h,
                                  self.body_image[2].h, self.body_image[3].h]

        self.body_frame = 0
        self.body_reload_frame = 0
        self.body_rad = 0
        self.bs = 0
        """
        무기
        """
        self.weapons = [weapon.Rifle_2(True), weapon.Gun(True), weapon.Gun(True)]
        self.select_weapon = 0

        self.event_que = []
        self.move_state = IDLE
        self.action_state = IDLE
        self.move_state.enter(self, None)


