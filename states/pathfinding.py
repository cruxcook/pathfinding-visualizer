import pygame, sys, os
from pygame.locals import *

from settings import *
from states.state import *

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

        if self.is_instruction_btn_pressed == True:
            self.draw_instruction(surface)
            self.is_instruction_btn_pressed = False

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
            elif event.button == 1 and self.is_instruction_btn_hovered:
                self.is_instruction_btn_pressed = True

    #-------------------------------------------------Load Data-----------------------------------------------------------#
    def load_props(self):
        # MENU BUTTON
        self.is_menu_btn_hovered = False

        # INSTRUCTION BUTTON
        self.is_instruction_closed = False
        self.is_instruction_btn_pressed = False
        self.is_next_btn_hovered = False
        self.is_back_btn_hovered = False
        self.is_close_btn_hovered = False

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

    def draw_instruction(self, surface):
        message_1 = "Press W to place Wall"
        message_2 = "Press L to place Start Marker"
        message_3 = "Press D to place End Marker"
        message_4 = "*------------Mouse------------*"
        message_4_color = Color("blue")
        message_4_size = 30
        message_5 = "Left Mouse to place Wall"
        message_6 = "Middle Mouse to place Start Marker"
        message_7 = "Right Mouse to place End Marker"

        next_btn_pos = 0 # Render "Next" btn at first
        back_btn_pos = 1000 # Hide "Back" btn at first
        
        while True and self.is_instruction_closed == False:
            draw_rect(WIDTH/2,HEIGHT/2,460,490, surface, Color("black"))
            draw_rect(WIDTH/2,HEIGHT/2,450,480, surface, Color("white"))

            draw_text("Instruction", surface, 40, Color("red"), WIDTH/2, HEIGHT/2 - 200)
            draw_text("*---------Keyboard---------*" , surface, 30, Color("blue"), WIDTH/2, HEIGHT/2 - 150)
            draw_text(message_1 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 - 100)
            draw_text(message_2 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 - 60)
            draw_text(message_3 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2-20)
            draw_text(message_4 , surface, message_4_size, message_4_color, WIDTH/2, HEIGHT/2 + 20)
            draw_text(message_5 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 + 60)
            draw_text(message_6 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 + 100)
            draw_text(message_7 , surface, 25, Color("Black"), WIDTH/2, HEIGHT/2 + 140)
            
            self.next_btn = draw_txt_rect(WIDTH/2-100,HEIGHT/2+200 + next_btn_pos,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Next", Color(TEXT_COLOR), TEXT_SIZE)
            self.back_btn = draw_txt_rect(WIDTH/2-100,HEIGHT/2+200 + back_btn_pos,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Back", Color(TEXT_COLOR), TEXT_SIZE)
            self.close_btn = draw_txt_rect(WIDTH/2+100,HEIGHT/2+200,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Close", Color(TEXT_COLOR), TEXT_SIZE)
            
            mouse_pos = vector(pygame.mouse.get_pos())

            if self.next_btn.collidepoint(mouse_pos):
                self.is_next_btn_hovered  = True
                self.next_btn = draw_txt_rect(WIDTH/2-100,HEIGHT/2+200 + next_btn_pos,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Next", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_next_btn_hovered  = False

            if self.back_btn.collidepoint(mouse_pos):
                self.is_back_btn_hovered  = True
                self.back_btn = draw_txt_rect(WIDTH/2-100,HEIGHT/2+200 + back_btn_pos,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Back", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_back_btn_hovered  = False
                
            if self.close_btn.collidepoint(mouse_pos):
                self.is_close_btn_hovered  = True
                self.close_btn = draw_txt_rect(WIDTH/2+100,HEIGHT/2+200,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Close", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_close_btn_hovered  = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.is_instruction_closed = True
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_next_btn_hovered :
                        next_btn_pos = 1000 # Hide "Next" btn
                        back_btn_pos = 0    # Render "Back" btn

                        # ----------- Update messages
                        message_1 = "Press Q to place Weighted Wall"
                        message_2 = "Press A to show/hide full path"
                        message_3 = "Press E to show/hide explored area"
                        message_4 = "Press M to animate the path"
                        message_4_color = Color("Black")
                        message_4_size = 25
                        message_5 = "Press P to print out the wall list"
                        message_6 = "Press Esc to exit"
                        message_7 = ""
                    if event.button == 1 and self.is_back_btn_hovered :
                        self.draw_instruction(surface)
                    elif event.button == 1 and self.is_close_btn_hovered:
                        self.is_instruction_closed = True
                        return
            #---------------------------------------------------------------------------------------#
            pygame.display.update()