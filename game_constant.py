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


class RectP:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


class Circle:
    def __init__(self, p, r):
        self.p = p
        self.r = r


def collide(object1, object2, pair):
    if pair == 'CO':
        if Rect2Rect(object1.getPs(), object2.getPs()):
            return True
        return False

    if pair == 'PI':
        # print(object1.get_bb())
        if AABB(object1.get_bb(), object2.get_bb()):
            return True
        return False

    if pair == 'BC':
        p = LineGr2Circle_RP(object1.getLine(), object1.rad, object2.getCircle())
        if p is not None:
            return [p, object2]
            # object1.collide_handle(object2, p)
            # object2.collide_handle(object1)

    if pair == 'BO':
        p = Line2Rect_RP(object1.getLine(), object2.getPs())
        if p is not None:
            return [p, object2]
            # object1.collide_handle(object2, p)
            # object2.collide_handle(object1)


def Point2Rect(p, rect):
    if p.x > rect.left and p.x < rect.right:
        if p.y > rect.bottom and p.y < rect.top:
            return True
    return False


"""
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
"""

def AABB(rect1, rect2):
    # lbrt
    if rect1[2] < rect2[0]:
        return False
    if rect1[3] < rect2[1]:
        return False
    if rect2[2] < rect1[0]:
        return False
    if rect2[3] < rect1[1]:
        return False
    return True


def Rect2Rect(rps1, rps2):
    ls1 = [Line(rps1[0], rps1[1]), Line(rps1[1], rps1[2]), Line(rps1[2], rps1[3]), Line(rps1[3], rps1[0])]
    ls2 = [Line(rps2[0], rps2[1]), Line(rps2[1], rps2[2]), Line(rps2[2], rps2[3]), Line(rps2[3], rps2[0])]
    for l1 in ls1:
        for l2 in ls2:
            if Line2Line(l1, l2):
                return True

    return False


def Line2Circle_RP(line, circle):
    d_rad = math.atan2(line.p2.y - line.p1.y, line.p2.x - line.p1.x) + math.pi / 2
    ds, dc = math.sin(d_rad), math.cos(d_rad)
    n_line = Line(Point(circle.p.x + circle.r * dc, circle.p.y + circle.r * ds),
                  Point(circle.p.x - circle.r * dc, circle.p.y - circle.r * ds))
    p = Line2Line_RP(n_line, line)
    return p


def Line2Circle(line, circle):
    d_rad = math.atan2(line.p2.y - line.p1.y, line.p2.x - line.p1.x) + math.pi / 2
    ds, dc = math.sin(d_rad), math.cos(d_rad)
    n_line = Line(Point(circle.p.x + circle.r * dc, circle.p.y + circle.r * ds),
                  Point(circle.p.x - circle.r * dc, circle.p.y - circle.r * ds))
    if Line2Line(n_line, line):
        return True
    return False


def LineGr2Circle_RP(line, rad, circle):
    d_rad = rad + math.pi / 2
    ds, dc = math.sin(d_rad), math.cos(d_rad)
    n_line = Line(Point(circle.p.x + circle.r * dc, circle.p.y + circle.r * ds),
                  Point(circle.p.x - circle.r * dc, circle.p.y - circle.r * ds))
    p = Line2Line_RP(n_line, line)
    return p


def LineGr2Circle(line, rad, circle):
    d_rad = rad + math.pi / 2
    ds, dc = math.sin(d_rad), math.cos(d_rad)
    n_line = Line(Point(circle.p.x + circle.r * dc, circle.p.y + circle.r * ds),
                  Point(circle.p.x - circle.r * dc, circle.p.y - circle.r * ds))
    if Line2Line(n_line, line):
        return True
    return False


def Line2Rect_RP(line, rps):
    min_p = None
    min_len = None

    ps = [Line2Line_RP(line, Line(rps[0], rps[1])), Line2Line_RP(line, Line(rps[1], rps[2])),
          Line2Line_RP(line, Line(rps[2], rps[3])), Line2Line_RP(line, Line(rps[3], rps[0]))]

    for p in ps:
        if p is not None:
            len = getLengthPow(line.p1, p)
            if min_len is None or len < min_len:
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


def Line2Line_RP(l1, l2):
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


# def returnGT(a, b, b):
#     if b:
#         if a >= b: return a
#         else: return b
#     else:
#         if a >= b: return b
#         else: return a

