"""
Project Name: 
File Name: 
Author: Lex Hall
Last Updated: 
Python Version: 2.7
Pygame Version: 1.9.1.win32-py2.7
"""

class VillagerState(enumerate):
    idle = 0
    searching = 1
    moving = 2
    eating = 3
    building = 4
    starving = 5
    dead = 6
    selected = 7
    forceMove = 8

class VillagerMood(enumerate):
    content = 0
    happy = 1
    sad = 2
    angry = 3
    dead = 4
    panicked = 5