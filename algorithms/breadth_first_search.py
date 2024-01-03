from pygame.locals import *
from collections import deque       # The double-ended queue, cannot access items in the middle, but perfect for either ends ( faster than using list )

from settings import *
from entities.grid import *
from entities.wall import *
from states.state import *

class BreadthFirstSearch(State):
    def __init__(self):
        super().__init__()

    def load_props(self, sg, starting_pos, ending_pos, 
                path_line, node_path, is_node_path_done, 
                is_timer_running, arrows,
                bfs_path, bfs_frontier, bfs_visited, is_bfs_done):
        self.sg = sg
        self.starting_pos = starting_pos
        self.ending_pos = ending_pos
        self.path_line = path_line
        self.node_path = node_path
        self.is_node_path_done = is_node_path_done
        self.is_timer_running = is_timer_running
        self.end_time = 0
        self.start_time = 0
        self.arrows = arrows 

        self.bfs_path = bfs_path
        self.bfs_frontier = bfs_frontier
        self.bfs_visited = bfs_visited
        self.is_bfs_done = is_bfs_done

    def run(self, graph, start, end, start_time):
        self.start_time = start_time
        if len(self.bfs_frontier)>0 and self.is_bfs_done == False:     # as long as there are things in frontier
            #current_node = self.checkB_DFS(self.bfs_frontier)     # Uncomment this if had checkB_DFS
            current_node = self.bfs_frontier.popleft()   #! Remove this if had checkB_DFS()   
            if current_node == end:
                self.is_bfs_done = True
            for next_node in graph.find_neighbors(current_node, graph.connection):       # find neightbor of current_node node
                if next_node not in self.bfs_visited:
                    self.bfs_frontier.append(next_node)
                    self.bfs_visited.append(next_node)
    
    def get_bfs_path(self, graph, start, end):
        """ Rerun BFS but from destination to location to draw the path"""
        frontier = deque()
        frontier.append(start)
        path = {}
        path[convert_vect_int(start)] = None
        while len(frontier) > 0:
            #current_node = self.checkB_DFS(frontier)    # Uncomment this if had checkB_DFS
            current_node = frontier.popleft()   #! Remove this if had checkB_DFS()       
            if current_node == end:
                break
            for next_node in graph.find_neighbors(current_node, graph.connection):
                if convert_vect_int(next_node) not in path:
                    frontier.append(next_node)
                    path[convert_vect_int(next_node)] = next_node - current_node 
        return path    
    
    def draw_bfs_area(self, surface):
        if self.path_line == "Diagonal":
            #visited_color = "#456e82"
            visited_color = "#318889"
            frontier_color = "#00fff3"
        else:
            #visited_color = "#456e82"
            visited_color = "#31897f"
            frontier_color = "#00ff9e"

        # filled visited areas
        for loc in self.bfs_visited:
            x, y = loc
            r = pygame.Rect(x * TILE_SIZE +1, y * TILE_SIZE +1, TILE_SIZE -1, TILE_SIZE-1)
            pygame.draw.rect(surface, Color(visited_color), r)
        
        # filled frontier areas
        if len(self.bfs_frontier) > 0:   
            for node in self.bfs_frontier:
                x, y = node
                r = pygame.Rect(x * TILE_SIZE +1, y * TILE_SIZE + 1, TILE_SIZE -1, TILE_SIZE -1)
                pygame.draw.rect(surface, Color(frontier_color), r)            

    def draw_bfs_path(self, surface):
        if self.is_bfs_done == True:
            self.bfs_path = self.get_bfs_path(self.sg, self.starting_pos, self.ending_pos)
            main_path = {}  # Save the final path from location to destination

            ''' Start rendering from destination back to location, due to the sign of arrows '''
            current_node = self.ending_pos - self.bfs_path[convert_vect_int(self.ending_pos)]
            while current_node != self.starting_pos:   
                # save the final path for path animation
                main_path[convert_vect_int(current_node)] = self.bfs_path[convert_vect_int(current_node)]
                # find next_node in path
                current_node = current_node - self.bfs_path[convert_vect_int(current_node)]    
                
            if self.is_node_path_done == False:
                for node in main_path:          # save node of the main path
                    self.node_path.append(node)      # use node_path[] instead of assigning directly main_path{} for splitting up node, from direction in mainMap 
                self.is_node_path_done = True

            if self.is_timer_running == True:   #? x2check about this method, seem not accurate
                self.end_time = pygame.time.get_ticks() - self.start_time 
                self.is_timer_running = False     
            draw_text(str(self.end_time)+"'", surface, 22, Color("red"), WIDTH/2 ,HEIGHT + (TILE_SIZE+20)/2 + 15)
        
        if self.is_node_path_done:            
            """ Update node_path as well as exclude updating main_path with new location"""
            for current_node in self.node_path:
                current_node = vector(current_node)
                x = current_node.x * TILE_SIZE + TILE_SIZE / 2
                y = current_node.y * TILE_SIZE + TILE_SIZE / 2
                img = self.arrows[convert_vect_int(self.bfs_path[convert_vect_int(current_node)])]
                r = img.get_rect(center=(x, y))
                surface.blit(img, r)
