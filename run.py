import pygame
import conway
from PIL import Image
import numpy as np
from os import listdir
from random import randint

MARINE = (1, 25, 93)
DARK_MARINE = (1, 20, 88)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOX_SIZE = 10
X_QUANTITY = 100
Y_QUANTITY = 70
SCREEN_SIZE_X = X_QUANTITY * BOX_SIZE
SCREEN_SIZE_Y = Y_QUANTITY * BOX_SIZE
SIDE_PANNEL_WIDTH = 100
FONT_SIZE = 25

def main():
	def next_frame():
		window.fill(MARINE)
		color = (BLACK, WHITE)
		

		g = int(not generating) - int(box_offset == 1 and not generating)
		pygame.draw.rect(window, BLACK, (SCREEN_SIZE_X, 0, SIDE_PANNEL_WIDTH + 1, SCREEN_SIZE_Y))
		for i, p in enumerate(patterns): 
			window.blit(p, (SCREEN_SIZE_X, i * FONT_SIZE))

		for cell in conway.currently_alive:
			x, y = cell
			if x - offset_x >= (SCREEN_SIZE_X // box_offset) or x - offset_x < 0: continue
			if y - offset_y >= SCREEN_SIZE_Y // box_offset or y - offset_y < 0: continue
			
			rectangle = ((x - offset_x) * box_offset + g, (y - offset_y) * box_offset + g, box_offset - g, box_offset - g)
			pygame.draw.rect(window, WHITE, rectangle)

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

	def load_image(name):
		im = Image.open('patterns/{}'.format(name))
		cells = np.array(im)
		conway.currently_alive = set()
		for y in range(cells.shape[0]):
			for x in range(cells.shape[1]):
				if cells[y][x] == 1: conway.currently_alive.add((x, y))
		offset_x = -X_QUANTITY // 2 + cells.shape[1] // 2 + 1
		offset_y = -Y_QUANTITY // 2 + cells.shape[0] // 2 + 1
		return offset_x, offset_y

	#pygame.display.set_icon #TODO
	offset_x = 0
	offset_y = 0
	box_offset = BOX_SIZE
	mouse_position = (0, 0)
	prev_coor = coor = (0, 0)
	generating = False
	time_point = 0
	set_speed = 30

	#TESTING
	# generating = True
	# cells, offset_x, offset_y = load_image('explosion.bmp')

	pygame.font.init()
	font = pygame.font.SysFont('Arial', FONT_SIZE)
	bitmap_names = listdir('patterns')
	patterns = [font.render(' ' + p[:-4].upper(), True, WHITE) for p in bitmap_names]


	clock = pygame.time.Clock()

	window = pygame.display.set_mode((SCREEN_SIZE_X + SIDE_PANNEL_WIDTH, SCREEN_SIZE_Y))

	active = True
	while True:
		#if generating: time_point += clock.tick(120)
		#else: clock.tick(120)

		pygame.event.pump()
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
					conway.get_generation()

				elif event.key == pygame.K_ESCAPE:
					offset_y = offset_x = 0
					generating = False
					conway.currently_alive = set()
					time_point = 0
					set_speed = 30
					bitmap_names = listdir('patterns')
					patterns = [font.render(' ' + p[:-4].upper(), True, WHITE) for p in bitmap_names]

				elif event.key == pygame.K_MINUS:
					set_speed += 30
					time_point = min(time_point, set_speed)
				elif event.key == pygame.K_EQUALS:
					set_speed = max(0, set_speed - 30)
					time_point -= 30

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and mouse_position[0] > SCREEN_SIZE_X:
					try:
						offset_x, offset_y = load_image(bitmap_names[mouse_position[1] // FONT_SIZE])
						generating = False
						time_point = 0
					except Exception as e: print(e)

				a = 0
				if event.button == 4:
					box_offset += 1
					#offset_x = (SCREEN_SIZE_X / box_offset) * offset_x // (SCREEN_SIZE_X // (box_offset - 1))
					#offset_y = (SCREEN_SIZE_Y / box_offset) * offset_y // (SCREEN_SIZE_Y // (box_offset - 1))
				elif event.button == 5:
					box_offset = max(box_offset - 1, 1)
					#offset_x = (SCREEN_SIZE_X // box_offset) * offset_x // (SCREEN_SIZE_X // (box_offset + 1))
					#offset_y = (SCREEN_SIZE_Y // box_offset) * offset_y // (SCREEN_SIZE_Y // (box_offset + 1))
				


		if pygame.mouse.get_pressed()[0] :
			if mouse_position[0] > SCREEN_SIZE_X:
				continue

			if coor[1] < -offset_x + 1:
				dist = -(coor[1] + offset_x) + 1
				conway.currently_alive = {(cell[0] + dist, cell[1]) for cell in conway.currently_alive}
				offset_x += dist
			elif coor[0] < -offset_y + 1:
				dist = -(coor[0] + offset_y) + 1
				conway.currently_alive = {(cell[0], cell[1] + dist) for cell in conway.currently_alive}
				offset_y += dist


			for c in get_points(prev_coor, coor):
				try:
					conway.currently_alive.add(c[::-1])
				except: pass
			prev_coor = coor

		elif pygame.mouse.get_pressed()[2]:
			for c in get_points(prev_coor, coor):
				try:
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
		if generating:# and time_point > set_speed:
			#time_point -= set_speed
			conway.get_generation()

			
		pygame.display.set_caption('{} {} {}'.format(coor, offset_x, offset_y))



if __name__ == '__main__': main()