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
		if time.clock() - self.startTime > 0.06:
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

		heuristics = [
			self.smoothness(state), 
			self.monotonicity(state), 
			self.freeTiles(state), 
			state.getMaxTile()]
		
		weights = [
			0.1,
			0.8,
			3.0,
			1.0
		]

		return sum(x * y for x, y in zip(heuristics, weights))
	
	def monotonicity(self, state):
		totals = [0, 0, 0, 0]

		for x in range(state.size):
			curr = 0
			next = curr + 1
			while next < state.size:
				while next < state.size and state.map[x][next] == 0:
					next += 1
				if next >= state.size:
					next -= 1
				currVal = math.log(state.map[x][curr]) / math.log(2) if state.map[x][curr] != 0 else 0
				nextVal = math.log(state.map[x][next]) / math.log(2) if state.map[x][next] != 0 else 0
				if currVal > nextVal:
					totals[0] += nextVal - currVal
				elif nextVal > currVal:
					totals[1] += currVal - nextVal
				curr = next
				next += 1
		
		for y in range(state.size):
			curr = 0
			next = curr + 1
			while next < state.size:
				while next < state.size and state.map[next][y] == 0:
					next += 1
				if next >= state.size:
					next -= 1
				currVal = math.log(state.map[curr][y]) / math.log(2) if state.map[curr][y] != 0 else 0
				nextVal = math.log(state.map[next][y]) / math.log(2) if state.map[next][y] != 0 else 0
				if currVal > nextVal:
					totals[2] += nextVal - currVal
				elif nextVal > currVal:
					totals[3] += currVal - nextVal
				curr = next
				next += 1

		return max(totals[0], totals[1]) + max(totals[2], totals[3])

	def smoothness(self, state):
		score = 0

		for x in range(state.size):
			for y in range(state.size):
				if state.map[x][y] != 0:
					value = math.log(state.map[x][y]) / math.log(2)

					i = x + 1
					while i < state.size and state.map[i][y] == 0:
						i += 1
					if i < state.size and state.map[i][y] != 0:
						targetValue = math.log(state.map[i][y]) / math.log(2)
						score -= math.fabs(value - targetValue)
					
					i = y + 1
					while i < state.size and state.map[x][i] == 0:
						i += 1
					if i < state.size and state.map[x][i] != 0:
						targetValue = math.log(state.map[x][i]) / math.log(2)
						score -= math.fabs(value - targetValue)
		
		return score

	def freeTiles(self, state):
		score = 0

		for x in range(state.size):
			for y in range(state.size):
				if state.map[x][y] == 0:
					score += 1
		
		return math.log(score)

	def result(self, state, action):
		newState = state.clone()
		newState.move(action)
		return newState
