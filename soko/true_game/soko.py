import sys
import pickle
import curses
import random

intro = '''~It is written in the Second Book of Amaterasu:

The Amulet of Yendor was recovered from Moloch's grasp by the demigoddess Tara.
However, unfortunately, Tara went, with the amulet, into a mysterious tower and
never came out. It is unclear exactly what happened, but there are rumors that
she got trapped by rocks or some such thing. TODO: make style of this book
more formal so my followers will actually understand that I care about this.
Also make it longer: right now it fits easily on one page. Also try to balance
benefit of making it clear that this is the Sokoban Tower with the fact that
if I do make it clear, no one in their right mind will want to go to the tower.

Your god Amaterasu seeks to repossess the Amulet, and with it to gain
ascendance over other gods.

You, untrained, just randomly stumbled upon a tower, and you feel,
for no good reason, that it's the tower Tara went to. You are destined
to recover the Amulet to Amaterasu; or at least you hope you are,
otherwise you'll probably fail, and you don't want that.
Your hour of destiny has come. For the sake of Amaterasu:
Don't make whatever mistake Tara made! '''

escape_text = '''~^You escape the Sokoban Tower!
Unfortunately, you did not retrieve the Amulet, but at least you survived. '''

ascend_text = '''You hear a heavenly choir singing...
---
You are bathed in a heavenly radiance...
---
You feel your knowledge expanding...
---
Amaterasu says, 'Congratulations, mortal!'
---
'In return for thy service, I grant thee the status of demigoddess!'
---
'Just try not to go up any other mysterious towers, OK?'~^'''

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

def update_stuff_item(old, loc_to_new):
    new = {i: {j for j in old[i]} for i in old}
    for j, (x, y) in loc_to_new:
        if x is not None:
            new[x].remove(j)
        if y is not None:
            new.setdefault(y, set())
            new[y].add(j)
    return new

def update_loc(state, loc_to_new):
    return {**state,
    **{'stuff': [i if ind != state['level'] else
    update_stuff_item(i, loc_to_new) for ind, i in enumerate(state['stuff'])]}}

def get_loc(stuff, i):
    return (list(stuff.get(i, set())) + [None])[0]

def at_for_move(board, stuff, i):
    if i in stuff['0']:
        return '0'
    if i in stuff['^']:
        return '^'
    return at(board, i)

def move_player(state, direction):
    stuff = state['stuff'][state['level']]
    board = state['board'][state['level']]
    player_loc = get_loc(stuff, '@')
    changes = get_changes(player_loc, stuff, board, direction)
    if changes is not None:
        return update_loc(state, changes)
    else:
        return None

def get_changes(player_loc, stuff, board, direction):
    move_player_to = at_for_move(board, stuff, add(direction, player_loc))
    if move_player_to == '.':
        return [(player_loc, ('@', None)), (add(direction, player_loc), (None, '@'))]
    elif move_player_to == '0':
        move_boulder_to = at_for_move(board, stuff, add(times(direction, 2), player_loc))
        if move_boulder_to == '.':
            return [(player_loc, ('@', None)), (add(direction, player_loc), ('0', '@')),
            (add(times(direction, 2), player_loc), (None, '0'))]
        elif move_boulder_to == '^':
            return [(player_loc, ('@', None)), (add(direction, player_loc), ('0', '@')),
            (add(times(direction, 2), player_loc), ('^', None))]
        else:
            return None
    else:
        return None

def get_display_item(stuff, loc):
    show = set()
    for i in stuff:
        if loc in stuff[i]:
            show.add(i)
    l = [i for i in '@0^"<>_' if i in show]
    return l[0] if l else None

def show_state(board, state):
    if type(state) == str:
        return state
    return '\n'.join(''.join(
    get_display_item(state['stuff'][state['level']], (ind, ind2)) or j
    for ind2, j in enumerate(i))
    for ind, i in enumerate(board[state['level']])) + '\n\n' + \
    f'Level: {state["level"] + 1} Turns: {state["turns"]} Undos: {state["undos"]}'

def last_board(states):
    for i in reversed(states):
        if type(i) == list:
            return i

def count(board, i):
    return sum(j.count(i) for j in board)

def show(stdscr, message, board):
    stdscr.clear()
    m = message.replace('~', '').replace('^', '').split('\n---\n')[0]
    stdscr.addstr(m +
    (('\n' + show_state(board['board'], board)) if '~' not in message else ''))
    stdscr.move(m.count('\n'), len(m.split('\n')[-1]))

def c_input(stdscr, message, board):
    show(stdscr, message, board)
    curses.echo()
    r = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return r

descs = {
    '@': 'you',
    '0': 'a boulder',
    '^': 'a pit',
    '"': 'the Amulet of Yendor',
    '<': 'a staircase up',
    '>': 'a staircase down',
    '_': 'a high altar'
}

terrain = '.|-\n '

def replace_stuff(text):
    return ''.join(i if i in terrain else '.' for i in text)

def get_stuff_locs(text):
    d = {}
    for ind, i in enumerate(text.split('\n')):
        for ind2, j in enumerate(i):
            if j not in terrain:
                d.setdefault(j, set())
                d[j].add((ind, ind2))
    return d

def read_all_boards(text):
    levels = [i.split('\n~~\n') for i in text.split('\n~~~~\n')]
    assert all(j.count('0') == j.count('^') for i in levels for j in i)
    chosen = [random.choice(i) for i in levels]
    return {'level': 0, 'turns': 0, 'undos': 0, 'board': [get_board(i) for i in chosen],
    'stuff': [get_stuff_locs(i) for i in chosen], 'inv': []}

def get_board(text):
    return [list(i) for i in replace_stuff(text).split('\n')]

def get_changing(x):
    return {i: x[i] for i in x if i != 'board'}

def get_loc_main(board, i):
    return get_loc(board['stuff'][board['level']], i)

def go_down(board):
    if get_loc_main(board, '>') != get_loc_main(board, '@'):
        return board, 'You are not at a staircase down! ', False
    if '"' in board['inv']:
        return board, 'Your amulet pulls on you, preventing you from going down! ', False
    if board['level'] == 0:
        return board, escape_text
    update_loc(board, [(get_loc_main(board, '@'), ('@', None))])
    board['level'] -= 1
    update_loc(board, [(get_loc_main(board, '>'), (None, '@'))])
    return board, 'You go down. ', True

def go_up(board):
    if get_loc_main(board, '<') != get_loc_main(board, '@'):
        return board, 'You are not at a staircase up! ', False
    board = update_loc(board, [(get_loc_main(board, '@'), ('@', None))])
    board['level'] += 1
    board = update_loc(board, [(get_loc_main(board, '>'), (None, '@'))])
    return board, 'You go up. ', True

movable = '"'

def movable_items_here(state):
    stuff = state['stuff'][state['level']]
    loc = get_loc_main(state, '@')
    return [i for i in movable if loc in stuff.get(i, set())]

def give_letters(l, bool_to_each=None):
    return {chr(ind + ord('a')): (i if bool_to_each is None else [i, bool_to_each])
    for ind, i in enumerate(l)}

def choose(stdscr, items):
    taken = give_letters(items, bool_to_each=False)
    while True:
        stdscr.clear()
        stdscr.addstr(items_disp(taken) + '\n')
        key = stdscr.getkey()
        if key in taken:
            taken[key][1] = not taken[key][1]
        elif key == '+':
            for i in taken:
                taken[i][1] = True
        elif key == '-':
            for i in taken:
                taken[i][1] = False
        elif key in 'q \n':
            return [i[0] for i in taken.values() if i[1]]

def add_to_inv(state, items):
    partial = update_loc(state, [(get_loc_main(state, '@'), (i, None)) for i in items])
    rest = {**partial, **{'inv': partial['inv'] + items}}
    return rest

def rem_from_inv(state, items):
    partial = update_loc(state, [(get_loc_main(state, '@'), (None, i)) for i in items])
    rest = {**partial, **{'inv': [i for i in partial['inv'] if i not in items]}}
    return rest

def offer_result(state, items):
    state = rem_from_inv(state, items)
    if '"' in items:
        message = ascend_text
    else:
        message = 'Your offering does not seem to be accepted. '
    return state, message, bool(items)

def take(stdscr, state):
    m = movable_items_here(state)
    if len(m) == 0:
        return state, 'There is nothing here. ', False
    items = choose(stdscr, m)
    return add_to_inv(state, items), '', bool(items)

def drop(stdscr, state):
    if state['inv'] == []:
        return state, 'You have nothing to drop! ', False
    items = choose(stdscr, state['inv'])
    return rem_from_inv(state, items), '', bool(items)

def offer(stdscr, state):
    if get_loc_main(state, '_') != get_loc_main(state, '@'):
        return state, 'You are not at an altar! ', False
    if state['inv'] == []:
        return state, 'You have nothing to offer! ', False
    items = choose(stdscr, state['inv'])
    return offer_result(state, items)


def item_disp(i, j):
    if type(j) == str:
        return f'{i} ({descs[j]})'
    else:
        return f'{i} ({descs[j[0]]}): {"-+"[j[1]]}'

def items_disp(x):
    return '\n'.join(item_disp(i, j) for i, j in x.items())

def inv(board):
    return items_disp(give_letters(board['inv'])) or 'You have nothing. '

def trim_message(message):
    if '\n---\n' not in message:
        return ''
    else:
        return '\n---\n'.join(message.split('\n---\n')[1:])

def main(stdscr):
    with open('data.txt') as f:
        text = f.read()
    board = read_all_boards(text)
    board = update_loc(board, [(get_loc_main(board, '>'), (None, '@'))])
    states = []
    moved = True
    message = intro
    done = False
    while not done:
        if moved:
            states.append(get_changing(board))
        show(stdscr, message, board)
        i = stdscr.getkey()
        if '^' in message and '\n---\n' not in message:
            done = True
        if '~' in message:
            message = trim_message(message)
            continue
        message = trim_message(message)
        moved = True
        if i == '#':
            i = c_input(stdscr, '# ', board)
        if i == 'u':
            num_boards = 0
            changing = get_changing(board)
            while num_boards < 2 and states:
                temp = states.pop()
                if type(temp) != str:
                    changing = temp
                    num_boards += 1
            changing['undos'] = board['undos'] + 1
            board.update(changing)
            states.append(changing)
            moved = False
        elif i in {'h', 'KEY_LEFT', 'j', 'KEY_DOWN',
        'k', 'KEY_UP', 'l', 'KEY_RIGHT'}:
            if i in {'h', 'KEY_LEFT'}:
                res = move_player(board, (0, -1))
            elif i in {'j', 'KEY_DOWN'}:
                res = move_player(board, (1, 0))
            elif i in {'k', 'KEY_UP'}:
                res = move_player(board, (-1, 0))
            elif i in {'l', 'KEY_RIGHT'}:
                res = move_player(board, (0, 1))
            if res is None:
                moved = False
                message = 'You cannot move that way! '
            else:
                board = res
        elif i == '<':
            board, message, moved = go_up(board)
        elif i == '>':
            if get_loc_main(board, '>') == get_loc_main(board, '@'):
                board, message, moved = go_down(board)
        elif i == ',':
            board, message, moved = take(stdscr, board)
        elif i == 'i':
            message = inv(board)
            moved = False
        elif i == 'd':
            board, message, moved = drop(stdscr, board)
        elif i == 'offer':
            board, message, moved = offer(stdscr, board)
        elif i == 'save':
            with open(c_input(stdscr, 'File to write to? ', board), 'wb') as f:
                pickle.dump({'board': board, 'states': states}, f)
            moved = False
        elif i == 'load':
            with open(c_input(stdscr, 'File to read from? ', board), 'rb') as f:
                data = pickle.load(f)
                board = data['board']
                states = data['states']
            moved = False
        elif i == 'display':
            with open(c_input(stdscr, 'File to write display to? ', board), 'w') as f:
                f.write('\n\n'.join(show_state(board, state) for state in states))
            moved = False
        elif i == 'c':
            states.append(c_input(stdscr, 'Comment? ', board))
            moved = False
        elif i == 'q':
            break
        elif i == 'stats':
            message = f'There are currently {count(board, "0")} boulders and {count(board, "^")} pits. '
            moved = False
        else:
            message = i + ' is not a command! '
            moved = False
        if moved:
            board['turns'] += 1


if __name__ == '__main__':
    curses.wrapper(main)
