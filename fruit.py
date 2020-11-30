############################################################################
# Purpose : A very small,basic snake game
# Author : Caleb Mugisha, Kidus Mengitsu

############################################################################
try:
    import random
    import os
    import sys
    import time
    import pygame
    from pygame.locals import *
except ImportError as err:
    print (f"Could not load module. {err}")
    sys.exit(2)
    
from snake import Snake 

div = 20
size = 500
tileSize = size // div
fps = pygame.time.Clock()
difficulty = 15
mode = "on"

green = pygame.Color(35, 112, 56)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gray = pygame.Color(180, 180, 180)
red = pygame.Color(255, 0, 0)
global snake
snake = Snake()


# only 1 instance per game that is moved to a new random location when the snake head reaches it
class Fruit():
    """
    class containing the fruit properties

    """

    def __init__(self):
        self.pos = [-1, -1]
        self.color = red

    # spawns the fruit in a new position and makes sure it is not overlapping any part of the snake
    def spawn(self):
        while True:
            flag = False
            self.pos[0] = random.randint(0, div - 1)
            self.pos[1] = random.randint(0, div - 1)
            for seg in snake.tail:
                if seg.pos[0] == self.pos[0] and seg.pos[1] == self.pos[1]:
                    flag = True
                    
                pass
            else:
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos[0] * tileSize + 1, self.pos[1] * tileSize + 1, tileSize - 2, tileSize - 2))
