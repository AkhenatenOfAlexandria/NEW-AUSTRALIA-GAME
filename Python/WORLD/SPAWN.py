import random
import logging
import math

from ENTITIES.MOBS.ABORIGINE import ABORIGINE
from ENTITIES.MOBS.BABOON import BABOON
from ENTITIES.MOBS.BAT import BAT
from ENTITIES.MOBS.FROG import FROG
from ENTITIES.MOBS.GIANT_FIRE_BEETLE import GIANT_FIRE_BEETLE
from ENTITIES.MOBS.KAREN import KAREN
from ENTITIES.MOBS.RAT import RAT
from ENTITIES.MOBS.GIANT_RAT import GIANT_RAT
from ENTITIES.MOBS.SCORPION import SCORPION
from ENTITIES.MOBS.SPIDER import SPIDER
from ENTITIES.MOBS.BANDIT import BANDIT
from ENTITIES.MOBS.GUARD import GUARD
from ENTITIES.MOBS.KOBOLD import KOBOLD
from ENTITIES.MOBS.PITBULL import PITBULL
from ENTITIES.MOBS.FLYING_SNAKE import FLYING_SNAKE
from ENTITIES.MOBS.VENOMOUS_SNAKE import VENOMOUS_SNAKE
from ENTITIES.MOBS.CONSTRICTOR_SNAKE import CONSTRICTOR_SNAKE
from ENTITIES.MOBS.STIRGE import STIRGE
from ENTITIES.MOBS.GIANT_BAT import GIANT_BAT
from ENTITIES.MOBS.GIANT_CENTIPEDE import GIANT_CENTIPEDE
from ENTITIES.MOBS.GIANT_CONSTRICTOR_SNAKE import GIANT_CONSTRICTOR_SNAKE
from ENTITIES.MOBS.GIANT_FROG import GIANT_FROG
from ENTITIES.MOBS.GIANT_LIZARD import GIANT_LIZARD
from ENTITIES.MOBS.APE import APE
import WORLD.GAME_WORLD as _WORLD
from WORLD.GLOBAL import PLAYERS, MOBS, REMOVE_ENTITY, GLOBAL_FLAGS, CONTAINERS
from ENTITIES.ITEMS.CONTAINERS.CHEST import CHEST
from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from LOGIC.FUNCTIONS import LOOT_TABLE
from LOGIC.MATH import CHOOSE_LOOT, NUMBERS_LOOT_TABLE, CHOOSE_NUMBER

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def PLAYER_SPAWN(COUNT):
    for i in range(COUNT):
        _PLAYER = PLAYER()
        _PLAYER.HEALTH = _PLAYER.MAX_HEALTH*100



def SPAWN():
    global GLOBAL_FLAGS
    LEVEL, REALM, DEBUG = GLOBAL_FLAGS["LEVEL"], GLOBAL_FLAGS["REALM"], GLOBAL_FLAGS["DEBUG"]

    logging.info("LOADING LEVEL...")
    for PLAYER in PLAYERS:
        PLAYER.POSITION[2:4] = [-2*(26-LEVEL), REALM]
        PLAYER.XP_LEVEL()
        if PLAYER.MAX_HEALTH > PLAYER.HEALTH or LEVEL == 1:
            PLAYER.HEALTH = PLAYER.MAX_HEALTH

    for MOB in MOBS:
        if MOB and not MOB in PLAYERS:
            REMOVE_ENTITY(MOB)
    
    MAX_X = 0
    MIN_X = 0
    MAX_Y = 0
    MIN_Y = 0
    _ROOMS_ = _WORLD.GAME_WORLD[LEVEL]

    MONSTERS = [FROG, # 0 XP
            ABORIGINE, BABOON, BAT, GIANT_FIRE_BEETLE, RAT, SCORPION, SPIDER, # 10 XP
            BANDIT, FLYING_SNAKE, GIANT_RAT, GUARD, KOBOLD, PITBULL, STIRGE, VENOMOUS_SNAKE, #25 XP
            CONSTRICTOR_SNAKE, GIANT_BAT, GIANT_CENTIPEDE, GIANT_FROG, GIANT_LIZARD, KAREN, # 50 XP
            APE, GIANT_CONSTRICTOR_SNAKE #100 XP
        ]
    
    if not LEVEL:
        GAME_WORLD = _WORLD.GAME_WORLD
        _ROOM = GAME_WORLD[0][1]
        POSITION0 = (-52, 0)
        POSITION1 = (int((_ROOM.MIN_X+_ROOM.MAX_X)/2), int((_ROOM.MIN_Y+_ROOM.MAX_Y)/2))
        for i in range(10):
            FROG([*POSITION1, *POSITION0])
        _ROOM = GAME_WORLD[0][2]
        POSITION2 = (int((_ROOM.MIN_X+_ROOM.MAX_X)/2), int((_ROOM.MIN_Y+_ROOM.MAX_Y)/2))
        for MONSTER in MONSTERS[1:8]:
            MONSTER([*POSITION2, *POSITION0])
        _ROOM = GAME_WORLD[0][3]
        POSITION3 = (int((_ROOM.MIN_X+_ROOM.MAX_X)/2), int((_ROOM.MIN_Y+_ROOM.MAX_Y)/2))
        for MONSTER in MONSTERS[8:16]:
            MONSTER([*POSITION3, *POSITION0])
        _ROOM = GAME_WORLD[0][4]
        POSITION4 = (int((_ROOM.MIN_X+_ROOM.MAX_X)/2), int((_ROOM.MIN_Y+_ROOM.MAX_Y)/2))
        for MONSTER in MONSTERS[16:22]:
            MONSTER([*POSITION4, *POSITION0])
        _ROOM = GAME_WORLD[0][5]
        POSITION5 = (int((_ROOM.MIN_X+_ROOM.MAX_X)/2), int((_ROOM.MIN_Y+_ROOM.MAX_Y)/2))
        for MONSTER in MONSTERS[22:]:
            MONSTER([*POSITION5, *POSITION0])
        
        logging.debug(POSITION1, POSITION2, POSITION3, POSITION4, POSITION5)
    
    else:
        for ROOM in _ROOMS_:
            MAX_X = int(max(MAX_X, ROOM.MAX_X))
            MAX_Y = int(max(MAX_Y, ROOM.MAX_Y))
            MIN_X = int(min(MIN_X, ROOM.MIN_X))
            MIN_Y = int(min(MIN_Y, ROOM.MIN_Y))

            logging.info(f"ADDING MONSTERS - {_ROOMS_.index(ROOM)}/{len(_ROOMS_)}.")

            if ROOM.VICTORY or ROOM.START:
                pass
            else:
                if LEVEL < 5: # Level 1
                    DIFFICULTY = random.choice([0, 25, 50, 75])
                elif LEVEL < 7: # Level 2
                    DIFFICULTY = random.choice([0, 50, 100, 150])
                elif LEVEL < 9: # Level 3
                    DIFFICULTY = random.choice([0, 75, 150, 225])
                elif LEVEL < 12: # Level 4
                    DIFFICULTY = random.choice([0, 125, 250, 375])
                elif LEVEL < 14: # Level 5
                    DIFFICULTY = random.choice([0, 250, 500, 750])
                elif LEVEL == 14: # Level 6
                    DIFFICULTY = random.choice([0, 300, 600, 900])
                elif LEVEL < 17: # Level 7
                    DIFFICULTY = random.choice([0, 350, 750, 1100])
                elif LEVEL == 17: # Level 8
                    DIFFICULTY = random.choice([0, 450, 900, 1400])
                elif LEVEL == 18: # Level 9
                    DIFFICULTY = random.choice([0, 550, 1100, 1600])
                elif LEVEL == 19: # Level 10
                    DIFFICULTY = random.choice([0, 600, 1200, 1900])
                elif LEVEL == 20: # Level 11
                    DIFFICULTY = random.choice([0, 800, 1600, 2400])
                elif LEVEL == 21: # Level 12
                    DIFFICULTY = random.choice([0, 1000, 2000, 3000])
                elif LEVEL == 22: # Level 14
                    DIFFICULTY = random.choice([0, 1250, 2500, 3800])
                elif LEVEL == 23: # Level 15
                    DIFFICULTY = random.choice([0, 1400, 2800, 4300])
                elif LEVEL == 24: # Level 17
                    DIFFICULTY = random.choice([0, 2000, 3900, 5900])
                else: # Level 18
                    DIFFICULTY = random.choice([0, 2100, 4200, 6300])

                COUNT = 1
                MONSTER_COUNT = 0
                _XP = 0
                XP = 0
                while _XP < DIFFICULTY and DIFFICULTY-_XP >= 10:
                    logging.info(f"Attempting to add MONSTER... {COUNT}")
                    if COUNT > 1024:
                        logging.error("UNABLE TO SPAWN MONSTER.")
                        break
                    _MONSTER_CLASS = random.choice(MONSTERS)
                    _POSITION = [random.randint(ROOM.MIN_X+1, ROOM.MAX_X-1), random.randint(ROOM.MIN_Y+1, ROOM.MAX_Y-1), (LEVEL-1)*2, REALM]
                    _MONSTER = _MONSTER_CLASS(_POSITION, _MONSTER_CLASS.HEALTH_ROLL())
                    if _MONSTER.EXPERIENCE_POINTS <= (DIFFICULTY-_XP) and _MONSTER.EXPERIENCE_POINTS <= LEVEL*10:
                        _MONSTER.DEFAULT_ITEMS()
                        MONSTER_COUNT += 1
                        XP += _MONSTER.EXPERIENCE_POINTS
                        if MONSTER_COUNT == 1:
                            _XP = XP*1.5
                        elif MONSTER_COUNT == 2:
                            _XP = XP*2
                        elif 3 <= MONSTER_COUNT <= 6:
                            _XP = XP*2.5
                        elif 7 <= MONSTER_COUNT <= 10:
                            _XP = XP*3
                        elif 11 <= MONSTER_COUNT <= 14:
                            _XP = XP*4
                        else:
                            _XP = XP*5
                    else:
                        REMOVE_ENTITY(_MONSTER, SAFE=False)
                    COUNT += 1

        logging.info("ADDING CHESTS...")
        _ROOMS = list(_WORLD.GAME_WORLD[LEVEL])
        
        CHEST_COUNT = 0
        TABLE = LOOT_TABLE()
        
        while CHEST_COUNT < LEVEL:
            for ROOM in _ROOMS:
                CHEST_SPAWN = random.randint(1, LEVEL)
                if CHEST_SPAWN == LEVEL and ROOM.DESCRIPTION in ("SMALL ROOM", "LARGE ROOM") and not ROOM.VICTORY:
                    CHEST_POSITION = (random.randint(ROOM.MIN_X+1, ROOM.MAX_X-1), random.randint(ROOM.MIN_Y+1, ROOM.MAX_Y-1), LEVEL, 0)
                    _CHEST = CHEST(CHEST_POSITION)
                    ROOM.LOCAL_ITEMS.append(_CHEST)
                    _ITEMS = random.randint(1,8)
                    for i in range(_ITEMS):
                        try:
                            LOOT = CHOOSE_LOOT(TABLE)
                            '''while not LOOT:
                                LOOT = CHOOSE_LOOT(TABLE)
                                logging.error(f"SPAWN(): No Loot generated.\n{TABLE}\n{LOOT}")'''
                            if LOOT == "ARROWS":
                                ARROWS = random.randint(1,20)
                                _CHEST.ARROWS += ARROWS
                            if LOOT == "SLING-PELLETS":
                                PELLETS = random.randint(1,20)
                                _CHEST.SLING_PELLETS += PELLETS
                            if LOOT == "WATER":
                                WATER = random.randint(1,8)
                                _CHEST.WATER += WATER
                            else:
                                _LOOT = LOOT()
                                _CHEST.ADD_ITEM(_LOOT)
                        except TypeError as e:
                            logging.error(f"TypeError: {e}\nCLASS: {LOOT}.")
                    if ROOM.DESCRIPTION == "SMALL ROOM":
                        _ROOMS.remove(ROOM)
                    CHEST_COUNT += 1
                logging.info(f"ADDING CHESTS: {CHEST_COUNT}/{LEVEL}")
                if CHEST_COUNT >= LEVEL:
                    break
                
