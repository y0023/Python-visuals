import pygame 
import math
from queue import PriorityQueue 

# initializes a square windown for the visualization to run
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* path finding visualized")

# set of colors used 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
GREY = (128, 128, 128)
PINK = (237, 138, 221)
ORANGE = (255, 128, 0)
SKYBLUE = (135, 206, 235)
 
class Node:
        # basic class
        def __init__(self, row, col, width, all_rows):
            self.row = row 
            self.col = col
            self.width = width
            self.all_rows = all_rows
            self.x = row * width
            self.y = col * width
            self.color = WHITE
            self.neighbors = []
        
        # returns (y,x) of a point node
        def get_pos(self):
              return self.row, self.col
        
        # color code the point of intrest on the board 
        # define all possible states 

        # nodes considered
        def is_looked(self):
              return self.color == RED
        
        # nodes to possibly visit 
        def is_possible(self):
              return self.color == GREEN 
        
        # a barrier that cannot be explored
        def is_wall(self):
              return self.color == BLACK
        
        # start position node
        def is_start(self):
              return self.color == SKYBLUE
        
        # end position node
        def is_end(self):
              return self.color == PINK
        
        # restetting all nodes to white when done
        def reset(self): 
              self.color = WHITE
        
        # next set of defines
        # makes certain nodes a certain color 

        # set considered nodes to red 
        def make_looked(self):
              self.color = RED

        # set possible nodes to green 
        def make_possible(self):
              self.color = GREEN
         
        # set barrier nodes to black
        def make_barrier(self): 
              self.color = BLACK

        # set start node to skyblue
        def make_start(self):
              self.color = SKYBLUE

        # set end nodes to pink 
        def make_end(self):
              self.color = PINK
        
        # sets the optimal path to orange
        def make_path(self):
              self.color = YELLOW
        # function to make the window with pygame
        def draw(self, win):
              pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
        # this function checks for valid neighbors that arent barriers
        # allows for our algirithem to see awhats surrounding it by what its neighbors are near
        def update_neigbors(self, grid):
              self.neighbors = []
              # checks a if current row is not the last row
              # this goes down the grid untill it terminates at the final row
              # for each row and col it will list if neighbors are barriers or not
              if self.row < self.all_rows - 1 and not grid[self.row + 1][self.col].is_wall():
                    self.neighbors.append(grid[self.row + 1][self.col])
                  # this goes up 
              if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
                    self.neighbors.append(grid[self.row - 1][self.col])
                  # this goes right in colums 
              if self.col < self.all_rows - 1 and not grid[self.row][self.col + 1].is_wall():
                    self.neighbors.append(grid[self.row][self.col + 1])
                  # this goes left in colums
              if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
                    self.neighbors.append(grid[self.row][self.col - 1])




        def __lt__ (self, other):
              return False
        
# this is the heuristic function 
# calculate the manhatten distance between 2 points
# uses the manhatten distatnce to traverse to end point 

def heuruistic(p1,p2):
     # split the up the x and y componets of each point  
      xa, ya = p1
      xb, yb = p2
      return abs(xa - xb) + abs(ya - yb)

# path building
def build_path(came_from, current, draw):
      while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

# our inplemented function
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  
    came_from = {}
    #g score is the shortest from start node to the current node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # predicted fistance from current node to end node 
    #uses the manhatten distance
    f_score = {node: float("inf") for row in grid for node in row} 
    f_score[start] = heuruistic(start.get_pos(), end.get_pos())
      # hash table consisting of the same itemes as priority queue 
      # lets us check what is in the priority queue 
    open_set_hash = {start}
    while not open_set.empty():
          for event in pygame.event.get():
                if event.type == pygame.QUIT:
                      pygame.quit()

          current = open_set.get()[2]  
          open_set_hash.remove(current)

          if current == end:
                build_path(came_from, end, draw)
                end.make_end()
                return True

          for neighbor in current.neighbors:
                # calculates g scores and updates g and f scores 
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                      came_from[neighbor] = current
                      g_score[neighbor] = temp_g_score
                      f_score[neighbor] = temp_g_score + heuruistic(neighbor.get_pos(), end.get_pos())
                      # checks out hash table to see if node is already in the priority queue
                      #adds it to both if it is not
                      if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.make_possible()
          draw()

          if current != start:
                current.make_looked()

    return False # if no path exists 





#  grid using our nodes 
def make_grid(rows, width):
    grid = []
    #spacing func
    gap = width // rows
    #horizontaal spacing beween nodes
    for i in range(rows):
        grid.append([])
    #vertical spacing between nodes
        for j in range(rows):
                node = Node(i, j, gap, rows)
                grid[i].append(node)
    return grid
 
 # make the grid lines in using pygame
def draw_grid(win, rows, width):
      gap = width // rows
      for i in range(rows):
            #draw horizontal 
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
            #draw vertical
                  pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# main draw function
def draw(win, grid, rows, width):
    # starts each fram with a white screen
      win.fill(WHITE)
      for row in grid:
            for node in row:
                 #draws a node in each posistion
                  node.draw(win)
      draw_grid(win, rows, width)
      pygame.display.update()

#Helper func to get most pos in y,x 
def get_push_pos(pos,rows,width):
      gap = width // rows
      y, x = pos

      row = y // gap
      col = x // gap

      return row, col


#main loopin func
def main(win,width):
      ROWS = 50
      grid = make_grid(ROWS,width)

      start = None
      end = None

      run = True
      
    #  game functinality loop 
      while run: 
            draw(win, grid, ROWS, width)
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                  
                  if pygame.mouse.get_pressed()[0]: # left click
                        pos = pygame.mouse.get_pos()
                        row, col = get_push_pos(pos, ROWS, width)
                        node = grid[row][col]
                        if not start and node != end:
                              start = node
                              start.make_start()
                        elif not end and node != start:
                              end = node
                              end.make_end()
                        elif node != end and node != start:
                              node.make_barrier()

                  elif pygame.mouse.get_pressed()[2]: # right click
                        pos = pygame.mouse.get_pos()
                        row, col = get_push_pos(pos, ROWS, width)
                        node = grid[row][col]
                        node.reset()
                        if node == start:
                              start = None
                        elif node == end:
                              end = None
                  
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and start and end :
                              for row in grid:
                                    for node in row:
                                          node.update_neigbors(grid)
                              algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                        if event.key == pygame.K_c:
                              start = None
                              end = None
                              grid = make_grid(ROWS, width)

                  
                              
                

      pygame.quit()
main(WIN, WIDTH)