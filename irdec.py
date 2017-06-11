#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import argparse

parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, description = 'Input: $ mode2 -d /dev/lirc0')
parser.add_argument('--hdr-mark', default = 3500, help = 'Header mark')
parser.add_argument('--hdr-space', default = 1700, help = 'Header space')
parser.add_argument('--bit-mark', default = 440, help = 'Bit mark')
parser.add_argument('--bit-one-space', default = 440, help = 'Bit one space')
parser.add_argument('--bit-zero-space', default = 1300, help = 'Bit zero space')
parser.add_argument('--tail-mark', default = 440, help = 'Tail mark')
parser.add_argument('--tail-space', default = 9950, help = 'Tail space')
parser.add_argument('-t', '--detection-threshold', default = 300, help = 'Detection threshold')
parser.add_argument('-s', '--bit-swap', choices = [0, 1], default = 1, help = 'Set bit swapping true or false')
args = parser.parse_args()

def getFrameStart(data):
	global doFSM

	[sigType, sigLen] = data

	print "Frame start:"
	print sigType
	print sigLen

	doFSM = getDataBit

def getDataBit(data):
	global doFSM

	[sigType, sigLen] = data

	print "Data bit:"
	print sigType
	print sigLen

first = True
doFSM = getFrameStart

def processLine(line):
	global first

	data = line.split()

	if first:
		first = False
		return

	doFSM(data)

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

print "%s lines processed" % (k)

sys.exit(0)
