from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from WORLD.GAME_DISPLAY import GAME_DISPLAY
from INTRODUCTION import INTRODUCTION
from WORLD.SPAWN import SPAWN
from WORLD.GLOBAL_LISTS import PLAYERS, INITIATIVE_MOBS


def GAME():
    GAME_RUNNING = True
    VERSION = "ALPHA 0.2.1"
    INTRODUCTION(VERSION)

    PLAYER_COUNT = 1

    for i in range(PLAYER_COUNT):
         _PLAYER = PLAYER()

    print("RUNNING GAME.")
    TURN = 1
    LEVEL = 1
    while GAME_RUNNING:

        SPAWN(LEVEL)

        while GAME_RUNNING:
            print(f"\nTURN: {TURN}")
            print(f"LEVEL: {LEVEL}\n")
            COMBAT = PLAYERS[0].ROOM_CHECK()
            # print(f"COMBAT: {COMBAT}; INITIATIVE: {INITIATIVE_MOB_NAMES}")
            if not COMBAT:
                for player in PLAYERS:
                    if player:
                        GAME_RUNNING, LEVEL_COMPLETE, TURN = player.UPDATE(TURN, LEVEL)
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
            else:
                for mob in INITIATIVE_MOBS:
                    if mob:
                        GAME_RUNNING, LEVEL_COMPLETE, TURN = mob.UPDATE(TURN, LEVEL)
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
            if LEVEL_COMPLETE or not GAME_RUNNING:
                break
            input(f"End of TURN {TURN}. ENTER to continue.\n")
            TURN += 1
        
        if not GAME_RUNNING:
                break

        LEVEL += 1

    SCORE = 0
    for player in PLAYERS:
         SCORE += player.EXPERIENCE
    print(f"\nGAME OVER.\nHIGHEST LEVEL: {LEVEL}\nSCORE: {SCORE}\n")
    print(f"Thank you for playing New Australia: The Game {VERSION} by John-Mary Knight.")
