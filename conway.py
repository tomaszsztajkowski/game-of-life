import numpy as np
from collections import deque


currently_alive = set()

def get_generation():
	def add_neighbours():
		for x, y in currently_alive:
			try: potentially_alive[(x, y)] += 0
			except: potentially_alive[(x, y)] = 0
			for coor in [(x-1, y-1), (x-1, y), (x, y-1), (x+1, y+1), (x+1, y), (x, y+1), (x-1, y+1), (x+1, y-1)]:
				try: potentially_alive[coor] += 1
				except: potentially_alive[coor] = 1
	
	global currently_alive

	potentially_alive = dict()

	add_neighbours()
	next_gen = deque([])

	for cell in potentially_alive:
		if potentially_alive[cell] == 3:
			next_gen.append(cell)
		elif potentially_alive[cell] == 2:
			if cell in currently_alive: next_gen.append((cell))
	currently_alive = set(next_gen)