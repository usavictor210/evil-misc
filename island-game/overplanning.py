species_abbreviations = {
    'a': 'aqua',
    'b': 'bat',
    'c': 'cow',
    'd': 'dragon',
    'e': 'eagle',
    'f': 'frog',
    'g': 'goat',
    'h': 'human',
    'i': 'impala',
    'j': 'jellyfish',
    'k': 'kraken',
    'l': 'lion',
    'm': 'mermaid',
    'n': 'newt',
    'o': 'owl',
    'p': 'phoenix',
    'q': 'quetzel',
    'r': 'rat',
    's': 'sheep',
    't': 'troll',
    'u': 'unicorn',
    'v': 'vulture',
    'w': 'wolf',
    'x': 'x',
    'y': 'yak',
    'z': 'zebra'
}

# todo: remove racism against dryads, dwarves, and elves
races_abbreviations = {
    'a': {'a': 'aqua', 'd': 'dryad'},
    'h': {'h': 'human', 'e': 'elf', 'd': 'dwarf'}
}


species_info = {
    'aa': {
        'name': 'aqua aqua',
        'home': '~',
        'allowed': ' ~#*',
        'features': ['intelligent', 'humanoid', 'spirit'],
        'size': 'medium',
        'eats': []
    },
    'ad': {
        'name': 'aqua dryad',
        'home': '#',
        'allowed': ' ~#*',
        'features': ['intelligent', 'humanoid', 'spirit'],
        'size': 'medium',
        'eats': []
    },
    'b': {
        'name': 'bat',
        'home': '#*',
        'allowed': ' #*',
        'features': ['flying'],
        'size': 'small',
        'eats': ['insects']
    },
    'c': {
        'name': 'cow',
        'home': ' #',
        'allowed': ' #',
        'features': ['domestic'],
        'size': 'medium',
        'produces': ['milk'],
        'eats': ['grass']
    },
    'd': {
        'name': 'dragon',
        'home': '*',
        'allowed': ' #*',
        'features': ['intelligent', 'flying', 'fire-breathing', 'claws'],
        'size': 'large',
        'produces': ['eggs'],
        'eats': ['meat']
    },
    'e': {
        'name': 'eagle',
        'home': '#*',
        'allowed': ' #*',
        'features': ['flying', 'claws'],
        'size': 'medium',
        'produces': ['eggs'],
        'eats': ['meat']
    },
    'f': {
        'name': 'frog',
        'home': ' #',
        'allowed': ' #',
    },
    'g': {
        'home': ' #',
        'allowed': ' #'
    },
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
    'i': {
        'home': ' ',
        'allowed': ' '
    },
    'i': {
        'home': ' ',
        'allowed': ' '
    },
    'i': {
        'home': ' ',
        'allowed': ' '
    },
    's': {
        'home': ' #',
        'allowed': ' #'
    }
}

home_environments = {
    'aa': '~',
    'ad': ' #',
    'b': '*',
    'c': ' #',
    'd': ' #*',
    'e': ''
}

allowed_environments = {
    'aa': '~',
    'ad': ' #',
    'b': '*',
    'c': ' #',
    'd': ' #*'
}
