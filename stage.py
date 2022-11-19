from pico2d import *

import character
import game_world

import ui
import object
import play_state
from character import Player, Enemy
from item import Target

from game_constant import *

stage_images = None
stage_num = None
STAGE_WIDTH, STAGE_HEIGHT = 0, 0

def setStage(n):
    global stage_images, stage_num, STAGE_WIDTH, STAGE_HEIGHT
    if stage_images is None:
        stage_images = [load_image('image/stage/stage_test.png'),
                        load_image('image/stage/stage_jungle.png'),
                        load_image('image/stage/stage_desert.png')]
        stage_num = 0

    game_world.add_object(ui.InfoBox(), game_world.UI_LAYER)
    if n == 0:
        stage_num = 0
        STAGE_WIDTH, STAGE_HEIGHT = 800, 800
        # stage_image
        game_world.add_object(stage_images[0], game_world.FLOOR_LAYER)
        # enemy
        game_world.add_object(Enemy(200, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(250, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(300, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(350, 200, 100, 100), game_world.CHARACTER_LAYER)
        # object
        game_world.add_object(object.SandBarricade(100, 170, 0), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(500, 500, 45), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(300, 400, 90), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(150, 600, 13), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(400, 300, 0), game_world.OBJECT_LAYER)
        # item
        game_world.add_object(Target(25, 775, 50, 50), game_world.ITEM_LAYER)
    elif n == 1:
        stage_num = 1
        STAGE_WIDTH, STAGE_HEIGHT = 800, 800
        # stage_image
        game_world.add_object(stage_images[0], game_world.FLOOR_LAYER)
        # enemy
        game_world.add_object(Enemy(200, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(250, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(300, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(350, 200, 100, 100), game_world.CHARACTER_LAYER)
        # object
        game_world.add_object(object.SandBarricade(100, 170, 0), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(500, 500, 45), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(300, 400, 90), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(150, 600, 13), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(400, 300, 0), game_world.OBJECT_LAYER)
        # item
        game_world.add_object(Target(25, 775, 50, 50), game_world.ITEM_LAYER)
    elif n == 2:
        stage_num = 2
        STAGE_WIDTH, STAGE_HEIGHT = 800, 800
        # stage_image
        game_world.add_object(stage_images[0], game_world.FLOOR_LAYER)
        # enemy
        game_world.add_object(Enemy(200, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(250, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(300, 200, 100, 100), game_world.CHARACTER_LAYER)
        game_world.add_object(Enemy(350, 200, 100, 100), game_world.CHARACTER_LAYER)
        # object
        game_world.add_object(object.SandBarricade(100, 170, 0), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(500, 500, 45), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(300, 400, 90), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(150, 600, 13), game_world.OBJECT_LAYER)
        game_world.add_object(object.SandBarricade(400, 300, 0), game_world.OBJECT_LAYER)
        # item
        game_world.add_object(Target(25, 775, 50, 50), game_world.ITEM_LAYER)

def drawStage():
    stage_images[stage_num].draw(STAGE_WIDTH // 2, STAGE_HEIGHT // 2, STAGE_WIDTH, STAGE_HEIGHT)

"""
class Stage:
    def __init__(self):
        self.objects = []
        self.enemies = []
        self.player = None
        self.stage_images = (load_image('image/stage/stage_test.png'),
                             load_image('image/stage/stage_jungle.png'),
                             load_image('image/stage/stage_desert.png'))
        self.stage_num = 0
        self.stage_w, self.stage_h = None, None

    def setStage(self, num):
        if num == -1:  # test_stage
            # set back
            self.stage_num = 0
            self.stage_w, self.stage_h = 800, 800
            # set object

            # set player
            self.player = character.Character(self.stage_w // 2, self.stage_h // 2, 100, 100)
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
        self.player.crashCharacter2Stage(self.stage_w, self.stage_h)

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
"""
