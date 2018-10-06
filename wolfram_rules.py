# Simulator for Wolfram's Rules

import sys
from PIL import Image
import numpy
import random

rule  = -1
steps = -1
width = -1
randomize = False
OFF =  0xFFFFFFFF # white
ON = 0xFF000000 # black

def usage():
	print "usage:"
	print "python wolfram_rules.py RULE WIDTH STEPS <RAND>"
	print "RULE: Wolfram rule 0-255"
	print "WIDTH: Width of image to render in pixels (at least 18)"
	print "STEPS: Number of generations/(height in pixels) to render (at least one)"
	print "RAND: (Optional) Randomize starting generation"

def test():
	#check to make sure parameters are in bounds
	exit = False
	if rule < 0:
		print "** rule must be greater than or equal to zero **", rule
		exit = True
	if rule > 255:
		print "** rule must be less than or equal to 255 **", rule
		exit = True
	if width < 18:
		print "** width must be greater than or equal to 18 **", width
		exit = True
	if steps <= 1:
		print "** steps must be greater than 1 **", steps
		exit = True
	return exit

def alive(i, step):
	#determine if we turn on a pixel, based on rule
	#i is index into step (column)
	#step is current row
	step = step - 1
	l = grid[step][i-1]
	c = grid[step][i]
	r = grid[step][i+1]
	if (rule & 0x80) and (l == ON and c == ON and r == ON): 
		return True
	elif (rule & 0x40) and (l == ON and c == ON and r == OFF): 
		return True
	elif (rule & 0x20) and (l == ON and c == OFF and r == ON): 
		return True
	elif (rule & 0x10) and (l == ON and c == OFF and r == OFF): 
		return True
	elif (rule & 0x08) and (l == OFF and c == ON and r == ON): 
		return True
	elif (rule & 0x04) and (l == OFF and c == ON and r == OFF): 
		return True
	elif (rule & 0x02) and (l == OFF and c == OFF and r == ON): 
		return True
	elif (rule & 0x01) and (l == OFF and c == OFF and r == OFF): 
		return True
	return False

#******************************************
#*********       START       **************
#******************************************

try:
	rule  = int(sys.argv[1])
	width = int(sys.argv[2])
	steps = int(sys.argv[3])
except:
	usage()
	exit()
if test():
	usage()
	exit()
if len(sys.argv) == 5: # assume any entry is valid
	randomize = True

grid = numpy.zeros((width, steps), numpy.uint32)
grid.shape = steps, width

# zero out starting matrix
for i in xrange(width):
	grid[0][i] = OFF
for i in xrange(steps):
	grid[i][width-1] = OFF
	grid[i][0] = OFF

# randomly seed row, or single pixel in the center
if randomize != False:
	for i in xrange(width):
		grid[0][i] = random.choice([ON, OFF])
else:
	grid[0][width/2] = ON

for step in xrange(1, steps):
	for col in xrange(1, width-1):
		if alive(col, step):
			grid[step][col] = ON
		else:
			grid[step][col] = OFF
grid.shape = steps, width
image = Image.frombuffer('RGBA', (width, steps), numpy.uint32(grid), 'raw', 'RGBA', 0, 1)
image.save("Rule%03d.png" % rule)
