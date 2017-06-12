#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

r401aHeader = [2, 32, 224, 4, 0, 0, 0, 6]

def decodeR401aFrame(frameId, frameData):
	global r401aHeader

	#print (frameId, frameData)

	if (frameId == 1):
		decodeR401aFrame.headerOk = True

		if (len(data) < len(constHeader)):
			#print 'len(data) < len(constHeader)'
			decodeR401aFrame.headerOk = False

		for i in range(0, len(constHeader)):
			if (data[i] != constHeader[i]):
				#print 'data[%d] != constHeader[%d]' % (i, i)
				decodeR401aFrame.headerOk = False
	else:
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
