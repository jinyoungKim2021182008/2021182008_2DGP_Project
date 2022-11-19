from pico2d import *

import game_framework
import game_world
import game_constant
import menu_state


class Item:
    image = None

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        if Item.image is None:
            pass

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def collide_handle(self, other):
        pass


class Target(Item):
    image = None

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        if Target.image is None:
            Target.image = load_image('image/item/target.png')

    def collide_handle(self, other):
        if game_world.returnEnemyCnt() == 0:
            print('you win')
            game_framework.change_state(menu_state)
        else:
            print(f'{game_world.returnEnemyCnt()} enemy left')
