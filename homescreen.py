import curses
MENU_BORDER_COLOR = 5
MENU_TITLE_COLOR = 6
MENU_SELECTED_COLOR = 7
MENU_OPTION_COLOR = 8

def homeScreen(stdscr):
    stdscr.clear()
    curses.start_color()
    curses.init_pair(MENU_BORDER_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(MENU_TITLE_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(MENU_SELECTED_COLOR, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(MENU_OPTION_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0, 0)
    win.keypad(True)
    win.attron(curses.color_pair(MENU_BORDER_COLOR))
    win.border()
    win.attroff(curses.color_pair(MENU_BORDER_COLOR))
    title = " PIXEL SNAKE "
    win.addstr(0, max(1, width // 2 - len(title) // 2), title, curses.color_pair(MENU_TITLE_COLOR))
    # win.addstr(3, 3, "tset")
    selection = 0
    option = ["Lauch game", "Quit game"]
    win.refresh()
    display_param_option(win, option, selection, gap_y=1)
    while True:
        key = win.getch()
        if key in (ord('q'), ord('Q')):
            return "quit"
        elif key in (ord('a'), ord('A')):
            win.addstr(0,0,"aaaaaaa")
            win.refresh()
        elif key == curses.KEY_UP:
            selection   = max(0, selection-1)
            display_param_option(win, option, selection, gap_y=1)
        elif key == curses.KEY_DOWN:
            selection = min(len(option)-1, selection+1,)
            display_param_option(win, option, selection, gap_y=1)
        elif key in (ord(' '), curses.KEY_ENTER, 10, 13):
            if selection == 0:
                return "launch"
            elif selection == 1:
                return "quit"


def display_param_option(win, option: list, selection, gap_y=1):
    height, width = win.getmaxyx()

    max_len = max(len(el) for el in option) + 2  # +2 pour "> "

    total_height = len(option) + (len(option) - 1) * gap_y
    start_y = height // 2 - total_height // 2

    for i, el in enumerate(option):
        ch = ">" if selection == i else " "
        text = f"{ch} {el}".ljust(max_len)

        pos_y = start_y + i * (1 + gap_y)
        pos_x = width // 2 - max_len // 2

        color = curses.color_pair(MENU_SELECTED_COLOR if selection == i else MENU_OPTION_COLOR)
        win.addstr(pos_y, pos_x, text, color)

    win.refresh()
