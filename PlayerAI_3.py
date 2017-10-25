import math
import time
from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
	def __init__(self):
		self.startTime = 0

	def getMove(self, grid):
		return self.alphaBetaSearch(grid)

	def alphaBetaSearch(self, state):
		self.startTime = time.clock()
		return self.maxValue(state, -math.inf, math.inf)[0]
	
	def maxValue(self, state, alpha, beta):
		if self.cutoffTest(state):
			return (None, self.eval(state))
		
		maxChild = None
		maxUtility = -math.inf

		for action in state.getAvailableMoves():
			child = self.result(state, action)
			u = self.minValue(child, alpha, beta)
			
			if u[1] > maxUtility:
				maxChild = action
				maxUtility = u[1]
			
			if maxUtility >= beta:
				break
			
			if maxUtility > alpha:
				alpha = maxUtility
		
		return (maxChild, maxUtility)
	
	def minValue(self, state, alpha, beta):
		if self.cutoffTest(state):
			return (None, self.eval(state))
		
		minChild = None
		minUtility = math.inf

		for action in state.getAvailableMoves():
			child = self.result(state, action)
			u = self.maxValue(child, alpha, beta)
			
			if u[1] < minUtility:
				minChild = action
				minUtility = u[1]
			
			if minUtility <= alpha:
				break
			
			if minUtility < beta:
				beta = minUtility
		
		return (minChild, minUtility)
	
	def cutoffTest(self, state):
		if time.clock() - self.startTime > 0.05:
			return True
		if state.getMaxTile() >= 2048:
			return True
		if state.getAvailableMoves() == []:
			return True

		return False
	
	def eval(self, state):
		if state.getMaxTile() >= 2048:
			return math.inf
		if state.getAvailableMoves() == []:
			return -math.inf

		return -self.smoothness(state) + self.monotonicity(state) + self.freeTiles(state)
	
	def monotonicity(self, state):
		score = 0

		lastDiff = state.map[0][1] - state.map[0][0]
		for x in range(state.size):
			for y in range(1, state.size):
				diff = state.map[x][y] - state.map[x][y - 1]
				if (diff > 0 and lastDiff > 0) or (diff < 0 and lastDiff < 0):
					score += 10
				elif (diff > 0 and lastDiff < 0) or (diff < 0 and lastDiff > 0):
					score -= 10
				lastDiff = diff
		
		lastDiff = state.map[1][0] - state.map[0][0]
		for y in range(state.size):
			for x in range(1, state.size):
				diff = state.map[x][y] - state.map[x - 1][y]
				if (diff > 0 and lastDiff > 0) or (diff < 0 and lastDiff < 0):
					score += 10
				elif (diff > 0 and lastDiff < 0) or (diff < 0 and lastDiff > 0):
					score -= 10
				lastDiff = diff
		
		# varies from -160 to 160
		return (score + 160) / 320

	def smoothness(self, state):
		score = 0

		for x in range(state.size):
			for y in range(state.size):
				if x + 1 < state.size:
					score += math.fabs(state.map[x][y] - state.map[x + 1][y])
				if y + 1 < state.size:
					score += math.fabs(state.map[x][y] - state.map[x][y + 1])
		
		# varies from 0 to ~49,152 (?)
		return score / 49152

	def freeTiles(self, state):
		score = 0

		for x in range(state.size):
			for y in range(state.size):
				if state.map[x][y] == 0:
					score += 1
		
		# varies from 0 to 16
		return score / 16

	def result(self, state, action):
		newState = state.clone()
		newState.move(action)
		return newState
