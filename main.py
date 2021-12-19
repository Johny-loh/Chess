from const import *
import os

def history(field, step):
    for i in range(7, 0, -1):
        field[i * 2 + 1][-1] = field[i * 2 - 1][-1]

    field[1][-1] = ' (' + ', '.join(step).upper() + ')'

    return field

def motion(field, stepout, stepin):
    global queue
    queue = (queue + 1) % 2
    field[stepin[0]][stepin[1]] = field[stepout[0]][stepout[1]]
    field[stepout[0]][stepout[1]] = ' '

    return field

def pos(OF, TO, mode=0):
    if mode:
        return dictionaryl[(OF[1] - 3) // 4] + str((17 - OF[0]) // 2), dictionaryl[(TO[1] - 3) // 4] + str((17 - TO[0]) // 2)
    else:
        return (17 - int(OF[1]) * 2, dictionaryr[OF[0]] * 4 + 3), (17 - int(TO[1]) * 2, dictionaryr[TO[0]] * 4 + 3)

def verify(OF, TO, white_turn, mode=1):
    if (FIELD[OF[0]][OF[1]] == ' '):
        if mode:
            print('Вы не выбрали фигуру')
        return True
    elif OF == TO:
        if mode:
            print('Недопустимый ход')
        return True
    elif FIELD[TO[0]][TO[1]] != ' ' and figuresl[FIELD[OF[0]][OF[1]]].split('_')[0] == figuresl[FIELD[TO[0]][TO[1]]].split('_')[0]:
        if mode:
            print('Недопустимый ход, вы не можете побить свою фигуру')
        return True
    elif (FIELD[OF[0]][OF[1]] in WHITE_PIECES) == white_turn:
        if mode:
            print('Очередь Белых' * (not white_turn) + 'Очередь Черных' * white_turn)
        return True

    if can_move_stage1(figuresl[FIELD[OF[0]][OF[1]]], OF, TO, FIELD):
        return True        

    return can_move_stage2(figuresl[FIELD[OF[0]][OF[1]]], OF, TO, FIELD )

def can_move_stage1(piece, chess_yx, move_yx, field):

    y1, x1, y2, x2 = chess_yx[0], chess_yx[1], move_yx[0], move_yx[1]

    if piece == 'BLACK_PAWN':
        if (y1 == 3) and (y2 in [5, 7]) and (x1 == x2):
            return False
        if y2 - y1 == 2 and x1 == x2:
            return False

        if y2 - y1 == 2 and abs(x1 - x2) == 4:
            return field[y2][x2] == ' '

        return True
    elif piece == 'WHITE_PAWN':
        if y1 == 13 and y2 in [11, 9] and x1 == x2:
            return False

        if y1 - y2 == 2 and x1 == x2:
            return False

        if y1 - y2 == 2 and abs(x1 - x2) == 4:
            return field[y2][x2] == ' '

        return True
    elif piece in ('BLACK_ROOK', 'WHITE_ROOK'):
        return not(x1 == x2 or y1 == y2)
    elif piece in ('BLACK_KING', 'WHITE_KING'):
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
    elif piece in ('BLACK_BISHOP', 'WHITE_BISHOP'):
        return abs(x1 - x2) == abs(y1 - y2)
    elif piece in ('BLACK_QUEEN', 'WHITE_QUEEN'):
        return abs(x1 - x2) == abs(y1 - y2) or x1 == x2 or y1 == y2
    elif piece in ('BLACK_KNIGHT', 'WHITE_KNIGHT'):
        t1 = abs(x1 - x2) // 2
        t2 = abs(y1 - y2) // 4

        return not((t1 == 1 and t2 == 2) or (t1 == 2 and t2 == 1))
    else:
        print(piece)
        raise Exception()

def check_intersection(y, x, is_white, field):
    chess = field[y][x]
    return not (chess != ' ' and is_white == (chess in WHITE_PIECES))

def can_move_stage2(piece, piece_yx, move_yx, field):

    y1, x1, y2, x2 = piece_yx[0], piece_yx[1], move_yx[0], move_yx[1]
    is_white = piece in WHITE_PIECES

    if piece in ('BLACK_PAWN', 'WHITE_PAWN'):
        if x1 == x2:
            r = (y1 + 2, y2 + 2, 2) if piece == 'BLACK_PAWN' else (y2, y1 - 1, 2)
            for y in range(*r):
                if not check_intersection(y, x1, is_white, field):
                    return True

        return False
    elif piece in ('BLACK_ROOK', 'WHITE_ROOK'):
        if x1 == x2:
            ma = max(y1, y2)
            mi = min(y1, y2)
            for y in range(mi, ma + 2, 2):
                if y != y1 and not check_intersection(y, x1, is_white, field):
                    return True
        else:
            ma = max(x1, x2)
            mi = min(x1, x2)
            for x in range(mi, ma + 4):
                if not check_intersection(y1, x, is_white, field):
                    return True
        return False
    elif piece in ('BLACK_KING', 'WHITE_KING'):
        return False
    elif piece in ('BLACK_BISHOP', 'WHITE_BISHOP'):
        steps = abs(x1 - x2) // 4

        step_x = -1 if x1 > x2 else 1
        step_y = -1 if y1 > y2 else 1

        for i in range(1, steps):
            if not check_intersection(y1 + 2 * i * step_y, x1 + 4 * i * step_x, is_white, field):
                return True
        return False
    elif piece in ('BLACK_QUEEN', 'WHITE_QUEEN'):
        if x1 == x2 or y1 == y2:
            return can_move_stage2('WHITE_ROOK' if piece in WHITE_PIECES else 'BLACK_ROOK', piece_yx, move_yx, field)
        else:
            return can_move_stage2('WHITE_BISHOP' if piece in WHITE_PIECES else 'BLACK_BISHOP', piece_yx, move_yx, field)
    elif piece in ('BLACK_KNIGHT', 'WHITE_KNIGHT'):
        return False
    else:
        print(piece)
        raise Exception()

# def generate_moves(field, white_turn = False):
#     moves = []

#     for y in range(len(field)):
#         for x in range(len(field[y])):
#             if not(field[y][x] in figuresl.keys()):
#                 continue

#             for y2 in range(len(field)):
#                 for x2 in range(len(field[y2])):
#                     if field[y2][x2] in figuresl.keys():
#                         s1 = (y, x)
#                         s2 = (y2, x2)

#                         if verify(s1, s2, white_turn, 0):
#                             moves.append((s1, s2))

#     return moves

# def king_eatable(field, king_yx, white_turn: bool):
#     moves = generate_moves(field, not white_turn)

#     for move in moves:
#         if move[1] == king_yx:
#             return True

#     return False

# def virtual_move(field, chess_yx, move_yx):
#     piece_y, piece_x, move_y, move_x = chess_yx[0], chess_yx[1], move_yx[0], move_yx[1]

#     field[move_y][move_x] = field[piece_y][piece_x]
#     field[piece_y][piece_x] = ' '

# def checkmate():
#     king_yx = None
#     for y in range(len(FIELD)):
#         for x in range(len(FIELD[y])):
#             if FIELD[y][x] == ('♚' if queue else '♔'):
#                 king_yx = (y, x)

#     if king_eatable(FIELD, king_yx, queue):
#         moves = generate_moves(FIELD, not queue)

#         king_moves = filter(lambda x: x[0] == king_yx, moves)

#         for move in king_moves:
#             virtual_move(FIELD, *move)
#             if not king_eatable(FIELD, move[1], queue):
#                 return False
#             virtual_move(FIELD, *reversed(move))

#         return True

def checkmate():
    if not any('♔' in x for x in FIELD) or not any('♚' in x for x in FIELD):
        return True
    return False

os.system('cls')
for _ in FIELD:
    print(''.join(_))
queue = 0
game = 1

while game:

    STEPOUT, STEPIN = input('Сделайте ход : ').split()
    if (STEPOUT[0].lower() not in acceptable_steps) or (STEPOUT[1].lower() not in acceptable_steps) or (STEPIN[0].lower() not in acceptable_steps) or (STEPOUT[1].lower() not in acceptable_steps):
        print('Вы вышли за границы игрового поля, попробуйте еще раз')
        continue
    STEPOUT, STEPIN = pos(STEPOUT.upper(), STEPIN.upper(), 0)
    check = verify(STEPOUT, STEPIN, queue)

    if check:
        continue

    FIELD = history(FIELD, pos(STEPOUT, STEPIN, 1))
    FIELD = motion(FIELD, STEPOUT, STEPIN)
    if checkmate():
        break


    os.system('cls')
    for i in FIELD:
        print(''.join(i))

print("Белые " * queue + 'Черные ' * (not queue) + "победили")