from WORLD.GLOBAL import PLAYERS, MOBS, UPDATE_DISPLAY, DISPLAY
from LOGIC.MATH import DISTANCE, ROLL

import logging
import random
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def BLOOD_DRAIN(MOB, ATTACHEE):
    if ATTACHEE:
        DAMAGE = ROLL(1,4)+3
        ATTACHEE.HEALTH -= DAMAGE

        _HUD = f"\n{MOB.NAME} drained {ATTACHEE.NAME}, dealing {DAMAGE} DAMAGE."
        logging.info(_HUD)
        HUD = _HUD
        DEATH = None
        if ATTACHEE.HEALTH <= 0:
            DEATH = f"\n{ATTACHEE.NAME} died."
            
            GAME_RUNNING = ATTACHEE.DIE()
            
        if DEATH:
            HUD += DEATH
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)
    else:
        ATTACK_PLAYER(MOB)


def ATTACK_PLAYER(MOB):
    PLAYER = PLAYERS[0]
    if not PLAYER:
        return
    PLAYER_X, PLAYER_Y = PLAYER.POSITION[0:2]
    MOB_X, MOB_Y = MOB.POSITION[0:2]
    WEAPON = MOB.INVENTORY["WEAPON"]

    _DISTANCE = DISTANCE(PLAYER_X, PLAYER_Y, MOB_X, MOB_Y)
    if _DISTANCE > math.sqrt(8):
        
        if WEAPON and "RANGED" in WEAPON.ATTRIBUTES:
            MOB.RANGED_ATTACK(PLAYER)
        else:
            for ITEM in MOB.INVENTORY["ITEMS"]:
                if "RANGED" in ITEM.ATTRIBUTES:
                    MOB.INVENTORY["ITEMS"].append(WEAPON)
                    MOB.INVENTORY["WEAPON"] = MOB.INVENTORY["ITEMS"].pop(ITEM)
                    return
            FOLLOW_PLAYER(MOB)

    elif math.sqrt(8) >= _DISTANCE > math.sqrt(2):
        if (WEAPON and "RANGED" in WEAPON.ATTRIBUTES) or not WEAPON:
            for ITEM in MOB.INVENTORY["ITEMS"]:
                    if not "RANGED" in ITEM.ATTRIBUTES:
                        MOB.INVENTORY["ITEMS"].append(WEAPON)
                        MOB.INVENTORY["WEAPON"] = MOB.INVENTORY["ITEMS"].pop(ITEM)
                        return
        FOLLOW_PLAYER(MOB)
    else:
        MOB.COMBAT_CHECK(PLAYER)


def FOLLOW_PLAYER(MOB):
    if MOB.PRONE:
        MOB.PRONE = False
    else:
        PLAYER = PLAYERS[0]
        PLAYER_X, PLAYER_Y = PLAYER.POSITION[0:2]
        MOVEMENT = MOB.SPEED/6
        while MOVEMENT > 0:
            M = float(MOVEMENT)
            while M > 1:
                M -= 1
            if random.random() < M:
                MOB_X, MOB_Y = MOB.POSITION[0:2]
                DIRECTION = {"LEFT":False, "RIGHT":False, "UP":False, "DOWN":False}
                
                if PLAYER_X-MOB_X > 0:
                    DIRECTION["RIGHT"] = True
                elif MOB_X-PLAYER_X > 0:
                    DIRECTION["LEFT"] = True
                elif PLAYER_Y-MOB_Y > 0:
                    DIRECTION["UP"] = True
                elif MOB_Y-PLAYER_Y > 0:
                    DIRECTION["DOWN"] = True
                
                for key, value in DIRECTION.items():
                    if value:
                        STAY = False
                        POSITION = MOB.MOVE(key)
                        for mob in MOBS:
                            if mob and POSITION == mob.POSITION[0:2]:
                                STAY = True
                                break
                        if not STAY:
                            MOB.POSITION[0:2] = POSITION
                            if MOB.ATTACHED and (
                                (abs(POSITION[0]-MOB.ATTACHED.POSITION[0]) > 1
                                ) or (
                                    abs(POSITION[1]-MOB.ATTACHED.POSITION[1]) > 1
                                    )):
                                MOB.ATTACHED.POSITION[0:2] = POSITION
            MOVEMENT -= 1

