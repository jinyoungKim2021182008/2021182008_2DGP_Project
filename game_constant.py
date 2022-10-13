import math

SCENE_WIDTH, SCENE_HEIGHT = 800, 800

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50


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
