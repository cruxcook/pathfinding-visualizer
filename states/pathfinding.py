import pygame, sys, os, time, math, random
import ast        # Convert string to list
from pygame.locals import *
from collections import deque       # The double-ended queue, cannot access items in the middle, but perfect for either ends ( faster than using list )

from settings import *
from states.state import *
from entities.grid import *
from entities.wall import *
from algorithms.breadth_first_search import *

class Pathfinding(State):
    def __init__(self):
        super().__init__()
        self.current = "PATHFINDING"
        self.load_props()   #? x2check if this is needed
        self.load_assets()  #? x2check if this is needed

        self.all_sprites = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()
        self.all_weighted_walls = pygame.sprite.Group()

        self.sg = SquareGrid(GRID_WIDTH,GRID_HEIGHT) 
        self.wg = WeightedGrid(GRID_WIDTH,GRID_HEIGHT) 

        self.bfs = BreadthFirstSearch()

    def update(self, dt):
        if self.is_random_btn_pressed == True:
            self.generate_random_map()
        else:
            self.width_pos = 0
            self.height_pos= 0

        if self.path_line == "Diagonal":
            self.sg.connection = [vector(1,0),vector(-1,0),vector(0,1),vector(0,-1),
                                vector(1,1),vector(-1,1),vector(1,-1),vector(-1,-1)]
        else:
            self.sg.connection = [vector(1,0),vector(-1,0),vector(0,1),vector(0,-1)]
        self.wg.connection = self.sg.connection

        if self.is_timer_running == True:   #? x2check this method, seem not accurate
            self.start_time = pygame.time.get_ticks()

        if self.search == "BFS":
            self.bfs.run(self.sg, self.starting_pos, self.ending_pos, self.start_time)

        self.all_sprites.update()
        self.all_walls.update()
    
    def draw(self, surface):
        surface.fill(Color(BACKGROUND_COLOR))
        pygame.draw.rect(surface, Color("white"),((0,HEIGHT),(WIDTH,TILE_SIZE+20)))
        draw_grid(surface)

        #----------------------------------------------------------------------#
        self.draw_btns(surface)

        if self.is_instruction_btn_pressed == True:
            self.draw_instruction(surface)
            self.is_instruction_btn_pressed = False

        if self.is_map_btn_pressed == True:
            self.draw_map(surface)
            self.is_map_btn_pressed = False

        if self.is_algorithm_btn_pressed == True:
            self.draw_algorithm_menu(surface)    
            self.is_algorithm_btn_pressed = False

        if self.is_path_btn_pressed == True:
            self.draw_path_menu(surface)
            self.is_path_btn_pressed = False

        if self.search is not None:
            draw_text(self.search, surface, 25, Color("red"), WIDTH/2 ,HEIGHT + (TILE_SIZE+20)/2 - 13)
            if self.search == "BFS":
                self.bfs.draw_bfs_area(surface)
                self.bfs.draw_bfs_path(surface)  

                if self.is_all_paths_showed == True:
                    draw_all_paths(surface, self.bfs.bfs_path, self.bfs.arrows)
        else:
            draw_text("HELLO", surface, 35, Color("red"), WIDTH/2 ,HEIGHT + (TILE_SIZE+20)/2) 
        
        #----------------------------------------------------------------------#
        self.draw_default_icons(surface)
        self.all_sprites.draw(surface)

    def get_event(self,event):
        mouse_pos = vector(pygame.mouse.get_pos()) // TILE_SIZE     # Division(floor)

        #!-----------Input from keys (WIP)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:     # Place regular wall
                self.is_mouse_pressed = True 
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT: 
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:            # Avoid placing wall on "start" and "end" icon
                        if mouse_pos in self.sg.walls :
                            pygame.sprite.spritecollide(Wall(self,vector(mouse_pos),self.wall_icon), self.all_sprites, True)
                            self.sg.walls.remove(mouse_pos)
                        else:
                            Wall(self,vector(mouse_pos),self.wall_icon)
                            self.sg.walls.append(mouse_pos)
                    self.wg.walls = self.sg.walls
                self.load_search()
            elif event.key == pygame.K_q:   # Place weighted wall
                self.is_weighted_pressed = True
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT: 
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:            # Avoid placing wall on "start" and "end" icon
                        if convert_vect_int(mouse_pos) in self.wg.weights :
                            pygame.sprite.spritecollide(WeightedWall(self,vector(mouse_pos),self.weighted_wall_icon), self.all_sprites, True)
                            self.wg.weights.pop(convert_vect_int(mouse_pos), None)      # Return none if that element not in dictionary
                        else:
                            WeightedWall(self,vector(mouse_pos),self.weighted_wall_icon)
                            self.wg.weights[convert_vect_int(mouse_pos)] = 50       # Low priority == Hight cost
                self.load_search()
            elif event.key == pygame.K_a:   # Show up all paths
                self.is_all_paths_showed = not self.is_all_paths_showed
        
        elif event.type == pygame.KEYUP:    # Stop dragging motion
            self.is_mouse_pressed = False 
            self.is_weighted_pressed = False

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
            elif event.button == 1 and self.is_map_btn_hovered:
                self.is_map_btn_pressed = True
            elif event.button == 1 and self.is_remove_btn_hovered:
                self.all_sprites = pygame.sprite.Group()
                self.sg.walls = []                      #Need to update ( remove or sth, not neccessary because we alread had all_sprites)
                self.wg.walls = []
                self.is_random_btn_pressed = False

                # Reset search value    
                self.new_search_props()  
                self.search = None
            elif event.button == 1 and self.is_algorithm_btn_hovered:
                self.is_algorithm_btn_pressed = True
            elif event.button == 1 and self.is_path_btn_hovered:
                self.is_path_btn_pressed = True
            elif event.button == 1:     # Left Mouse places a regular wall
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT: 
                    self.is_mouse_pressed = True 
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:            # not make wall on "start" and "end" icon
                        if mouse_pos in self.sg.walls :
                            pygame.sprite.spritecollide(Wall(self,vector(mouse_pos),self.wall_icon), self.all_sprites, True)
                            self.sg.walls.remove(mouse_pos)
                        else:
                            Wall(self,vector(mouse_pos),self.wall_icon)
                            self.sg.walls.append(mouse_pos)
                    self.wg.walls = self.sg.walls                      
                    self.load_search()
            elif event.button == 3:     # Right Mouse places Ending Icon
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT:
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:
                        if not mouse_pos in self.sg.walls :
                            self.ending_pos = mouse_pos
                            self.load_search()
            elif event.button == 2:     # Middle Mouse places Starting Icon
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT:
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:
                        if not mouse_pos in self.sg.walls :
                            self.starting_pos = mouse_pos
                            self.load_search()
                            
        # Combine `MOUSEMOTION` & `MOUSEBUTTONUP` to place walls/weighted walls
        # when holding mouse, not clicking 1 by 1.
        elif event.type == pygame.MOUSEMOTION:
            if self.is_mouse_pressed:
                if (0 <= int(mouse_pos.x) < GRID_WIDTH) and (0 <= int(mouse_pos.y) < GRID_HEIGHT): 
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:            # not make wall on "start" and "end" icon
                        if mouse_pos not in self.sg.walls :
                            Wall(self,vector(mouse_pos),self.wall_icon)
                            self.sg.walls.append(mouse_pos)
                    self.wg.walls = self.sg.walls 

            elif self.is_weighted_pressed:
                if 0 <= int(mouse_pos.x) < GRID_WIDTH and 0 <= int(mouse_pos.y) < GRID_HEIGHT: 
                    if check_collision(mouse_pos, self.starting_pos) == False and check_collision(mouse_pos, self.ending_pos) == False:            # not make wall on "start" and "end" icon
                        if convert_vect_int(mouse_pos) not in self.wg.weights :
                            WeightedWall(self,vector(mouse_pos),self.weighted_wall_icon)
                            self.wg.weights[convert_vect_int(mouse_pos)] = 50       # low priority == hight cost
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_mouse_pressed = False
            self.is_weighted_pressed = False

    #-------------------------------Load Data----------------------------------#
    def load_props(self):
        self.walls = []
        self.saved_walls = []
        
        self.width_pos = 0
        self.height_pos = 0

        self.is_all_paths_showed = False
    
        # MENU BUTTON
        self.is_menu_btn_hovered = False

        # INSTRUCTION BUTTON
        self.is_instruction_closed = False
        self.is_instruction_btn_pressed = False
        self.is_next_btn_hovered = False
        self.is_back_btn_hovered = False
        self.is_close_btn_hovered = False   #? x2check if we can use it locally inside each function

        # MAP BUTTON
        self.is_map_btn_pressed = False
        self.is_random_btn_pressed = False
        self.is_file_btn_hovered = False
        self.is_random_btn_hovered = False
        self.starting_pos = vector(20,0)    # Default starting position
        self.ending_pos = vector(3,13)      # Default ending position
        self.is_mouse_pressed = False       # Place regular wall on map 
        self.is_weighted_pressed = False    # Place weighted wall on map

        # REMOVE BUTTON
        self.is_remove_btn_hovered = False

        # ALGORITHM BUTTON
        self.search = None                  # Track running `Search` algorithm 
        self.is_algorithm_btn_pressed = False
        self.is_algorithm_btn_hovered = False
        self.is_bfs_done = False
        self.is_timer_running = False

        # PATH BUTTON
        self.is_path_btn_hovered = False
        self.is_path_btn_pressed = False
        self.path_line = None               # Change line to Diagonal or Straight

    def load_assets(self):
        super().load_dirs()
        #---------------------------Load Map
        data = ""
        # Choose file to open here, original or new walls
        f = open(path.join(self.assets_dir,"default_wall_map.txt"),"rt")
        for line in f:
            data += line.strip()
        
        #ast.literal_eval(...)     # String representation of list to list 
        self.walls = ast.literal_eval(data) 
        
        #----------------------------Load Images
        self.wall_icon = pygame.image.load(path.join(self.icons_dir, 'icons8-brick-wall-58.png')).convert_alpha()
        self.wall_icon = pygame.transform.scale(self.wall_icon, (TILE_SIZE + 6, TILE_SIZE + 8))       #(54,58)
        
        self.weighted_wall_icon = pygame.image.load(path.join(self.icons_dir, 'icons8-brick-wall-58_orange.png')).convert_alpha()
        self.weighted_wall_icon = pygame.transform.scale(self.weighted_wall_icon, (TILE_SIZE + 6, TILE_SIZE + 8))
        
        self.ending_icon = pygame.image.load(path.join(self.icons_dir, 'icons8-roulette-51.png')).convert_alpha()
        self.ending_icon = pygame.transform.scale(self.ending_icon, (TILE_SIZE + 3, TILE_SIZE + 3))     #(51,51)
        #self.ending_icon.fill((0, 255, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)        # paint color on image
        
        self.starting_icon = pygame.image.load(path.join(self.icons_dir, 'icons8-home-address-48.png')).convert_alpha()
        self.starting_icon = pygame.transform.scale(self.starting_icon, (TILE_SIZE, TILE_SIZE))
        #self.starting_icon.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.arrows = {}
        self.arrow_icon = pygame.image.load(path.join(self.icons_dir, 'arrowRight.png')).convert_alpha()
        self.arrow_icon = pygame.transform.scale(self.arrow_icon, (TILE_SIZE + 2, TILE_SIZE + 2))       #(50,50) change size of image to (newWidth,newHeight)
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1,1), (-1,1),(1,-1),(-1,-1)]:
            self.arrows[direction] = pygame.transform.rotate(self.arrow_icon, vector(direction).angle_to(vector(1, 0)))  
        
        '''
        self.arrows[(1,0)] = pygame.transform.rotate(self.arrow_icon, 0)       
        self.arrows[(0,1)] = pygame.transform.rotate(self.arrow_icon, 270)     
        self.arrows[(-1,0)] = pygame.transform.rotate(self.arrow_icon, 180)        
        self.arrows[(0,-1)] = pygame.transform.rotate(self.arrow_icon, 90) 
        self.arrows[(1,1)] = pygame.transform.rotate(self.arrow_icon, 315)       
        self.arrows[(-1,1)] = pygame.transform.rotate(self.arrow_icon, 225)     
        self.arrows[(1,-1)] = pygame.transform.rotate(self.arrow_icon, 45)        
        self.arrows[(-1,-1)] = pygame.transform.rotate(self.arrow_icon, 135)    
        '''  

    def load_walls(self, wall_map):
        data = []
        for wall in wall_map:
            data.append(vector(wall))
            Wall(self,vector(wall),self.wall_icon)
        return data
    
    #? x2check this with new_search_props() & load_search_props()
    def load_search(self):
        if self.search == "BFS" or self.search == "DFS":
            self.is_bfs_done = False  # Reset search value   

        self.new_search_props() 
        self.load_search_props()

    #? x2check this with load_search() & load_search_props()
    def new_search_props(self):
        self.bfs_frontier = deque()
        self.bfs_visited = []
        self.bfs_path = {}       # {node( int(vector) ) : direction(vector)}

        self.node_path = deque() # Save only node of "main path" to pop out

    #? x2check this with load_search() & new_search_props()
    def load_search_props(self):
        self.bfs_frontier.append(self.starting_pos) 
        self.bfs_visited.append(self.starting_pos)
        self.bfs_path[convert_vect_int(self.starting_pos)] = None  

        self.start_time = 0
        self.end_time = 0
        self.is_timer_running = True    #? x2check this method, seem not accurate
        self.is_node_path_done = False            # need to check in case loop of program add up more path in "node_path"
        self.node_path = deque()

        self.bfs.load_props(self.sg, self.starting_pos, self.ending_pos, 
                            self.path_line, self.node_path, self.is_node_path_done, 
                            self.is_timer_running, self.arrows,
                            self.bfs_path, self.bfs_frontier, self.bfs_visited, self.is_bfs_done)

    #-------------------------------Support functions--------------------------#
    #! Fix this to PRIVATE
    def generate_random_map(self):
        '''
        for y in range(0, GRID_HEIGHT, 1):
            h = random.randrange(0,4,1)
            for x in range(0, GRID_WIDTH, 1):
                w = random.randrange(0,5,1)
                if w == h and vector(x,y) != self.starting_pos and vector(x,y) != self.ending_pos:
                    Wall(self,vector(x,y),self.wall_icon)
                    self.sg.walls.append(vector(x,y))
        self.wg.walls = self.sg.walls
        '''
        if self.height_pos < GRID_HEIGHT:
            h = random.randrange(0,4,1)
            if self.width_pos < GRID_WIDTH:
                w = random.randrange(0,5,1)
                if (w == h) and (vector(self.width_pos,self.height_pos) != self.starting_pos) and (vector(self.width_pos,self.height_pos) != self.ending_pos):
                    Wall(self,vector(self.width_pos,self.height_pos),self.wall_icon)
                    self.sg.walls.append(vector(self.width_pos,self.height_pos))
                    self.wg.walls = self.sg.walls
                self.width_pos+=1
            else:
                self.height_pos+=1
                self.width_pos = 0
        else:
            self.is_random_btn_pressed = False
            
    #---------------------------------Rendering--------------------------------#
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
            #------------------------------------------------------------------#
            pygame.display.update()

    #? Consider separating Map function into a class
    def draw_map(self, surface):
        while True:
            draw_rect(WIDTH/2,HEIGHT/2,250,350, surface, Color("black"))
            draw_rect(WIDTH/2,HEIGHT/2,240,340, surface, Color("white"))

            draw_text("Load Map", surface, 40, Color("red"), WIDTH/2, HEIGHT/2 - 160 + 30)
            
            self.file_btn   = draw_txt_rect(WIDTH/2,HEIGHT/2- 80 + 30,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "File", Color(TEXT_COLOR), TEXT_SIZE)
            self.random_btn = draw_txt_rect(WIDTH/2,HEIGHT/2 +30 ,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Random", Color(TEXT_COLOR), TEXT_SIZE)
            self.close_btn  = draw_txt_rect(WIDTH/2,HEIGHT/2+80 + 30,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Close", Color(TEXT_COLOR), TEXT_SIZE)
            
            mouse_pos = vector(pygame.mouse.get_pos())

            if self.file_btn.collidepoint(mouse_pos):
                self.is_file_btn_hovered  = True
                self.file_btn = draw_txt_rect(WIDTH/2,HEIGHT/2-80 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "File", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_file_btn_hovered  = False
                
            if self.random_btn.collidepoint(mouse_pos):
                self.is_random_btn_hovered  = True
                self.random_btn = draw_txt_rect(WIDTH/2,HEIGHT/2 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Random", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_random_btn_hovered  = False
                
            if self.close_btn.collidepoint(mouse_pos):
                self.is_close_btn_hovered  = True
                self.close_btn = draw_txt_rect(WIDTH/2,HEIGHT/2+80 + 30 ,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Close", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_close_btn_hovered  = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_file_btn_hovered:
                        self.all_sprites = pygame.sprite.Group()
                        self.starting_pos = vector(20,0)            # restart location of "start" to original, in case of collision with walls
                        self.ending_pos = vector(3,13)          # restart location of "destination" to original
                        self.sg.walls = []
                        self.wg.walls = []
                        self.is_random_btn_pressed = False
                        self.sg.walls = self.load_walls(self.walls)
                        self.wg.walls = self.sg.walls
                        
                        # Reset search value    
                        self.new_search_props()   
                        self.search = None
                        return
                    
                    if event.button == 1 and self.is_random_btn_hovered:
                        self.all_sprites = pygame.sprite.Group()
                        self.starting_pos = vector(20,0)            # restart location of "start" to original, in case of collision with walls
                        self.ending_pos = vector(3,13)          # restart location of "destination" to original
                        self.sg.walls = []
                        self.wg.walls = []
                        self.is_random_btn_pressed = True
                        
                        # Reset search value    
                        self.new_search_props()   
                        self.search = None
                        return
                    
                    if event.button == 1 and self.is_close_btn_hovered:
                        return
            #------------------------------------------------------------------#
            pygame.display.update()

    # Draw algorithm options to choose
    def draw_algorithm_menu(self, surface):
        while True:
            draw_rect(WIDTH/2,HEIGHT/2,560,410, surface, Color("black"))
            draw_rect(WIDTH/2,HEIGHT/2,550,400, surface, Color("white"))
            draw_text("Algorithm", surface, 40, Color("red"), WIDTH/2, HEIGHT/2 - 190 + 30)
            
            self.bfs_btn      = draw_txt_rect(WIDTH/2, HEIGHT/2-120 + 30, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "BFS", Color(TEXT_COLOR), TEXT_SIZE)
            self.close_btn    = draw_txt_rect(WIDTH/2, HEIGHT/2+120 + 30, BUTTON_WIDTH, BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Close", Color(TEXT_COLOR), TEXT_SIZE)
                
            mouse_pos = vector(pygame.mouse.get_pos())

            if self.bfs_btn.collidepoint(mouse_pos):
                self.is_bfs_btn_hovered  = True
                self.bfs_btn = draw_txt_rect(WIDTH/2,HEIGHT/2-120 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "BFS", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_bfs_btn_hovered  = False
                
            if self.close_btn.collidepoint(mouse_pos):
                self.is_close_btn_hovered  = True
                self.close_btn = draw_txt_rect(WIDTH/2,HEIGHT/2+120 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Close", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_close_btn_hovered  = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_bfs_btn_hovered:
                        self.search = "BFS"
                        self.new_search_props()
                        self.load_search_props()
                        return
                    if event.button == 1 and self.is_close_btn_hovered:
                        return
            pygame.display.update()   

    def draw_path_menu(self, surface):
        while True:
            draw_rect(WIDTH/2,HEIGHT/2,250,350, surface, Color("black"))
            draw_rect(WIDTH/2,HEIGHT/2,240,340, surface, Color("white"))

            draw_text("Path Line", surface, 40, Color("red"), WIDTH/2, HEIGHT/2 - 160 + 30)
            
            self.diagonal_btn = draw_txt_rect(WIDTH/2,HEIGHT/2- 80 + 30,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Diagonal", Color(TEXT_COLOR), TEXT_SIZE)
            self.straight_btn = draw_txt_rect(WIDTH/2,HEIGHT/2 +30 ,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Straight", Color(TEXT_COLOR), TEXT_SIZE)
            self.close_btn    = draw_txt_rect(WIDTH/2,HEIGHT/2+80 + 30,BUTTON_WIDTH,BUTTON_HEIGHT, surface, Color(BUTTON_COLOR), "Close", Color(TEXT_COLOR), TEXT_SIZE)
            
            mouse_pos = vector(pygame.mouse.get_pos())

            if self.diagonal_btn.collidepoint(mouse_pos):
                self.is_diagonal_btn_hovered  = True
                self.diagonal_btn = draw_txt_rect(WIDTH/2,HEIGHT/2-80 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Diagonal", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_diagonal_btn_hovered  = False
                
            if self.straight_btn.collidepoint(mouse_pos):
                self.is_straight_btn_hovered  = True
                self.straight_btn = draw_txt_rect(WIDTH/2,HEIGHT/2 + 30,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Straight", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_straight_btn_hovered  = False
                
            if self.close_btn.collidepoint(mouse_pos):
                self.is_close_btn_hovered  = True
                self.close_btn = draw_txt_rect(WIDTH/2,HEIGHT/2+80 + 30 ,BUTTON_HOVER_WIDTH,BUTTON_HOVER_HEIGHT, surface, Color(BUTTON_HOVER_COLOR), "Close", Color(TEXT_HOVER_COLOR), TEXT_HOVER_SIZE)
            else:
                self.is_close_btn_hovered  = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_diagonal_btn_hovered:
                        self.path_line = "Diagonal"
                        self.load_search()
                        self.load_search_props()
                        return
                    if event.button == 1 and self.is_straight_btn_hovered:
                        self.path_line = "Straight"
                        self.load_search()
                        self.load_search_props()
                        return
                    if event.button == 1 and self.is_close_btn_hovered:
                        return
            #---------------------------------------------------------------------------------------#
            pygame.display.update()

    #! Fix this to PRIVATE
    # Draw Starting & Ending icons
    def draw_default_icons(self, surface):
        self.center_ending_pos = (self.ending_pos.x * TILE_SIZE + TILE_SIZE / 2, self.ending_pos.y * TILE_SIZE + TILE_SIZE / 2)
        surface.blit(self.ending_icon, self.ending_icon.get_rect(center=self.center_ending_pos))
        
        self.center_starting_pos = (self.starting_pos.x * TILE_SIZE + TILE_SIZE / 2, self.starting_pos.y * TILE_SIZE + TILE_SIZE / 2)
        surface.blit(self.starting_icon, self.starting_icon.get_rect(center=self.center_starting_pos))
