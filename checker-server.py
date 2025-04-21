from flask import Flask, request, jsonify
from flask_cors import CORS
import copy

app = Flask(__name__)
CORS(app)

# Global board state
board = []

def initialize_board():
    global board
    board = [
        [-1 if (i + j) % 2 == 1 and i < 3 else 
         1 if (i + j) % 2 == 1 and i > 4 else 
         0 for i in range(8)] 
        for j in range(8)
    ]

def print_board():
    print("Current board state:")
    for row in board:
        print(' '.join(str(x) for x in row))
    print("==============================")

def is_valid_move(boardstate, x_old, y_old, x_new, y_new, color, turn):
    # Correct turn
    if color != turn:
        return False
    # Bounds check
    if not (0 <= x_old < 8 and 0 <= y_old < 8 and 0 <= x_new < 8 and 0 <= y_new < 8):
        return False
    # Target must be empty
    if boardstate[y_new][x_new] != 0:
        return False
    # Valid color
    if color not in [-1, 1, -2, 2]:
        return False
    # Must move diagonally
    if abs(x_new - x_old) != abs(y_new - y_old):
        return False

    is_king = abs(color) == 2

    # Non-king must move forward only
    if not is_king:
        if color == 1 and y_new >= y_old:  # White moves up
            return False
        if color == -1 and y_new <= y_old:  # Black moves down
            return False

    # Normal move
    if abs(x_new - x_old) == 1 and abs(y_new - y_old) == 1:
        return True

    # Capture move
    if abs(x_new - x_old) == 2 and abs(y_new - y_old) == 2:
        mid_x = (x_old + x_new) // 2
        mid_y = (y_old + y_new) // 2
        # Must capture opposite color
        if boardstate[mid_y][mid_x] * color < 0:
            return True

    return False

def take_user_turn(boardstate, y_old, x_old, y_new, x_new, color):
    # Move piece
    boardstate[y_old][x_old] = 0
    boardstate[y_new][x_new] = color

    # Handle capture
    if abs(x_new - x_old) == 2 and abs(y_new - y_old) == 2:
        mid_x = (x_old + x_new) // 2
        mid_y = (y_old + y_new) // 2
        boardstate[mid_y][mid_x] = 0  # Remove captured piece

    # Promote to king
    if color == 1 and y_new == 0:
        boardstate[y_new][x_new] = 2
    elif color == -1 and y_new == 7:
        boardstate[y_new][x_new] = -2

    return boardstate

def take_computer_turn(boardstate):
    # Placeholder: computer does nothing for now
    return boardstate

@app.route('/initialize', methods=['GET'])
def initialize():
    initialize_board()
    print_board()
    return jsonify({"board": board})

@app.route('/move', methods=['POST'])
def move():
    data = request.json

    x_old = data.get('x_old')
    y_old = data.get('y_old')
    x_new = data.get('x_new')
    y_new = data.get('y_new')
    color = data.get('color')
    turn = data.get('turn')
    old_board = data.get('board')

    # Work with a deepcopy of the received board to avoid side effects
    new_board = copy.deepcopy(old_board)

    if is_valid_move(new_board, x_old, y_old, x_new, y_new, color, turn):
        new_board = take_user_turn(new_board, y_old, x_old, y_new, x_new, color)
        new_board = take_computer_turn(new_board)

        print_board()

        return jsonify({"valid": True, "board": new_board})
    else:
        print_board()
        return jsonify({"valid": False, "board": old_board})

if __name__ == '__main__':
    initialize_board()
    print_board()
    app.run(host='0.0.0.0', port=2000, debug=True)
