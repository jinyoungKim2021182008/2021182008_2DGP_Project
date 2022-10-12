from pico2d import *
import object

class Stage:
    def __init__(self):
        self.objects = []
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
            self.objects.append(object.SandBarricade(500, 500, 50))

        elif num == 0:  # jungle_stage
            # set back
            self.stage_num = 1
            self.stage_w, self.stage_h = 800, 800
            # set object

        elif num == 1:  # desert_stage
            # set back
            self.stage_num = 2
            self.stage_w, self.stage_h = 800, 800
            # set object

    def render(self):
        # draw back
        self.stage_images[self.stage_num].draw(self.stage_w // 2, self.stage_h // 2, self.stage_w, self.stage_h)
        # draw object
        for object in self.objects:
            object.render()
