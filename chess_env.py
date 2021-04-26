import numpy as np
import random

def test_field():
    field = np.empty(shape = (8, 8), dtype = object)

    for _ in range(8):
        field[_] = np.array(["    " for _ in range(8)])

    field[7, 5] = "wBis"
    field[6, 6] = "wKin"

    return field

def initialize_field():
    """
    function that returns an 8 by 8 matrix of strings representing the playing field
    """
    field = np.empty(shape = (8, 8), dtype = object)

    for _ in range(2, 6):
        field[_] = np.array(["    " for _ in range(8)])

    field[0] = np.array(["bRok", "bKni", "bBis", "bQue", "bKin", "bBis", "bKni", "bRok"])
    field[1] = np.array(["bPwn" for _ in range(8)])
    field[6] = np.array(["wPwn" for _ in range(8)])
    field[7] = np.array(["wRok", "wKni", "wBis", "wQue", "wKin", "wBis", "wKni", "wRok"])

    return field

def get_possible_moves(field, player):
    """
    given current state (playing field and player who's turn it is),
    returns a dictionary where the keys are the player's pieces and the values
    are lists of coordinates for possible moves
    """

    if player == 'w':
        op = 'b'
    else:
        op = 'w'

    def get_pawn_moves(field, position):
        allowed_indices = [x for x in range(8)]
        moves = []

        #determine at which row pawns can move 2 squares and which way pawns move
        if player == 'w':
            start = 6
            m = -1
        else:
            start = 1
            m = 1

        #check if allowed to move 2 squares
        if position[0] == start and field[position[0] + 2*m, position[1]] == "    ":
            moves.append((position[0] + 2*m, position[1]))

        #check if pawns can take opponent's material
        if position[0] + 1*m in allowed_indices and position[1] - 1 in allowed_indices and field[position[0] + 1*m, position[1] - 1][0] == op:
            moves.append((position[0] + 1*m, position[1] - 1))
        if position[0] + 1*m in allowed_indices and position[1] + 1 in allowed_indices and field[position[0] + 1*m, position[1] + 1][0] == op:
            moves.append((position[0] + 1*m, position[1] + 1))

        #check if possible to move 1 forward
        if position[0] + 1*m in allowed_indices and field[position[0] + 1*m, position[1]] == "    ":
            moves.append((position[0] + 1*m, position[1]))

        return moves

    def get_knight_moves(field, position):
        allowed_indices = [x for x in range(8)]
        moves = []

        #set different combinations of directions and distances for knight movements
        values = [[1, 2], [2, 1]]
        multipliers = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

        #check if move is allowed for different combinations
        for v1, v2 in values:
            for m1, m2 in multipliers:
                if position[0] + v1*m1 in allowed_indices and position[1] + v2*m2 in allowed_indices:
                    if field[position[0] + v1*m1, position[1] + v2*m2] == "    " or field[position[0] + v1*m1, position[1] + v2*m2][0] == op:
                        moves.append((position[0] + v1*m1, position[1] + v2*m2))

        return moves

    def get_rook_moves(field, position):
        allowed_indices = [x for x in range(8)]
        moves = []

        for i in range(1, 8):
            if(position[0] + i in allowed_indices and field[position[0] + i, position[1]] == "    "):
                moves.append((position[0] + i, position[1]))
            elif(position[0] + i in allowed_indices and field[position[0] + i, position[1]][0] == op):
                moves.append((position[0] + i, position[1]))
                break
            else:
                break

        for i in range(1, 8):
            if(position[0] - i in allowed_indices and field[position[0] - i, position[1]] == "    "):
                moves.append((position[0] - i, position[1]))
            elif(position[0] - i in allowed_indices and field[position[0] - i, position[1]][0] == op):
                moves.append((position[0] - i, position[1]))
                break
            else:
                break

        for i in range(1, 8):
            if(position[1] + i in allowed_indices and field[position[0], position[1] + i] == "    "):
                moves.append((position[0], position[1] + i))
            elif(position[1] + i in allowed_indices and field[position[0], position[1] + i][0] == op):
                moves.append((position[0], position[1] + i))
                break
            else:
                break

        for i in range(1, 8):
            if(position[1] - i in allowed_indices and field[position[0], position[1] - i] == "    "):
                moves.append((position[0], position[1] - i))
            elif(position[1] - i in allowed_indices and field[position[0], position[1] - i][0] == op):
                moves.append((position[0], position[1] - i))
                break
            else:
                break

        return moves

    def get_bishop_moves(field, position):
        allowed_indices = [x for x in range(8)]
        moves = []

        multipliers = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

        for m1, m2 in multipliers:
            for i in range(1, 8):
                if(position[0] + i*m1 in allowed_indices and position[1] + i*m2 in allowed_indices and field[position[0] + i*m1, position[1] + i*m2] == "    "):
                    moves.append((position[0] + i*m1, position[1] + i*m2))
                elif(position[0] + i*m1 in allowed_indices and position[1] + i*m2 in allowed_indices and field[position[0] + i*m1, position[1] + i*m2][0] == op):
                    moves.append((position[0] + i*m1, position[1] + i*m2))
                    break
                else:
                    break

        return moves

    def get_king_moves(field, position):
        allowed_indices = [x for x in range(8)]
        moves = []

        values = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
        for v1, v2 in values:
            if position[0] + v1 in allowed_indices and position[1] + v2 in allowed_indices:
                if field[position[0] + v1, position[1] + v2] == "    " or field[position[0] + v1, position[1] + v2][0] == op:
                    moves.append((position[0] + v1, position[1] + v2))

        return moves

    def get_queen_moves(field, position):
        return get_rook_moves(field, position) + get_bishop_moves(field, position) #my favorite :)

    #iterate bord squares to check if they contain player's material
    possible_moves = {}
    for i in range(8):
        for j in range(8):
            if field[i, j][0] == player:
                #find relevant moves and add to the moves dictionary
                if field[i, j][1] == "P":
                    possible_moves[(i, j)] = get_pawn_moves(field, (i, j))
                elif field[i, j][3] == "i":
                    possible_moves[(i, j)] = get_knight_moves(field, (i, j))
                elif field[i, j][1] == "R":
                    possible_moves[(i, j)] = get_rook_moves(field, (i, j))
                elif field[i, j][1] == "B":
                    possible_moves[(i, j)] = get_bishop_moves(field, (i, j))
                elif field[i, j][1] == "Q":
                    possible_moves[(i, j)] = get_queen_moves(field, (i, j))
                else:
                    possible_moves[(i, j)] = get_king_moves(field, (i, j))

    return possible_moves

def check_if_check(field, player):
    """
    Determines whether current player is being checked by opponent
    If so, returns True, else False
    """
    if player == 'w':
        op = 'b'
    else:
        op = 'w'

    #find position of player's king
    king_cor = (np.where(field == f"{player}Kin")[0][0], np.where(field == f"{player}Kin")[1][0])

    #check if opponent's possible moves include moving to king's position
    opponent_moves = get_possible_moves(field, op)
    for key, val in opponent_moves.items():
        if king_cor in val:
            return True

    return False

def check_if_checkmate(field, player):
    moves = get_possible_moves(field, player)
    for piece in moves.keys():
        for move in moves[piece]:
            temp_field = execute_move(field, piece, move)
            if not check_if_check(temp_field, player):
                return False
    return True

def check_if_sufficient_material(field):
    """
    Checks if field still contains sufficient material for either player to win
    """
    #look for either pawns, rooks or queens
    for i in range(8):
        for j in range(8):
            if field[i, j][1] == "P":
                return True
            elif field[i, j][1] == "R":
                return True
            elif field[i, j][1] == "Q":
                return True

    #no pawns, rooks or queens of either color
    return False

def execute_move(field, old, new):
    """
    returns new state of playing field given certain move
    """
    new_field = field.copy()

    #for pawns, check if they reached end of board (and if so turn into queen)
    if new_field[old][1] == "P":
        if new_field[old][0] == 'w' and new[0] == 0:
            new_field[old] = "    "
            new_field[new] = "wQue"
        elif new_field[old][0] == 'b' and new[0] == 7:
            new_field[old] = "    "
            new_field[new] = "bQue"
        else:
            piece = new_field[old]
            new_field[old] = "    "
            new_field[new] = piece
    else:
        piece = new_field[old]
        new_field[old] = "    "
        new_field[new] = piece
        
    return new_field

def clean_illegal_moves(field, player, moves):
    temp_field = field.copy()
    for piece in moves.keys():
        for move in moves[piece]:
            new_field = execute_move(temp_field, piece, move)
            if check_if_check(new_field, player):
                moves[piece].remove(move)
    return moves

def pick_random_move(moves):
    pos_moves = []
    while pos_moves == []:
        piece = random.choice(list(moves.keys()))
        pos_moves = moves[piece]

    if pos_moves == []:
        return None

    move = random.choice(pos_moves)
    return piece, move
