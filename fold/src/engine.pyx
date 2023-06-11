# cython: language_level=3
# distutils: language=c

import random

ctypedef enum Direction:
    UP,DOWN,RIGHT,LEFT

cdef class Position:
    cdef public int x
    cdef public int y
    def __init__(self, int x, int y):
        self.x = x
        self.y = y

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
        print("Nod")
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

    def __init__(self, Position position, data=None):
        self.position = position
        self.neighbors = Neighbors()
        self.data = data

    def __repr__(self):
        return str(self.position )#f"{self.position}:{self.neighbors}:{self.data}"
    def __str__(self):
        return self.__class__.__name__ + ": " + self.__repr__()

    def get_position(self):
        return self.position

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
    def __init__(self, Position position = Position(0, 0)):
        self.node = create_node(0, 0)
        self.position = position

    def get_position(self):
        return self.position

    def traverse(self, Direction direction):
        print("Traversed")
        print(direction)
    
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


    
 
cdef class GGDBEngine(_Engine):
    """Grid graph database engine front-end"""

    def __init__(self):
        super().__init__()
        print(self.get_position())

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
        return self.node

    def put(self, key):
        pass

    def up(self):
        self.traverse(Direction.UP)
    
    def down(self):
        self.traverse(Direction.DOWN)

    def left(self):
        self.traverse(Direction.LEFT)

    def right(self):
        self.traverse(Direction.RIGHT)

    
