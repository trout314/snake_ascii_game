from setup import *
import curses    # for displaying text to screen
import time      # for time related tasts
import random    # for choosing a random character movement direction
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
    {"x":12, "y":10},
    {"x":15, "y":15}
]

snakes = [
    [{"x":12, "y":2}, {"x":13, "y":2}, {"x":14, "y":2}, {"x":15, "y":2}, {"x":16, "y":2}, {"x":17, "y":2}, {"x":18, "y":2}],
    [{"x":9, "y":3}, {"x":8, "y":3}, {"x":7, "y":3}, {"x":6, "y":3}, {"x":5, "y":3}]
]

mushrooms = [{"x":12, "y":7},{"x": 23, "y":5},{"x":68, "y":12},{"x":12, "y":15}]
    
#-----------------------------------------------------------------------------
# Global constants:
#     In this section we will put data items that the whole program will need
#     but that should not be changed during the game.
#-----------------------------------------------------------------------------

# limits for display area
min_x, max_x = 0, 79
min_y, max_y = 0, 23

snake_head_sym = "O"
snake_body_sym = "o"
player_sym = "@"
bullet_sym = "*"
spider_sym = "S"
mushroom_sym = "M"

time_delay = 0.05

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
#draw and move snakes
#-----------------------------------------------------------------------------

def move_snakes():
    global snakes
    for snake in snakes:
        head_pos = dict(snake[-1])
        if (head_pos["y"] % 2 == 0):
            head_pos["x"] += 1
            if (head_pos in mushrooms) or (head_pos["x"] > max_x):
                head_pos["x"] -= 1
                head_pos["y"] += 1
        else:
            head_pos["x"] -= 1
            if (head_pos in mushrooms) or (head_pos["x"] < 0):
                head_pos["x"] += 1
                head_pos["y"] += 1

        put(snake[0], " ")
        del snake[0]
        snake.append(head_pos)

def draw_snakes():
    for snake in snakes:
        for snake_pos in snake[:-1]:
            put(snake_pos,snake_body_sym)
        put(snake[-1], snake_head_sym)
        
#-----------------------------------------------------------------------------
#draw and move spiders
#-----------------------------------------------------------------------------
def draw_spiders():
    for spider_pos in spiders:
        put(spider_pos,spider_sym)

def move_spider_up(spider_pos):
    # put blank in current position before moving   
    put(spider_pos, " ")
    if spider_pos["y"] > 0:
        spider_pos["y"] -= 1
        if spider_pos["y"]==player_pos["y"] and spider_pos["x"]==player_pos["x"]:
            exit()       

def move_spider_down(spider_pos):
    # put blank in current position before moving    
    put(spider_pos, " ")
    if spider_pos["y"] < max_y-1: #last line for messages
        spider_pos["y"] += 1
        if spider_pos["y"]==player_pos["y"] and spider_pos["x"]==player_pos["x"]:
            exit()

def move_spider_left(spider_pos):
    # put blank in current position before moving    
    put(spider_pos, " ")
    if spider_pos["x"] > 0:
        spider_pos["x"] -= 1
        if spider_pos["y"]==player_pos["y"] and spider_pos["x"]==player_pos["x"]:
            exit()

def move_spider_right(spider_pos):
    # put blank in current position before moving    
    put(spider_pos, " ")
    if spider_pos["x"] < max_x:
        spider_pos["x"] += 1
        if spider_pos["y"]==player_pos["y"] and spider_pos["x"]==player_pos["x"]:
            exit()
                           
def move_spiders():
    for spider_pos in spiders:
        random.choice([move_spider_right,move_spider_left, move_spider_down, move_spider_up])(spider_pos)

def do_spider_bullet_collisions():
    global bullets
    global spiders

    new_spiders=[pos for pos in spiders if not pos in bullets]
    new_bullets=[pos for pos in bullets if not pos in spiders]

    spiders=new_spiders
    bullets=new_bullets
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

    # Draw spiders
    draw_spiders()
    
    draw_snakes()

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
    do_spider_bullet_collisions()

    move_bullets()

    move_spiders()

    move_snakes()
    
    # resolve consequences of collisions.
    # NOTE: some of these may be best handled by putting code elsewhere
