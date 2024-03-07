import numpy as np
import sudokutester as st
import sidefunc as sf
from sidefunc import alphabet, rev_alphabet
import time

class SolvingGrid():
	def __init__(self, grid=np.array([]), solving_grid=None):
		if solving_grid != None:
			self.grid = np.array([[c for c in row] for row in solving_grid.grid])
			self.placed_nums_row = np.array([sf.copy_set(c) for c in solving_grid.placed_nums_row])
			self.placed_nums_columns = np.array([sf.copy_set(c) for c in solving_grid.placed_nums_columns])
			self.placed_nums_cells = np.array([sf.copy_set(c) for c in solving_grid.placed_nums_cells])
		else:
			self.grid = np.array([[c for c in row] for row in grid])
			self.generate_available_nums()
	def generate_available_nums(self):
		placed_nums_row = [set() for _ in self.grid]
		placed_nums_columns = [set() for _ in self.grid]
		placed_nums_cells = [set() for _ in self.grid]
		sqrt_size = int(np.sqrt(len(self.grid)))
		for y, row in enumerate(self.grid):
			for x, c in enumerate(row):
				placed_nums_row[y].add(c)
				placed_nums_columns[x].add(c)
				cell_idx = sqrt_size * (y//sqrt_size) + (x // sqrt_size)
				placed_nums_cells[cell_idx].add(c)
		self.placed_nums_row = placed_nums_row
		self.placed_nums_columns = placed_nums_columns
		self.placed_nums_cells = placed_nums_cells
	def insert_number(self, pos, c):
		y, x = pos
		self.grid[pos] = c
		self.placed_nums_row[y].add(c)
		self.placed_nums_columns[x].add(c)
		sqrt_size = int(np.sqrt(len(self.grid)))
		cell_idx = sqrt_size * (y//sqrt_size) + (x // sqrt_size)
		self.placed_nums_cells[cell_idx].add(c)
	def get_available_nums(self, pos):
		y, x = pos
		sqrt_size = int(np.sqrt(len(self.grid)))
		cell_idx = sqrt_size * (y//sqrt_size) + (x // sqrt_size)
		available_nums = []
		for possible_num in [alphabet[x] for x in range(len(self.grid))]:
			if not possible_num in self.placed_nums_row[y] and not possible_num in self.placed_nums_columns[x] and not possible_num in self.placed_nums_cells[cell_idx]:
				available_nums.append(possible_num)
		return np.array(available_nums)

def solve_sudoku(grid, seed=0):
	if seed != 0:
		grid = sf.from_seed(len(grid), seed)
	elif not st.is_partially_valid(grid):
		return np.array([]), np.array([])
	animated_solution = []
	start_time = time.perf_counter()
	solving_grid = SolvingGrid(grid=grid)
	solved_grid = backtrack(solving_grid, animated_solution)
	end_time = time.perf_counter()
	print(end_time-start_time)
	return solved_grid, np.array(animated_solution)

def backtrack(solving_grid, animated_solution):
	if st.is_valid(solving_grid.grid):
		return solving_grid.grid
	else:
		first_empty_index = -1
		for y, row in enumerate(solving_grid.grid):
			for x, c in enumerate(row):
				if c == '':
					first_empty_index = (y,x)
					break
			if first_empty_index != -1:
				break
		if first_empty_index == -1:
			return np.array([])
		for x in solving_grid.get_available_nums(first_empty_index):
			p_solving_grid = SolvingGrid(solving_grid=solving_grid)
			p_solving_grid.insert_number(first_empty_index, x)
			animated_solution.append(x)
			rec_grid = backtrack(p_solving_grid, animated_solution)
			if len(rec_grid) > 0:
				return rec_grid
			else:
				animated_solution.append('<')
		return np.array([])