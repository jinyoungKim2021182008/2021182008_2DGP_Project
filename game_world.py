import game_constant


FLOOR_LAYER = 0
OBJECT_LAYER = 1
CHARACTER_LAYER = 2
BULLET_EFFECT_LAYER = 3
BULLET_LAYER = 4


objects = [[], [], [], [], []]

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
    for bullet in objects[BULLET_LAYER]:
        for character in objects[CHARACTER_LAYER]:
            if game_constant.collide(bullet, character):
                pass

        for object in objects[OBJECT_LAYER]:
            if game_constant.collide(bullet, object):
                pass

    for character in objects[CHARACTER_LAYER]:
        for object in objects[OBJECT_LAYER]:
            if game_constant.collide(character, object):
                pass


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