import numpy as np

def process_field(field):
    arr = np.zeros((8, 8))
    arr[np.where(field == "wPwn")] = 1
    arr[np.where(field == "bPwn")] = -1
    arr[np.where(field == "wKni")] = 3
    arr[np.where(field == "bKni")] = -3
    arr[np.where(field == "wBis")] = 5
    arr[np.where(field == "bBis")] = -5
    arr[np.where(field == "wRok")] = 8
    arr[np.where(field == "bRok")] = -8
    arr[np.where(field == "wQue")] = 15
    arr[np.where(field == "bQue")] = -15
    arr[np.where(field == "wKin")] = 100
    arr[np.where(field == "bKin")] = -100
    arr = arr.reshape((64,))
    return arr

def move_to_vector(old_pos, new_pos):
    arr = np.zeros(64*64)
    old_pos = old_pos[0] * 8 + old_pos[1]
    new_pos = new_pos[0] * 8 + new_pos[1]
    arr[old_pos * 64 + new_pos] = 1
    return arr

def vector_to_move(arr):
    i = np.where(arr == 1)[0][0]
    new_pos = i%64
    new_pos = (new_pos//8, new_pos%8)
    old_pos = i//64
    old_pos = (old_pos//8, old_pos%8)
    return old_pos, new_pos

def move_in_moves(piece, move, moves):
    if piece not in list(moves.keys()):
        return False
    elif move not in moves[piece]:
        return False
    else:
        return True
