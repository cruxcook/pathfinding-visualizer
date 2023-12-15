import pygame, sys, os
from pygame.locals import *

from states.state import *

class About(State):
    def __init__(self):
        super().__init__()
        self.current = "ABOUT"
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.fill(Color("red"))

    def get_event(self,event):
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next = "PATHFINDING"
                self.previous = self.current
                self.current = None
                self.done = True
            if event.key == pygame.K_m:
                self.next = "MENU"
                self.previous = self.current
                self.current = None
                self.done = True
