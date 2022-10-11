from pico2d import *
import math
import weapon

CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
STAGE_WIDTH, STAGE_LENGTH = 800, 800
SCENE_WIDTH, SCENE_HEIGHT = 800, 800

game_running = True
open_canvas(STAGE_WIDTH, STAGE_LENGTH)

class Cursur:
    def __init__(self):
        self.cursur_image = load_image('image/character/cursur.png')
        self.x, self.y = SCENE_WIDTH // 2, SCENE_HEIGHT // 2
        hide_cursor()
        pass

    def set_pos(self, x, y):
        self.x, self.y = x, y
    def render(self):
        self.cursur_image.draw(self.x, self.y, 30, 30)

class Character:
    def __init__(self, x, y):
        """
        캐릭터 위치 및 정보
        """
        self.x, self.y = x, y
        self.walk_speed, self.run_speed = 2.0, 3.5

        """
        캐릭터 발  
        """
        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.feet_image = (load_image('image/character/feet/idle.png'),             # cnt = 1
                           load_image('image/character/feet/walk.png'),             # cnt = 20
                           load_image('image/character/feet/run.png'),              # cnt = 20
                           load_image('image/character/feet/strafe_left.png'),      # cnt = 20
                           load_image('image/character/feet/strafe_right.png'))     # cnt = 20
        self.feet_image_width = (self.feet_image[0].w, self.feet_image[1].w // 20, self.feet_image[2].w // 20, self.feet_image[3].w // 20, self.feet_image[4].w // 20)
        self.feet_image_height = (self.feet_image[0].h, self.feet_image[1].h, self.feet_image[2].h, self.feet_image[3].h, self.feet_image[4].h)
        self.feet_status = 0    # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        self.feet_direction = 0
        self.feet_dir_x = 0
        self.feet_dir_y = 0
        self.feet_frame = 0

        """
        캐릭터 몸  
        """
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        self.body_image = (load_image('image/character/body/idle.png'),             # cnt = 20
                           load_image('image/character/body/move.png'),             # cnt = 20
                           load_image('image/character/body/reload.png'),           # cnt = 20
                           load_image('image/character/body/shoot.png'))            # cnt = 3
        self.body_image_width = (self.body_image[0].w // 20, self.body_image[1].w // 20, self.body_image[2].w // 20, self.body_image[3].w // 3)
        self.body_image_height = (self.body_image[0].h, self.body_image[1].h, self.body_image[2].h, self.body_image[3].h)
        self.body_status = 0
        self.body_frame = 0
        self.body_reload_frame = 0
        self.body_rad = 0

        """
        조작키
        """
        self.run_key = False
        self.shoot_key = False
        self.reload_key = False

        """
        커서
        """
        self.cursur = Cursur()

        """
        무기
        """
        self.main_weapon = weapon.Rifle_1(True)

    def animation(self):
        # feet animation
        if self.feet_status == 0:
            self.feet_frame = 0
        else:
            self.feet_frame = (self.feet_frame + 1) % 20

        # body animation
        if self.body_status == 3:
            self.body_frame = (self.body_frame + 1) % 3
        elif self.reload_key:
            self.body_reload_frame = (self.body_reload_frame + 1) % 2
            if self.body_reload_frame == 1:
                self.body_frame += 1
            if self.body_frame >= 19:
                self.reload_key = False
        else:
            self.body_frame = (self.body_frame + 1) % 20


    def attack(self):
        if self.body_status == 3 and self.body_frame == 0:
            self.main_weapon.shoot(self.x, self.y, self.body_rad)

    def move(self):
        # 0 = idle, 1 = walk, 2 = run, 3 = left_strafe, 4 = right_strafe
        if self.feet_dir_x == 0 and self.feet_dir_y == 0:   # idle
            self.feet_status = 0
        elif self.run_key:
            self.feet_status = 2
        else:
            self.feet_status = 1

        speed = 0
        if self.feet_status == 1:
            speed = self.walk_speed
        elif self.feet_status == 2:
            speed = self.run_speed

        # 0 = right, 1 = ru, 2 = up, 3 = lu, 4 = left, 5 = ld, 6 = down, 7 = rd
        direction = ((3, 2, 1),
                     (4, 0, 0),
                     (5, 6, 7))
        self.feet_direction = direction[1 - self.feet_dir_y][1 + self.feet_dir_x]
        move_distance = ((speed, 0), (speed / 1.4, speed / 1.4), (0, speed), (-speed / 1.4, speed / 1.4),
                         (-speed, 0), (-speed / 1.4, -speed / 1.4), (0, -speed), (speed / 1.4, -speed / 1.4))
        self.x += move_distance[self.feet_direction][0]
        self.y += move_distance[self.feet_direction][1]
        # 몸의 커서를 따라감
        self.body_rad = math.atan2(self.y - self.cursur.y, self.x - self.cursur.x) + math.pi
        #point_distance = math.pow(self.x - self.cursur.x, 2) + math.pow(self.y - self.cursur.y, 2)
        #self.body_rad -= math.atan2(point_distance, 400)

    def action(self):
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        if self.reload_key:
            self.body_status = 2
        elif self.shoot_key:
            self.body_status = 3
        elif self.feet_status == 0:
            self.body_status = 0
        else:
            self.body_status = 1

    def update(self):
        self.action()
        self.move()
        self.attack()
        self.main_weapon.update()

        self.animation()



    def events_handler(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.feet_dir_x += 1
            elif event.key == SDLK_w:
                self.feet_dir_y += 1
            elif event.key == SDLK_a:
                self.feet_dir_x -= 1
            elif event.key == SDLK_s:
                self.feet_dir_y -= 1
            elif event.key == SDLK_r:
                self.reload_key = True
                self.body_frame = 0
            elif event.key == SDLK_LSHIFT:
                self.run_key = True
                self.body_frame = 0

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                self.feet_dir_x -= 1
            elif event.key == SDLK_w:
                self.feet_dir_y -= 1
            elif event.key == SDLK_a:
                self.feet_dir_x += 1
            elif event.key == SDLK_s:
                self.feet_dir_y += 1
            elif event.key == SDLK_LSHIFT:
                self.run_key = False

        elif event.type == SDL_MOUSEMOTION:
            player.cursur.set_pos(event.x, SCENE_HEIGHT - 1 - event.y)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            self.shoot_key = True

        elif event.type == SDL_MOUSEBUTTONUP:
            self.shoot_key = False

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

        self.cursur.render()

        self.main_weapon.render()


stage = load_image('image/stage/stage_test.png')
player = Character(STAGE_WIDTH // 2, STAGE_LENGTH // 2)

game_running = True

def input_manager():
    global game_running
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_running = False
        player.events_handler(event)

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

while game_running == True:
    game_update()

close_canvas()