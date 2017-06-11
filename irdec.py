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

k = 0
try:
	while True:
		data = sys.stdin.readline()

		if not data:
			break

		print data
		k = k + 1

except KeyboardInterrupt:
	sys.stdout.flush()
	pass

print "%s lines processed" % (k)

sys.exit(0)
