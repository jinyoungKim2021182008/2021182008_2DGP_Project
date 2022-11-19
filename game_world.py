import game_constant
import play_state

FLOOR_LAYER = 0
OBJECT_LAYER = 1
CHARACTER_EFFECT_LAYER = 2
ITEM_LAYER = 3
CHARACTER_LAYER = 4
BULLET_EFFECT_LAYER = 5
BULLET_LAYER = 6
UI_BUTTON = 7
UI_LAYER = 8


objects = [[], [], [], [], [], [], [], [], []]

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


def object_collider():
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

        min_len, min_obj, min_p = None, None, None
        if ps:
            for p, object2 in ps:
                len = game_constant.getLength(bullet.getPos(), p)
                if min_len is None or len < min_len:
                    min_len = len
                    min_obj = object2
                    min_p = p

            if min_obj is not None:
                bullet.collide_handle(min_obj, min_p)
                min_obj.collide_handle(bullet)

    # 캐릭터와 구조물 처리
    for character in objects[CHARACTER_LAYER]:
        for object in objects[OBJECT_LAYER]:
            if game_constant.collide(character, object, 'CO'):
                play_state.player.collide_handle(object)

    # 아이템과 캐릭터 처리
    for item in objects[ITEM_LAYER]:
        if game_constant.collide(play_state.player, item, 'PI'):
            play_state.player.collide_handle(item)
            item.collide_handle(play_state.player)


def returnEnemyCnt():
    cnt = 0
    for character in objects[CHARACTER_LAYER]:
        if type(character).__name__ == 'Enemy':
            cnt += 1

    return cnt


"""
def add_collision_pairs(object1, object2, group):
    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [[], []]   # list of list : list pair

    if object1:
        if type(object2) is list: collision_group[group][1] += object2
        else: collision_group[group][1].append(object2)

    if object2:
        if type(object1) is list: collision_group[group][0] += object1
        else: collision_group[group][0].append(object1)


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(object):
    for pairs in collision_group.values():
        if object in pairs[0]:
            pairs[0].remove(object)
        if object in pairs[1]:
            pairs[1].remove(object)
"""