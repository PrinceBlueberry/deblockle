# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:40:21 2019

@author: Owen-Laptop
"""

from pyquaternion import Quaternion
import numpy

        
def eq_with_tol(a, b, tol):
    return abs(a-b) < tol

class Block:
    '''
    Assume the user is looking down at the board, then X is positive to the
    right, Y is positive up, and Z is positive toward the user.  
    
    The location of all the block's faces can be tracked by tracking the 
    orientation of two of the block's faces.  I chose to track the stop face 
    and the slide face.  The location of all the other faces can be derived 
    using those two vectors and knowing the design of the block.  Here's an 
    example of what the block looks like with the star face up
    +-------+
    |   +   |
    | o * \ |
    |   x   |
    +-------+
    Where the faces are represented as symbols as follow:
    stop:  s
    star:  *
    slide: \
    hoops: o
    diag:  x
    adj:   +
    '''
            
    opposites = {
        'stop':'star',
        'star':'stop',
        'slide':'hoops',
        'hoops':'slide',
        'diag':'adj',
        'adj':'diag'
    }
    
    def __init__(self, coords, stop_face_v=None, slide_face_v=None):
        self.coords = coords
        if stop_face_v is None and slide_face_v is None:
            stop_face_v, slide_face_v = self.generate_random_orientation()
        else:
            self.stop_face_v = stop_face_v
            self.slide_face_v = slide_face_v
        # Define a 3D vector for every face of the block
        self.face_v = {}
        self.face_v['stop'] = stop_face_v
        self.face_v['slide'] = slide_face_v
        self.face_v['diag'] = numpy.cross(self.face_v['stop'], self.face_v['slide'])
        self.face_v['hoops'] = [-ii for ii in self.face_v['slide']]
        self.face_v['star'] = [-ii for ii in self.face_v['stop']]
        self.face_v['adj'] = [-ii for ii in self.face_v['diag']]
        
    def __repr__(self):
        return f'Block at {self.coords}, with the {self.get_face_at_location("top")} face up.'
    
    def __str__(self):
        return self.__repr__()
    
    def print_orientation(self):
        up = self.get_face_at_location('up')
        left = self.get_face_at_location('left')
        top = self.get_face_at_location('top')
        right = self.get_face_at_location('right')
        down = self.get_face_at_location('down')
        text =  f'+-------+\n'
        text += f'|   {up}   |\n'
        text += f'| {left} {top} {right} |\n'
        text += f'|   {down}   |\n'
        text += f'+-------+\n'
        print(text)
    
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
        for face in self.face_v:
            self.face_v[face] = q.rotate(self.face_v[face])
        
    def get_face_at_location(self, location):
        if location == 'top':
            axis_to_check = 1
            direction = 1
        elif location == 'left':
            axis_to_check = 0
            direction = -1
        elif location == 'up':
            axis_to_check = 2
            direction = 1
        elif location == 'right':
            axis_to_check = 0
            direction = 1
        elif location == 'down':
            axis_to_check = 1
            direction = -1
        for face in self.face_v:
            if eq_with_tol(self.face_v[face][axis_to_check], direction, 0.0001):
                return face
        raise ValueError(f'Could not find any faces at location: "{location}" \nface_v:{self.face_v}')
        
    
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
        slide_face_v.insert(stop_face_axis, 0)
        return stop_face_v, slide_face_v
        
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
