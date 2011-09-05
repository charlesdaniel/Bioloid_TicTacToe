#!/usr/bin/python

## This is a quick script to move the 2 arms to neutral poses

from LoidArm import *;
from RobArm import *;

loid = LoidArm();
rob = RobArm();

loid.sendPose('neutral');
rob.sendPose('neutral');
