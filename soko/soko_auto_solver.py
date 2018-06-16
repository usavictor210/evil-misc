import sys

def add(a, b):
    return tuple(i + j for i, j in zip(a, b))

def at(a, pos):
    for i in pos:
        a = a[i]
    return a

def change(a, pos, n):
    for i in pos[:-1]:
        a = a[i]
    a[pos[-1]] = n

def times(a, n):
    return tuple(i * n for i in a)

def get_player_loc(board):
    for i in range(len(board)):
        if '@' in board[i]:
            return i, board[i].index('@')
        if '#' in board[i]:
            return i, board[i].index('#')

def move_player(board, direction):
    c = get_changes(board[1], board[0], direction)
    if c is None:
        return None
    else:
        return add(board[0], direction), make_changes(board[1], c)

def make_changes(board, changes):
    new_board = [[j for j in i] for i in board]
    for i in changes:
        change(new_board, i, changes[i])
    return tuple(tuple(i) for i in new_board)

def initial(v):
    return {'@': '.', '#': ','}[v]

def get_changes(board, player_loc, direction):
    assert at(board, player_loc) in '@#'
    move_player_to = at(board, add(direction, player_loc))
    if move_player_to == '.':
        return {player_loc: initial(at(board, player_loc)), add(direction, player_loc): '@'}
    elif move_player_to == ',':
        return {player_loc: initial(at(board, player_loc)), add(direction, player_loc): '#'}
    elif move_player_to == sys.argv[2]:
        move_boulder_to = at(board, add(times(direction, 2), player_loc))
        if move_boulder_to == '.':
            return {player_loc: initial(at(board, player_loc)), add(direction, player_loc): '@',
            add(times(direction, 2), player_loc): sys.argv[2]}
        elif move_boulder_to == '^':
            return {player_loc: initial(at(board, player_loc)), add(direction, player_loc): '@',
            add(times(direction, 2), player_loc): '.'}
        elif move_boulder_to == '!':
            return {player_loc: initial(at(board, player_loc)), add(direction, player_loc): '@'}
        else:
            return None
    else:
        return None

def show_state(state):
    return state if type(state) == str else \
    '\n'.join(''.join(i) for i in state)

def last_board(states):
    for i in reversed(states):
        if type(i) == list:
            return i

def count(board, i):
    return sum(j.count(i) for j in board)

def get_pairs(x):
    l = x.split('\n')
    ret = []
    for k in 'abcdefghijklmnopqrstuvwxyz':
        if k in x:
            ret.append((
            tuple((i_ind, j_ind) for i_ind, i in enumerate(l) for j_ind, j in enumerate(i) if j == k),
            tuple((i_ind, j_ind) for i_ind, i in enumerate(l) for j_ind, j in enumerate(i) if j == k.upper())))
    return ret

def pairs_ok(i, pairs):
    for j in pairs:
        if all(at(i[1], k) == sys.argv[2] for k in j[0]) and i[0] not in j[1]:
            return False
    return True

final_board = tuple(tuple(i) for i in '''   ----
 ---,,---
 |,...0,|
 |,0...,|
 |,0.0.--
 |,0.0,|
 |--.-----
--,.0-,,,|
|#......,|
|,.,-,,,--
--!------
 ---'''.split('\n'))

"""
final_board = tuple(tuple(i) for i in '''   ----
 ---,,---
 |,0..0,|
 |,.0..,|
 |,@...--
 |,..0,|
 |--0-----
--,0.-,,,|
|,0....0,|
|,.,-,,,--
--!------
 ---'''.split('\n'))
"""

final_board = get_player_loc(final_board), final_board

def main(s):
    import time
    t0 = time.time()
    steps = 0
    with open(s) as f:
        text = f.read().replace(sys.argv[3], sys.argv[2])
    first_text_board = text.split('\n~\n')[0]
    others = text.split('\n~\n')[1:]
    start_just_board = tuple(tuple(i) for i in first_text_board.split('\n'))
    start_board = get_player_loc(start_just_board), start_just_board
    pairs = [j for i in others for j in get_pairs(i)]
    print(pairs)
    new_boards = {start_board: None}
    seen_boards = {}
    while new_boards:
        l = list(new_boards)
        for i in new_boards:
            seen_boards[i] = new_boards[i]
        new_boards = {}
        for board in l:
            new = {(i, move_player(board, i)) for i in ((0, -1), (1, 0), (-1, 0), (0, 1))}
            for i, j in new:
                if j is not None and j not in seen_boards and pairs_ok(j, pairs):
                    new_boards[j] = (i, board)
        steps += 1
        print(len(seen_boards) / (time.time() - t0))
        print(steps, len(seen_boards), min(sum(j.count(sys.argv[2]) for j in i[1]) for i in seen_boards))
        if final_board in seen_boards:
            print(path(seen_boards, final_board))
            exit()

def path(seen_boards, x):
    ret = []
    while seen_boards[x] != None:
        ret.append(seen_boards[x][0])
        x = seen_boards[x][1]
    return ret[::-1]

if __name__ == '__main__':
    main(sys.argv[1])
