import pygame
import random
import math
from classes import Tetrimino as t
from classes.resources import Palette as colors

pygame.init()

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600
GRID_RIGHT = 550
GRID_THICKNESS = 3
FPS = 30

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
		tetrimino.y -= t.Tetrimino.block_size

	elif action_flag == 3:
		tetrimino.x += t.Tetrimino.block_size

	elif action_flag == 4:
		tetrimino.x -= t.Tetrimino.block_size

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
	tetrimino.y += t.Tetrimino.block_size

	return 2

def move_tetrimino_left(tetrimino, tetriminoes, grid_area):
	# move movable tetrimino block one step left
	tetrimino.x -= t.Tetrimino.block_size
	
	return 3

def move_tetrimino_right(tetrimino, tetriminoes, grid_area):
	# move movable tetrimino block one step right
	tetrimino.x += t.Tetrimino.block_size

	return 4

def game_loop():
	# dictionary containing mappings from rects to their colors. EX: {rect(...): colors.GREEN, ...}
	tetriminoes = {}
	# rectangle containing tetrimino blocks
	grid_area = draw_grid_area()
	running = True
	game_over = False
	movable_tetrimino = t.Tetrimino(350, DISPLAY_HEIGHT/2)
	action_flag = 0

	while running:
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

			# check for typing a letter
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




		# check if tetris block has hit bottom of grid_area
		hit_bottom = False
		for rect in movable_tetrimino.rects:
			rect_y = rect[1]
			if rect_y >= DISPLAY_HEIGHT - t.Tetrimino.block_size:
				
				hit_bottom = True 
				break

		# TODO: check if tetris block has hit top of placed tetriminos and needs to stop moving

		if hit_bottom:
			# add current movable tetrimino block's rects to set of placed tetrimino rects 
			for rect in movable_tetrimino.rects:
				tetriminoes[rect] = movable_tetrimino.color

			# create new tetris block to move
			movable_tetrimino = t.Tetrimino(350, DISPLAY_HEIGHT/2)

		#Update
		#for tetrimino in tetriminoes:
			#tetrimino.update()

		#Draw/Render
		game_display.fill(colors.BLACK)
		display_score()
		draw_grid_area()
		draw_tetriminoes(movable_tetrimino, tetriminoes)

		pygame.display.update()
		# use dt to speed up tetrimino blocks later
		dt = clock.tick(FPS)

display_start_menu()
game_loop()

pygame.quit()