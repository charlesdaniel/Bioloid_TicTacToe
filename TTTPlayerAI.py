# Import the TTTPlayer class because TTTPlayerAI will just inherit off of it and change the getMove() method
from TTTPlayer import *

## NOTE We're inheriting from TTTPlayer class which means we get everything that TTTPlayer has/offers.
## The only reason we're even having this class is so we can override the getMove() method and replace it
## with some artificial intelligence (ie. the computer player)

class TTTPlayerAI(TTTPlayer):
	def __init__(self, name, myPiece, armBot):
		# Pass all the parameters over to our parent class TTTPlayer so it can initialize appropriately
		TTTPlayer.__init__(self, name, myPiece, armBot)


	def getMove(self, board):
		# This method overrides the one TTTPlayer offers us and uses the winning combinations array to figure out
		# the best spot for our move.
		# This winningCombinations array was shamelessly stolen from the TTTBoard
		winningCombinations = [ [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6] ]

		# We run through all the winning combinations and look for a combination that has 2 of the cells having the same piece in it
		# so we can choose the third cell in that combination as our move. We don't care what the actual pieces are in the other 2
		# cells (ours or theirs), we'll either be blocking them or winning the game.
		# NOTE that we make sure that the third cell is empty before we pick it also.
		## TODO: Make this AI smarter by preferring a win over a block (we know our own piece which is my self.myPiece)
		for i in range(len(winningCombinations)):
			if (board[winningCombinations[i][0]] == board[winningCombinations[i][1]]) and (board[winningCombinations[i][2]] == ' '):
				return winningCombinations[i][2] 
			if (board[winningCombinations[i][1]] == board[winningCombinations[i][2]]) and (board[winningCombinations[i][0]] == ' '):
				return winningCombinations[i][0]
			if (board[winningCombinations[i][0]] == board[winningCombinations[i][2]]) and (board[winningCombinations[i][1]] == ' '):
				return winningCombinations[i][1]

		# If we reached this point that means we didn't find any cell winning combinations with 2 cells having the same piece in it
		# but we still need to make a move. So we'll just walk the board array from the beginning and pick the first empty spot.
		## TODO: Make this strategy smarter by maybe creating an array of cell ids listed in a certain order of best to worst that it can 
		## walk through and pick the first empty one from that order that is empty.
		for i in range(9):
			if (board[i] == ' '):
				return i
            
