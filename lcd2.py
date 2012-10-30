#!/ust/bin/python

from hd44780 import HD44780
from datetime import datetime
from time import sleep
from thread import start_new_thread

lcd = HD44780()
sleep(0.1)
text = "Nirvana - Smells Like Teen Spirit"
def printlcd(msg):
	lcd.clear()
	sleep(0.1)
	lcd.message(msg)

def scrollingText():
	while True:
		lcd.scrollingText(text)
	

print "start thread..."
start_new_thread(scrollingText,())
print "thread started"
sleep(5)
text = "Metallica - Enter Sandman"

for i in range(0, 100):
	#print i
	sleep(1)