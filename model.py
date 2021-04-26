import numpy as np
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout

from chess_env import *
from util import *

def generate_random_game_data(total_games):
    training_data = {'X':[], 'y':[]}
    games_appended = 0
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
            game_memory['y'].append(move_to_vector(piece, move))

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
            else:
                winner = 'w'
                #if white won, append to training data
                training_data['X'] += game_memory['X']
                training_data['y'] += game_memory['y']
                games_appended += 1
                print(f"{games_appended}/{total_games} training games", end = '\r')

    print("")
    return training_data

def create_model(total_games, epochs):
    model = Sequential()

    model.add(Dense(64, activation = "linear", input_shape = (64,)))
    model.add(Dropout(.1))
    model.add(Dense(256, activation = "linear"))
    model.add(Dropout(.1))
    model.add(Dense(256, activation = "linear"))
    model.add(Dense(64*64, activation = "softmax"))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    training_data = generate_random_game_data(total_games)

    model.fit(np.array(training_data["X"]), np.array(training_data["y"]), epochs = epochs)
    field = initialize_field()
    field = process_field(field)
    model.save(f"./models/{total_games}_random_games-model")

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
        while not checkmate and not draw:
            initial_check = check_if_check(field, player)

            moves = get_possible_moves(field, player)

            while 1:
                if player == 'w':
                    processed = np.array([process_field(field)])
                    prediction = model.predict(processed)[0]
                    move_vector = np.zeros(len(prediction))
                    move_vector[np.argmax(prediction)] = 1
                    piece, move = vector_to_move(move_vector)
                    t = 0

                    while not move_in_moves(piece, move, moves):
                        t += 1
                        #print(t, end = '\r')
                        #print("illegal move")
                        prediction[np.argmax(prediction)] = -1
                        move_vector = np.zeros(len(prediction))
                        move_vector[np.argmax(prediction)] = 1
                        piece, move = vector_to_move(move_vector)

                    #print(t)

                else:
                    piece, move = pick_random_move(moves)

                new_field = execute_move(field, piece, move)
                if not check_if_check(new_field, player):
                    field = new_field
                    break
                else:
                    #potential move led to being checked
                    if player == 'w':
                        prediction[np.argmax(prediction)] = -1
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
        else:
            games["D"] += 1

    for outcome in games.keys():
        print(f'{outcome}:')
        print(f"\t{(games[outcome]/total_games)*100:.2f}%")

#create_model(500, 10)
test_model("./models/500_random_games-model", 100)
