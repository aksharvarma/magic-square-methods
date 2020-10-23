import curses
import utilities as U

def curses_init():              # Create a window and initialize curses
    stdscr = curses.initscr()   # initialize curses screen
    curses.noecho()             # turn off auto echoing of keypress on to screen
    curses.cbreak()             # enter break mode where pressing Enter key
                                # after keystroke is not required for it to register
    stdscr.keypad(1)            # enable special Key values like curses.KEY_LEFT etc.

    curses.start_color()
    curses.curs_set(False)
    return stdscr

def curses_close(stdscr):       # Exit curses gracefully
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def pause_for(delay=500):       # for readability
    curses.napms(delay)

def get_column(j, display_size):
    # The initial 2 is for numpy's double [[ start to a matrix
    # The +1 is for the gap between two column entries
    # The display size is for the space the number takes up.
    # j is the number of numbers
    return 2+(display_size+1)*j

def print_cell(w, m, i, j, delay=500, base_yx=None):
    '''
    When the [i, j] entry of matrix m gets updated, reprint just that.
    '''
    n = m.shape[0]
    display_size = U.get_display_size(n)
    base_y, base_x = base_yx if base_yx is not None else (0, 0)
    x, y = base_x + get_column(j, display_size), base_y + i

    pause_for(delay)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    display_format_string = U.get_display_format_string(n)
    if curses.has_colors():
        w.addstr(y, x, display_format_string.format(m[i, j]), curses.color_pair(3))
    else:
        w.addstr(y, x, display_format_string.format(m[i, j]))
    w.refresh()
