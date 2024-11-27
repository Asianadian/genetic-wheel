import numpy as np

def init_representation():
    rand = np.random.randint(0, 2, (100, 100))
    print(rand)
    # rand = 
    return rand


def get_coordinates(representation):
    return [(int(x), int(y)) for x, y in zip(np.where(representation == 1)[0], np.where(representation == 1)[1])]

if __name__ == '__main__':
    rep = init_representation()
    print(rep)
    print(get_coordinates(rep))


