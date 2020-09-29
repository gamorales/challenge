#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# Obtained from https://github.com/jacklam718/cursesDialog

import curses
import sys

encoding = sys.getdefaultencoding()


def rectangle(win, begin_y, begin_x, height, width, attr):
    win.vline(begin_y, begin_x, curses.ACS_VLINE, height, attr)
    win.hline(begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.hline(height+begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.vline(begin_y, begin_x+width, curses.ACS_VLINE, height, attr)
    win.addch(begin_y, begin_x, curses.ACS_ULCORNER,  attr)
    win.addch(begin_y, begin_x+width, curses.ACS_URCORNER,  attr)
    win.addch(height+begin_y, begin_x, curses.ACS_LLCORNER, attr)
    win.addch(begin_y+height, begin_x+width, curses.ACS_LRCORNER, attr)
    win.refresh()


class CursBaseDialog:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        self.win = curses.newwin(20, 110, int((self.maxy/2)-6), int((self.maxx/2)-48))
        self.win.box()
        self.y, self.x = self.win.getmaxyx()
        self.title_attr = options.get('title_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr = options.get('msg_attr',   curses.A_BOLD)
        self.opt_attr = options.get('opt_attr',   curses.A_BOLD)
        self.focus_attr = options.get('focus_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.title = options.get('title',      curses.A_BOLD)
        self.message = options.get('message', '')
        self.win.addstr(0, 0, ' '*110, self.title_attr)
        self.win.keypad(1)
        self.focus = 0
        self.enterKey = False
        self.win.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

    def left_right_key_event_handler(self, max):
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max-1:
            self.focus += 1
        elif key == ord('\n'):
            self.enterKey = True


class ShowMessageDialog(CursBaseDialog):
    def showMessage(self):
        if self.title:
            self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, self.title_attr)

        if type(self.message) == tuple:
            counter = 0
            for options in self.message:
                self.win.addstr(counter, 2, options[1], self.msg_attr)
                counter += 1
        else:
            for (i, msg) in enumerate(self.message.split('\n')):
                self.win.addstr(i+1, 2, msg, self.msg_attr)

        rectangle(self.win, 14, int(self.x/2-2), 2, 3, self.opt_attr | self.focus_attr)
        self.win.addstr(15, int(self.x/2-1), 'Ok', self.opt_attr | self.focus_attr)
        if self.win.getch() != ord('\n'):
            self.showMessage()
