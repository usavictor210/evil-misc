import sys

if sys.version_info[0] < 3:
    raise Exception('Use Python 3!')

import math

# ~ = ocean, * = mountain, # = forest, empty = normal (meadow)

c = lambda x, y: '~' if x < 0 else '*' if x >= 2 else '#' if y >= 7 else ' '

# in this world weather comes from the west, apparently
rain = lambda i, j: 10 - sum(f(i, j - k) for k in range(1, 6))

f = lambda i, j: sum(k ** .2 * (
    math.sin(i / (2 ** k + 1) + j / (2 ** k - 1)) +
    math.cos(i / (2 * 2 ** k + 1) - j / (2 * 2 ** k - 1)) - 1
    ) for k in range(2, 10))

def main(down, right):
    return c(f(down, right), rain(down, right))
