import pygame, sys, os
from pygame.locals import *

from states.state import *

class PathFinding(State):
    def __init__(self):
        super().__init__()
        self.current = "PATHFINDING"
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.fill(Color("blue"))

    def get_event(self,event):
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next = "MENU"
                self.done = True
            if event.key == pygame.K_a:
                self.next = "ABOUT"
                self.done = True
