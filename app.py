import curses
from curses import wrapper
from random import randint
import time
from snake import Snake
from apple import Apple
from homescreen import homeScreen
SNAKE_COLOR = 1
APPLE_COLOR = 2
TICK = 0.1

# q = game_over
# ESCHAP = pause()

def main(stdscr):
    while True:
        homescreen = homeScreen(stdscr)

        if homescreen == "launch":
            result = game_loop(stdscr)
            if result != "restart":
                break

        elif homescreen == "quit":
            break
            
            

    

def update_direction(key, current):
    dy, dx = current
    if key == curses.KEY_UP and dy != 1:
        return (-1, 0)
    if key == curses.KEY_DOWN and dy != -1:
        return (1, 0)
    if key == curses.KEY_LEFT and dx != 1:
        return (0, -1)
    if key == curses.KEY_RIGHT and dx != -1:
        return (0, 1)
    return current




def render(win, snake, apple, side, xp, debug):
    win.erase()
    win.box()

    for i, (y, x) in enumerate(snake):
        char = "X" if i == 0 else "x"
        win.addch(y, x, char, curses.color_pair(SNAKE_COLOR))
    
    for ap in apple:
        win.addch(ap.pos[0], ap.pos[1], "O", curses.color_pair(APPLE_COLOR))
    win.refresh()
    side.addstr(0,0,f"XP : {xp}")
    side.refresh()


def game_over(stdscr):
    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(0, 0, "GAME OVER - Press [r] to restart or [q] to quit")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            return "quit"
        elif key in (ord('r'), ord('R')):
            return "restart"
    

def game_loop(stdscr):
        SNAKE = Snake(start=(4,0), direction=(0,1))
        NB_APPLE = 3
        APPLE = []
        for i in range(NB_APPLE):
            APPLE.append(Apple())
        
        # ===== INIT CURSES =====
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(SNAKE.snake_color, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(APPLE_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)

        stdscr.nodelay(True)
        stdscr.keypad(True)

        height, width = stdscr.getmaxyx()
        win = curses.newwin(height - 2, width, 2, 0)
        win.nodelay(True)
        win.keypad(True)

        side_bar = curses.newwin(3, width, 0, 0)
        side_bar.clear()


        

        xp = 0
        # spawn apple init
        for apple in APPLE:
            apple.spawn_apple(SNAKE.snake_body, (height, width))

        running = True

        while running:
            time.sleep(TICK)
            key = stdscr.getch()
            curses.set_escdelay(25)
            if key == 27: 
                stdscr.nodelay(False) 
                while True:
                    time.sleep(1)
                    key = win.getch()
                    if key == 27: #ECHAP
                        
                        stdscr.nodelay(True)
                        break
            elif key in (ord('q'), ord('Q')):
                break
            elif key in (ord('r'), ord('R')):
                pass
            else:
                pass


            SNAKE.direction = update_direction(key, SNAKE.direction)

            new_head = SNAKE.move()

            if SNAKE.colision(new_head, (height, width)):
                break

            SNAKE.snake_body.insert(0, new_head)
            for apple in APPLE:
                if new_head == apple.pos:
                    apple.spawn_apple(SNAKE.snake_body, (height, width))
                    xp += 100
                    SNAKE.snake_body.insert(0, new_head) # to conter .pop


            SNAKE.snake_body.pop()


            render(win, SNAKE.snake_body, APPLE, side_bar, xp, SNAKE.direction)

        return game_over(stdscr)

wrapper(main)
