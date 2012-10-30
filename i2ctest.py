#! /usr/bin/python

import smbus
import sys
import getopt
import time 
import mpd

bus = smbus.SMBus(0)

GREEN = 1
YELLOW = 2
GREEN_YELLOW = 3
LED_OFF = 0

BTN1 = 1
BTN2 = 2
BTN3 = 4

address = 0x20 # I2C address of MCP23017
bus.write_byte_data(address,0x00,0x00) # Set all of bank A to outputs
bus.write_byte_data(address,0x01,0x01) # Set all of bank B to outputs 

delay = 0.05
delay2= 0.2

#init the MPD client
client = mpd.MPDClient()
client.connect("localhost", 6600, timeout=10)
client.setvol(90)
print (client.mpd_version)
#print (client.status())


def set_led(data):
	set_led2(data, 1)
	return

def set_led2(data,bank):
  if bank == 1:
   bus.write_byte_data(address,0x12,data)
  else:
   bus.write_byte_data(address,0x13,data)
  return

# Handle the command line arguments
def main():
   a = 0

def getTitle():
	return client.currentsong()["title"]
   
def togglePlay():
	#currently playing?
	playing = client.status()["state"] == "play"
	
	if (playing): # --> pause
		client.setvol(0)
		client.pause()	
		client.setvol(0)		
		print "pause"
	else: # --> play		
		client.setvol(0)
		client.play()
		client.setvol(90)
		#get the played title
		title = getTitle()
		print "playing: {0}".format(title)
	
def exit():
	#close MPD session etc
	client.stop()
	client.close()
	client.disconnect()
	#turn LEDs off
	set_led(LED_OFF)
	#quit the program
	print "quit"
	quit()
	
def next():
	client.next()
	print "next"
	
def prev():
	client.previous()
	print "prev"
   
def btn_1():
	prev()
	time.sleep(delay2)

def btn_2():
	togglePlay()
	time.sleep(delay2)
	
def btn_3():
	next()
	time.sleep(delay2)
	
def btn_1_2_3():	
	time.sleep(delay2)
	return

def btn_1_3():	
	time.sleep(delay2)
	return
	
def btn_1_2():
	exit()
	time.sleep(delay2)
	
def btn_2_3():	
	return
	time.sleep(delay2)

def no_btn():
	return
	#do nothing

buttons = { 0 : btn_1_2_3, 
			1 : btn_2_3,
			2 : btn_1_3,
			3 : btn_3,
			4 : btn_1_2,
			5 : btn_2,
			6 : btn_1, 
			7 : no_btn,
}


#bus setup
bus.write_byte_data(address, 0x12,  0) # write 0 to bus A
bus.write_byte_data(address, 0x13,  7) # write 7 to bus B

#turn yellow LED on
set_led(YELLOW)

#turn the green LED on when playing
playing = client.status()["state"] == "play"
if (playing):
	set_led(GREEN_YELLOW)	

#the main loop
while True:
	rx12 = bus.read_byte_data(address, 0x12)
	rx13 = bus.read_byte_data(address, 0x13)
	#print "0x12: {1} \t \t 0x13: {0}".format(rx13, rx12) 
	
	#execute button actions
	buttons[rx13]()
	
	playing = client.status()["state"] == "play"
	if (playing):
		set_led(GREEN_YELLOW)
	else:
		set_led(YELLOW)

	#wait some time
	time.sleep(delay)
	
  
if __name__ == "__main__":
   main()

