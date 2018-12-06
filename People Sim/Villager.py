"""
Project Name: People Sim
File Name: Villager.py
Author: Lex Hall
Last Updated: 12-6-2018
Python Version: 3.6
Pygame Version: 1.9.3
"""

import pygame
import math
from random import *
import Constants as const
from Enums import *

class Villager(object):
    def __init__(self, screen, count):
        self.screen = screen
        self.textFont = pygame.font.SysFont("Comic Sans MS", 10)
        self.bodyColor = const.WHITE
        self.headColor = const.SKINTONE
        self.stateText = "NULL"
        self.xGridPos = randint(1, const.GAME_XCELLS - 5)
        self.yGridPos = randint(1, const.GAME_YCELLS - 5)
        self.xActual = self.xGridPos * const.PIXELSIZE
        self.yActual = self.yGridPos * const.PIXELSIZE
        self.state = VillagerState.idle
        self.mood = VillagerMood.content
        self.name = "Villager " + str(count)
        self.foodValue = randint(5,15)
        self.foodDecayCount = 0
        self.woodValue = 5
        self.tickCount = 0

        self.goToLocation = (1, 1)
        self.isTargetReached = False
        self.idleTargetSet = False

        self.searchLoop = -1 
        self.lookingTile = (0 ,0)

        self.isSelected = False

    ### Tick: Called every game tick
    def tick(self, mapController):
        if self.state != VillagerState.dead:
            # Update tick counter
            self.tickCount += 1
            if self.tickCount == 61:
                self.tickCount = 1
            # Update Villager
            self.update(mapController)

        # Draw Villager
        self.draw()


    ### Update: updates villager state
    def update(self, mapController):
        # Increment food decay counter
        self.foodDecayCount += 1

        # Decrement villager food every 10 seconds (appx. when running near full FPS)
        if self.foodDecayCount == const.FRAMERATE * 10:
            self.foodValue -= 1
            if self.foodValue <= 5:
                self.state == VillagerState.idle
            # Reset food decay counter
            self.foodDecayCount = 0

        # If Villager runs out of food he dies
        if self.foodValue == 0:
            self.state = VillagerState.dead

        # STATE = DEAD
        if self.state == VillagerState.dead:
            self.mood = VillagerMood.dead

        if self.state == VillagerState.selected:
            pass

        # STATE = IDLE
        elif self.state == VillagerState.idle:
            # If food low look for food
            if self.foodValue <= 5:
                self.state = VillagerState.searchingForFood
                self.mood = VillagerMood.sad
            # If building needs to be built
            elif mapController.isBuildingReadyToBuild():
                if self.woodValue == 0:
                    self.state = VillagerState.searchingForWood
                    self.mood = VillagerMood.sad
                else:
                    self.state = VillagerState.building
                    self.mood = VillagerMood.working
            # Random wander walk set up
            elif not self.isTargetReached and not self.idleTargetSet and randint(0, 100) < 1:
                while True:
                    x = self.xGridPos + randint(-4, 4)
                    if x < const.GAME_XCELLS - 1 and x > 1:
                        break
                while True:
                    y = self.yGridPos + randint(-4, 4)
                    if y < const.GAME_YCELLS - 1 and y > 1:
                        break
                self.goToLocation = (x, y)
                self.idleTargetSet = True
            elif self.idleTargetSet and self.tickCount % 2 == 0:
                self.isTargetReached = self.moveToTarget()
                if self.isTargetReached:
                    self.idleTargetSet = False
                    self.isTargetReached = False


        # STATE = SEARCHING FOR FOOD
        elif self.state == VillagerState.searchingForFood:
            if self.searchLoop == -1:
                self.searchLoop = 1
                # Passed bools indicate type of search
                if self.lookForTile(mapController, True, False):
                    self.state = VillagerState.moving
                    self.mood = VillagerMood.angry
                    self.goToLocation = self.lookingTile
                    self.searchLoop = -1
            else:
                if self.tickCount == const.FRAMERATE / 4:
                    self.searchLoop += 1
                    self.tickCount = 0
                    # Passed bools indicate type of search
                    if self.lookForTile(mapController, True, False):
                        self.state = VillagerState.moving
                        self.mood = VillagerMood.angry
                        self.goToLocation = self.lookingTile
                        self.searchLoop = -1

        # STATE = SEARCHING FOR WOOD
        elif self.state == VillagerState.searchingForWood:
            if self.searchLoop == -1:
                self.searchLoop = 1
                # Passed bools indicate type of search
                if self.lookForTile(mapController, False, True):
                    self.state = VillagerState.moving
                    self.mood = VillagerMood.working
                    self.goToLocation = self.lookingTile
                    self.searchLoop = -1
            else:
                if self.tickCount == const.FRAMERATE / 4:
                    self.searchLoop += 1
                    self.tickCount = 0
                    # Passed bools indicate type of search
                    if self.lookForTile(mapController, False, True):
                        self.state = VillagerState.moving
                        self.mood = VillagerMood.working
                        self.goToLocation = self.lookingTile
                        self.searchLoop = -1

        # STATE = MOVING
        elif self.state == VillagerState.moving:
            self.isTargetReached = self.moveToTarget()
            if self.isTargetReached and self.mood == VillagerMood.angry:
                self.state = VillagerState.eating
                self.mood = VillagerMood.happy
            elif self.isTargetReached and self.mood == VillagerMood.working:
                self.state = VillagerState.harvesting

        # STATE = FORCEMOVING
        elif self.state == VillagerState.forceMove:
            self.isTargetReached = self.moveToTarget()
            if self.isTargetReached:
                self.isTargetReached = False
                self.state = VillagerState.idle
                self.mood = VillagerMood.content

        # STATE = HARVESTING
        elif self.state == VillagerState.harvesting:
            if self.tickCount == const.FRAMERATE and self.woodValue < 5 and mapController.woodTiles[self.goToLocation].getWoodValue() > 0:
                self.woodValue += 1
                mapController.woodTiles[self.goToLocation].decrementWoodValue()
            elif self.woodValue == 5 or mapController.woodTiles[self.goToLocation].getWoodValue() <= 0:
                self.isTargetReached = False
                self.idleTargetSet = False
                self.state = VillagerState.building

        # STATE = EATING
        elif self.state == VillagerState.eating:
            if self.tickCount == const.FRAMERATE and self.foodValue < 18 and mapController.foodTiles[self.goToLocation].getFoodValue() > 0:
                self.foodValue += 1
                mapController.foodTiles[self.goToLocation].decrementFoodValue()
            elif self.foodValue == 18 or mapController.foodTiles[self.goToLocation].getFoodValue() <= 0:
                self.isTargetReached = False
                self.idleTargetSet = False
                self.state = VillagerState.idle
                self.mood = VillagerMood.content
            else:
                pass

        # STATE = BUILDING
        elif self.state == VillagerState.building:
            building = mapController.getBuildingReadyToBuild()
            if building:
                buildingCenter = building.getBuildLocation()
                if math.sqrt(pow((buildingCenter[0] - self.xGridPos), 2) + pow((buildingCenter[1] - self.yGridPos), 2)) > 10:
                    hypoSide = math.sqrt(pow((buildingCenter[0] - self.xGridPos), 2) + pow((buildingCenter[1] - self.yGridPos), 2))
                    bSide = buildingCenter[1] - self.yGridPos
                    angle = math.asin(bSide/hypoSide)
                    if self.xGridPos <= buildingCenter[0]:
                        newPointX = buildingCenter[0] - (5 * math.cos(angle))
                    else:
                        newPointX = buildingCenter[0] + (5 * math.cos(angle))
                    newPointY = buildingCenter[1] - (5 * math.sin(angle)) 
                    self.goToLocation = (round(newPointX), round(newPointY))
                self.isTargetReached = self.moveToTarget()
                if self.isTargetReached and self.woodValue != 0 and self.tickCount == const.FRAMERATE:
                    self.woodValue -= 1
                    building.inputWood()
                elif self.isTargetReached and self.woodValue == 0 and self.tickCount == const.FRAMERATE:
                    self.isTargetReached = False
                    self.state = VillagerState.idle
                    self.mood = VillagerMood.content
            else:
                self.isTargetReached = False
                self.state = VillagerState.idle
                self.mood = VillagerMood.content


        # STATE = STARVING
        elif self.state == VillagerState.starving:
            while True:
                x = self.xGridPos + randint(-2, 2)
                if x < const.GAME_XCELLS - 1 and x > 1:
                    break
            while True:
                y = self.yGridPos + randint(-2, 2)
                if y < const.GAME_YCELLS - 1 and y > 1:
                    break
            self.goToLocation = (x, y)
            self.idleTargetSet = True
            if self.idleTargetSet and self.tickCount % 4 == 0:
                self.isTargetReached = self.moveToTarget()
                if self.isTargetReached:
                    self.idleTargetSet = False
                    self.isTargetReached = False

        # Moods Color Assignment
        if self.mood == VillagerMood.content:
            self.bodyColor = const.WHITE
        elif self.mood == VillagerMood.sad:
            self.bodyColor = const.BLUE
        elif self.mood == VillagerMood.angry:
            self.bodyColor = const.RED
        elif self.mood == VillagerMood.happy:
            self.bodyColor = const.GREEN
        elif self.mood == VillagerMood.dead:
            self.headColor = const.GREENSKINTONE
            self.bodyColor = const.GREY
        elif self.mood == VillagerMood.panicked:
            self.bodyColor = const.YELLOW
        elif self.mood == VillagerMood.working:
            self.bodyColor = const.PURPLE

        # State Text Assignment
        if self.state == VillagerState.dead:
            self.stateText = "Villager is Dead"
        elif self.state == VillagerState.idle:
            self.stateText = "Villager is Idle"
        elif self.state == VillagerState.searchingForFood:
            self.stateText = "Villager is Searching for Food"
        elif self.state == VillagerState.searchingForWood:
            self.stateText = "Villager is Searching for Wood"
        elif self.state == VillagerState.moving:
            self.stateText = "Villager is Moving to Target"
        elif self.state == VillagerState.forceMove:
            self.stateText = "Villager is Obeying Move Order"
        elif self.state == VillagerState.eating:
            self.stateText = "Villager is Eating"
        elif self.state == VillagerState.building:
            self.stateText = "Villager is Building"
        elif self.state == VillagerState.starving:
            self.stateText = "Villager is Starving!"
        elif self.state == VillagerState.harvesting:
            self.stateText = "Villager is Harvesting"

    def draw(self):
        # Draw head and body
        pygame.draw.circle(self.screen, self.bodyColor, (self.xActual, self.yActual), 10)
        pygame.draw.circle(self.screen, self.headColor, (self.xActual, self.yActual), 6)

        if self.isSelected:
            length = len(self.stateText) * 5 + 10
            # White Box
            pygame.draw.rect(self.screen, const.WHITE, (self.xActual - length/2, self.yActual - 70, length, 45))
            # Villager Name
            self.screen.blit(self.textFont.render(str(self.stateText), True, const.BLACK),
                            (self.xActual - length/2 + 5, self.yActual - 70, length, 30))
            # Food Bar
            pygame.draw.rect(self.screen, const.GREEN,
                            (self.xActual - length/2 + 10, self.yActual - 53, self.foodValue * 3, 10))
            # Food Text
            self.screen.blit(self.textFont.render("Food Level", True, const.BLACK),
                             (self.xActual - length/2 + 10, self.yActual - 56, 70, 35))
            # Wood Bar
            pygame.draw.rect(self.screen, const.BROWN,
                            (self.xActual - length/2 + 10, self.yActual - 38, self.woodValue * 10, 10))
            # Wood Text
            self.screen.blit(self.textFont.render("Wood Level", True, const.BLACK),
                             (self.xActual - length/2 + 10, self.yActual - 41, 70, 35))


    def moveToTarget(self):
        # Move to X column and set appx xGridPos
        if self.xActual < self.goToLocation[0] * const.PIXELSIZE:
            self.xActual += 1
            self.xGridPos = int(round(self.xActual / const.PIXELSIZE))
        elif self.xActual > self.goToLocation[0] * const.PIXELSIZE:
            self.xActual -= 1
            self.xGridPos = int(round(self.xActual / const.PIXELSIZE))
        else:
            pass

        # Move to Y column and set appx yGridPos
        if self.yActual < self.goToLocation[1] * const.PIXELSIZE:
            self.yActual += 1
            self.yGridPos = int(round(self.yActual / const.PIXELSIZE))
        elif self.yActual > self.goToLocation[1] * const.PIXELSIZE:
            self.yActual -= 1
            self.yGridPos = int(round(self.yActual / const.PIXELSIZE))
        else:
            pass

        # Has Villager reached given target?
        if self.xActual == self.goToLocation[0] * const.PIXELSIZE and self.yActual == self.goToLocation[1] * const.PIXELSIZE:
            return True
        else:
            return False


    def lookForTile(self, mapController, isFoodSearch, isWoodSearch):
        # Set and Check first search location (1 up from start)
        if self.searchLoop == 1:
            self.lookingTile = (self.xGridPos, self.yGridPos - 1)
            if isFoodSearch:
                if mapController.isTileFood(self.lookingTile):
                    return True
            elif isWoodSearch:
                if mapController.isTileWood(self.lookingTile):
                    return True

        # Look 40 Tiles away if fail cancel search and update state and mood
        elif self.searchLoop >= 40:
            if isFoodSearch:
                self.state = VillagerState.starving
                self.mood = VillagerMood.panicked
                self.searchLoop = -1
                return False
            elif isWoodSearch:
                self.state = VillagerState.idle
                self.searchLoop = -1
                return False            
        
        # Right : move right from current location checking each spot
        for i in range((self.searchLoop * 2) - 1):
            self.lookingTile = (self.lookingTile[0] + 1, self.lookingTile[1])
            if isFoodSearch:
                if mapController.isTileFood(self.lookingTile):
                    return True
            elif isWoodSearch:
                if mapController.isTileWood(self.lookingTile):
                    return True

        # Down : move down from current location checking each spot
        for i in range(self.searchLoop * 2):
            self.lookingTile = (self.lookingTile[0], self.lookingTile[1] + 1)
            if isFoodSearch:
                if mapController.isTileFood(self.lookingTile):
                    return True
            elif isWoodSearch:
                if mapController.isTileWood(self.lookingTile):
                    return True

        # Left : move left from current location checking each spot
        for i in range(self.searchLoop * 2):
            self.lookingTile = (self.lookingTile[0] - 1, self.lookingTile[1])
            if isFoodSearch:
                if mapController.isTileFood(self.lookingTile):
                    return True
            elif isWoodSearch:
                if mapController.isTileWood(self.lookingTile):
                    return True

        # Up : move up from current location checking each spot
        for i in range((self.searchLoop * 2) + 1):
            self.lookingTile = (self.lookingTile[0], self.lookingTile[1] - 1)
            if isFoodSearch:
                if mapController.isTileFood(self.lookingTile):
                    return True
            elif isWoodSearch:
                if mapController.isTileWood(self.lookingTile):
                    return True
        # If chosen tile not found this loop return False
        return False
