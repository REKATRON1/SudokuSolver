import numpy as np

def is_valid(grid):
	grid_size = int(np.sqrt(len(grid)))
	seen_horizontal = [set(v for v in row if v != '') for row in grid]
	seen_vertical = [set(row[x] for row in grid if row[x] != '') for x in range(len(grid))]
	if sum([len(x) for x in seen_horizontal]) == len(grid)**2 and sum([len(x) for x in seen_vertical]) == len(grid)**2:
		boxes = np.array([[set() for _ in range(grid_size)] for _ in range(grid_size)])
		for y, row in enumerate(grid):
			for x, cell in enumerate(row):
				idx = int(y/grid_size), int(x/grid_size)
				if cell in boxes[idx]:
					return False
				else:
					boxes[idx].add(cell)
		return True
	return False

def is_partially_valid(grid):
	placed_points = sum([sum([1 for v in row if v != '']) for row in grid])
	seen_horizontal = [set(v for v in row if v != '') for row in grid]
	seen_vertical = [set(row[x] for row in grid if row[x] != '') for x in range(len(grid))]
	if sum([len(x) for x in seen_horizontal]) == placed_points and sum([len(x) for x in seen_vertical]) == placed_points:
		grid_size = int(np.sqrt(len(grid)))
		boxes = np.array([[set() for _ in range(grid_size)] for _ in range(grid_size)])
		for y, row in enumerate(grid):
			for x, cell in enumerate(row):
				idx = int(y/grid_size), int(x/grid_size)
				if cell != '' and cell in boxes[idx]:
					return False
				else:
					boxes[idx].add(cell)
		return True
	return False