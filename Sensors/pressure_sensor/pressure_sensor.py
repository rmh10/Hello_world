#!/usr/bin/python
# -*- coding: Latin-1 -*-
import os
import sys
from time import sleep
#import rpi.gpio as gpio
#import spidev
import binascii
import I2C_LCD_driver
import ad7705

#CE0  = 24
#MOSI = 19
#MISO = 21
#SCLK = 23

#RPI.GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(CS, GPIO.OUT)

display = I2C_LCD_driver.lcd()

#spi = spidev.SpiDev()
#spi.open(0,0)
#spi.max_speed_hz = 50000

def poll_sensor(channel):
    assert 0 <= channel <= 1
    
    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    r = spi.xfer2([1,cbyte,0])
    return((r[1] & 31) << 6) + (r[2] >> 2)

try:
    while True:
        adc = ad7705.AD770X()
        channel = 0
        adc.initChannel(channel)
        #channeldata = poll_sensor(channel)
        channeldata = adc.readADResultRaw(channel) 

        #voltage = round(((channeldata * 5000) / 1024),3)
        #pressure = round(((250/4000) * voltage) - (250/8000),2)
        voltage = adc.readVoltage(channel, 5)
        pressure = round(((250/4) * voltage) - (250/8),2)
        display.lcd_display_string('Pres: %.2fPsi   ' %pressure)
        print('Pressure    : {}'.format(pressure))
        print('Voltage (V) : {}'.format(voltage))
        print('Data        : {}/n'.format(channeldata))
        sleep(1) # sleep for 0.1 seconds

        #print('Recieved: 0x{0}'.format(binascii.hexlify(bytearray(resp))))

#except KeyboardInterrupt: # Ctrl+C pressed, so…
finally:
    #spi.close() # … close the port before exit
    print "/n All cleaned up."
    #end try
