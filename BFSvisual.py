import pygame
import queue
import math
import random

pygame.init()

SCREEN_LENGTH = 750
SCREEN_WIDTH = 600
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
GREY = (51, 51, 51)

CELL_SIZE = 25
NUM_OF_CELLS_H = int(SCREEN_LENGTH/CELL_SIZE)
NUM_OF_CELLS_V = int(SCREEN_WIDTH/CELL_SIZE)

class BFS:
	def __init__(self):
		self.goal_j = 9
		self.goal_i = 9
		self.board = [[0 for i in range(NUM_OF_CELLS_H)] for j in range(NUM_OF_CELLS_V)]
		self.board[math.floor(NUM_OF_CELLS_V/2)][math.floor(NUM_OF_CELLS_H/2)] = 1
		
		self.path = ""
		self.cells = []
		self.cache = {}
		self.goalSelected = False

	def showBoard(self, path=""):
		self.board[self.goal_j][self.goal_i] = 2
		for r, rows in enumerate(self.board):
			for c, columns in enumerate(rows):
				if self.board[r][c] == 1:
					rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, (255, 0, 0), rect)
					i = c
					j = r
				elif self.board[r][c] == 2:
					rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, (0, 255, 0), rect)
				elif self.board[r][c] == 3:
					rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, (255,255, 255), rect)


		self.pos = []
		for move in path:
			if move == 'L':
				i -= 1
			elif move == 'R':
				i += 1
			elif move == 'U':
				j -= 1
			elif move == 'D':
				j += 1
			self.pos.append((j, i))

		for r, rows in enumerate(self.board):
			for c, columns in enumerate(rows):
				if (r, c) in self.pos:
					rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, (255, 0, 0), rect)

		return True

	def valid(self, moves, pos):
		if not(0 <= pos[1] < len(self.board[0]) and 0 <= pos[0] < len(self.board)):
			return False


		if pos in self.cells:
			return False

		if 0 <= pos[1] < len(self.board[0]) and 0 <= pos[0] < len(self.board):
			if self.board[pos[0]][pos[1]] == 3:
				return False

		return True

	def findEnd(self, moves, pos):
		self.animations()
		pygame.display.update()
		

		if self.board[pos[0]][pos[1]] == 2:
			return True

		return False

	def getPos(self, moves):
		for r, rows in enumerate(self.board):
			for c, columns in enumerate(rows):
				if self.board[r][c] == 1:
					i = c
					j = r
		currentMove = ""
		for move in moves:

			if move == 'L':
				currentMove += 'L'
				i -= 1
			elif move == 'R':
				currentMove += 'R'
				i += 1
			elif move == 'U':
				currentMove += 'U'
				j -= 1
			elif move == 'D':
				currentMove += 'D'
				j += 1

		
		return (j, i)

	def animations(self):
		self.showBoard()
		grid(SCREEN_LENGTH, SCREEN_WIDTH, NUM_OF_CELLS_H, NUM_OF_CELLS_V, CELL_SIZE)
		for cell in self.cells:
			rect = pygame.Rect(cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(screen, (255, 255, 0), rect)

	def setObs(self):
		if pygame.mouse.get_pressed()[0] == True and not self.goalSelected:
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]

			if not(math.floor(x/CELL_SIZE) == self.goal_i and math.floor(y/CELL_SIZE) == self.goal_j):
				self.board[math.floor(y/CELL_SIZE)][math.floor(x/CELL_SIZE)] = 3

	def genMaze(self):
		for r, row in enumerate(self.board):
			for c, column in enumerate(row):
				if self.board[r][c] == 3:
					self.board[r][c] = 0
		for r, row in enumerate(self.board):
			for c, column in enumerate(row):
				if self.board[r][c] == 0:
					n = random.random()
					if n > 0.65:
						self.board[r][c] = 3
					else:
						continue

	def reset(self):
		self.cells.clear()
		self.pos.clear()
		self.path = ""
		for r, row in enumerate(self.board):
			for c, column in enumerate(row):
				if self.board[r][c] == 3:
					self.board[r][c] = 0
				if self.board[r][c] == 0:
					rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(screen, (0,0, 0), rect)

	def setGoalStatus(self):
		if self.goalSelected:
			self.goalSelected = False
			self.board[self.goal_j][self.goal_i] = 0
			self.goal_i = math.floor(pygame.mouse.get_pos()[0]/CELL_SIZE)
			self.goal_j = math.floor(pygame.mouse.get_pos()[1]/CELL_SIZE)
		else:
			if self.goal_i * CELL_SIZE < pygame.mouse.get_pos()[0] < (self.goal_i * CELL_SIZE) + CELL_SIZE:
				if self.goal_j * CELL_SIZE < pygame.mouse.get_pos()[1] < (self.goal_j * CELL_SIZE) + CELL_SIZE:
					if not self.goalSelected:
						self.goalSelected = True

	def setGoal(self):
		if self.goalSelected:
			rect = pygame.Rect(math.floor(pygame.mouse.get_pos()[0]/CELL_SIZE) * CELL_SIZE, math.floor(pygame.mouse.get_pos()[1]/CELL_SIZE)* CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(screen, (180, 242, 87), rect)



def grid(length, width, numCellsH, numCellsV, cellSize):
	x, y = 0, 0
	for i in range(numCellsH + 1):
		pygame.draw.line(screen, GREY, (x, y), (x, y + width), 2)
		x += cellSize
		
	x = 0
	for i in range(numCellsV + 1):
		pygame.draw.line(screen, GREY, (x, y), (x + length, y), 2)
		y += cellSize

b = BFS()
# Game Loop
running = True
while running:

	screen.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			b.setGoalStatus()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_m:
				b.genMaze()
			if event.key == pygame.K_r:
				b.reset()
			if event.key == pygame.K_SPACE:
				nums = queue.Queue()
				nums.put("")
				add = ""

				while not b.findEnd(add, b.getPos(add)):
					add = nums.get()
					for move in ('L','R','U','D'):
						put = add + move
						if b.valid(put, b.getPos(put)):
							nums.put(put)
							if b.getPos(put) not in b.cells:
								b.cells.append(b.getPos(put))


							print(put)

				b.path = add
		

	grid(SCREEN_LENGTH, SCREEN_WIDTH, NUM_OF_CELLS_H, NUM_OF_CELLS_V, CELL_SIZE)
	
	b.animations()
	b.setObs()
	b.showBoard(b.path)
	b.setGoal()
	clock.tick(60)
	pygame.display.update()