#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os; sys.dont_write_bytecode = True
import argparse
import dec_R401A

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

def dummyDecodeFrame(frameId, frameData):
	pass

def processLine(line):
	global strByte, cntBit, cntByte, frameId, frameData

	if processLine.first:
		processLine.first = False
		return

	[sigType, sigLen] = line.split()

	if (sigType == 'space'):
		tokenType = getTokenType(int(sigLen))

		if (tokenType == 0):
			print ''

			decodeFrame(frameId, frameData)

			frameData = []
			frameId = 0

			strByte = ''
			cntBit = 0
			cntByte = 0
		elif (tokenType == 1):
			sys.stdout.write(', ')

			decodeFrame(frameId, frameData)

			frameData = []
			frameId += 1

			strByte = ''
			cntBit = 0
			cntByte = 0
		elif (tokenType == 3):
			strByte += '1'
			cntBit += 1
		elif (tokenType == 4):
			strByte += '0'
			cntBit += 1

		#print cntBit

		if (cntBit >= 8):
			if (args.bit_swap == 1):
				strByte = strByte[::-1]

			byte = int(strByte, 2)
			frameData.append(byte)
			hexByte = '%0.2X' % byte
			sys.stdout.write(hexByte)
			#sys.stdout.write('_')
			strByte = ''
			cntBit = 0
			cntByte += 1

			if (cntByte % 4 == 0):
				sys.stdout.write(' ')

processLine.first = True

# Parse Arguments
parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, description = 'Infrared communication decoder. Usage: $ mode2 -d /dev/lirc0 | python irdec.py')
#parser.add_argument('--hdr-mark', default = 3500, help = 'Header mark')
#parser.add_argument('--bit-mark', default = 440, help = 'Bit mark')
#parser.add_argument('--tail-mark', default = 440, help = 'Tail mark')
parser.add_argument('-t', '--tail-space', type = int, default = 15000, help = 'Tail space')
parser.add_argument('-r', '--hdr-space', type = int, default = 1700, help = 'Header space')
parser.add_argument('-o', '--bit-one-space', type = int, default = 1300, help = 'Bit one space')
parser.add_argument('-z', '--bit-zero-space', type = int, default = 400, help = 'Bit zero space')
parser.add_argument('-s', '--bit-swap', type = int, choices = [0, 1], default = 1, help = 'Set bit swapping true or false')
parser.add_argument('-d', '--decoder', choices = ['R401A'], help = 'Set specific decoder. R401A .. Panasonic R401A inverter')
args = parser.parse_args()

decoderList = {
	'R401A' : dec_R401A.decodeR401aFrame,
}
decodeFrame = decoderList.get(args.decoder, dummyDecodeFrame)

# Init
createThresholds()
k = 0
frameData = []
frameId = 0
strByte = ''
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
