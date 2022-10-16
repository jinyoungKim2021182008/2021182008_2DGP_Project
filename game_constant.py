import math
import object
import character
from pico2d import *

SCENE_WIDTH, SCENE_HEIGHT = 800, 800

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
CHARACTER_WALK_SPEED, CHARACTER_RUN_SPEED = 2, 3.5


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def bullet_crash(bullet, other):
    if type(other).__name__ == 'SandBarricade':
        bx1, by1 = bullet.x - 25 * math.cos(bullet.rad), bullet.y - 25 * math.sin(bullet.y)
        bx2, by2 = bullet.x + 25 * math.cos(bullet.rad), bullet.y + 25 * math.sin(bullet.y)

        if crashLine2Rect(bx1, by1, bx2, by2, other.x, other.y, other.rad, 100, 15):
            return True

    return False

def crashCharacter2Object(character, object):
    d = (object.width / 2) - 20
    dis = object.height + 10
    rad = object.rad
    rx, ry = math.cos(rad), math.sin(rad)
    x1, y1 = object.x + d * rx, object.y + d * ry
    x2, y2 = object.x - d * rx, object.y - d * ry

    return_crash = crashCircle2Line(character.x, character.y, dis, x1, y1, x2, y2, rad)

    if return_crash > 0:
        if character.feet_dir_x == 1:  # right move
            character.x -= character.speed
        elif character.feet_dir_x == -1:  # left move
            character.x += character.speed
        if character.feet_dir_y == 1:  # up move
            character.y -= character.speed
        elif character.feet_dir_y == -1:  # down move
            character.y += character.speed

    if return_crash == 1:
        if character.feet_dir_x == 1:  # right move
            character.x += character.speed * math.cos(rad)
            if rad != math.pi / 2 and rad != math.pi / 2 * 3:
                character.y += character.speed * math.sin(rad)
        elif character.feet_dir_x == -1:  # left move
            character.x -= character.speed * math.cos(rad)
            if rad != math.pi / 2 and rad != math.pi / 2 * 3:
                character.y -= character.speed * math.sin(rad)
        if character.feet_dir_y == 1:  # up move
            if rad != 0 and rad != math.pi:
                character.x += character.speed * math.cos(rad)
            character.y += character.speed * math.sin(rad)
        elif character.feet_dir_y == -1:  # down move
            if rad != 0 and rad != math.pi:
                character.x -= character.speed * math.cos(rad)
            character.y -= character.speed * math.sin(rad)

    elif return_crash == 2 or return_crash == 3:
        pass


def crashCircle2Line(cx, cy, r, x1, y1, x2, y2, rad):
    d_rad = rad + math.pi / 2
    rx, ry = math.cos(d_rad), math.sin(d_rad)
    cx1, cy1 = cx + r * rx, cy + r * ry
    cx2, cy2 = cx - r * rx, cy - r * ry
    if crashLine2Line(Point(cx1, cy1), Point(cx2, cy2), Point(x1, y1), Point(x2, y2)):
        return 1
    val = pow(x1 - cx, 2) + pow(y1 - cy, 2)
    if val <= r * r:
        return 2
    val = pow(x2 - cx, 2) + pow(y2 - cy, 2)
    if val <= r * r:
        return 3

    return -1


def crashLine2Rect(x1, y1, x2, y2, rx, ry, rad, rw, rh):
    lp1 = Point(x1, y1)
    lp2 = Point(x2, y2)

    rp1 = Point(rx - (rw / 2) * math.cos(rad), ry - (rh / 2) * math.sin(rad))
    rp2 = Point(rx + (rw / 2) * math.cos(rad), ry - (rh / 2) * math.sin(rad))
    rp3 = Point(rx + (rw / 2) * math.cos(rad), ry + (rh / 2) * math.sin(rad))
    rp4 = Point(rx - (rw / 2) * math.cos(rad), ry + (rh / 2) * math.sin(rad))

    if crashLine2Line(lp1, lp2, rp1, rp2):
        return True
    if crashLine2Line(lp1, lp2, rp2, rp3):
        return True
    if crashLine2Line(lp1, lp2, rp3, rp4):
        return True
    if crashLine2Line(lp1, lp2, rp4, rp1):
        return True

    return False


def crashLine2Line(p1, p2, p3, p4):
    a = CCW(p1, p2, p3)
    b = CCW(p1, p2, p4)
    c = CCW(p3, p4, p1)
    d = CCW(p3, p4, p2)

    if a * b <= 0 and c * d <= 0:
        return True

    return False


def CCW(p1, p2, p3):
    val = (p1.x * p2.y + p2.x * p3.y + p3.x * p1.y - (p2.x * p1.y + p3.x * p2.y + p1.x * p3.y))

    if val > 0:
        return 1
    elif val == 0:
        return 0
    else:
        return -1


def returnGT(a, b, bool):
    if bool:
        if a >= b:
            return a
        else:
            return b
    else:
        if a >= b:
            return b
        else:
            return a
