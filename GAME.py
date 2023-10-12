from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from WORLD.GAME_DISPLAY import GAME_DISPLAY
from INTRODUCTION import INTRODUCTION
from WORLD.SPAWN import SPAWN


def GAME():
    GAME_RUNNING = True
    VERSION = "ALPHA.1.0"
    INTRODUCTION(VERSION)

    TURN = 1
    PLAYER_COUNT = 1

    PLAYERS = []
    
    for i in range(PLAYER_COUNT):
         PLAYERS.append(PLAYER())
         PLAYER.NAME = f"PLAYER {i+1}"
         

    print("RUNNING GAME.")
    LEVEL = 1
    while GAME_RUNNING:

        MOBS = SPAWN(PLAYERS, LEVEL)

        GAME_DISPLAY(MOBS, LEVEL, TURN)

        while GAME_RUNNING:
            for mob in MOBS:
                GAME_RUNNING, LEVEL_COMPLETE, TURN = mob.UPDATE(MOBS, TURN)
                if LEVEL_COMPLETE or not GAME_RUNNING:
                        break
            if LEVEL_COMPLETE or not GAME_RUNNING:
                break
            input(f"End of TURN {TURN}. ENTER to continue.\n")
            TURN += 1
            GAME_DISPLAY(MOBS, LEVEL, TURN)
        
        if not GAME_RUNNING:
                break

        LEVEL += 1

    print(f"\nGAME OVER.\nHIGHEST LEVEL: {LEVEL}\n")
    print(f"Thank you for playing New Australia: The Game {VERSION} by John-Mary Knight.")
