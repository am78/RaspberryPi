#! /usr/bin/python

import smbus
import sys
import getopt
import time 
import mpd
from hd44780 import HD44780
from thread import start_new_thread, allocate_lock

bus = smbus.SMBus(0)

#init the lcd
lcd = HD44780()

global playing
playing = False

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
DEFAULT_VOLUME = 5

lock = allocate_lock()

#init the MPD client
client = mpd.MPDClient()
client.connect("localhost", 6600, timeout=10)
client.setvol(DEFAULT_VOLUME)
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

def getTitle():
	title = "----------------\n----------------"
	if (client.currentsong()):
		if ("title" in client.currentsong()):
			title = client.currentsong()["title"]	
			#title = title.replace(" - ", "\n")
	return title
   
def printTitle():
	playing = isPlaying()
	print client.currentsong()
	if (playing):
		title = getTitle()
		#printLCDScrolling(title)
		printlcd("\n" + title)
	else:
		printlcd("\n----------------")
	#printlcd("----------------\n----------------")

def togglePlay():
	global playing
	#currently playing?
	playing = isPlaying()
	if (playing): # --> pause
		client.setvol(0)
		client.pause()
		client.setvol(0)
		print "pause"
	else: # --> play
		client.setvol(0)
		client.play()
		client.setvol(DEFAULT_VOLUME)
		#get the played title
		title = getTitle()
		print "playing: {0}".format(title)
		
	#update playing status
	#if ("state" in client.status()):
	playing = client.status()["state"] == "play"
		
	print isPlaying()

def exit():
	#clear lcd
	lcd.clear()
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
	time.sleep(delay2)
	
def btn_2_3():	
	exit()
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

def printLCDScrolling(msg):
	lcd.clear()
	time.sleep(0.1)
	lcd.scrollingText(msg)
	#print "LCD: " + msg

def printlcd(msg):
	lcd.clear()
	time.sleep(0.1)
	lcd.message(msg)
	#print "LCD: " + msg
	
def init():
		
	printlcd("INIT...")

	#bus setup
	bus.write_byte_data(address, 0x12,  0) # write 0 to bus A
	bus.write_byte_data(address, 0x13,  7) # write 7 to bus B

	#turn yellow LED on
	set_led(YELLOW)

	#turn the green LED on when playing
	playing = isPlaying()
	if (playing):
		set_led(GREEN_YELLOW)

def updateLCD():
	while True:
		#print "updateLCD"
		playing = isPlaying()
		#client.status()["state"] == "play"
		#print client.currentsong()
		if (playing):
			title = getTitle()
			printLCDScrolling("\n" + title)
			#printlcd(title)
		else:
			printlcd("\n----------------")
		time.sleep(0.5)

def isPlaying():
	global playing
	#print client.status()
	#if ("state" in client.status()):
	#	playing = client.status()["state"] == "play"
	return playing
	
# Handle the command line arguments
def main():
	useScrollingText = False
	global playing	
	init()
	
	print client.status()
	if ("state" in client.status()):
		playing = client.status()["state"] == "play"
	
	currentTitle = getTitle()
	oldTitle = ""

	#update the LCD display using a thread
	if (useScrollingText) :
		start_new_thread(updateLCD,())
	
	#the main loop
	while True:
		rx12 = bus.read_byte_data(address, 0x12)
		rx13 = bus.read_byte_data(address, 0x13)
		#print "0x12: {1} \t \t 0x13: {0}".format(rx13, rx12) 
	
		#execute button actions
		buttons[rx13]()
		
		if (isPlaying()):
			set_led(GREEN_YELLOW)
		else:
			set_led(YELLOW)

		if (not useScrollingText):
			currentTitle = getTitle()
			if (currentTitle != oldTitle):
				printTitle()
				oldTitle = currentTitle
			
		#wait some time
		time.sleep(delay)
   
  
if __name__ == "__main__":
   main()

