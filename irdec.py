#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import argparse

parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, description = 'Input: $ mode2 -d /dev/lirc0')
#parser.add_argument('--hdr-mark', default = 3500, help = 'Header mark')
#parser.add_argument('--bit-mark', default = 440, help = 'Bit mark')
#parser.add_argument('--tail-mark', default = 440, help = 'Tail mark')
parser.add_argument('--tail-space', default = 9950, help = 'Tail space')
parser.add_argument('--hdr-space', default = 1700, help = 'Header space')
parser.add_argument('--bit-one-space', default = 1300, help = 'Bit one space')
parser.add_argument('--bit-zero-space', default = 440, help = 'Bit zero space')
#parser.add_argument('-s', '--bit-swap', choices = [0, 1], default = 1, help = 'Set bit swapping true or false')
args = parser.parse_args()

def createThresholds():
	global tailToHdr, hdrToOne, oneToZero

	tailToHdr = (args.tail_space + args.hdr_space) / 2
	hdrToOne = (args.hdr_space + args.bit_one_space) / 2
	oneToZero = (args.bit_one_space + args.bit_zero_space) / 2

	#print 'tailToZero: %d' % tailToZero
	#print 'hdrToOne: %d' % hdrToOne
	#print 'oneToZero: %d' % oneToZero

def getTokenType(sigLen):
	global tailToHdr, hdrToOne, oneToZero

	#print sigLen

	if (sigLen > args.tail_space + 3000):
		return 0 # IDLE
	elif (sigLen > tailToHdr):
		return 1 # Tail
	elif (sigLen > hdrToOne):
		return 2 # Header
	elif (sigLen > oneToZero):
		return 3 # One
	else:
		return 4 # Zero

def printData(data):
	#print data

	switch = data[5] & 0b1
	#hexData = '%0.2X' % data[5]
	#print hexData
	if (switch):
		print 'Power: ON'
	else:
		print 'Power: OFF'

	mode = data[5] >> 4
	if (mode == 0):
		print 'Mode: AUTO'
	elif (mode == 2):
		print 'Mode: DRY'
	elif (mode == 3):
		print 'Mode: COOL'
	elif (mode == 4):
		print 'Mode: HEAT'
	elif (mode == 6):
		print 'Mode: FAN'
	else:
		print 'Mode: <unknown>'

	temp = data[6] >> 1
	print 'Temperature: %d°C' % temp

def processLine(line):
	global strByte, cntBit, cntByte, data

	if processLine.first:
		processLine.first = False
		return

	[sigType, sigLen] = line.split()

	if (sigType == 'space'):
		tokenType = getTokenType(int(sigLen))

		if (tokenType == 0):
			print ''
			cntByte = 0
			printData(data)
		elif (tokenType == 1):
			sys.stdout.write('  ')
			data = []
			cntByte = 0
		elif (tokenType == 3):
			strByte += '1'
			cntBit += 1
		elif (tokenType == 4):
			strByte += '0'
			cntBit += 1

		#print cntBit

		if (cntBit >= 8):
			byte = int(strByte[::-1], 2)
			data.append(byte)
			hexByte = '%0.2X' % byte
			sys.stdout.write(hexByte)
			#sys.stdout.write('_')
			strByte = ''
			cntBit = 0
			cntByte += 1

			if (cntByte % 3 == 0):
				sys.stdout.write(' ')

processLine.first = True

# Init
createThresholds()
k = 0
strByte = ''
data = []
cntBit = 0
cntByte = 0

# Processing
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
