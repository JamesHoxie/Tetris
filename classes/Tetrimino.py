import random

# class definition for a tetrimino block
class Tetrimino():
	tetris_shapes = {1: "I", 2: "O", 3: "T", 4: "J", 5: "L", 6: "S", 7: "Z"}

	def __init__(self):
		self.active = True
		self.shape = self.tetris_shapes[random.randint(1, 7)]
		self.rotation = 0

	def __str__(self):
		return self.shape + " block"

	# public methods
	# check if this tetrimino has been placed or is being moved still
	def been_placed(self):
		return self.active == False
