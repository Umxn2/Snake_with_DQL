import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import testing
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pygame
import numpy as np
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))
num_episodes = 1000
class Snake():
    def __init__(self) -> None:
        pygame.font.init()
        self.score = 0
        #self.Score_test_font = pygame.font.Font(None, 50)
        #_text_surface = self.Score_test_font.render(f'Score: {self.score}', False, (255,255,255))
        self.Head = Node(random.randrange(50,250),random.randrange(50,250))
        self.Nodes = []
        self.Nodes.append(self.Head)
        self.x_dir = 0
        self.y_dir = 0
        
    def number_of_nodes(self):
        return len(self.Nodes)
    def direction_by_AI(self, x_direction, y_direction, action):
        direction_var = self.check_direction(x_direction, y_direction)
        keys = pygame.key.get_pressed()
        if action ==0:
            if direction_var != 'UP':
                y_direction = +1
                x_direction = 0
        if action==1:
            if direction_var != 'DOWN':
                y_direction = -1
                x_direction = 0
        if action==2:
            if direction_var != 'LEFT':
                y_direction = 0
                x_direction = 1
        if action==3:
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
    def check_direction_for_ai(self,x_dir, y_dir):
        if x_dir==0 and y_dir ==1:     
            direction = 0
        if x_dir==0 and y_dir ==-1:
            direction = 1
        if x_dir==1 and y_dir ==0:
            direction = 2
        if x_dir==-1 and y_dir ==0:
            direction = 3
        if x_dir==0 and y_dir ==0:
            direction =4
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
    Boundary1_surface_left = pygame.Surface((20,300))
    Boundary1_surface_left.fill("White")
    Boundary1_rect_left = Boundary1_surface_left.get_rect(topleft=(0,0))
    Boundary1_rect_right = Boundary1_surface_left.get_rect(topleft=(280,0))
    Boundary1_surface_up = pygame.Surface((300,20))
    Boundary1_surface_up.fill('White')
    Boundary1_rect_up = Boundary1_surface_up.get_rect(topleft=(0,0))
    Boundary1_rect_down = Boundary1_surface_up.get_rect(topleft=(0,280))
class Food():
    def __init__(self) -> None:
        self.x_pos =   random.randrange(50,250)
        self.y_pos = random.randrange(50,250)
        self.test_surface_Food1 = pygame.Surface((20,20))
        self.test_surface_Food1.fill('Green')
        self.test_rect = self.test_surface_Food1.get_rect(center =(self.x_pos, self.y_pos))
class laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Green'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10
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
def distances_from_wall(snek, boundary):
        dist_down_wall = boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-10
        
        distanace_up_wall = boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-10
        distance_left_wall = boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-10
        distance_right_wall = boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-10
        return dist_down_wall, distanace_up_wall, distance_left_wall, distance_right_wall
def distance_from_food(snek, food):
    distance_x = snek.Head.test_rect.center[0] - food.test_rect.center[0]
    distance_y = snek.Head.test_rect.center[1] - food.test_rect.center[1]
    return distance_x, distance_y   
class left_laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Blue'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
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
class right_laser():
    def __init__(self, snek, boundary, x_dir, y_dir) -> None:
        self.distance = 9999
        self.direction_of_head = snek.check_direction(x_dir, y_dir)
        if self.direction_of_head=="DOWN":
            self.size_of_laser = abs(boundary.Boundary1_rect_right.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10)
                    self.distance = nodes.test_rect.center[0]-snek.Head.test_rect.center[0]-10
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midleft =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="UP":
            self.size_of_laser = abs(boundary.Boundary1_rect_left.center[0]- snek.Head.test_rect.center[0]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.length, self.width))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midright =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="LEFT":
            self.size_of_laser = abs(boundary.Boundary1_rect_up.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance =nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midbottom =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
        if self.direction_of_head=="RIGHT":
            self.size_of_laser = abs(boundary.Boundary1_rect_down.center[1]- snek.Head.test_rect.center[1]-10)
            self.width = 1
            self.length = self.size_of_laser
            self.color = 'Yellow'
            self.laser_surface = pygame.Surface((self.width, self.length))
            self.laser_surface.fill(self.color)
            self.laser_rect = self.laser_surface.get_rect(midtop =(snek.Head.test_rect.center[0], snek.Head.test_rect.center[1]))
            for nodes in snek.Nodes[1:]:
                if self.laser_rect.colliderect(nodes.test_rect):
                    self.length = abs(nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10)
                    self.distance = nodes.test_rect.center[1]-snek.Head.test_rect.center[1]-10
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
class Snakegame():
    def __init__(self, snek) -> None:
        pygame.init() 
        vsync=30
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((300,300), pygame.NOFRAME, vsync= vsync) 
        self.Boundary1 = Boundaries()
        self.Food1 = Food()
        self.step_without_penalty = 0
        
    def get_state(self, snek):
        x_from_food, y_from_food = distance_from_food(snek, self.Food1)
        x_of_head, y_of_head = snek.Head.test_rect.center[0],snek.Head.test_rect.center[1]
        x_of_food, y_of_food = self.Food1.test_rect.center[0],self.Food1.test_rect.center[1]
        dist_from_down, dist_from_up, dist_from_left, dist_from_right = distances_from_wall(snek, self.Boundary1)
        eyes = laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
        left_eye = left_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir )
        right_eye = right_laser(snek, self.Boundary1, snek.x_dir, snek.y_dir)
        direction = snek.check_direction_for_ai(snek.x_dir, snek.y_dir)
        time = self.step_without_penalty
        state = [x_of_food, y_of_food, dist_from_up, dist_from_down,dist_from_left, dist_from_right, eyes.distance, left_eye.distance, right_eye.distance, direction, time, x_of_head, y_of_head]
        state = np.array(state) 
        return state 
    def game(self, snek):
        actions_set = [0,1,2,3]
        actions_set = np.array(actions_set)
        old_score = 0
        for episode in range(num_episodes):
            file1 = open('score.txt', 'a')
            
            L = f"score for episode {episode-1} : {old_score} \n"
            file1.writelines(L)
            file1.close()

            old_fitness_function = 0
            fitness_function  = 0
            time_penalty = 0
            steps_done = 0
            warning = 0
            state = self.get_state(snek)
            old_score = 0
            self.step_without_penalty= 0

            
            
            
            state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            old_x_from_food, old_y_from_food = 999,999
            while True:
                print(episode)
                sample = random.random()
                eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done * episode / EPS_DECAY)
                steps_done += 1
                if sample > eps_threshold:
                    with torch.no_grad():
                       
                        action = policy_net(state).max(1).indices.view(1, 1)
                        print('exploiting')
                else:
                    action = torch.tensor([[random.randint(0,3)]], device=device, dtype=torch.long)
                    print('exploring')
                time_penalty= time_penalty + 0.000001
                self.step_without_penalty = self.step_without_penalty +1

                self.count = 0
                for i in range(1, len(snek.Nodes)):
                    snek.Nodes[i].x_node_pos = positions_x[self.count]
                    snek.Nodes[i].y_node_pos = positions_y[self.count]
                    snek.Nodes[i].test_rect = snek.Nodes[i].test_surface.get_rect(center =(snek.Nodes[i].x_node_pos, snek.Nodes[i].y_node_pos))
                    self.count += 1
            
                snek.x_dir, snek.y_dir = snek.direction_by_AI( snek.x_dir, snek.y_dir, action)
                snek.direction_var = snek.check_direction(snek.x_dir, snek.y_dir)
                if snek.x_dir==0 and snek.y_dir ==1:     
                    snek.Head.test_rect.top+=10
                if snek.x_dir==0 and snek.y_dir ==-1:
                    snek.Head.test_rect.top+=-10
                    
                if snek.x_dir==1 and snek.y_dir ==0:
                    snek.Head.test_rect.left+=10
                    
                if snek.x_dir==-1 and snek.y_dir ==0:
                    snek.Head.test_rect.left+=-10
                x_from_food, y_from_food = distance_from_food(snek, self.Food1)
                if(abs(x_from_food)>abs(old_x_from_food) or abs(y_from_food)>abs(old_y_from_food)):
                    fitness_function=fitness_function - 0.009
                old_x_from_food =  x_from_food
                old_y_from_food = y_from_food
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
                #self.screen.blit(snek.Score_text_surface,(50, 50))
                if (snek.Head.test_rect.colliderect(self.Food1.test_rect)):
                    snek.score = snek.score +1
                    del self.Food1
                    #snek.Score_test_font = pygame.font.Font(None, 50)
                    #snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                    self.Food1 = Food()
                    end = snek.number_of_nodes()
                    Node2 = Node(positions_x[end-1],positions_y[end-1])
                    snek.Nodes.append(Node2)
                    self.screen.blit(self.Food1.test_surface_Food1,self.Food1.test_rect )
                    fitness_function = fitness_function + 14
                    time_penalty = 0
                    self.step_without_penalty = 0
                if (snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_right)or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_left) or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_up) or snek.Head.test_rect.colliderect(self.Boundary1.Boundary1_rect_down) ):
                    
                    old_score = old_score+snek.score
                    
                    del snek
                    snek = Snake()
                    snek.score = 0
                    #snek.Score_test_font = pygame.font.Font(None, 50)
                    #snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                    snek.x_dir = 0
                    snek.y_dir = 0
                    fitness_function = fitness_function -15
                    warning = warning +1
                    
                    
                    if(warning%20)==0:
                        warning = 0
                        break
                # for i in range(len(snek.Nodes)-1):
                #     for j in range(len(snek.Nodes)-1):
                #         if i!=j:
                #             if(snek.Nodes[i].test_rect.colliderect(snek.Nodes[j].test_rect)):
                               
                #                 old_score = old_score+snek.score
                                
                #                 del snek
                #                 snek = Snake()
                #                 snek.score = 0
                #                 snek.Score_test_font = pygame.font.Font(None, 50)
                #                 snek.Score_text_surface = snek.Score_test_font.render(f'Score: {snek.score}', False, (255,255,255))
                #                 snek.x_dir = 0
                #                 snek.y_dir = 0
                #                 fitness_function = fitness_function -5
                #                 warning = warning + 1
                                
                #                 if(warning%20)==0:
                #                     warning = 0
                #                     break
                #                 break 
                fitness_function = fitness_function - time_penalty
                pygame.display.update()
                self.clock.tick(20)
                positions_x = []
                positions_y = []
                for nodes in snek.Nodes:
                    positions_x.append(nodes.test_rect.center[0])
                    positions_y.append(nodes.test_rect.center[1])
                observation = self.get_state(snek)
                reward = fitness_function - old_fitness_function
                old_fitness_function = fitness_function
                reward = torch.tensor([reward], device=device)
                next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)
                memory.push(state, action, next_state, reward)
                state = next_state
                optimize_model()
                target_net_state_dict = target_net.state_dict()
                policy_net_state_dict = policy_net.state_dict()
                for key in policy_net_state_dict:
                    target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
                    target_net.load_state_dict(target_net_state_dict)
                print(reward)
                print(len(memory))
                

                if(len(memory)==12999):
                    some_random = random.random()
                    if(some_random>0.2):
                        for i in range(len(memory)-1):
                            if(abs((memory.memory[i].reward)))<2:
                                memory.memory.rotate(i)
                                memory.memory.popleft()
                                memory.memory.rotate(i)
                                break
                    else:
                        memory.memory.popleft()
                    
              
class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))
    

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    # def print_som(self):
    #     return self.memory[0]
    def __len__(self):
        return len(self.memory)
class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 1024)
        self.layer2 = nn.Linear(1024, 1024)
        self.layer3 = nn.Linear(1024, n_actions)
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)
BATCH_SIZE = 1024
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 2000
TAU = 0.005
LR = 1e-4
actions_set = [0,1,2,3]
n_actions = len(actions_set)
n_observations = 13
policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())
optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(13000)
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1).values


    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()
    
if __name__ == "__main__":
    snek = Snake()
    game_played = Snakegame(snek)
    game_played.game(snek)
