import RPi.GPIO as GPIO
import random as r
from time import sleep as s

def SwitchLED(all, who):
	for a in all:
		GPIO.output(a,False)
	
	GPIO.output(who,True)

def Flash(who, long):
	GPIO.output(who,False)
	s(long)
	GPIO.output(who,True)
	s(long)
	GPIO.output(who,False)
	s(long)

def TurnOnAll(all):
	for a in all:
		GPIO.output(a,True)

def RandomPos(c):
	dice = r.randint(0,2)

	if dice is 0:
		p = 1
	else:
		p = -1

	s = r.randint(0,c)

	return s,p
