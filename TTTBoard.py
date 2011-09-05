## Import the base TTTPlayer class (we'll need it later to prompt for input)
from TTTPlayer import *

## The TTTBoard is the engine that drives the game. It handles prompting for input from
## any TTTPlayer class (this includes TTTPlayerAI since that inherits from TTTPlayer).
## Additionally this class prints out the board to the screen, checks for any winnings,
## and tells the winner if they won.
class TTTBoard():
	def __init__(self, player0, player1):
		self.players = [player0, player1]

		# The Board is a 1 dimensional array layed out like so
		#  0 | 1 | 2
		# -----------
		#  3 | 4 | 5
		# -----------
		#  6 | 7 | 8
		#
		# The values in the cells are ' ' or a player's index from the players array (ie. "0" or "1")
		self.board = []

	def resetBoard(self):
		# This method resets the board values to a space character (no piece) in each cell
		self.board = [	' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

	def checkWin(self):
		## This method scans through all the possible winning combinations of cells and sees if the values
		## in those cells are the same (and not " " empty). If it finds a combination then it returns the
		## combination back. Otherwise it returns the value None.

		# These are all the winning cell combinations in Tic-Tac-Toe
		winningCombinations = [ [0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6] ]

		# Run through those winning combinations looking for matching values in each cell in each combination
		# Also make sure the cells actually have a value other than ' '
		for c in winningCombinations:
			if((self.board[c[0]] != ' ') and
			   (self.board[c[0]] == self.board[c[1]]) and
			   (self.board[c[1]] == self.board[c[2]])):

				return c	# Found a combination which has all the same values, win

		return None	# Didn't find any combinations that won


	def printBoard(self):
		## This method prints out the nice board
		print " %s | %s | %s " % (self.board[0], self.board[1], self.board[2])
		print "-----------"
		print " %s | %s | %s " % (self.board[3], self.board[4], self.board[5])
		print "-----------"
		print " %s | %s | %s " % (self.board[6], self.board[7], self.board[8])



	def playGame(self):
		## This method is the main engine of a (one) game (the driver).

		# Clear the board of pieces
		self.resetBoard()

		winningMove = None	# This will hold the winning combination
		numMoves = 0

		p = 0  # The index of the current player in the self.players array

		# Main Loop: Prompt for move and check winnings until there's a winner or 8 moves have been made
		while ((numMoves < 9) and (winningMove == None)):
			# Print the board for the user
			self.printBoard()

			# Ask the current player for a move via the TTTPlayer/TTTPlayerAI getMove() method
			m = self.players[p].getMove(self.board)

			# Check to see if that cell is empty or not
			if(self.board[m] == ' '):

				# Place the piece (value of p either 0 or 1) on that cell
				self.board[m] = p

				# Tells the current player the piece has been placed successfully
				# (this is so the TTTPlayer/TTTPlayerAI can move the robot arms to put
				# the marking in that cell.
				self.players[p].placePiece(m)

				# Increment the count of moves taken
				numMoves = numMoves + 1

				# Toggle to make the other player the current player
				p = 1 - p	# Simple trick to toggle between p = 0 and p = 1

			else:
				# If we're here then it means the cell was not empty
				print "ILLEGAL MOVE PLAYER ", self.players[p].name, " TRY AGAIN "

			
			# We check to see if anybody won
			winningMove = self.checkWin()


		# We are outside the main game loop here. So we print the final board out for the user to see.
		self.printBoard()

		# We check to see how we exited the main game loop (either winningMove contains the winning combination
		# or we reached the maximum number of moves). So this if statement checks to see if winningMove is not None
		# like we initialized it before the loop.
		if (winningMove != None):
			# We find out the piece (0 or 1) that won from the first cell of the winningMove array
			winner = self.board[winningMove[0]]

			# Tell them they won
			print "PLAYER ", self.players[winner].name, " HAS WON THIS GAME USING POSITIONS ", winningMove

			# Tell the TTTPlayer/TTTPlayerAI to draw their winning line (using the arms)
			self.players[winner].placeWinningLine(winningMove)

		else:
			# If we're here then we must have exited the loop because we reached the limit of moves
			print "NOBODY WON !"


