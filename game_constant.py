from pico2d import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Rect:
    def __init__(self, p, width, height, rad):
        self.p = p
        self.width = width
        self.height = height
        self.rad = rad


def collide(object1, object2):
    object1_name, object2_name = type(object1).__name__, type(object2).__name__

    if object1_name == 'Bullet' and object2_name == 'Character':
        pass

    if object1_name == 'Bullet' and object2_name == 'SandBarricade':
        if Line2Rect(object1.getLine(), object2.getRect()):
            object1.collide_handle(object2)
            object2.collide_handle(object1)


"""
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

"""
def Line2Rect_ReturnPoint(line, rect):
    rs, rc = math.sin(rect.rad), math.cos(rect.rad)
    rp1 = Point(rect.p.x - (rect.width / 2) * rc, rect.p.y - (rect.height / 2) * rs)
    rp2 = Point(rect.p.x + (rect.width / 2) * rc, rect.p.y - (rect.height / 2) * rs)
    rp3 = Point(rect.p.x + (rect.width / 2) * rc, rect.p.y + (rect.height / 2) * rs)
    rp4 = Point(rect.p.x - (rect.width / 2) * rc, rect.p.y + (rect.height / 2) * rs)

    min_p = None
    min_len = None

    ps = []
    ps += Line2Line_ReturnPoint(line, Line(rp1, rp2))
    ps += Line2Line_ReturnPoint(line, Line(rp2, rp3))
    ps += Line2Line_ReturnPoint(line, Line(rp3, rp4))
    ps += Line2Line_ReturnPoint(line, Line(rp4, rp1))

    for p in ps:
        if p is not None:
            len = getLengthPow(line.p1, p)
            if len < min_len or min_len is None:
                min_p, min_len = p, len
    return min_p


def Line2Rect(line, rect):
    rs, rc = math.sin(rect.rad), math.cos(rect.rad)
    rp1 = Point(rect.p.x - (rect.width / 2) * rc, rect.p.y - (rect.height / 2) * rs)
    rp2 = Point(rect.p.x + (rect.width / 2) * rc, rect.p.y - (rect.height / 2) * rs)
    rp3 = Point(rect.p.x + (rect.width / 2) * rc, rect.p.y + (rect.height / 2) * rs)
    rp4 = Point(rect.p.x - (rect.width / 2) * rc, rect.p.y + (rect.height / 2) * rs)

    if Line2Line(line, Line(rp1, rp2)):
        return True
    if Line2Line(line, Line(rp2, rp3)):
        return True
    if Line2Line(line, Line(rp3, rp4)):
        return True
    if Line2Line(line, Line(rp4, rp1)):
        return True

    return False


def Line2Line_ReturnPoint(l1, l2):
    if Line2Line(l1, l2):
        x1 = l1.p1.x - l1.p2.x
        x2 = l2.p1.x - l2.p2.x
        y1 = l1.p1.y - l1.p2.y
        y2 = l2.p1.y - l2.p2.y
        b = x1 * y2 - y1 * x2
        if b == 0:
            return None
        else:
            z1, z2 = l1.p1.x * l1.p2.y - l1.p1.y * l1.p2.x, l2.p1.x * l2.p2.y - l2.p1.y * l2.p2.x
            return Point((z1 * x2 - x1 * z2) / b, (z1 * y2 - y1 * z2) / b)
    return None


def Line2Line(l1, l2):
    a = l1.p1
    b = l1.p2
    c = l2.p1
    d = l2.p2

    ab = CCW(a, b, c) * CCW(a, b, d)
    cd = CCW(c, d, a) * CCW(c, d, b)
    if ab == 0 and cd == 0:
        if a > b: a, b = b, a
        if c > d: c, d = d, c
        return c <= b and a <= d

    return ab <= 0 and cd <= 0


def CCW(p1, p2, p3):
    val = (p1.x * p2.y + p2.x * p3.y + p3.x * p1.y - (p2.x * p1.y + p3.x * p2.y + p1.x * p3.y))
    if val > 0:
        return 1
    elif val == 0:
        return 0
    else:
        return -1


def getLength(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def getLengthPow(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

"""
def returnGT(a, b, bool):
    if bool:
        if a >= b: return a
        else: return b
    else:
        if a >= b: return b
        else: return a
"""
