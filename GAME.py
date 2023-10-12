import random

from WORLD.GAME_DISPLAY import GAME_DISPLAY
from ENTITIES.MOBS.PLAYER.PLAYER import PLAYER
from ENTITIES.MOBS.KAREN import KAREN
from WORLD.LOCATION_ID import LOCATION_ID


def GAME():
    GAME_RUNNING = True
    VERSION = "ALPHA.0.1"
    input(f"Welcome to New Australia: The Game {VERSION}!")
    input("New Australia: The Game is brought to you by iReverend Studios' The Jesuit.")
    input("The Jesuit (created by CaffeineSnake) is upcoming Christian superhero film from the studio that brought you The Methodist. Ignatius of Loyola is sent from Heaven to purify the Jesuit Order. Meanwhile, the Order sends Lenyn Ynot to find J. K. Rowling. Can Ignatius stop them before they activate the Millennium Clock?\n")
    input("New Australia is a turn-based dungeon crawler.")
    input("The objective is to escape the dungeon without being killed by the monsters.")
    input("To move, enter NORTH, SOUTH, EAST, or WEST.")
    input("To pass, enter LOOK.")
    input("To attack a monster, enter ATTACK.")
    input("To exit the game, enter QUIT.")
    input("For help, enter HELP.")
    input("Enter when ready.")
    
    PLAYER_COUNT = 1
    while True:
        try:
            KAREN_COUNT = int(input("Enter difficulty: "))
            if KAREN_COUNT >= 0:
                break  # Exit the loop if the user entered a valid integer
            else:
                print("Invalid input. Enter a whole number.")    
        except ValueError:
            print("Invalid input. Enter a whole number.")


    print("CREATING PLAYER.")
    
    MOBS = []
    
    # initalize Player
    PLAYER1 = PLAYER()
    MOBS.append(PLAYER1)
    
    if KAREN_COUNT:
        print("ADDING MONSTERS.\n")
        for i in range(KAREN_COUNT):
            _POSITION = (100, 100)
            while not LOCATION_ID(*_POSITION):
                _POSITION = (random.randint(-15, 15), random.randint(-15, 15))
            MOBS.append(KAREN(POSITION=(_POSITION))) # initalize Karen
            MOBS[i+PLAYER_COUNT].NAME += f".{i+PLAYER_COUNT}"
    
    print("Game ready.")
    TURN = 1
    GAME_DISPLAY(MOBS, TURN)
    
    while GAME_RUNNING:
        for mob in MOBS:
            GAME_RUNNING = mob.UPDATE(MOBS, TURN)
            if not GAME_RUNNING:
                break
        if not GAME_RUNNING:
            break
        
        input(f"End of TURN {TURN}.\n")
        TURN += 1
        GAME_DISPLAY(MOBS, TURN)
        

    print("\nGAME OVER.\n")
    print(f"Thank you for playing New Australia: The Game {VERSION} by John-Mary Knight.")
