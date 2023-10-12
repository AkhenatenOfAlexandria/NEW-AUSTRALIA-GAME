from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION

def GAME_DISPLAY(MOBS, LEVEL, TURN):
    for MOB in MOBS:
        if MOB.NAME == "YOU":
            if TURN:
                print(f"\nTURN: {TURN}")
                print(f"LEVEL: {LEVEL}")
                CURRENT_LOCATION = LOCATION_ID(*MOB.POSITION)
                print(f"HEALTH: {MOB.HEALTH}/{MOB.MAX_HEALTH}.")
                print(f"ARMOR CLASS: {MOB.ARMOR_CLASS}")
                print(f"LOCATION: {MOB.POSITION}")
                print(f"You are in a {CURRENT_LOCATION.DESCRIPTION}.{CURRENT_LOCATION.DESCRIBE_LOCATION(MOB)}")
        elif LOCATION_ID(*MOB.POSITION) == LOCATION_ID(*MOBS[0].POSITION):
            MOB_INDEX = MOBS.index(MOB)
            X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*MOBS[0].POSITION, *MOB.POSITION)
            print(f"\t{MOB.NAME} (ID: {MOB_INDEX}, HEALTH: {MOB.HEALTH}/{MOB.MAX_HEALTH}, ARMOR CLASS: {MOB.ARMOR_CLASS}): {Y_DISTANCE} feet {Y_DIRECTION}, {X_DISTANCE} feet {X_DIRECTION}.")
    