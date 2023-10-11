from ENTITIES.MOBS.MOB import MOB
from LOGIC.PROCESS_COMMAND import PROCESS_COMMAND

class PLAYER(MOB):
    def __init__(
            self,
            POSITION=(0,0),
            STRENGTH=16,
            DEXTERITY=14,
            CONSTITUTION=15,
            INTELLIGENCE=13,
            WISDOM=11,
            CHARISMA=9,
            HEALTH=10,
            *args
            ):
        
        super().__init__(
            POSITION,
            STRENGTH,
            DEXTERITY,
            CONSTITUTION,
            INTELLIGENCE,
            WISDOM,
            CHARISMA,
            HEALTH,
            *args
            )
        
        self.NAME = "PLAYER"


    def GET_PLAYER_COMMAND(self):
        return input("Enter your COMMAND: ")

    
    def UPDATE(self, MOBS, *args):
        COMMAND = self.GET_PLAYER_COMMAND()
        GAME_RUNNING, self.POSITION = PROCESS_COMMAND(COMMAND, self, MOBS)
        return GAME_RUNNING
    

    def DIE(self, MOBS):
        print("You died.")
        return False
