# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:40:21 2019

@author: Owen-Laptop
"""

from pyquaternion import Quaternion
import numpy

class Block:
    def __init__(self, coords, stop_face_v=None, slide_face_v=None):
        self.coords = coords
        if stop_face_v is None and slide_face_v is None:
            self.generate_random_orientation()
        else:
            self.stop_face_v = stop_face_v
            self.slide_face_v = slide_face_v
        
    def __repr__(self):
        return f'Block at {self.coords}, with the "{self.get_top_face_from_orientation()}" face up.'
    
    def __str__(self):
        return self.__repr__()
    
    def translate(self, direction):
        self.coords = self.coords + direction
        
    def tip(self, direction):
        if direction.lower() == 'right':
            axis = [0, 1, 0]
            translation = Coord(1, 0)
        elif direction.lower() == 'down': 
            axis = [1, 0, 0]
            translation = Coord(0, -1)
        elif direction.lower() == 'left':
            axis = [0, -1, 0]
            translation = Coord(-1, 0)
        elif direction.lower() == 'up':
            axis = [-1, 0, 0]
            translation = Coord(0, 1)
        else:
            raise ValueError('unknown tip direction: ' + str(direction))
        self.translate(translation)
        q = Quaternion(axis=axis, degrees=90)
        self.stop_face_v = q.rotate(self.stop_face_v)
        self.slide_face_v = q.rotate(self.slide_face_v)
        
    def get_top_face_from_orientation(self):
        if self.stop_face_v[2] > 0:
            top_face = 'stop'
        elif self.stop_face_v[2] < 0:
            top_face = 'star'
        elif self.slide_face_v[2] > 0:
            top_face = 'slide'
        elif self.slide_face_v[2] < 0:
            top_face = 'hoops'
        elif numpy.cross(self.stop_face_v, self.slide_face_v)[2] > 0:
            top_face = 'diag'
        elif numpy.cross(self.stop_face_v, self.slide_face_v)[2] < 0:
            top_face = 'adj'
        else:
            raise ValueError('Something went wrong with the orientation vectors')
        return top_face
    
    def generate_random_orientation(self):
        stop_face_axis = numpy.random.randint(0, 3)
        stop_face_magnitude = numpy.random.randint(0, 2)*2 - 1
        stop_face_v = [0, 0, 0]
        stop_face_v[stop_face_axis] = stop_face_magnitude
        possible_slide_face_directions = [
                [0, 1],
                [0, -1],
                [1, 0],
                [-1, 0]]
        slide_face_v = possible_slide_face_directions[numpy.random.randint(len(possible_slide_face_directions))]
        slide_face_v.insert(0, stop_face_axis)
        
        self.stop_face_v = stop_face_v
        self.slide_face_v = slide_face_v
        
    def move_using_top_face(self):
        pass

class Coord:
    def __init__(self, x, y):
        if (type(x) is not int) or (type(y) is not int):
            raise ValueError('Coordinates must be integers')
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)
        

GRID_X = 7
GRID_Y = 7

star1 = Coord(4, 2)
star2 = Coord(4, 7)

pawn1 = Block(Coord(1, 1))
