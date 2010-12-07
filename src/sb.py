##! /usr/bin/python



import cwiid, random, sys
from time import sleep
from subprocess import call

random.seed()

print "press 1+2 now"
w = cwiid.Wiimote()
w.rpt_mode = cwiid.RPT_CLASSIC


# just to show things are working, flick on a LED
w.led = 1

# Turn the guitar on (which masquerades as a classic controller)
w.rpt_mode = cwiid.RPT_CLASSIC


letters = {}


letters[0] = " "		# 00000  :-)
letters[1] = "a"		# 10000  :-)  
letters[2] = "e"		# 01000  :-)
letters[4] = "i"		# 00100  :-)
letters[8] = "o"		# 00010  :-)
letters[16] = "u"		# 00001  :-)
letters[3] = "t"		# 11000  :-)
letters[6] ="s"			# 01100  :-)
letters[12] = "r"		# 00110
letters[24] = "f"		# 00011
letters[5] = "h"		# 10100  :-)
letters[10] = "l"		# 01010
letters[20] = "v"		# 00101  :-)
letters[9] = "c"		# 10010  :-)
letters[18] = "k"		# 01001  :-)
letters[7] = "n"		# 11100  :-)
letters[14] = "g"		# 01110  :-)
letters[28] = "y"		# 00111  :-)
letters[13] = "d"		# 10110  :-)
letters[26] = "b"		# 01011  :-)
letters[11] = "p"		# 11010  :-)
letters[22] = "q"		# 01101  :-)
letters[25] = "j"		# 10011
letters[21] = "x"		# 10101  :-)
letters[15] = "m"		# 11110  :-)<
letters[30] = "w"		# 01111  :-)
letters[29] = "z"		# 10111



current_letter = ""
whammy_released = True
joystick_centered = True
next_letter_uppercase = True

while (1):

	letter_number = 0

	if w.state.has_key("classic"):
		state = w.state["classic"]["buttons"]
		whammy = w.state["classic"]["r"]  # range appears to be 15-26, with 16 as the default.
		joystick = w.state["classic"]["l_stick"] # center is around (32,32), 
		
		# first, check if we're actually getting a stroke (we dont want to do anything if there's no strum
		if ((state & 1) | (state & 16384)):
		
			# only act if the previous iteration of the loop had the strummer released (to stop lots of letters on one strum)
			if current_letter == "":
			
				# Calculate the letter being pressed. Number from 0 to 31.
				if state & 16:
					letter_number += 1
				if state & 64:
					letter_number +=2
				if state & 8:
					letter_number +=4
				if state & 32:
					letter_number +=8
				if state & 128:
					letter_number +=16
				
				
				
				if letters.has_key(letter_number) & (letter_number != current_letter):	
					letter = letters[letter_number]

						
					# 1 is an upstroke, and 16384 is a downstroke, if we choose to use this information later.	
					if (state & 1) | (state & 16384):
						if (next_letter_uppercase==True):
							letter = str.upper(letter)
							next_letter_uppercase = False
						#sys.stdout.write( letter )
						call ( ["/usr/bin/xdotool",  "type", letter] )
	
						
					w.led = random.randint(1,16)
					sys.stdout.flush()
					
					current_letter = letter_number
		else:
			# if the strum is just released, sleep to stop bounce and repeat characters
			if (current_letter != ""):
				sleep(0.075) 
			#reset the current letter to nothing, to allow repeat characters
			current_letter = ""

			
		
			# with no strum, but the first button held down, we change the behaviour of the stick to be arrow keys
			if (state & 16):
				
				# joystick deals with delete, Upper Case, comma and full stop
				if (joystick_centered == True) & (joystick[0] < 12 ):
					call ( ["/usr/bin/xdotool",  "key", "Left"] )
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[0] > 52 ):
					call ( ["/usr/bin/xdotool",  "key", "Right"] )
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[1] < 12 ):
					call ( ["/usr/bin/xdotool",  "key", "Down"] )
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[1] > 52 ):
					call ( ["/usr/bin/xdotool",  "key", "Up"] )
					joystick_centered = False				
				
				
				
			else:
				# joystick deals with delete, Upper Case, comma and full stop
				if (joystick_centered == True) & (joystick[0] < 12 ):
					call ( ["/usr/bin/xdotool",  "key", "BackSpace"] )
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[0] > 52 ):
					call ( ["/usr/bin/xdotool",  "type", ", "] )
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[1] < 12 ):
					call ( ["/usr/bin/xdotool",  "type", ".  "] )
					next_letter_uppercase = True
					joystick_centered = False
				
				if (joystick_centered == True) & (joystick[1] > 52 ):
					next_letter_uppercase = True
					joystick_centered = False
		
		
		if ( (joystick[0] > 28) & (joystick[0] < 36) ) &( (joystick[1] > 28) & (joystick[1] < 36) ):
			joystick_centered = True
			
			

		# whammy sends a carriage return
		if (whammy_released == True) & (whammy>20)  :
			#sys.stdout.write( "\n" )
			call ( ["/usr/bin/xdotool",  "key", "Return"] )
			next_letter_uppercase = True
			whammy_released = False
			
		if (whammy < 18):
			whammy_released = True
			

	else:
		# Wait for the wiimote to correctly configure itself
		sleep(0.5) 



