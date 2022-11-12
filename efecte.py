from pico2d import *
import game_framework
import game_world

ACTION_PER_TIME = 30
FRAMES_PER_ACTION = 5


class BulletEffect:
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y):
        self.x, self.y = x, y
        if BulletEffect.image is None:
            BulletEffect.image = load_image('image/effect/bullet_effect.png')
            BulletEffect.image_w = self.image.w // 5
            BulletEffect.image_h = self.image.h
        self.frame = 0

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) >= FRAMES_PER_ACTION:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.image_w, 0, self.image_w, self.image_h, self.x, self.y, 15, 15)


PIXEL_PER_METER = 15.0
SPEED_KMPH = 30.0
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
SPEED_MPS = (SPEED_MPM / 60.0)
SPEED_PPS = (SPEED_MPS * PIXEL_PER_METER)


class BloodEffect:
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y, rad):
        self.x, self.y = x, y
        self.rad = rad
        if BloodEffect.image is None:
            BloodEffect.image = load_image('image/effect/blood_effect.png')
            BloodEffect.image_w = self.image.w
            BloodEffect.image_h = self.image.h
        self.frame = 0
        self.state = True
        self.size = 0

    def update(self):
        if self.state:
            self.frame = (self.frame + ACTION_PER_TIME * game_framework.frame_time)
            self.x += math.cos(self.rad) * SPEED_PPS * game_framework.frame_time
            self.y += math.sin(self.rad) * SPEED_PPS * game_framework.frame_time
            self.size = self.frame / FRAMES_PER_ACTION
            if int(self.frame) >= FRAMES_PER_ACTION:
                self.state = False

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image_w, self.image_h, self.rad, '0',
                                       self.x, self.y, self.image_w * self.size, self.image_h * self.size)


class DeadEffect:
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y):
        self.x, self.y = x, y
        if DeadEffect.image is None:
            DeadEffect.image = load_image('image/effect/dead_effect.png')
            DeadEffect.image_w = self.image.w
            DeadEffect.image_h = self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.image_w, self.image_h)
