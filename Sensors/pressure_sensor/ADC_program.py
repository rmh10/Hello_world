#!/usr/bin/python
# -*- coding: Latin-1 -*-
import os
import sys
from time import sleep
#import rpi.gpio as gpio
#import i2c_lcd_driver
import spidev
import binascii

#CE0  = 24
#MOSI = 19
#MISO = 21
#SCLK = 23

#RPI.GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(CS, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode=1

try:
     while True:
         resp = spi.xfer([0x6000, 0x0000, 0x0000]) # transfer one byte
         print('Recieved: 0x{0}'.format(binascii.hexlify(bytearray(resp))))
         sleep(1) # sleep for 0.1 seconds
            #end while
#except KeyboardInterrupt: # Ctrl+C pressed, so…
finally:
    spi.close() # … close the port before exit
     #end try
