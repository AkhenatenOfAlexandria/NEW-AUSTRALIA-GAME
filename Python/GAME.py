from INTRODUCTION import INTRODUCTION
from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from WORLD.SPAWN import SPAWN
from WORLD.GLOBAL import PLAYERS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES, GLOBAL_FLAGS, UPDATE_FLAG, INITIALIZE_DISPLAY, REFRESH_DISPLAY
from WORLD.GAME_WORLD import CREATE_LEVEL

import logging, os
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def clear_console():
    if os.name == 'posix':
        _ = os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        _ = os.system('cls')


def GAME():
    global GLOBAL_FLAGS
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    
    GAME_RUNNING = True
    VERSION = "ALPHA 0.3.0"
    INTRODUCTION(VERSION)

    PLAYER_COUNT = 1

    for i in range(PLAYER_COUNT):
         _PLAYER = PLAYER()
    
    INITIALIZE_DISPLAY()

    print("RUNNING GAME.")

    while GAME_RUNNING:
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        LEVEL = UPDATE_FLAG("LEVEL", LEVEL+1)
        if LEVEL > 1:
             CREATE_LEVEL()
        
        SPAWN()
        
        
        while GAME_RUNNING:
            if not DEBUG:
                clear_console()
            COMBAT, TIME = GLOBAL_FLAGS["COMBAT"], GLOBAL_FLAGS["TIME"]
            TIME = UPDATE_FLAG("TIME", TIME+1)
            print(REFRESH_DISPLAY())
                        
            if DEBUG:
                logging.debug(f"LEVEL COMBAT: {COMBAT}; INITIATIVE: {INITIATIVE_MOB_NAMES}")
            
            if not COMBAT:
                for player in PLAYERS:
                    if player:
                        GAME_RUNNING, LEVEL_COMPLETE = player.UPDATE()
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
                    COMBAT = GLOBAL_FLAGS["COMBAT"]
            else:
                for mob in INITIATIVE_MOBS:
                    if mob:
                        GAME_RUNNING, LEVEL_COMPLETE = mob.UPDATE()
                        if LEVEL_COMPLETE or not GAME_RUNNING:
                                break
                    COMBAT = GLOBAL_FLAGS["COMBAT"]
            if LEVEL_COMPLETE or not GAME_RUNNING:
                break
            input(f"End of TIME {TIME}. ENTER to continue.\n")
            
        
        if not GAME_RUNNING:
                break

    SCORE = 0
    for player in PLAYERS:
         SCORE += player.EXPERIENCE
    print(f"\nGAME OVER.\nHIGHEST LEVEL: {LEVEL}\nSCORE: {SCORE}\n")
    print(f"Thank you for playing New Australia: The Game {VERSION} by John-Mary Knight.")
