import pygame, sys, os
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
    
def draw_txt_rect(x,y,w,h, surface, rectColor, text, txt_color, size):
    rect = draw_rect(x,y,w,h, surface, rectColor)
    draw_text(text, surface, size, txt_color, x, y)
    return rect