"""
Project Name: People Sim
File Name: Buildings.py
Author: Lex Hall
Last Updated: 11-13-2018
Python Version: 3.6
Pygame Version: 1.9.3
"""

import pygame
from random import *
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

    def update(self, mapController):
        self.buildingProgress = (self.currentWood * 100) / self.requiredWood
        if self.buildingProgress >= 100:
            self.isComplete = True

    def draw(self, gameMap):
        if not self.isComplete:
            pygame.draw.rect(gameMap, const.BROWN, self.rect, 3)
            pygame.draw.rect(gameMap, const.BROWN, (self.originXActual, self.originYActual + 100 - self.buildingProgress,
                                                    self.gridWidth * const.PIXELSIZE, self.buildingProgress))
        else:
            pygame.draw.rect(gameMap, const.DARKBROWN, self.rect)

    def getBuildLocation(self):
        return(self.originXGrid + 5, self.originYGrid + 5)

    def inputWood(self):
        self.currentWood += 1


class FarmHouse(VillageBuilding):

    def update(self, mapController):
        VillageBuilding.update(self, mapController)
        if self.isComplete:
            if randint(0,10000) == 1:
                newFood = self.getBuildLocation()
                if randint(0,1) == 0:
                    newFoodX = newFood[0] + randint(5,20)
                else:
                    newFoodX = newFood[0] - randint(5,20)
                if randint(0,1) == 0:
                    newFoodY = newFood[1] + randint(5,20)
                else:
                    newFoodY = newFood[1] - randint(5,20)
                mapController.spawnFood(newFoodX, newFoodY)

    def draw(self, gameMap):
        if not self.isComplete:
            pygame.draw.rect(gameMap, const.YELLOW, self.rect, 3)
            pygame.draw.rect(gameMap, const.YELLOW, (self.originXActual, self.originYActual + 100 - self.buildingProgress,
                                                    self.gridWidth * const.PIXELSIZE, self.buildingProgress))
        else:
            pygame.draw.rect(gameMap, const.DARKYELLOW, self.rect)