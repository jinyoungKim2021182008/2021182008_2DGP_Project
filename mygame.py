import game_framework
import pico2d

import play_state
import menu_state

pico2d.open_canvas(800, 800)
game_framework.run(menu_state)
pico2d.close_canvas()