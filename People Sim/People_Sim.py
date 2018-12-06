"""
Project Name: People Sim
File Name: People_Sim.py
Author: Lex Hall
Last Updated: 11-13-2018
Python Version: 3.6
Pygame Version: 1.9.3
"""

import sys
import pygame
import Constants as const
import VillagerController
import MapController


def handleMouseClick(clickPos, mapController, villagerController, isRightClick):
    clickPos = (clickPos[0] + mapController.mapX, clickPos[1] + mapController.mapY)
    if not isRightClick:
        villagerWasSelected = villagerController.checkCollision(clickPos)
        if villagerWasSelected:
            mapController.deselectAllTiles()
        else:
            mapController.checkAllCollision(clickPos)
    else:
        villagerController.forceMove(clickPos)

### Main calls game sets screen and runs game loop
def main():
    pygame.init()

    # Build the screen
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    gameMap = pygame.Surface((const.MAP_WIDTH, const.MAP_HEIGHT))

    done = False

    # Variables used during loop - Tracks States
    buildingSelected = False
    buildingSelector = -1

    # Start the clock
    clock = pygame.time.Clock()

    # Build MapController
    mapController = MapController.MapController(gameMap, screen)

    # Build VillagerList
    villagerController = VillagerController.VillagerController(gameMap, mapController)

    # Lock cursor to window
    pygame.event.set_grab(True)

    # Loop Start
    while not done:

        mousePos = pygame.mouse.get_pos()
        mapController.handleScrolling(pygame.key.get_pressed(), mousePos)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_1:
                    buildingSelected = not buildingSelected
                    buildingSelector = 1
                    villagerController.deselectAllVillagers()
                    mapController.deselectAllTiles()
                elif event.key == pygame.K_2:
                    buildingSelected = not buildingSelected
                    buildingSelector = 2
                    villagerController.deselectAllVillagers()
                    mapController.deselectAllTiles()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Was the click Left Button
                if event.button == 1:
                    if not buildingSelected:
                        handleMouseClick(mousePos, mapController, villagerController, False)
                    else:
                        mapController.spawnBuilding(mousePos, buildingSelector)
                        buildingSelected = False
                        buildingSelector = -1
                # Was the click Right Button?
                elif event.button == 3:
                    buildingSelected = False
                    handleMouseClick(mousePos, mapController, villagerController, True)
                    

        # Clear map and screen before tick and draw calls
        pygame.draw.rect(gameMap, const.BLACK, (0, 0, const.MAP_WIDTH, const.MAP_HEIGHT))
        pygame.draw.rect(screen, const.BLACK, (0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

        # Tick Updates
        mapController.tick(buildingSelected, mousePos)
        villagerController.tick()

        # Draw everything
        mapController.drawMap()

        # Throttle frame rate
        clock.tick(const.FRAMERATE)
        # Uncomment below to output fps to console #
        #print(clock.get_fps())
               
        # Flip to user
        pygame.display.flip()

    #Loop End

    pygame.quit()
    sys.exit()

# Call main to start game
if __name__ == "__main__":
    main()