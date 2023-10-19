# Define the initial values for global variables in a dictionary
GLOBAL_FLAGS = {
    "TURN": 0,
    "COMBAT": False,
    "LEVEL": 0,
    "REALM": 0
}

# Function to update global variables
def UPDATE_FLAG(FLAG, VALUE):
    global GLOBAL_FLAGS
    if FLAG in GLOBAL_FLAGS:
        GLOBAL_FLAGS[FLAG] = VALUE
    return GLOBAL_FLAGS[FLAG]