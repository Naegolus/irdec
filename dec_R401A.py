#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

def decodeR401aFrame(frameId, frameData):
	r401aHeader = [2, 32, 224, 4, 0, 0, 0, 6]

	#print (frameId, frameData)

	if (frameId == 0):
		decodeR401aFrame.headerOk = True

		if (len(frameData) < len(r401aHeader)):
			#print 'len(frameData) < len(r401aHeader)'
			decodeR401aFrame.headerOk = False

		for i in range(0, len(r401aHeader)):
			if (frameData[i] != r401aHeader[i]):
				#print 'frameData[%d] != r401aHeader[%d]' % (i, i)
				decodeR401aFrame.headerOk = False
	else:
		if (len(frameData) == 19):
			if (decodeR401aFrame.headerOk):
				print 'Header:\t\tOK'
			else:
				print 'Header:\t\tNot OK'
				sys.stdout.write('  Should be:\t')
				for i in range(0, len(r401aHeader)):
					hexByte = '%0.2X' % r401aHeader[i]
					sys.stdout.write(hexByte)
					if ((i + 1) % 4 == 0):
						sys.stdout.write(' ')
				print ''

			checkSum = 0
			for i in range(0, 17):
				checkSum += frameData[i]
			checkSum = checkSum & 255

			if (checkSum == frameData[18]):
				print 'Checksum:\tOK'
			else:
				print 'Checksum:\tNot OK'
				print '  Calculated:\t%0.2X' % checkSum

			switch = frameData[5] & 0b1
			#hexData = '%0.2X' % frameData[5]
			#print hexData
			if (switch):
				print 'Power:\t\tON'
			else:
				print 'Power:\t\tOFF'

			mode = frameData[5] >> 4
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

			temp = frameData[6] >> 1 # = Byte 7
			print 'Temperature:\t%d°C' % temp

			#profile = frameData[13]
			#if (profile == 16):
				#print 'Profile: NORMAL'
			#elif (profile == 17):
				#print 'Profile: BOOST'
			#elif (profile == 48):
				#print 'Profile: QUIET'
			#else:
				#print 'Profile: <unknown>'

			swing = frameData[8] & 0b1111
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

			fanSpeed = frameData[8] >> 4
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
		else:
			print 'Unknown frame, decoding aborted'
			print '  ID:\t%d' % frameId
			print '  Data:\t%s' % frameData
			print '  Len:\t%d' % len(frameData)

	return

decodeR401aFrame.headerOk = True
