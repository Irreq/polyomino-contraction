# cython: language_level=3
# distutils: language=c

import random

# from libcpp cimport bool

from libc cimport bool as bool_t

ctypedef enum Direction:
    UP,DOWN,RIGHT,LEFT

# cpdef enum Direction:
#     UP,DOWN,RIGHT,LEFT  

class InvalidPositionException(Exception):
    pass

cdef class Position:
    cdef public int x
    cdef public int y
    def __init__(self, int x, int y):
        self.x = x
        self.y = y

        assert isinstance(self.x, int) and isinstance(self.y, int), InvalidPositionException("Wrong position")

    def compute_direction(self, Direction direction):
        if direction == Direction.UP:
            return Position(self.x, self.y+1)
        elif direction == Direction.DOWN:
            return Position(self.x, self.y-1)
        elif direction == Direction.LEFT:
            return Position(self.x-1, self.y)
        elif direction == Direction.RIGHT:
            return Position(self.x+1, self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
    def __str__(self):
        return self.__class__.__name__ + ": " + self.__repr__()





cdef class Neighbors:
    """Bi-Directional data-structure for storing nodes and their respective positions"""
    cdef dict neighbors
    cdef dict neighbors_inverted
    def __init__(self):
        self.neighbors = {}
        self.neighbors_inverted = {}
    
    def is_neighbor(self, Node node):
        """Find out if a neighbor is here"""
        return node in self.neighbors_inverted.keys()
    
    def is_neighbor_position(self, Position position):
        """Find out if a neighbor is here"""
        return position in self.neighbors.keys()

    def add(self, Node node):
        """
        Add a node from the neighbors
        """
        self.neighbors_inverted[node] = node.get_position()
        self.neighbors[node.get_position()] = node
    
    def remove(self, Node node):
        """
        Remove a node from the neighbors
        """
        position = self.neighbors_inverted.pop(node)
        self.neighbors.pop(position)

    def get_neighbors(self):
        """
        Retrieve a list of all available neighbors
        """
        return self.neighbors.values()

    def get_neighbors_positions(self):
        return self.neighbors.keys()

    def update(self):
        """Updates the map structure"""
        old_neighbors = self.neighbors_inverted.keys()
        self.neighbors.clear()
        self.neighbors_inverted.clear()

        for node in old_neighbors:
            self.add(node)


    def __repr__(self):
        # return "["+",".join(self.neighbors.keys())+"]"
        result = "["
        for position in self.neighbors.keys():
            result += position.__repr__() + ",\n"
        result += "]"
        return result

    def __str__(self):
        return self.__class__.__name__ + ": " + self.__repr__()

cdef class Node:

    cdef Position position
    cdef Neighbors neighbors
    cdef object data

    cdef int priority

    def __init__(self, Position position, data=None):
        self.position = position
        self.neighbors = Neighbors()
        self.data = data

        self.priority = 0

    def __repr__(self):
        return str(self.position )#f"{self.position}:{self.neighbors}:{self.data}"
    def __str__(self):
        return self.__class__.__name__ + ": " + self.__repr__()

    def get_position(self):
        return self.position

    def get_data(self):
        return self.data

    def set_data(self, key):
        self.data = key

    def connect(self, Node node):
        if not self.neighbors.is_neighbor(node):
            self.neighbors.add(node)

    def disconnect(self, Node node):
        if self.neighbors.is_neighbor(node):
            self.neighbors.remove(node)

    def can_connect(self, Node node):
        """Determines if a node is immediately nearby to be called neighbor"""
        other_position = node.get_position()

        diff_x = other_position.x - self.position.x
        diff_y = other_position.y - self.position.y

        return \
        (-1 <= diff_x <= 1) and \
        (-1 <= diff_y <= 1) and \
        not (diff_y == 0 and diff_x == 0)

    def can_traverse(self, Direction direction):
        """Determines if a node is present in the direction"""
        new_position = self.position.compute_direction(direction)

        return self.neighbors.is_neighbor_position(new_position)

    def get_nearby(self):
        return self.neighbors.get_neighbors()

    def get_valid_directions(self):
        return self.neighbors.get_neighbors_positions()




cdef find_nearby(node):
    cdef set visited = set()
    cdef set nodes_to_check = set()
    cdef set allowed = set([node])
    cdef set layer = set([node])

    def find_new_layer():
        nonlocal nodes_to_check, layer

        nodes_to_check.clear()
        layer.clear()

        for current_node in allowed:
            if current_node not in visited: # and node.is_nearby(current_node):
                nodes_to_check.update(current_node.get_nearby())
                visited.add(current_node)
                layer.add(current_node)

        allowed.clear()
        allowed.update(nodes_to_check)

    def generate_layers():
        nonlocal layer, allowed

        find_new_layer()
        while allowed:
            yield layer
            find_new_layer()

    return generate_layers()

cdef dict _create_map(Node node, int n_layers):
    cdef int i = 0

    cdef set visited = set()

    cdef dict grid = {}

    for layer in find_nearby(node):
        if i > n_layers:
            break
        for node in layer:
            position = node.get_position()
            if position not in visited:
                grid[position] = node.get_data()
                visited.add(position)
        i += 1

    return grid


def connect_nodes(Node node1, Node node2):
    node1.connect(node2)
    node2.connect(node1)

    node2.neighbors.is_neighbor(node1)
    node2.neighbors.is_neighbor_position(node1.get_position())
    
def create_node(int x, int y):
    return Node(Position(x, y))

cdef class _Engine:

    cdef Position position
    cdef Node node

    cdef list possible_positions # = []
    cdef list possible_directions# = []

    cdef object can_modify

    cdef int render_distance

    def __init__(self, render_distance, Position position = Position(0, 0), can_modify = True):
        
        self.render_distance = render_distance
        
        self.node = create_node(0, 0)
        self.position = position
        self.can_modify = can_modify

        self.possible_directions = []
        self.possible_positions = []

    def get_position(self):
        return self.position

    def traverse(self, Direction direction):

        new_pos = self.node.get_position().compute_direction(direction)

        if self.node.can_traverse(direction):
            self.node = self.node.get_nearby
        print("Traversed")
        print(direction)

    def find_valid_directions(self):
        return self.node.get_valid_directions()
        

    def _find(self, Node target):
        for layer in find_nearby(self.node):
            for node in layer:
                if node == target:
                    return True
        return False

    def _find_from_position(self, Position target_position):
        """Tries to find data by traveling there"""
        for layer in find_nearby(self.node):
            for node in layer:
                if node.get_position() == target_position:
                    return node
        return None




def create_map(node, n):
    return _create_map(node, n)

def load_map_from_array(list arr, object ignore=None, inverted_y=True):
    """Convert a 2D map to a network
    You may use inverted_y to mimic the way a 2D array is structured compared to 
    the normal coordinate system
    """
    network = []

    max_x = len(arr)
    max_y = len(arr[0])

    for x in range(max_x):
        for y in range(max_y):
            if inverted_y:
                item = arr[x][(max_y - 1) - y]
            else:
                item = arr[x][y]

            if item != ignore:
                node = Node(Position(x, y), item)
                network.append(node)

    return network



 
cdef class GGDBEngine(_Engine):
    """Grid graph database engine front-end"""

    def __init__(self, int render_distance):
        super().__init__(render_distance)

    def test(self, Node node):
        self.node = node

    def add_close_to(self, key, close=[]):
        pass

    def isEmpty(self):
        pass

    def find(self, key):
        i = 0
        for layer in find_nearby(self.node):
            if i > 1:
                break
            print("Layer\n")
            for node in layer:
                print("Found ", node)
            i+=1

    def get(self):
        return self.node.get_data()

    def put(self, key):
        self.node.set_data(key)

    def up(self):
        self.traverse(Direction.UP)
    
    def down(self):
        self.traverse(Direction.DOWN)

    def left(self):
        self.traverse(Direction.LEFT)

    def right(self):
        self.traverse(Direction.RIGHT)

    def get_possible(self) -> list[Position]:
        return list(self.find_valid_directions())

    def set_render_distance(self, int value):
        assert isinstance(value, int), "Value must be of integer type"
        assert 0 <= value, "Value must be a positive integer"
        self.render_distance = value

    def get_render_distance(self):
        return int(self.render_distance)

    
