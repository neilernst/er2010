""" A simple way to manipulate global state """
solution = set([])
time = 0
tabu_list = []
tlim = 0
checks = 0
expire = 0# 1/5th of the total time
memoized_fail = [] # sets we tried for admissibility and failed (make it faster)
memoized_succ = [] # sets we tried for admissibility and succeeded (make it faster)