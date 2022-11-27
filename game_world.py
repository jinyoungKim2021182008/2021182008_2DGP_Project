import game_constant
import play_state

FLOOR_LAYER = 0
OBJECT_LAYER = 1
CHARACTER_EFFECT_LAYER = 2
ITEM_LAYER = 3
CHARACTER_LAYER = 4
BULLET_EFFECT_LAYER = 5
GRENADE_LAYER = 6
BULLET_LAYER = 7
UI_BUTTON = 8
UI_LAYER = 9


objects = [[], [], [], [], [], [], [], [], [], []]
collision_group = dict()


def add_object(object, depth):
    objects[depth].append(object)


def add_objects(object_list, depth):
    objects[depth] += object_list


def remove_object(object):
    for layer in objects:
        if object in layer:
            layer.remove(object)
            del object
            return
    raise ValueError('Trying destroy non existing object')


def all_objects():
    for layer in objects[1:]:
        for object in layer:
            yield object


def clear():
    for object in all_objects():
        del object
    for layer in objects:
        layer.clear()


def collide_objects():
    # 총알이 한번에 여러 물체에 충돌하는 경우 가장 가까운 경우만 처리
    for bullet in objects[BULLET_LAYER]:
        ps = []
        for character in objects[CHARACTER_LAYER]:
            p = game_constant.collide(bullet, character, 'BC')
            if p is not None:
                ps.append(p)

        for object in objects[OBJECT_LAYER]:
            p = game_constant.collide(bullet, object, 'BO')
            if p is not None:
                ps.append(p)

        min_len, min_p, min_obj = None, None, None
        if ps:
            for p in ps:
                print(p)
                len = game_constant.getLength(bullet.get_pos(), p[0])
                if min_len is None or len < min_len:
                    min_len = len
                    min_p = p[0]
                    min_obj = p[1]

        if min_p is not None:
            bullet.handle_collide(min_p)
            min_obj.handle_collide(bullet)

    # 수류탄과 구조물 처리
    for grenade in objects[GRENADE_LAYER]:
        for object in objects[OBJECT_LAYER]:
            p, rad = game_constant.collide(grenade, object, 'GO')
            if p is not False:
                grenade.handle_collide(p, rad)

    # 캐릭터와 구조물 처리
    for character in objects[CHARACTER_LAYER]:
        for object in objects[OBJECT_LAYER]:
            if game_constant.collide(character, object, 'CO'):
                play_state.player.handle_collide(object)

    # 아이템과 캐릭터 처리
    for item in objects[ITEM_LAYER]:
        if game_constant.collide(play_state.player, item, 'PI'):
            play_state.player.handle_collide(item)
            item.handle_collide(play_state.player)


def return_enemy_cnt():
    cnt = 0
    for character in objects[CHARACTER_LAYER]:
        if type(character).__name__ == 'Enemy':
            cnt += 1
    return cnt


def add_collision_pairs(a, b, group):

    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [ [], [] ] # list of list : list pair

    if a:
        if type(a) is list:
            collision_group[group][1] += a
        else:
            collision_group[group][1].append(a)

    if b:
        if type(b) is list:
            collision_group[group][0] += b
        else:
            collision_group[group][0].append(b)

    print(collision_group)


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def update():
    for game_object in all_objects():
        game_object.update()


# game_world.add_collision_pairs(server.boy, server.balls, 'BB')