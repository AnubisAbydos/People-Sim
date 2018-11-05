"""
Project Name: 
File Name: 
Author: Lex Hall
Last Updated: 
Python Version: 2.7
Pygame Version: 1.9.1.win32-py2.7
"""

import pygame
from random import *
import Constants as const


class Map(object):
    def __init__(self, screen):
        self.screen = screen
        self.foodCells = []
        for i in xrange(5):
            self.spawnFood()
        print(self.foodCells)

    def spawnFood(self):
        x = randint(10,70)
        y = randint(10,70)
        self.foodCells.append((x,y))

    def tick(self):
        self.draw()

    def draw(self):
        for food in self.foodCells:
            rect = pygame.Rect((food[0] * const.PIXELSIZE) - const.PIXELSIZE/2,
                               (food[1] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                const.PIXELSIZE, const.PIXELSIZE)
            self.screen.fill((255,255,0), rect)

    def isCellFood(self, coords):
        return coords in self.foodCells