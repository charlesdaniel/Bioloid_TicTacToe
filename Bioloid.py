import serial;
import os, sys, math;

## This class handles all low level communication with the Bioloid computer. It uses the pyserial module (see above "import serial")
## to connect to the Bioloid computer via the serial port and send it the raw command to move servos to appropriate pulse widths.

class Bioloid():
	def __init__(self, port=None, baud=57600):
		self.botConnected = False;
		self.botConnectPort = port;
		self.botConnectBaud = baud;

		if(self.openBotConnection()):
			self.botConnected = True;


	def __del__(self):
		self.closeBotConnection();
			
	def openBotConnection(self):
		try:
			banner = '';
			if(self.botConnectPort != None):
				# If we were passed a port to connect to then use it
				self.serialPort = serial.Serial(self.botConnectPort, self.botConnectBaud, timeout=.25);
				self.writeToBot("scan");
				x = self.readFromBot(1024);
				while(len(x) > 0):
					banner += x;
					x = self.readFromBot(1024);

			else:
				# If we weren't given any ports then we better start scanning through ports looking for the bioloids
				testPorts = [];
				if(os.name == 'nt'):		## This is for windows 
					for i in range(1,6):
						testPorts.append("COM%d" % (i));
				else:				## This is for Linux
					for i in range(6):
						testPorts.append("/dev/ttyUSB%d" % (i));

				# Run through the ports and try connecting and sending the "scan" bioloid command.
				# "scan" seemed to be the safest (non-volatile) command to send to see if we get a response.
				# We then look for the word "Dynamixel" somewhere in the response and see if it is successful.
				for i in testPorts:
					try:
						self.botConnectPort = i;
						print "TRYING PORT ", self.botConnectPort;
						self.serialPort = serial.Serial(self.botConnectPort, self.botConnectBaud, timeout=.25);

						# Send the "scan" command
						self.writeToBot("scan");

						# Read from the bot 1024 characters at a time appending to banner
						x = self.readFromBot(1024);
						while(len(x) > 0):
							banner += x;
							x = self.readFromBot(1024);

						# Look for the word "Dynamixel"
						if(banner.find("Dynamixel") >= 0):
							print banner, "\n";
							print "Found a Dynamixel port at :", self.botConnectPort;
							break;

					except serial.SerialException:
						# Pyserial must have thrown an exception so the port is fail
						print "SERIAL FAILED ON ", self.botConnectPort;
						self.botConnectPort = None;

				if(self.botConnectPort == None):
					# If no ports were found from the scanning return false
					return False;

		except serial.SerialException, exception:
			# Pyserial must have thrown an exception so return False
			return False;

		# Assume we're good, return True
		return True;


	def closeBotConnection(self):
		# Close the serial port connection to the bioloid computer
		try:
			if(self.serialPort.isOpen()):
				# Reset Bot?
				self.serialPort.close();

		except: # Exception, exception:
			return False;

		return True;


	def writeToBot(self, cmd):
		# This method sends a raw command to the Bioloid computer (tacks on a \r)
		#print "<- ", cmd, "\n";
		cmd += "\r";
		self.serialPort.write(cmd);


	def readFromBot(self, bytes):
		# This method reads a certain amount of bytes from the Bioloid computer
		r = '';
		r = self.serialPort.read(bytes);
		#print "-> ", r, "\n";
		return r;


	def moveServoTo(self, servoID, pulseWidth, time):
		# This method moves a particular servo on the chain of Bioloid servos hooked up
		# to the Bioloid computer (CM-5) to a given pulseWidth in a given amount of time.
		# Note the sequence of raw instructions to move a servo to a pulse width is as follows
		#
		# cid servoID
		# go pulseWidth time
		#
		# where servoID, pulseWidth, and time are all integers. Be sure to read the response from
		# the bioloid computer too in between instructions.

		self.writeToBot("cid %d" % (servoID));
		self.readFromBot(255);
		self.writeToBot("go %d %d" % (pulseWidth, time));
		self.readFromBot(255);


