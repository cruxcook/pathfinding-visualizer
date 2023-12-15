import pygame, sys, os
from settings import *

from states.menu import *
from states.pathfinding import *
from states.about import * 

class StateManager:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT+TILE_SIZE))
        self.clock = pygame.time.Clock()
        
        #---------------------------------------------------------------------------------------#
        self.state_dict = {"MENU" : Menu(),
                          "PATHFINDING" : PathFinding(),
                          "ABOUT" : About()}
        
        self.load_state("MENU")
        
    def load_state(self, state_name):
        self.state = self.state_dict[state_name]
    
    def flip_state(self):
        self.state.done = False
        self.state_name = self.state.next
        self.load_state(self.state_name)

    def run(self):
        while(self.running):
            self.delta_time = self.clock.tick(FPS) / 1000
            self.event_handler()
            self.update(self.delta_time)
            self.draw(self.screen)
            pygame.display.flip()
        self.end()
        
    def end(self):
        pygame.quit()
        sys.exit()
    
    def update(self, dt):
        if self.state.done == True:
            self.flip_state()
            
        self.state.update(dt)
        
    def draw(self, surface):
        self.state.draw(surface)
        
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            self.state.get_event(event)