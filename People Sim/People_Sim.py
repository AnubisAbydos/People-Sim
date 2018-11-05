"""
Project Name: 
File Name: 
Author: Lex Hall
Last Updated: 
Python Version: 2.7
Pygame Version: 1.9.1.win32-py2.7
"""

import sys
import pygame
import Constants as const
import Villager
import Map

### Main calls game sets screen and runs game loop
def main():
    pygame.init()

    # Build the screen
    screen = pygame.display.set_mode((const.GAME_WIDTH, const.GAME_HEIGHT))

    done = False

    # Start the clock
    clock = pygame.time.Clock()
    map = Map.Map(screen)
    villagers = []
    for i in xrange(3):
       villagers.append(Villager.Villager(screen))
    # Loop Start
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.draw.rect(screen, (0,0,0), (0,0,800,800))
        
        map.tick()
        for villager in villagers:
            villager.tick(map)

        # Throttle frame rate
        clock.tick(const.FRAMERATE)

        # Flip to user
        pygame.display.flip()
    #Loop End

    pygame.quit()
    sys.exit()

# Call main to start game
if __name__ == "__main__":
    main()