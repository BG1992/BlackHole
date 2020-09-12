from sympy.functions.combinatorial.numbers import binomial
from operator import itemgetter

vecs = [(0,1), (0,-1), (1,0), (-1,0)]

#all pawn positions after possible moves are made
def positions_after_move(state, pawn):
    _positions_after_move = []
    for vec in vecs:
        i = 1
        while pawn[0] + i * vec[0] <= 4 and pawn[0] + i * vec[0] >= 0 and \
                pawn[1] + i * vec[1] <= 4 and pawn[1] + i * vec[1] >= 0 and \
                (pawn[0] + i * vec[0], pawn[1] + i * vec[1]) not in state[0] and \
                (pawn[0] + i * vec[0], pawn[1] + i * vec[1]) not in state[1]:
            i += 1
        if i > 1: _positions_after_move.append((pawn[0] + (i-1)*vec[0], pawn[1] + (i-1) * vec[1]))

    return _positions_after_move

#all states after possible moves of a given pawn
def states_after_move(state, pawn):
    _states_after_move = []
    for vec in vecs:
        i = 1
        while pawn[0] + i*vec[0] <= 4 and pawn[0] + i*vec[0] >= 0 and \
            pawn[1] + i*vec[1] <= 4 and pawn[1] + i*vec[1] >= 0 and \
            (pawn[0] + i*vec[0], pawn[1] + i*vec[1]) not in state[0] and \
            (pawn[0] + i*vec[0], pawn[1] + i*vec[1]) not in state[1]:
            i += 1
        if i > 1:
            new_state = list(state)
            new_state[state[2]] = new_state[state[2]].difference({pawn})
            if (pawn[0] + (i-1)*vec[0], pawn[1] + (i-1)*vec[1]) != (2,2):
                new_state[state[2]].add((pawn[0] + (i-1)*vec[0], pawn[1] + (i-1)*vec[1]))
            new_state[2] ^= 1
            _states_after_move.append(tuple(new_state))

    return _states_after_move

#all children of the state, given in the 5-elements tuple
def next_states(state):
    _next_states = []
    for pawn in state[state[2]]:
        _next_states += states_after_move(state, pawn)
    return list(map(lambda x: state_to_num(x), _next_states))

#all children of the state, given in the 3-elements tuple
def next_states_sets(state):
    _next_states = []
    for pawn in state[state[2]]:
        _next_states += states_after_move(state, pawn)
    return _next_states

#horizontal symmetry of the board
def sym_horizontal(s):
    _s = set()
    for w in s:
        _s.add((4 - w[0], w[1]))
    return _s

#vertical symmetry of the board
def sym_vertical(s):
    _s = set()
    for w in s:
        _s.add((w[0], 4 - w[1]))
    return _s

#left diagonal symmetry of the board
def sym_left_diag(s):
    _s = set()
    for w in s:
        _s.add((w[1], w[0]))
    return _s

#right diagonal symmetry of the board
def sym_right_diag(s):
    _s = set()
    for w in s:
        _s.add((4 - w[1], 4 - w[0]))
    return _s

#90 degree clockwise rotation of the board
def rot_90(s):
    _s = set()
    for w in s:
        _s.add((w[1], 4-w[0]))
    return _s

#converting state as 3-element tuple to 5-element tuple, including reducing states space via symmetry/rotations
def state_to_num(state):
    nums = []
    nums.append(comb_to_num(vec_to_comb(state[0])) + comb_to_num(vec_to_comb(state[1])) + (state[2],))

    _state = (sym_horizontal(state[0]), sym_horizontal(state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (sym_vertical(state[0]), sym_vertical(state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (sym_left_diag(state[0]), sym_left_diag(state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (sym_right_diag(state[0]), sym_right_diag(state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (rot_90(state[0]), rot_90(state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (rot_90(_state[0]), rot_90(_state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    _state = (rot_90(_state[0]), rot_90(_state[1]), state[2])
    nums.append(comb_to_num(vec_to_comb(_state[0])) + comb_to_num(vec_to_comb(_state[1])) + (_state[2],))

    nums.sort(key= itemgetter(1, 3))
    return nums[0]

#get the index of combination
def comb_to_num(comb):
    _comb = sorted(list(comb), reverse=True)
    k = len(_comb)
    n = 0
    for i in range(len(_comb)):
        n += int(binomial(_comb[i], k-i))
    return (k, n)

#get the combination from its index
def num_to_comb(k, n):
    if k == 0: return set()
    _comb = set()
    _k, _n = k, n
    while len(_comb) < k:
        i = _k-1
        res = 0
        while res <= _n:
            res = binomial(i, _k)
            i += 1
        _comb.add(i-2)
        _n -= binomial(i-2, _k)
        _k -= 1
    return _comb

#get the set of 2D points from single numbers
def comb_to_vec(comb):
    vec = set()
    for el in comb:
        vec.add((el//5, el % 5))
    return vec

#get the set of single numbers from 2D points
def vec_to_comb(vec):
    comb = set()
    for el in vec:
        comb.add(el[0]*5 + el[1])
    return comb

