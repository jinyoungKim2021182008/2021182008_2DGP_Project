import pico2d
import stage
from game_constant import *

game_running = True
stage = None

pico2d.open_canvas(SCENE_WIDTH, SCENE_HEIGHT)

def set_game():
    global stage
    stage = stage_manager.Stage()
    stage.setStage(-1)    # test_stage

def game_input():
    global game_running
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            game_running = False
        stage.events_handler(event)

def render_scene():
    pico2d.clear_canvas()
    stage.render()
    pico2d.update_canvas()

def game_update():
    game_input()
    stage.update()
    render_scene()
    pico2d.delay(0.03)


set_game()

while game_running == True:
    game_update()

pico2d.close_canvas()