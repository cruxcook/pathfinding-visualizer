import pygame, sys, os
from pygame.locals import *

from settings import *
from states.state import *

vector = pygame.math.Vector2
class Pathfinding(State):
    def __init__(self):
        super().__init__()
        self.current = "PATHFINDING"
        self.load_props()
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.fill(Color(BACKGROUND_COLOR))
        pygame.draw.rect(surface, Color("white"),((0,HEIGHT),(WIDTH,TILE_SIZE+20)))
        draw_grid(surface)

        self.draw_btns(surface)

    def get_event(self,event):
        #-----------Input from keys (WIP)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next = "MENU"
                self.is_done = True

        #-----------Input from mouse
        # 1: Left Mouse
        # 2: Middle Mouse
        # 3: Right Mouse
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1 and self.is_menu_btn_hovered:
                self.next = "MENU"
                self.is_done = True

    #-------------------------------------------------Load Data-----------------------------------------------------------#
    def load_props(self):
        self.is_menu_btn_hovered = False
        self.is_instruction_closed = False

    #-------------------------------------------------Rendering-------------------------------------------#
    def draw_btns(self, surface):
        self.menu_btn         = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH*3  - 150   ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Main Menu", Color(TEXT_COLOR), TEXT_SIZE)
        self.instruction_btn  = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH*2  - 83    ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Instruction", Color(TEXT_COLOR), TEXT_SIZE)
        self.map_btn          = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH    - 15    ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Load Map", Color(TEXT_COLOR), TEXT_SIZE)
        self.remove_btn       = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH    + 15    ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Remove Map", Color(TEXT_COLOR), TEXT_SIZE)
        self.algorithm_btn    = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH*2  + 83    ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Algorithm", Color(TEXT_COLOR), TEXT_SIZE)
        self.path_btn         = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH*3  + 150   ,HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Path Setting", Color(TEXT_COLOR), TEXT_SIZE)

        mouse_pos = vector(pygame.mouse.get_pos())

        if self.menu_btn.collidepoint(mouse_pos):
            self.is_menu_btn_hovered =  True
            self.menu_btn = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH*3 - 150,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Main Menu", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_menu_btn_hovered  = False
            
        if self.instruction_btn.collidepoint(mouse_pos):
            self.is_instruction_btn_hovered =  True
            self.instruction_btn = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH*2 - 83,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Instruction", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_instruction_btn_hovered  = False
        self.is_instruction_closed = False          # Check to close all instructions 
            
        if self.map_btn.collidepoint(mouse_pos):
            self.is_map_btn_hovered =  True
            self.map_btn = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH - 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Load Map", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_map_btn_hovered  = False
            
        if self.remove_btn.collidepoint(mouse_pos):
            self.is_remove_btn_hovered =  True
            self.remove_btn = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH + 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Remove Map", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_remove_btn_hovered  = False
            
        if self.algorithm_btn.collidepoint(mouse_pos):
            self.is_algorithm_btn_hovered =  True
            self.algorithm_btn = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH*2 + 83,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Algorithm", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_algorithm_btn_hovered  = False
            
        if self.path_btn.collidepoint(mouse_pos):
            self.is_path_btn_hovered =  True
            self.path_btn = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH*3 + 150,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Path Setting", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_path_btn_hovered  = False