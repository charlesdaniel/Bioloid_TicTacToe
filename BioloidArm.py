from Bioloid import *;
from Armature import *;
import os, sys, math, time;

BioloidArmDefaultWaitTime = 10;

## The BioloidArm class inherits from Bioloid (for raw communications to the Bioloid computer/servos)
## and Armature class (to give us the Inverse Kinematics computations)
## NOTE: The BioloidArm needs to be passed in the servoIDs of the servos that represent the joints in
## the particular bioloid arm configuration. The best way to do this is to inherit from BioloidArm and
## pass in the servoIDs in your inherited class's init call to BioloidArm's init.

class BioloidArm(Bioloid, Armature):
	def __init__(self, servoIDs, port=None):
		## servoIDs must be of the form
		##  { 'base': 1, 'shoulder': 2, 'elbow': 3, 'hand': 4 }
		## where the 1, 2, 3, 4 are the servo ids written on the physical Bioloid servo
		self.servoIDs = servoIDs;

		## Initialize the Bioloid class computer connection
		Bioloid.__init__(self, port=port);

		## Initialize the Armature class by passing in the lengths of the arm bones
		Armature.__init__(self, [
						2.0, # base height
						3.65, # humerus
						3.65, # ulna
						2.65, # hand
		]);


		## Set the pulseRanges for the various joints/servos that make sense.
		## Note that midway should be around 90degrees on the servo. You may
		## want to fudge around with the ranges to get things nice.
		self.pulseRange = {
			'base': [200, 800],
			'shoulder': [215, 815],
			'elbow': [800, 200],
			'hand': [300, 800],
		};

		## This will hold all our poses, we include a neutral pose
		self.poses = {
			'neutral': {'base': 500, 'shoulder': 515, 'elbow': 515, 'hand': 500},
		};

		## This is the order of operations of moving the servos since we can only move
		## one servo at a time in the Bioloid setup.
		self.servoMoveOrder = ['base', 'shoulder', 'elbow', 'hand'];

		## This is for us to keep track of our currentPulseWidths since we don't pull that
		## info from the bioloid servos (maybe a TODO later)
		self.currentPulseWidths = { 'base': 0, 'shoulder': 0, 'elbow': 0, 'hand': 0 };

	def createPosePulseWidths(self, poseName, servoPulseWidths):
		# This method lets you setup a pulse width configuration and call it a pose
		self.poses[poseName] = servoPulseWidths;

	def createPoseDegrees(self, poseName, servoDegrees):
		# This method does the same as the above but lets you pass in the configuration as degree values
		# then this method recursively goes through the structure and converts the degrees to the
		# appropriate pulse width values. Note that self.poses must contain only pulse width values.

		def recursivePulseWidthConversion(servoDegrees):
			if(type(servoDegrees).__name__ == 'dict'):
				servoDegrees.update(self.computePulseWidths(servoDegrees));
				return servoDegrees;
			elif(type(servoDegrees).__name__ == 'list'):
				for i in range(len(servoDegrees)):
					servoDegrees[i] = recursivePulseWidthConversion(servoDegrees[i]);
				return servoDegrees;
			elif(type(servoDegrees).__name__ == 'str'):
				return servoDegrees;

		self.poses[poseName] = recursivePulseWidthConversion(servoDegrees);


	def sendPose(self, pose):
		# This method walks through a pose's data structure and calls sendMotion with the appropriate
		# pulse width configurations.

		if(type(pose).__name__ == 'list'):
			for i in pose:
				self.sendPose(i);
		elif(type(pose).__name__ == 'str'):
			if(self.poses.has_key(pose)):
				self.sendPose(self.poses[pose]);
		elif(type(pose).__name__ == 'dict'):
			if(pose.has_key('time')):
				self.sendMotion(pose, time=pose['time']);
			else:
				self.sendMotion(pose);
			
		return True;


	def computePulseWidths(self, servoDegrees):
		# This method converts from degrees to pulsewidth values for each servo (based on the self.pulseRange)
		# The degree range is 0..180 and that maps out to the pulseRange[servo][0]..pulseRange[servo][1]
		servoPulseWidths = {};
		for i in servoDegrees:
			if(self.pulseRange.has_key(i)):
				normalized = servoDegrees[i] / 180.0;
				range = self.pulseRange[i][1] - self.pulseRange[i][0];
				pulseWidth = (range * normalized) + self.pulseRange[i][0];
				servoPulseWidths[i] = pulseWidth;

		return servoPulseWidths;


	def waitForDone(self):
		# We'll sleep for a bit ourselves until the servo hardware catches up with the instruction.
		# NOTE we're not polling the hardware, we're just guestimating the time to wait.
		t = self.currentMovementTimeMS / 1000.0;
		print "SOFT WAIT [%f]\n" % t;
		time.sleep(t);
		

	def sendMotion(self, servoPulseWidths, time=BioloidArmDefaultWaitTime, wait=True, interpolationPoints=1):
		# This method sends a pulse width configuration to the servos on the bioloid arm.
		# NOTE that we handle the interpolation of the movement by splitting each pulsewidth movement
		# (newPulseWidth - currentPulseWidth) into interpolationPoints increments. Then we walk that
		# many increments and move each servo (in the order of servoMoveOrder) at each step.

		increment = {};
		for i in servoPulseWidths:
			increment[i] = (servoPulseWidths[i] - self.currentPulseWidths[i]);
			increment[i] = increment[i] / interpolationPoints;

		print "INTERPOLATION INCREMENT ", increment;

		for t in range(interpolationPoints):
			for i in self.servoMoveOrder:
				if((servoPulseWidths.has_key(i)) and (self.servoIDs.has_key(i)) and (increment[i] != 0)):
					self.currentPulseWidths[i] = self.currentPulseWidths[i] + increment[i];
					self.moveServoTo(self.servoIDs[i], self.currentPulseWidths[i], 200);

		if(wait):
			self.currentMovementTimeMS = time;
			self.waitForDone();



	def moveToIK(self, x, y, handAngle=-1, baseAngle=-1, time=-1, interpolationPoints=1):
		# This method uses the Armature's compute2DIK to solve the Inverse Kinematics for (x,y) to get the
		# degrees for the shoulder, elbow, hand and then calls computePulseWidths to convert those degrees
		# to pulse widths and then finally calls sendMotion to send the actual pulse width configuration to
		# the hardware.

		print "MOVING TO IK (%f, %f) @ (%d interpolations)\n" % (x,y, interpolationPoints);
		degrees = self.compute2DIK(x, y, handAngle);
		print "DEGREES IS ", degrees;
		if(baseAngle >= 0):
			degrees['base'] = baseAngle;

		motion = self.computePulseWidths(degrees);
		print "MOTION IS ", motion;
		if(time > -1):
			self.sendMotion(motion, time=time, interpolationPoints=interpolationPoints);
		else:
			self.sendMotion(motion, interpolationPoints=interpolationPoints);


