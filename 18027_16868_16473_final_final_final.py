# Pre pokretanja programa, u terminalu ukucati naredbu:
# pip install colorama

import copy
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)


# ========================================================================BOARD

def create_board(n, m):
    board = []

    for i in range(n):
        mat = m * [' ']
        board = board + [mat]

    return board


def enter_board_dimensions():
    skip = True
    num_row = ''
    while True:
        try:
            if skip:
                num_row = int(input(Fore.GREEN + 'Enter board rows:'))
                if num_row > 20:
                    raise Exception(Fore.RED + "Too many rows")
                if num_row < 2:
                    raise Exception(Fore.RED + "Number of rows must be positive and more than one")
            skip = False
            num_column = int(input(Fore.GREEN + 'Enter board columns:'))
            if num_column > 20:
                raise Exception(Fore.RED + "Too many columns")
            if num_column < 2:
                raise Exception(Fore.RED + "Number of columns must be positive and more than one")
            break
        except ValueError:
            print(Fore.RED + "Not a number")
        except Exception as i:
            print(i)
    return num_row, num_column


def print_board(board):
    m = len(board[0])
    n = len(board)
    z = 0
    u = 65

    board.reverse()

    print("   ", end="")
    while z < m:
        print(Fore.YELLOW + "   %c" % u, end="")
        u += 1
        z += 1
    print(end='\n')
    sep = m * ' —  '
    print(Fore.GREEN + '     ' + sep)
    countX = m * [False]
    for i in range(n):
        countO = False
        sep = m * ' —  '
        print(f'{Fore.YELLOW}{n - i} ', end='  ') if (n - i) < 10 else print(f'{Fore.YELLOW}{n - i}', end='  ')
        for j in range(m):
            if not j:
                print(Fore.GREEN + '|', end=' ')
            if board[i][j] == 'O':
                countO = not countO
            if j < m - 1:
                print(f"{Fore.RED if board[i][j] == 'X' else Fore.BLUE}{board[i][j]}", end=Fore.BLUE + ' O ') if \
                    board[i][j] == 'O' and board[i][j + 1] == 'O' and countO else print(
                    f"{Fore.RED if board[i][j] == 'X' else Fore.BLUE}{board[i][j]}", end=Fore.GREEN + ' | ')
            else:
                print(f"{Fore.RED if board[i][j] == 'X' else Fore.BLUE}{board[i][j]}", end=Fore.GREEN + ' | ')
            if i < n - 1:
                if board[i][j] == 'X':
                    countX[j] = not countX[j]
                if board[i][j] == 'X' and board[i + 1][j] == 'X' and countX[j]:
                    sep = sep[:j * 4] + " X  " + sep[j * 4:4 * (m - 1)]

        print(end='\n')
        print('    ', end=' ')
        for i in sep:
            print(Fore.GREEN + i if i != 'X' else Fore.RED + i, end='')
        print(end='\n')
    print()

    board.reverse()


def board_example(list_of_moves):
    print(list_of_moves)
    brd = create_board(list_of_moves[0], list_of_moves[1])
    player = 1
    for i in list_of_moves[2:]:
        player = play_move(brd, i, player, 0)
    print_board(brd)


# ========================================================================MOVE
def play_move(board, move, player, minmaxVal):  # player X=1 player O=0
    if minmaxVal:
        board = copy.deepcopy(board)
    go_next = True
    if ord(move[-1]) > 90:
        move = move[:-1] + chr(ord(move[-1]) - 32)
    if len(move) > 3 or len(move) == 0 or ord(move[-1]) < 65 or ord(move[-1]) > 91 or not move[0].isnumeric():
        go_next = False
    if len(move) == 3 and not move[1].isnumeric():
        go_next = False
    if len(move) > 2 and len(board) < 10:
        go_next = False

    if go_next:
        if len(move) > 2:
            x = int(move[0:2])
            y = ord(move[2]) - 64
        else:
            x = int(move[0])
            y = ord(move[1]) - 64
        val = validate_move(board, x, y, player, 0)
        if val:
            if player:
                board[x][y - 1] = 'X'
                board[x - 1][y - 1] = 'X'
            else:
                board[x - 1][y - 1] = 'O'
                board[x - 1][y] = 'O'
            player = not player
    else:
        print(Fore.RED + 'Invalid input!')

    return board if minmaxVal else player


def possible_moves(player, board):
    m = len(board[0])
    n = len(board)

    possibles = []
    for i in range(n):
        for j in range(m):
            val = validate_move(board, i + 1, j + 1, player, 1)
            if val:
                string = str(i + 1) + chr(j + 65)
                possibles.append(string)
    return possibles


# ========================================================================VALIDATION

def validate_end(board, player):
    val = False

    if player:
        m = len(board[0])
        n = len(board)
        for i in range(n - 1):
            for j in range(m):
                if board[i][j] == ' ' and board[i + 1][j] == ' ':
                    val = True
        if not val:
            print(Fore.LIGHTGREEN_EX + "O player won!")
    else:
        m = len(board[0])
        n = len(board)
        for i in range(n):
            for j in range(m - 1):
                if board[i][j] == ' ' and board[i][j + 1] == ' ':
                    val = True
        if not val:
            print(Fore.LIGHTGREEN_EX + "X player won!")

    return val


def validate_move(board, row, column, player, check_possible):
    v = True

    if row > len(board) or column > len(board[0]) or row <= 0 or column <= 0:
        if not check_possible:
            print(Fore.RED + 'Board overreached!')
        v = False
        return v

    if player:
        if row >= len(board):
            if not check_possible:
                print(Fore.RED + 'Invalid input - row overreach for X!')
            v = False

        elif board[row - 1][column - 1] != ' ' or board[row][column - 1] != ' ':
            v = False
            if not check_possible:
                print(Fore.RED + 'Invalid input - field occupied!')
    else:
        if column >= len(board[0]):
            if not check_possible:
                print(Fore.RED + 'Invalid input - column overreach for O!')
            v = False
        elif board[row - 1][column - 1] != ' ' or board[row - 1][column] != ' ':
            v = False
            if not check_possible:
                print(Fore.RED + 'Invalid input - field occupied!')

    return v


def first_player():
    first = input(Fore.LIGHTGREEN_EX + 'Choose first to play (C/P): ')

    if first == 'C' or first == 'c':
        return 1
    elif first == 'P' or first == 'p':
        return 0
    else:
        print(Fore.RED + 'Invalid input!')
        first = first_player()
        return first


# ========================================================================MINMAX
def minimax(board, depth, player, alpha=(None, -10), beta=(None, 10)):
    if player:
        return max_value(board, depth, alpha, beta)
    else:
        return min_value(board, depth, alpha, beta)


def max_value(board, depth, alpha, beta, move=None):
    list_of_moves = possible_moves(1, board)
    if list_of_moves is None or depth == 0 or len(list_of_moves) == 0:
        return move, heuristic(board)

    else:
        for list_move in list_of_moves:
            alpha = max(alpha, min_value(play_move(board, list_move, 1, 1), depth - 1, alpha, beta,
                                         list_move if move is None else move), key=lambda x: x[1])
            if alpha[1] >= beta[1]:
                return beta

    return alpha


def min_value(board, depth, alpha, beta, move=None):

    list_of_moves = possible_moves(0, board)
    if list_of_moves is None or depth == 0 or len(list_of_moves) == 0:
        return move, heuristic(board)

    else:
        for list_move in list_of_moves:
            beta = min(beta, max_value(play_move(board, list_move, 0, 1), depth - 1, alpha, beta,
                                       list_move if move is None else move), key=lambda x: x[1])
            if beta[1] <= alpha[1]:
                return alpha

    return beta


def heuristic(board):
    return len(possible_moves(1, board)) - len(possible_moves(0, board))


def play_with_minimax():
    player = True
    num_row, num_column = enter_board_dimensions()
    b = create_board(num_row, num_column)
    first = first_player()
    print_board(b)
    #poss = possible_moves(x, b)
    #print(f'{Fore.BLUE}Possible moves: {poss}')
    val = True

    while val:
        print(Fore.GREEN + 'X player is on the move.') if player else print(Fore.GREEN + 'O player is on the move.')
        if player ^ first:
            move = input(Fore.YELLOW + 'Enter move (e.g. 3A): ')
        else:
            board2 = copy.deepcopy(b)
            computer_move = minimax(board2, 2, player, alpha=(None, -10), beta=(None, 10))
            move = computer_move[0]
            print(f'{Fore.YELLOW}Computer is playing the move {move}')
        player = play_move(b, move, player, 0)
        print_board(b)
        #poss = possible_moves(x, b)
        #print(f'{Fore.BLUE}Possible moves: {poss}')
        val = validate_end(b, player)
        if not val:
            new_game = input(Fore.CYAN+"Do you want to play another game [y/n]: ")
            if new_game == 'y' or new_game == 'Y':
                play_with_minimax()


play_with_minimax()

# def play():
#     x = True
#     num_row, num_column = enter_board_dimensions()
#     b = create_board(num_row, num_column)
#     first = first_player()
#     print_board(b)
#     poss = possible_moves(x, b)
#     print(f'{Fore.BLUE}Possible moves: {poss}')
#     br_pot = 0
#     val = True
#
#     while val:
#         print(Fore.GREEN + 'X player is on the move.') if x else print(Fore.GREEN + 'O player is on the move.')
#         if x ^ first:
#             move = input(Fore.YELLOW + 'Enter move (e.g. 3A): ')
#         else:
#             move = best_move(b, x)
#             print(f'{Fore.YELLOW}Computer is playing the move {move}')
#         x = play_move(b, move, x, 0)
#         print_board(b)
#         poss = possible_moves(x, b)
#         print(f'{Fore.BLUE}Possible moves: {poss}')
#         br_pot += 1
#         val = validate_end(b, x)
#
#
# def del_move(board, move, player):
#     if len(move) > 2:
#         x = int(move[0:2])
#         y = ord(move[2]) - 64
#     else:
#         x = int(move[0])
#         y = ord(move[1]) - 64
#     if player:
#         board[x][y - 1] = ' '
#         board[x - 1][y - 1] = ' '
#     else:
#         board[x - 1][y - 1] = ' '
#         board[x - 1][y] = ' '
#
#
# def best_move(board, player):
#     best_m = ["", 1000]
#     poss = possible_moves(player, board)
#     for p in poss:
#         play_move(board, p, player, 0)
#         outcome = len(possible_moves(not player, board))
#         if outcome < best_m[1]:
#             best_m[0] = p
#             best_m[1] = outcome
#         del_move(board, p, player)
#     return best_m[0]
