import pygame 
import heapq
from pygame.locals import *

from settings import *
from entities.wall import *

vector = pygame.math.Vector2

class SquareGrid():
    def __init__(self, w, h):
        self.width_pos = w
        self.height_pos = h
        self.walls = []
        
        # Direction (right, left, down, up)
        self.connection = [vector(1,0),vector(-1,0),vector(0,1),vector(0,-1)]
    
    def in_bounds(self, node):       # inside screen area
        '''return 0 <= node.x < self.width_pos and 0 <= node.y < self.height_pos'''
        if 0 <= node.x < self.width_pos and 0 <= node.y < self.height_pos:
            return node
        
    def passable(self, node):       # neightbor nodes not wall
        '''return node not in self.walls'''
        if not node in self.walls:
            return node
        
    def find_neighbors(self, node, connection):
        #neighbors = [node + c for c in connection]         # active this can make a error with the first node on the top left 
        
        neighbors = []
        for c in connection:
            neighbors.append(node+c)
        
        #if len(connection) == 4:               # update this function only apply for straight path, not diagonal
        #    if (node.x + node.y) % 2:
        #        neighbors.reverse()
        
        #neighbors = filter(self.in_bounds,neighbors)     # return node in neighbors with function=True
        #neighbors = filter(self.passable, neighbors)
        
        remove_list = []
        for n in neighbors:
            if n != self.in_bounds(n)  or n != self.passable(n): 
                remove_list.append(n)
        for r in remove_list:
            neighbors.remove(r)
            
        return neighbors
        
class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vector(to_node) - vector(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 1
        else:
            return self.weights.get(to_node, 0) + 1.4        # square root of 2

class PriorityQueue():
    def __init__(self):
        self.nodes = []

    def push(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def pop(self):
        return heapq.heappop(self.nodes)[1]

    def is_empty(self):
        return len(self.nodes) == 0