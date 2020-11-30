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


class Segment():
    def __init__(self, pos):
        self.pos = pos
        self.color = green

    def draw(self, surface, eyes=False):
        xPos = self.pos[0]
        yPos = self.pos[1]

        pygame.draw.rect(surface, self.color, (xPos * tileSize + 1, yPos * tileSize + 1, tileSize - 1, tileSize - 1))
        

# only 1 instance of this per game, holds the segment classes in the tail array
class Snake():
    def __init__(self):
        # creates the head instance, starts it in the center of the grid, and adds it to the tail array
        self.head = Segment([10, 10])
        self.tail = []
        self.tail.append(self.head)
        self.dir = 'stop'
        self.dead = False
        self.winner = False
        self.color = green

    # called when the game is replayed to set values back to their initial state
    def reset(self):
        self.head = Segment([10, 10])
        self.tail = []
        self.tail.append(self.head)
        self.dir = 'stop'
        self.dead = False
        self.winner = False

    # loops through each segment in the tail array and calls its draw method
    def draw(self, surface):
        for seg in self.tail:
            if seg == self.tail[0]:
                seg.draw(surface, True)
            else:
                seg.draw(surface)

    # moves the snake by popping off the last segment in the tail array,
    # changing its position to where the head just was,
    # and moving the head in the necessary direction.
    # With this method, only the head and the last tail segment are recalculated each frame
    def move(self, dir):
        lastHeadPos = self.head.pos
        last = self.tail.pop()
        last.pos = [lastHeadPos[0], lastHeadPos[1]]
        self.tail.insert(1, last)

        if dir == 'up':
            self.head.pos[1] -= 1
        if dir == 'down':
            self.head.pos[1] += 1
        if dir == 'left':
            self.head.pos[0] -= 1
        if dir == 'right':
            self.head.pos[0] += 1
        

    # checks if the snake head has hit its own tail or the wall if walls are on
    def checkDead(self):
        for seg in self.tail:
            if seg == self.head:
                pass
            else:
                if seg.pos[0] == self.head.pos[0] and seg.pos[1] == self.head.pos[1]:
                    self.dead = True
        # if wall mode is on, snake dies when head touches a wall, if not, snake comes out other side of board
        if mode == "on":
            if self.head.pos[0] >= div or self.head.pos[0] < 0 or self.head.pos[1] < 0 or self.head.pos[1] >= div:
                self.dead = True
        else:
            if self.head.pos[0] >= div:
                self.head.pos[0] = 0
            elif self.head.pos[0] < 0:
                self.head.pos[0] = div - 1
            elif self.head.pos[1] >= div:
                self.head.pos[1] = 0
            elif self.head.pos[1] < 0:
                self.head.pos[1] = div - 1

    # checks if the player has won, meaning filled the entire board with tail
    def checkWin(self):
        if len(self.tail) >= div * div:
            self.dead = True
            self.winner = True

    # spawns the fruit in a new location and adds a new tail segment at the end of the tail
    # by finding which direction around the current last tail segment is occupied by another tail
    # (meaning which direction the body is in) and adding a new segment opposite to that position
    def eatFruit(self):
        fruit = Fruit()
        fruit.spawn()

        # if it is the first tail segment, location is chosen based on the direction of the head instead
        if len(self.tail) == 1:
            if self.dir == 'up':
                firstX = self.head.pos[0]
                firstY = self.head.pos[1] + 1
            elif self.dir == 'down':
                firstX = self.head.pos[0]
                firstY = self.head.pos[1] - 1
            elif self.dir == 'left':
                firstX = self.head.pos[0] + 1
                firstY = self.head.pos[1]
            elif self.dir == 'right':
                firstX = self.head.pos[0] - 1
                firstY = self.head.pos[1]
            self.tail.append(Segment([firstX, firstY]))
        else:
            if self.tail[-1].pos[0] - 1 == self.tail[-2].pos[0]:
                newX = self.tail[-1].pos[0] + 1
                newY = self.tail[-1].pos[1]
            elif self.tail[-1].pos[0] + 1 == self.tail[-2].pos[0]:
                newX = self.tail[-1].pos[0] - 1
                newY = self.tail[-1].pos[1]
            elif self.tail[-1].pos[1] - 1 == self.tail[-2].pos[1]:
                newX = self.tail[-1].pos[0]
                newY = self.tail[-1].pos[1] + 1
            elif self.tail[-1].pos[1] + 1 == self.tail[-2].pos[1]:
                newX = self.tail[-1].pos[0]
                newY = self.tail[-1].pos[1] - 1
            self.tail.append(Segment([newX, newY]))

# only 1 instance per game that is moved to a new random location when the snake head reaches it
class Fruit():
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
                    
            if flag:
                pass
            else:
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos[0] * tileSize + 1, self.pos[1] * tileSize + 1, tileSize - 2, tileSize - 2))



# create global instances of the snake and fruit classes and spawn the fruit in its first location
global snake, fruit
snake = Snake()
fruit = Fruit()
fruit.spawn()