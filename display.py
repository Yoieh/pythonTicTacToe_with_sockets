# -*- coding: utf-8 -*-

import curses
import curses.textpad
import time


class Display(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.dimes = self.screen.getmaxyx()
        self.show_screen = 'start_menu'
        self.action = ''
        self.input = ''

    def main(self):
        curses.wrapper(self.display)

    def dialog(self, msg, input_with):

        dimes = self.dimes

        max_with = len(msg) + 4 + input_with
        max_hight = 4

        dialog = curses.newwin(
            max_hight, max_with, dimes[0] / 2 - (6 / 2), dimes[1] / 2 - (max_with / 2))

        dialog.border()
        dialog.addstr(1, 1, msg)
        dialog.refresh()
        q = dialog.getstr()

        dialog.clear()
        dialog.refresh()
        return q

    def noinput_dialog(self, msg):
        dimes = self.dimes

        max_with = len(msg) + 4
        max_hight = 4

        dialog = curses.newwin(
            max_hight, max_with, dimes[0] / 2 - (6 / 2), dimes[1] / 2 - (max_with / 2))
        dialog.border()
        dialog.addstr(1, 1, msg)
        dialog.refresh()

    def listen(self):
        self.noinput_dialog('Listen after players..')

    def connect(self):
        self.noinput_dialog('Connecting to players..')

    def start_menu(self):
        dimes = self.dimes

        menu_list = ['Chose from the list below, the * dosent work yet!',
                     ' * (M) Start Local (M)ultiplayer',
                     ' (L) Start (L)istening after players',
                     ' (C) Start server for players to (C)onnect',
                     ' (E) (E)xit Tic-Tac-Toe']

        max_with = len(max(menu_list, key=len)) + 4
        max_hight = len(menu_list) + 2

        menu = curses.newwin(
            max_hight, max_with, dimes[0] / 2 - (6 / 2), dimes[1] / 2 - (max_with / 2))
        menu.border()

        menu.addstr(1, 1, menu_list[0])
        menu.addstr(2, 1, menu_list[1])
        menu.addstr(3, 1, menu_list[2])
        menu.addstr(4, 1, menu_list[3])
        menu.addstr(5, 1, menu_list[4])

        menu.refresh()

        q = menu.getch()

        if q == ord('M') or q == ord('m'):
            self.show_screen = '*'
            menu.clear()
            menu.refresh()
        if q == ord('L') or q == ord('l'):
            self.show_screen = 'listen'
            self.action = 'listen'
            menu.clear()
            menu.refresh()
        if q == ord('C') or q == ord('c'):
            self.show_screen = 'connect'
            self.action = 'connect'
            menu.clear()
            menu.refresh()
        if q == ord('E') or q == ord('e'):
            self.show_screen = 'quit'
            menu.clear()
            menu.refresh()
            exit(0)

    def game(self, bord, game_info, player_name):

        dimes = self.dimes

        options_box = curses.newwin(3, dimes[1], 0, 0)
        player1_box = curses.newwin(6, dimes[1] / 2, 2, 0)
        player_box = curses.newwin(6, dimes[1] / 2, 8, 0)
        game_bord_box = curses.newwin(
            dimes[0] - 2, dimes[1] / 2 + 1, 2, dimes[1] / 2)

        options_box.border()
        player1_box.border()
        player_box.border()
        game_bord_box.border()

        options_box.addstr(1, 1, 'Menu')

        player1_info = game_info['players_info'][game_info['players'][0]]
        player2_info = game_info['players_info'][game_info['players'][1]]

        player1_box.addstr(1, 1, 'Name: ' + player1_info['name'])
        player1_box.addstr(2, 1, 'Score: ' + str(player1_info['score']))
        player1_box.addstr(3, 1, 'Marker: ' + player1_info['mark_type'])
        player1_box.addstr(4, 1, 'Address: ' + player1_info['address'])

        player_box.addstr(1, 1, 'Name: ' + player2_info['name'])
        player_box.addstr(2, 1, 'Score: ' + str(player2_info['score']))
        player_box.addstr(3, 1, 'Marker: ' + player2_info['mark_type'])
        player_box.addstr(4, 1, 'Address: ' + player2_info['address'])

        row_num = 1
        for row in bord:
            col_num = 1
            for col in row:
                game_bord_box.addch(row_num, col_num, self.translater(col))
                col_num += 1
            row_num += 1

        if player_name == game_info['current_player']:
            game_bord_box.addstr(row_num, 1, 'Input : ')
        else:
            game_bord_box.addstr(
                row_num, 1, 'Waiting for ' +
                game_info['current_player'] + ' move..')

        options_box.refresh()
        player1_box.refresh()
        player_box.refresh()
        game_bord_box.refresh()

        if player_name == game_info['current_player']:
            self.input = game_bord_box.getstr()

    def display(self, screen):

        screen.clear()
        self.dimes = screen.getmaxyx()

        screen.refresh()
        if self.show_screen == 'quit':
            return
        elif self.show_screen == 'start_menu':
            self.start_menu()

    def clean_input(self):
        if len(self.input) == 2:
            if self.input[1] == 'A':
                self.input = str(int(self.input[0]) - 1) + '0'
            elif self.input[1] == 'B':
                self.input = str(int(self.input[0]) - 1) + '1'
            elif self.input[1] == 'C':
                self.input = str(int(self.input[0]) - 1) + '2'
            else:
                return False
            if int(self.input[0]) == 0 or int(self.input[0]) == 1 or int(self.input[0]) == 2:
                return True
            else:
                return False
        else:
            return False

    def translater(self, c):

        if c == '[':
            out_c = curses.ACS_ULCORNER
        elif c == '}':
            out_c = curses.ACS_LRCORNER
        elif c == '{':
            out_c = curses.ACS_LLCORNER
        elif c == ']':
            out_c = curses.ACS_URCORNER

        elif c == 'T':
            out_c = curses.ACS_TTEE
        elif c == 't':
            out_c = curses.ACS_BTEE
        elif c == '>':
            out_c = curses.ACS_RTEE
        elif c == '<':
            out_c = curses.ACS_LTEE

        elif c == '-':
            out_c = curses.ACS_HLINE
        elif c == '|':
            out_c = curses.ACS_VLINE
        elif c == '+':
            out_c = curses.ACS_PLUS

        elif c == 'A':
            out_c = ord('A')
        elif c == 'B':
            out_c = ord('B')
        elif c == 'C':
            out_c = ord('C')
        elif c == 'X':
            out_c = ord('X')
        elif c == 'O':
            out_c = ord('O')
        elif c == ' ':
            out_c = ord(' ')
        elif c == '':
            out_c = ord('')
        else:
            out_c = ord(c)

        return out_c

    def exit_display(self):
        exit(0)
