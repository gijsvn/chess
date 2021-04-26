from chess_env import *
from util import *

field = initialize_field()
checkmate = False
draw = False
player = 'w'
turn = 0
while not checkmate and not draw:
    print(turn, end = '\r')
    if not turn%100:
        print(field)
    turn += 1
    initial_check = check_if_check(field, player)

    moves = get_possible_moves(field, player)
    while 1:
        if player == 'w':
            best_move_score = -1
            for piece in moves.keys():
                for move in moves[piece]:
                    #print(field)
                    test_field = execute_move(field, piece, move)
                    #input(field)
                    if not check_if_check(test_field, player):
                        network_input = np.array([process_field(test_field)])
                        score = model.predict(network_input)[0][0]
                        if score > best_move_score:
                            best_piece = piece
                            best_move = move
                            best_move_score = score

            piece, move = best_piece, best_move
        else:
            piece = (0, 0)
            piece[0] = input("enter row for piece")
            piece[1] = input("enter column for piece")
            move = (0, 0)
            move[0] = input("enter row for new position")
            move[1] = input("enter column for new position")

            test_field = execute_move(field, piece, move)
            while check_if_check(temp_field, player):
                print('you checked yourself mate')
                piece = (0, 0)
                piece[0] = input("enter row for piece")
                piece[1] = input("enter column for piece")
                move = (0, 0)
                move[0] = input("enter row for new position")
                move[1] = input("enter column for new position")
                test_field = execute_move(field, piece, move)

        new_field = execute_move(field, piece, move).copy()
        if not check_if_check(new_field, player):
            field = new_field
            break
        else:
            input("got heree")

    if player == 'w':
        player = 'b'
    else:
        player = 'w'

    if not draw and not checkmate:
        draw = not check_if_sufficient_material(field)
        checkmate = check_if_checkmate(field, player)

if checkmate:
    if player == 'w':
        winner = 'b'
        print(f'{winner} won!')
    else:
        winner = 'w'
        print(f'{winner} won!')
else:
    print("draw... :(")
