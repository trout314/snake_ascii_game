import curses    # for displaying text to screen
import time      # for time related tasts
import atexit    # for running code when program exits

#-----------------------------------------------------------------------------
# Set up curses window
#-----------------------------------------------------------------------------
scr = curses.initscr() # initialize a curses screen, scr
curses.noecho()        # turn off printing keyboard input to screen
curses.curs_set(False) # disable blinky cur.sor
curses.cbreak()        # don't wait for enter key to get input
scr.nodelay(True)      # don't wait for key press in getch()
scr.keypad(True)       # enable special values for arrow, pageup keys etc

#-----------------------------------------------------------------------------
# At program exit, put terminal back the way it was and close curses window
#-----------------------------------------------------------------------------
def clean_up():
    # NOTE: Uncomment this next line to see debugging messages
    time.sleep(5)
    curses.echo()
    curses.curs_set(True)
    curses.nocbreak()
    scr.nodelay(False)
    scr.keypad(False)
    curses.endwin()

atexit.register(clean_up)
