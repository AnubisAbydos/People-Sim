"""
Project Name: 
File Name: 
Author: Lex Hall
Last Updated: 
Python Version: 2.7
Pygame Version: 1.9.1.win32-py2.7
"""

import pygame
import datetime
from random import *
import heapq
import Constants as const
from Enums import *



class Villager(object):
    def __init__(self, screen):
        self.screen = screen
        self.bodyColor = const.WHITE
        self.headColor = const.SKINTONE
        self.xGridPos = randint(1,79)
        self.yGridPos = randint(1,79)
        self.xActual = self.xGridPos * const.PIXELSIZE
        self.yActual = self.yGridPos * const.PIXELSIZE
        self.state = VillagerState.idle
        self.mood = VillagerMood.content
        self.name = "Jim"
        self.foodValue = randint(5,10)
        self.foodDecayCount = 0
        self.tickCount = 0
        
        self.goToLocation = (1, 1)
        self.isTargetReached = False
        self.idleTargetSet = False

        self.foodLoop = -1 
        self.lookingCell = (0 ,0)


    def tick(self, map):
        self.tickCount += 1
        if self.tickCount == 61:
            self.tickCount = 1
        self.update(map)
        self.draw()


    def update(self, map):
        self.foodDecayCount += 1
        if self.foodDecayCount == const.FRAMERATE * 10:
            self.foodValue -= 1
            self.foodDecayCount = 0
        if self.foodValue == 0:
            self.state = VillagerState.dead
            pass

        if self.state == VillagerState.dead:
            self.mood = VillagerMood.dead

        elif self.state == VillagerState.idle:
            if self.foodValue <= 5:
                self.state = VillagerState.searching
                self.mood = VillagerMood.sad
            elif not self.isTargetReached and not self.idleTargetSet:
                while True:
                    x = self.xGridPos + randint(-4, 4)
                    if x < 79 and x > 1:
                        break
                while True:
                    y = self.yGridPos + randint(-4, 4)
                    if y < 79 and y > 1:
                        break
                self.goToLocation = (x, y)
                self.idleTargetSet = True
            elif self.idleTargetSet and self.tickCount % 2 == 0:
                self.isTargetReached = self.moveToTarget()
                if self.isTargetReached:
                    self.idleTargetSet = False
                    self.isTargetReached = False


        elif self.state == VillagerState.searching:
            if self.foodLoop == -1:
                self.foodLoop = 1
                if self.lookForFood(map):
                    self.state = VillagerState.moving
                    self.goToLocation = self.lookingCell
                    self.foodLoop = -1
            else:
                if self.tickCount == const.FRAMERATE / 4:
                    self.foodLoop += 1
                    self.tickCount = 0
                    if self.lookForFood(map):
                        self.state = VillagerState.moving
                        self.mood = VillagerMood.angry
                        self.goToLocation = self.lookingCell
                        self.foodLoop = -1

        elif self.state == VillagerState.moving:
            self.isTargetReached = self.moveToTarget()
            if self.isTargetReached:
                self.state = VillagerState.eating
                self.mood = VillagerMood.happy

        elif self.state == VillagerState.eating:
            if self.tickCount == const.FRAMERATE and self.foodValue < 20:
                self.foodValue += 1
            elif self.foodValue == 20:
                self.state = VillagerState.idle
                self.mood = VillagerMood.content
            else:
                pass

        elif self.state == VillagerState.building:
            pass

        elif self.state == VillagerState.starving:
            while True:
                x = self.xGridPos + randint(-2, 2)
                if x < 79 and x > 1:
                    break
            while True:
                y = self.yGridPos + randint(-2, 2)
                if y < 79 and y > 1:
                    break
            self.goToLocation = (x, y)
            self.idleTargetSet = True
            if self.idleTargetSet and self.tickCount % 4 == 0:
                self.isTargetReached = self.moveToTarget()
                if self.isTargetReached:
                    self.idleTargetSet = False
                    self.isTargetReached = False

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
        pygame.draw.circle(self.screen, self.bodyColor, (self.xActual, self.yActual), 10)
        pygame.draw.circle(self.screen, self.headColor, (self.xActual, self.yActual), 6)

    def moveToTarget(self):
        if self.xActual < self.goToLocation[0] * const.PIXELSIZE:
            self.xActual += 1
            self.xGridPos = int(round(self.xActual / const.PIXELSIZE))
        elif self.xActual > self.goToLocation[0] * const.PIXELSIZE:
            self.xActual -= 1
            self.xGridPos = int(round(self.xActual / const.PIXELSIZE))
        else:
            pass
        if self.yActual < self.goToLocation[1] * const.PIXELSIZE:
            self.yActual += 1
            self.yGridPos = int(round(self.yActual / const.PIXELSIZE))
        elif self.yActual > self.goToLocation[1] * const.PIXELSIZE:
            self.yActual -= 1
            self.yGridPos = int(round(self.yActual / const.PIXELSIZE))
        else:
            pass
        if self.xActual == self.goToLocation[0] * const.PIXELSIZE and self.yActual == self.goToLocation[1] * const.PIXELSIZE:
            return True
        else:
            return False

    def lookForFood(self, map):
        if self.foodLoop == 1:
            self.lookingCell = (self.xGridPos, self.yGridPos - 1)
            if  map.isCellFood(self.lookingCell):
                return True
        elif self.foodLoop >= 80:
            self.state = VillagerState.starving
            self.mood = VillagerMood.panicked
            return False
        
        for i in xrange((self.foodLoop * 2) - 1):
            if self.lookingCell[0] < 79:
                self.lookingCell = (self.lookingCell[0] + 1, self.lookingCell[1])
                if  map.isCellFood(self.lookingCell):
                    return True
            else:
                break

        for i in xrange(self.foodLoop * 2):
            if self.lookingCell[1] < 79:
                self.lookingCell = (self.lookingCell[0], self.lookingCell[1] + 1)
                if  map.isCellFood(self.lookingCell):
                    return True
            else:
                break

        for i in xrange(self.foodLoop * 2):
            if self.lookingCell[0] > 1:
                self.lookingCell = (self.lookingCell[0] - 1, self.lookingCell[1])
                if  map.isCellFood(self.lookingCell):
                    return True
            else:
                break

        for i in xrange((self.foodLoop * 2) + 1):
            if self.lookingCell[1] > 1:
                self.lookingCell = (self.lookingCell[0], self.lookingCell[1] - 1)
                if  map.isCellFood(self.lookingCell):
                    return True
            else:
                break
        return False
