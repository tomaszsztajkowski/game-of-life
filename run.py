import pygame
import conway
import numpy as np

MARINE = (1, 25, 93)
DARK_MARINE = (1, 20, 88)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOX_SIZE = 10
X_QUANTITY = 100
Y_QUANTITY = 70
SCREEN_SIZE_X = X_QUANTITY * BOX_SIZE
SCREEN_SIZE_Y = Y_QUANTITY * BOX_SIZE

def main():
	def next_frame():
		window.fill(MARINE)
		color = (BLACK, WHITE)
		
		left_x = max(0, offset_x)
		right_x = min(SCREEN_SIZE_X // box_offset + offset_x + 1, cells.shape[0])
		top_y = max(0, offset_y)
		bottom_y = min(SCREEN_SIZE_Y // box_offset + offset_y + 1, cells.shape[1])

		g = not generating

		pygame.draw.rect(window, DARK_MARINE, (-offset_x * box_offset, -offset_y * box_offset, cells.shape[1] * box_offset, cells.shape[0] * box_offset))

		for cell in conway.currently_alive:
			x, y = cell
			display = WHITE #TODO
			rectangle = ((x - offset_x) * box_offset + g, (y - offset_y) * box_offset + g, box_offset - g, box_offset - g)
			pygame.draw.rect(window, display, rectangle)

		pygame.display.update()


	def get_points(c1, c2):
		def lerp(start, end, t):
			return start + t * (end-start)
		def lerp_point(p1, p2, t):
			return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))
		def round_point(p):
			return (round(p[0]), round(p[1]))
		
		if not c1 or c1 == c2:
			p = (c2[0] + offset_y, c2[1] + offset_x)
			return [p] if p[0] >= 0 and p[1] >= 0 else []
		c1 = (c1[0] + offset_y, c1[1] + offset_x)
		c2 = (c2[0] + offset_y, c2[1] + offset_x)
		points = []
		diagonal_distance = max((abs(c1[0] - c2[0]), abs(c1[1] - c2[1])))

		for i in range(diagonal_distance):
			t = 0 if diagonal_distance == 0 else i / diagonal_distance
			points.append(round_point(lerp_point(c1, c2, t)))

		return [p for p in points if p[0] >= 0 and p[1] >= 0]

	#pygame.display.set_icon #TODO
	cells = np.zeros((Y_QUANTITY, X_QUANTITY))
	offset_x = 0
	offset_y = 0
	box_offset = BOX_SIZE
	mouse_position = (0, 0)
	prev_coor = coor = (0, 0)
	generating = False
	time_point = 0
	set_speed = 40

	conway.get_generation(np.array([]))

	clock = pygame.time.Clock()

	window = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))

	active = True
	while active:
		if generating: time_point += clock.tick(120)
		else: clock.tick(120)

		for event in pygame.event.get():

			# quit
			if event.type == pygame.QUIT:
				return

			elif event.type == pygame.MOUSEMOTION:
				mouse_position = pygame.mouse.get_pos()
				coor = (mouse_position[1] // box_offset, mouse_position[0] // box_offset)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					generating = not generating

				elif event.key == pygame.K_RIGHT:
					cells, offset = conway.get_generation(cells)
					offset_y += offset[0]
					offset_x += offset[1]

				elif event.key == pygame.K_ESCAPE:
					cells = np.zeros((Y_QUANTITY, X_QUANTITY))
					offset_y = offset_x = 0
					generating = False
					conway.currently_alive = set()
					time_point = 0

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4: box_offset += 1
				elif event.button == 5: box_offset -= 1
				box_offset = max(box_offset, 2)


		if pygame.mouse.get_pressed()[0] :
			if coor[1] >= cells.shape[1] - offset_x - 1:
				cells = np.concatenate((cells, np.zeros((cells.shape[0], coor[1] - cells.shape[1] + offset_x + 1 + 1))), axis=1)
			if coor[1] < -offset_x + 1:
				dist = -(coor[1] + offset_x) + 1
				cells = np.concatenate((np.zeros((cells.shape[0], dist)), cells), axis=1)
				conway.currently_alive = {(cell[0] + dist, cell[1]) for cell in conway.currently_alive}
				offset_x += dist
			if coor[0] >= cells.shape[0] - offset_y - 1:
				cells = np.concatenate((cells, np.zeros((coor[0] - cells.shape[0] + offset_y + 1 + 1, cells.shape[1])) ))
			if coor[0] < -offset_y + 1:
				dist = -(coor[0] + offset_y) + 1
				cells = np.concatenate((np.zeros((dist, cells.shape[1])), cells))
				conway.currently_alive = {(cell[0], cell[1] + dist) for cell in conway.currently_alive}
				offset_y += dist


			for c in get_points(prev_coor, coor):
				try:
					cells[c[0]][c[1]] = 1
					conway.currently_alive.add(c[::-1])
				except: pass
			prev_coor = coor

		elif pygame.mouse.get_pressed()[2]:
			for c in get_points(prev_coor, coor):
				try:
					cells[c[0]][c[1]] = 0
					conway.currently_alive.remove(c[::-1])
				except: pass
			prev_coor = coor

		elif pygame.mouse.get_pressed()[1]:
			if not prev_mouse_position:
				prev_mouse_position = pygame.mouse.get_pos()
				mouse_y = mouse_x = 0
			elif prev_mouse_position == mouse_position: pass
			else:
				mouse_y += prev_mouse_position[1] - mouse_position[1]
				mouse_x += mouse_position[0] - prev_mouse_position[0]
				while mouse_y <= -box_offset:
					mouse_y += box_offset
					offset_y -= 1
				while mouse_y >= box_offset:
					mouse_y -= box_offset
					offset_y += 1
				while mouse_x <= -box_offset:
					mouse_x += box_offset
					offset_x += 1
				while mouse_x >= box_offset:
					mouse_x -= box_offset
					offset_x -= 1
				prev_mouse_position = mouse_position

		else:
			prev_coor = None
			prev_mouse_position = None



		next_frame()
		if generating and time_point > set_speed:
			time_point -= set_speed
			cells, offset = conway.get_generation(cells)
			offset_y += offset[0]
			offset_x += offset[1]
			
		pygame.display.set_caption('{} {} {}'.format(coor, offset_x, offset_y))



if __name__ == '__main__': main()