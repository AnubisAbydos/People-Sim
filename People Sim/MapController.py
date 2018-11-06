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


class MapController(object):
    def __init__(self, screen):
        self.screen = screen
        self.foodCells = []
        self.woodCells = []
        for i in xrange(const.STARTSPAWNFOODSOURCES):
            self.spawnFood()
        for i in xrange(const.STARTSPAWNWOODSOURCES):
            self.spawnWood()

    def spawnFood(self):
        x = randint(1, const.GAME_XCELLS - 10)
        y = randint(1, const.GAME_YCELLS - 10)
        if (x,y) in self.foodCells or (x,y) in self.woodCells:
            self.spawnFood()
        else:
            self.foodCells.append((x,y))

    def spawnWood(self):
        x = randint(1, const.GAME_XCELLS - 10)
        y = randint(1, const.GAME_YCELLS - 10)
        if (x,y) in self.foodCells or (x,y) in self.woodCells:
            self.spawnWood()
        else:
            self.woodCells.append((x,y))

    def tick(self):
        self.draw()

    def draw(self):
        for food in self.foodCells:
            self.screen.fill(const.YELLOW, ((food[0] * const.PIXELSIZE) - const.PIXELSIZE/2,
                               (food[1] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                const.PIXELSIZE, const.PIXELSIZE))
        for wood in self.woodCells:
            self.screen.fill(const.BROWN, ((wood[0] * const.PIXELSIZE) - const.PIXELSIZE/2,
                               (wood[1] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                const.PIXELSIZE, const.PIXELSIZE))

    def isCellFood(self, coords):
        return coords in self.foodCells

    def isCellWood(self, coords):
        return coords in self.woodCells

    def checkAllCollision(self, coords):
        pass

    def drawMiniMap(self, screen, mapX, mapY):
        miniMap = pygame.Surface((const.MAP_WIDTH / 10, const.MAP_HEIGHT / 10))
        for food in self.foodCells:
            miniMap.fill(const.YELLOW, (food[0], food[1], 1, 1))
        for wood in self.woodCells:
            miniMap.fill(const.BROWN, (wood[0], wood[1], 1, 1))
        pygame.draw.rect(miniMap, const.RED, (mapX / 10, mapY / 10, 80,80), 2)
        pygame.draw.rect(miniMap, const.WHITE, (0,0,const.MAP_WIDTH / 10, const.MAP_HEIGHT / 10), 4)
        screen.blit(miniMap, (15, 15))