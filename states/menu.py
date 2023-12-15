import pygame, sys, os
from pygame.locals import *

from states.state_manager import *
from states.state import *

vector = pygame.math.Vector2
class Menu(State):
    def __init__(self):
        super().__init__()
        self.current = "MENU"
        self.next = None
        
        self.hover_pathfinding  = False
        
        self.btn_width = 450
        self.btn_height = 250
        self.hover_width = 520
        self.hover_height = 320
        
        self.btn_color = "blue"
        self.hover_color = "green"
        
        self.txt_color = "white"
        self.txt_size = 50
        self.hover_txt_size = 70
        
    def update(self, dt):
        pass
            
    def draw(self, surface):
        surface.fill(Color("yellow"))
        self.red_btn = draw_txt_rect(WIDTH/2,HEIGHT/2, self.btn_width,
                                           self.btn_height, surface, 
                                           Color(self.btn_color), "pathfinding", 
                                           Color(self.txt_color), self.txt_size)
        
        mousePosition = vector(pygame.mouse.get_pos())
        if self.red_btn.collidepoint(mousePosition):
            self.hover_pathfinding =  True
            self.red_btn = draw_txt_rect(WIDTH/2,HEIGHT/2, self.hover_width,
                                               self.hover_height, surface, 
                                               Color(self.hover_color), "PATHFINDING", 
                                               Color(self.txt_color), self.hover_txt_size)
        else:
            self.hover_pathfinding  = False
        
    def get_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next = "PATHFINDING"
                self.done = True
            if event.key == pygame.K_a:
                self.next = "ABOUT"
                self.done = True

        if event.type == pygame.MOUSEBUTTONDOWN:      
            if event.button == 1 and self.hover_pathfinding :
                self.next = "PATHFINDING"
                self.done = True
    