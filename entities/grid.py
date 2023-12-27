import pygame 
import heapq
from pygame.locals import *
from settings import *
from entities.wall import *

vector = pygame.math.Vector2

class SquareGrid():
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.walls = []
        
        # direction ( right, left, down, up)
        self.connection = [vector(1,0),vector(-1,0),vector(0,1),vector(0,-1)]
    
    def inBounds(self, node):       # inside screen area
        '''return 0 <= node.x < self.width and 0 <= node.y < self.height'''
        if 0 <= node.x < self.width and 0 <= node.y < self.height:
            return node
        
    def passable(self, node):       # neightbor nodes not wall
        '''return node not in self.walls'''
        if not node in self.walls:
            return node
        
    def findNeighbors(self, node, connection):
        #neighbors = [node + c for c in connection]         # active this can make a error with the first node on the top left 
        
        neighbors = []
        for c in connection:
            neighbors.append(node+c)
        
        #if len(connection) == 4:               # update this function only apply for straight path, not diagonal
        #    if (node.x + node.y) % 2:
        #        neighbors.reverse()
        
        #neighbors = filter(self.inBounds,neighbors)     # return node in neighbors with function=True
        #neighbors = filter(self.passable, neighbors)
        
        removeList = []
        for n in neighbors:
            if n != self.inBounds(n)  or n != self.passable(n): 
                removeList.append(n)
        for r in removeList:
            neighbors.remove(r)
            
        return neighbors