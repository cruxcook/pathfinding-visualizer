import pygame, sys, os
from pygame.locals import *

from states.state import *

vector = pygame.math.Vector2
class About(State):
    def __init__(self):
        super().__init__()
        self.current = "ABOUT"
        self.load_props()

    def load_props(self):
        self.is_pathfinding_btn_hovered  = False
        self.is_menu_btn_hovered = False
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.fill(Color(BACKGROUND_COLOR))
        pygame.draw.rect(surface, Color("white"),((0,HEIGHT),(WIDTH,TILE_SIZE+20)))
        draw_grid(surface)
        
        self.draw_btns(surface)
        self.draw_abt_info(surface)

    def get_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:      
            if event.button == 1 and self.is_pathfinding_btn_hovered :
                self.next = "PATHFINDING"
                self.is_done = True
            elif event.button == 1 and self.is_menu_btn_hovered:
                self.next = "MENU"
                self.is_done = True

    def draw_btns(self, surface):
        self.menu_btn           = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH - 15, HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Main Menu", Color(TEXT_COLOR), TEXT_SIZE)
        self.pathfinding_btn    = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH + 15, HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Pathfinding", Color(TEXT_COLOR), TEXT_SIZE)
        
        mouse_pos = vector(pygame.mouse.get_pos())
        if self.menu_btn.collidepoint(mouse_pos):
            self.is_menu_btn_hovered =  True
            self.menu_btn = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH - 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH, BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Main Menu", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_menu_btn_hovered  = False
            
        if self.pathfinding_btn.collidepoint(mouse_pos):
            self.is_pathfinding_btn_hovered =  True
            self.pathfinding_btn = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH + 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH, BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Pathfinding", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_pathfinding_btn_hovered  = False

    #! Fix position and size of rectangle, should adjust automatically based on the content.
    def draw_abt_info(self, surface):
        draw_rect(WIDTH/2,HEIGHT/2,460,260, surface, Color("black"))
        draw_rect(WIDTH/2,HEIGHT/2,450,250, surface, Color("white"))
        
        draw_text("About", surface, 40, Color("red"), WIDTH/2, HEIGHT/2- 200 + 100 )
        draw_text("*---------Author---------*" , surface, 30, Color("#178134"), WIDTH/2, HEIGHT/2 - 150 + 100)
        draw_text("Name: Crux Cook" , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 - 105 + 100)
        draw_text("Github: cruxcook" , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 - 60 + 100)