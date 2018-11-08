"""
Project Name: 
File Name: 
Author: Lex Hall
Last Updated: 
Python Version: 2.7
Pygame Version: 1.9.1.win32-py2.7
"""

import pygame
import Constants as const

class VillageBuilding(object):
    def __init__(self, originXGrid, originYGrid):
        self.originXGrid = originXGrid
        self.originYGrid = originYGrid
        self.originXActual = self.originXGrid * const.PIXELSIZE - 5
        self.originYActual = self.originYGrid * const.PIXELSIZE - 5
        self.gridWidth = 10
        self.gridHeight = 10
        self.rect = pygame.Rect(self.originXActual, self.originYActual,
                                 self.gridWidth * const.PIXELSIZE, self.gridHeight * const.PIXELSIZE)
        self.buildingProgress = 0
        self.isComplete = False
        self.requiredWood = 50
        self.currentWood = 0
        self.buildLocationCount = -1

    def update(self):
        self.buildingProgress = (self.currentWood * 100) / self.requiredWood
        if self.buildingProgress == 100:
            self.isComplete = True

    def draw(self, gameMap):
        if not self.isComplete:
            pygame.draw.rect(gameMap, const.BROWN, self.rect, 3)
            pygame.draw.rect(gameMap, const.BROWN, (self.originXActual, self.originYActual + 100 - self.buildingProgress,
                                                    self.gridWidth * const.PIXELSIZE, self.buildingProgress))
        else:
            pygame.draw.rect(gameMap, const.DARKBROWN, self.rect)

    def getBuildLocation(self):
        return(self.originXGrid, self.originYGrid)

    def inputWood(self):
        self.currentWood += 1