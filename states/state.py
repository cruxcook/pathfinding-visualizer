import pygame, sys, os
from pygame.locals import *
from os import path
from settings import * 

class State():
    def __init__(self):
        self.done =  False
        self.current = None
        self.next = None
        
    def new(self):
        pass
    def update(self, dt):
        pass
    def draw(self, surface):
        pass
    def get_event(self,event):
        pass

    def load_dirs(self):
        self.current_dir = path.dirname(__file__)
        self.parent_dir = path.abspath(path.join(self.current_dir, os.pardir))
        self.assets_dir = path.join(self.parent_dir, "assets")
        self.icons_dir = path.join(self.assets_dir, 'icons')
    
def draw_text(text, surface, size, color, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    # render: calculate exactly what pattern of pixels is needed
    text_object = font.render(text, True, color)       #render(text, on/off anti-aliasing, color)
    text_rectangle = text_object.get_rect()
    text_rectangle.center = (x,y)
    surface.blit(text_object, text_rectangle)
    return text_rectangle
    
def draw_rect(x,y,w,h, surface, color):
    rectangle = pygame.Rect(x,y,w,h)
    rectangle.center = (x,y)  
    pygame.draw.rect(surface, color, rectangle)
    return rectangle
    
def draw_txt_rect(x,y,w,h, surface, rect_color, text, txt_color, size):
    rect = draw_rect(x,y,w,h, surface, rect_color)
    draw_text(text, surface, size, txt_color, x, y)
    return rect

def draw_grid(surface):
    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, Color(GRID_COLOR),(x,0),(x,HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, Color(GRID_COLOR),(0,y),(WIDTH,y))
    
    # draw the last line 
    pygame.draw.line(surface, Color(GRID_COLOR),(0,HEIGHT),(WIDTH,HEIGHT))