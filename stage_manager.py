from pico2d import *
import object
import character
from game_constant import *
import weapon


class Stage:
    def __init__(self):
        self.objects = []
        self.enemies = []
        self.player = None
        self.stage_images = (load_image('image/stage/stage_test.png'),
                             load_image('image/stage/stage_test.png'),
                             load_image('image/stage/stage_test.png'))
        self.stage_num = 0
        self.stage_w, self.stage_h = None, None

    def setStage(self, num):
        if num == -1:  # test_stage
            # set back
            self.stage_num = 0
            self.stage_w, self.stage_h = 800, 800
            # set object
            self.objects.append(object.SandBarricade(100, 100, 0))
            self.objects.append(object.SandBarricade(500, 500, 45))
            self.objects.append(object.SandBarricade(300, 400, 90))
            self.objects.append(object.SandBarricade(400, 300, 0))
            # set player
            self.player = character.Character(self.stage_w // 2, self.stage_h // 2)
            # set enemies

        elif num == 0:  # jungle_stage
            # set back
            self.stage_num = 1
            self.stage_w, self.stage_h = 800, 800
            # set object

            # set player

            # set enemies

        elif num == 1:  # desert_stage
            # set back
            self.stage_num = 2
            self.stage_w, self.stage_h = 800, 800
            # set object

            # set player

            # set enemies

    def events_handler(self, event):
        self.player.events_handler(event)

    def update(self):
        self.player.update()

        for i in range(0, 30):
            if self.player.main_weapon.check_bullets[i]:
                for object in self.objects:
                    if bullet_crash(self.player.main_weapon.bullets[i], object):
                        self.player.main_weapon.check_bullets[i] = False

        for object in self.objects:
            crashCharacter2Object(self.player, object)

    def render(self):
        # draw back
        self.stage_images[self.stage_num].draw(self.stage_w // 2, self.stage_h // 2, self.stage_w, self.stage_h)
        # draw object
        for object in self.objects:
            object.render()

        # draw player
        self.player.render()
