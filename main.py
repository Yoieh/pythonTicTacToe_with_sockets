#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is my atempt to code a Tic Tac Toe that uses sokets for remote multiplayer.
I ran out of time and i had to rush the code together
but it works just not fine.
Try it local with to terminals.
Havent tryed it on two computers yet but it should work.
"""
import server_handler
import game
import display

Game = game.Game()
Server = server_handler.Server_Handler()
Messages = server_handler.Messages()

Screen = display.Display()

Board = game.Board()


def turn(player_name):
    '''This is the main turn function. Takes a str(player_name)
    the name of the local player and going throu alot of cheks.
    Its a bad writen functoin.
    exits if a player dosent want to play any more after someone has won.
    '''
    # this is the marker of the player hos turn it is.
    currnet_marker = Game.game_info['players_info'][
        Game.game_info['current_player']]['mark_type']

    # check if some one has won, lopping tho the players
    for player in Game.game_info['players']:
        # getting the mark from each player
        player_mark = Game.game_info['players_info'][player]['mark_type']

        # cheking if the players has won
        if Board.winns(player_mark):
            # The sring used in "the new game?" dialog
            win_str = player + ' winns. Play agin? Y/n'
            new = Screen.dialog(win_str, 1)
            # cheking the input fom new game dialoge
            if new == 'Y' or new == 'y':

                Board.new()  # creating a clean new screen
                Game.board = Board.game_board  # cleanig the old board
                Game.update_game_info()  # updating the game info.

            else:
                # exit action. Instad of listening or connecting
                Screen.action = 'exit'
                return True  # return to exit the function

    Board.display()  # creating the displayebol board from the board
    # Showing the game screen.
    Screen.game(Board.display_board, Game.game_info, player_name)
    # cheks if the Screen.input is cleean enough to move on.
    if Screen.clean_input():

        # updating the boads from the inputed location from the player
        if Board.update(int(Screen.input[0]), int(Screen.input[1]),
                        currnet_marker):

            # Cangching players turn
            Game.turn()

            # doing a check if the palyer has won agin
            # cheking if the players has won
            if Board.winns(player_mark):
                # The sring used in "the new game?" dialog
                win_str = player + ' winns. Play agin? Y/n'
                new = Screen.dialog(win_str, 1)
            # cheking the input fom new game dialoge
                if new == 'Y' or new == 'y':

                    Board.new()  # creating a clean new screen
                    Game.board = Board.game_board  # cleanig the old board
                    Game.update_game_info()  # updating the game info.

                else:
                    # exit action. Instad of listening or connecting
                    Screen.action = 'exit'
                    return True  # return to exit the function

            Board.display()  # creating the displayebol board from the board
            # Showing the game screen.
            Screen.game(Board.display_board, Game.game_info, player_name)

        else:  # if the inputed position is not empty we will run the functin again.
            turn(player_name)
    else:  # if Screen.input is not clean whe run the this function again
        turn(player_name)


while Game.run:

    Screen.main()  # run the main Screen method to wrapp the screen

    if Screen.action == 'listen':  # player chosed to listen after players

        if Server.connected == False:  # cheks if a conection allready exists.
            name = Screen.dialog('Player Name: ', 20)
            playerO = game.Player(name, 'O')  # Creating playerO
            # Adding the new playerO to the list of players in the Game
            # object.
            # Adding the first player to our player list
            Game.players.append(playerO.player['name'])
            Game.update_players_info(playerO.player)  # Updating player info
            Game.update_game_info()  # Updating the main game info

            # getting the ip of the player by showing the player a dialog.
            server_ip = Screen.dialog('Your Ip: ', 12)

            # if server_ip is left empty we set the ip to local adress.
            if server_ip == '':
                server_ip = '127.0.0.1'

            Screen.listen()  # shoing the listen screen
            Server.server(server_ip)  # starting the Server.
            Server.listen()  # setting the server to listen after conection.

            in_msg = Messages.decode(Server.data)  # decoding the resaved msg
            # creating playerX by the decoded msg
            playerX = game.Player(in_msg['players'][0], 'X')
            # Adding the new playerX to the list of players in the Game
            # object.
            Game.players.append(playerX.player['name'])

            Game.update_players_info(
                in_msg['players_info'][playerX.player['name']])
            Game.update_game_info()  # updating then main game info.
            # We need to update the game info befor roling the dice
            if Game.dice():  # determine whos starting.
                board = game.Board()  # creating the game Board.
                # adding the game board to the Game object.
                Game.board = Board.game_board
                Game.update_game_info()  # updating the game info.

            # encoding game_info
            out_msg = Messages.encode(Game.game_info)
            Server.send(out_msg)  # sending all the game_info to the client.

        elif Server.connected == True:
            # decoding the message from the client.
            in_msg = Messages.decode(Server.data)
            # syncing the main game info from the message.
            Game.sync(in_msg)
            # syncing the game bord.
            Board.sync(in_msg['board'])
            # check if it is this players turn.
            if Game.game_info['current_player'] == playerO.player['name']:
                # rungin the bad writen turn function.
                turn(playerO.player['name'])
            # encoding the man game info agin.
            out_msg = Messages.encode(Game.game_info)
            # sending the encoded message.
            Server.send(out_msg)
        # setting the server to listen for messages from client
        Server.listen()

    elif Screen.action == 'connect':  # player chosed to connct to a server.

        if Server.connected == False:
            # getting hte players name by showing a dialog.
            name = Screen.dialog('Player Name: ', 20)
            # creating a player
            playerX = game.Player(name, 'X')

            # getting the servers ip by showing the player a dialog.
            server_ip = Screen.dialog('Servers Ip: ', 12)

            # if server ip left empty we set the ip to local adress.
            if server_ip == '':
                server_ip = '127.0.0.1'

            # showing a connecting to server screen på the player.
            Screen.connect()

            Game.update_players_info(playerX.player)
            # Adding the local player to players.
            Game.players = [playerX.player['name']]
            Game.update_game_info()  # Updating main game info.

            # encoding main game info.
            out_msg = Messages.encode(Game.game_info)
            # conecting to the server an sending the encoded message to the
            # server.
            Server.clinet(server_ip, out_msg)

            # creating a empty board in the in the Board object.
            Board.new()

            # listen after servers answer.
            Server.listen()

            # when server has answerd the data gets decoded.
            in_msg = Messages.decode(Server.data)

            # Creating the remote players player object.
            PlayerO = game.Player(in_msg['players'][1], 'O')

            # Syncing main game info from the message.
            # Mearging the msg data with the allready existing data.
            Game.sync(in_msg)

            # Encoding the main game info.
            out_msg = Messages.encode(Game.game_info)
            # Sending the encoded main game info to the server.
            Server.send(out_msg)

        elif Server.connected == True:

            # decoding the message sent form the server.
            in_msg = Messages.decode(Server.data)
            # syncing the game info with the decoded message.
            Game.sync(in_msg)
            # syncing the Board object.
            Board.sync(in_msg['board'])

            # cheking if it is this players turn.
            if Game.game_info['current_player'] == playerX.player['name']:

                # calling the bad writen turn functin.
                turn(playerX.player['name'])
            # encoding the main game info
            out_msg = Messages.encode(Game.game_info)
            # sending the encoded game info to the server
            Server.send(out_msg)

        # setting the client to listen after messages from the server
        Server.listen()

    elif Screen.action == 'exit':
        Server.close()
        Game.exit_game()  # exiting the game
        Screen.exit_display()
        # here we even should send a message to the server/client that we want
        # to close the game but i havet bother with that yet.


# closing the server
Server.close()

exit(0)
