#!/usb/bin/python

from hd44780 import HD44780
from datetime import datetime
from time import sleep

lcd = HD44780()

def printlcd(msg):
	#lcd.clear()
	sleep(0.1)
	lcd.message(msg)
	print "LCD: " + msg

while True:
	delay = 0.2
	
	printlcd("test")	
	sleep(delay)
	
	printlcd(" test")	
	sleep(delay)
	
	printlcd("  test")	
	sleep(delay)
	
	printlcd("   test")	
	sleep(delay)
	
	printlcd("    test")	
	sleep(delay)
	
	printlcd("     test")	
	sleep(delay)