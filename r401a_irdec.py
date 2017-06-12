#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import argparse

parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, description = 'Panasonic R401A infrared communication decoder. Input: $ mode2 -d /dev/lirc0')
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

constHeader = [2, 32, 224, 4, 0, 0, 0, 6]
def checkHeaderOk(data):
	global headerOk

	#print data

	if (len(data) < len(constHeader)):
		#print 'len(data) < len(constHeader)'
		return False

	for i in range(0, len(constHeader)):
		if (data[i] != constHeader[i]):
			#print 'data[%d] != constHeader[%d]' % (i, i)
			return False

	return True

def printData(data):
	global headerOk

	#print data

	if (len(data) < 19):
		print 'len(data) < 19, aborting'
		return

	if (headerOk):
		print 'Header:\t\tOK'
	else:
		print 'Header:\t\tNot OK'
		sys.stdout.write('  Should be:\t')
		for i in range(0, len(constHeader)):
			hexByte = '%0.2X' % constHeader[i]
			sys.stdout.write(hexByte)
			if (i == 2 or i == 5):
				sys.stdout.write(' ')
		print ''

	checkSum = 0
	for i in range(0, 17):
		checkSum += data[i]
	checkSum = checkSum & 255

	if (checkSum == data[18]):
		print 'Checksum:\tOK'
	else:
		print 'Checksum:\tDiffers'
		print '  Calculated:\t%0.2X' % checkSum

	switch = data[5] & 0b1
	#hexData = '%0.2X' % data[5]
	#print hexData
	if (switch):
		print 'Power:\t\tON'
	else:
		print 'Power:\t\tOFF'

	mode = data[5] >> 4
	if (mode == 0):
		print 'Mode:\t\tAUTO'
	elif (mode == 2):
		print 'Mode:\t\tDRY'
	elif (mode == 3):
		print 'Mode:\t\tCOOL'
	elif (mode == 4):
		print 'Mode:\t\tHEAT'
	elif (mode == 6):
		print 'Mode:\t\tFAN'
	else:
		print 'Mode:\t\t<unknown>'

	temp = data[6] >> 1 # = Byte 7
	print 'Temperature:\t%d°C' % temp

	#profile = data[13]
	#if (profile == 16):
		#print 'Profile: NORMAL'
	#elif (profile == 17):
		#print 'Profile: BOOST'
	#elif (profile == 48):
		#print 'Profile: QUIET'
	#else:
		#print 'Profile: <unknown>'

	swing = data[8] & 0b1111
	if (swing == 15):
		print 'Swing:\t\tAUTO'
	elif (swing == 1):
		print 'Swing:\t\t1 (Horizontal)'
	elif (swing == 2):
		print 'Swing:\t\t2'
	elif (swing == 3):
		print 'Swing:\t\t3'
	elif (swing == 4):
		print 'Swing:\t\t4'
	elif (swing == 5):
		print 'Swing:\t\t5 (Vertical)'
	else:
		print 'Swing:\t\t<unknown>'

	fanSpeed = data[8] >> 4
	if (fanSpeed == 10):
		print 'Fan Speed:\tAUTO'
	elif (fanSpeed == 3):
		print 'Fan Speed:\t1 (Slowest)'
	elif (fanSpeed == 4):
		print 'Fan Speed:\t2'
	elif (fanSpeed == 5):
		print 'Fan Speed:\t3'
	elif (fanSpeed == 6):
		print 'Fan Speed:\t4'
	elif (fanSpeed == 7):
		print 'Fan Speed:\t5 (Fastest)'
	else:
		print 'Fan Speed:\t<unknown>'

def processLine(line):
	global strByte, cntBit, cntByte, data, headerOk

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
			data = []
		elif (tokenType == 1):
			sys.stdout.write('  ')
			headerOk = checkHeaderOk(data)
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
headerOk = False

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
