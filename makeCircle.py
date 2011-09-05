#!/usr/bin/python

## This is a quick script to have the arms trace a small circle

import sys, os, math;
from RobArm import *;
#from LoidArm import *;

rob = RobArm();
#loid = LoidArm();

c = [6, 6];
r = 3.0;	# radius

for i in range(0,36):
	i *= 10;
	j = (i / 180.0) * math.pi;
	x = r * math.cos(j) + c[0];
	y = r * math.sin(j) + c[1];
	print "X %.2f   Y %.2f\n" % (x, y);

	degrees = rob.compute2DIK(x, y);
	print degrees;
	motion = rob.computePulseWidths(degrees);
	print motion;
	rob.sendMotion(motion, time=1, wait=False);
#	loid.sendMotion(motion, time=1, wait=False);

