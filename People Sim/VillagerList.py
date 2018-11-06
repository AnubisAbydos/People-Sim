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
import Villager
from Enums import *
import Constants as const

class VillagerList(object):
    def __init__(self, screen, mapController):
        self.screen = screen
        self.mapController = mapController
        self.villagers = []
        for i in xrange(const.STARTSPAWNVILLAGERS):
            self.villagers.append(Villager.Villager(self.screen, i))

    def tick(self):
        for villager in self.villagers:
            villager.tick(self.mapController)

    def checkCollision(self, coords):
        xGrid = int(round(coords[0] / const.PIXELSIZE))
        yGrid = int(round(coords[1] / const.PIXELSIZE))
        for villager in self.villagers:
            villager.isSelected = False
            if villager.xGridPos >= xGrid - 1 and villager.xGridPos <= xGrid + 1:
                if villager.yGridPos >= yGrid - 1 and villager.yGridPos <= yGrid + 1:
                    villager.isSelected = True

    def forceMove(self, coords):
        xGrid = int(round(coords[0] / const.PIXELSIZE))
        yGrid = int(round(coords[1] / const.PIXELSIZE))
        for villager in self.villagers:
            if villager.isSelected:
                villager.goToLocation = (xGrid, yGrid)
                villager.state = VillagerState.forceMove
                villager.mood = VillagerMood.angry