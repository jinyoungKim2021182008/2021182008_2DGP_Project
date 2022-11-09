from pico2d import *

class SandBarricade:
    def __init__(self, x, y, degree):
        self.image = load_image('image/stage/stage_object/sand_barricade.png')
        self.img = load_image('image/gp.png')
        self.rad = math.radians(degree)
        self.y = y
        self.x = x
        self.width = 100
        self.height = 15

    def update(self):
        pass

    def setpos(self, x, y, rad):
        self.rad = rad
        self.x = y
        self.y = x

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                       self.rad, '0', self.x, self.y, self.width, self.height)
        d = (self.width / 2) - 10
        rx, ry = math.cos(self.rad), math.sin(self.rad)
        x1, y1 = self.x + d * rx, self.y + d * ry
        x2, y2 = self.x - d * rx, self.y - d * ry
        self.img.draw(x1, y1)
        self.img.draw(x2, y2)

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


