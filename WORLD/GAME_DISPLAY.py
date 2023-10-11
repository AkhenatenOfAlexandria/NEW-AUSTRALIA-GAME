from LOGIC.LOCATION_ID import LOCATION_ID
from ENTITIES.MOBS.KAREN import KAREN

def GAME_DISPLAY(MOBS):       
    for MOB in MOBS:
        if MOB.NAME == "PLAYER":
            CURRENT_LOCATION = LOCATION_ID(*MOB.POSITION).DESCRIPTION
            print(f"Health: {MOB.HEALTH}.\nLocation: {MOB.POSITION}\n{CURRENT_LOCATION}")
        elif LOCATION_ID(*MOB.POSITION) == LOCATION_ID(*MOBS[0].POSITION):
            MOB_INDEX = MOBS.index(MOB)
            print(f"{MOB_INDEX} {MOB.NAME} at {MOB.POSITION}. Health: {MOB.HEALTH}")