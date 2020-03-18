# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 23:40:21 2019

@author: Owen-Laptop
"""

from pyquaternion import Quaternion
import numpy

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
    opposite = {
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
            self.generate_random_orientation()
        else:
            self.stop_face_v = stop_face_v
            self.slide_face_v = slide_face_v
        
    def __repr__(self):
        return f'Block at {self.coords}, with the "{self.get_faces_from_orientation()[0]}" face up.'
    
    def __str__(self):
        return self.__repr__()
    
    def show(self):
        top, up, left, right, down, bot = self.get_faces_from_orientation()
    
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
        
    def print_orientation(self):
        top, up, left, right, down, bot = self.get_faces_from_orientation()
        text =  f'+-------+\n'
        text += f'|   {up}   |\n'
        text += f'| {left} {top} {right} |\n'
        text += f'|   {down}   |\n'
        text += f'+-------+\n'
        print(text)
        
    def get_faces_from_orientation(self):
        tol = 0.0001
        if self.stop_face_v[2] > tol:
            top_face = 'stop'
            if self.slide_face_v[1] > tol:
                up_face = 'slide'
                left_face = 'diag'
            elif self.slide_face_v[1] < tol:
                up_face = 'hoops'
                left_face = 'adj'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] > tol:
                up_face = 'diag'
                left_face = 'hoops'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] < tol:
                up_face = 'adj'
                left_face = 'slide'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        elif self.stop_face_v[2] < tol:
            top_face = 'star'
            if self.slide_face_v[1] > tol:
                up_face = 'slide'
                left_face = 'diag'
            elif self.slide_face_v[1] < tol:
                up_face = 'hoops'
                left_face = 'adj'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] > tol:
                up_face = 'diag'
                left_face = 'hoops'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] < tol:
                up_face = 'adj'
                left_face = 'slide'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        elif self.slide_face_v[2] > tol:
            top_face = 'slide'
            if self.stop_face_v[1] > tol:
                up_face = 'stop'
                left_face = 'diag'
            elif self.stop_face_v[1] < tol:
                up_face = 'star'
                left_face = 'adj'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] > tol:
                up_face = 'adj'
                left_face = 'stop'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] < tol:
                up_face = 'diag'
                left_face = 'star'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        elif self.slide_face_v[2] < tol:
            top_face = 'hoops'
            if self.stop_face_v[1] > tol:
                up_face = 'stop'
                left_face = 'diag'
            elif self.stop_face_v[1] < tol:
                up_face = 'star'
                left_face = 'adj'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] > tol:
                up_face = 'adj'
                left_face = 'stop'
            elif numpy.cross(self.stop_face_v, self.slide_face_v)[1] < tol:
                up_face = 'diag'
                left_face = 'star'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        elif numpy.cross(self.stop_face_v, self.slide_face_v)[2] > tol:
            top_face = 'diag'
            if self.slide_face_v[1] > tol:
                up_face = 'slide'
                left_face = 'stop'
            elif self.slide_face_v[1] < tol:
                up_face = 'hoops'
                left_face = 'star'
            elif self.stop_face_v[1] > tol:
                up_face = 'stop'
                left_face = 'hoops'
            elif self.stop_face_v[1] < tol:
                up_face = 'star'
                left_face = 'slide'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        elif numpy.cross(self.stop_face_v, self.slide_face_v)[2] < tol:
            top_face = 'adj'
            if self.slide_face_v[1] > tol:
                up_face = 'slide'
                left_face = 'stop'
            elif self.slide_face_v[1] < tol:
                up_face = 'hoops'
                left_face = 'star'
            elif self.stop_face_v[1] > tol:
                up_face = 'stop'
                left_face = 'hoops'
            elif self.stop_face_v[1] < tol:
                up_face = 'star'
                left_face = 'slide'
            else:
                raise ValueError('Something went wrong with the orientation vectors')
        else:
            raise ValueError('Something went wrong with the orientation vectors')
        right_face = self.opposite[left_face]
        down_face = self.opposite[up_face]
        bot_face = self.opposite[top_face]
        return top_face, up_face, left_face, right_face, down_face, bot_face
    
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
