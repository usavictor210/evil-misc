import sys
import json
import curses

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

def move_player(board, direction):
    return make_changes(board, get_changes(board, direction))

def make_changes(board, changes):
    new_board = [[j for j in i] for i in board]
    for i in changes:
        change(new_board, i, changes[i])
    return new_board

def get_changes(board, direction):
    player_loc = get_player_loc(board)
    assert at(board, player_loc) == '@'
    move_player_to = at(board, add(direction, player_loc))
    if move_player_to == '.':
        return {player_loc: '.', add(direction, player_loc): '@'}
    elif move_player_to == sys.argv[2]:
        move_boulder_to = at(board, add(times(direction, 2), player_loc))
        if move_boulder_to == '.':
            return {player_loc: '.', add(direction, player_loc): '@',
            add(times(direction, 2), player_loc): sys.argv[2]}
        elif move_boulder_to  == '^':
            return {player_loc: '.', add(direction, player_loc): '@',
            add(times(direction, 2), player_loc): '.'}
        else:
            print(f'Failed (could not move boulder to {move_boulder_to}!')
            return {}
    else:
        print(f'Failed (could not move to {move_player_to})!')
        return {}

def show_state(state):
    return state if type(state) == str else \
    '\n'.join(''.join(i) for i in state)

def last_board(states):
    for i in reversed(states):
        if type(i) == list:
            return i

def count(board, i):
    return sum(j.count(i) for j in board)

def show(stdscr, message, board):
    stdscr.clear()
    stdscr.addstr(message + '\n' + show_state(board))
    stdscr.move(0, len(message))

def c_input(stdscr, message, board):
    show(stdscr, message, board)
    curses.echo()
    r = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return r

def main(stdscr):
    with open(sys.argv[1]) as f:
        text = f.read().replace(sys.argv[3], sys.argv[2])
    board = [list(i) for i in text.split('\n')]
    states = []
    moved = True
    message = ''
    while True:
        if moved:
            states.append(board)
        show(stdscr, message, board)
        moved = True
        i = stdscr.getkey()
        if i == '#':
            i = c_input(stdscr, '# ', board)
        if i == 'u':
            boards = 0
            while boards < 2:
                board = states.pop()
                if type(board) == list:
                    boards += 1
        elif i in {'h', 'KEY_LEFT'}:
            board = move_player(board, (0, -1))
        elif i in {'j', 'KEY_DOWN'}:
            board = move_player(board, (1, 0))
        elif i in {'k', 'KEY_UP'}:
            board = move_player(board, (-1, 0))
        elif i in {'l', 'KEY_RIGHT'}:
            board = move_player(board, (0, 1))
        elif i == 'save':
            with open(c_input(stdscr, 'File to write to? ', board), 'w') as f:
                f.write(json.dumps({'board': board, 'states': states}))
            moved = False
        elif i == 'load':
            with open(c_input(stdscr, 'File to read from? ', board)) as f:
                data = json.loads(f.read())
                board = data['board']
                states = data['states']
            moved = False
        elif i == 'display':
            with open(c_input(stdscr, 'File to write display to? ', board), 'w') as f:
                f.write('\n\n'.join(show_state(state) for state in states))
            moved = False
        elif i == 'c':
            states.append(c_input(stdscr, 'Comment? ', board))
            moved = False
        elif i == 'q':
            break
        elif i == 'stats':
            message = f'There are currently {count(board, sys.argv[2])} boulders and {count(board, "^")} pits. '
            moved = False
        else:
            message = i + ' is not a command! '
            moved = False


if __name__ == '__main__':
    curses.wrapper(main)
