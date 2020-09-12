#GUI for the Black Hole: Escape game.

from tkinter import *
from os import path
from blackhole_helper import *
from random import shuffle
import csv

folder = 'D://' #your folder path with images and blackhole_scores.csv file.

class Cell(Button):
    def __init__(self, window, position, img, img_label):
        super().__init__(window, image=img, command=self.click)
        self.window = window
        self.position = position
        self.grid(padx=(10*(position[0]==0),0), pady=(10*(position[1]==0),0),
                  column=position[0], row=position[1])
        self.img_label = img_label
        self.is_human = True

    def update_img(self, new_img, new_img_label):
        self.configure(image=new_img)
        self.img_label = new_img_label

    def update_colors(self, colors):
        self.colors = colors

    def click(self):
        if self.window.app.game is not None:
            Move.clear_AI(self.window)
            if str(self.colors.index('human')) in self.img_label:
                if self.window.to_move is None:
                    PotentialMoves.mark(self.window, self.position)
                else:
                    PotentialMoves.clear(self.window)
            else:
                if 'potential' in self.img_label:
                    self.window.app.game.update_state(Move.make_human(self.window, self.window.to_move, self.position))
                else:
                    PotentialMoves.clear(self.window)

class Move:
    @staticmethod
    def make_AI(window, scores):
        state = window.app.game.state
        next_state = PlayerAI.make_move(state, scores, window.app.game.winning_memo)
        position = list(state[state[2]].difference(next_state[state[2]]))[0]
        try:
            next_position = list(next_state[state[2]].difference(state[state[2]]))[0]
        except IndexError:
            next_position = (2, 2)
        window.made_cache[position] = 'neutral'
        window.cells[position].update_img(window.images['neutral made'], 'neutral made')
        if next_position == (2, 2):
            window.cells[next_position].update_img(window.images['hole made'], 'hole made')
            window.made_cache[next_position] = 'hole'
        else:
            window.cells[next_position].update_img(window.images[str(state[2]) + ' made'], str(state[2]) + ' made')
            window.made_cache[next_position] = str(state[2]) + ' occupied'
        return next_state

    @staticmethod
    def clear_AI(window):
        for position in window.made_cache:
            window.cells[position].update_img(window.images[window.made_cache[position]],
                                              window.made_cache[position])
        window.made_cache.clear()

    @staticmethod
    def make_human(window, position, next_position):
        state = window.app.game.state
        next_state = PlayerHuman.make_move(state, position, next_position)
        PotentialMoves.clear(window)
        window.cells[position].update_img(window.images['neutral'], 'neutral')
        if next_position != (2, 2):
            window.cells[next_position].update_img(window.images[str(state[2]) + ' occupied'],
                                                   str(state[2]) + ' occupied')
        return next_state

class PotentialMoves:
    @staticmethod
    def mark(window, position):
        state = window.app.game.state
        window.potential_cache[position] = str(state[2]) + ' occupied'
        _potential_moves = PlayerHuman.potential_moves(state, position)
        for _next_pos in _potential_moves:
            if _next_pos == (2, 2):
                window.cells[_next_pos].update_img(window.images['hole potential'], 'hole potential')
                window.potential_cache[_next_pos] = 'hole'
            else:
                window.cells[_next_pos].update_img(window.images['neutral potential'], 'neutral potential')
                window.potential_cache[_next_pos] = 'neutral'
        window.to_move = position

    @staticmethod
    def clear(window):
        for position in window.potential_cache:
            window.cells[position].update_img(window.images[window.potential_cache[position]],
                                              window.potential_cache[position])
        window.potential_cache.clear()
        window.to_move = None

class PlayerHuman:
    @staticmethod
    def potential_moves(state, position):
        return positions_after_move(state, position)

    @staticmethod
    def make_move(state, position, next_position):
        _next_state = [state[0].copy(), state[1].copy(), state[2]]
        _next_state[state[2]].remove(position)
        if next_position != (2,2):
            _next_state[state[2]].add(next_position)
        _next_state[2] ^= 1
        return _next_state

class PlayerAI:
    @staticmethod
    def get_score(state, scores):
        if len(state[0]) == 2: return 2
        if len(state[1]) == 2: return -2
        _state_to_num = state_to_num(state)
        if _state_to_num in scores:
            return scores[_state_to_num]
        return 0

    @staticmethod
    def make_move(state, scores, winning_memo):
        _next_states_sets = next_states_sets(state)
        allowed = []
        if state[2] == 0:
            curr_score = -1
            chosen_ns = None
            for ns in _next_states_sets:
                _ns_score = PlayerAI.get_score(ns, scores)
                if _ns_score == 2:
                    return ns
                elif _ns_score == 1:
                    if (frozenset(ns[0]), frozenset(ns[1]), ns[2]) not in winning_memo:
                        winning_memo.add((frozenset(ns[0]), frozenset(ns[1]), ns[2]))
                        chosen_ns = ns
                if _ns_score > curr_score:
                    allowed = [ns]
                    curr_score = _ns_score
                elif _ns_score == curr_score:
                    allowed.append(ns)
            if chosen_ns is not None: return chosen_ns
            shuffle(allowed)
            allowed.sort(key=lambda x: len(x[0]))
        else:
            curr_score = 1
            chosen_ns = None
            for ns in _next_states_sets:
                _ns_score = PlayerAI.get_score(ns, scores)
                if _ns_score == -2:
                    return ns
                elif _ns_score == -1:
                    if (frozenset(ns[0]), frozenset(ns[1]), ns[2]) not in winning_memo:
                        winning_memo.add((frozenset(ns[0]), frozenset(ns[1]), ns[2]))
                        chosen_ns = ns
                if _ns_score < curr_score:
                    allowed = [ns]
                    curr_score = _ns_score
                elif _ns_score == curr_score:
                    allowed.append(ns)
            if chosen_ns is not None: return chosen_ns
            shuffle(allowed)
            allowed.sort(key=lambda x: len(x[1]))
        return allowed[0]

class Window(Tk):

    colors = ['red', 'green']
    def __init__(self, app):
        super().__init__()
        self.title("Black Hole: Escape")
        self.geometry('800x600')
        self.potential_cache = {}
        self.made_cache = {}
        self._upload_images()
        self.init_grid()
        self.app = app
        self.init_menu()
        self.to_move = None

    def _upload_images(self):
        self.images = {}
        self.images['neutral'] = PhotoImage(file=path.join(folder, 'cell_neutral.png'))
        self.images['hole'] = PhotoImage(file=path.join(folder, 'cell_hole.png'))
        self.images['0 occupied'] = PhotoImage(file=path.join(folder, 'cell_red.png'))
        self.images['1 occupied'] = PhotoImage(file=path.join(folder, 'cell_green.png'))
        self.images['neutral potential'] = PhotoImage(file=path.join(folder, 'cell_move.png'))
        self.images['0 potential'] = PhotoImage(file=path.join(folder, 'cell_move_red.png'))
        self.images['1 potential'] = PhotoImage(file=path.join(folder, 'cell_move_green.png'))
        self.images['hole potential'] = PhotoImage(file=path.join(folder, 'cell_move_hole.png'))
        self.images['neutral made'] = PhotoImage(file=path.join(folder, 'cell_move_made.png'))
        self.images['0 made'] = PhotoImage(file=path.join(folder, 'cell_move_made_red.png'))
        self.images['1 made'] = PhotoImage(file=path.join(folder, 'cell_move_made_green.png'))
        self.images['hole made'] = PhotoImage(file=path.join(folder, 'cell_move_made_hole.png'))

    def init_menu(self):
        self.msg = Label(self, width=40, height=1, text='Press one of the buttons below:')
        self.msg.place(x=500, y=80)
        self.rednew = Button(self, text='New game, red pawns (first to move)', width=40, height=1,
                             bg='#ff795c', command=self.start_red)
        self.rednew.place(x=500, y=100)
        self.greennew = Button(self, text='New game, green pawns (second to move)', width=40, height=1,
                             bg='#90fea9', command=self.start_green)
        self.greennew.place(x=500, y=125)

    def init_grid(self, state=({(0,0), (1,1), (3,1), (4,0)}, {(0,4), (1,3), (3,3), (4,4)}, 0)):
        self.cells = {}
        for position in [(i, j) for i in range(5) for j in range(5)]:
            if position in state[0]:
                img_label = '0 occupied'
            elif position in state[1]:
                img_label = '1 occupied'
            elif position == (2, 2):
                img_label = 'hole'
            else:
                img_label = 'neutral'
            _cell = Cell(self, position, self.images[img_label], img_label)
            self.cells[position] = _cell

    def start_red(self):
        self.app.init_game(['human', 'AI'])

    def start_green(self):
        self.app.init_game(['AI', 'human'])
        self.app.game.state = Move.make_AI(self, self.app.scores)

    def update_color_cells(self, colors):
        for cell in self.cells:
            self.cells[cell].update_colors(colors)

class App():
    def __init__(self):
        self.game = None
        self.window = Window(self)
        self.scores = {}
        self.get_scores()
        self.window.mainloop()

    def get_scores(self):
        ind = 0
        with open(path.join(folder, 'blackhole_scores.csv'), 'r', newline='') as csvfile:
            _reader = csv.reader(csvfile, delimiter=';')
            for row in _reader:
                self.scores[eval(row[0])] = int(row[1])
                if ind % 100000 == 0: print('Loading scores.. ', round(100*ind/4240000, 2), '%')
                ind += 1
            print('Loading scores.. 100 %')

    def init_game(self, colors):
        self.window.init_grid()
        self.game = Game(colors, self)
        self.window.msg['text'] = 'In progress, draw at the moment.'

class Game():
    def __init__(self, colors, app):
        self.state = ({(0, 0), (1, 1), (3, 1), (4, 0)}, {(0, 4), (1, 3), (3, 3), (4, 4)}, 0)
        self.status = 'In progress, draw at the moment.'
        self.colors = colors
        self.app = app
        self.app.window.update_color_cells(colors)
        self.winning_memo = set()

    def update_state(self, new_state):
        self.state = new_state
        if len(self.state[0]) > 2 and len(self.state[1]) > 2:
            self.state = Move.make_AI(self.app.window, self.app.scores)
            if len(self.state[self.colors.index('AI')]) == 2:
                self.app.window.msg['text'] = 'Finished, AI won.'
                self.app.game = None
            else:
                if (PlayerAI.get_score(self.state, self.app.scores) == 1 and self.colors.index('human') == 0) or \
                        (PlayerAI.get_score(self.state, self.app.scores) == -1 and self.colors.index('human') == 1):
                    self.app.window.msg['text'] = 'In progress, player may force the win.'
                elif (PlayerAI.get_score(self.state, self.app.scores) == 1 and self.colors.index('AI') == 0) or \
                        (PlayerAI.get_score(self.state, self.app.scores)== -1 and self.colors.index('AI') == 1):
                    self.app.window.msg['text'] = 'In progress, AI is forcing the win.'
                else:
                    self.app.window.msg['text'] = 'In progress, draw at the moment.'
        elif len(self.state[self.colors.index('human')]) == 2:
            self.app.window.msg['text'] ='Finished, player won.'
            self.app.game = None
        elif len(self.state[self.colors.index('AI')]) == 2:
            self.app.window.msg['text'] ='Finished, AI won.'
            self.app.game = None

app = App()
