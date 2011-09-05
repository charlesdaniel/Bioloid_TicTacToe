## This class is the base class for any player of the TicTacToe game.
class TTTPlayer():
	def __init__(self, name, myPiece, armbot):
		# Initialize with the name of the player (that was passed in)
		self.name = name

		# Hold on to what our piece is (0 or 1) (that was passed in)
		self.myPiece = myPiece

		# Hold on to our robot arm (that was passed in)
		self.armbot = armbot

		# Tell our robot arm to go to its neutral position (just for sanity sake)
		self.armbot.sendPose('neutral');

		# These are the inches in the IK where our robot's end effector must reach
		# in order to place the mark in the appropriate cell.
		self.cellpositions = [[4.5,7],[6,7],[7.5,7],[4.5,5],[6,5],[7.5,5],[4.5,3],[6,3],[7.5,3]]

	def getMove(self, board):
		# This method prompts the player for a move and ensures that
		# its between 0..8

		# NOTE: This remap array was so we can use a numeric keypad of the keyboard as the physical
		# representation of the tic tac toe board for the human. It simply remaps the number the human hits
		# on the keypad to the appropriate cell value. The numeric keypad has the following configuration
		#	 7 | 8 | 9
		#	-----------
		#	 4 | 5 | 6
		#	-----------
		#	 1 | 2 | 3
		# and it has to be mapped out to our cell ids in our board which looks like this
		#	 0 | 1 | 2
		#	-----------
		#	 3 | 4 | 5
		#	-----------
		#	 6 | 7 | 8
		# So we put the appropriate cell ids in the remap array in the positions that the keypad evaluates to.
		# For example when they hit "1" on the keypad it uses remap[1] which has the cell id 6 for the board.
		remap = [None, 6, 7, 8, 3, 4, 5, 0, 1, 2]

		m = -1
		while ((m < 0) or (m > 8)):
			# Prompt the player for move
			m = raw_input("PLAYER " + self.name + " MOVE: ")

			# Verify that it's a value between 1 and 9 (we're using the numeric keypad with remap)
			if((m >= '1') and (m <= '9')):
				# convert it to a number instead of a string character we get from raw_input
				m = int(m)

				# Again check to see if it's between 1 and 9 (sanity check)
				if((m >= 1) and (m <= 9)):
					return remap[m]		# Return the cell id of the board (using remap)

			# If we're here that means we didn't return and it must be an invalid input
			print "TRY AGAIN!"


	def placePiece(self, cell):
		# This method gets called by TTTBoard after it determines the move is valid so we move the arm
		# to the appropriate IK position of the cell and put the dot there.

		print "Placing piece ", self.myPiece, " at cell ", cell
		self.armbot.moveToIK(x=self.cellpositions[cell][0], y=self.cellpositions[cell][1]); 
		self.armbot.sendPose('put_dot');


	def placeWinningLine(self, winningMove):
		# This method gets called by TTTBoard when it determines that we won. We get passed in the winningMove
		# array of 3 cells. So we move the arm to the first cell's IK, put a dot, and move to the 2nd cell and the
		# 3rd cell. Then lift up the pen, thus drawing a line from the first to the last cell of the winning move.
		# NOTE that we're setting the interpolationPoints so the armbots can take small steps to get to the location
		# because the BioloidArms can't do straight lines in one shot.

		print "Drawing a Line from ", winningMove[0] , " to ", winningMove[1], " to ", winningMove[2]
		self.armbot.moveToIK(self.cellpositions[winningMove[0]][0],self.cellpositions[winningMove[0]][1]);
		self.armbot.sendPose('pen_down');
		self.armbot.moveToIK(self.cellpositions[winningMove[1]][0],self.cellpositions[winningMove[1]][1], interpolationPoints=10);
		self.armbot.moveToIK(self.cellpositions[winningMove[2]][0],self.cellpositions[winningMove[2]][1], interpolationPoints=10);
		self.armbot.sendPose('pen_up');

