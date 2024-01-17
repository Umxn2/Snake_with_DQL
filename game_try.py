import pygame
import random
from sys import exit
import neat
class Snake():
    def __init__(self) -> None:
        pygame.font.init()
        self.score = 0
        self.Score_test_font = pygame.font.Font(None, 50)
        self.Score_text_surface = self.Score_test_font.render(f'Score: {self.score}', False, (255,255,255))
        self.Head = Node(random.randrange(50,550),random.randrange(50,550))
        self.Nodes = []
        self.Nodes.append(self.Head)
        self.x_dir = 0
        self.y_dir = 0
        self.fitness_function  = 0
    def number_of_nodes(self):
        return len(self.Nodes)
    def direction_by_AI(self, x_direction, y_direction, action):
        direction_var = self.check_direction(x_direction, y_direction)
        keys = pygame.key.get_pressed()
        if action ==1:
            if direction_var != 'UP':
                y_direction = +1
                x_direction = 0
        if action==2:
            if direction_var != 'DOWN':
                y_direction = -1
                x_direction = 0
        if action==3:
            if direction_var != 'LEFT':
                y_direction = 0
                x_direction = 1
        if action==4:
            if direction_var != 'RIGHT':
                y_direction = 0
                x_direction = -1  
        return x_direction, y_direction

    def direction(self, x_direction, y_direction):
        direction_var = self.check_direction(x_direction, y_direction)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if direction_var != 'UP':
                y_direction = +1
                x_direction = 0
        if keys[pygame.K_UP]:
            if direction_var != 'DOWN':
                y_direction = -1
                x_direction = 0
        if keys[pygame.K_RIGHT]:
            if direction_var != 'LEFT':
                y_direction = 0
                x_direction = 1
        if keys[pygame.K_LEFT]:
            if direction_var != 'RIGHT':
                y_direction = 0
                x_direction = -1  
        return x_direction, y_direction
    def check_direction(self,x_dir, y_dir):
        if x_dir==0 and y_dir ==1:     
            direction = "DOWN"
        if x_dir==0 and y_dir ==-1:
            direction = "UP"
        if x_dir==1 and y_dir ==0:
            direction = "RIGHT"
        if x_dir==-1 and y_dir ==0:
            direction = "LEFT"
        if x_dir==0 and y_dir ==0:
            direction ="UNDEFINED"
        return direction
class Node():
    def check_collisions(self, wall):
        if(self.test_rect.colliderect(wall)):
            print("game_over")
    def __init__(self, x_pos, y_pos):
        self.x_node_pos = x_pos
        self.y_node_pos = y_pos
        self.x_size = 10  
        self.y_size = 10
        self.x_vel = 0
        self.y_vel = 0
        self.color = "Red"
        self.test_surface = pygame.Surface((self.x_size,self.y_size))
        self.test_surface.fill(self.color)
        self.test_rect = self.test_surface.get_rect(center =(self.x_node_pos, self.y_node_pos))
class Boundaries():
    Boundary1_surface_left = pygame.Surface((20,600))
    Boundary1_surface_left.fill("White")
    Boundary1_rect_left = Boundary1_surface_left.get_rect(topleft=(0,0))
    Boundary1_rect_right = Boundary1_surface_left.get_rect(topleft=(580,0))
    Boundary1_surface_up = pygame.Surface((600,20))
    Boundary1_surface_up.fill('White')
    Boundary1_rect_up = Boundary1_surface_up.get_rect(topleft=(0,0))
    Boundary1_rect_down = Boundary1_surface_up.get_rect(topleft=(0,580))
class Food():
    def __init__(self) -> None:
        self.x_pos =   random.randrange(50,550)
        self.y_pos = random.randrange(50,550)
        self.test_surface_Food1 = pygame.Surface((20,20))
        self.test_surface_Food1.fill('Green')
        self.test_rect = self.test_surface_Food1.get_rect(center =(self.x_pos, self.y_pos))


        
class laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UNDEFINED":
            self.size_of_laser = 1
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.x_node_pos, snek.Head.y_node_pos))
            self.distance = 9999
        
        #
        # (f"laser left:{self.length}")
def distances_from_wall(snek, boundary):
        dist_down_wall = boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-15
        
        distanace_up_wall = boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-15
        distance_left_wall = boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-15
        distance_right_wall = boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-15
        return dist_down_wall, distanace_up_wall, distance_left_wall, distance_right_wall
def distance_from_food(snek, food):
    distance_x = snek.Head.test_rect.center[0]- food.test_rect.center[0]
    distance_y = snek.Head.test_rect.center[1]- food.test_rect.center[1]
    return distance_x, distance_y


        
class left_laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UNDEFINED":
            self.size_of_laser = 1
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.x_node_pos, snek.Head.y_node_pos))
            self.distance = 9999
        #print(f"laser:{self.length}")

class right_laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance =nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-15)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-15
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UNDEFINED":
            self.size_of_laser = 1
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.x_node_pos, snek.Head.y_node_pos))
            self.distance = 9999
        #(f"laser right :{self.length}")

class Snakegame():
    def __init__(self, snek) -> None:
        pygame.init() 
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600,600)) 
        self.Boundary1 = Boundaries()
        self.Food1 = Food()
        self.Food2 = Food()
        self.Food3 = Food()
    def get_state(self, snek):
        x_from_food, y_from_food = distance_from_food(snek, self.Food1)
        dist_from_down, dist_from_up, dist_from_left, dist_from_right = distances_from_wall(snek, self.Boundary1)
        eyes = laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
        left_eye = left_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
        right_eye = right_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir)
        state = [x_from_food, y_from_food, dist_from_up, dist_from_down,dist_from_left, dist_from_right, eyes.distance, left_eye.distance, right_eye.distance]
        return state
        
    def game(self, snek):
        while True:
            self.count = 0
            for i in range(1, len(snek.Nodes)):

                
                snek.Nodes[i].x_node_pos = positions_x[self.count]
                snek.Nodes[i].y_node_pos = positions_y[self.count]
                snek.Nodes[i].test_rect = snek.Nodes[i].test_surface.get_rect(center =(snek.Nodes[i].x_node_pos, snek.Nodes[i].y_node_pos))
                self.count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
            snek.x_dir, snek.y_dir = snek.direction( snek.x_dir, snek.y_dir)
            snek.direction_var = snek.check_direction(snek.x_dir, snek.y_dir)
            if snek.x_dir==0 and snek.y_dir ==1:     
                snek.Head.test_rect.top+=10
            if snek.x_dir==0 and snek.y_dir ==-1:
                snek.Head.test_rect.top+=-10
                
            if snek.x_dir==1 and snek.y_dir ==0:
                snek.Head.test_rect.left+=10
                
            if snek.x_dir==-1 and snek.y_dir ==0:
                snek.Head.test_rect.left+=-10
            old_x_from_food, old_y_from_food = 999,999
            x_from_food, y_from_food = distance_from_food(snek, self.Food1)
            if(x_from_food>old_x_from_food and y_from_food>old_y_from_food):
                snek.fitness_function=snek.fitness_function + 0.01
            else:
                snek.fitness_function=snek.fitness_function - 0.01    
            self.screen.fill('Black')
            self.eyes = laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
            self.left_eye = left_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
            self.right_eye = right_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir)
            for i in range(len(snek.Nodes)):
                self.screen.blit(snek.Nodes[i].test_surface, snek.Nodes[i].test_rect)
            self.screen.blit(self.eyes.laser_surface, self.eyes.laser_rect)
            self.screen.blit(self.left_eye.laser_surface, self.left_eye.laser_rect)
            self.screen.blit(self.right_eye.laser_surface, self.right_eye.laser_rect)
            self.screen.blit(self.Boundary1.Boundary1_surface_left, self.Boundary1.Boundary1_rect_left)
            self.screen.blit(self.Boundary1.Boundary1_surface_left, self.Boundary1.Boundary1_rect_right)
            self.screen.blit(self.Boundary1.Boundary1_surface_up, self.Boundary1.Boundary1_rect_up)
            self.screen.blit(self.Boundary1.Boundary1_surface_up, self.Boundary1.Boundary1_rect_down)
            self.screen.blit(self.Food1.test_surface_Food1,self.Food1.test_rect)
            self.screen.blit(self.Food2.test_surface_Food1,self.Food2.test_rect)
            self.screen.blit(self.Food3.test_surface_Food1,self.Food3.test_rect)

            self.screen.blit(snek.Score_text_surface,(50, 50))
            if (snek.Head.test_rect.colliderect(self.Food1.test_rect)):
                snek.score = snek.score +1
                del self.Food1
                snek.Score_test_font = pygame.font.Font(None, 50)
                snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                self.Food1 = Food()
                end = snek.number_of_nodes()
                Node2 = Node(positions_x[end-1],positions_y[end-1])
                snek.Nodes.append(Node2)
                self.screen.blit(self.Food1.test_surface_Food1,self.Food1.test_rect )
            if (snek.Head.test_rect.colliderect(self.Food2.test_rect)):
                snek.score = snek.score +1
                snek.Score_test_font = pygame.font.Font(None, 50)
                snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                self.Food2 = Food()
                end = snek.number_of_nodes()
                Node2 = Node(positions_x[end-1],positions_y[end-1])
                snek.Nodes.append(Node2)
                self.screen.blit(self.Food2.test_surface_Food1,self.Food2.test_rect )
            if (snek.Head.test_rect.colliderect(self.Food3.test_rect)):
                snek.score = snek.score +1
                del self.Food3
                snek.Score_test_font = pygame.font.Font(None, 50)
                snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                self.Food3 = Food()
                end = snek.number_of_nodes()
                Node2 = Node(positions_x[end-1],positions_y[end-1])
                snek.Nodes.append(Node2)
                self.screen.blit(self.Food3.test_surface_Food1,self.Food3.test_rect )
            if (snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_right)or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_left) or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_up) or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_down) ):
                self.score = 0
                del snek
                snek = Snake()
                snek.score = 0
                snek.Score_test_font = pygame.font.Font(None, 50)
                snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
            
                snek.x_dir = 0
                snek.y_dir = 0
                snek.fitness_function =-1
                
            for i in range(len(snek.Nodes)-1):
                for j in range(len(snek.Nodes)-1):
                    if i!=j:
                        if(snek.Nodes[i].test_rect.colliderect(snek.Nodes[j].test_rect)):
                            
                            self.score = 0
                            del snek
                            snek = Snake()
                            snek.score = 0
                            snek.Score_test_font = pygame.font.Font(None, 50)
                            snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
            
                            snek.x_dir = 0
                            snek.y_dir = 0
                            snek.fitness_function = -1
                            break            
            pygame.display.update()
            self.clock.tick(30)
            positions_x = []
            positions_y = []
            for nodes in snek.Nodes:
                positions_x.append(nodes.test_rect.center[0])
                positions_y.append(nodes.test_rect.center[1])
            print(self.get_state(snek))
        

snek = Snake()
game_played = Snakegame(snek)
game_played.game(snek)