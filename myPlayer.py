#!/usr/bin/python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import subprocess
import os
from random import randint

MPFiles = []

#class player:
#	def __init__(this):
 #               os.execv(
		

#sox -t mp3 "http://updox.upd.edu.ph/stream/2/;stream.nsv" -t wav --input-buffer 80000 -r 22050 -c 1 - | sudo ./pi_fm_rds -ps test -rt 'Call 453589032' -freq 100.0 -audio -


def find_files(path):
        find_files=[]
        for root,dirs,files in os.walk(path):
                find_files+=[os.path.join(root,name) for name in files if name.endswith('.mp3')]
        return find_files



path = "/media/usb0/"

MPFiles+=find_files(path)
MPFiles+=find_files("/home/pi/")

print len(MPFiles)


Mfiles = list(MPFiles)

Mlen = len(Mfiles)

count = 1

CurrentSong = 0

i=0
        
while i<Mlen:  
	cs = MPFiles[i]
	r = randint(0,Mlen - 1)
	MPFiles[i] = MPFiles[r]
	MPFiles[r] = cs
	i += 1

Mlen = len(Mfiles)

count = 1

CurrentSong = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN) #vol up
GPIO.setup(6, GPIO.IN) #vol dn
GPIO.setup(13, GPIO.IN) #play
GPIO.setup(19, GPIO.IN) #shft
GPIO.setup(26, GPIO.IN) #mode

print GPIO.input(5)
print GPIO.input(6)
print GPIO.input(13)
print GPIO.input(19)
print GPIO.input(26)

player = subprocess.Popen(["mplayer", "-quiet", MPFiles[CurrentSong]] + MPFiles[CurrentSong:], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print "Started"

s = ""
i = 0


while s != "q":
	if GPIO.input(13)==0: 
		i = i + 1
		if i >= 10: 
			s = "q"
	else: 
		if i > 0:
			player.stdin.write("p")
		i=0

	if GPIO.input(6)==0: #vol down	
		player.stdin.write("/")

	if GPIO.input(26)==0: #vol up
        	player.stdin.write("*")

	if GPIO.input(5)==0: #next
        	player.stdin.write(">")


	sleep(0.2)  
	
	

player.stdin.write("q")
