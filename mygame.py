import game_framework
import game_constant
import pico2d

import play_state

pico2d.open_canvas(game_constant.SCENE_WIDTH, game_constant.SCENE_HEIGHT)
game_framework.run(play_state)
pico2d.close_canvas()