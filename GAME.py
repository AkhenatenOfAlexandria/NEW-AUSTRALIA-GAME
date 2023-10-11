import random

from WORLD.GAME_DISPLAY import GAME_DISPLAY
from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from ENTITIES.MOBS.KAREN import KAREN


def GAME():
    GAME_RUNNING = True
    print("GAME RUNNING.")
    
    PLAYER_COUNT = 1
    KAREN_COUNT = 8
    
    MOBS = []
    
    # initalize Player
    PLAYER1 = PLAYER()
    MOBS.append(PLAYER1)
    
    for i in range(KAREN_COUNT):
        MOBS.append(KAREN(POSITION=(random.randint(-15, 15), random.randint(-15, 15)))) # initalize Karen
        MOBS[i+PLAYER_COUNT].NAME += str(i+1)
    

    GAME_DISPLAY(MOBS)
    while GAME_RUNNING:
        for mob in MOBS:
            GAME_RUNNING = mob.UPDATE(MOBS, PLAYER1)
            if not GAME_RUNNING:
                break
        if not GAME_RUNNING:
            break
        
        if PLAYER1.POSITION[1] < -15:
            print("Level complete!")
            break
        GAME_DISPLAY(MOBS)

    print("GAME OVER.")
