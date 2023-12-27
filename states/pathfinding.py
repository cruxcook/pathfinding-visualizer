import pygame, sys, os
from pygame.locals import *

from states.state import *

class Pathfinding(State):
    def __init__(self):
        super().__init__()
        self.current = "PATHFINDING"
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.fill(Color(BACKGROUND_COLOR))
        pygame.draw.rect(surface, Color("white"),((0,HEIGHT),(WIDTH,TILE_SIZE+20)))
        draw_grid(surface)

    def get_event(self,event):
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next = "MENU"
                self.is_done = True
            if event.key == pygame.K_a:
                self.next = "ABOUT"
                self.is_done = True