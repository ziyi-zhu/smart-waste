from serial import Serial
import time 
board = Serial('COM6', 9600)
# This creates an object able to establish a serial communication channel
# with the board. The first parameter depends on your operating system
# and probably needs to be updated.
# The second is the baud rate. It needs to match the board's settings.
time.sleep(1)
x = 1
while x==0:
	line = board.readline()
	print(line)
	if "x" in line:
		x =1 
	

board.write(b'0')