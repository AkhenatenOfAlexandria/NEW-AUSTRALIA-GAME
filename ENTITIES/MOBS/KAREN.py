from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import FOLLOW_PLAYER

class KAREN(MOB):
    def __init__(
            self,
            POSITION=(0,0),
            STRENGTH=8,
            DEXTERITY=14,
            CONSTITUTION=10,
            INTELLIGENCE=10,
            WISDOM=8,
            CHARISMA=8,
            HEALTH=7,
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
           self.NAME = "KAREN"
    

    def UPDATE(self, MOBS, PLAYER):
        GAME_RUNNING = True
        DIRECTION = FOLLOW_PLAYER(PLAYER, self)
        if DIRECTION:
            self.POSITION = self.MOVE(DIRECTION)
        else:
            try:
                 ATTACK, GAME_RUNNING = self.COMBAT_CHECK(PLAYER, MOBS)
            except TypeError as e:
                 print(f"TypeError: {e}.")
                 GAME_RUNNING = False
        return GAME_RUNNING