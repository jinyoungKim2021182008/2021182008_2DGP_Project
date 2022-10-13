from pico2d import *

class SandBarricade:
    def __init__(self, x, y, rad):
        self.image = load_image('image/stage/stage_object/sand_barricade.png')
        self.rad = rad
        self.y = y
        self.x = x
    def setpos(self, x, y, rad):
        self.rad = rad
        self.x = y
        self.y = x

    def render(self):
        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, self.rad, '0', self.x, self.y, 100, 15)

class SteelBarricade:
    def __init__(self):

        pass

    def render(self):

        pass


class Stone:
    def __init__(self):
        pass

    def render(self):
        pass

class TargetPoint:
    def __init__(self):
        pass

    def render(self):
        pass


