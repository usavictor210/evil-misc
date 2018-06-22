import random
import curses

intro = '''~Intro message goes here. '''

death_message = '''Amazing! ~
---
You have managed to die! ~
---
The version of the game in which this message was written
has no way for you to be damaged, so that's quite an achievement! ~
---
Now try doing it again and see if it's consistent. ~^'''

def plus(a, b):
    return tuple(i + j for (i, j) in zip(a, b))

def minus(a, b):
    return tuple(i - j for (i, j) in zip(a, b))

def times(c, x):
    return tuple(c * i for i in x)

def dist(a, b):
    return norm(minus(a, b))

def norm(a):
    return inner(a, a) ** .5

def inner(a, b):
    return sum(i * j for (i, j) in zip(a, b))

neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

all_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

def get_a(x, l):
    for i in l:
        x = x[i]
    return x

def set_a(x, l, v):
    for i in l[:-1]:
        x = x[i]
    x[l[-1]] = v

def in_range(h, w, loc):
    return 1 <= loc[0] <= h - 2 and 1 <= loc[1] <= w - 2

def make_room(x, h, w, loc):
    s1 = random.randint(1, 3)
    s2 = random.randint(1, 3)
    for i in range(-s1, s1 + 1):
        for j in range(-s2, s2 + 1):
            try_set_loc(x, h, w, plus(loc, (i, j)))

def try_set_loc(x, h, w, loc):
    if in_range(h, w, loc):
        set_a(x, loc, True)

def make_corridor(x, h, w, loc):
    targets = {i: plus(loc, times(random.randint(5, 15), i)) for i in neighbors}
    targets = {i: j for i, j in targets.items() if in_range(h, w, j)}
    target = random.choice(stable_list(targets.keys()))
    while loc != targets[target]:
        set_a(x, loc, True)
        loc = plus(loc, target)
    return loc

def make_map(h, w):
    x = [[False for i in range(w)] for j in range(h)]
    loc = random.randint(1, h - 2), random.randint(1, w - 2)
    for k in range(random.randint(10, 25)):
        if random.random() < .7:
            make_room(x, h, w, loc)
        new_loc = make_corridor(x, h, w, loc)
        if random.random() < .8:
            loc = new_loc
    return x

class GameObject:
    def __init__(self, info_dict):
        for i in info_dict:
            self.__dict__[i] = info_dict[i]

    def get(self, x, default):
        return self.__dict__.get(x, default)

class ObjectCollection:
    def __init__(self):
        self.loc_to_object = {}
        self.object_to_loc = {}

    def add_obj_to_loc(self, loc, obj):
        t = tuple(loc)
        self.loc_to_object.setdefault(t, set())
        self.loc_to_object[loc].add(obj)

    def remove_obj_from_loc(self, loc, obj):
        t = tuple(loc)
        self.loc_to_object[t].remove(obj)
        if len(self.loc_to_object[t]) == 0:
            del self.loc_to_object[t]

    def add(self, loc, obj):
        t = tuple(loc)
        self.add_obj_to_loc(t, obj)
        self.object_to_loc[obj] = t

    def get_loc(self, obj):
        return self.object_to_loc[obj]

    def obj_at_loc(self, loc):
        t = tuple(loc)
        return self.loc_to_object.get(t, set())

    def move(self, new_loc, obj):
        self.remove(obj)
        self.add(tuple(new_loc), obj)

    def remove(self, obj):
        self.remove_obj_from_loc(self.get_loc(obj), obj)

order = '@fhjknr0)%'

def rank_symbol(x):
    if x in order:
        return order.index(x)
    else:
        raise Exception('Unknown item ' + x)

def is_empty(m, o, loc):
    r = at_for_move(m, o, loc)
    # removed boulder, change if you add it back
    return r != '#'

def move_toward(l1, l2):
    if l1 == l2:
        raise Exception('Two locations the same!')
    m = minus(l2, l1)
    return [plus(l1, i) for i in all_neighbors if inner(m, i) / (norm(i) * norm(m)) > .8]

def get_can_see(m, o, loc, p_loc):
    if dist(loc, p_loc) > 3.3:
        return False
    if loc == p_loc:
        return True
    current = {loc}
    seen = {loc}
    while True:
        new = {j for i in current for j in move_toward(i, p_loc)
        if is_empty(m, o, j) and j not in seen}
        if p_loc in new:
            return True
        if not new:
            return False
        current = new
        seen |= new

def disp_space(x, loc, empty, o, rem, p_loc):
    can_see = get_can_see(x, o, loc, p_loc)
    if can_see:
        objs = o.obj_at_loc(loc)
        if objs:
            r = min([i.symbol for i in objs], key=rank_symbol)
        else:
            r = '#.'[empty]
        rem[loc] = r
        return r
    elif loc in rem:
        return rem[loc]
    else:
        return ' '

def disp_board(x, obj, rem, p_loc):
    return '\n'.join(''.join(disp_space(x, (ind1, ind2), j, obj, rem, p_loc)
    for ind2, j in enumerate(i)) for ind1, i in enumerate(x))

def random_empty(m, o):
    return random.choice([(i, j) for i in range(len(m)) for j in range(len(m[0]))
    if get_a(m, (i, j)) and not o.obj_at_loc((i, j))])

def at_for_move(m, o, loc):
    objs = o.obj_at_loc(loc)
    for i in objs:
        # removed boulder, change if you add it back
        if i.get('alive', False):
            return i
    return '#.'[get_a(m, loc)]

def move_player(m, o, direction, player):
    changes = get_changes(m, o, direction, player)
    if type(changes) == str:
        return changes
    if changes is not None:
        for loc, i in changes:
            o.move(loc, i)
        return True
    else:
        return False

def kill(o, monster):
    if monster.get('player', False):
        # our monster is the player, kill it
        return death_message
    # turn monster into a corpse
    assert monster.alive
    # not anymore it won't be
    monster.symbol = '%'
    monster.description += ' corpse'
    monster.alive = False
    # put all the items of monster on the floor
    if monster.get('inventory', None):
        for i in monster.inventory:
            o.add(o.get_loc(monster), i)
        monster.inventory = set()
    assert not monster.alive

def local_attack(o, a, b):
    # general code for one monster attacking another, at least locally
    # a uses wielded weapon if any, otherwise hands
    weapon = a.get('wielded', None)
    max_attack_strength = weapon.power if weapon else a.get('attack', 0)
    attack_strength = max_attack_strength * (1 - random.random() / 3)
    armor = b.get('armor', None)
    max_defense_strength = (armor.power if armor else 0) + b.get('defense', 0)
    defense_strength = max_defense_strength * (1 - random.random() / 3)
    attack_through = max(attack_strength - defense_strength, 0)
    if attack_through > 0:
        b.hp -= attack_through
        if b.hp <= 0:
            return kill(o, b)
    assert b.hp > 0

def get_changes(m, o, direction, player):
    player_loc = o.get_loc(player)
    move_player_to = at_for_move(m, o, plus(direction, player_loc))
    # removed boulder case, change if you add it back
    if move_player_to == '.':
        return [(plus(direction, player_loc), player)]
    elif move_player_to == '#':
        return None
    elif 'a' <= move_player_to.symbol <= 'z' and move_player_to.get('alive', False):
        return local_attack(o, player, move_player_to) or []
    else:
        raise Exception('Have not handled ' + move_player_to.symbol)

def c_input(stdscr, message, board):
    show(stdscr, message, board)
    curses.echo()
    r = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return r

def trim_message(message):
    if '\n---\n' not in message:
        return ''
    else:
        return '\n---\n'.join(message.split('\n---\n')[1:])

def show(stdscr, message, state):
    stdscr.clear()
    m = message.replace('~', '').replace('^', '').split('\n---\n')[0]
    s = m + (('\n' + state) if '~' not in message else '')
    if s.count('\n') > 23:
        raise Exception('Too long!')
    stdscr.addstr(s)
    stdscr.move(m.count('\n'), len(m.split('\n')[-1]))

'''
kobold (omnivorous, intelligent, poisonous, has darts)
fungus (does not move, can reproduce)
jackal (carnivorous)
rat (nothing special)
newt (slow, weak, but slimy (it attacks you, there's a chance of getting slime on your hands, which can make you drop things and goes away after a few turns))
hellhound (stronger jackal, can attack with fire)
'''

def weapon(name, attack, t):
    return GameObject({'symbol': ')', 'description': name, 'power': max(0, attack + random.gauss(0, 1)), 'type': t})

def make_monster(i):
    if i == 'f':
        return GameObject({'symbol': 'f', 'description': 'fungus', 'immobile': True, 'diet': 'plant', 'alive': True, 'living': True,
        'attack': 0, 'defence': 1, 'hp': 7, 'maxhp': 7})
    elif i == 'h':
        return GameObject({'symbol': 'h', 'description': 'hellhound', 'diet': 'carnivore', 'alive': True, 'living': True, 'attacks': ['fire'],
        'attack': 10, 'defence': 6, 'hp': 12, 'maxhp': 12})
    elif i == 'j':
        return GameObject({'symbol': 'j', 'description': 'jackal', 'diet': 'carnivore', 'alive': True, 'living': True,
        'attack': 8, 'defence': 4, 'hp': 12, 'maxhp': 12})
    elif i == 'k':
        return GameObject({'symbol': 'k', 'description': 'kobold', 'intelligent': True, 'poisonous': True, 'diet': 'omnivore', 'alive': True, 'living': True,
        'inventory': {weapon('dart', 3, 'range') for _ in range(random.randint(5, 15))},
        'attack': 3, 'defence': 3, 'hp': 18, 'maxhp': 18})
    elif i == 'n':
        return GameObject({'symbol': 'n', 'description': 'newt', 'diet': 'insectivore', 'alive': True, 'living': True, 'slow': True, 'attacks': ['slime'],
        'attack': 2, 'defence': 4, 'hp': 3, 'maxhp': 3})
    elif i == 'r':
        return GameObject({'symbol': 'r', 'description': 'rat', 'diet': 'insectivore', 'alive': True, 'living': True,
        'attack': 2, 'defence': 4, 'hp': 5, 'maxhp': 5})


def random_monster():
    t = random.choice(''.join(i * n for (i, n) in (('f', 15), ('h', 2), ('j', 7), ('k', 4), ('n', 8), ('r', 8))))
    return make_monster(t)

def movable_items_here(player, o):
    return [i for i in o.obj_at_loc(o.get_loc(player)) if i.get('take-able', True) and not i.get('alive', False)]

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

def add_to_inv(player, o, items):
    for i in items:
        o.remove(i)
        player.inventory.add(i)

def rem_from_inv(player, o, items):
    loc = o.get_loc(player)
    for i in items:
        o.add(loc, i)
        player.inventory.remove(i)

def take(stdscr, player, o):
    m = movable_items_here(player, o)
    if len(m) == 0:
        return 'There is nothing here. ', False
    items = choose(stdscr, m)
    if len(items) + len(player.inventory) > 16:
        return 'You cannot carry all those items! ', False
    add_to_inv(player, o, items)
    return '', bool(items)

def drop(stdscr, player, o):
    if not player.inventory:
        return 'You have nothing to drop! ', False
    items = choose(stdscr, stable_list(player.inventory))
    rem_from_inv(player, o, items)
    return '', bool(items)

def item_disp(i, j):
    if type(j) not in (tuple, list):
        return f'{i} ({j.description})'
    else:
        return f'{i} ({j[0].description}): {"-+"[j[1]]}'

def items_disp(x):
    return '\n'.join(item_disp(i, j) for i, j in x.items())

def stable_list(x):
    return list(sorted(x, key=id))

def inv(player):
    return '~' + items_disp(give_letters(stable_list(player.inventory))) + '\n' or 'You have nothing. '

def main(stdscr):
    curses.use_default_colors()
    m = make_map(20, 76)
    o = ObjectCollection()
    player = GameObject({'symbol': '@', 'player': True, 'description': 'you', 'layer': True, 'diet': 'omnivore', 'alive': True, 'living': True, 'inventory': set(), 'attack': 4, 'defence': 4,
    'hp': 15, 'maxhp': 15})
    o.add(random_empty(m, o), player)
    for i in range(random.randint(10, 30)):
        o.add(random_empty(m, o), random_monster())
    rem = {}
    message = intro
    done = False
    while not done:
        show(stdscr, message, disp_board(m, o, rem, o.get_loc(player)))
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
        if i in {'h', 'KEY_LEFT', 'j', 'KEY_DOWN',
        'k', 'KEY_UP', 'l', 'KEY_RIGHT'}:
            if i in {'h', 'KEY_LEFT'}:
                res = move_player(m, o, (0, -1), player)
            elif i in {'j', 'KEY_DOWN'}:
                res = move_player(m, o, (1, 0), player)
            elif i in {'k', 'KEY_UP'}:
                res = move_player(m, o, (-1, 0), player)
            elif i in {'l', 'KEY_RIGHT'}:
                res = move_player(m, o, (0, 1), player)
            if not res:
                moved = False
                message = 'You cannot move that way! '
            if type(res) == str:
                message = res
        elif i == 'q':
            break
        elif i == ',':
            message, moved = take(stdscr, player, o)
        elif i == 'i':
            message = inv(player)
            moved = False
        elif i == 'd':
            message, moved = drop(stdscr, player, o)
        else:
            message = i + ' is not a command! '
            moved = False

if __name__ == '__main__':
    curses.wrapper(main)
