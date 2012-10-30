#! /usr/bin/python

import smbus
import sys
import getopt
import time 
bus = smbus.SMBus(0)

address = 0x20 # I2C address of MCP23017
bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs 
#bus.write_byte_data(0x20,0x01,0x00) # Set all of bank B to outputs 



def set_led(data,bank):
  if bank == 1:
   bus.write_byte_data(address,0x12,data)
  else:
   bus.write_byte_data(address,0x13,data)
  return

# Handle the command line arguments
def main():
   a = 0
delay = 0.25   
add = 0

while True:
	d = bus.read_byte(0x20)	
	print "data: {0}".format(d)
	
	
	add = add +1

	r = bus.read_byte_data(0x20, add)
	print "{0}: {1}".format(add, r) 	

	time.sleep(delay)

	#green + yellow + red
	#set_led(7, 1)
	#time.sleep(delay)

	#yellow + red
	#set_led(6, 1)
	#time.sleep(delay)

	#red
	#set_led(4, 1)
	#time.sleep(delay)

	#all off
	set_led(8, 1)
	time.sleep(delay)
	
  
if __name__ == "__main__":
   main()

