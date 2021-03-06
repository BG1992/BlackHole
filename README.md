# Black Hole: Escape - strongly solved?

Looks like I have managed to strongly solve the Black Hole: Escape abstract strategy board game. Game description can be found here: https://boardgamegeek.com/boardgame/64229/black-hole-escape, here: https://www.youtube.com/watch?v=GMsibjRgRO8, or here (in Polish only): https://rygalo.com/2016/10/06/black-hole-escape/.

In a nutshell, the game is played on 5x5 board with a hole in the center. Each of two players has four pawns, placed as in the picture below:

![Starting position](https://github.com/BG1992/BlackHole/blob/master/bh_start.png)

Players alternate turns. A turn in the game consists in moving chosen pawn either horizontally or vertically till stopped by other pawn (it does not matter whether it is player's pawn or enemy's pawn) or an edge of the board. While moving, a pawn jumps over the hole, if the hole pass through its route. However, if the pawn is stopped by other pawn while landed on the hole, the pawn is removed. Player who manages to remove two own pawns, wins. Pawns cannot be moved diagonally, cannot be captured.

Based on my calculations, I am claiming neither player is able to force the win, assuming both play perfectly.

Some technical details on the calculations:

1) While computing, the states space has been split into four separate classes: (3x3, 3x4, 4x3, 4x4), where axb stands for the subspace containing states with a red pawns and b green pawns.

2) Since the game is described by Directed Cyclic Graphs (DCGs) - no dfs/bfs was applied. To overcome the issue with repeated states, an iterative approach was used, till the lack of updates of states:

a) For each state of the given subspace mark terminal states as 1 or -1, depending on who is a winner of this state and remaining states as 0.

b) Go through all states of the given subspace and for each state marked as 0 and compute max/min (depending on who is to move) of scores of its children.

c) Repeat b) till the lack of updates.

3) Children were generated before the iteration processes and stored in csv. After iteration processes, scores have been saved and stored in csv.

4) Symmetries and rotations of the board were used to reduce size of the states space.

5) File blackhole_scores.csv contains only winning/losing states. If some state is a draw, it is not contained in the file (to reduce size of the file).

6) States are converted to tuple: (number of red pawns, index of the combination representing positions of the red pawns, number of green pawns, index of the combination representing positions of the green pawns, player to move). Index of the combination is described here: https://en.wikipedia.org/wiki/Combinatorial_number_system.

7) AI does not rush into a win from draw positions - for instance, choosing variants that may potentially be traps for the player. Therefore, it may happen that AI repeats the same moves - this means such state/states do not allow AI to force the win. AI may also easily allow the player to remove first pawn - however, the second pawn may be much harder to remove :)

To get the details of the calculation, have a look at files: blackhole_helper.py, blackhole_generation.py, blackhole_iteration.py.

To play with (as seems to be :)) unbeatable AI, follow the steps:

1) Download all images that names start with 'cell'.
2) Download and unzip blackhole_scores.csv file.
3) Place images and blackhole_scores.csv file in some folder ('D://' in my case), update folder variable in blackhole_gui.py file.
4) Make sure tkinter library is imported. I was using version 8.6.
5) Run the script blackhole_gui.py. Around 1-2 minutes are needed to get scores from the csv file.
6) Enjoy ;)
