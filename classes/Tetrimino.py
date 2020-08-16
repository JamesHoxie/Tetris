import random
import pygame
from classes.resources import Palette as colors

# class definition for a tetrimino block
class Tetrimino():
	tetris_shapes = {1: "I", 2: "O", 3: "T", 4: "J", 5: "L", 6: "S", 7: "Z"}
	tetris_shape_colors = {"I": colors.ORANGE, "O": colors.RED, "T": colors.YELLOW, "J": colors.PINK, "L": colors.BLUE, "S": colors.NEW_GREEN, "Z": colors.PURPLE}
	block_size = 25

	def __init__(self, x, y):
		self.active = True
		self.shape = self.tetris_shapes[random.randint(1, 7)]
		self.color = self.tetris_shape_colors[self.shape]
		self.rotation = 0
		# the x and y coordinates to move and rotate the tetrimino around
		self.x = x 
		self.y = y
		# list of the typles that represent pygame.Rects that currently make up this tetrimino
		self.rects = []
		self.update()
		
	def __str__(self):
		return self.shape + " block"

	# public methods
	# check if this tetrimino has been placed or is being moved still
	def been_placed(self):
		return self.active == False

	# updates given tetrimino's rects
	def update(self):
		if self.shape == "I":
			if self.rotation == 0 or self.rotation == 180:
				# horizontal
				# block is		****
				self.rects = [(self.x, self.y, self.block_size, self.block_size), 
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+2*self.block_size, self.y, self.block_size, self.block_size)]
				

			else: # rotation is 90 or 270
				# vertical
				# block is		*
				#           	*
				#           	*
				#           	*
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
						 	  (self.x, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x, self.y+2*self.block_size, self.block_size, self.block_size)]			
				
		
		elif self.shape == "O":
			# drawing O shape does not change no matter rotation amount
			# block is		**
			#          		**
			self.rects = [(self.x, self.y, self.block_size, self.block_size),
						  (self.x, self.y+self.block_size, self.block_size, self.block_size),
						  (self.x+self.block_size, self.y, self.block_size, self.block_size),
						  (self.x+self.block_size, self.y+self.block_size, self.block_size, self.block_size)]

		elif self.shape == "T":
			if self.rotation == 0:
				# block is   	*** 
				#             	 *
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size)]
			
			elif self.rotation == 90:
				# block is    	 *
				#            	**
				#             	 *
				self.rects = [(self.x, self.y, self.block_size, self.block_size), 
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size)]
			
			elif self.rotation == 180:
				# block is    	 *
				#            	***
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size)]            
			
			else: # rotation is 270
				# block is    	 *
				#             	 **
				#             	 *
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size)]
		
		elif self.shape == "J":
			if self.rotation == 90:
				# block is   	* 
				#             	*
				#              **
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y+self.block_size, self.block_size, self.block_size)]

			elif self.rotation == 180:
				# block is     *
				#              ***
				#             	 
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y-self.block_size, self.block_size, self.block_size)]

			elif self.rotation == 270:
				# block is    	**
				#            	*
				#               *
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size)]       
			
			else: # rotation is 0
				# block is    	
				#              *** 
				#             	 *
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y+self.block_size, self.block_size, self.block_size)]
		
		elif self.shape == "L":
			if self.rotation == 270:
				# block is   	* 
				#             	*
				#               **
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y+self.block_size, self.block_size, self.block_size)]
			
			elif self.rotation == 0:
				# block is     
				#              ***
				#              * 
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y+self.block_size, self.block_size, self.block_size)]

			elif self.rotation == 90:
				# block is     **
				#            	*
				#               *
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size)]            
			
			else: # rotation is 180
				# block is    	 *
				#              *** 
				#             	 
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y-self.block_size, self.block_size, self.block_size)]
		
		elif self.shape == "S":
			if self.rotation == 0 or self.rotation == 180:
				# block is     **	 
				#             **	
				#              
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y+self.block_size, self.block_size, self.block_size)]
			else: # rotation == 90 or rotation == 270
				# block is    *
				#             **
				#              *   	 
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y-self.block_size, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y+self.block_size, self.block_size, self.block_size)]
		
		elif self.shape == "Z":
			if self.rotation == 0 or self.rotation == 180:
				# block is     **	 
				#               **	
				#              
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x-self.block_size, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y+self.block_size, self.block_size, self.block_size)]
			
			else: # rotation == 90 or rotation == 270
				# block is     *
				#             **
				#             *   	 
				self.rects = [(self.x, self.y, self.block_size, self.block_size),
							  (self.x, self.y+self.block_size, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y, self.block_size, self.block_size),
							  (self.x+self.block_size, self.y-self.block_size, self.block_size, self.block_size)]