import pygame
import random
import math
from classes import Tetrimino as t
from classes.resources import Palette as colors

pygame.init()

DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 600
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

# draw all current tetriminoes on game screen
def draw_tetriminoes(tetriminoes):
	for tetrimino in tetriminoes:
		tetrimino.draw(game_display)

def game_loop():
	tetriminoes = []
	time_since_last_added_word = 0
	running = True
	game_over = False
	movable_tetrimino = t.Tetrimino(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

	tetriminoes.append(movable_tetrimino)

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
					for tetrimino in tetriminoes:
						print(tetrimino)
				elif event.key == pygame.K_UP:
					movable_tetrimino.rotation += 90
					movable_tetrimino.rotation %= 360
					# rotate movable tetrimino block
				elif event.key == pygame.K_DOWN: 
					movable_tetrimino.y += t.Tetrimino.block_size
					# move movable tetrimino block one step downward
				elif event.key == pygame.K_LEFT:
					movable_tetrimino.x -= t.Tetrimino.block_size
					# move movable tetrimino block one step left
				elif event.key == pygame.K_RIGHT:
					movable_tetrimino.x += t.Tetrimino.block_size
					# move movable tetrimino block one step right

				

		#Update
		#for tetrimino in tetriminoes:
			#tetrimino.update()

		#Draw/Render
		game_display.fill(colors.BLACK)
		display_score()
		draw_tetriminoes(tetriminoes)

		pygame.display.update()
		# use dt to speed up tetrimino blocks later
		dt = clock.tick(FPS)
		time_since_last_added_word += dt

display_start_menu()
game_loop()

pygame.quit()