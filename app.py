import argparse
import curses
from curses import wrapper
import time
from snake import Snake
from apple import Apple
from homescreen import homeScreen, draw_box
import json
from pathlib import Path
from platformdirs import user_data_dir

DATA_DIR = Path(user_data_dir("pixel-snake-tui", "OrAxelerator")) / "data.json"

SNAKE_COLOR = 1
APPLE_COLOR = {
    "normal":2,
    "gold":4,
    "uranium":1,
    "glitch":3
}
INFO_COLOR = 3
MODE_COLOR = 4
GAME_OVER_COLOR = 9
TICK = 0.1
SIDE_BAR_HEIGHT = 3

# q = game_over
# ESCHAP = pause()

def load_data():
    DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_DIR.exists():
        DATA_DIR.write_text(json.dumps({"bestScore": 0}))

    with open(DATA_DIR, "r") as f:
        return json.load(f)


def save_data(data):
    DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR, "w") as f:
        json.dump(data, f)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-apple", type=int, default=1)
    parser.add_argument("-no-colision", action="store_true")
    return parser.parse_args()


def main(stdscr, args):
    curses.curs_set(0)
    
    while True:
        homescreen = homeScreen(stdscr)

        if homescreen == "launch":
            result = game_loop(stdscr, args.apple, collision=args.no_colision)
            if result != "restart":
                break

        elif homescreen == "quit":
            break
            
            

    

def update_direction(key, current, glitched=False):
    if glitched:
        if key in (curses.KEY_UP, ord('k'), ord('K')):
            key = curses.KEY_DOWN
        elif key in (curses.KEY_DOWN, ord('j'), ord('J')):
            key = curses.KEY_UP
        elif key in (curses.KEY_LEFT, ord('h'), ord('H')):
            key = curses.KEY_RIGHT
        elif key in (curses.KEY_RIGHT, ord('l'), ord('L')):
            key = curses.KEY_LEFT

    dy, dx = current

    if key in (curses.KEY_UP, ord('k'), ord('K')) and dy != 1:
        return (-1, 0)
    if key in (curses.KEY_DOWN, ord('j'), ord('J')) and dy != -1:
        return (1, 0)
    if key in (curses.KEY_LEFT, ord('h'), ord('H')) and dx != 1:
        return (0, -1)
    if key in (curses.KEY_RIGHT, ord('l'), ord('L')) and dx != -1:
        return (0, 1)

    return current




def safe_addstr(win, y, x, text, color=0):
    height, width = win.getmaxyx()
    if y < 0 or y >= height or x >= width:
        return
    win.addstr(y, x, text[:max(0, width - x - 1)], color)


def render(win, snake, apple, side, xp, direction, collision, tick, score, glitched=False):
    win.erase()
    draw_box(win)

    for i, (y, x) in enumerate(snake):
        char = "X" if i == 0 else "x"
        win.addch(y, x, char, curses.color_pair(APPLE_COLOR["glitch"] if glitched else SNAKE_COLOR))
    
    for ap in apple:
        # input(ap.type) # lsite ["normal"]
        # input(APPLE_COLOR) # dict
        # input(APPLE_COLOR["normal"]) # 2
        typ = ap.type
        # input(typ)
        win.addch(ap.pos[0], ap.pos[1], "O", curses.color_pair(APPLE_COLOR[typ]))
    win.refresh()

    side.erase()
    draw_box(side)
    mode = "off" if collision else "on"
    dy, dx = direction
    direction_name = {
        (-1, 0): "↑",
        (1, 0): "↓",
        (0, -1): "←",
        (0, 1): "→",
    }.get((dy, dx), "NONE")

    

    safe_addstr(side, 0, 2, " PIXEL SNAKE ", curses.color_pair(MODE_COLOR))
    safe_addstr(side, 1, 2, f"XP {xp}", curses.color_pair(INFO_COLOR))
    safe_addstr(side, 1, 14, f"LEN {len(snake)}", curses.color_pair(SNAKE_COLOR))
    safe_addstr(side, 1, 28, f"APPLE {len(apple)}", curses.color_pair(APPLE_COLOR["normal"]))
    safe_addstr(side, 1, 43, f"COLISION {mode}", curses.color_pair(MODE_COLOR))
    safe_addstr(side, 1, 61, f"BEST {score}", curses.color_pair(INFO_COLOR))
    safe_addstr(side, 2, 2, f" DIR {direction_name} | q quit | r restart | esc pause ", curses.color_pair(INFO_COLOR))
    side.refresh()


def game_over(stdscr, snake, bestScore):
    stdscr.nodelay(False)
    stdscr.clear()
    curses.init_pair(GAME_OVER_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr(0, 0, "GAME OVER - Press [r] to restart or [q] to quit", curses.color_pair(GAME_OVER_COLOR))
    stdscr.refresh()
    if snake > bestScore:
        stdscr.addstr(1, 0, f"NEW RECORD : {snake}", curses.color_pair(MODE_COLOR))
        stdscr.addstr(2, 0, f"Old : {bestScore}", curses.color_pair(INFO_COLOR))
        stdscr.refresh()

        save_data({"bestScore": snake})

    while True:
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            return "quit"
        elif key in (ord('r'), ord('R'), curses.KEY_ENTER, 10, 13):
            return "restart"
    

def game_loop(stdscr, nbAplle, collision):
        SNAKE = Snake(start=(4,4), direction=(0,1), collision=collision)
        NB_APPLE = nbAplle
        APPLE = []
        for i in range(NB_APPLE):
            APPLE.append(Apple())

        glitch_until = 0
        
        # ===== INIT CURSES =====
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(SNAKE.snake_color, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(APPLE_COLOR["normal"], curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(INFO_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(MODE_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        stdscr.nodelay(True)
        stdscr.keypad(True)

        height, width = stdscr.getmaxyx()
        win = curses.newwin(height - SIDE_BAR_HEIGHT, width, SIDE_BAR_HEIGHT, 0)
        win.nodelay(True)
        win.keypad(True)
        game_size = win.getmaxyx()

        side_bar = curses.newwin(SIDE_BAR_HEIGHT, width, 0, 0)
        side_bar.clear()


        data = load_data()

        bestScore = data["bestScore"]

        xp = 0
        # spawn apple init
        for apple in APPLE:
            apple.spawn_apple(SNAKE.snake_body, game_size)

        running = True

        while running:
            time.sleep(TICK)
            key = stdscr.getch()
            if hasattr(curses, "set_escdelay"):
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
                return "quit"
            elif key in (ord('r'), ord('R')) :
                return "restart"
            else:
                pass

            glitched = time.time() < glitch_until
            SNAKE.direction = update_direction(key, SNAKE.direction, glitched)

            new_head = SNAKE.move()

            if collision:
                new_head = SNAKE.wrap_head(new_head, game_size)

            if SNAKE.isCollision(new_head, game_size):
                break

            SNAKE.snake_body.insert(0, new_head)
            for apple in APPLE:
                if new_head == apple.pos:
                    
                    if apple.type == "normal":
                        xp += 100
                        SNAKE.snake_body.insert(0, new_head) # to conter .pop
                    elif apple.type == "gold":
                        xp += 200
                        SNAKE.snake_body.insert(0, new_head) # to conter .pop
                        SNAKE.snake_body.insert(0, new_head) # to conter .pop
                    elif apple.type == "uranium":
                        xp -= 200
                        if len(SNAKE.snake_body) > 2: # cause end : onather pop
                            SNAKE.snake_body.pop()
                    elif apple.type == "glitch" :
                        xp += 100
                        glitch_until = time.time() + 1 # 1s glitch

                    apple.type = apple.init_type() # Change type
                    apple.spawn_apple(SNAKE.snake_body, game_size)

            
            SNAKE.snake_body.pop()


            render(win, SNAKE.snake_body, APPLE, side_bar, xp, SNAKE.direction, collision, TICK, bestScore, glitched=glitched)

        return game_over(stdscr, len(SNAKE.snake_body), bestScore)



def run():
    args = parse_args()
    wrapper(lambda stdscr: main(stdscr, args))
