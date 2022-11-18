from pico2d import *

import game_constant
import game_world
import play_state


class Cursor:
    def __init__(self):
        self.image = load_image('image/ui/cursor.png')
        self.x, self.y = 0, 0
        hide_cursor()
        game_world.add_object(self, game_world.UI_LAYER)

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def get_pos(self):
        return self.x, self.y

    def getPoint(self):
        return game_constant.Point(self.x, self.y)

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.set_pos(event.x, 800 - 1 - event.y)


class Button:
    def __init__(self, image1, image2, x, y, w, h, name):
        self.image = [image1, image2]
        self.state = 0
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.name = name
        game_world.add_object(self, game_world.UI_LAYER)

    def draw(self):
        self.image[self.state].draw(self.x, self.y, self.w, self.h)

    def update(self):
        pass

    def getRect(self):
        return game_constant.RectP(self.y + self.w // 2, self.y - self.w // 2, self.x - self.w // 2, self.x + self.w // 2)

class InfoBox:
    def __init__(self):
        self.image = load_image('image/ui/infobox.png')
        self.num_img = [load_image('image/ui/num/0.png'), load_image('image/ui/num/1.png'),
                        load_image('image/ui/num/2.png'), load_image('image/ui/num/3.png'),
                        load_image('image/ui/num/4.png'), load_image('image/ui/num/5.png'),
                        load_image('image/ui/num/6.png'), load_image('image/ui/num/7.png'),
                        load_image('image/ui/num/8.png'), load_image('image/ui/num/9.png')]
        # 10, 16
        self.w, self.h = 800, 80
        self.x, self.y = 400, 40
        self.hp, self.armor, self.maz, self.max = 0, 0, 0, 0

    def update(self):
        self.hp, self.armor, self.maz, self.max = play_state.player.getInfo()

    def drawInfo(self):
        hps = []
        hps.append(self.hp // 100)
        hps.append((self.hp - hps[0] * 100) // 10)
        hps.append(self.hp - hps[0] * 100 - hps[1] * 10)
        armors = []
        armors.append(self.armor // 100)
        armors.append((self.armor - armors[0] * 100) // 10)
        armors.append(self.armor - armors[0] * 100 - armors[1] * 10)
        mazs = []
        mazs.append(self.maz // 100)
        mazs.append((self.maz - mazs[0] * 100) // 10)
        mazs.append(self.maz - mazs[0] * 100 - mazs[1] * 10)
        maxs = []
        maxs.append(self.max // 100)
        maxs.append((self.max - maxs[0] * 100) // 10)
        maxs.append(self.max - maxs[0] * 100 - maxs[1] * 10)
        for i in range (3):
            self.num_img[hps[i]].draw(120 + i * 20, 56, 10, 16)
            self.num_img[armors[i]].draw(120 + i * 20, 24, 10, 16)
            self.num_img[mazs[i]].draw(575 + i * 20, 40, 10, 16)
            self.num_img[maxs[i]].draw(720 + i * 20, 40, 10, 16)


    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        self.drawInfo()