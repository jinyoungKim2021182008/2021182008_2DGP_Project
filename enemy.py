import math

from pico2d import *
from character import *
from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf
import play_state

class Enemy(Character):
    feet_image = None
    feet_image_w = []
    feet_image_h = []
    body_image = None
    body_image_w = []
    body_image_h = []

    def __init__(self, x, y, hp, armor):
        """
        캐릭터 위치 및 정보
        """
        self.x, self.y = x, y
        self.tx, self.ty, self.trad = x, y, 0.0
        self.speed = 0
        self.hp = hp
        self.armor = armor
        self.timer = 1.0
        """
        캐릭터 발  
        """
        # 0 = idle, 1 = walk, 2 = run
        if Enemy.feet_image is None:
            Enemy.feet_image = [load_image('image/character/enemy/feet/idle.png'),  # cnt = 1
                                load_image('image/character/enemy/feet/walk.png'),  # cnt = 20
                                load_image('image/character/enemy/feet/run.png')]  # cnt = 20
            Enemy.feet_image_w = [self.feet_image[0].w, self.feet_image[1].w // 20, self.feet_image[2].w // 20]
            Enemy.feet_image_h = [self.feet_image[0].h, self.feet_image[1].h, self.feet_image[2].h]

        self.feet_direction = 0
        self.feet_dir_x, self.feet_dir_y = 0, 0
        self.feet_frame = 0
        self.fs = 0
        """
        캐릭터 몸  
        """
        # 0 = idle, 1 = move, 2 = reload, 3 = shoot
        if Enemy.body_image is None:
            Enemy.body_image = [load_image('image/character/enemy/body/idle.png'),  # cnt = 20
                                load_image('image/character/enemy/body/move.png'),  # cnt = 20
                                load_image('image/character/enemy/body/reload.png'),  # cnt = 20
                                load_image('image/character/enemy/body/shoot.png')]  # cnt = 3
            Enemy.body_image_w = [self.body_image[0].w // 20, self.body_image[1].w // 20,
                                  self.body_image[2].w // 20, self.body_image[3].w // 3]
            Enemy.body_image_h = [self.body_image[0].h, self.body_image[1].h,
                                  self.body_image[2].h, self.body_image[3].h]

        self.body_frame = 0
        self.body_reload_frame = 0
        self.body_rad = 0
        self.bs = 0
        """
        무기
        """
        self.weapons = [weapon.Rifle_1(True)]
        self.select_weapon = 0

        self.event_que = []
        self.move_state = IDLE
        self.action_state = IDLE
        self.move_state.enter(self, None)

        self.build_behavior_tree()

    def calculate_current_position(self):
        # self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # self.x = clamp(50, self.x, 1280 - 50)
        # self.y = clamp(50, self.y, 1024 - 50)

        # print(self.trad, self.body_rad)
        pass

    def shoot(self):
        if self.timer <= 0:
            self.action_state.exit(self, 'q')
            self.action_state = SHOOT
            self.action_state.enter(self, 'q')
            self.timer = 0.1
        return BehaviorTree.SUCCESS

    def check_ammo(self):
        if self.weapons[self.select_weapon].magazine_capacity <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def reload(self):
        if self.action_state != RELOAD:
            self.action_state.exit(self, 'q')
            self.action_state = RELOAD
            self.action_state.enter(self, 'q')
        return BehaviorTree.SUCCESS

    def find_player(self):
        px, py = play_state.player.x, play_state.player.y
        dis = math.sqrt((px - self.x) ** 2 + (py - self.y) ** 2)
        if dis < 500.0:
            trad = math.atan2(py - self.y, px - self.x)
            if math.degrees(math.fabs(self.body_rad - trad)) < 45.0 or math.degrees(math.fabs(self.body_rad + trad)) < 45.0 or dis < 100.0:
                self.trad = trad
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def idle(self):
        if self.action_state != IDLE:
            self.action_state = IDLE
            self.action_state.enter(self, 'q')
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def turn_head(self):
        if math.fabs(self.trad - self.body_rad) < math.fabs(self.trad + self.body_rad):
            drad = self.trad - self.body_rad
        else:
            drad = self.trad + self.body_rad

        if math.fabs(drad) < 0.1:
            self.body_rad = self.trad
            return BehaviorTree.SUCCESS
        elif drad < 0:
            self.body_rad -= 0.1
        elif drad > 0:
            self.body_rad += 0.1
        if math.fabs(self.body_rad) > math.pi:
            self.body_rad %= math.pi
        return BehaviorTree.FAIL

    """
    def find_random_location(self):
        self.tx, self.ty = random.randint(50, 1230), random.randint(50, 974)
        return BehaviorTree.SUCCESS

    def move_to(self, radius = 0.5):
        distance = (self.tx - self.x) ** 2 + (self.ty - self.y) ** 2
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        if distance < (PIXEL_PER_METER * radius) ** 2:
            self.speed = 0
            return BehaviorTree.SUCCESS
        else:
            self.speed = 10
            return BehaviorTree.RUNNING
    """
    def update(self):
        self.move_state.do(self)
        self.timer -= game_framework.frame_time
        if self.action_state != IDLE:
            self.action_state.do(self)

        self.weapons[self.select_weapon].setPos(self.x, self.y, self.body_rad)
        self.weapons[self.select_weapon].update()

        self.bt.run()
        self.calculate_current_position()

    def calculate_squared_distance(self, a, b):
        return (a.x-b.x)**2 + (a.y-b.y)**2

    def move_to_target(self):
        # fill here
        pass

    def build_behavior_tree(self):
        # find_random_location_node = Leaf('Find Random Location', self.find_random_location)
        # move_to_node = Leaf('Move To', self.move_to)
        # wander_sequence = Sequence('Wander', find_random_location_node, move_to_node)

        check_ammo_node = Leaf('Check Ammo', self.check_ammo)
        reload_node = Leaf('Reload', self.reload)
        ammo_sequence = Sequence('Ammo', check_ammo_node, reload_node)

        find_player_node = Leaf('Find Player', self.find_player)
        turn_head_node = Leaf('Turn Head', self.turn_head)
        shoot_node = Leaf('Shoot Head', self.shoot)
        player_sequence = Sequence('Player', find_player_node, turn_head_node, shoot_node)

        idle_node = Leaf('Idle', self.idle)
        idle_sequence = Sequence('Ammo', idle_node)

        selector = Selector('Wander or Eat Ball', ammo_sequence, player_sequence, idle_sequence)
        self.bt = BehaviorTree(selector)
