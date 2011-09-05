#!/usr/bin/python

from RobArm import *;
from LoidArm import *;
from Tkinter import *;

# Servo increment/decrement pulseWidth steps for each direction
incr = { 'base': 25, 'shoulder': 25, 'elbow': 25, 'hand': 25 };


class Remote:
	def __init__(self, master):
		self.bioloid = RobArm();
		self.servoPulseWidths = {}; #'base': 500, 'shoulder': 500, 'elbow': 500, 'hand': 500};
		#self.bioloid.sendMotion(self.servoPulseWidths);
		self.gotoNeutral();

		self.entries = {};

		f = Frame(master);
		f.pack();

		l = Label(f, text="Bioloid Remote");
		l.pack(side=TOP);

		f = Frame(master);
		f.pack();
		Label(f, text="Hand (#%2d):     " % (self.bioloid.servoIDs['hand'])).pack(side=LEFT);
		Button(f, text=" <- ", fg="red", command=self.moveHandLeft).pack(side=LEFT);
		self.entries['hand']= Entry(f);
		self.entries['hand'].pack(side=LEFT);
		Button(f, text=" -> ", fg="red", command=self.moveHandRight).pack(side=LEFT);

		f = Frame(master);
		f.pack();
		Label(f, text="Elbow (#%2d):    " % (self.bioloid.servoIDs['elbow'])).pack(side=LEFT);
		Button(f, text=" <- ", fg="red", command=self.moveElbowLeft).pack(side=LEFT);
		self.entries['elbow']= Entry(f);
		self.entries['elbow'].pack(side=LEFT);
		Button(f, text=" -> ", fg="red", command=self.moveElbowRight).pack(side=LEFT);

		f = Frame(master);
		f.pack();
		Label(f, text="Shoulder (#%2d): " % (self.bioloid.servoIDs['shoulder'])).pack(side=LEFT);
		Button(f, text=" <- ", fg="red", command=self.moveShoulderLeft).pack(side=LEFT);
		self.entries['shoulder']= Entry(f);
		self.entries['shoulder'].pack(side=LEFT);
		Button(f, text=" -> ", fg="red", command=self.moveShoulderRight).pack(side=LEFT);

		f = Frame(master);
		f.pack();
		Label(f, text="Base (#%2d):     " % (self.bioloid.servoIDs['base'])).pack(side=LEFT);
		Button(f, text=" <- ", fg="red", command=self.moveBaseLeft).pack(side=LEFT);
		self.entries['base']= Entry(f);
		self.entries['base'].pack(side=LEFT);
		Button(f, text=" -> ", fg="red", command=self.moveBaseRight).pack(side=LEFT);

		f = Frame(master);
		f.pack();
		Button(f, text=" Neutral Pose ", command=self.gotoNeutral).pack();

		f = Frame(master);
		f.pack();
		Label(f, text="X:     ").pack(side=LEFT);
		self.entries['x']= Entry(f);
		self.entries['x'].pack(side=LEFT);

		f.pack();
		Label(f, text="Y:     ").pack(side=LEFT);
		self.entries['y']= Entry(f);
		self.entries['y'].pack(side=LEFT);

		f.pack();
		Label(f, text="interpolations:     ").pack(side=LEFT);
		self.entries['interpolationPoints']= Entry(f);
		self.entries['interpolationPoints'].pack(side=LEFT);
		self.entries['interpolationPoints'].insert(0, "1");


		Button(f, text=" Do IK ", fg="red", command=self.doIK).pack(side=LEFT);

	def gotoNeutral(self):
		self.bioloid.sendPose('neutral');
		self.servoPulseWidths.update(self.bioloid.poses['neutral']);
		#for i in self.entries:
			#self.entries[i].

	def updateEntries(self):
		for i in ('base','shoulder', 'elbow', 'hand'):
			self.entries[i].delete(0, END);
			self.entries[i].insert(0, "%.2f" %(self.servoPulseWidths[i]));

	def doIK(self):
		x = int(self.entries['x'].get());
		y = int(self.entries['y'].get());
		interpolationPoints = int(self.entries['interpolationPoints'].get());
		print "X = %d, Y = %d " % (x, y);
		self.bioloid.moveToIK(x=x, y=y, interpolationPoints=interpolationPoints);

	def moveBaseLeft(self):
		self.servoPulseWidths['base'] += incr['base'];
		self.bioloid.moveServoTo(servoIDs['base'], self.servoPulseWidths['base'], 10);
		self.updateEntries();

	def moveBaseRight(self):
		self.servoPulseWidths['base'] -= incr['base'];
		self.bioloid.moveServoTo(servoIDs['base'], self.servoPulseWidths['base'], 10);
		self.updateEntries();

	def moveShoulderLeft(self):
		self.servoPulseWidths['shoulder'] += incr['shoulder'];
		self.bioloid.moveServoTo(servoIDs['shoulder'], self.servoPulseWidths['shoulder'], 10);
		self.updateEntries();

	def moveShoulderRight(self):
		self.servoPulseWidths['shoulder'] -= incr['shoulder'];
		self.bioloid.moveServoTo(servoIDs['shoulder'], self.servoPulseWidths['shoulder'], 10);
		self.updateEntries();

	def moveElbowLeft(self):
		self.servoPulseWidths['elbow'] += incr['elbow'];
		self.bioloid.moveServoTo(servoIDs['elbow'], self.servoPulseWidths['elbow'], 10);
		self.updateEntries();

	def moveElbowRight(self):
		self.servoPulseWidths['elbow'] -= incr['elbow'];
		self.bioloid.moveServoTo(servoIDs['elbow'], self.servoPulseWidths['elbow'], 10);
		self.updateEntries();

	def moveHandLeft(self):
		self.servoPulseWidths['hand'] += incr['hand'];
		self.bioloid.moveServoTo(servoIDs['hand'], self.servoPulseWidths['hand'], 10);
		self.updateEntries();

	def moveHandRight(self):
		self.servoPulseWidths['hand'] -= incr['hand'];
		self.bioloid.moveServoTo(servoIDs['hand'], self.servoPulseWidths['hand'], 10);
		self.updateEntries();



root = Tk();
r = Remote(root);
root.mainloop();
