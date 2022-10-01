from pico2d import *
import math

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
STAGE_WIDTH, STAGE_LENGTH = 800, 800

game_running = True
open_canvas(800, 800)

class Cursur:
    def __init__(self):
        pass
    pass

class Character:
    def __init__(self, x, y):
        self.x, self.y = x, y

        self.walk_speed, self.run_speed = 2.0, 5.0

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
        self.feet_direction = 0

        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.body_image = (load_image('image/character/body/idle.png'),             # cnt = 20
                           load_image('image/character/body/move.png'),             # cnt = 20
                           load_image('image/character/body/reload.png'),           # cnt = 20
                           load_image('image/character/body/shoot.png'))            # cnt = 3
        self.body_image_width = (self.body_image[0].w // 20, self.body_image[1].w // 20, self.body_image[2].w // 20, self.body_image[3].w // 3)
        self.body_image_height = (self.body_image[0].h, self.body_image[1].h, self.body_image[2].h, self.body_image[3].h)
        self.body_status = 0
        self.body_frame = 0
        self.body_rad = 0
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

    def walk(self, dir):
        self.feet_status = 1        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.body_status = 1        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.feet_direction = dir   # 0 = right, 1 = ru, 2 = up, 3 = lu, 4 = left, 5 = ld, 6 = down, 7 = rd

    def run(self, dir):
        self.feet_status = 2        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.body_status = 1        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.feet_direction = dir   # 0 = right, 1 = ru, 2 = up, 3 = lu, 4 = left, 5 = ld, 6 = down, 7 = rd

    def reload(self):
        self.body_status = 2        # 0 = idle, 1 = move, 2 = reload, 3 = shoot

    def attack(self):
        self.body_status = 3        # 0 = idle, 1 = move, 2 = reload, 3 = shoot

    def idle(self):
        self.feet_status = 0        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.feet_frame = 0
        self.body_status = 0        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.body_frame = 0

    def update(self):
        s = 0
        if self.feet_status == 1:
            s = self.walk_speed
        elif self.feet_status == 2:
            s = self.run_speed

        # 0 = right, 1 = ru, 2 = up, 3 = lu, 4 = left, 5 = ld, 6 = down, 7 = rd
        move_distance = ((s, 0), (s / 1.4, s / 1.4), (0, s), (-s / 1.4, s / 1.4),
                         (-s, 0), (-s / 1.4, -s / 1.4), (0, -s), (s / 1.4, -s / 1.4))
        self.x += move_distance[self.feet_direction][0]
        self.y += move_distance[self.feet_direction][1]

        self.animation()

    def render(self):
        fs, bs = self.feet_status, self.body_status
        self.feet_image[fs].clip_composite_draw(self.feet_frame * self.feet_image_width[fs], 0,
                                                self.feet_image_width[fs], self.feet_image_height[fs],
                                                (math.pi / 4) * self.feet_direction, '0', self.x, self.y,
                                                self.feet_image_width[fs] // 5, self.feet_image_height[fs] // 5)

        self.body_image[bs].clip_composite_draw(self.body_frame * self.body_image_width[bs], 0,
                                                self.body_image_width[bs], self.body_image_height[bs],
                                                self.body_rad, '0', self.x, self.y,
                                                self.body_image_width[bs] // 5, self.body_image_height[bs] // 5)



stage = load_image('image/stage/stage_test.png')
player = Character(STAGE_WIDTH // 2, STAGE_LENGTH // 2)


w, a, s, d = False, False, False, False
def input_manager():
    global game_running
    global w, a, s, d
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_running = False
            if event.key == SDLK_d:
                d = True
            elif event.key == SDLK_w:
                w = True
            elif event.key == SDLK_a:
                a = True
            elif event.key == SDLK_s:
                s = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                d = False
            elif event.key == SDLK_w:
                w = False
            elif event.key == SDLK_a:
                a = False
            elif event.key == SDLK_s:
                s = False

    if w and s:
        w, s = False, False
    if a and d:
        a, d = False, False

    if w and d:
        player.walk(1)
    elif w and a:
        player.walk(3)
    elif s and a:
        player.walk(5)
    elif s and d:
        player.walk(7)
    elif d:
        player.walk(0)
    elif w:
        player.walk(2)
    elif a:
        player.walk(4)
    elif s:
        player.walk(6)
    else:
        player.idle()

def render_scene():
    clear_canvas()
    stage.draw(STAGE_WIDTH // 2, STAGE_LENGTH // 2, STAGE_WIDTH, STAGE_LENGTH)
    player.render()
    update_canvas()

def game_update():
    input_manager()
    player.update()
    render_scene()
    delay(0.03)

def events_handler():
    events = get_events()
    print(events)

while game_running == True:
    game_update()

close_canvas()