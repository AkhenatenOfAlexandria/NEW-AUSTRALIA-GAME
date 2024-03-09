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
from ENTITIES.MOBS.APE import APE
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
import WORLD.GAME_WORLD as _WORLD
from WORLD.GLOBAL import PLAYERS, MOBS, REMOVE_ENTITY, GLOBAL_FLAGS, CONTAINERS
from ENTITIES.ITEMS.CONTAINERS.CHEST import CHEST
from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from LOGIC.FUNCTIONS import LOOT

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def PLAYER_SPAWN(COUNT):
    for i in range(COUNT):
        _PLAYER = PLAYER()
    for i in range(100):
        _POSITION = [random.randint(-30,30), random.randint(-30,30), 0, 0]
        _KAREN = KAREN(_POSITION)



def SPAWN():
    global GLOBAL_FLAGS
    LEVEL, REALM, DEBUG = GLOBAL_FLAGS["LEVEL"], GLOBAL_FLAGS["REALM"], GLOBAL_FLAGS["DEBUG"]
    LEVEL_XP = LEVEL*10

    logging.info("LOADING LEVEL...")
    for PLAYER in PLAYERS:
        PLAYER.POSITION[2:4] = [LEVEL*2, REALM]
        PLAYER.XP_LEVEL()
        PLAYER.HEALTH = PLAYER.MAX_HEALTH

    for MOB in MOBS:
        if MOB and not MOB in PLAYERS:
            REMOVE_ENTITY(MOB)
    
    MAX_X = 0
    MIN_X = 0
    MAX_Y = 0
    MIN_Y = 0
    for ROOM in _WORLD.GAME_WORLD[LEVEL]:
        MAX_X = int(max(MAX_X, ROOM.MAX_X))
        MAX_Y = int(max(MAX_Y, ROOM.MAX_Y))
        MIN_X = int(min(MIN_X, ROOM.MIN_X))
        MIN_Y = int(min(MIN_Y, ROOM.MIN_Y))

    while LEVEL_XP >= 10:
        logging.info(f"ADDING MONSTERS - {LEVEL_XP} XP REMAINING.")
        _LOCATION = None
        COUNT = 0
        while not _LOCATION or _LOCATION.START or _LOCATION.VICTORY:
            logging.info(f"Attempting to add MONSTER... {COUNT}")
            _POSITION = [random.randint(MIN_X, MAX_X), random.randint(MIN_Y, MAX_Y), (LEVEL-1)*2, REALM]
            _LOCATION = LOCATION_ID(*_POSITION[0:2])
            COUNT += 1
            if COUNT > 1024:
                logging.debug("UNABLE TO SPAWN MONSTER.")
                break
        
        MONSTERS = [FROG, # 0 XP
                    ABORIGINE, BABOON, BAT, GIANT_FIRE_BEETLE, RAT, SCORPION, SPIDER, # 10 XP
                    BANDIT, FLYING_SNAKE, GIANT_RAT, GUARD, KOBOLD, PITBULL, #25 XP
                    KAREN, # 50 XP
                    APE #100 XP
                    ]
        _MONSTER_CLASS = random.choice(MONSTERS)
        _MONSTER = _MONSTER_CLASS(_POSITION, _MONSTER_CLASS.HEALTH_ROLL())
        if _MONSTER.EXPERIENCE_POINTS <= LEVEL_XP and _MONSTER.EXPERIENCE_POINTS <= LEVEL*10:
            _MONSTER.DEFAULT_ITEMS()
            LEVEL_XP -= _MONSTER.EXPERIENCE_POINTS
        else:
            REMOVE_ENTITY(_MONSTER, SAFE=False)

    
    logging.info("ADDING CHESTS...")
    EMPTY_ROOMS = list(_WORLD.GAME_WORLD[LEVEL])
    
    CHEST_COUNT = 0
    while True:
        for ROOM in EMPTY_ROOMS:
            CHEST_SPAWN = random.randint(1, LEVEL)
            if CHEST_SPAWN == LEVEL and ROOM.DESCRIPTION == "SMALL ROOM" and not ROOM.VICTORY:
                CHEST_POSITION = (random.randint(ROOM.MIN_X+1, ROOM.MAX_X-1), random.randint(ROOM.MIN_Y+1, ROOM.MAX_Y-1), LEVEL, 0)
                ROOM.LOCAL_ITEMS.append(CHEST(CHEST_POSITION))
                EMPTY_ROOMS.remove(ROOM)
            CHEST_COUNT += 1
            print(f"{CHEST_COUNT}/{LEVEL*2}")
            if CHEST_COUNT >= LEVEL:
                break
        if CHEST_COUNT >= LEVEL:
                break
            
    
    CHEST_GOLD = LEVEL
    while CHEST_GOLD > 0 and len(CONTAINERS) > 0:
        for container in CONTAINERS:
            if random.randint(1, len(CONTAINERS)) == 1:
                _LOOT = random.choice(LOOT)
                logging.info(f"Loot selected: {_LOOT}")
                if type(_LOOT) == str:
                    container.GOLD = round(container.GOLD+0.01, 2)
                    CHEST_GOLD = round(CHEST_GOLD-0.01, 2)
                    _CHEST_COUNT = math.floor(LEVEL+CHEST_GOLD*10)
                    print(f"{_CHEST_COUNT}/{LEVEL*2}")
                elif len(container.CONTENTS) < 10:
                    _LOOT = _LOOT()
                    logging.info(f"LOOT PRICE: {_LOOT.PRICE}; CHEST GOLD: {CHEST_GOLD}")
                    if CHEST_GOLD >= _LOOT.PRICE:
                        container.ADD_ITEM(_LOOT)
                        logging.info(f"Added Loot: {_LOOT.NAME}.")
                        CHEST_GOLD -= _LOOT.PRICE
                    else:
                        REMOVE_ENTITY(_LOOT, SAFE=False)
                        logging.info(f"Discarded Loot: {_LOOT.NAME}.")

    if DEBUG:
            for ROOM in _WORLD.GAME_WORLD[LEVEL]:
                logging.debug(f"{ROOM.DESCRIPTION}:{ROOM.LOCAL_ITEMS}")
    
