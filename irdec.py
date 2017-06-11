#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import argparse

parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, description = 'Input: $ mode2 -d /dev/lirc0')
#parser.add_argument('--hdr-mark', default = 3500, help = 'Header mark')
#parser.add_argument('--hdr-space', default = 1700, help = 'Header space')
#parser.add_argument('--bit-mark', default = 440, help = 'Bit mark')
parser.add_argument('--bit-one-space', default = 440, help = 'Bit one space')
parser.add_argument('--bit-zero-space', default = 1300, help = 'Bit zero space')
#parser.add_argument('--tail-mark', default = 440, help = 'Tail mark')
parser.add_argument('--tail-space', default = 12000, help = 'Tail space')
parser.add_argument('-s', '--bit-swap', choices = [0, 1], default = 1, help = 'Set bit swapping true or false')
args = parser.parse_args()

def createThresholds():
	global tailToZero, zeroToOne

	tailToZero = (args.tail_space + args.bit_zero_space) / 2
	zeroToOne = (args.bit_zero_space + args.bit_one_space) / 2

	#print 'tailToZero: %d' % tailToZero
	#print 'zeroToOne: %d' % zeroToOne

def getTokenType(sigLen):
	global tailToZero, zeroToOne

	#print sigLen

	if (sigLen > args.tail_space):
		return 0 # IDLE
	elif (sigLen > tailToZero):
		return 1 # Tail
	elif (sigLen > zeroToOne):
		return 2 # Zero
	else:
		return 3 # One

def processLine(line):

	if processLine.first:
		processLine.first = False
		return

	[sigType, sigLen] = line.split()

	if (sigType == 'space'):
		tokenType = getTokenType(int(sigLen))

		if (tokenType == 0):
			print ''
		elif (tokenType == 1):
			sys.stdout.write('  ')
		elif (tokenType == 2):
			sys.stdout.write('0')
		else:
			sys.stdout.write('1')

processLine.first = True

# Init
createThresholds()

# Processing
k = 0
try:
	while True:
		line = sys.stdin.readline()

		if not line:
			break

		processLine(line)
		k = k + 1

		#if k == 15: break

except KeyboardInterrupt:
	sys.stdout.flush()
	pass

print ''
#print "%s lines processed" % (k)

sys.exit(0)
