from pico2d import *
import game_framework
import game_world

ACTION_PER_TIME = 30
FRAMES_PER_ACTION = 5


class BulletEffect:
    image = None
    image_w, image_h = None, None

    def __init__(self, x, y):
        print(1)
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
