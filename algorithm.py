#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: algorithm.py
# Description: Python implementation of the Polyomino contraction algorithm
# Author: irreq
# Date: 23/04/2023

import numpy as np
import math

"""Documentation

This program provides an algorithm for contracting polyominos with neighbor conservation.

The pseudo code works as following:

1. Identify contractable parts
2. Find allowed contractions and rotations
3. Find contraction with lowest resulting general distance
4. Contract and repeat the process

This is a naive implementation that will take first best contraction and contract. It does not
have the capacity to find moves that will generate more efficients folds in the future. Therefore,
try enabling and disabling `ALLOW_DIAGONAL_NEIGHBORS` to see if it contracts more efficient.
"""

TARGET = 1  # What to fold, as binary
ALLOW_DIAGONAL_NEIGHBORS = True


def get_nearby(x: int, y: int, allow_diagonal=ALLOW_DIAGONAL_NEIGHBORS) -> tuple[tuple]:
   """
   Return a tuple of four tuples, where each inner tuple contains two integer values
   representing the coordinates of a nearby point relative to the input point (x, y).

   Parameters:
   x (int): The x-coordinate of the input point.
   y (int): The y-coordinate of the input point.

   Returns:
   tuple of tuples: A tuple containing four tuples, where each inner tuple contains two
   integer values representing the coordinates of a nearby point relative to the input point.
   The nearby points are defined as:
   - (x, y+1) which is one unit above the input point
   - (x-1, y) which is one unit to the left of the input point
   - (x+1, y) which is one unit to the right of the input point
   - (x, y-1) which is one unit below the input point

   Example:
   >>> get_nearby(0, 0)
   ((0, 1), (-1, 0), (1, 0), (0, -1))
   """
   

   if allow_diagonal:

      return (
         (x-1, y+1), (x, y+1), (x+1, y+1),
         (x-1, y),              (x+1, y),
         (x-1, y-1), (x, y-1), (x+1, y-1)
      )
   
   else:
      return (
                     (x, y+1),
         (x-1, y),             (x+1, y),
                     (x, y-1),
      )




def rotate_points(points: list[tuple], origin: tuple, angle: float) -> list[tuple]:
   """
   Rotate a list of points around a given origin point by a specified angle in degrees.

   Parameters:
   points (list of tuples): A list of tuples, where each tuple represents a point to be rotated.
   origin (tuple): A tuple representing the origin point around which the points should be rotated.
   angle (float): The angle (in degrees) by which the points should be rotated.

   Returns:
   list of tuples: A list of tuples representing the rotated points.

   Example:
   >>> rotate_points([(1, 1), (2, 2), (3, 3)], (0, 0), 45)
   [(1, 1), (0, 2), (-1, 3)]
   """

   radians = math.radians(angle)
   cos_val = math.cos(radians)
   sin_val = math.sin(radians)

   # translate points so that a is at the origin
   translated_points = [(p[0]-origin[0], p[1]-origin[1]) for p in points]

   # rotate points
   rotated_points = [(p[0]*cos_val - p[1]*sin_val, p[0]*sin_val + p[1]*cos_val) for p in translated_points]

   # translate points back to their original position
   final_points = [(int(round(p[0]+origin[0],1)), int(round(p[1]+origin[1], 1))) for p in rotated_points]

   return final_points


def mean_distance(points: list[tuple]) -> float:
   """
   Calculate the mean distance between all pairs of points in a given list.

   Parameters:
   points (list of tuples): A list of tuples representing the points for which the mean distance should be calculated.

   Returns:
   float: The mean distance between all pairs of points in the given list.

   Example:
   >>> mean_distance([(1, 1), (2, 2), (3, 3)])
   1.6329931620475584
   """

   n = len(points)
   total_distance = 0
   for i in range(n):
      for j in range(i+1, n):
         distance = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
         total_distance += distance
   mean_distance = total_distance / (n*(n-1)/2)
   return mean_distance


def find_movements(points: list[tuple]) -> list[tuple]:

   free = []

   def is_shape(enumerations) -> bool:
      """
      Determines if a given polyomino shape (represented as a set of positions) matches any of the given enumerations.

      Parameters:
      enumerations (list of sets): A list of sets, each representing a possible polyomino shape as a set of positions.

      Returns:
      bool: True if the given shape matches any of the enumerations, False otherwise.
      """

      is_found = False
      for enum in enumerations:
         tmp = True
         for pos in enum:
               if pos not in points:
                  tmp = False
                  break
         if tmp == True:
               is_found = True
               break

      return is_found
    
   for (x, y) in points:

      # Filter immovable parts
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


   return free


def type_finder(points: list[tuple]):
   free = find_movements(points)

   movable = []
   for point in free:
      x, y = point
      connections = 0
      for nearby_pos in get_nearby(x, y):
         if nearby_pos in points:
               connections += 1

      if connections > 1:
         movable.append(point)

   return movable


def get_width(shape):
    return len(shape[0])

def get_height(shape):
    return len(shape)

def get_positions(shape):
   for y in range(get_height(shape)):
      for x in range(get_width(shape)):
         yield (x, y)

def get_value_at(x: int, y: int, shape):
   return shape[y][x]
   
def invert_map(dictionary):
    return {value:key for key, value in dictionary.items()}

def create_shape_map(shape):
   shape_map = {}

   index = 1
   for (x, y) in get_positions(shape):
      if get_value_at(x, y, shape) == TARGET:
         shape_map[(x, y)] = index
         index += 1

   return shape_map

def calculate_score(structure):
    return mean_distance(list(structure.values()))

def convert_position_to_id(position, structure):
   for index, pos in structure.items():
      if pos == position:
         return index

def movement_finder(moveable, structure):
   to_contract = {}
   for index in moveable:
      x, y = structure[index]

      joints = {}

      for possible in get_nearby(x, y):
         if possible in structure.values():
            xp, yp = possible
            transforms = []
            for neighbor in get_nearby(xp, yp):
               if not neighbor in structure.values():
                  transforms.append(neighbor)

            if transforms != []:
               joints[convert_position_to_id(possible, structure)] = transforms
      
      if joints != {}:
         to_contract[index] = joints

   return to_contract


def find_moving_tiles(index, joint_index, original_relation):

   contracting = [index]
   visited = [index, joint_index]
   current_indexes = [index]

   while current_indexes != []:
      i = current_indexes.pop()
      for neighbor_index in original_relation[i]:
         if neighbor_index not in visited:
            current_indexes.append(neighbor_index)
            contracting.append(neighbor_index)
            visited.append(neighbor_index)

   return contracting

def get_neighbors_new(index, new_shape):
   x, y = new_shape[index]
   d = [possible for possible in get_nearby(x, y) if possible in new_shape.values()]
   return [index for index, pos in new_shape.items() if pos in d]


def is_allowed_update(new_shape, original_relation):
   for index, neighbors in original_relation.items():
      if index not in new_shape:
         return False
      
      x, y = new_shape[index]
      d = [possible for possible in get_nearby(x, y) if possible in new_shape.values()]
      new_neighbors = [index for index, pos in new_shape.items() if pos in d]
      for neighbor in neighbors:
         if neighbor not in new_neighbors:
            return False
            
   return True

def possible_solutions(index, joint_index, new_pos, structure, original_relation):
   contracting = find_moving_tiles(index, joint_index, original_relation)

   to_move = {}

   point = structure[index]

   dx, dy = new_pos[0] - point[0], new_pos[1] - point[1]

   to_rotate_current = []
   to_rotate_new = []

   for i in contracting:
      x, y = structure[i]

      to_rotate_current.append((x, y))
      to_rotate_new.append((x+dx, y+dy))


   def can_rotate(rotated, to_rotate):

      can_rotate = True
      for rotated_point in rotated:
         x, y = rotated_point
         if rotated_point in structure.values():
            if (x, y) not in to_rotate:
               can_rotate = False
               break

      return can_rotate
   
   def perform_rotation(to_move, rotated):
      new_grid = structure.copy()
      new_grid = invert_map(new_grid)
      for ide, current, rotatedt in zip(contracting, to_rotate_current, rotated):
            new_grid[current] = 0
            new_grid[rotatedt] = ide

      new_grid = {v: k for k, v in new_grid.items() if v != 0}

      return new_grid
   
   possible_grids = []

   for angle in (0, 90, 180, 270):
      # Order is a must
      rotated_current = rotate_points(to_rotate_current, point, angle)

      # Check rotation on current position
      if can_rotate(rotated_current, to_rotate_current):
         new_grid = perform_rotation(to_move, rotated_current)
         if is_allowed_update(new_grid, original_relation):
            possible_grids.append(new_grid)


      rotated_new = rotate_points(to_rotate_new, new_pos, angle)

      # Check rotation on proposed position
      if can_rotate(rotated_new, to_rotate_current):
         new_grid = perform_rotation(to_move, rotated_new)
         if is_allowed_update(new_grid, original_relation):
            possible_grids.append(new_grid)
   
   return possible_grids


def convert_poly_to_shape(structure):
   positions = list(structure.values())
   min_x, max_x = positions[0][0], positions[0][0]
   min_y, max_y = positions[0][1], positions[0][1]

   # Calculate width and height for array
   for x, y in positions:
      if x < min_x:
         min_x = x
      if x > max_x:
         max_x = x
      if y < min_y:
         min_y = y
      if y > max_y:
         max_y = y

   max_x -= min_x
   max_y -= min_y

   shape = np.zeros((max_y+1, max_x+1))

   for index, (x, y) in structure.items():
      shape[y-min_y][x-min_x] = index

   return shape


def solver(shape: list[list[int]]) -> list[list[int]]:
   
   shape_map = create_shape_map(shape)

   structure = invert_map(shape_map)

   def get_neighbors(index):
       
       x, y = structure[index]

       neighbors = []

       for position in get_nearby(x, y):
           if position in shape_map:
               neighbors.append(shape_map[position])
       
       return neighbors
   
   # How the polyomino is attached
   original_relation = {index:get_neighbors(index) for index in structure}

   points = list(structure.values())

   # Find which parts can be modified
   moveable = [shape_map[move] for move in type_finder(points)]

   original_mapping = convert_poly_to_shape(structure.copy())

   score = calculate_score(structure) + 10

   times = 0
   while True:
      to_contract = movement_finder(moveable, structure)

      solutions = {}
      
      global_solution = []

      for movable in to_contract:
         joints = to_contract[movable]
         for joint in joints:
            for new_pos in joints[joint]:
               solutions = possible_solutions(movable, joint, new_pos, structure, original_relation)

               result = {mean_distance(list(solution.values())):solution for solution in solutions}

               current_score = sorted(result.keys())[0]
               best = result[current_score]
               if current_score < score:
                  global_solution = best
                  score = current_score

      # Converged
      if global_solution == []:
         break
      else:
         structure = global_solution

      times += 1

   result_mapping = convert_poly_to_shape(structure)

   print(f"Converged after {times} contractions")

   return result_mapping, original_mapping
       


if __name__ == "__main__":
   
   grid = np.array([
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
      [1],
   ])

   # grid = np.array([
   #    [1,0,1,1],
   #    [1,0,1,0],
   #    [1,1,1,0],
   #    [1,0,1,0],
   #    [1,0,1,0],
   #    [1,0,1,0],
   #    [1,0,1,0],
   # ])

   # grid = np.array([
   #    [1,0,1,1,0,1,1,1,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,1,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,1,1,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   #    [1,0,1,0,0,1,1,0,0,1],
   # ])

   grid = np.array([
      [1,0,0,0,0,0],
      [1,0,0,0,1,1],
      [1,0,0,0,1,1],
      [1,0,0,0,0,0],
      [1,0,0,0,0,0],
      [1,0,0,0,0,0],
      [1,1,1,1,1,1],
   ])

   solution, original = solver(grid)
   print("\nOriginal:")
   print(original)

   print("\nSolution:")
   print(solution)

   def get_width(shape: list[int]) -> int:
      return len(shape[0])

   def get_height(shape: list[int]) -> int:
      return len(shape)

   def get_points(shape: list[int]) -> list[tuple]:
      points = []
      for x, y in get_positions(shape):
         if shape[y][x] != 0:
            points.append((x, y))
      return points

   original_value = mean_distance(get_points(original))
   new_value = mean_distance(get_points(solution))
   percentage_smaller = ((original_value - new_value) / original_value) * 100

   print(f"\nThe new layout is {round(percentage_smaller, 2)}% contracted")