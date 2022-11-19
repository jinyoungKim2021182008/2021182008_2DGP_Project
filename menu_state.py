from pico2d import *
import game_framework
import game_world
import ui
import game_constant
import play_state


menu_image = None
cursor = None
stage_buttons = []
play_button = None
stage_num = 1

main_weapons = []
main_weapon_num = 0
sub_weapons = []
sub_weapon_num = 0
grenades = []
grenade_num = 0
weapon_buttons = []


def collider():
    global stage_num, main_weapon_num, sub_weapon_num, grenade_num
    for button in stage_buttons:
        if game_constant.Point2Rect(cursor.getPoint(), button.getRect()):
            for b in stage_buttons:
                b.state = 0
            if button.name == 't':
                stage_num = 0
            if button.name == '1':
                stage_num = 1
            if button.name == '2':
                stage_num = 2
            stage_buttons[stage_num].state = 1

    if game_constant.Point2Rect(cursor.getPoint(), play_button.getRect()):
        game_framework.change_state(play_state)

    for button in weapon_buttons:
        if game_constant.Point2Rect(cursor.getPoint(), button.getRect()):
            if button.state == 1:
                if button.name == 'main_l':
                    main_weapon_num -= 1
                if button.name == 'main_r':
                    main_weapon_num += 1
                if button.name == 'sub_l':
                    sub_weapon_num -= 1
                if button.name == 'sub_r':
                    sub_weapon_num += 1
                if button.name == 'grenade_l':
                    grenade_num -= 1
                if button.name == 'grenade_r':
                    grenade_num += 1


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            cursor.handle_event(event)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            collider()


def enter():
    global menu_image, cursor, stage_buttons, play_button
    if menu_image is None:
        menu_image = load_image('image/ui/menu.png')
    if len(stage_buttons) == 0:
        stage_buttons.append(ui.Button(load_image('image/ui/button/t.png'), load_image('image/ui/button/t_select.png'), 150, 520, 100, 100, 't'))
        stage_buttons.append(ui.Button(load_image('image/ui/button/1.png'), load_image('image/ui/button/1_select.png'), 400, 600, 100, 100, '1'))
        stage_buttons.append(ui.Button(load_image('image/ui/button/2.png'), load_image('image/ui/button/2_select.png'), 650, 550, 100, 100, '2'))
        stage_buttons[1].state = 1

    for button in stage_buttons:
        game_world.add_object(button, game_world.UI_LAYER)

    if play_button is None:
        play_button = ui.Button(load_image('image/ui/button/play.png'), load_image('image/ui/button/play.png'), 650, 100, 150, 75, 'play')
    game_world.add_object(play_button, game_world.UI_LAYER)

    if len(main_weapons) == 0:
        main_weapons.append(load_image('image/weapon/rifle_1.png'))
        main_weapons.append(load_image('image/weapon/rifle_2.png'))
    if len(sub_weapons) == 0:
        sub_weapons.append(load_image('image/weapon/handgun.png'))
    if len(grenades) == 0:
        grenades.append(load_image('image/weapon/grenade_1.png'))
        grenades.append(load_image('image/weapon/grenade_2.png'))

    if len(weapon_buttons) == 0:
        weapon_buttons.append(ui.Button(load_image('image/ui/button/l_button_off.png'), load_image('image/ui/button/l_button_on.png'), 220, 210, 30, 30, 'main_l'))
        weapon_buttons.append(ui.Button(load_image('image/ui/button/r_button_off.png'), load_image('image/ui/button/r_button_on.png'), 345, 210, 30, 30, 'main_r'))
        weapon_buttons.append(ui.Button(load_image('image/ui/button/l_button_off.png'), load_image('image/ui/button/l_button_on.png'), 80, 80, 30, 30, 'sub_l'))
        weapon_buttons.append(ui.Button(load_image('image/ui/button/r_button_off.png'), load_image('image/ui/button/r_button_on.png'), 180, 80, 30, 30, 'sub_r'))
        weapon_buttons.append(ui.Button(load_image('image/ui/button/l_button_off.png'), load_image('image/ui/button/l_button_on.png'), 250, 80, 30, 30, 'grenade_l'))
        weapon_buttons.append(ui.Button(load_image('image/ui/button/r_button_off.png'), load_image('image/ui/button/r_button_on.png'), 350, 80, 30, 30, 'grenade_r'))
        for b in weapon_buttons:
            b.state = 1

    for button in weapon_buttons:
        game_world.add_object(button, game_world.UI_LAYER)

    if cursor is None:
        cursor = ui.Cursor()
    game_world.add_object(cursor, game_world.UI_LAYER)


def exit():
    game_world.clear()


def update():
    for game_object in game_world.all_objects():
        game_object.draw()
    game_world.object_collider()
    for b in weapon_buttons:
        b.state = 1
    if main_weapon_num == 0:
        weapon_buttons[0].state = 0
    if main_weapon_num == len(main_weapons) - 1:
        weapon_buttons[1].state = 0
    if sub_weapon_num == 0:
        weapon_buttons[2].state = 0
    if sub_weapon_num == len(sub_weapons) - 1:
        weapon_buttons[3].state = 0
    if grenade_num == 0:
        weapon_buttons[4].state = 0
    if grenade_num == len(grenades) - 1:
        weapon_buttons[5].state = 0
    delay(0.02)


def draw_world():
    menu_image.draw(400, 400, 800, 800)
    main_weapons[main_weapon_num].draw(285,250,150,100)
    sub_weapons[sub_weapon_num].draw(130, 110, 100, 100)
    grenades[grenade_num].draw(300, 110, 100, 100)
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
