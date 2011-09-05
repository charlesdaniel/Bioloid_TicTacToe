import sys, os, math;

## This is the Armature module it handles all the computations for Inverse Kinematics for a special case of armatures
## based on the LynxMotion arm servo configurations (which is what the Bioloid arms are setup as).
## The inverse kinematics used here has to be passed the lengths of the base-to-shoulder, shoulder-to-elbow, elbow-to-hand and hand-to-endtip

class ArmatureException(Exception):
	def __init__(self, *args):
		Exception.__init__(self, *args);
		print "EXCEPTION ", sys.exc_info();

class Armature:
	def __init__(self, lengths):
		self.l = lengths;

	def deg2rad(self, degrees):
		# Method to convert from degrees to radians
		return (degrees / 180.0) * math.pi;

	def rad2deg(self, radians):
		# Method to convert from radians to degrees
		return (radians / math.pi) * 180.0;

	def compute2DIK(self, x, y, handAngle=0):
		# Converts a given (x,y) coordinate (in inches) to the appropriate servo degrees using triginometry. handAngle specifies the angle
		# of the hand relative to the ground plane (defaults to 0 if not passed in).

		offset = [
			math.cos(self.deg2rad(handAngle)) * self.l[3],
			math.sin(self.deg2rad(handAngle)) * self.l[3]
		];

		r = math.sqrt( ( ( y - offset[1] - self.l[0] ) * ( y - offset[1] - self.l[0] ) ) + ( ( x - offset[0] ) * ( x - offset[0] ) ) );

		print "R = ", r, "\n";
		if(r > (self.l[1] + self.l[2])):
			raise ArmatureException("NO SOLUTION");

		theta1 = math.atan2( ( y - offset[1] - self.l[0] ), ( x - offset[0] ) );
		theta2 = math.acos( ( ( self.l[1] * self.l[1] ) - ( self.l[2] * self.l[2] ) + ( r * r ) ) / ( 2.0 * self.l[1] * r ) );

		shoulder = self.rad2deg(theta1 + theta2);

		elbow = math.acos( ( ( self.l[1] * self.l[1] ) + ( self.l[2] * self.l[2] ) - ( r * r ) ) / ( 2.0 * self.l[1] * self.l[2] ) );

		elbow =  ( 180.0 - self.rad2deg(elbow) );
		hand = 90.0 + handAngle + elbow - shoulder;

		return { 'shoulder' : shoulder, 'elbow' : elbow, 'hand' : hand };


	def moveToIK(self, x, y, handAngle, baseAngle):
		# Whoever inherits from this class will move their arm appropriately, this is just here to catch anyone calling the method.
		pass;




