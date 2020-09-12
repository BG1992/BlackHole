#Iteration process for 4x4 subspace. Same can be easily done for the rest of subspaces. 

import csv
from blackhole_helper import *

memo = {}

ind = 0
with open('D://blackhole34_scores.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        memo[eval(row[0])] = int(row[1])
        if ind % 10000 == 0: print(ind)
        ind += 1

ind = 0
with open('D://blackhole43_scores.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        memo[eval(row[0])] = int(row[1])
        if ind % 10000 == 0: print(ind)
        ind += 1

ind = 0
with open('D://blackhole44_children.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        memo[eval(row[0])] = 0
        if ind % 10000 == 0: print(ind)
        ind += 1

start_state = ({(0,0), (1,1), (3,1), (4,0)}, {(0,4), (1,3), (3,3), (4,4)}, 0)
start_state_num = state_to_num(start_state)

def get_value(state):
    if state[0] == 2: return 1
    if state[2] == 2: return -1
    return memo[state]

all_updated = [0]
def f():
    updates = 0
    ind = 0
    with open('D://blackhole44_children.csv', 'r', newline='') as csvfile:
        _reader = csv.reader(csvfile, delimiter=';')
        for row in _reader:
            state = eval(row[0])
            children = eval(row[1])
            if memo[state] == 0:
                if state[4] == 0:
                    curr_score = -1
                    for child in children:
                        curr_score = max(curr_score, get_value(child))
                        if curr_score == 1: break
                else:
                    curr_score = 1
                    for child in children:
                        curr_score = min(curr_score, get_value(child))
                        if curr_score == -1: break
                if memo[state] != curr_score:
                    memo[state] = curr_score
                    updates += 1
                    all_updated[0] += 1
            if ind % 10000 == 0: print(ind, updates, len(memo), all_updated, memo[start_state_num])
            ind += 1
    return updates

ind = 0
while 1:
    updates = f()
    print(ind, updates, len(memo), all_updated)
    ind += 1
    if ind % 5 == 0:
        with open('D://blackhole44_scores' + str(ind) + '.csv', 'w', newline='') as csvfile:
            _writer = csv.writer(csvfile, delimiter=';')
            for el in memo:
                _writer.writerow([el, memo[el]])
    if updates == 0: break

with open('D://blackhole44_scores_final.csv', 'w', newline='') as csvfile:
    _writer = csv.writer(csvfile, delimiter=';')
    for el in memo:
        _writer.writerow([el, memo[el]])
