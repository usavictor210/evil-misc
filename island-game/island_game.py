import sys

import island

import curses

import random

def rrange(a, b, c):
    while a < b + c / 2:
        yield a
        a += c
    return a

def display(stdscr, player, game_data, inc):
    size = 10
    i, j = player.location
    start_and_end = '+' + '-' * (2 * size + 1) + '+'
    l = [[island.main(a, b) for b in rrange(
        j - size * inc, j + size * inc, inc)]
        for a in rrange(i - size * inc, i + size * inc, inc)]
    game_data.modify_display(l, player.location, inc)
    stdscr.clear()
    stdscr.addstr(
        start_and_end + '\n' + '\n'.join('|' + ''.join(i) + '|' for i in l) +
        '\n' + start_and_end)

dirs = {
    'KEY_UP': (-.1, 0),
    'KEY_DOWN': (.1, 0),
    'KEY_LEFT': (0, -.1),
    'KEY_RIGHT': (0, .1)
}

def add(a, b):
    return tuple(i + j for i, j in zip(a, b))

def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))

def okay(new_player_location, player, game_data):
    if island.main(*new_player_location) not in player.environments():
        return False, 'You cannot go in the ' + \
            env_names[island.main(*new_player_location)] + '!'
    elif game_data.object_locs.rcontains(new_player_location):
        return False, 'You cannot go to an occupied location!'
    else:
        return True, None

data = {
   'hd': {
       'home': '*',
       'allowed': ' #*'
   },
   'he': {
       'home': '#',
       'allowed': ' #*'
   },
   'hh': {
       'home': ' ',
       'allowed': ' #*'
   },
   'm': {
       'home': '~',
       'allowed': '~'
   }
}

env_names = {
    ' ': 'grassland',
    '~': 'ocean',
    '#': 'forest',
    '*': 'mountain'
}

all_environments = ' ~#*'

class Player:
    def __init__(self, location, species, race):
        self.location = location
        self.species = species
        self.race = race
        self.symbol = '@'

    def environments(self):
        return data[self.species + self.race]['allowed']

class Animal:
    def __init__(self, location, species, race=''):
        self.location = location
        self.species = species
        self.race = race
        self.symbol = species

    def environments(self):
        return data[self.species + self.race]['allowed']

def get_appropriate_animal(loc):
    k = random.choice(list(data.keys()))
    if island.main(*loc) in data[k]['home']:
        return Animal(loc, *k)

def debug(m):
    with open('debug.txt', 'a') as f:
        f.write(str(m) + '\n')

class ObjectLocs:
    def __init__(self, d):
        self.d = d
        self.rev = {}
        for i in self.d:
            self.rev.setdefault(self.d[i], set())
            self.rev[self.d[i]].add(i)

    def modify(self, key, value):
        if key in self.d:
            self.rev[self.d[key]].remove(key)
            if not self.rev[self.d[key]]:
                del self.rev[self.d[key]]
        self.d[key] = value
        self.rev.setdefault(value, set())
        self.rev[value].add(key)

    def contains(self, key):
        return key in self.d

    def rcontains(self, value):
        return bool(self.rev.get(value))

    def items(self):
        return self.d.items()

    def keys(self):
        return self.d.keys()

    def get(self, key):
        return self.d[key]

def prec(t):
    return tuple(round(i, 1) for i in t)

class GameData:
    def __init__(self, player):
        self.locs = set()
        self.player = player
        self.object_locs = ObjectLocs({player: player.location})

    def player_at(self, loc):
        self.object_locs.modify(self.player, self.player.location)
        i, j = loc
        size = 10
        inc = .1
        for loc_i in rrange(i - 2 * size * inc, i + 2 * size * inc, inc):
            for loc_j in rrange(j - 2 * size * inc, j + 2 * size * inc, inc):
                new_loc = round(loc_i, 1), round(loc_j, 1)
                if new_loc in self.locs:
                    continue
                self.locs.add(new_loc)
                if random.random() < .01 and \
                    not self.object_locs.rcontains(new_loc):
                    self.spawn(new_loc)

    def spawn(self, loc):
        animal = get_appropriate_animal(loc)
        if animal is not None:
            self.object_locs.modify(animal, loc)

    def move_all(self):
        for i in self.object_locs.keys():
            if i == self.player:
                continue
            rdir = random.choice(list(dirs.values()))
            new_loc = prec(add(rdir, self.object_locs.get(i)))
            if okay(new_loc, i, self)[0]:
                self.object_locs.modify(i, new_loc)

    def modify_display(self, display, loc, inc):
        size = 10
        d = {}
        epsilon = 1e-5
        for i, place in self.object_locs.items():
            coords = tuple(j / inc for j in sub(place, loc))
            if all(-size - epsilon < j < size + epsilon for j in coords) and \
                all(abs(round(j) - j) < epsilon for j in coords):
                assert 0 <= round(coords[0]) + size < len(display)
                assert 0 <= round(coords[1]) + size < len(display[0])
                if display[round(coords[0]) + size][round(coords[1]) + size] \
                    not in all_environments:
                    raise Exception('Two things in one place!')
                display[round(coords[0]) + size][round(coords[1]) + size] = \
                    i.symbol[0]




def main(stdscr):
    if len(sys.argv) < 2 or sys.argv[1] != 'random':
        loc = (343395, 476890)
    else:
        while True:
            loc = (random.randrange(0, 10 ** 6), random.randrange(0, 10 ** 6))
            if island.main(*loc) != '~':
                break
    inc = .1
    stdscr.clear()
    player = Player(loc, 'h', 'h')
    game_data = GameData(player)
    curses.curs_set(0)
    message = ''
    game_data.player_at(player.location)
    while True:
        display(stdscr, player, game_data, inc)
        stdscr.addstr(message)
        stdscr.refresh()
        message = ''
        k = stdscr.getkey()
        if k == 'q':
            curses.curs_set(1)
            return
        elif k == 'g':
            inc *= 2
        elif k == 'l':
            inc /= 2
        elif k == 'd':
            inc = .1
        elif k in dirs:
            new_player_location = prec(add(player.location, dirs[k]))
            test, msg = okay(new_player_location, player, game_data)
            if not test:
                message = '\n' + msg
            else:
                player.location = new_player_location
            game_data.player_at(player.location)
            game_data.move_all()


if __name__ == '__main__':
    curses.wrapper(main)
