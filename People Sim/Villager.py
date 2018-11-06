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
from Enums import *

class Villager(object):
    def __init__(self, screen, count):
        self.screen = screen
        self.textFont = pygame.font.SysFont("Comic Sans MS", 10)
        self.bodyColor = const.WHITE
        self.headColor = const.SKINTONE
        self.xGridPos = randint(1, const.GAME_XCELLS - 5)
        self.yGridPos = randint(1, const.GAME_YCELLS - 5)
        self.xActual = self.xGridPos * const.PIXELSIZE
        self.yActual = self.yGridPos * const.PIXELSIZE
        self.state = VillagerState.idle
        self.mood = VillagerMood.content
        self.name = "Villager " + str(count)
        self.foodValue = randint(5,15)
        self.foodDecayCount = 0
        self.tickCount = 0

        self.goToLocation = (1, 1)
        self.isTargetReached = False
        self.idleTargetSet = False

        self.foodLoop = -1 
        self.lookingCell = (0 ,0)

        self.isSelected = False

    def tick(self, mapController):
        # Update tick counter
        self.tickCount += 1
        if self.tickCount == 61:
            self.tickCount = 1
        self.update(mapController)
        self.draw()


    def update(self, mapController):
        # Increment food decay counter
        self.foodDecayCount += 1

        # Decrement villager food every 10 seconds (appx. when running near full FPS)
        if self.foodDecayCount == const.FRAMERATE * 10:
            self.foodValue -= 1
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
            if self.foodValue <= 5:
                self.state = VillagerState.searching
                self.mood = VillagerMood.sad
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


        # STATE = SEARCHING
        elif self.state == VillagerState.searching:
            if self.foodLoop == -1:
                self.foodLoop = 1
                if self.lookForFood(mapController):
                    self.state = VillagerState.moving
                    self.goToLocation = self.lookingCell
                    self.foodLoop = -1
            else:
                if self.tickCount == const.FRAMERATE / 4:
                    self.foodLoop += 1
                    self.tickCount = 0
                    if self.lookForFood(mapController):
                        self.state = VillagerState.moving
                        self.mood = VillagerMood.angry
                        self.goToLocation = self.lookingCell
                        self.foodLoop = -1

        # STATE = MOVING
        elif self.state == VillagerState.moving:
            self.isTargetReached = self.moveToTarget()
            if self.isTargetReached:
                self.state = VillagerState.eating
                self.mood = VillagerMood.happy

        # STATE = FORCEMOVING
        elif self.state == VillagerState.forceMove:
            self.isTargetReached = self.moveToTarget()
            if self.isTargetReached:
                self.isTargetReached = False
                self.state = VillagerState.idle
                self.mood = VillagerMood.content

        # STATE = EATING
        elif self.state == VillagerState.eating:
            if self.tickCount == const.FRAMERATE and self.foodValue < 18:
                self.foodValue += 1
            elif self.foodValue == 18:
                self.isTargetReached = False
                self.idleTargetSet = False
                self.state = VillagerState.idle
                self.mood = VillagerMood.content
            else:
                pass

        # STATE = BUILDING
        elif self.state == VillagerState.building:
            pass

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


    def draw(self):
        # Draw head and body
        pygame.draw.circle(self.screen, self.bodyColor, (self.xActual, self.yActual), 10)
        pygame.draw.circle(self.screen, self.headColor, (self.xActual, self.yActual), 6)

        if self.isSelected:
            # White Box
            pygame.draw.rect(self.screen, const.WHITE, (self.xActual - 20, self.yActual - 50, 70, 30))
            # Villager Name
            self.screen.blit(self.textFont.render(str(self.name), True, const.BLACK),
                            (self.xActual - 17, self.yActual - 50, 70, 30))
            # Food Bar
            pygame.draw.rect(self.screen, const.GREEN,
                            (self.xActual - 10, self.yActual - 33, self.foodValue * 3, 10))
            # Food Text
            self.screen.blit(self.textFont.render("Food Level", True, const.BLACK),
                             (self.xActual - 10, self.yActual - 36, 70, 35))


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


    def lookForFood(self, mapController):
        # Set and Check first search location (1 up from start)
        if self.foodLoop == 1:
            self.lookingCell = (self.xGridPos, self.yGridPos - 1)
            if  mapController.isCellFood(self.lookingCell):
                return True

        # Look 40 cells away if fail cancel search and update state and mood
        elif self.foodLoop >= 40:
            self.state = VillagerState.starving
            self.mood = VillagerMood.panicked
            return False
        
        # Right : move right from current location checking each spot
        for i in xrange((self.foodLoop * 2) - 1):
            self.lookingCell = (self.lookingCell[0] + 1, self.lookingCell[1])
            if mapController.isCellFood(self.lookingCell):
                return True

        # Down : move down from current location checking each spot
        for i in xrange(self.foodLoop * 2):
            self.lookingCell = (self.lookingCell[0], self.lookingCell[1] + 1)
            if mapController.isCellFood(self.lookingCell):
                return True

        # Left : move left from current location checking each spot
        for i in xrange(self.foodLoop * 2):
            self.lookingCell = (self.lookingCell[0] - 1, self.lookingCell[1])
            if mapController.isCellFood(self.lookingCell):
                return True

        # Up : move up from current location checking each spot
        for i in xrange((self.foodLoop * 2) + 1):
            self.lookingCell = (self.lookingCell[0], self.lookingCell[1] - 1)
            if mapController.isCellFood(self.lookingCell):
                return True
        # If food not found this loop return False
        return False
