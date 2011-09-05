README.txt

This package contains all the files used in creating the TicTacToe game built by the interns at GirlTech.


REQUIREMENTS
============
Requirements for TicTacToe without arms:
	- Python 2.5+

Additional requirements for the Bioloid arms:
	- If running this on Windows you need to download/install the pywin32 Python modules which are found here
		http://sourceforge.net/project/showfiles.php?group_id=78018&package_id=79063

	- The pySerial Python module which can be downloaded from (make sure you install pywin32 from above first)
		http://pyserial.wiki.sourceforge.net/pySerial


RUNNING
=======
Double click the Run.bat file

OR

To run the game either open main.py in your python editor and choose run current file

OR

Drag the TTT folder to the Desktop and do the following:
Open up a command line via WindowsKey+R, then type "cmd", then type "cd %userprofile%\Desktop\", hit enter, then type "python main.py", hit enter




Components of the TicTacToe Game
=================================
main.py - The starting point of the TicTacToe game 
TTTBoard - The TicTacToe board (and game engine)
TTTPlayer - The player class (human)
TTTPlayerAI - The artificial intelligence player class (computer)


Components of the Bioloid Robot Arms
=====================================
Core Modules
------------
Armature - Does simple Inverse Kinematics calculations
Bioloid - Does low level communication with the Bioloid computer/servos raw
BioloidArm - Combines Armature and Bioloid and creates a generic bioloid robot arm
RobArm - A specific set of servos that are used in creating one of the arms (inherits BioloidArm)
LoidArm - A specific set of servos that are used in creating the other arm (inherits BioloidArm)
FakeBioloidArm - Implements the same methods as BioloidArm but doesn't need any robots (fakes doing servo stuff)

Simple Scripts
--------------
neutral.py - Simple script to show how to move the arm into a neutral pose
makeCircle.py - Simple script that shows how to move the arm in a circular motion

Utility Scripts
---------------
bioloidArmRemoteControl.py - A simple Tcl/Tk based GUI for controlling a robot arm
bioloidArmRemoteControl - Loid.py - A simple Tcl/Tk based GUI for controlling a robot arm (LoidArm)
bioloidArmRemoteControl - Rob.py - A simple Tcl/Tk based GUI for controlling a robot arm (RobArm)


