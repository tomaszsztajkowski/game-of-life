import numpy as np


currently_alive = set()
neighbours = np.array([[]])

def get_generation(cells):
	def add_neighbours():
		global neighbours
		for x, y in currently_alive:
			for i in {-1, 0, 1}:
				for j in {-1, 0, 1}:
					neighbours[y + i][x + j] += 1 * (not (i == 0 and j == 0))
					potentially_alive.add((x + i, y + j))

	
	global currently_alive, neighbours

	potentially_alive = set()

	add_neighbours()
	currently_alive = set()

	top = bottom = left = right = False

	for cell in potentially_alive:
		x, y = cell
		if neighbours[y][x] == 3:
			top += y == 0
			bottom += y == (cells.shape[0] - 1)
			left += x == 0
			right += x == (cells.shape[1] - 1)
			currently_alive.add((x, y))
			cells[y][x] = 1
		elif neighbours[y][x] == 2:
			if cells[y][x] == 1: currently_alive.add((x, y))
		else:
			cells[y][x] = 0
		neighbours[y][x] = 0


	if left:
		cells = np.concatenate((np.zeros((cells.shape[0], 1)), cells), axis=1)
		neighbours = np.concatenate((np.zeros((neighbours.shape[0], 1)), neighbours), axis=1)
		currently_alive = {(cell[0] + 1, cell[1]) for cell in currently_alive}
	if right:
		cells = np.concatenate((cells, np.zeros((cells.shape[0], 1))), axis=1)
		neighbours = np.concatenate((neighbours, np.zeros((neighbours.shape[0], 1))), axis=1)
	if top:
		cells = np.concatenate((np.zeros((1, cells.shape[1])), cells))
		neighbours = np.concatenate((np.zeros((1, neighbours.shape[1])), neighbours))
		currently_alive = {(cell[0], cell[1] + 1) for cell in currently_alive}
	if bottom:
		cells = np.concatenate((cells, np.zeros((1, cells.shape[1])) ))
		neighbours = np.concatenate((neighbours, np.zeros((1, neighbours.shape[1])) ))

	return (cells, (top > 0, left > 0))