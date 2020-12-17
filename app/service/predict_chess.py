import os
import chess
import numpy as np
from tensorflow import keras

chess_dict = {
    'p': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'P': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'n': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'N': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'b': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'B': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'r': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'q': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Q': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'k': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    '': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
}

new_chess_dict = {}

for term in chess_dict:
    definition = tuple(chess_dict[term])
    new_chess_dict[definition] = term
    new_chess_dict[term] = definition


def make(board):
    matrix = make_matrix(board)
    data = np.reshape(translate(matrix, chess_dict), (1, 8, 8, 14))
    return data


def make_matrix(board):
    pgn = board.epd()
    foo = []
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo


def translate(matrix, chess_dict):
    rows = []
    for row in matrix:
        terms = []
        for term in row:
            terms.append(chess_dict[term])
        rows.append(terms)
    return rows


path_model = os.path.abspath("").replace("\\", "/") + "/app/service/model"
model = keras.models.load_model(filepath=path_model)


def predict(moves):
    board = chess.Board()
    moves = moves.split(' ')

    for move in moves:
      board.push_san(move)

    moves = list(board.legal_moves)

    rs = -1
    res = ""
    # print("----------------------------")
    for move in moves:
      board_copy = board.copy()
      board_copy.push(move)
      t = model.predict(make(board_copy))[0][0]
      # print(f'{move} {t}')
      if t > rs:
        rs = t
        res = move
    return res