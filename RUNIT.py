# Real Time Count TEST

import RPi.GPIO as GPIO
import random as r
from time import sleep as s
import backend as B

# HERE ARE ALL OF THE GPIO PINS THAT I USE FOR THE LEDs IN ORDER
lP = [19, 26, 12, 16, 21, 24, 23, 18, 22, 27, 17, 4]

# HERE ARE THE GPIO PINS FOR THE PLAYER 1 & 2 BUTTONS
button = [25, 20]

gameOver = 1
gP = 5 # Game Point
bIsDown = [False, False] # Button is Down

SSMM = [1000, 200000] # Step Speed Min Max
stepSpd = SSMM[gameOver]
waitFor = 1
buffer = 0
bSet = 3 # Buffer Set
lockInp = False #Lock Inputs
timer = stepSpd
stepCheck = None
cap = len(lP)-1
quit = [0,0]

points = [0,0]

step, polarity = B.RandomPos(cap)

GPIO.setmode(GPIO.BCM)

for a in lP:
	GPIO.setup(a, GPIO.OUT)
	GPIO.output(a, False)

GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
	while True:
		# THE STEP SPEED IS DETERMINED ON THE GAME MODE
		stepSpd = SSMM[gameOver]

		# WE COMPARE OUR CURRENT STEP TO OUR STEP CHECK TO TELL IF WE HAVE MOVED IN TIME OR NOT
		if step is not stepCheck:
	
			# THIS JUST CHECKS FOR IF PLAYERS ARE HOLDING THEIR BUTTONS & WANT TO QUIT
			if quit[0] > 100 and quit[1] > 100:
				B.TurnOnAll(lP)
				s(2)
				lockInp = False
				points = [0,0]
				gameOver = 1
				step, polarity = B.RandomPos(goal)

			B.SwitchLED(lP,lP[step])

			# IF EITHER PLAYER IS HOLDING THEIR BUTTON WHILE IN GAME, THEN LETS ADD TO THEIR HOLD TIME ELSE RESET IT
			for a in range(2):
				if gameOver is 0 and GPIO.input(button[a]) is 0:
					quit[a]+=1
				else:
					quit[a] = 0

		#IF GAME IS ACTIVE
		if gameOver is 0:

			# THIS IS ACTUAL GAMEPLAY FUNCTIONALITY
	    		if lockInp is False and buffer is 0:

				# PLAYER BUTTON PRESSES
				for a in range(2):
					if a is 0:
						goal = cap
					else:
						goal = 0

					# IF EITHER PLAYER PRESSES THE BUTTONS & WE KNOW ITS THEIR FIRST PRESS
					if GPIO.input(button[a]) is 0 and bIsDown[a] is False:

						bIsDown[a] = True

						if step is not goal:
	        					lockInp = True
							buffer = bSet
							s(waitFor)
							lockInp = False
							step, polarity = B.RandomPos(goal)
						else:
							points[a]+=1
							lockInp = True

							if points[a] >= gP:
								B.TurnOnAll(lP)
								for a in range(10):
									B.Flash(lP[step],.1)
								lockInp = False
								points = [0,0]
								gameOver = 1
								step, polarity = B.RandomPos(goal)
							else:
								for a in range(points[a]):
									B.Flash(lP[step],.3)
								step, polarity = B.RandomPos(goal)
								lockInp = False
					elif GPIO.input(button[a]) is 1:
						bIsDown[a] = False

		# IF GAME IS NOT ACTIVE
		else:
			if GPIO.input(button[0]) is 0 and GPIO.input(button[1]) is 0:
				B.TurnOnAll(lP)
				s(2)
				buffer = 4
				gameOver = 0

		# FIRST WE NEED TO GET A REFERENCE TO THE PREVIOUS STEP BEFORE WE CHANGE OUR STEP
		stepCheck = step

		# IF INPUTS ARE NOT LOCKED THEN PLAY TIMER
    		if not lockInp:
        		timer -=1

		# IF TIMER RUNS OUT THEN CHANGE STEP
		if timer is 0:
			if polarity is 1:
        			if step < cap:
                			step +=1
            			else:
                			polarity = -1
							step -=1
			elif polarity is -1:
				if step > 0:
					step -=1
				else:
					polarity = 1
					step +=1

			if buffer > 0:
				buffer -= 1
            		timer = stepSpd

finally:
	GPIO.cleanup()
