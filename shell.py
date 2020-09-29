import curses

from dialog import ShowMessageDialog


screen = None
g = {}
ENTER = [curses.KEY_ENTER, 10]
DELETE = [curses.KEY_BACKSPACE, curses.KEY_DC, 8, 127, 263]
SHELL_COLOR = curses.COLOR_BLUE

# Init curses screen
screen = curses.initscr()
screen.keypad(1)
curses.noecho()
try:
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
except curses.error:
    pass

curses.cbreak()
g['height'], g['width'] = screen.getmaxyx()


def close_window():
    global screen
    screen.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def print_help():
    message = """
help: Prints help dialog
exit: Exits
"""
    msg = ShowMessageDialog(message=message, title='Challenge Help')
    msg.showMessage()


def main():
    word = ""
    shell = "challenge >>> "

    screen.addstr(f"\n{shell}", curses.color_pair(SHELL_COLOR))

    while True:
        # Current position
        y, x = screen.getyx()
        try:
            # Get char
            event = screen.getch()
            try:
                char = chr(event)
            except:
                char = ''
        except KeyboardInterrupt:
            break

        # Enter key
        if event in ENTER:
            screen.clrtobot()

            if word == "exit":
                break
            elif word == "help":
                print_help()

            # Touch the screen's end
            if y - g['height'] > -3:
                screen.addstr(y, 0, shell, curses.color_pair(SHELL_COLOR))
            else:
                screen.addstr(y+1, 0, shell, curses.color_pair(SHELL_COLOR))

            word = ''

        # Delete key
        elif event in DELETE:
            # Touch to line start
            if x < len(shell) + 1:
                screen.move(y, x)
                word = ''
            # Midle of line
            else:
                word = word[:-1]
                screen.move(y, x-1)
                screen.clrtoeol()
                screen.move(y, x-1)

        else:
            # Explicitly print char
            screen.addstr(char)
            word += char
            screen.move(y, x+1)

    # Reset
    close_window()


if __name__ == "__main__":
    main()
