import math

def get_nearby(x, y):

    return (
                    (x, y+1),
        (x-1, y),             (x+1, y),
                    (x, y-1),
    )

def get_value(x, y, shape):
    return shape[y][x]

def get_width(shape):
    return len(shape[0])

def get_height(shape):
    return len(shape)

def get_nodes(shape):
    polyomino = []
    for y in range(get_height(shape)):
        for x in range(get_width(shape)):
            if shape[y][x] == 1:
                polyomino.append((x, y))
    return polyomino

def get_circumference(shape):
    polyomino = get_nodes(shape)

    circumference = 0
    for x, y in polyomino:
        if (x+1, y) not in polyomino:
            circumference += 1
        if (x-1, y) not in polyomino:
            circumference += 1
        if (x, y+1) not in polyomino:
            circumference += 1
        if (x, y-1) not in polyomino:
            circumference += 1

    return circumference

def mean_distance(points):
    """
    Calculates the mean distance between a list of points in two-dimensional space.
    Args:
        points (list): A list of tuples representing (x, y) coordinates of points.
    Returns:
        float: The mean distance between the points.
    """
    n = len(points)
    total_distance = 0
    for i in range(n):
        for j in range(i+1, n):
            distance = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
            total_distance += distance
    mean_distance = total_distance / (n*(n-1)/2)
    return mean_distance

def shape_center(a):
    """
    Calculate the center (i.e., midpoint) of a shape represented as a set of coordinate pairs on a 2D grid.
    """

    epsilon = 1e-5

    shape = get_nodes(a)
    
    n = len(shape)
    sum_y = sum(y for _, y in shape)
    sum_x = sum(x for x, _ in shape)
    center_x = sum_x / n + epsilon
    center_y = sum_y / n + epsilon
    return (center_x, center_y)