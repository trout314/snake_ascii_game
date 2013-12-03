from setup import *
import curses    # for displaying text to screen
import time      # for time related tasts

#-----------------------------------------------------------------------------
# Some little helper functions
#-----------------------------------------------------------------------------

def put(pos, char):
    scr.addch(pos["y"], pos["x"], char)

# Display a message on the bottom line of the screen
def message(msg):
    scr.addstr(max_y, min_x, " "*max_x)
    scr.addstr(max_y, min_x, msg[:max_x])

#-----------------------------------------------------------------------------
# Player movement actions
#-----------------------------------------------------------------------------

def move_player_up():
    put(player_pos, " ")
    if player_pos["y"] > 0:
        player_pos["y"] -= 1

def move_player_down():
    put(player_pos, " ")
    if player_pos["y"] < max_y-1: #last line is for messages
        player_pos["y"] += 1

def move_player_left():
    put(player_pos, " ")
    if player_pos["x"] > 0:
        player_pos["x"] -= 1

def move_player_right():
    put(player_pos, " ")
    if player_pos["x"] < max_x:
        player_pos["x"] += 1

#-----------------------------------------------------------------------------
# Bullet actions
#-----------------------------------------------------------------------------

def add_bullet():
    if player_pos["y"] > 0:
        # append a copy of the player position dictionary
        bullets.append(dict(player_pos))

def move_bullets():
    global bullets

    # put blanks in current positions
    for pos in bullets: put(pos, " ")

    # remove bullets at top of screen
    bullets = [pos for pos in bullets if pos["y"]>0]

    # move bullets
    for pos in bullets: pos["y"] -= 1
 

def draw_bullets():
    for bullet_pos in bullets:
        put(bullet_pos, bullet_sym)

#-----------------------------------------------------------------------------
# Global game-state variables
#     Here we will put data that the whole program will need to use and to 
#     modify.
#-----------------------------------------------------------------------------

player_pos = {"x":40, "y": 20}

bullets = []

spiders = [
    {"x":10, "y":10},
    {"x":15, "y":15}
]

snakes = [
    {"x":2, "y":2}, {"x":3, "y":2}, {"x":4, "y":2}, {"x":5, "y":2},
    {"x":5, "y":3}, {"x":6, "y":3}, {"x":7, "y":3}, {"x":8, "y":3}
]
    
#-----------------------------------------------------------------------------
# Global constants:
#     In this section we will put data items that the whole program will need
#     but that should not be changed.
#-----------------------------------------------------------------------------

# limits for display area
min_x, max_x = 0, 79
min_y, max_y = 0, 23

player_sym = "@"
bullet_sym = "*"

mushroom_syms = ["_", "m", "M"]

time_delay = 0.03

key_actions = {
    'q' : exit,
    'Q' : exit,
    'w' : move_player_up,
    's' : move_player_down,
    'a' : move_player_left,
    'd' : move_player_right,
    ' ' : add_bullet
}

#-----------------------------------------------------------------------------
# Main game code
#-----------------------------------------------------------------------------

# clear screen and display start message
scr.clear()
message("Press 'Q' or 'q' to quit.")
scr.refresh()

# This is the main game loop
while True:
    # Draw player symbol
    put(player_pos, player_sym)

    # Draw bullets
    draw_bullets()

    # TO DO #1: draw_centipedes
    # TO DO #2: draw_spiders
    # TO DO #3: draw_mushrooms

    # draw screen and then wait
    scr.refresh()
    time.sleep(time_delay)

    # get key-press, as numerical value
    key_pressed = scr.getch()

    # flush input buffer so key-presses don't acccumulate
    curses.flushinp()

    # perform actions associated with keys
    for key in key_actions:
        if key_pressed == ord(key):
            key_actions[key]()
    
    # perform other movements
    move_bullets()

    # TO DO #4: move_centipedes
    # TO DO #5: move_spiders
    
    # resolve consequences of collisions
    
    #TO DO #7)  Bullet hits snake segment (SEGMENT REMOVED, NOW TWO SNAKES) 
    #TO DO #8)  Bullet hits spider (SPIDER REMOVED)
    #TO DO #9)  Spider hits player (GAME OVER)
    #TO DO #10) Centipede hits player (GAME OVER)
    #TO DO #11) Centipede touches last playable row (GAME OVER)