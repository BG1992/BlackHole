#Generation of the 4x4 subspace. Same can be easily done for the rest of subspaces.

from itertools import combinations
from blackhole_helper import *
from time import perf_counter
import csv

squares = {(i,j) for i in range(5) for j in range(5)}.difference({(2,2)})

children = set()
white_children = set()
ind = 0
in_memo = 0
with open('D://blackhole44_children.csv', 'w', newline='') as csvfile:
    _writer = csv.writer(csvfile, delimiter=';')
    for white in combinations(squares, 4):
        _white = set(white)
        __white = state_to_num((_white, {(2,2)}, 1))
        if __white not in white_children:
            st = perf_counter()
            print(white, len(children), ind, in_memo, len(white_children))
            for black in combinations(squares.difference(_white), 4):
                _black = set(black)
                state = (_white, _black, 0)
                num = state_to_num(state)
                if num not in children:
                    children.add(num)
                    _writer.writerow([num, next_states(state)])
                else:
                    in_memo += 1
                state = (_white, _black, 1)
                num = state_to_num(state)
                if num not in children:
                    children.add(num)
                    _writer.writerow([num, next_states(state)])
                else:
                    in_memo += 1
            white_children.add(__white)
            ind += 1
            print(perf_counter() - st)
