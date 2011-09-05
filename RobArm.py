# This module is a particular configuration of a BioloidArm (note the servoIDs)
# NOTE that this module is mainly for the TicTacToe playing robots (note the poses)

from BioloidArm import *;

servoIDs = {
	'base': 18,
	'shoulder': 15,
	'elbow': 14,
	'hand': 7,
};

class RobArm(BioloidArm):
	def __init__(self):
		# NOTE: RobArm goes on COM3. Windows has issues with 2 things communicating on
		# the same serial port. So we have to hardcode this arm to be on COM3 and make
		# sure we plug the seria-to-usb cable in the same USB slot every time.
		BioloidArm.__init__(self, servoIDs, port="COM3");

		# NOTE: This particular servo set required a little fudging of pulseRanges
		# for the servos since they didn't seem to be mounted securely enough.
		self.pulseRange = {
			'elbow': [800, 200],
			'base': [200, 800],
			'shoulder': [245, 815],
			'hand': [300, 800],
		};

		self.servoIDs = servoIDs;

		# Define some poses for this particular arm.
		# NOTE: The neutral pose must move the arm away from the vertical TicTacToe board
		self.poses['neutral'].update({'base': 400});
		self.createPosePulseWidths('pen_down', {'base': 500});
		self.createPosePulseWidths('pen_up', ['neutral']);
		self.createPosePulseWidths('put_dot', ['pen_down', 'pen_up']);


