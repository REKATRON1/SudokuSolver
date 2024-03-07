import random
import numpy as np

alphabet = [f'{x}' for x in range(1,10)]
alphabet.extend([chr(x) for x in range(ord('A'), ord('Z')+1)])
rev_alphabet = {f'{x}':x-1 for x in range(1,10)} | {chr(x+65):x+9 for x in range(0,26)}

def get_random_int(s, e):
	return random.randint(s, e)

def get_random_char(m):
	i = random.randint(0,m-1)
	return alphabet[i]

def get_random_pos(m):
	i, j = random.randint(0,m-1), random.randint(0,m-1)
	return i, j

def faculty(n):
	if n > 1:
		return n*faculty(n-1)
	return 1

def get_random_seed(size):
	return get_random_int(0, faculty(size)-1)

def from_seed(size, seed):
	first_row_picks = []
	for x in range(size-1, 0, -1):
		n = faculty(x)
		first_row_picks.append(int(seed/n))
		seed = seed % n
	available = [alphabet[x] for x in range(size)]
	first_grid_row = []
	while len(first_row_picks) > 0:
		first_grid_row.append(available[first_row_picks[0]])
		available.pop(first_row_picks[0])
		first_row_picks.pop(0)
	first_grid_row.append(available[0])
	grid = [first_grid_row]
	grid.extend([['' for _ in range(size)] for _ in range(size-1)])
	return np.array(grid)

def get_partial_solution(animation_part):
	nums = []
	for x in animation_part:
		if x == '<':
			nums.pop(-1)
		else:
			nums.append(x)
	return nums

def copy_set(o):
	n = set()
	for c in o:
		n.add(c)
	return n