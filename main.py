## Make sure we import the 3 modules we need for TicTacToe
from TTTBoard import *
from TTTPlayer import *
from TTTPlayerAI import *


## The following 4 lines only work if you have actual BioloidArms built
## and hooked up correctly, otherwise we use the FakeBioloidArm below.
#from RobArm import *
#from LoidArm import *
#rob = RobArm()
#loid = LoidArm()


## The following 3 lines are for faking the robot arms using FakeBioloidArm
from FakeBioloidArm import *
rob = FakeBioloidArm()
loid = FakeBioloidArm()

## We'll hold their choice in the variable choice
choice = ''

## We loop until they enter a '0' character
while(choice != '0'):
	## Initialize our player objects to None at first
	playerO = None
	playerX = None

	## Print the pretty menu
	print "== TIC TAC TOE =="
	print "[1] Human (O) vs Human (X)"
	print "[2] Human (O) vs Computer (X)"
	print "[3] Computer (O) vs Human (X)"
	print "[4] Computer (O) vs Computer (X)"
	print "---------------------------------"
	print "[0] Quit"
	print "_________________________________"
	print ""

	## Prompt and get their choice 
	choice = raw_input("Choice : ")

	## Create player objects for Human vs Human
	if(choice == '1'):
		name = raw_input("Enter Name for Human Player O: ")
		playerO = TTTPlayer(name, 0, rob)
		name = raw_input("Enter Name for Human Player X: ")
		playerX = TTTPlayer(name, 1, loid)

	## Create player objects for Human vs Computer
	elif(choice == '2'):
		name = raw_input("Enter Name for Human Player O: ")
		playerO = TTTPlayer(name, 0, rob)
		playerX = TTTPlayerAI("Computer(X)", 1, loid)

	## Create player objects for Computer vs Human
	elif(choice == '3'):
		playerO = TTTPlayerAI("Computer(O)", 0, rob)
		name = raw_input("Enter Name for Human Player X: ")
		playerX = TTTPlayer(name, 1, loid)

	## Create player objects for Computer vs Computer
	elif(choice == '4'):
		playerO = TTTPlayerAI("Computer(O)", 0, rob)
		playerX = TTTPlayerAI("Computer(X)", 1, loid)

	## If it's none of the choices above and it still isn't "0" then
	## tell them it's a bad choice and they fail at life.
	elif(choice != '0'):
		print "BAD CHOICE, TRY AGAIN!"
		print ""

	## Sanity check, make sure our player objects are actual objects
	## rather than the None we set them to originally. Then create a
	## TTTBoard object and pass in the players and play a game.
	if(playerO != None and playerX != None):
		game = TTTBoard(playerO, playerX)
		game.playGame()


