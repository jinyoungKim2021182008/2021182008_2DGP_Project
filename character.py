from pico2d import *

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
STAGE_WIDTH, STAGE_LENGTH = 800, 800

game_running = True
open_canvas(800, 800)

class Character:
    def __init__(self, x, y, angle):
        self.x, self.y, self.angle = x, y, angle

        self.walk_speed, self.run_speed = 1.0, 2.0

        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.feet_image = (load_image('image/character/feet/idle.png'),             # cnt = 1
                           load_image('image/character/feet/walk.png'),             # cnt = 20
                           load_image('image/character/feet/run.png'),              # cnt = 20
                           load_image('image/character/feet/strafe_left.png'),      # cnt = 20
                           load_image('image/character/feet/strafe_right.png'))     # cnt = 20
        self.feet_image_width = (self.feet_image[0].w, self.feet_image[1].w // 20, self.feet_image[2].w // 20, self.feet_image[3].w // 20, self.feet_image[4].w // 20)
        self.feet_image_height = (self.feet_image[0].h, self.feet_image[1].h, self.feet_image[2].h, self.feet_image[3].h, self.feet_image[4].h)
        self.feet_status = 0
        self.feet_frame = 0

        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.body_image = (load_image('image/character/body/idle.png'),             # cnt = 20
                           load_image('image/character/body/move.png'),             # cnt = 20
                           load_image('image/character/body/reload.png'),           # cnt = 20
                           load_image('image/character/body/shoot.png'))            # cnt = 3
        self.body_image_width = (self.body_image[0].w // 20, self.body_image[1].w // 20, self.body_image[2].w // 20, self.body_image[3].w // 3)
        self.body_image_height = (self.body_image[0].h, self.body_image[1].h, self.body_image[2].h, self.body_image[3].h)
        self.body_status = 0
        self.body_frame = 0

    def animation(self):
        # feet animation
        if self.feet_status == 0:
            self.feet_frame = 0
        else:
            self.feet_frame = (self.feet_frame + 1) % 20
        # body animation
        if self.body_status == 3:
            self.body_frame = 3
        else:
            self.body_frame = (self.body_frame + 1) % 20

    def move(self):
        self.feet_status = 1
        self.feet_frame = 0
        self.body_status = 1
        self.body_frame = 0

    def reload(self):
        self.body_status = 2
        self.body_frame = 0

    def attack(self):
        self.body_status = 3
        self.body_frame = 0

    def idle(self):
        self.feet_status = 0
        self.feet_frame = 0
        self.body_status = 0
        self.body_frame = 0

    def render(self):
        fs, bs = self.feet_status, self.body_status
        self.feet_image[fs].clip_draw(self.feet_frame * self.feet_image_width[fs], 0, self.feet_image_width[fs], self.feet_image_height[fs],
                                                    self.x, self.y, self.feet_image_width[fs] // 5, self.feet_image_height[fs] // 5)
        self.body_image[bs].clip_draw(self.body_frame * self.body_image_width[bs], 0, self.body_image_width[bs], self.body_image_height[bs],
                                                    self.x, self.y, self.body_image_width[bs] // 5, self.body_image_height[bs] // 5)


player = Character(STAGE_WIDTH // 2, STAGE_LENGTH // 2, 0)
#player.move()

def render_scene():
    clear_canvas()
    player.render()
    update_canvas()

def game_update():
    player.animation()
    render_scene()
    delay(0.05)

while game_running == True:
    game_update()

close_canvas()