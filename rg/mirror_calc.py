import math
import sys

def cap_upgrades(log_cap_power):
    # initial log
    req = 0
    res = 0
    log_mult = math.log(1.5)
    while req <= log_cap_power:
        res += 1
        req += log_mult
        if req > math.log(2 ** 64):
            log_mult += math.log(257 / 256)
    return res

def mirror_price(m, log_cap_power, extra_twos):
    n = 1
    div = 1 + cap_upgrades(log_cap_power) / 1024
    n_plus = float('inf')
    def f(x):
        return math.log(64) * (m + 2) + math.log(x) * (2 * m + 4) + \
        math.log(2) * extra_twos > \
        math.log(16) + math.log(100) * (m + 1) + math.log(2) * (x / div)
    while not f(n):
        n += 1
    while n + 1 < n_plus:
        half = (n + n_plus) // 2 if n_plus < float('inf') else n * 2
        if f(half):
            n = half
        else:
            n_plus = half
    return n_plus

def equib(cap_power, extra_twos):
    m = 30
    n = float('inf')
    while m + 1 < n:
        half = (m + n) // 2 if n < float('inf') else m * 2
        if mirror_price(half, cap_power, extra_twos) >= int((half + 1) * (16 + half / 20)):
            m = half
        else:
            n = half
    return n

def print_data(i, a, b):
    p = mirror_price(i, a, b)
    get_10_exp = (p / 2048) ** 2 + math.log(2, 10)
    exp = int(get_10_exp)
    mant = 10 ** (get_10_exp - exp)
    print(i, p, (i + 1) * 16, int((i + 1) * (16 + i / 20)), str(mant) + 'e' + str(exp))

if __name__ == '__main__':
    if sys.argv[1] == 'iter':
        x, b = math.log(float(sys.argv[2])), float(sys.argv[3])
        eter = float(sys.argv[4])
        import time
        while True:
            i = equib(x, b)
            print_data(i, x, b)
            reward = (mirror_price(i, x, b) / 2048) ** 2 * math.log(2)
            dims = sum(reward > math.log(i) for i in (1, 16, 256, 2 ** 16, 2 ** 32))
            x = reward * dims - math.log(2) * sum((0, 4, 8, 16, 32)[:dims]) + math.log(1e5) * dims + math.log(32 * 16) + math.log(eter) * dims
            if reward > math.log(2 ** 24):
                x += math.log(math.log(x, 2)) * dims
            time.sleep(.1)
    elif len(sys.argv) == 3:
        i = equib(math.log(float(sys.argv[1])), float(sys.argv[2]))
        print_data(i, float(sys.argv[1]), float(sys.argv[2]))
    else:
        for i in range(int(sys.argv[1]), int(sys.argv[2])):
            print_data(i, math.log(float(sys.argv[3])), float(sys.argv[4]))

# Call the reset: reflect
# You get reflections and reflection points.
# You can buy, with reflection points, mirror power and replicanti galaxies.
# number of mirrors = mirror power + floor((percent / 100 + 1) ** mirrors) - 1
# effect of mirrors: replication number is multiplied by mirrors + 1
# effect of replicanti galaxies: increase in replicanti is raised to a power,
# as if it happened (replicanti galaxies + 1) times.
# also, speed of light is (2^2^10)^((rg + 1)^2)
# you can't grow by a factor of more than this per second.

# That settles it. It's going to be 2^2^14 per x2,
# prices 2^(((n + 1) * 16 + int(1.1 ** n) - 1)^2 - 1), n starting from 1
# except... we really kind of want replicanti galaxies too.
# What do they do? I think they should give a rather small boost.
# Hmm...
# How about this: they make everything go (rg + 1) times quicker,
# and time dimensions produce extra replicanti galaxies rather quickly?
# This makes everything after first rg price reflection points rather quick, which is good,
# since if we have x2^2^10 every second at the end it takes 2^16 seconds to get
# eternity, which is too many, but if we have 10 or 20 rg
# this becomes much better (a few hours).

# Replicanti galaxies are almost certainly too expensive at 1e170 RP. Some simple calculation says that around 10 mirrors,
# it will take at least 5 hours per mirror, probably 10 or 15, even more probably a day, maybe even a few days.
# Instead, rg prices will be 16^(n^2) RP, starting at 16 RP. At this point, with 10 mirrors, we have 5 rg,
# and above becomes:
# It will take at least 1 hour per mirror, probably 2 or 3, even more probably 5 hours, maybe even 10 or 15 hours.
# I can live with that. It's maybe a bit slow, but it's tolerable.

# We thought we needed a speed of light, but no.
# Speed of light is fairly useless when all you're doing is lifting the cap.

# Milestones: 6 autobuyers:
# 1: chance autobuyer
# 2: cap autobuyer
# 4: replication number autobuyer
# 8: softness autobuyer
# 16: reset autobuyer
# 32: reflection autobuyer
# four bonuses (3, 6, 12, 24):
# 3: start with 100% replication chance
# 6: start with infinite cap
# 12: start with 256 replication number
# 24: start with 16 softness

# It's actually 2^2^28 where the reset happens.
# Just 2^16 cap points is enough for the biggest numbers.

# Really, galactic dimensions will need to be very strong to have
# any noticable impact at all; basically, they'll need
# to produce 2^2^10 replicanti galaxies. Doing this
# in a non-trivial way is really tough. What's useful
# is if these galaxies are produced in a natural way.

# Another idea: cap upgrades. Upgrade the cap by 2^2^64 and see what happens.

# An improvement to both (maybe?): cap dimensions. Each multiple of 17 / 16
# in cap power, the cap limit doubles.
# What one should perhaps do is have 5 cap dimensions,
# with initial prices 1, 16, 256, 4096, 2^16.
# Price x2 each time you buy, but power x16 (except first time).

# Next reset is called overflow, you have overflows and overflow points (OP).

# First cap dimension is multiplied by log2(log2(replicanti)): 16 OP.
# Cap dimensions are multiplied by overflows: 256 OP.
# Each cap limit double gives a free replicanti galaxy: 4096 OP.
# Overflow autobuyer: 2^16 OP.

# This could lead to runaway inflation in theory, and apparently it actually does in practice.
# Who expected that?

# Way we deal with this: after a certain point, cap upgrade requirement increases quadratically,
# which apparently resolves the problem.

# Keep reflections (but not reflection points) on overflow.
