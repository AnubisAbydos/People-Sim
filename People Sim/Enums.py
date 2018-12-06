"""
Project Name: People Sim
File Name: Enums.py
Author: Lex Hall
Last Updated: 11-13-2018
Python Version: 3.6
Pygame Version: 1.9.3
"""

class VillagerState(enumerate):
    idle = 0
    searchingForFood = 1
    moving = 2
    eating = 3
    building = 4
    starving = 5
    dead = 6
    selected = 7
    forceMove = 8
    harvesting = 9
    searchingForWood = 10

class VillagerMood(enumerate):
    content = 0
    happy = 1
    sad = 2
    angry = 3
    dead = 4
    panicked = 5
    working = 6