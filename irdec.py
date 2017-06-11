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
	buff = ''
	while True:
		buff += sys.stdin.read(1)
		if buff.endswith('\n'):
			print buff[:-1]
			buff = ''
			k = k + 1
except KeyboardInterrupt:
	sys.stdout.flush()
	pass
print k

sys.exit(0)
