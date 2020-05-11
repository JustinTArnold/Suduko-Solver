

from pynput.keyboard import Key, Controller
keyboard = Controller()
import time
import pyperclip
puzzle_old = []
print ("you have 2 second to click into the puzzle")
time.sleep(2)
for _ in range(80):
		keyboard.press('0')
		keyboard.release('0')
		keyboard.press(Key.tab)
		keyboard.release(Key.tab)
keyboard.press('0')
keyboard.release('0')
keyboard.press(Key.right)
keyboard.release(Key.right)
keyboard.press(Key.down)
keyboard.release(Key.down)
time.sleep(2)
for _ in range(80):
	keyboard.press(Key.ctrl)
	keyboard.press('a')
	keyboard.release('a')
	keyboard.release(Key.ctrl)
	keyboard.press(Key.ctrl)
	keyboard.press('c')
	keyboard.release('c')
	keyboard.release(Key.ctrl)
	time.sleep(.05)
	letter = int(pyperclip.paste())
	puzzle_old.append(letter)
	keyboard.press(Key.tab)
	keyboard.release(Key.tab)
keyboard.press(Key.ctrl)
keyboard.press('a')
keyboard.release('a')
keyboard.release(Key.ctrl)
keyboard.press(Key.ctrl)
keyboard.press('c')
keyboard.release('c')
keyboard.release(Key.ctrl)
time.sleep(.1)
letter = int(pyperclip.paste())
puzzle_old.append(letter)
puzzle_new = [[int(c) for c in puzzle_old[n:n+9]] for n in (0,9,18,27,36,45,54,63,72)]



    
def zeros_in(puzzle):
    total = 0
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                total += 1
    return total

def possible_in_cell(puzzle, a, b):
    vals = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for i in range(9):
        vals -= {puzzle[i][b]}
        vals -= {puzzle[a][i]}
    i, j = (a // 3) * 3, (b // 3) * 3
    for a in range(i, i + 3):
        for b in range(j, j + 3):
            vals -= {puzzle[a][b]}
    return tuple(vals)
    
def possibilities(puzzle):
    possibles = [[0] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] > 0:
                possibles[i][j] = None
            else:
                possibles[i][j] = possible_in_cell(puzzle, i, j)
    return possibles


from pprint import pprint
from itertools import product
from copy import deepcopy


def sudoku_solver(puzzle):
    def next_free_cell(puzzle):
        for i, j in product(range(9), repeat=2):
            if puzzle[i][j] == 0:
                return i, j
        return False, False
    
    def possibilities(puzzle, a, b):
        vals = [0,1,2,3,4,5,6,7,8,9]
        for i in range(9):
            vals[puzzle[i][b]], vals[puzzle[a][i]] = 0, 0
        a, b = (a // 3) * 3, (b // 3) * 3
        for i in range(a, a + 3):
            for j in range(b, b + 3):
                vals[puzzle[i][j]] = 0
        return [n for n in vals if n]

    
    def fill_squares(puzzle):
        while True:
            found = False
            for i, j in product(range(9), repeat=2):
                if puzzle[i][j] != 0:
                    continue
                possible = possibilities(puzzle, i, j)
                if len(possible) == 1:
                    puzzle[i][j] = possible.pop()
                    found = True
            if not found:
                break
    
    i, j = next_free_cell(puzzle)
    if i is False:
        return puzzle
    for n in possibilities(puzzle, i, j):
        new_state = deepcopy(puzzle)
        new_state[i][j] = n
        fill_squares(new_state)
        result = sudoku_solver(new_state)
        if result:
            return result
    return False


def valid_solution(initial, result):
    for i, j in product(range(9), repeat=2):
        if initial[i][j] != 0 and initial[i][j] != result[i][j]:
            print(f'bad match at cell {i}, {j}')
            return False
    
    complete = {*range(1, 10)}
    for n in range(9):
        if {result[n][i] for i in range(9)} != complete:
            print(f'bad row #{n+1}')
            return False
        if {result[i][n] for i in range(9)} != complete:
            print(f'bad column #{n+1}')
            return False
        square = set()
        x = (n // 3) * 3
        for i in range(x, x + 3):
            for j in range(x, x + 3):
                square.add(result[i][j])
        if square != complete:
            print(f'bad square #{n+1}')
            return False
    return True
        

def timer(f, n, runs=5, average=False, output=False):
    import time
    total, res = 0, []
    for _ in range(runs):
        start = time.time()
        input_copy = deepcopy(n)
        res.append(f(input_copy))
        total += time.time() - start
    if average:
        total /= runs
    if output:
        return total, res
    return total

use_puzzle = puzzle_new

secs, outputs = timer(sudoku_solver, use_puzzle, output=True)
if all(result and valid_solution(use_puzzle, result) for result in outputs):
    print(f"I took {secs} seconds to solve the puzzle")
else:
    print("I couldn't solve the puzzle")

keyboard.press(Key.right)
keyboard.release(Key.right)
keyboard.press(Key.right)
keyboard.release(Key.right)
keyboard.press(Key.down)
keyboard.release(Key.down)
keyboard.press(Key.ctrl)
keyboard.press('a')
keyboard.release('a')
keyboard.release(Key.ctrl)
for i in sudoku_solver(puzzle_new):
	for x in i:
		keyboard.press(str(x))
		keyboard.release(str(x))
		keyboard.press(Key.tab)
		keyboard.release(Key.tab)