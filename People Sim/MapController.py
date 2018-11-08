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
import Buildings
import Constants as const


class MapController(object):
    def __init__(self, gameMap, screen):
        self.gameMap = gameMap
        self.screen = screen
        self.foodTiles = {}
        self.woodTiles = {}
        self.buildings = []
        self.mapX = 400
        self.mapY = 400
        self.textFont = pygame.font.SysFont("Comic Sans MS", 10)
        for i in xrange(const.STARTSPAWNFOODSOURCES):
            self.spawnFood()
        for i in xrange(const.STARTSPAWNWOODSOURCES):
            self.spawnWood()

    def spawnFood(self):
        x = randint(1, const.GAME_XCELLS - 10)
        y = randint(1, const.GAME_YCELLS - 10)
        if (x,y) in self.foodTiles or (x,y) in self.woodTiles:
            self.spawnFood()
        else:
            self.foodTiles[x, y] = FoodTile(x, y)

    def spawnWood(self):
        x = randint(1, const.GAME_XCELLS - 10)
        y = randint(1, const.GAME_YCELLS - 10)
        if (x,y) in self.foodTiles or (x,y) in self.woodTiles:
            self.spawnWood()
        else:
            self.woodTiles[x, y] = WoodTile(x, y)

    def spawnBuilding(self, mousePos):
        mouseActualPos = (mousePos[0] + self.mapX, mousePos[1] + self.mapY)
        xGridPos = int(round(mouseActualPos[0] / const.PIXELSIZE))
        yGridPos = int(round(mouseActualPos[1] / const.PIXELSIZE))
        self.buildings.append(Buildings.VillageBuilding(xGridPos, yGridPos))

    def handleScrolling(self, keys, mousePos):
        if keys[pygame.K_UP]:
            self.mapY -= 5
        if keys[pygame.K_DOWN]:
            self.mapY += 5
        if keys[pygame.K_LEFT]:
            self.mapX -= 5
        if keys[pygame.K_RIGHT]:
            self.mapX += 5

        if mousePos[0] <= 0:
            self.mapX -= 10
        if mousePos[0] >= const.SCREEN_WIDTH - 1:
            self.mapX += 10
        if mousePos[1] <= 0:
            self.mapY -= 10
        if mousePos[1] >= const.SCREEN_HEIGHT - 1:
            self.mapY += 10

        if self.mapY > ((const.MAP_HEIGHT - const.SCREEN_HEIGHT) + 50):
            self.mapY = (const.MAP_HEIGHT - const.SCREEN_HEIGHT) + 50
        elif self.mapY < -50:
            self.mapY = -50
        if self.mapX > ((const.MAP_WIDTH - const.SCREEN_WIDTH) + 50):
            self.mapX = (const.MAP_WIDTH - const.SCREEN_WIDTH) + 50
        elif self.mapX < -50:
            self.mapX = -50

    def tick(self, buildingSelected, mousePos):
        self.updateTiles()
        for building in self.buildings:
            building.update()
        if buildingSelected:
            mouseActualPos = (mousePos[0] + self.mapX, mousePos[1] + self.mapY)
            xGridPos = int(round(mouseActualPos[0] / const.PIXELSIZE))
            yGridPos = int(round(mouseActualPos[1] / const.PIXELSIZE))
            pygame.draw.rect(self.gameMap, const.RED, (xGridPos * const.PIXELSIZE - 5, yGridPos * const.PIXELSIZE - 5, 100,100), 5)

    def updateTiles(self):
        for food in self.foodTiles:
            if self.foodTiles[food[0], food[1]].foodValue > 0:
                self.gameMap.fill(const.YELLOW, ((food[0] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                   (food[1] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                     const.PIXELSIZE, const.PIXELSIZE))

            if self.foodTiles[food[0], food[1]].isSelected == True and self.foodTiles[food[0], food[1]].foodValue > 0:
                # White Box
                pygame.draw.rect(self.gameMap, const.WHITE, ((food[0] * const.PIXELSIZE) - 50, (food[1] * const.PIXELSIZE) - 30, 100, 15))
                # Food remaining text
                self.gameMap.blit(self.textFont.render("Food Remaining: " + str(self.foodTiles[food[0], food[1]].foodValue), True, const.BLACK),
                                   ((food[0] * const.PIXELSIZE) - 48, (food[1] * const.PIXELSIZE) - 30, 100, 15))

        for wood in self.woodTiles:
            if self.woodTiles[wood[0], wood[1]].woodValue > 0:
                self.gameMap.fill(const.BROWN, ((wood[0] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                   (wood[1] * const.PIXELSIZE) - const.PIXELSIZE/2,
                                     const.PIXELSIZE, const.PIXELSIZE))
            if self.woodTiles[wood[0], wood[1]].isSelected == True and self.woodTiles[wood[0], wood[1]].woodValue > 0:
                # White Box
                pygame.draw.rect(self.gameMap, const.WHITE, ((wood[0] * const.PIXELSIZE) - 50, (wood[1] * const.PIXELSIZE) - 30, 100, 15))
                # Food remaining text
                self.gameMap.blit(self.textFont.render("Wood Remaining: " + str(self.woodTiles[wood[0], wood[1]].woodValue), True, const.BLACK),
                                   ((wood[0] * const.PIXELSIZE) - 48, (wood[1] * const.PIXELSIZE) - 30, 100, 15))

        for building in self.buildings:
            building.draw(self.gameMap)

    def drawMap(self):
        self.screen.blit(self.gameMap, (0, 0), (self.mapX, self.mapY, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.drawMiniMap()

    def isTileFood(self, coords):
        return coords in self.foodTiles

    def isTileWood(self, coords):
        return coords in self.woodTiles

    def isBuildingReadyToBuild(self):
        for building in self.buildings:
            if building != None and building.isComplete == False:
                return True
        return False

    def getBuildingReadyToBuild(self):
        for building in self.buildings:
            if not building.isComplete:
                return building
        return None

    def checkAllCollision(self, coords):
        xGrid = int(round(coords[0] / const.PIXELSIZE))
        yGrid = int(round(coords[1] / const.PIXELSIZE))
        for food in self.foodTiles:
            self.foodTiles[food[0], food[1]].isSelected = False
            if self.foodTiles[food[0], food[1]].gridX >= xGrid - 1 and self.foodTiles[food[0], food[1]].gridX <= xGrid + 1:
                if self.foodTiles[food[0], food[1]].gridY >= yGrid - 1 and self.foodTiles[food[0], food[1]].gridY <= yGrid + 1:
                    self.foodTiles[food[0], food[1]].isSelected = True
        for wood in self.woodTiles:
            self.woodTiles[wood[0], wood[1]].isSelected = False
            if self.woodTiles[wood[0], wood[1]].gridX >= xGrid - 1 and self.woodTiles[wood[0], wood[1]].gridX <= xGrid + 1:
                if self.woodTiles[wood[0], wood[1]].gridY >= yGrid - 1 and self.woodTiles[wood[0], wood[1]].gridY <= yGrid + 1:
                    self.woodTiles[wood[0], wood[1]].isSelected = True

    def deselectAllTiles(self):
        for food in self.foodTiles:
            self.foodTiles[food[0], food[1]].isSelected = False
        for wood in self.woodTiles:
            self.woodTiles[wood[0], wood[1]].isSelected = False

    def drawMiniMap(self):
        miniMap = pygame.Surface((const.MAP_WIDTH / 10, const.MAP_HEIGHT / 10))
        for food in self.foodTiles:
            if self.foodTiles[food[0], food[1]].foodValue > 0:
                miniMap.fill(const.YELLOW, (food[0], food[1], 1, 1))
        for wood in self.woodTiles:
            if self.woodTiles[wood[0], wood[1]].woodValue > 0:
                miniMap.fill(const.BROWN, (wood[0], wood[1], 1, 1))
        pygame.draw.rect(miniMap, const.RED, (self.mapX / 10, self.mapY / 10, 80,80), 2)
        pygame.draw.rect(miniMap, const.WHITE, (0,0,const.MAP_WIDTH / 10, const.MAP_HEIGHT / 10), 4)
        self.screen.blit(miniMap, (15, 15))




class FoodTile(object):
    def __init__(self, gridX, gridY):
        self.gridX = gridX
        self.gridY = gridY
        self.foodValue = const.FOODSPAWNAMOUNT
        self.isSelected = False

    def getFoodValue(self):
        return self.foodValue

    def decrementFoodValue(self):
        self.foodValue -= 1

class WoodTile(object):
    def __init__(self, gridX, gridY):
        self.gridX = gridX
        self.gridY = gridY
        self.woodValue = const.WOODSPAWNAMOUNT
        self.isSelected = False

    def getWoodValue(self):
        return self.woodValue

    def decrementWoodValue(self):
        self.woodValue -= 1