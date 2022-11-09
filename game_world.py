
FLOOR_LAYER = 0
OBJECT_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3

objects = [[], [], [], []]

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