import pico2d
import stage
import character

SCENE_WIDTH, SCENE_HEIGHT = 800, 800
game_running = True
map = None
player = None

pico2d.open_canvas(SCENE_WIDTH, SCENE_HEIGHT)

def set_game():
    global player, map
    map = stage.Stage()
    player = character.Character(SCENE_WIDTH // 2, SCENE_HEIGHT // 2)
    map.setStage(-1)    # test_stage

def game_input():
    global game_running
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            game_running = False
        player.events_handler(event)

def render_scene():
    pico2d.clear_canvas()
    map.render()
    player.render()
    pico2d.update_canvas()

def game_update():
    game_input()
    player.update()
    render_scene()
    pico2d.delay(0.03)


set_game()

while game_running == True:
    game_update()

pico2d.close_canvas()