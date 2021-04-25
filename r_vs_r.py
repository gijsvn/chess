import numpy as np

from chess_env import *
from util import *

INITIAL_GAMES = 10000
games = {'b':0, 'w':0, 'D':0}

for game in range(INITIAL_GAMES):
    if not game%50:
        print(f"{game}/{INITIAL_GAMES}", end = "\r")
    game_memory = {'X':[], 'y':[]}
    field = initialize_field()
    checkmate = False
    draw = False
    player = 'w'
    while not checkmate and not draw:
        initial_check = check_if_check(field, player)

        moves = get_possible_moves(field, player)

        while 1:
            piece, move = pick_random_move(moves)
            new_field = execute_move(field, piece, move)
            if not check_if_check(new_field, player):
                field = new_field
                break
            else:
                #potential move led to being checked
                moves[piece].remove(move)

                #if all moves led to being checked either checkmate or draw
                if sum(moves.values(), []) == []:
                    if initial_check:
                        checkmate = True
                        break
                    else:
                        draw = True
                        break

        if player == 'w':
            player = 'b'
        else:
            player = 'w'

        if not checkmate and not draw:
            draw = not check_if_sufficient_material(field)
            checkmate = check_if_checkmate(field, player)

    if checkmate:
        if player == 'w':
            winner = 'b'
        else:
            winner = 'w'

        games[winner] += 1
    else:
        games['D'] += 1

for outcome in games.keys():
    print(f"{outcome}:")
    print(f"\t{(games[outcome]/INITIAL_GAMES)*100:.2f}")
