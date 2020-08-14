import pygame
import random
import math
from classes import Tetrimino as t
from classes.resources import Palette as colors

pygame.init()
pygame.key.set_repeat(10, 100)

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600
GRID_RIGHT = 300
GRID_THICKNESS = 3
FPS = 30
BLOCK_SIZE = t.Tetrimino.block_size
MAX_BLOCKS_PER_ROW = GRID_RIGHT/BLOCK_SIZE

FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_FONT = pygame.font.Font(None, 28)
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
score = 0
score_text = SCORE_FONT.render(str(score), True, colors.WHITE, colors.BLACK)
score_rect = score_text.get_rect()

# functions
def draw_grid_area():
	return pygame.draw.rect(game_display, colors.WHITE, (0, 0, GRID_RIGHT, DISPLAY_HEIGHT), GRID_THICKNESS)

def draw_grid():
	for x in range(BLOCK_SIZE, GRID_RIGHT, BLOCK_SIZE):
		pygame.draw.line(game_display, colors.BLACK, (x, 0), (x, DISPLAY_HEIGHT), 1)

	for y in range(BLOCK_SIZE, DISPLAY_HEIGHT, BLOCK_SIZE):
		pygame.draw.line(game_display, colors.BLACK, (0, y), (GRID_RIGHT, y), 1)



def display_score():
	font_color = colors.WHITE

	if score < 0:
		font_color = COLORS.RED

	score_text = SCORE_FONT.render("Score: " + str(score), True, font_color, colors.BLACK)
	score_rect = score_text.get_rect()
	score_rect.x = 930
	score_rect.y = 10
	game_display.blit(score_text, score_rect)

def display_start_menu():
	MENU_FONT = pygame.font.Font("freesansbold.ttf", 28)
	TILE_TEXT_FONT = pygame.font.Font('freesansbold.ttf', 70)
	title_text = TILE_TEXT_FONT.render("Tetris", True, colors.WHITE, colors.BLACK)
	title_text_rect = title_text.get_rect()
	title_text_rect.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/4))
	menu = True

	while menu:
		# check for exiting game early
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		game_display.fill(colors.BLACK)
		game_display.blit(title_text, title_text_rect)

		# get mouse x and y
		mouse_x = pygame.mouse.get_pos()[0]
		mouse_y = pygame.mouse.get_pos()[1]

		# get left mouse clicked val
		clicked = pygame.mouse.get_pressed()[0]

		# easy mode button settings
		easy_button_length = 100
		easy_button_width = 30
		easy_button_x = DISPLAY_WIDTH/2 - easy_button_length/2
		easy_button_y = DISPLAY_HEIGHT/2

		# button container panel settings
		button_container_length = 200
		button_container_width = 6*easy_button_width
		button_container_x = DISPLAY_WIDTH/2 - button_container_length/2
		button_container_y = DISPLAY_HEIGHT/2 - easy_button_width

		# draw button container
		pygame.draw.rect(game_display, colors.BLUE, (button_container_x, button_container_y, button_container_length, button_container_width))

		# easy button highlighting functionality
		if easy_button_x + easy_button_length > mouse_x > easy_button_x and easy_button_y + easy_button_width > mouse_y > easy_button_y:
			pygame.draw.rect(game_display, colors.GREEN, (easy_button_x, easy_button_y, easy_button_length, easy_button_width))
			if clicked:
				return

		else:
			pygame.draw.rect(game_display, colors.DARK_GREEN, (easy_button_x, easy_button_y, easy_button_length, easy_button_width))
		
		# button texts
		easy_text = MENU_FONT.render("Start", True, colors.BLACK)
		easy_text_rect = easy_text.get_rect()
		easy_text_rect.x = easy_button_x + easy_button_length/5
		easy_text_rect.y = easy_button_y

		game_display.blit(easy_text, easy_text_rect)

		pygame.display.update()
		clock.tick(15)


def pause():
	PAUSE_FONT = pygame.font.Font("freesansbold.ttf", 35)
	pause_text = PAUSE_FONT.render("Paused", True, colors.WHITE, colors.BLACK)
	pause_rect = pause_text.get_rect()
	pause_rect.center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
	paused = True

	game_display.blit(pause_text, pause_rect)
	pygame.display.update()


	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return True

		clock.tick(5)

# checks for collisions between the movable tetrimino and the other tetriminoes' rects that have been placed
# and/or the bottom of the grid area. Returns True if a collision has occurred, else False when no collision has occurred
def check_for_collisions(tetrimino, tetriminoes, grid_area):
	for rect in tetrimino.rects:
		# check if block has moved outside of grid area
		if not grid_area.contains(rect):
			return True

		# check if block is colliding with any placed tetrimino blocks
		else:
			for rect_tuple in tetriminoes:
				rect_object = pygame.Rect(rect_tuple)

				if rect_object.contains(rect):
					return True
	
	return False

# draw all current tetriminoes' rects and movable tetrimino on game screen
def draw_tetriminoes(tetrimino, tetriminoes):
	for rect in tetrimino.rects:
		game_display.fill(tetrimino.color, rect)

	for placed_tetrimino in tetriminoes:
		color = tetriminoes[placed_tetrimino]
		rect = placed_tetrimino
		game_display.fill(color, rect)

# undo last action indicated by action flag()
def undo_action(action_flag, tetrimino):
	if action_flag == 1:
		if tetrimino.rotation == 0:
			tetrimino.rotation = 270
		else:
			tetrimino.rotation -= 90

	elif action_flag == 2:
		tetrimino.y -= BLOCK_SIZE

	elif action_flag == 3:
		tetrimino.x += BLOCK_SIZE

	elif action_flag == 4:
		tetrimino.x -= BLOCK_SIZE

	else:
		# action_flag is 0, do nothing
		pass

# rotate given tetrimino by 90 degrees and check if result is valid
def rotate_tetrimino(tetrimino, tetriminoes, grid_area):
	tetrimino.rotation += 90
	tetrimino.rotation %= 360

	return 1

def drop_tetrimino(tetrimino, tetriminoes, grid_area):
	# move movable tetrimino block one step downward
	tetrimino.y += BLOCK_SIZE

	return 2

def move_tetrimino_left(tetrimino, tetriminoes, grid_area):
	# move movable tetrimino block one step left
	tetrimino.x -= BLOCK_SIZE
	
	return 3

def move_tetrimino_right(tetrimino, tetriminoes, grid_area):
	# move movable tetrimino block one step right
	tetrimino.x += BLOCK_SIZE

	return 4

def move_down_rows(rows_cleared, tetriminoes):
	# need to move all placed tetrimino rects down
	for i in range(len(rows_cleared)-1, -1, -1):
		row_y = rows_cleared[i]
		# list of rects to be removed per row
		rects = []

		for rect in tetriminoes.keys():
			if rect[1] < row_y:
				rects.append((rect, tetriminoes[rect]))

		for rect in rects: 
			tetriminoes.pop(rect[0])

		for rect in rects:
			tetriminoes[(rect[0][0], rect[0][1] + BLOCK_SIZE, rect[0][2], rect[0][3])] = rect[1]

def check_for_completed_rows_to_clear(tetriminoes):
	# list of rects to remove if a row has been cleared
	rects_to_remove = []
	# y coordinates of rows cleared this step
	rows_cleared = []

	# bottom to top
	for y in range(DISPLAY_HEIGHT, 0, -BLOCK_SIZE):
		for x in range(0, GRID_RIGHT, BLOCK_SIZE):
			for rect in tetriminoes:
				rect_x = rect[0]
				rect_y = rect[1]


				if rect_x == x and rect_y == y:
					rects_to_remove.append(rect)
					break
		
		# check if the row was full
		if len(rects_to_remove) == MAX_BLOCKS_PER_ROW:
			# remove all rects from this row from tetriminoes
			for rect in rects_to_remove:
				tetriminoes.pop(rect)

			# add row y to rows cleared for this step
			rows_cleared.append(y)

		# clear rects_to_remove for next row to check
		rects_to_remove = []

	if len(rows_cleared) > 0:
		move_down_rows(rows_cleared, tetriminoes)

	return len(rows_cleared)

def check_if_tetrimino_should_stop_moving(tetrimino, tetriminoes):
	# check if tetrimino has hit bottom of grid area and needs to stop moving
	for rect in tetrimino.rects:
		rect_y = rect[1]
		
		if rect_y == DISPLAY_HEIGHT - BLOCK_SIZE:	
			return True 

	# check if tetris block has hit top of placed tetriminoes and needs to stop moving
	for m_rect in tetrimino.rects:
		for p_rect in tetriminoes:
			m_rect_x = m_rect[0]
			p_rect_x = p_rect[0]
			m_rect_y = m_rect[1]
			p_rect_y = p_rect[1]

			if m_rect_y == p_rect_y - BLOCK_SIZE and m_rect_x == p_rect_x:
				return True

# generator function to compute current level speeed
def generate_level_speed():
	speed = 200
	while speed >= 100:
		yield speed
		speed -= 50

def game_loop():
	# dictionary containing mappings from rects to their colors. EX: {rect(...): colors.GREEN, ...}
	tetriminoes = {}
	# rectangle containing tetrimino blocks
	grid_area = draw_grid_area()
	running = True
	game_over = False
	movable_tetrimino = t.Tetrimino(GRID_RIGHT/2, BLOCK_SIZE)
	action_flag = 0
	dt = 0
	touch_timer = 0
	num_rows_cleared = 0
	curr_level = 1
	next_level = 1
	level_speeds = generate_level_speed()
	touch_time_limit = 4000


	while running:
		# increase speed when current level reaches the next level
		if curr_level == next_level:
			next_level += 1
			touch_time_limit -= 1000

			if touch_time_limit < 4000:
				touch_time_limit = 4000

			try: 
				down_speed = next(level_speeds) 
			except StopIteration:
				down_speed = 100
		
		print(down_speed)
		print(touch_time_limit)

		if game_over:
			game_over_text = FONT.render("Game Over", True, colors.WHITE, colors.BLACK)
			game_over_rect = game_over_text.get_rect()
			game_over_rect.x = DISPLAY_WIDTH / 2 - (game_over_rect.right - game_over_rect.left) / 2
			game_over_rect.y = DISPLAY_HEIGHT / 2
			game_display.blit(game_over_text, game_over_rect)
			pygame.display.update()

		while game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					game_over = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						running = False
						game_over = False
						
		#Process input (events)
		for event in pygame.event.get():
			#check for closing window
			if event.type == pygame.QUIT:
				running = False

			# check for player input
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					running = pause()
				
				elif event.key == pygame.K_2:
					for tetrimino_rect in tetriminoes:
						print(tetrimino_rect)
				
				elif event.key == pygame.K_UP:
					# rotate movable tetrimino block
					action_flag = rotate_tetrimino(movable_tetrimino, tetriminoes, grid_area)			
				
				elif event.key == pygame.K_DOWN: 
					# move movable tetrimino block down one step
					action_flag = drop_tetrimino(movable_tetrimino, tetriminoes, grid_area)
					
				elif event.key == pygame.K_LEFT:
					# move movable tetrimino block one step to right
					action_flag = move_tetrimino_left(movable_tetrimino, tetriminoes, grid_area)
									
				elif event.key == pygame.K_RIGHT:
					# move movable tetrimino block one step to left
					action_flag = move_tetrimino_right(movable_tetrimino, tetriminoes, grid_area)

			else:
				# no action taken this step
				action_flag = 0
					
		# update movable tetrimino after action
		movable_tetrimino.update()

		if check_for_collisions(movable_tetrimino, tetriminoes, grid_area) == True:
			# if a collision ocurred, undo the last action
			undo_action(action_flag, movable_tetrimino)	
			# update movable tetrimino after undoing action
			movable_tetrimino.update()

		# move movable tetrimino down by one step automatically every second (based on dt)
		if dt >= down_speed:
			drop_tetrimino(movable_tetrimino, tetriminoes, grid_area)
			movable_tetrimino.update()
			if check_for_collisions(movable_tetrimino, tetriminoes, grid_area) == True:
				undo_action(2, movable_tetrimino)
				movable_tetrimino.update()
			dt = 0

		# check if tetris block has hit bottom of grid_area or top of placed tetrimino blocks
		hit_bottom_or_top = check_if_tetrimino_should_stop_moving(movable_tetrimino, tetriminoes)
	
		if hit_bottom_or_top:
			if touch_timer >= touch_time_limit:
				# add current movable tetrimino block's rects to set of placed tetrimino rects 
				for rect in movable_tetrimino.rects:
					tetriminoes[rect] = movable_tetrimino.color

				# create new tetris block to move
				movable_tetrimino = t.Tetrimino(GRID_RIGHT/2, BLOCK_SIZE)
				touch_timer = 0

			else:
				touch_timer += dt

		if hit_bottom_or_top:
			num_rows_cleared += check_for_completed_rows_to_clear(tetriminoes)

		if num_rows_cleared >= 1:
			curr_level += 1
			num_rows_cleared = 0

		#Draw/Render
		game_display.fill(colors.BLACK)
		display_score()
		draw_tetriminoes(movable_tetrimino, tetriminoes)
		draw_grid()
		draw_grid_area()

		pygame.display.update()
		# use dt to speed up tetrimino blocks later
		dt += clock.tick(FPS)


display_start_menu()
game_loop()

pygame.quit()