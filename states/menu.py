import pygame, sys, os
from pygame.locals import *

from settings import *
from states.state import *

vector = pygame.math.Vector2
class Menu(State):
    def __init__(self):
        super().__init__()
        self.current = "MENU"
        self.load_props()
        
    def load_props(self):
        self.is_pathfinding_btn_hovered  = False
        self.is_about_btn_hovered = False
        
    def update(self, dt):
        pass
            
    def draw(self, surface):
        surface.fill(Color(BACKGROUND_COLOR))
        pygame.draw.rect(surface, Color("white"),((0, HEIGHT),(WIDTH, TILE_SIZE+20)))
        draw_grid(surface)
        
        self.draw_btns(surface)
        self.draw_letters(surface)
        
    def get_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:      
            if event.button == 1 and self.is_pathfinding_btn_hovered :
                self.next = "PATHFINDING"
                self.is_done = True
            elif event.button == 1 and self.is_about_btn_hovered:
                self.next = "ABOUT"
                self.is_done = True
    
    def draw_btns(self,surface):
        self.pathfinding_btn    = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH - 15, HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Start", Color(TEXT_COLOR), TEXT_SIZE)
        self.about_btn          = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH + 15, HEIGHT + (TILE_SIZE+20)/2, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "About", Color(TEXT_COLOR), TEXT_SIZE)

        mouse_pos = vector(pygame.mouse.get_pos())
        if self.pathfinding_btn.collidepoint(mouse_pos):
            self.is_pathfinding_btn_hovered =  True
            self.pathfinding_btn = draw_txt_rect(WIDTH/2 - BUTTON_WIDTH - 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH, BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Start", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_pathfinding_btn_hovered  = False
            
        if self.about_btn.collidepoint(mouse_pos):
            self.is_about_btn_hovered =  True
            self.about_btn = draw_txt_rect(WIDTH/2 + BUTTON_WIDTH + 15,HEIGHT + (TILE_SIZE+20)/2,BUTTON_HOVER_WIDTH, BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "About", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
        else:
            self.is_about_btn_hovered  = False
            
    def draw_letters(self, surface):
        super().load_dirs()
        
        self.p_img = self.__load_letters(self.icons_dir, "letter_P.png")
        self.a_img = self.__load_letters(self.icons_dir, "letter_A.png")
        self.t_img = self.__load_letters(self.icons_dir, "letter_T.png")
        self.h_img = self.__load_letters(self.icons_dir, "letter_H.png")
        self.f_img = self.__load_letters(self.icons_dir, "letter_F.png")
        self.i_img = self.__load_letters(self.icons_dir, "letter_I.png")
        self.n_img = self.__load_letters(self.icons_dir, "letter_N.png")
        self.g_img = self.__load_letters(self.icons_dir, "letter_G.png")
        self.d_img = self.__load_letters(self.icons_dir, "letter_D.png")

        surface.blit(self.p_img, self.p_img.get_rect(center=(WIDTH/2-240, HEIGHT/2-100)))   # Center        P: (WIDTH/2-240, HEIGHT/2-100)
        surface.blit(self.a_img, self.a_img.get_rect(center=(WIDTH/2-80, HEIGHT/2-100)))    # Center        A: (WIDTH/2-80, HEIGHT/2-100)
        surface.blit(self.t_img, self.t_img.get_rect(center=(WIDTH/2+80, HEIGHT/2-100)))    # Center        T: (WIDTH/2+80, HEIGHT/2-100)
        surface.blit(self.h_img, self.h_img.get_rect(center=(WIDTH/2+240, HEIGHT/2-100)))   # Center        H: (WIDTH/2+240, HEIGHT/2-100)
        surface.blit(self.f_img, self.f_img.get_rect(center=(WIDTH/2-480, HEIGHT/2+100)))   # Center        F: (WIDTH/2-480, HEIGHT/2+100)
        surface.blit(self.i_img, self.i_img.get_rect(center=(WIDTH/2-320, HEIGHT/2+100)))   # Center 1st    I: (WIDTH/2-320, HEIGHT/2+100)
        surface.blit(self.n_img, self.n_img.get_rect(center=(WIDTH/2-160, HEIGHT/2+100)))   # Center 1st    N: (WIDTH/2-160, HEIGHT/2+100)
        surface.blit(self.d_img, self.d_img.get_rect(center=(WIDTH/2, HEIGHT/2+100)))       # Center        D: (WIDTH/2, HEIGHT/2+100)
        surface.blit(self.i_img, self.i_img.get_rect(center=(WIDTH/2+320, HEIGHT/2+100)))   # Center 2nd    I: (WIDTH/2+320, HEIGHT/2+100)
        surface.blit(self.n_img, self.n_img.get_rect(center=(WIDTH/2+160, HEIGHT/2+100)))   # Center 2nd    N: (WIDTH/2+160, HEIGHT/2+100)
        surface.blit(self.g_img, self.g_img.get_rect(center=(WIDTH/2+480, HEIGHT/2+100)))   # Center        G: (WIDTH/2+480, HEIGHT/2+100)


    def __load_letters(self, icons_dir, file_name):
        img = pygame.image.load(path.join(self.icons_dir, file_name)).convert_alpha()
        img = pygame.transform.scale(img, (LETTER_SIZE, LETTER_SIZE))
        return img