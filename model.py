import numpy as np
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout

from chess_env import *
from util import *

def generate_random_game_data(total_games):
    training_data = {'X':[], 'y':[]}
    games_appended = 0
    turns = []
    while games_appended < total_games:
        game_memory = {'X':[], 'y':[]}

        field = initialize_field()
        checkmate = False
        draw = False
        player = 'w'
        turn = 0
        while not checkmate and not draw:
            turn += 1
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

            game_memory['X'].append(process_field(field))
            game_memory['y'].append(turn)

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
                training_data['X'] += game_memory['X']
                training_data['y'] += list((np.array(game_memory['y'])/turn)*-1)
                games_appended += 1
            else:
                winner = 'w'
                #if white won, append to training data
                training_data['X'] += game_memory['X']
                training_data['y'] += list(np.array(game_memory['y'])/turn)
                games_appended += 1

        turns.append(turn)
        print(turn)
    print(np.mean(turns))
    input(np.std(turns))


        #print(f"{games_appended}/{total_games} training games", end = '\r')

    print("")
    return training_data

def create_model(total_games, epochs):
    model = Sequential()

    model.add(Dense(64, activation = "linear", input_shape = (64,)))
    model.add(Dropout(.1))
    model.add(Dense(256, activation = "linear"))
    model.add(Dropout(.1))
    model.add(Dense(256, activation = "linear"))
    model.add(Dropout(.1))
    model.add(Dense(256, activation = "linear"))
    model.add(Dropout(.1))
    model.add(Dense(128, activation = "linear"))
    model.add(Dropout(.1))
    model.add(Dense(64, activation = "linear"))
    model.add(Dense(1, activation = "tanh"))

    model.compile(loss = 'mean_squared_error', optimizer = 'adam')

    training_data = generate_random_game_data(total_games)

    model.fit(np.array(training_data["X"]), np.array(training_data["y"]), epochs = epochs)
    field = initialize_field()
    field = process_field(field)
    model.save(f"./models/model_{total_games}_random_games")

def test_model(model_name, total_games):
    model = load_model(f"{model_name}")

    games = {"w":0, "b":0, "D":0}
    for game in range(total_games):
        if not game%5:
            print(f"{game}/{total_games}", end = "\r")

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
                    piece, move = pick_random_move(moves)
                    test_field = execute_move(field, piece, move)
                    while check_if_check(test_field, player):
                        #potential move led to being checked
                        moves[piece].remove(move)
                        piece, move = pick_random_move(moves)
                        test_field = execute_move(field, piece, move)

                        #if all moves led to being checked either checkmate or draw
                        if sum(moves.values(), []) == []:
                            if initial_check:
                                checkmate = True
                                break
                            else:
                                draw = True
                                break

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
                games[winner] += 1
            else:
                winner = 'w'
                games[winner] += 1
            print(winner)
        else:
            print("draw")
            games["D"] += 1
        input(field)


    for outcome in games.keys():
        print(f'{outcome}:')
        print(f"\t{(games[outcome]/total_games)*100:.2f}%")

#create_model(200, 1)
test_model("./models/model_500_random_games", 100)
