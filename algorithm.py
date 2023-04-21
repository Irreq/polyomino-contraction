import numpy as np
from shape import *

def naive_finder(polymino):
    free = []

    def is_shape(enumerations):
        """
        Determines if a given polyomino shape (represented as a set of positions) matches any of the given enumerations.
        Args:
            enumerations (list of sets): A list of sets, each representing a possible polyomino shape as a set of positions.
        Returns:
            bool: True if the given shape matches any of the enumerations, False otherwise.
        """
        is_found = False
        for enum in enumerations:
            tmp = True
            for pos in enum:
                if pos not in polymino:
                    tmp = False
                    break
            if tmp == True:
                is_found = True
                break

        return is_found

    for (x, y) in polymino:
        if is_shape(
            (
            # ((x-1,y), (x+1,y)),

            # ((x, y+1),
            #  (x, y-1)),

            
            ((x-1, y),
            (x-1,y-1), (x,y-1)),

            (
            (x-1,y-1), (x, y-1), (x+1,y-1)),

            (         (x+1,y),
            (x, y-1), (x+1,y-1)
            ),

            (
            (x+1,y+1),
            (x+1,y),
            (x+1,y-1)
            ),

            (
            (x,y+1), (x+1,y+1),
                     (x+1,y)
            ),
            (
            (x-1,y+1), (x, y+1), (x+1,y+1)
            ),

            (
            (x-1,y+1), (x, y+1),
            (x-1,y)
            ),

            (
            (x-1,y+1),
            (x-1,y),
            (x-1,y-1)
            )
             )
        ):
            continue

        free.append((x,y))

    # Determines if a point is endpoint or not
    endpoints = []
    movable = []
    for point in free:
        x, y = point
        connections = 0
        if (x+1, y) in polymino:
            connections += 1
        if (x-1, y) in polymino:
            connections += 1
        if (x, y+1) in polymino:
            connections += 1
        if (x, y-1) in polymino:
            connections += 1

        if connections <= 1:
            endpoints.append(point)
        else:
            movable.append(point)

    return movable, endpoints

def get_neighbors(point, points):
    x, y = point
    return [possible for possible in get_nearby(x, y) if possible in points]

def neighbor_identifier(shape):
    back = np.zeros_like(shape)

    points = get_nodes(shape)

    index = 1

    for (x, y) in points:
        back[y][x] = index
        index += 1

    
    neighbor_info = {}

    for (x, y) in points:
        neighbor_info[back[y][x]] = []
        for neighbor in get_neighbors((x, y), points):
            nx, ny = neighbor
            neighbor_info[back[y][x]].append(back[ny][nx])

    return back, neighbor_info



def finder(shape):
    a_p = get_nodes(shape)
    avg = mean_distance(a_p)
    center = shape_center(shape)


    movable, endpoints = naive_finder(a_p)

    for point in movable:
        possible_transforms = []
        x, y = point
        for possible in get_nearby(x, y):
            if possible in a_p:
                possible_transforms.append(possible)

        target = {math.dist(possible, center):possible for possible in possible_transforms}

        tile = target[sorted(target.keys())[0]]
        print(tile)

        x, y = tile

        transforms = []
        for neighbor in get_nearby(x, y):
            if neighbor not in a_p:
                transforms.append(neighbor)


        target = {math.dist(possible, center):possible for possible in transforms}

        tile = target[sorted(target.keys())[0]]

        print(tile)
        print(transforms)

        print(point)
        print(center)




grid = np.array([[0., 0., 0., 0., 0.],
       [0., 0., 0., 1., 0.],
       [0., 0., 0., 1., 1.],
       [0., 0., 1., 1., 0.],
       [0., 1., 1., 1., 0.]])

outside = np.zeros((grid.shape[0]+2, grid.shape[1]+2))
outside[1:-1, 1: -1] = grid
shape = outside


finder(shape)