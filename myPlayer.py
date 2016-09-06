import RPi.GPIO as GPIO
from time import sleep
import subprocess
import os
from random import randint

Mfiles = []

path = "/media/usb0/"

files = os.listdir(path)
MPFiles = images = filter(lambda x: x.endswith('.mp3'), files); 
i=0


for mf in MPFiles:
	MPFiles[i] = path+mf
	i = i+1

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
		player.stdin.write("*")

	if GPIO.input(26)==0: #vol up
        	player.stdin.write("/")

	if GPIO.input(5)==0: #next
        	player.stdin.write(">")


	sleep(0.2)  
	
	

player.stdin.write("q")
