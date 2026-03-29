import curses
from curses import wrapper
from random import randint
import time


SNAKE_COLOR = 1
APPLE_COLOR = 2
TICK = 0.1

# q = game_over
# ESCHAP = pause()

def main(stdscr):
    # ===== INIT CURSES =====
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(SNAKE_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(APPLE_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.nodelay(True)
    stdscr.keypad(True)

    height, width = stdscr.getmaxyx()
    win = curses.newwin(height - 2, width, 2, 0)
    win.nodelay(True)
    win.keypad(True)

    side_bar = curses.newwin(3, width, 0, 0)
    side_bar.clear()

    snake = [(5, 5),(4,5)]
    direction = (0, 1)  # droite
    apple = spawn_apple(win, snake)
    xp = 0

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


        direction = update_direction(key, direction)

        new_head = move_snake(snake[0], direction)

        if collision(new_head, snake, win):
            break

        snake.insert(0, new_head)

        if new_head == apple:
            apple = spawn_apple(win, snake)
            xp += 100
        else:
            snake.pop()

        render(win, snake, apple, side_bar, xp)

    game_over(stdscr)


def spawn_apple(win, snake):
    h, w = win.getmaxyx()
    while True:
        pos = (randint(1, h - 4), randint(1, w - 4))
        if pos not in snake:
            return pos


    

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


def move_snake(head, direction):
    y, x = head
    dy, dx = direction
    return (y + dy, x + dx)


def collision(head, snake, win):
    h, w = win.getmaxyx()
    y, x = head
    if y <= 0 or y >= h - 1 or x <= 0 or x >= w - 1:
        return True
    if head in snake:
        return True
    return False


def render(win, snake, apple, side, xp):
    win.erase()
    win.box()

    for i, (y, x) in enumerate(snake):
        char = "X" if i == 0 else "x"
        win.addch(y, x, char, curses.color_pair(SNAKE_COLOR))
        
    win.addch(apple[0], apple[1], "O", curses.color_pair(APPLE_COLOR))
    win.refresh()
    side.addstr(0,0,f"Point d'XP : {xp}")
    side.refresh()


def game_over(stdscr):
    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.addstr(0, 0, "GAME OVER - Press any key [r] to restart")
    stdscr.refresh()
    stdscr.getch()
    

wrapper(main)
