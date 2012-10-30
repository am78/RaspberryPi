#!/usr/bin/python

import RPi.GPIO as GPIO
from array import *
from time import sleep

class HD44780:

    def __init__(self, pin_rs=25, pin_e=4, pins_db=[24, 23, 22, 21]):
        print "init hd44780"
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        
    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        txt = text[:33]
        for char in txt:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)
    
    def scrollingText(self, txt):
		self.cmd(0x2)
		delay = 0.2
		c = len(txt)
		
		if (c < 16):
			self.cmd(0x2) #move cursor to start
			for char in tmp2: #self.cmd(ord(char),True) #print chars
				if char == '\n': self.cmd(0xC0) # next line
				else: self.cmd(ord(char),True)
			sleep(delay) #wait a bit
			return
		
		for offset in range(0, c-15):
			tmp = txt[offset:offset+16]
			self.cmd(0x2) #move cursor to start
			for char in tmp: #self.cmd(ord(char),True) #print chars
				if char == '\n': self.cmd(0xC0) # next line
				else: self.cmd(ord(char),True)
			sleep(delay) #wait a bit
		
		for offset in range(c-16, -1, -1): 
			tmp = txt[offset:offset+16]
			self.cmd(0x2) #move cursor to start
			for char in tmp: 
				#self.cmd(ord(char),True) #print chars
				if char == '\n': self.cmd(0xC0) # next line
				else: self.cmd(ord(char),True)
			sleep(delay) #wait a bit

    def scrollingText2(self, txt):
		#sleep(delay)
		delay = 0.2
		c = len(txt)
		tmp = txt.rjust(c+16)
		tmp = tmp.ljust(c+32)
		print tmp + "."
		
		c2 = len(tmp)
		for offset in range(0, c2-16):
			tmp2 = tmp[offset:c2]
			tmp2 = tmp2[:16]
			#print tmp2 + "."
			
			self.cmd(0x2) #move cursor to start
			for char in tmp2: self.cmd(ord(char),True) #print chars
			sleep(delay) #wait a bit
		
		for offset in range(c2-16, -1, -1): 						
			tmp2 = tmp[offset:c2]
			tmp2 = tmp2[:16]
			#print tmp2 + "."
			
			self.cmd(0x2) #move cursor to start
			for char in tmp2: self.cmd(ord(char),True) #print chars
			sleep(delay) #wait a bit


if __name__ == '__main__':
    lcd = HD44780()
    sleep(0.1)
    lcd.clear()
    sleep(0.1)
    #lcd.message("I'm Raspberry Pi\n  Take a byte!")
    #sleep(1)

    txt = "Nirvana - Smells like teen spirit"
    lcd.clear()
    sleep(0.1)
    while 1:
        lcd.scrollingText(txt)
