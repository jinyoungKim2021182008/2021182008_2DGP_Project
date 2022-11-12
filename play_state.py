from pico2d import *
import game_framework
import game_world
import stage
import ui

player = None
cursor = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            cursor.handle_event(event)
        else:
            player.handle_event(event)


def enter():
    global cursor
    cursor = ui.Cursor()
    stage.setStage(-1)


def exit():
    game_world.clear()


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    game_world.object_collider()

    delay(0.02)


def draw_world():
    stage.drawStage()
    for game_object in game_world.all_objects():
        game_object.draw()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass


def resume():
    pass
