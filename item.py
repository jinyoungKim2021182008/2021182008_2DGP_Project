from pico2d import *

import game_framework
import game_world
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

    def handle_collide(self, other):
        pass


class Target(Item):
    image = None

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        if Target.image is None:
            Target.image = load_image('image/item/target.png')

    def handle_collide(self, other):
        if game_world.return_enemy_cnt() == 0:
            print('you win')
            game_framework.change_state(menu_state)
        else:
            print(f'{game_world.return_enemy_cnt()} enemy left')


class HealPack(Item):
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        if Target.image is None:
            Target.image = load_image('image/item/heal_pack.png')

    def handle_collide(self, other):
        game_world.remove_object(self)


class ArmorPack(Item):
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        if Target.image is None:
            Target.image = load_image('image/item/armor_pack.png')

    def handle_collide(self, other):
        game_world.remove_object(self)
