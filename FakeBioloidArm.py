import os, sys, math, time;

## This is a fake Bioloid Arm that implements (and ignores) the various methods that are found in the real BioloidArm

class FakeBioloidArm():
	def __init__(self):
		print "Currently using the FakeBioloidArm... We are Armless... oh noooes... we'll fake/ignore all actual calls to the arm.";

	def createPosePulseWidths(self, poseName, servoPulseWidths):
		pass;	## do nothing

	def createPoseDegrees(self, poseName, servoDegrees):
		pass;	## do nothing

	def sendPose(self, pose):
		print "POSE: ", pose
		pass;	## do nothing

	def computePulseWidths(self, servoDegrees):
		pass;	## do nothing

	def waitForDone(self):
		pass;	## do nothing
		
	def sendMotion(self, servoPulseWidths, time=0, wait=True, interpolationPoints=1):
		pass;	## do nothing

	def moveToIK(self, x, y, handAngle=-1, baseAngle=-1, time=-1, interpolationPoints=1):
		print "MOVING TO IK (%f, %f) @ (%d interpolations)\n" % (x,y, interpolationPoints);
		pass;	## do nothing

