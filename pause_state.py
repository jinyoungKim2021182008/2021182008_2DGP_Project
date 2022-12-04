from pico2d import *
import game_framework
import play_state
import menu_state


pause_image = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            play_state.exit()
            game_framework.change_state(play_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            play_state.exit()
            game_framework.change_state(menu_state)


def enter():
    global pause_image
    pause_image = load_image('image/ui/pause.png')
    pass


def exit():
    global pause_image
    del pause_image


def update():
    pass


def draw_world():
    play_state.draw_world()
    pause_image.draw(400, 400)


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def pause():
    pass


def resume():
    pass
