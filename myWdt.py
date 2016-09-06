import RPi.GPIO as GPIO
from time import sleep
import subprocess
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN) #power acc or bat

i = 0;
while 1:
	if GPIO.input(3) == 0:
		i = i + 1
		if i >= 20: 
			subprocess.call("shutdown")
			exit()
	else:
		i=0


	sleep(2.5)
	
