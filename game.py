# -*- coding: utf-8 -*-

import random


class Game():
    """
    This class is used as a core class for all the information about the game.
    """

    def __init__(self):
        self.run = True
        self.game_run = False
        self.players = []
        self.players_info = {}
        self.current_player = ''
        self.board = []
        self.msg = ''
        self.game_info = {}  # this is only used to get info not to post

    def update_game_info(self):
        self.game_info = {
            'players': self.players,
            'players_info': self.players_info,
            'current_player': self.current_player,
            'board': self.board,
            'msg': self.msg
        }

    def update_players_info(self, player_info):
        """
        updateing the basic players_info
        """
        self.players_info[player_info['name']] = player_info

    def sync(self, game_info):
        """
        Syncing the old main game_info with the new main game_info
        """
        self.current_player = game_info['current_player']
        self.players = game_info['players']
        self.board = game_info['board']

        for player in game_info['players_info']:
            self.update_players_info(game_info['players_info'][player])

        self.update_game_info()

    def turn(self):
        """
                Changin the currnet player to the next.
        """
        if self.game_info['current_player'] == self.game_info['players'][0]:
            self.current_player = self.game_info['players'][1]
            self.update_game_info()
            return True
        elif self.game_info['current_player'] == self.game_info['players'][1]:
            self.current_player = self.game_info['players'][0]
            self.update_game_info()
            return True
        else:
            return False

    def dice(self):
        """
        Chosing the player that will start there move
        """
        num = random.randint(0, 100)
        num_of_players = len(self.game_info['players'])

        line = 100 / num_of_players
        x = 0

        while x < num_of_players:
            # Cheking if num is in range of numbers
            if x * line <= num <= (x * line) + line:
                self.current_player = self.game_info['players'][x]
                self.update_game_info()
                return True
            else:
                x = x + 1
        return False

    def exit_game(self):
        self.game_run = False


class Board():
    """
        Class for the board
    """

    def __init__(self):
        self.game_board = [[]]
        self.display_board = []
        self.new()

    def new(self):
        """
        creates new game_board dictionarie with empty lists as valus
                returns True
        """
        self.game_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        return True

    def sync(self, board):
        """
        syncing the old board with the new on
        """
        self.game_board = board
        return True

    def update(self, x, y, p):
        """
        Updating the game_board on that position inputed
        x = position of makrer
        y = position of marker
        p = the carakter you want to plaes down.

        inputs int(x), int(y), str(p)
                checks if list[x][y] is empty
                return True or False
        """
        if self.game_board[int(x)][int(y)] != ' ':
            return False
        else:
            self.game_board[x][y] = p
        return True

# displays the board
# returns True
    def display(self):
        """
        Creates a displayable plays holder for the game board.
        Saving a list into self.display_board.
        """
        game_board = self.game_board
        display_board = []

        first_row = '[---T---T---T---]'
        second_row = '|   | A | B | C |'
        middel_row = '<---+---+---+--->'
        last_row = '{---t---t---t---}'

        display_board.append(first_row)
        display_board.append(second_row)
        i = 0
        while i < len(game_board):
            display_board.append(middel_row)
            row = '| ' + str(i + 1) + ' | ' + str(game_board[i][0]) + ' | ' + str(
                game_board[i][1]) + ' | ' + str(game_board[i][2]) + ' |'
            display_board.append(row)
            i = i + 1
        display_board.append(last_row)

        self.display_board = display_board  # saving the new display list

        return True

    def full_board(self):
        board = self.game_board
        if board[0][0] != ' ' and board[0][1] != ' ' and board[0][2] != ' ' and board[1][0] != ' ' and board[1][1] != ' ' and board[1][2] != ' ' and board[2][0] != ' ' and board[2][1] != ' ' and board[2][2] != ' ':
            return True
        else:
            return False

    def winns(self, l):
        """
        Checkts all the possible wining senarums.
        returns True or False if no wan has won
        """
        return (
            # Top vertical
            (self.game_board[0][0] == l and
             self.game_board[0][1] == l and
             self.game_board[0][2] == l) or
            # Bottom vetical
            (self.game_board[0][2] == l and
             self.game_board[1][2] == l and
             self.game_board[2][2] == l) or
            # Right horizontal
            (self.game_board[0][0] == l and
             self.game_board[1][0] == l and
             self.game_board[2][0] == l) or
            # Right diagonal
            (self.game_board[0][0] == l and
             self.game_board[1][1] == l and
             self.game_board[2][2] == l) or
            # Middle horizontal
            (self.game_board[0][1] == l and
             self.game_board[1][1] == l and
             self.game_board[2][1] == l) or
            # Middle vertical
            (self.game_board[1][0] == l and
             self.game_board[1][1] == l and
             self.game_board[1][2] == l) or
            # Left horizontal
            (self.game_board[2][0] == l and
             self.game_board[2][1] == l and
             self.game_board[2][2] == l) or
            # Left diagonal
            (self.game_board[0][2] == l and
             self.game_board[1][1] == l and
             self.game_board[2][0] == l))


class Player():
    """
    Basic player inforamtion about. One for each player.
    """

    def __init__(self, name, mark):
        self.name = name
        self.mark_type = mark
        self.score = 0
        self.address = ''
        self.player = {}
        self.update_player()

    def add_score(self):
        self.score = self.score + 1
        self.update_player()
        return True

    def add_address(self, address):
        self.address = address
        self.update_player()
        return True

    def update_player(self):
        self.player = {'name': self.name,
                       'mark_type': self.mark_type,
                       'score': self.score,
                       'address': self.address}
        return True
