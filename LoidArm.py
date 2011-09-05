# This module is a particular configuration of a BioloidArm (note the servoIDs)
# NOTE that this module is mainly for the TicTacToe playing robots (note the poses)

from BioloidArm import *;

servoIDs = {
	'base': 1,
	'shoulder': 2,
	'elbow': 3,
	'hand': 4,
};

class LoidArm(BioloidArm):
	def __init__(self):
		# NOTE: LoidArm goes on COM5. Windows has issues with 2 things communicating on
		# the same serial port. So we have to hardcode this arm to be on COM5 and make
		# sure we plug the seria-to-usb cable in the same USB slot every time.
		BioloidArm.__init__(self, servoIDs, port="COM5");

		self.servoIDs = servoIDs;

		# Define some poses for this particular arm.
		# NOTE: The neutral pose must move the arm away from the vertical TicTacToe board
		self.poses['neutral'].update({'base': 600});
		self.createPosePulseWidths('pen_down', {'base': 500});
		self.createPosePulseWidths('pen_up', ['neutral']);
		self.createPosePulseWidths('put_dot', ['pen_down', 'pen_up']);

