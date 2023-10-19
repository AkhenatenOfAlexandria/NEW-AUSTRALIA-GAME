from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from INTRODUCTION import INTRODUCTION
from WORLD.SPAWN import SPAWN
from WORLD.GLOBAL_LISTS import PLAYERS, INITIATIVE_MOBS
from LOGIC.GLOBAL_FLAGS import GLOBAL_FLAGS, UPDATE_FLAG


def GAME():
    global GLOBAL_FLAGS
    COMBAT, LEVEL, TURN = GLOBAL_FLAGS["COMBAT"], GLOBAL_FLAGS["LEVEL"], GLOBAL_FLAGS["TURN"]
    
    GAME_RUNNING = True
    VERSION = "ALPHA 0.2.2"
    INTRODUCTION(VERSION)

    PLAYER_COUNT = 1

    for i in range(PLAYER_COUNT):
         _PLAYER = PLAYER()

    print("RUNNING GAME.")

    while GAME_RUNNING:
        LEVEL = UPDATE_FLAG("LEVEL", LEVEL+1)

        SPAWN(LEVEL)

        while GAME_RUNNING:
            TURN = UPDATE_FLAG("TURN", TURN+1)
            print(f"\nTURN: {TURN}")
            print(f"LEVEL: {LEVEL}\n")
            COMBAT = PLAYERS[0].ROOM_CHECK()
            # print(f"COMBAT: {COMBAT}; INITIATIVE: {INITIATIVE_MOB_NAMES}")
            if not COMBAT:
                for player in PLAYERS:
                    if player:
                        GAME_RUNNING, LEVEL_COMPLETE = player.UPDATE()
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
            else:
                for mob in INITIATIVE_MOBS:
                    if mob:
                        GAME_RUNNING, LEVEL_COMPLETE = mob.UPDATE()
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
            if LEVEL_COMPLETE or not GAME_RUNNING:
                break
            input(f"End of TURN {TURN}. ENTER to continue.\n")
            
        
        if not GAME_RUNNING:
                break

    SCORE = 0
    for player in PLAYERS:
         SCORE += player.EXPERIENCE
    print(f"\nGAME OVER.\nHIGHEST LEVEL: {LEVEL}\nSCORE: {SCORE}\n")
    print(f"Thank you for playing New Australia: The Game {VERSION} by John-Mary Knight.")
