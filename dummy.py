from game_constant import *


l1, l2 = Line(Point(5, 0), Point(5, 10)), Line(Point(0, 5), Point(10, 5))
p = Line2Line_ReturnPoint(l2, l1)
print(p.x, p.y)