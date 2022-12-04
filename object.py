import math

from pico2d import *

from game_constant import Point, Rect


class SandBarricade:
    def __init__(self, x, y, degree):
        self.image = load_image('image/stage/stage_object/sand_barricade.png')
        self.img = load_image('image/gp.png')
        self.rad = math.radians(degree)
        self.y = y
        self.x = x
        self.width = 100
        self.height = 15
        self.ps = []
        dis = math.sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)
        dtheta = math.atan(self.height / self.width)
        self.ps.append(Point(self.x + dis * math.cos(self.rad + dtheta),
                             self.y + dis * math.sin(self.rad + dtheta)))
        self.ps.append(Point(self.x + dis * math.cos(self.rad - dtheta),
                             self.y + dis * math.sin(self.rad - dtheta)))
        self.ps.append(Point(self.x + dis * math.cos(self.rad + dtheta + math.pi),
                             self.y + dis * math.sin(self.rad + dtheta + math.pi)))
        self.ps.append(Point(self.x + dis * math.cos(self.rad - dtheta + math.pi),
                             self.y + dis * math.sin(self.rad - dtheta + math.pi)))

    def update(self):
        pass

    def set_pos(self, x, y, rad):
        self.rad = rad
        self.x = y
        self.y = x

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                       self.rad, '0', self.x, self.y, self.width, self.height)

    def get_ps(self):
        return self.ps

    def handle_collide(self, other):
        pass


class SteelBarricade:
    def __init__(self):

        pass

    def draw(self):

        pass


class Stone:
    def __init__(self):
        pass

    def draw(self):
        pass

class TargetPoint:
    def __init__(self):
        pass

    def draw(self):
        pass


