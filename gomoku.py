"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.
Last modified: Oct. 30, 2021
"""

# Poject 2: Gomoku
# Ziyi Huang
# Python 3.8.8
# 2021. 11. 16

def is_empty(board):
    # returns True iff there are no stones on the board
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != " ":
                return False

    return True

def is_full(board):
    # returns True iff there are no available space on the board
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                return False

    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''
    analyses the sequence of length length that ends at location (y end, x end)

    returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open,
    and "CLOSED" if the sequence is closed
    '''
    previous, after = True, True
    if y_end - length * d_y <= -1 or (x_end - length * d_x) not in range(len(board)):
        previous = False
    if y_end + d_y >= len(board) or (x_end + d_x) not in range(len(board)):
        after = False

    if previous and board[y_end - length * d_y][x_end - length * d_x] != " ":
        previous = False
    if after and board[y_end + d_y][x_end + d_x] != " ":
        after = False

    if previous and after:
        return "OPEN"

    elif previous or after:
        return "SEMIOPEN"

    else:
        # not previous and not after, where both previous and after are False
        return "CLOSED"


def detect_row(board, col, y_start, x_start, length, d_y, d_x, check_closed = False):
    '''
    analyses the row (let’s call it R) of squares that
    starts at the location (y start,x start) and goes in the direction (d y,d x)

    returns a tuple whose first element is the number of open sequences of
    colour col of length length in the row R, and whose second element is the number of
    semi-open sequences of colour col of length length in the row R.
    '''
    open_seq_count, semi_open_seq_count, closed_seq_count, row_length = 0, 0, 0, 1
    if d_y + d_x == 1:
        row_length = len(board)
    elif d_y + d_x == 2:
        row_length = len(board) - max(x_start, y_start)
    elif d_y + d_x == 0:
        if y_start == 0:
            row_length = x_start + 1
        else:
            row_length = len(board) - y_start

    if length > row_length:
        if check_closed:
            return 0, 0, 0
        else:
            return 0, 0
    else:
        for i in range(row_length - length + 1):
            if board[y_start + d_y*i][x_start + d_x*i] == col:
                continuous, complete = True, True
                if i > 0:
                    if board[y_start + d_y*(i-1)][x_start + d_x*(i-1)] == col:
                        complete = False

                for j in range(1, length):
                    if board[y_start + d_y*(i + j)][x_start + d_x*(i + j)] != col:
                        continuous = False
                        break
                if i + length < row_length:
                    if board[y_start + d_y*(i + length)][x_start + d_x*(i + length)] == col:
                        complete = False

                if continuous and complete and is_bounded(board, y_start + d_y * (i + length - 1), x_start + d_x * (i + length - 1), length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif continuous and complete and is_bounded(board, y_start + d_y * (i + length - 1), x_start + d_x * (i + length - 1), length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                elif continuous and complete and is_bounded(board, y_start + d_y * (i + length - 1), x_start + d_x * (i + length - 1), length, d_y, d_x) == "CLOSED":
                    closed_seq_count += 1

        if check_closed:
            return open_seq_count, semi_open_seq_count, closed_seq_count
        else:
            return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length, check_closed = False):
    '''
    returns a tuple, whose first element is the number of
    open sequences of colour col of length length on the entire board,
    and whose second element is the number of semi-open sequences of
    colour col of length length on the entire board
    '''
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    # hori
    open_seq, semi_open_seq, closed_seq = detect_row(board, col, 7, 0, length, 0, 1, True)
    open_seq_count += open_seq
    semi_open_seq_count += semi_open_seq
    closed_seq_count += closed_seq

    # vert
    open_seq, semi_open_seq, closed_seq = detect_row(board, col, 0, 7, length, 1, 0, True)
    open_seq_count += open_seq
    semi_open_seq_count += semi_open_seq
    closed_seq_count += closed_seq

    for i in range(len(board)-1):
        for j in range(-1, 2, 1):
            if j == -1:
                # diagonal-up right to lower left
                open_seq, semi_open_seq, closed_seq = detect_row(board, col, i, 7, length, 1, j, True)
                open_seq_count += open_seq
                semi_open_seq_count += semi_open_seq
                closed_seq_count += closed_seq

            else:
                # horizontal(j=0) and diagonal-up left to lower right(j=1)
                open_seq, semi_open_seq, closed_seq = detect_row(board, col, i, 0, length, j, 1, True)
                open_seq_count += open_seq
                semi_open_seq_count += semi_open_seq
                closed_seq_count += closed_seq

            # vertical and diagonals
            open_seq, semi_open_seq, closed_seq = detect_row(board, col, 0, i, length, 1, j, True)
            open_seq_count += open_seq
            semi_open_seq_count += semi_open_seq
            closed_seq_count += closed_seq

    open_seq, semi_open_seq, closed_seq = detect_row(board, col, 0, 0, length, 1, 1, True)
    open_seq_count -= open_seq
    semi_open_seq_count -= semi_open_seq
    closed_seq_count += closed_seq

    if check_closed:
        return open_seq_count, semi_open_seq_count, closed_seq_count
    else:
        return open_seq_count, semi_open_seq_count

def get_free_squares(board):
    '''
    return the available squares in the board
    '''
    free_square = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                free_square.append([i, j])
    return free_square

def search_max(board):
    free_square = get_free_squares(board)
    attempt_score = [0] * len(free_square)
    for i in range(len(free_square)):
        board[free_square[i][0]][free_square[i][1]] = "b"
        attempt_score[i] = score(board)
        board[free_square[i][0]][free_square[i][1]] = " "
    best_move_index = attempt_score.index(max(attempt_score))
    move_y, move_x = free_square[best_move_index]
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    check_closed = True
    length = 5

    b_open, b_semi, b_closed = detect_rows(board, "b", length, check_closed)
    if b_open > 0 or b_semi > 0 or b_closed > 0:
        return "Black won"

    w_open, w_semi, w_closed = detect_rows(board, "w", length, check_closed)
    if w_open > 0 or w_semi > 0 or w_closed > 0:
        return "White won"

    if is_full(board):
        return "Draw"

    return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open, closed = detect_rows(board, c, i, True);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
            print("Closed rows of length %d: %d" % (i, closed))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        attempt = [move_y, move_x]

        # ensure the player doesn't enter an invalid square location
        while attempt not in get_free_squares(board):
            print("The square is not available. Try again: ")
            move_y = int(input("y coord: "))
            move_x = int(input("x coord: "))

        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 3; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 4
    x_end = 4

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 3; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 1, 7, length, d_y, d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    col = 'w'
    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (0,1):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def test_is_win():
    board = make_empty_board(8)
    x = 1; y = 0; d_x = 1; d_y = 0; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 2; y = 1; d_x = 0; d_y = 1; length = 2; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 2; y = 3; d_x = 0; d_y = 1; length = 5; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 3; y = 4; d_x = 0; d_y = 1; length = 2; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 4; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
#     x = 6; y = 6; d_x = 0; d_y = 1; length = 2; col = 'b'
#     put_seq_on_board(board, y, x, d_y, d_x, length, col)
    board[4][7] = 'w'
    board[6][7] = 'w'
#     board[1][2] = 'b'
#     board[4][3] = 'w'
#     board[1][5] = 'w'
#     board[0][5] = 'b'
    print_board(board)
    if is_win(board) == "White won":
        print("TEST CASE for is_win PASSED")
    else:
        print("TEST CASE for is_win FAILED")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    print(play_gomoku(11))
    #easy_testset_for_main_functions()
    #test_is_bounded()
    #test_detect_row()
    #test_detect_rows()
    #some_tests()
    #test_is_win()