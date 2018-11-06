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
import VillagerList
import MapController


def handleMouseClick(clickPos, mapController, villagers, mapX, mapY, isRightClick):
    clickPos = (clickPos[0] + mapX, clickPos[1] + mapY)
    if not isRightClick:
        villagers.checkCollision(clickPos)
    else:
        villagers.forceMove(clickPos)

### Main calls game sets screen and runs game loop
def main():
    pygame.init()

    # Build the screen
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    gameMap = pygame.Surface((const.MAP_WIDTH, const.MAP_HEIGHT))
    mapX = const.MAP_WIDTH / 4
    mapY = const.MAP_HEIGHT / 4

    done = False

    # Start the clock
    clock = pygame.time.Clock()

    # Build MapController
    mapController = MapController.MapController(gameMap)

    # Build VillagerList
    villagers = VillagerList.VillagerList(gameMap, mapController)

    # Lock cursor to window
    pygame.event.set_grab(True)

    # Loop Start
    while not done:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            mapY -= 5
        if keys[pygame.K_DOWN]:
            mapY += 5
        if keys[pygame.K_LEFT]:
            mapX -= 5
        if keys[pygame.K_RIGHT]:
            mapX += 5

        mousePos = pygame.mouse.get_pos()
        if mousePos[0] <= 0:
            mapX -= 10
        if mousePos[0] >= const.SCREEN_WIDTH - 1:
            mapX += 10
        if mousePos[1] <= 0:
            mapY -= 10
        if mousePos[1] >= const.SCREEN_HEIGHT - 1:
            mapY += 10

        if mapY > ((const.MAP_HEIGHT - const.SCREEN_HEIGHT) + 50):
            mapY = (const.MAP_HEIGHT - const.SCREEN_HEIGHT) + 50
        elif mapY < -50:
            mapY = -50
        if mapX > ((const.MAP_WIDTH - const.SCREEN_WIDTH) + 50):
            mapX = (const.MAP_WIDTH - const.SCREEN_WIDTH) + 50
        elif mapX < -50:
            mapX = -50
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handleMouseClick(mousePos, mapController, villagers, mapX, mapY, False)
                elif event.button == 3:
                    handleMouseClick(mousePos, mapController, villagers, mapX, mapY, True)

        pygame.draw.rect(gameMap, const.BLACK, (0, 0, const.MAP_WIDTH, const.MAP_HEIGHT))
        pygame.draw.rect(screen, const.BLACK, (0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

        mapController.tick()
        villagers.tick()

        screen.blit(gameMap, (0, 0), (mapX, mapY, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        mapController.drawMiniMap(screen, mapX, mapY)

        # Throttle frame rate
        clock.tick(const.FRAMERATE)
        # Uncomment below to output fps to console
        #print(clock.get_fps())
               
        # Flip to user
        pygame.display.flip()

    #Loop End

    pygame.quit()
    sys.exit()

# Call main to start game
if __name__ == "__main__":
    main()