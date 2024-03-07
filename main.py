import numpy as np
import pygame as pg
import sudokutester as st
import sudokusolver as solver
import sidefunc as sf
from sidefunc import alphabet

class Grid():
	def __init__(self, size, seed=-1):
		self.size = size
		self.grid_values = np.array([['' for _ in range(self.size**2)] for _ in range(self.size**2)])
		self.grid_values_fixes = np.array([[False for _ in range(self.size**2)] for _ in range(self.size**2)])
		self.n_grid_values_fixes = 0
		if seed != -1:
			self.seed = seed
			self.request_solution() #solution = solver.solve_sudoku(sf.from_seed(self.size**2, self.seed))
		else:
			self.seed = -1
			self.solution = np.array([])
			self.animated_solution = np.array([])
	def get_fixed_grid(self):
		return np.array([[v if self.grid_values_fixes[y,x] else '' for x, v in enumerate(row)] for y, row in enumerate(self.grid_values)])
	def set_fixed_grid(self):
		self.seed = -1
		self.solution = np.array([])
		self.animated_solution = np.array([])
		for ri, row in enumerate(self.grid_values):
			for ci, c in enumerate(row):
				if c != '':
					self.grid_values_fixes[ri,ci] = True
				else:
					self.grid_values_fixes[ri,ci] = False
	def request_solution(self, seed=-1, forced=False):
		if len(self.solution) > 0 and not forced:
			return
		elif self.seed == -1 or forced:
			if seed == -1:
				self.solution, self.animated_solution = solver.solve_sudoku(self.get_fixed_grid())
			else:
				self.seed = seed
				self.solution, self.animated_solution = solver.solve_sudoku(sf.from_seed(self.size**2, self.seed))
		else:
			self.solution, self.animated_solution = solver.solve_sudoku(sf.from_seed(self.size**2, self.seed))
	def show_solution(self, visual_infos):
		self.request_solution(forced=True)
		visual_infos.solving_mode = True
		visual_infos.animated_solution = self.animated_solution
		if len(self.solution) > 0:
			self.grid_values = np.copy(self.solution)
	def clear_solution(self):
		self.grid_values = self.get_fixed_grid()
	def generate_puzzle(self, n_visible_numbers=-1):
		if n_visible_numbers < 1:
			n_visible_numbers = sf.get_random_int(self.size**2, int(np.sqrt(self.size)*self.size**3))
		while self.n_grid_values_fixes < n_visible_numbers and n_visible_numbers < self.size**4:
			if self.seed == -1:
				self.seed = sf.get_random_seed(self.size**2)
				self.request_solution()
			if len(self.solution) > 0:
				placed = False
				while not placed:
					random_pos = sf.get_random_pos(self.size**2)
					if not self.grid_values_fixes[random_pos]:
						placed = True
				self.grid_values = self.get_fixed_grid()
				self.grid_values[random_pos] = self.solution[random_pos]
				self.grid_values_fixes[random_pos] = True
				self.n_grid_values_fixes += 1
	def test_for_valid(self):
		return st.is_valid(self.grid_values)
	def get_errors(self):
		self.request_solution()
		errors = []
		for y, row in enumerate(self.grid_values):
			for x, (v, s) in enumerate(zip(row, self.solution[y])):
				if v != s:
					errors.append((y,x))
		return errors

class AlgoInfos():
	def __init__(self, grid_size=3):
		"""
		algorithm variables
		"""
		self.grid = Grid(grid_size)
		self.currently_valid = False

		self.current_seed = -1

class VisualInfos():
	def __init__(self, algo_infos):
		"""
		visualizing variables
		"""
		self.screen_size = (720, 720)
		self.screen_center = (self.screen_size[0]/2, self.screen_size[1]/2)

		self.main_font = pg.font.SysFont('Comic Sans MS', int(400/algo_infos.grid.size**2))

		self.cell_size = (self.screen_size[0]/algo_infos.grid.size**2, self.screen_size[1]/algo_infos.grid.size**2)
		self.center_points = np.array([[(x*self.cell_size[0]+self.cell_size[0]/2, y*self.cell_size[1]+self.cell_size[1]/2) for x in range(algo_infos.grid.size**2)] for y in range(algo_infos.grid.size**2)])
		self.cell_rects = np.array([[pg.Rect((int(cX-self.cell_size[0]/2+1),int(cY-self.cell_size[1]/2+1)), (self.cell_size[0]-1,self.cell_size[1]-1)) for cX, cY in row] for row in self.center_points])
		self.seleced_cell = (0,0)

		self.meta_delay = 0

		self.solving_mode = False
		self.animated_solution = np.array([])
		self.animation_status = 0
		self.animation_speed = 30000

def __main__():
	"""
	initialize pygame + used fonts
	"""
	pg.init()
	pg.font.init()
	
	algo_infos = AlgoInfos(3)
	visual_infos = VisualInfos(algo_infos)
	"""
	base pygame stats
	"""
	main_screen = pg.display.set_mode(visual_infos.screen_size)
	fullscreen = False
	
	"""
	meta variables
	"""
	fps_clock = pg.time.Clock()
	tick_rate = 500
	delta_time = 0

	"""
	runtime variables
	"""
	
	running = True

	def key_input_handling(key_infos, algo_infos, visual_infos):
		test_for_valid = False
		if not visual_infos.solving_mode:
			if algo_infos.currently_valid:
				if key_infos[pg.K_RETURN]:
					algo_infos.currently_valid = None
			elif key_infos[pg.K_RETURN]:
				test_for_valid = True
			else:
				if visual_infos.seleced_cell != None and not algo_infos.grid.grid_values_fixes[visual_infos.seleced_cell]:
					if key_infos[pg.K_BACKSPACE]:
						algo_infos.grid.grid_values[visual_infos.seleced_cell] = ''
					else:
						pressed_idx = key_infos.index(1)+5
						if pressed_idx >= 35 and pressed_idx < 45:
							pressed_idx -= 35
						if pressed_idx < algo_infos.grid.size**2:
							algo_infos.grid.grid_values[visual_infos.seleced_cell] = alphabet[pressed_idx]
				if key_infos[pg.K_RIGHT]:
					algo_infos.grid = Grid(algo_infos.grid.size)
					algo_infos.grid.generate_puzzle()
					visual_infos.meta_delay = pg.time.get_ticks() + 200
				elif key_infos[pg.K_SPACE]:
					algo_infos.grid.set_fixed_grid()
				elif key_infos[pg.K_DELETE]:
					algo_infos.grid = Grid(algo_infos.grid.size)
				elif key_infos[pg.K_UP]:
					algo_infos.grid.show_solution(visual_infos)
					visual_infos.meta_delay = pg.time.get_ticks() + 200
				elif key_infos[pg.K_DOWN]:
					algo_infos.grid.clear_solution()
		if test_for_valid:
			if algo_infos.grid.test_for_valid():
				algo_infos.currently_valid = pg.Color(0,120,0)
			else:
				algo_infos.currently_valid = pg.Color(120,0,0)

	def mouse_input_handling(mouse_infos, algo_infos, visual_infos):
		if mouse_infos[0]:
			"""
			check for left-button presses
			"""
			for y, row in enumerate(visual_infos.cell_rects):
				for x, cell in enumerate(row):
					if pg.Rect(cell).collidepoint(pg.mouse.get_pos()):
						visual_infos.seleced_cell = (y,x)

	def animate_solution(visual_infos, algo_infos):
		for ri, row in enumerate(algo_infos.grid.grid_values_fixes):
			for ci, ((x, y), v) in enumerate(zip(visual_infos.center_points[ri], row)):
				if v:
					text_surface = visual_infos.main_font.render(algo_infos.grid.grid_values[ri,ci], False, "white")
					text_rect = text_surface.get_rect(center=(x, y))
					main_screen.blit(text_surface, text_rect)

		animation_percent = visual_infos.animation_status/visual_infos.animation_speed

		n = int((len(visual_infos.animated_solution))*animation_percent)
		nums_to_place = sf.get_partial_solution(visual_infos.animated_solution[:n])
		i = 0
		orange_mode = False
		for ri, row in enumerate(algo_infos.grid.grid_values_fixes):
			for ci, ((x, y), v) in enumerate(zip(visual_infos.center_points[ri], row)):
				if i == len(nums_to_place):
					break
				if not v:
					if i == len(nums_to_place)-1 and len(visual_infos.animated_solution) > n and visual_infos.animated_solution[n] == '<':
						text_surface = visual_infos.main_font.render(nums_to_place[i], False, "red")
					elif orange_mode or algo_infos.grid.solution[ri,ci] != nums_to_place[i]:
						text_surface = visual_infos.main_font.render(nums_to_place[i], False, "orange")
						orange_mode = True
					else:
						text_surface = visual_infos.main_font.render(nums_to_place[i], False, "green")
					text_rect = text_surface.get_rect(center=(x, y))
					main_screen.blit(text_surface, text_rect)
					i += 1

	def draw_grid(main_screen, algo_infos, visual_infos):
		#fill background
		main_screen.fill("black")
		#draw grid-lines
		inner_grid_size = algo_infos.grid.size**2
		for x in range(1, inner_grid_size):
			if x % algo_infos.grid.size == 0:
				color = "green"
				thickness = 3
			else:
				color = "white"
				thickness = 1
			pg.draw.line(main_screen, color, (x*visual_infos.screen_size[0]/inner_grid_size, 0), (x*visual_infos.screen_size[0]/inner_grid_size, visual_infos.screen_size[1]), thickness)
			pg.draw.line(main_screen, color, (0, x*visual_infos.screen_size[1]/inner_grid_size), (visual_infos.screen_size[0], x*visual_infos.screen_size[1]/inner_grid_size), thickness)
		if not visual_infos.solving_mode:
			if algo_infos.currently_valid:
				for y, row in enumerate(visual_infos.cell_rects):
					for x, cell in enumerate(row):
						pg.draw.rect(main_screen, algo_infos.currently_valid, visual_infos.cell_rects[y,x])
			else:
				#color selected-cell
				if visual_infos.seleced_cell != None:
					if algo_infos.grid.grid_values[visual_infos.seleced_cell] != '':
						for y, row in enumerate(visual_infos.cell_rects):
							for x, cell in enumerate(row):
								if algo_infos.grid.grid_values[y,x] == algo_infos.grid.grid_values[visual_infos.seleced_cell]:
									pg.draw.rect(main_screen, pg.Color(120, 70, 0), cell)
					pg.draw.rect(main_screen, pg.Color(120, 0, 0), visual_infos.cell_rects[visual_infos.seleced_cell])


			#draw cell-values
			for ri, row in enumerate(algo_infos.grid.grid_values):
				for ci, ((x, y), v) in enumerate(zip(visual_infos.center_points[ri], row)):
					if v != '':
						if algo_infos.grid.grid_values_fixes[ri,ci]:
							text_surface = visual_infos.main_font.render(v, False, "white")
						elif len(algo_infos.grid.solution) > 0 and algo_infos.grid.solution[ri,ci] == v:
							text_surface = visual_infos.main_font.render(v, False, "green")
						else:
							text_surface = visual_infos.main_font.render(v, False, "orange")
						text_rect = text_surface.get_rect(center=(x, y))
						main_screen.blit(text_surface, text_rect)

	while running:
		"""
		key-input handling
		"""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			elif event.type == pg.KEYDOWN and pg.time.get_ticks() > visual_infos.meta_delay:
				key_input_handling(pg.key.get_pressed(), algo_infos, visual_infos)

		"""
		mouse handling
		"""
		if any(pg.mouse.get_pressed(num_buttons=3)):
			mouse_input_handling(pg.mouse.get_pressed(num_buttons=3), algo_infos, visual_infos)
			
		"""
		initialize screen
		"""
		draw_grid(main_screen, algo_infos, visual_infos)
		if visual_infos.solving_mode:
			if len(visual_infos.animated_solution) > 0:
				animate_solution(visual_infos, algo_infos)
				if visual_infos.animation_status >= visual_infos.animation_speed:
					visual_infos.animation_status = 0
					visual_infos.solving_mode = False
				visual_infos.animation_status += delta_time * 1000
			else:
				visual_infos.solving_mode = False
			
		"""
		update pygame-display and meta-stats
		"""
		pg.display.flip()
		delta_time = fps_clock.tick(tick_rate) / 1000

__main__() #start programm